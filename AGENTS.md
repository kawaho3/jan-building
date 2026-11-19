# AGENTS.md — instructions for Codex and AI coding agents

Read **README.md**, **docs/CURRENT_STATE.md**, **docs/START_HERE.md**, **docs/ARCHITECTURE_AND_WORKSPACE.md**, **docs/BUILD_PLAN.md**, and **docs/TEST_PLAN.md** before editing.

## Mission

Build a truly usable independent video editor, not a static mockup or promotional UI. CapCut-like discoverability plus increasingly professional workflows is a long-term target. The live repo began with only a README; never assume that OpenReel, FreeCut, or historical files are already present.

## Non-negotiable behavior

1. Inspect the checked-out filesystem and Git history *first*. Record branch, commit, directories, executable scripts, workflow files, and test results. If files are missing, say so.
2. Never report an upstream capability as a capability of Jan Building. Distinguish **verified now**, **upstream-reported**, **planned**, and **blocked**.
3. Preserve existing user-owned work. No destructive reorganizations, unrequested deletions, force-pushes, secrets exposure, or rewriting history. If an old workspace appears elsewhere, inventory and compare before moving it.
4. Prefer one coherent editing/document/rendering architecture. Do not paste two complete editors together. Study OpenReel and FreeCut; use an ADR before importing third-party code.
5. Copy source only after checking exact version, attribution, license texts, dependencies, assets, patents/codecs where applicable, and security posture. Never assume an upstream MIT license covers third-party weights, media, fonts, or assets.
6. Prioritize an end-to-end vertical slice: **import actual file -> view/play -> add to timeline -> trim -> save -> reload -> export -> compare**. Reject placeholder MP4 output and frontend-only fake controls.
7. Keep CPU-only developer operations possible where feasible; test feature-detected WebGPU/WebCodecs paths on supported browsers/hardware.
8. Don't require paid APIs, hosted services, plugins, or credentials for the primary local workflow. AI may be opt-in later.
9. For each code change: specify what changed, tests actually executed, results, evidence links, limitations, and exact next steps. Do not invent numbers or claim unrun tests passed.
10. Update docs and acceptance checklists when a feature is implemented. Add a regression test before marking a defect closed.

## First executable task

- Inspect the repo and verify that it is documentation-only.
- Read docs/adr/0001-foundation-selection.md; compare the two candidate reference projects at pinned commit SHAs.
- Create an issue/ADR or PR justifying the chosen foundation and its license/provenance.
- Make the **smallest independently runnable editor** with verified local instructions, then implement the required vertical slice in ordered stages.
- Keep the root README truthful as the implementation evolves.

## Design invariants

- Timeline state has a versioned schema, stable IDs, rational time/frame-rate handling, and deterministic actions with undo/redo.
- Media files remain separate from project metadata; never serialize giant media blobs directly into timeline JSON.
- Preview, export, thumbnailing, and audio processing consume the same canonical clip timing and effect model.
- Imports and exports are cancellable and report explicit errors; crash recovery and integrity checks are required before release.
- No external upload without clear, user-initiated consent; protect local projects.
- Performance and accessibility are part of acceptance criteria, not optional polish.

## Pull-request handoff format

Summary / files changed; before-and-after behavior; commands and exact outcomes; media fixtures and test evidence; licenses/provenance; risks; TODOs with issues. Ask for review for architecture changes rather than silently replacing subsystems.

Useful entry points: docs/START_HERE.md, docs/BUILD_PLAN.md, docs/HANDOFF.md.