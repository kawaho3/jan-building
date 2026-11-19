# Complete handoff — how to resume this project without earlier chats

## Verified snapshot

Date: 2026-11-19.
Repo: https://github.com/kawaho3/jan-building
Default branch: main.
Original baseline SHA: 1e5b743c75198514952b9b452c65d6b2a7667aaf.
Observed starting contents: only README.md, containing # jan-building.
No editor, lockfile, test setup, study file, or real CI was present. This documentation commit adds the handoff; it does not implement the editor.

## Product brief

Build an independently branded, accessible, local-first professional video editor. Historical target: friendly CapCut-like experience progressing toward advanced non-linear editing functions. Implement actual video/audio manipulation, project save/reopen, and validated export, not UI simulations.

## Research decisions carried forward

Exactly two priority upstream references:

1. **Augani/openreel-video** — provisional primary browser-first React/TypeScript monorepo foundation. MIT declared. Must validate commit, tests and actual import/edit/save/reopen/export.
2. **walterlow/freecut** — comparative reference for durable workspace, advanced timeline, proxies, media relinking, compositing, audio and headless test patterns. MIT declared. Do not wholesale-merge.

Detailed dossier: docs/RESEARCH_AND_REFERENCES.md. Historical mention of a 22-entry repository list was not recoverable from target repo; do not invent its contents.

## What the next contributor must do

1. Confirm current git tree, branches, and whether recovered project code exists elsewhere.
2. Verify upstream project versions/SHAs and test both with identical real media fixtures.
3. Complete ADR 0001 and settle one canonical foundation.
4. Import only justified/pinned code, with license notices, actual workspace, lockfile, CI.
5. Prove the vertical slice and output validation; make README install commands truthful.
6. Update BUILD_PLAN and TEST_PLAN with exact pass/fail evidence and links.
7. Choose next highest-priority defect/capability without rewriting the working pipeline.

## Required status report after every substantial change

- Branch, start SHA, end SHA, new/changed paths, PR/commit link.
- Features: verified implemented versus unverified versus planned.
- Exact executed commands and outcomes with OS/browser/Node/GPU when pertinent.
- Input fixture checksums and output probe evidence (do not attach unlicensed videos).
- Third-party source/license notices, security implications and known blockers.
- One clear next task with acceptance criteria.

## Owner decisions still open

- Final product name, intended release license and commercialization model.
- Whether historical implementation is located in an external archive.
- Exact first supported OS/browser/codec matrix.
- Adopt OpenReel as codebase or use it as a reference only (after tests).
- Distribution/desktop release timeline and installer/update security.
- AI priorities, if any; AI must not be required for base editing.

## No false progress

Old discussions described a larger codebase and passing tests. Treat those as past reports only; no proof was located in the live audited branch. A handoff should always point to actual code and reproducible tests before using words like complete, built, merged, or verified.

Entry points: README.md, AGENTS.md, docs/START_HERE.md, docs/adr/0001-foundation-selection.md, docs/BUILD_PLAN.md.