#!/usr/bin/env python3
"""Exercise probe safeguards on tiny synthetic files, never the real model."""
import hashlib
import json
import os
from pathlib import Path
import signal
import struct
import tempfile

import gguf_probe as probe

BASE = Path(__file__).resolve().parent


def text(value):
    raw = value.encode()
    return struct.pack("<Q", len(raw)) + raw


def make_fixture(path):
    def tensor(name, shape, offset):
        return text(name) + struct.pack("<I", len(shape)) + struct.pack("<" + "Q" * len(shape), *shape) + struct.pack("<IQ", 0, offset)
    header = b"GGUF" + struct.pack("<IQQ", 3, 2, 2)
    header += text("general.architecture") + struct.pack("<I", 8) + text("fixture")
    header += text("general.name") + struct.pack("<I", 8) + text("probe fixture")
    header += tensor("output_norm.weight", [2], 0) + tensor("token_embd.weight", [2, 8], 32)
    header += bytes((-len(header)) % 32)
    original = struct.pack("<ff", 1.25, -2.5)
    path.write_bytes(header + original + bytes(24) + bytes(64))
    return original


def prepare(folder, model, original, info, identity):
    backup = folder / "backup.bin"
    probe.atomic_bytes(backup, original)
    state = {"state": "prepared", "model": str(model), "model_bytes": model.stat().st_size,
             "model_identity": identity, "tensor": info["tensor"], "original_sha256": probe.sha256(model),
             "backup_path": str(backup), "backup_sha256": hashlib.sha256(original).hexdigest()}
    manifest = folder / "recovery.json"
    probe.save_json(manifest, state)
    return manifest, backup, state


def main():
    checks = {}
    destination = BASE / "selfcheck"
    destination.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination) as scratch:
        folder = Path(scratch)
        model = folder / "fixture.gguf"
        original = make_fixture(model)
        info = probe.inspect_gguf(model)
        assert info["tensor"]["bytes"] == 8 and info["vocabulary_size"] == 8
        checks["fixture_directory_parsed"] = True
        with probe.model_lock(model) as identity:
            alias = folder / "hardlink.gguf"
            os.link(model, alias)
            try:
                with probe.model_lock(alias):
                    raise AssertionError("Concurrent hard-link lock was accepted")
            except BlockingIOError:
                checks["hardlink_concurrent_lock_rejected"] = True

            manifest, backup, state = prepare(folder, model, original, info, identity)
            probe.write_tensor(model, info["tensor"], bytes(8), identity, state["model_bytes"])
            assert probe.sha256(model) != state["original_sha256"]
            restored = probe.restore_pending(manifest, identity)
            assert restored["state"] == "restored" and probe.sha256(model) == state["original_sha256"]
            checks["mutation_restored_full_sha"] = True

            state["state"] = "prepared"
            probe.save_json(manifest, state)
            backup.write_bytes(bytes(8))
            before = probe.sha256(model)
            try:
                probe.restore_pending(manifest, identity)
                raise AssertionError("Corrupt backup was accepted")
            except RuntimeError as error:
                assert "checksum mismatch" in str(error)
            assert probe.sha256(model) == before
            checks["corrupt_backup_rejected_before_write"] = True
            backup.write_bytes(original)

            # Verify recovery's own signal mask, rather than the caller's mask.
            saved_write = probe.write_tensor
            def interrupted_write(*args):
                os.kill(os.getpid(), signal.SIGTERM)
                return saved_write(*args)
            probe.write_tensor = interrupted_write
            probe.restore_pending(manifest, identity)
            probe.write_tensor = saved_write
            assert probe.sha256(model) == before
            checks["recovery_completed_during_sigterm"] = True

            # Replace the pathname while the old inode remains locked.
            state["state"] = "prepared"
            probe.save_json(manifest, state)
            replacement = folder / "replacement.gguf"
            replacement.write_bytes(bytes([0xA5]) * state["model_bytes"])
            replacement_sha = probe.sha256(replacement)
            os.replace(replacement, model)
            try:
                probe.restore_pending(manifest, identity)
                raise AssertionError("Same-size replacement was overwritten")
            except RuntimeError as error:
                assert "identity changed" in str(error)
            assert probe.sha256(model) == replacement_sha
            checks["same_size_replacement_rejected_on_opened_fd"] = True

        with probe.model_lock(model) as replacement_identity:
            try:
                probe.restore_pending(manifest, replacement_identity)
                raise AssertionError("Stale manifest was accepted for a new inode")
            except RuntimeError as error:
                assert "identity differs" in str(error)
            assert probe.sha256(model) == replacement_sha
            checks["stale_recovery_identity_rejected"] = True
    checks["real_model_never_written"] = True
    probe.save_json(destination / "results.json", checks)
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
