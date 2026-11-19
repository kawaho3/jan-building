# Product vision and requirements

## Identity and target

Working name: **Jan Building**. Goal: a user-owned, independently branded video editing product suitable for creators who want the accessible flow of CapCut plus a pathway to advanced capabilities associated with Premiere Pro and DaVinci Resolve. This comparison defines UX goals, not technical compatibility or feature parity. Final brand, company ownership, commercial license, platforms, and distribution strategy require owner decisions.

## Principles

- **Real edits:** user actions affect real media and exports, not demo-only state.
- **Local-first:** ordinary import/edit/save/export works without accounts, subscriptions, or hosted inference.
- **Predictable:** a saved project has stable semantics across reloads and application versions.
- **Cross-platform direction:** browser first for minimal friction; desktop packaging after a verified editing engine.
- **Approachable and scalable:** novice-friendly defaults, keyboard shortcuts, and progressive disclosure of professional tools.
- **Privacy:** source files never leave the device except with explicit user action.
- **Accessibility:** usable keyboard navigation, visible focus states, labels, and non-color-only status.

## Release tiers (proposed; unimplemented)

### Minimum useful editor (M0/M1)

- Select local video/audio/image; detect metadata; provide readable failure for unsupported codecs.
- Media bin and thumbnail/waveform generation; timeline with at least video and audio.
- Play/pause, seek, split, trim, move clips, snap, simple cut, undo/redo.
- Maintain correct source time offsets and track layering.
- Save versioned project document and media references; reopen after restarting app.
- Export correct video and audio at at least one validated resolution/codec combination.
- Cancel/export-progress/error handling and fixture-based proof.
- Keyboard shortcuts and core accessibility.

### Strong creator editor (later)

- Multitrack effects, text/captions, image overlays, transitions and compositing.
- Keyframes, speed curves, masks, chroma key, basic color correction, LUT handling.
- Audio gain/pan, fading, mixing, loudness check, waveform editing.
- Proxies, media relinking, frame caching, background jobs, autosave/recovery.
- Export presets, custom frame rates, subtitles and metadata handling.
- Stable project compatibility and performance targets from realistic footage.

### Professional growth (much later)

- More sophisticated color scopes, proxy workflows, multicam/nested sequences, conform/relink, higher-bit-depth processing, collaborative review, plugin interfaces, professional interchange and desktop-native media pipelines.
- Optional locally running AI assistants for transcription, subtitles, scene detection, reframing, cleanup, search, and timeline operations, behind a capability-adapter interface.
- Mobile UI is an additional product and performance effort, not guaranteed by a web UI.

## Scope exclusions for the first implementation

No fake editor with only toolbar buttons; no claims of parity with commercial products; no required paid generative AI; no unsupported GPU/codec promise; no mandatory cloud upload; no two competing timelines/renderers pasted together.

## Acceptance at product level

An independent contributor should be able to clone, build, import a provided test media fixture, make a known cut, save, reopen, and export; the export should be decodable, match expected duration/frames, contain the expected audio, and not corrupt originals. A beautiful preview without this flow does not satisfy the first milestone.

## Risks to manage

Codec/container availability differs by browser/OS; WebGPU availability varies; large-file memory pressure; file permissions and stale media handles; audio/video clock drift; GPU device loss; cross-device project portability; content licensing; storage quota; undo state corruption; broken exports. See TEST_PLAN.md and SECURITY_AND_LICENSING.md.