# Proposed architecture and workspace

**Status: proposed only. None of these directories existed at the verified audit.** Choose/pin the actual upstream foundation before authoring a manifest or copying source.

## Core architecture rule

Use one canonical, versioned **project document**, one authoritative **timeline/time model**, and one render/export semantic model. UI and AI issue typed editing commands; they do not secretly mutate an unrelated copy of timeline state. Preview and export must interpret the same effect graph, source trims, layer ordering, transitions, and audio envelopes.

## Proposed repository layout

~~~text
jan-building/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  docs/
    START_HERE.md
    CURRENT_STATE.md
    PRODUCT_REQUIREMENTS.md
    ARCHITECTURE_AND_WORKSPACE.md
    RESEARCH_AND_REFERENCES.md
    BUILD_PLAN.md
    TEST_PLAN.md
    SECURITY_AND_LICENSING.md
    HANDOFF.md
    adr/
  apps/
    web/                 # Browser UI, preview host, import flows
    desktop/             # Later, only after reliable browser MVP
  packages/
    project-schema/      # Versioned document types, migrations, validation
    timeline-core/       # Time model, commands, deterministic edits, undo/redo
    media-core/          # Media metadata, decoding abstraction, proxies
    render-core/         # Effects, compositing, shared preview/export contracts
    audio-core/          # Audio timing, mixing, meters, envelope graph
    ui/                  # Shared accessible controls, shortcuts
    agent/               # Optional AI command adapter; no required API
  tests/
    fixtures/            # Licensed or generated small test media
    e2e/                 # Browser and exported-artifact verification
    perf/                # Playback/render benchmarks and budgets
  scripts/               # Reproducible setup/test/probe/packaging scripts
  .github/workflows/     # CI once code and test commands actually exist
  third_party/           # Only if imported with full license/provenance
~~~

These names are a target architecture, **not** a demand to reorganize an adopted upstream project immediately. If OpenReel is selected, begin from its actual monorepo and adapt with minimal disruption; use a documented mapping between its real paths and the long-term boundaries above. Avoid speculative abstractions until tests justify them.

## Document and time

- Schema: version, project ID, sequence settings, asset references/checksums, tracks, clip instances, effects, keyframes, audio, and migration history.
- Use integer timestamps/rational frame rates or other explicitly defined exact timebase; avoid cumulative floating-point drift.
- Stable command API for insert, trim, split, ripple, move, undo/redo with invariant checks.
- Clip source in/out differs from timeline placement; preserve both.
- Save editable project JSON/DB and separately managed media; support relinking missing source media.
- Autosave via transactional snapshots/journal, validated recovery and migration.

## Processing boundaries

1. **Media ingestion:** permissions, metadata, codec probing, thumbnail and waveform tasks, source checksum, cache.
2. **Timeline core:** deterministic edit and sequence/time calculations.
3. **Preview:** decoded frames + effects + synchronized audio clock; quality-scaled GPU path with graceful feature detection.
4. **Export:** same timeline model, deterministic progress/cancel/error; mux valid container with audio, color, and timestamps.
5. **Storage:** browser IndexedDB/OPFS and file handles only after compatibility testing; user-controlled project files for portability. Desktop storage is an adapter, not a second document format.
6. **Optional AI:** propose typed commands via validation and undo; cannot mutate files or upload media behind user consent.

## Browser/Desktop decisions

- First optimize for Chromium with WebCodecs and WebGPU where available; test CPU/Canvas fallback and explain unsupported cases.
- Don't assume H.264/H.265, ProRes, or system encoders are available on every device. Probe and present supported export profiles at runtime.
- Desktop shell (Tauri/Electron/etc.) is a later ADR after measurable requirements for filesystem access, native codecs, and installation. Don't package an unreliable editor.
- Offload expensive work to workers; bound caches and handle GPU device-loss and storage quota errors.

## Interface contracts to define after selecting foundation

- Project schema validation + migration tests.
- MediaReader metadata/openFrame/readAudio with cancellation, lifecycle and error contracts.
- RenderFrame(sequence, timestamp, quality) and RenderAudio(time range) semantics for preview/export agreement.
- ExportJob request, supportedProfiles, progress, cancel, result artifact/probe metadata.
- Command transaction, validation, undo/redo, serialized audit trail.

Record compatibility assumptions and version boundaries in ADRs. Keep any external editor as a research dependency until a reproducible end-to-end baseline is demonstrated.