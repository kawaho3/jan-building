#!/usr/bin/env python3
"""A reversible selected-weight capability probe, not model training.

Default mode only inspects the GGUF. --run performs baseline -> zero final
normalization -> restore, restarting Jan's worker between every phase.
Only one F32 tensor is backed up; the model is never copied in full.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import secrets
import select
import signal
import struct
import subprocess
import time
import urllib.error
import urllib.request

BASE = Path(__file__).resolve().parent
DEFAULT_MODEL = BASE.parent / "jan-benchmark/models/Jan-code-4b-Q4_K_M.gguf"
DEFAULT_WORKER = BASE.parent / "jan-test/squashfs-root/usr/lib/Jan/resources/bin/jan-llama-worker"
EXPECTED_SHA = "6f9bcb1fdced9494fc477af6ca7e6c0e203540da5343d370eb89c1391b3644e0"
MODEL_ID = "jan-weight-probe"
FORMATS = {0: "B", 1: "b", 2: "H", 3: "h", 4: "I", 5: "i", 6: "f", 7: "?", 10: "Q", 11: "q", 12: "d"}


def sha256(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def atomic_bytes(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as handle:
        os.chmod(temporary, 0o600)
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def save_json(path, value):
    atomic_bytes(path, (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode())


def inspect_gguf(path):
    """Parse GGUF v3 metadata/tensor directory without reading weight arrays."""
    path = Path(path).resolve()
    size = path.stat().st_size
    with path.open("rb") as handle:
        def read(n):
            result = handle.read(n)
            if len(result) != n:
                raise ValueError("Truncated GGUF")
            return result

        def number(fmt):
            return struct.unpack("<" + fmt, read(struct.calcsize("<" + fmt)))[0]

        def string(keep=True):
            length = number("Q")
            if length > size - handle.tell():
                raise ValueError("GGUF string extends beyond the file")
            if keep:
                return read(length).decode("utf-8")
            handle.seek(length, 1)

        def value(kind, keep=False):
            if kind in FORMATS:
                return number(FORMATS[kind])
            if kind == 8:
                return string(keep)
            if kind == 9:
                element_type, count = number("I"), number("Q")
                if element_type in FORMATS:
                    n = count * struct.calcsize("<" + FORMATS[element_type])
                    if n > size - handle.tell():
                        raise ValueError("GGUF array extends beyond the file")
                    handle.seek(n, 1)
                else:
                    for _ in range(count):
                        value(element_type)
                return {"count": count, "element_type": element_type}
            raise ValueError(f"Unknown GGUF metadata type {kind}")

        if read(4) != b"GGUF":
            raise ValueError("Not a GGUF file")
        version, count, metadata_count = number("I"), number("Q"), number("Q")
        if version != 3 or count > 100000 or metadata_count > 100000:
            raise ValueError("Probe requires a sane GGUF v3 tensor directory")
        metadata = {}
        for _ in range(metadata_count):
            key, kind = string(), number("I")
            item = value(kind, key in {"general.architecture", "general.name"})
            if kind != 8 or key in {"general.architecture", "general.name"}:
                metadata[key] = item
        tensors = []
        for _ in range(count):
            name, dimensions = string(), number("I")
            if not 1 <= dimensions <= 4:
                raise ValueError("Invalid tensor dimensions")
            shape = [number("Q") for _ in range(dimensions)]
            tensors.append({"name": name, "shape": shape, "type": number("I"), "relative_offset": number("Q")})
        alignment = metadata.get("general.alignment", 32)
        if not isinstance(alignment, int) or alignment <= 0 or alignment > 1048576:
            raise ValueError("Invalid GGUF alignment")
        data_offset = ((handle.tell() + alignment - 1) // alignment) * alignment
        selected = [tensor for tensor in tensors if tensor["name"] == "output_norm.weight"]
        if len(selected) != 1:
            raise ValueError("Expected exactly one output_norm.weight tensor")
        tensor = selected[0]
        if tensor["type"] != 0 or len(tensor["shape"]) != 1:
            raise ValueError("Probe only edits a one-dimensional F32 final norm")
        tensor["elements"] = math.prod(tensor["shape"])
        tensor["bytes"] = tensor["elements"] * 4
        tensor["offset"] = data_offset + tensor["relative_offset"]
        if tensor["bytes"] > 1048576 or tensor["offset"] + tensor["bytes"] > size:
            raise ValueError("Selected tensor is too large or outside the model")
        handle.seek(tensor["offset"])
        raw = read(tensor["bytes"])
        values = struct.unpack("<" + "f" * tensor["elements"], raw)
        if not all(math.isfinite(v) for v in values):
            raise ValueError("Final norm contains non-finite values")
        tensor["minimum"] = min(values)
        tensor["maximum"] = max(values)
        output = next((t for t in tensors if t["name"] == "output.weight"), None)
        output = output or next((t for t in tensors if t["name"] == "token_embd.weight"), None)
        vocabulary = output["shape"][-1] if output else metadata["tokenizer.ggml.tokens"]["count"]
        return {"model": str(path), "model_bytes": size, "gguf_version": version,
                "architecture": metadata.get("general.architecture"), "name": metadata.get("general.name"),
                "tensor_count": count, "vocabulary_size": vocabulary, "tensor": tensor}


def ensure_unmapped(model):
    """Refuse to edit weights still mapped by a visible live process."""
    model = str(Path(model).resolve())
    readers = []
    for entry in Path("/proc").glob("[0-9]*"):
        try:
            if model in (entry / "maps").read_text():
                readers.append(int(entry.name))
        except (PermissionError, ProcessLookupError, FileNotFoundError):
            continue
    if readers:
        raise RuntimeError(f"Model remains memory-mapped by processes {readers}; stop them first")


def file_identity(handle):
    details = os.fstat(handle.fileno())
    return {"device": details.st_dev, "inode": details.st_ino}


@contextmanager
def model_lock(model):
    """An inode lock also serializes runs using different paths/hard links."""
    with Path(model).open("rb") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield file_identity(handle)


def write_tensor(model, tensor, raw, expected_identity, expected_size):
    if len(raw) != tensor["bytes"]:
        raise ValueError("Tensor backup has an unexpected length")
    ensure_unmapped(model)
    with Path(model).open("r+b", buffering=0) as handle:
        # Check the opened object, then write through that same descriptor.
        # A same-sized replacement at this path must never receive old weights.
        if file_identity(handle) != expected_identity:
            raise RuntimeError("Model file identity changed; refusing tensor write")
        if os.fstat(handle.fileno()).st_size != expected_size:
            raise RuntimeError("Model file size changed; refusing tensor write")
        handle.seek(tensor["offset"])
        if handle.write(raw) != len(raw):
            raise IOError("Short tensor write")
        os.fsync(handle.fileno())


def restore_pending(manifest_path, locked_identity):
    # Every recovery entry point, including startup/--restore-only, finishes
    # restoration before honoring ordinary termination signals again.
    handlers = {sig: signal.signal(sig, signal.SIG_IGN) for sig in (signal.SIGINT, signal.SIGTERM)}
    try:
        return _restore_pending(manifest_path, locked_identity)
    finally:
        for sig, handler in handlers.items():
            signal.signal(sig, handler)


def _restore_pending(manifest_path, locked_identity):
    manifest_path = Path(manifest_path)
    if not manifest_path.exists():
        return None
    state = json.loads(manifest_path.read_text())
    if state.get("model_identity") != locked_identity:
        raise RuntimeError("Recovery model identity differs from the locked model; refusing write")
    if state["state"] == "restored":
        return state
    model = Path(state["model"])
    backup = Path(state["backup_path"]).read_bytes()
    if hashlib.sha256(backup).hexdigest() != state["backup_sha256"]:
        raise RuntimeError("Recovery backup checksum mismatch")
    if model.stat().st_size != state["model_bytes"]:
        raise RuntimeError("Recovery target size changed")
    # A killed parent closes worker stdin; allow its normal shutdown to finish.
    deadline = time.monotonic() + 25
    while True:
        try:
            ensure_unmapped(model)
            break
        except RuntimeError:
            if time.monotonic() >= deadline:
                raise
            time.sleep(0.25)
    write_tensor(model, state["tensor"], backup, state["model_identity"], state["model_bytes"])
    restored_sha = sha256(model)
    if restored_sha != state["original_sha256"]:
        raise RuntimeError("Restored tensor but full model checksum differs; retain recovery artifacts")
    state.update(state="restored", restored_sha256=restored_sha, restored_at_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    save_json(manifest_path, state)
    return state


@contextmanager
def engine(worker, model, folder, phase):
    preset = folder / f"{phase}.preset.ini"
    preset.write_text(f"[*]\nfit = off\nthreads = 2\nthreads-batch = 2\nctx-size = 512\nparallel = 1\ncache-ram = 0\njinja = true\n\n[{MODEL_ID}]\nmodel = {model}\nn-gpu-layers = 0\nload-on-startup = false\n")
    token = secrets.token_urlsafe(32)
    environment = dict(os.environ, JAN_LLAMA_API_KEY=token, OMP_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    log = (folder / f"{phase}.engine.log").open("w")
    process = subprocess.Popen([str(worker), "--preset", str(preset), "--port", "0", "--models-max", "1", "--slot-cache-mib", "0"],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log, text=True, env=environment)
    try:
        deadline = time.monotonic() + 45
        boot = None
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(f"Worker exited {process.returncode}; inspect {log.name}")
            ready, _, _ = select.select([process.stdout], [], [], 0.5)
            if ready:
                line = process.stdout.readline()
                try:
                    item = json.loads(line)
                    if "port" in item:
                        boot = item
                        break
                except json.JSONDecodeError:
                    pass
        if boot is None:
            raise RuntimeError("No worker readiness JSON")
        save_json(folder / f"{phase}.worker.json", boot)
        def post(path, payload):
            request = urllib.request.Request(f"http://127.0.0.1:{boot['port']}{path}",
                data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})
            try:
                with opener.open(request, timeout=180) as response:
                    return json.load(response)
            except urllib.error.HTTPError as error:
                raise RuntimeError(f"HTTP {error.code}: {error.read().decode()}") from error
        post("/models/load", {"model": MODEL_ID})
        yield post
    finally:
        if process.stdin:
            process.stdin.close()
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
        if process.stdout:
            process.stdout.close()
        log.close()


def sample(worker, model, folder, phase):
    request = {"model": MODEL_ID, "prompt": "def add(a, b):\n    return a", "n_predict": 1,
               "temperature": 0, "seed": 42, "n_probs": 5, "post_sampling_probs": False,
               "cache_prompt": False, "stream": False}
    save_json(folder / f"{phase}.request.json", request)
    started = time.monotonic()
    with engine(worker, model, folder, phase) as post:
        response = post("/completion", request)
    ensure_unmapped(model)
    save_json(folder / f"{phase}.response.json", response)
    probabilities = response.get("completion_probabilities", [])
    if len(probabilities) != 1 or len(probabilities[0].get("top_logprobs", [])) < 5:
        raise RuntimeError("Engine did not return one token with five presampling logprobs")
    first = probabilities[0]
    top = [{key: item[key] for key in ["id", "token", "logprob"]} for item in first["top_logprobs"]]
    return {"phase": phase, "seconds_including_load": round(time.monotonic() - started, 3),
            "content": response.get("content"), "sampled_token_id": first["id"], "top_logprobs": top}


def interrupted(signum, _frame):
    raise InterruptedError(f"Received signal {signum}; restoring selected weights")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--worker", type=Path, default=DEFAULT_WORKER)
    parser.add_argument("--artifacts", type=Path, default=BASE / "artifacts")
    parser.add_argument("--expected-sha", default=EXPECTED_SHA)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--run", action="store_true", help="Run the reversible baseline/edit/restore probe")
    mode.add_argument("--baseline-only", action="store_true", help="Load/sample the original model without editing")
    mode.add_argument("--restore-only", action="store_true", help="Recover a pending tensor backup and verify its full model checksum")
    args = parser.parse_args()
    args.model, args.worker, args.artifacts = args.model.resolve(), args.worker.resolve(), args.artifacts.resolve()
    args.artifacts.mkdir(parents=True, exist_ok=True)
    with model_lock(args.model) as model_identity, (args.artifacts / ".probe.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = args.artifacts / "recovery.json"
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, interrupted)
        if args.run or args.restore_only:
            restored = restore_pending(manifest, model_identity)
            if args.restore_only:
                print(json.dumps(restored or {"state": "no_pending_backup"}, indent=2))
                return
        info = inspect_gguf(args.model)
        save_json(args.artifacts / "inspection.json", info)
        print(json.dumps(info, indent=2), flush=True)
        if not (args.run or args.baseline_only):
            return
        actual_sha = sha256(args.model)
        if actual_sha != args.expected_sha:
            raise RuntimeError("Original model SHA256 differs from the expected official file")
        ensure_unmapped(args.model)
        folder = args.artifacts / time.strftime("run-%Y%m%dT%H%M%SZ", time.gmtime())
        folder.mkdir()
        results = {"capability_probe_only": True, "training_performed": False,
                   "original_sha256": actual_sha, "worker_sha256": sha256(args.worker),
                   "inspection": info, "samples": []}
        results["samples"].append(sample(args.worker, args.model, folder, "baseline"))
        if args.baseline_only:
            save_json(folder / "results.json", results)
            print(json.dumps(results, indent=2), flush=True)
            return
        tensor = info["tensor"]
        with args.model.open("rb") as handle:
            if file_identity(handle) != model_identity:
                raise RuntimeError("Model file identity changed before tensor backup")
            handle.seek(tensor["offset"])
            original = handle.read(tensor["bytes"])
        backup = folder / "selected-tensor.backup.bin"
        atomic_bytes(backup, original)
        state = {"state": "prepared", "model": str(args.model), "model_bytes": info["model_bytes"],
                 "model_identity": model_identity,
                 "tensor": tensor, "original_sha256": actual_sha, "backup_path": str(backup),
                 "backup_sha256": hashlib.sha256(original).hexdigest()}
        save_json(manifest, state)
        try:
            write_tensor(args.model, tensor, bytes(tensor["bytes"]), model_identity, info["model_bytes"])
            state["state"] = "patched"
            save_json(manifest, state)
            results["modified_sha256"] = sha256(args.model)
            results["samples"].append(sample(args.worker, args.model, folder, "zero-final-norm"))
        finally:
            # Ignore a second ordinary termination signal while restoring. SIGKILL
            # cannot be caught; the fsynced backup supports next-run recovery.
            for sig in (signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, signal.SIG_IGN)
            recovery = restore_pending(manifest, model_identity)
            results["restoration"] = {key: recovery[key] for key in ["state", "restored_sha256", "restored_at_utc"]}
            save_json(folder / "results.json", results)
            for sig in (signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, interrupted)
        results["samples"].append(sample(args.worker, args.model, folder, "restored"))
        baseline, patched, restored = results["samples"]
        p = [item["logprob"] for item in patched["top_logprobs"]]
        uniform_expected = -math.log(info["vocabulary_size"])
        uniform = max(p) - min(p) < 1e-6 and abs(p[0] - uniform_expected) < 1e-4
        restored_matches = baseline["sampled_token_id"] == restored["sampled_token_id"] and baseline["top_logprobs"] == restored["top_logprobs"]
        changed = baseline["top_logprobs"] != patched["top_logprobs"]
        results["checks"] = {"weights_changed_model_hash": results["modified_sha256"] != actual_sha,
                             "output_distribution_changed": changed, "zero_norm_top5_uniform": uniform,
                             "uniform_logprob_expected": uniform_expected,
                             "original_full_checksum_restored": recovery["restored_sha256"] == actual_sha,
                             "restored_baseline_matches": restored_matches}
        results["passed"] = all(value for key, value in results["checks"].items() if key != "uniform_logprob_expected")
        save_json(folder / "results.json", results)
        save_json(args.artifacts / "latest-results.json", results)
        print(json.dumps(results, indent=2), flush=True)
        if not results["passed"]:
            raise SystemExit("Capability probe did not meet all checks; original model was restored")


if __name__ == "__main__":
    main()
