# Research dossier — authoritative references

Research reviewed on 2026-11-19. Source facts below come from upstream repository README, package manifests, and GitHub metadata; **no upstream capabilities were tested in Jan Building**. This repository had no code at the audit.

## Exactly two priority study repositories

### 1. OpenReel Video — provisional primary foundation

Repository: https://github.com/Augani/openreel-video
Docs: https://github.com/Augani/openreel-video/blob/main/README.md
License declared by GitHub repository: **MIT**. Exact license, dependencies, bundled assets, and commit SHA must be pinned and verified prior to reuse.

Upstream reports a React/TypeScript monorepo with Zustand, WebCodecs, WebGPU, MediaBunny, Web Audio, and desktop support in development. It documents multitrack timeline, splitting/trimming, effects, compositing, audio, project operations, and exports. Package.json at review specified pnpm@11.7.0 and apps/*, packages/* workspaces, with scripts for dev, typecheck, test, lint, and build. Do not infer all marketing-list items are fully working on every system.

**Why primary:** closest initial architectural fit for an approachable browser-first creator editor with modular UI/core split. Best first investigation: *does a real user-media import -> edit -> project reopen -> export path work reliably, including audio?*

**Risks:** large codebase, rapid upstream change, version-specific dependencies, GPU/browser/media variability, and possible mismatch between documentation and actual tests. Desktop packaging may be less mature than browser runtime.

### 2. FreeCut — comparative architecture and workflow reference

Repository: https://github.com/walterlow/freecut
Docs: https://github.com/walterlow/freecut/blob/main/README.md
License declared by GitHub repository: **MIT** (verify full dependency/asset details).

Upstream reports browser-based editing with WebGPU/WebCodecs, OPFS, File System Access API, Web Workers, sequence/compound-clip editing, proxies, relinking, frame-aware composition, workspace-backed caches, audio tools, and export. Package.json at review specified npm@11.8.0 with development/build/test/verify scripts. It recommends modern Chrome/Edge; GPU test portability may vary.

**Why second:** useful for studying workspace persistence, proxy strategies, performance boundaries, advanced trimming tools, and automated headless media workflows, without requiring adoption of a second canonical editing engine.

**Risks:** hardware/browser limitations; storage permission complexity; advanced controls may add product scope too early; avoid transferring large components without API/semantics/license review.

## Priority comparison

| Criterion | OpenReel (study) | FreeCut (study) | Jan Building decision |
| --- | --- | --- | --- |
| Product UX | Browser creator editor + desktop direction | Browser-first advanced NLE | Start with approachable browser MVP |
| Repository structure | pnpm apps/packages monorepo | npm application-oriented repo | Pick one base; do not combine wholesale |
| Video pipeline | WebCodecs/WebGPU/MediaBunny advertised | WebGPU/WebCodecs + custom runtime advertised | Inspect code paths and exported files |
| Persistent media workspace | Must trace real implementation | OPFS/File System Access and relinking advertised | One versioned document + recoverable media references |
| Testing | Upstream scripts advertised | Extensive verify/headless scripts advertised | Run pinned commit's actual tests locally |
| Licensing | MIT declared | MIT declared | Respect full code, assets, and dependency licenses |
| Decision state | **Candidate**, not installed | **Reference**, not installed | First ADR remains provisional |

## Additional optional reference literature (not selected primary foundations)

These are **research leads** for particular subsystems; no assertion that they were part of the earlier missing 22-item inventory, and no integration approval. Before reuse inspect version, license, security, and compatibility:

- https://github.com/FFmpeg/FFmpeg — external media probe, encode/decode and container reference; assess LGPL/GPL build configuration.
- https://github.com/mltframework/mlt — media timeline/rendering reference for native workflows.
- https://github.com/mltframework/shotcut — mature desktop UX/MLT integration patterns.
- https://github.com/KDE/kdenlive — non-linear desktop workflow and proxy references.
- https://github.com/mifi/lossless-cut — lossless trimming and codec/container edge cases.
- https://github.com/remotion-dev/remotion — programmatic composition concepts; check its actual licensing/terms before commercial reuse.
- https://github.com/Vanilagy/mediabunny — browser media processing library and export/mux reference.
- https://github.com/w3c/webcodecs — evolving specification/issues; browser support varies.
- https://github.com/gpuweb/gpuweb — WebGPU standard and interoperability discussions.
- https://github.com/olive-editor/olive — alternative desktop editor architecture (evaluate activity).

No source has been downloaded or included in Jan Building by this documentation commit.

## Research method for the next developer

1. Capture UTC date, repo URL, exact commit SHA, language/stack/package manager, license and THIRD_PARTY notices.
2. Compare critical workflows using the same legally distributable 10-second video+audio fixture.
3. Record build, test, media probe, hardware/browser, memory/performance and failure behavior.
4. Test import, scrub, split/trim, undo, save, close, reopen, relink, export, cancel, audio sync, and portability.
5. Score each candidate on reproducibility, UX, code ownership, render correctness, extension cost, platform fit, and licensing.
6. Make a written selection with alternatives rejected and reversible integration plan. Add that evidence to the ADR.

## Earlier missing research

An earlier project discussion referenced a 22-item study file (21 GitHub and 1 Hugging Face). **That original list was not in the audited target repository, and its exact entries are not available in this audit.** Do not call the ten optional links above a reconstruction of the missing file. If the original file is recovered later, compare and merge source-by-source, retaining provenance.