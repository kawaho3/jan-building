# Verified repository state — 2026-11-19

Repository: https://github.com/kawaho3/jan-building
Audit commit: 1e5b743c75198514952b9b452c65d6b2a7667aaf (initial commit)
Audited branch: main

## Facts observed through GitHub

| Area | Observation at audit |
| --- | --- |
| Repository visibility | Public |
| Default branch | main |
| Root contents | README.md only |
| README contents | # jan-building |
| Application source | None |
| Package manager lockfile or manifest | None |
| Tests / reproducible build | None |
| CI workflow files | None |
| Documentation or study-repository .txt | None |
| Open pull requests | None found |
| Open issues | None found |
| Branches | main only |
| Releases | None |

GitHub Actions workflow collection was not independently retrieved, but no .github directory or workflow files appeared in the complete root listing. The root had only one file. After this documentation commit the root contains guidance files, still no runnable app unless implementation is added later.

## Historical context versus current code

Earlier project discussions described a professional video editor built around an OpenReel-style workspace, and mentioned editor/apps/web, editor/apps/desktop, editor/packages/core, editor/packages/ui, and editor/packages/agent. One earlier report mentioned a substantial test suite and a study inventory of 22 entries (21 GitHub repositories, one Hugging Face resource). **These are historical discussion claims; none of the related files, tests, or inventory appeared in the audited live repository.** They must not be presented as currently checked-in or verified.

If historical code is available in another repository, local archive, fork, or branch, **do not overwrite it**. First inventory, compare hashes/licenses, run existing tests and preserve its history. The initial GitHub history observed here contained only the initial commit.

## Confidence legend

- **Verified:** directly inspected in target GitHub repository as of audit.
- **Upstream-reported:** published in external upstream READMEs, without Jan Building integration or local tests.
- **Proposed:** our suggested architecture, behavior, or milestones.
- **Historical/unverified:** remembered from an earlier chat but absent from current live repository.

## Immediate blockers

1. No app to start or test.
2. No chosen/pinned foundation implementation.
3. No maintained project manifest or actual directory conventions.
4. No reproducible sample-media test suite or export path.
5. No verified rebuildable installer.
6. Old 22-item study file is not recoverable from this repository; do not fabricate it.

Next: follow START_HERE, select the foundation via ADR, establish CI, and demonstrate the first real media vertical slice. Preserve this audit as the baseline rather than continually rewriting history.