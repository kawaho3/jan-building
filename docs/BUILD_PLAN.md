# Build plan — evidence-driven roadmap

**All items below are planned and unchecked unless specifically documented as completed with commit/test evidence.** The target is reliable real-media editing, not a full commercial-suite clone in one sprint.

## Phase 0 — repository recovery, research, decision

- [ ] Identify and preserve any historical workspace elsewhere (other repo/zip/fork) before code import.
- [x] Audit target repository as documentation-only on 2026-11-19 (see CURRENT_STATE).
- [x] Document the two research priority references (OpenReel and FreeCut).
- [ ] Clone and pin both upstream SHAs; test build, lint, test and sample workflow on a compatible environment.
- [ ] Record detailed license/dependency/asset and security audit.
- [ ] Choose one base or original implementation via ADR. Assess whether an upstream fork/subtree/import is maintainable.
- [ ] Add actual project manifest/lockfile with pinned toolchain, first source tree, LICENSE/NOTICE policy.
- [ ] Add minimal CI that runs real install, lint, types, units, build; don't create empty green jobs.

**Exit gate:** clean clone produces a real app preview; source/provenance is documented; CI executes genuine tests.

## Phase 1 — end-to-end real media vertical slice (first priority)

- [ ] Local media import + metadata + supported-codec error handling.
- [ ] Video+audio playback and user-controlled seeking with stable AV clock.
- [ ] Timeline insert, trim, split and arrange with undo/redo.
- [ ] Versioned save/reopen, media references and relink UX.
- [ ] Export playable MP4 or supported alternative containing correct video + audio.
- [ ] Automated fixture: deterministic two-cut sequence with expected timing and decodeable output.
- [ ] Export matches preview source trims/layering; verify with ffprobe and frame/sample comparisons.
- [ ] Progress, cancellation, clean error handling, no source mutation.

**Exit gate:** a fresh clone with documented prerequisites can edit/save/reopen/export a real fixture, with CI evidence or clearly disclosed local GPU-specific checks.

## Phase 2 — creator-ready quality

- [ ] Multiple tracks, overlap/transitions, text/graphics.
- [ ] Audio fades, level/pan, waveforms, mixing and sync safeguards.
- [ ] Effects and keyframes with preview/export parity.
- [ ] Fast thumbnails, scrubbing, bounded cache and proxy generation.
- [ ] Autosave, crash recovery, stable project migration.
- [ ] User-facing keyboard shortcuts and accessible editing controls.
- [ ] Portable project bundle and error recovery.

**Exit gate:** suites pass with multiple codec/FPS/size fixtures; projects survive reloads; performance budgets documented.

## Phase 3 — advanced editor + desktop candidate

- [ ] Masking, color tools/LUT, motion/keyframe curves, compound/nested sequences.
- [ ] Scopes, multicam/proxy workflow research, speed ramps, caption import/export.
- [ ] Desktop shell ADR and platform-specific filesystem/codec/packaging smoke tests.
- [ ] Installer signing strategy, updater security and release artifact verification.
- [ ] Expanded media compatibility and large project benchmarks.

**Exit gate:** public beta with documented supported media matrix and reproducible release pipeline.

## Phase 4 — optional intelligent editing

- [ ] Versioned typed agent action API with preview, validate, user approval, and undo.
- [ ] Local/offline transcription, text-to-caption, scene detection, clip search where feasible.
- [ ] BYO model/endpoint optional; no required paid inference for editing.
- [ ] Guardrails against arbitrary file deletion, silent uploads, uncontrolled billable work.
- [ ] Benchmark quality, latency, resources, accessibility, cost, and data privacy.

**Exit gate:** AI outputs are editable, reversible, permission-scoped and tested; core editor runs without AI.

## Minimum PR sequence

1. docs/adr decision + reproducible foundation proof.
2. buildable app/CI baseline (with truthful README commands).
3. import/play/metadata.
4. timeline split/trim/undo.
5. save/reopen/relink.
6. export+audio+ffprobe and real fixture e2e.
7. regression/performance gate.
8. creator features, one tested slice at a time.

## Prioritization policy

P0: broken/corrupt output, destructive behavior, missing media, unbuildable repo, security.
P1: audio drift, wrong frame/timing, failure to reopen, unusable basic edits.
P2: creator usability and unsupported codecs with clear fallback.
P3: polish, AI and experimental professional tools.

No success claims without a link to real code and executable evidence. Keep this checklist in sync with issues/PRs and update checkbox only when verified.