# Jan weight-space experiments

This repository starts with a bounded CPU capability test for direct edits to
Jan-Code-4B Q4_K_M weights. It checks that the runtime responds to a deliberate
parameter change and that restoring the original bytes restores its behavior.
It does not train the model or claim improved coding accuracy.

## First experiment

`gguf_probe.py` uses Jan v0.8.8's bundled llama.cpp worker and the official
`janhq/Jan-code-4b-gguf` checkpoint. Both downloads are pinned and verified.

1. Load the original model and record one token's presampling log probabilities.
2. Stop the worker, back up the 10,240-byte F32 `output_norm.weight` tensor, and
   zero that tensor.
3. Start a fresh worker and check for the expected uniform output distribution.
4. Stop the worker, restore the original tensor, and verify the full original
   model SHA256.
5. Reload and check that the original token and probabilities are reproduced.

The probe keeps a small durable backup and recovery manifest before editing.
It holds a model-inode lock, checks file identity before writes, and restores
weights after ordinary failures or termination. `--restore-only` recovers an
interrupted run; supply the same `--model` and `--artifacts` paths used by that run.

## Run

The GitHub Actions workflow runs on Ubuntu 24.04 with standard CPU hardware,
read-only repository permissions, and a 30-minute job limit. A relevant push on
`codex/jan-weight-space-probe*` triggers the test. Manual dispatch is available
after the workflow exists on the repository's default branch.

For a new local runtime with at least 8 GiB free:

```sh
python3 bootstrap.py --root work/runtime
python3 gguf_probe.py \
  --model work/runtime/models/Jan-code-4b-Q4_K_M.gguf \
  --worker work/runtime/application/squashfs-root/usr/lib/Jan/resources/bin/jan-llama-worker \
  --artifacts results/probe --run
```

Python 3.11+ and curl are sufficient. Existing verified assets can be reused;
see `python3 bootstrap.py --help`. No full model copy is made for the edit.
Actions artifacts contain small metrics and logs, excluding model weights and
binary tensor backups. See [WORKFLOW.md](WORKFLOW.md) for download and artifact
details, and `python3 selftest_probe.py` for small synthetic safety checks.

## Observed coding limitations to improve

`baseline_results.json` records an initial small coding evaluation of this exact
quantized checkpoint. Each answer was generated once and tested without repairs.

| Problem | Local checks passed | Whole problem |
|---|---:|---|
| Two Sum | 209/209 | Pass |
| Longest Substring Without Repeating Characters | 316/316 | Pass |
| Coin Change | 264/264 | Pass |
| Trapping Rain Water | 315/315 | Pass |
| Burst Balloons | 0/184 | Fail: array indexing exception |
| Tiling a Rectangle with the Fewest Squares | 43/169 | Fail: incorrect recurrence and special cases |

An original inspection-span problem combined a battery budget, a per-badge
occurrence cap, and cost/earliest-start tie rules. The model passed 904 of 1,018
completed small checks and failed 114, including a supplied example. It updated
the best cost without updating the answer indices. Its quadratic enumeration
then exhausted a 30-CPU-second limit on the first 100,000-entry stress case;
six stress checks remained uncompleted.

The first improvement target is generalization to new constraint combinations:
correct tie handling and linear-time window algorithms. Later evaluation should
use held-out problem families and seeds, retain the successful baseline tasks as
regression checks, and compare unchanged prompts and sampling settings. The
selected-tensor capability probe is an infrastructure control for that work.
These few problems do not establish a universal difficulty ceiling.

## Resources

The current Codex workspace has a 2-CPU quota, 8 GiB RAM, no GPU, and about 2 GB
free disk with this checkpoint already installed. Small selected-weight edits
fit that setup. The original full-precision checkpoint alone is approximately
8.82 GB, so a full training plan needs a separately sized environment.

Official sources: [Jan model](https://huggingface.co/janhq/Jan-code-4b-gguf),
[Jan release](https://github.com/janhq/jan/releases/tag/v0.8.8),
[GitHub runner specifications](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).
