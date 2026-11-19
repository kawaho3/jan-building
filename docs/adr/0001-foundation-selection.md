# ADR 0001 — choose one editor foundation

- Status: **PROPOSED — NOT ACCEPTED**
- Date: 2026-11-19
- Owners: Jan Building maintainers

## Context

The target repository contained no application code at audit. Historical research considered building a CapCut-friendly but professionally expandable editor. We want to reuse public research without creating multiple conflicting timeline/rendering models or losing maintainability.

## Leading option: adopt OpenReel with tracked upstream provenance

Candidate: https://github.com/Augani/openreel-video (MIT declared).
It already describes a React/TypeScript monorepo and browser media editing pipeline. If confirmed by tests, using a documented/pinned OpenReel base could reduce time to a real vertical slice. Maintain attribution, record exact imported commit, keep a reproducible upstream-sync plan and document product-specific changes.

## Comparison option: use FreeCut as an independent reference

Reference: https://github.com/walterlow/freecut (MIT declared).
It describes WebGPU/WebCodecs editing, OPFS/FS Access workspace, relinking, proxy workflows and an extensive quality gate. Study patterns after a real test; do not mix its app state or renderer wholesale with OpenReel.

## Alternative

Build clean-room editor modules while studying both. Benefits: maximum control of domain model and ownership of implementation. Costs: high rendering and export risk; greater time before usable MVP. Only choose after measuring candidate shortcomings.

## Decision (pending)

**Provisional research priority**: evaluate OpenReel first, FreeCut second. **No code adoption approved or performed by this ADR.** Choose the foundation after reproducing real media workflows at pinned upstream SHAs.

## Required evidence before accepting

- Record exact SHA/branch/version and approved license provenance.
- Clone/install/build/test outputs on known OS/browser/GPU.
- Demonstrate input import, clip split/trim, save/reopen/relink and export with audio.
- Inspect whether preview and export share timing and effect semantics.
- Document perf risks, bundle/dependencies, media/codec compatibility, security and maintenance.
- Compare against FreeCut with identical fixture and acceptance rubric.
- Record chosen strategy: subtree/fork/vendor package or clean implementation, with update policy and rollback steps.

## Consequences

Selection should determine actual monorepo layout and package manager. Keep third-party core changes bounded; create shared contracts only when justified by an end-to-end working editor. Any later switch requires an ADR and project-file migration strategy.