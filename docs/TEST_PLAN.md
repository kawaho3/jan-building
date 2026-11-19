# Test and validation strategy

**Current status:** no application or test runner was present in Jan Building at the 2026-11-19 audit. These are future acceptance criteria, not a report of passing tests.

## Core testing layers

1. Unit: rational timebase and FPS conversion, clip in/out, split/ripple/trim/move invariants, overlap and track ordering, command validation, undo/redo, schema migrations.
2. Integration: real file metadata, thumbnail/waveform, media missing/relink, preview graph, multitrack audio, project save/reload, cancellation, job lifecycle.
3. Browser end to end: keyboard/mouse/touch interactions, import, timeline edit, save, restart, export, download, clear failure recovery, focus/ARIA.
4. Output validation: ffprobe stream/codec/container/duration, decode full artifact with FFmpeg, compare known frame checksums or perceptual tolerances, validate audio content and timestamps.
5. GPU/codec support: feature detection on Windows/macOS/Linux and supported Chrome/Edge versions; CPU/headless fallback; device-loss behavior; missing encoder errors.
6. Performance: seek latency, dropped preview frames, memory/storage usage, 4K and long timeline workloads, proxy/cache hit rate, export speed and cancellation.
7. Security/privacy: malformed media, path traversal during project import, unsafe assets, project migrations, file permission revocation, no unexpected outbound transfers.

## Reproducible media fixture suite

Use self-created/generated or permissively licensed assets only, with checksums in a manifest. Suggested synthetic scenarios:

- Ten-second test clip 1920x1080, 30 fps, moving frame counters/timecode, clear color changes and stereo tone/metronome.
- Fractional-frame-rate test (30000/1001 fps) and short 24 fps fixture.
- 48 kHz audio test with known click offsets to measure AV sync.
- VFR input (if supported), vertical 9:16, still-image clip, mixed sample rates.
- Unsupported codec, corrupt file, missing media, zero-length clip and no-audio source.
- Nested edit/transition/effect examples once implemented.

Example future CLI checks (commands require an actual artifact; none exists now):

~~~sh
ffprobe -v error -show_format -show_streams -of json path/to/export.mp4
ffmpeg -v error -i path/to/export.mp4 -f null -
~~~

A zero process exit does not prove that preview and export match; compare expected frames/time/audio properties too.

## Phase 1 golden workflow

Given a 10-second clip with a visual frame counter and audible marker:
1. Import and add to timeline.
2. Remove a known segment by trim/split, move one part, and undo/redo.
3. Save, close and reopen; prove frame-accurate clip positions.
4. Export and decode all video/audio; assert expected duration and marker position.
5. Run twice and compare stable metadata and toleranced frame/audible characteristics.
6. Repeat with storage permission loss and unsupported export codec; verify user-readable errors.
7. Confirm input file is byte-identical before and after.

## CI policy

- Fast PR gate: install from lockfile, format/lint, typecheck, unit/integration, build, dependency/security checks and deterministic media tests when portable.
- Scheduled/manual media matrix: Chromium/WebGPU/WebCodecs tests on known device/driver; release smoke tests for each packaged OS.
- Make optional hardware tests explicit. A skipped GPU test is **not** a pass.
- Artifacts: test logs, browser version, codec capability probe, checksum/metadata and small sample exports (observe license/privacy).
- Never claim a historical upstream test count is Jan Building's test count; only current repo command outputs count.

## Release-blocking conditions

- Project corruption/data loss; output with missing audio; inconsistent timebase; silently failed export; source overwrite; undocumented cloud upload; invalid license attribution; installer that cannot run; unsupported device without a clear error.

The first person who adds code must update this file with exact test scripts, fixture provenance, thresholds and CI URLs.