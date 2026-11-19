# Contributing to Jan Building

Jan Building currently has a documented product plan, not a runnable application. The first code contribution must establish a verified reproducible baseline; see [START_HERE](docs/START_HERE.md).

## Before coding

- Review the two primary study projects in [RESEARCH_AND_REFERENCES](docs/RESEARCH_AND_REFERENCES.md).
- Read the architecture decision record and record a version/commit and license check for any imported source.
- Open a focused issue or describe the problem and measurable acceptance criteria in your PR. Do not create unreviewable mega-commits.
- Use a branch such as feat/import-workflow or fix/export-timing; never force-push main.

## Local development

Current repository: clone and read documentation. There is **no runnable app setup command** yet.

~~~sh
git clone https://github.com/kawaho3/jan-building.git
cd jan-building
git status
find . -maxdepth 3 -type f | sort
~~~

The proposed workspace is documented in docs/ARCHITECTURE_AND_WORKSPACE.md. It is not an existing directory listing. Once implementation begins, lock the package manager/runtime versions and add an actual install, dev, test, build, and export-smoke command here.

## Coding and architecture expectations

- Strict TypeScript for the browser UI and domain contracts when that stack is adopted.
- Keep rendering, audio, document, media I/O, timeline editing, and UI responsibilities separated.
- Do not make UI state the sole source of truth for the editable project.
- Avoid flaky wall-clock tests; use fixture clocks and deterministic media.
- Respect browser security, codec availability, file permissions, and hardware feature detection.
- Put fixtures under test fixtures with known copyright status; do not commit personal user media.
- Include attribution and third-party notices for any reused source.

## PR checklist

- [ ] Real user-facing behavior and known limitations described accurately
- [ ] Relevant unit, integration, and media end-to-end tests added/updated
- [ ] Install/build/typecheck/lint/tests executed, or blocked commands explained
- [ ] Sample-media import/save/reopen/export evidence included when applicable
- [ ] Performance, accessibility, privacy, and undo/redo impact considered
- [ ] License/dependency/security review completed for added packages/assets
- [ ] Docs/BUILD_PLAN.md and README status updated if milestone advanced

Treat upstream README claims as hypotheses until reproduced locally. Code review focuses first on determinism, preservation of source media, correct rendered output, and recovery from errors.