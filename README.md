# Jan Building — independent professional video editor (planning and research)

**Project status: planning / documentation only. There is no runnable editor in this repository as of 2026-11-19.**

Jan Building is the working repository for a proposed independently branded, local-first video editor. The historical product brief is to combine the ease of CapCut with progressively more capable workflows associated with DaVinci Resolve and Adobe Premiere Pro. This is a product ambition, **not a claim of parity** or existing functionality.

## Start here

1. [New developer / AI-agent onboarding](docs/START_HERE.md)
2. [Verified repository audit](docs/CURRENT_STATE.md)
3. [Product vision and requirements](docs/PRODUCT_REQUIREMENTS.md)
4. [Architecture and workspace design](docs/ARCHITECTURE_AND_WORKSPACE.md)
5. [Research and exactly two priority references](docs/RESEARCH_AND_REFERENCES.md)
6. [Build roadmap and acceptance gates](docs/BUILD_PLAN.md)
7. [Validation and test strategy](docs/TEST_PLAN.md)
8. [Licensing, privacy, and security rules](docs/SECURITY_AND_LICENSING.md)
9. [Developer handoff and current blockers](docs/HANDOFF.md)
10. [Architecture decision record](docs/adr/0001-foundation-selection.md)
11. [AI coding-agent instructions](AGENTS.md) and [contribution guide](CONTRIBUTING.md)

## Project at a glance

- **Product direction:** edit real video and audio with a responsive multitrack timeline, reliable project persistence, reproducible previews, and export.
- **Primary study foundation (candidate, not integrated):** [Augani/openreel-video](https://github.com/Augani/openreel-video).
- **Second, independent study reference:** [walterlow/freecut](https://github.com/walterlow/freecut).
- **Preferred first release:** an offline-first browser prototype, followed by a desktop packaging decision after end-to-end media editing works.
- **No paid API needed for the core editor.** AI-assisted enhancements must be optional and must not block ordinary editing.
- **Ownership:** this repo is the product workspace. Upstream repositories remain separate projects; copying requires license and provenance review.

## What works today?

This repository currently contains **documentation only**. No package.json, application source, media engine, tests, desktop build, export workflow, or CI configuration existed at the verified initial audit. The documentation commit does not change that fact.

Do not run imaginary setup commands in this repository. To begin implementation, follow the selection and baseline-validation instructions in [START_HERE](docs/START_HERE.md) and record the first real working commands after the chosen code is imported.

## Contribution standard

Every feature claim must be backed by a reproducible test, screenshot/screencast where relevant, and exact commit. Projects must reopen intact; preview and exported output must agree on timing, transforms, and effects. See [CONTRIBUTING.md](CONTRIBUTING.md).

*Audit date: 2026-11-19. Historical research and suggested design are intentionally separated from live repository facts.*