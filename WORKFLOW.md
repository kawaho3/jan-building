# GitHub Actions execution

The workflow and probe scripts live at the repository root. If the experiment
is moved into a subdirectory, update the workflow command paths and push-path
filters together.

The workflow uses `ubuntu-24.04`, read-only repository permissions, a 30-minute
timeout, and two CPU threads. It runs only by manual dispatch or a relevant-file
push to a branch matching `codex/jan-weight-space-probe*`. It does not install
PyTorch, require a GPU, cache models, or upload model weights.

`bootstrap.py` checks available disk before any download (8 GiB minimum by
default), downloads the official Jan v0.8.8 AppImage and the revision-pinned
Jan-Code-4B Q4_K_M model, and verifies both exact byte counts and SHA256 hashes.
AppImage extraction does not need FUSE. The worker runs directly; no desktop
graphics dependencies are installed. Python 3.11+ and curl are required and are
provided by the selected runner image.

Runtime assets live under `$RUNNER_TEMP`, outside the artifact source tree.
`gguf_probe.py --run` performs baseline, selected F32 final-normalization ablation,
and restoration. The ordinary-error recovery step calls `--restore-only`; a
hard runner timeout may prevent cleanup, but only the disposable runner's
downloaded model is involved. This is a selected-weight capability check, not
training or fine-tuning.

`collect_artifacts.py` stages only small JSON/JSONL/CSV/Markdown/text/log files
from `results/`. It excludes model/binary weight extensions, backup names,
runtime directories, symbolic links, files larger than 2 MiB, and total content
beyond 25 MiB. Artifacts are retained for seven days. Recovery manifests contain
paths and checksums; the original tensor backup is a binary and is excluded.

Official action tags were resolved to immutable commit SHAs through GitHub's
repository metadata; provenance is recorded in `action-pins.json`:

- `actions/checkout` v7.0.1: `3d3c42e5aac5ba805825da76410c181273ba90b1`
- `actions/upload-artifact` v7.0.2: `cf430e030ddbb5b0abf93d22962f4752f3646cd9`

Local checks used only tiny fixture files: asset hash/size acceptance and
rejection, artifact exclusions, Python compilation, CLI help, and workflow YAML
structural validation. Large assets were not downloaded again.
