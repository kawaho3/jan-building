# Start here — onboarding for a new developer

**Read this before changing code.** You do not need access to earlier ChatGPT conversations.

## 1. Understand what is being built

Jan Building is a proposed independently branded video editor: convenient import, intuitive trimming, accurate multitrack timeline, project save/reopen, faithful preview, dependable export, and later professional effects/audio/color, desktop packaging, and optional AI. It is **not currently implemented** in this repository. See PRODUCT_REQUIREMENTS.md.

## 2. Verify your exact checkout

~~~sh
git clone https://github.com/kawaho3/jan-building.git
cd jan-building
git branch --show-current
git log -5 --oneline
git ls-files
git status --short
~~~

At the 2026-11-19 audit there was only a tiny README; this handoff commit adds documentation. **There is no npm install / pnpm dev step to run in Jan Building yet.** Don't misrepresent commands from the study repos as commands for this project.

## 3. Set up a cost-conscious research workspace (separate clones)

Suggested prerequisites: Git; current supported Node.js LTS; Corepack/pnpm only for the OpenReel reference; npm for FreeCut; latest Chrome or Edge with WebCodecs and where supported WebGPU; FFmpeg CLI for independently inspecting fixture output. A usable GPU can improve preview but test capability detection and CPU/Canvas fallbacks. Do not commit credentials, real customer media, or large model weights.

~~~sh
mkdir jan-research
cd jan-research
git clone https://github.com/Augani/openreel-video.git
git clone https://github.com/walterlow/freecut.git
cd openreel-video
git rev-parse HEAD
corepack enable
pnpm install --frozen-lockfile
pnpm typecheck
pnpm test
pnpm build
~~~

These are **upstream OpenReel research commands**, not Jan Building commands. Confirm the Node and pnpm versions against that repository's exact pinned package.json and lockfile before installing. Pin the checked SHA and record actual outcomes; do not assume tests pass.

FreeCut evaluation in a separate clone:

~~~sh
cd ../freecut
git rev-parse HEAD
npm ci
npm run test:run
npm run build
npm run verify
~~~

These are **upstream FreeCut commands** (the verify gate may require Chromium/headless test prerequisites). Run only on a machine compatible with its packageManager and browser requirements. FreeCut documents a modern Chromium browser and WebGPU/WebCodecs/OPFS/File System Access dependency. Some GPU-specific tests may not be portable to hosted CI.

## 4. Make the architectural choice before copying

Use docs/adr/0001-foundation-selection.md. Study **exactly two priority editors**: OpenReel as the provisional initial candidate; FreeCut as comparison and targeted pattern source. Measure startup, real file import, scrubbing, project persistence, deterministic export, and platform support. Investigate licenses and nested dependencies. Record reproducible evidence and choose **one** canonical edit/document/render pipeline. Do not bulk-merge their source trees.

## 5. First real product milestone

Prove on your own branch using legally usable test media:

1. Import a video with audio.
2. Add it to a timeline with correct source in/out and frame rate.
3. Scrub, play, split, and trim it.
4. Save the project, close it, reopen it, and verify media links.
5. Export a file containing the intended video and audio.
6. Inspect output with ffprobe and visually compare frames and audio sync against preview.
7. Re-run after a fresh clone and clean install; capture exact steps.
8. Add tests and CI, then update README and roadmap status.

Prioritize reliable behavior before advanced UI, AI effects, cloud services, or dozens of toggles.

## 6. Where should things live?

See ARCHITECTURE_AND_WORKSPACE.md for a **proposed** apps/packages/test/docs split. The proposal is *not* a list of existing directories. Document the final structure after the foundation decision, then keep this guide synchronized.

## 7. How to hand work to another developer

Provide the exact commit, platform/runtime/OS, install steps, failing/passing commands, test fixture checksums, screenshots or sample exports, accepted decisions, open issues, and the next single smallest task. Follow HANDOFF.md and AGENTS.md. A new contributor must be able to progress without private chat history or paid external services.