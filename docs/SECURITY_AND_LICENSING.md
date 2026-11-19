# Security, provenance, privacy, and licensing

This guidance is not legal advice. Verify the exact code, files, notices, and distribution obligations before importing or shipping.

## The two candidate editors

- OpenReel https://github.com/Augani/openreel-video — GitHub declares MIT licensing.
- FreeCut https://github.com/walterlow/freecut — GitHub declares MIT licensing.

**MIT attribution is not automatic permission for everything inside a repository.** Validate the actual LICENSE at pinned SHA, contributors, fonts, sample media, model weights, dependencies, vendor binaries, trademarks, submodules and export codecs individually. Retain required copyright and license notices in source and packaged distributions.

## Reuse checklist

- [ ] Pinned exact upstream commit SHA and source URL
- [ ] Review git history, LICENSE, third-party notices and dependency manifests
- [ ] Inventory every reused file/module and reasons for selection
- [ ] Confirm build/runtime dependency licenses and compatible distribution obligations
- [ ] Inspect asset/model-weight licenses and restrictions separately
- [ ] Check code security advisories, supply-chain risk and bundled binary provenance
- [ ] Store attribution and source-origin mapping in repository documentation
- [ ] Confirm redistributed binaries include appropriate notices; assess codec patent exposure by jurisdiction
- [ ] Preserve ability to update upstream security fixes
- [ ] Do not use upstream branding, trademark, logos or screenshots as Jan Building property

Do not copy a second complete editor on top of the first. Integration must pass a functionality, API, license and regression review.

## Minimum security properties

- Open user media with explicit local file permissions. No silent upload or outbound scanning.
- Validate imported project manifests, schemas, archive paths, lengths, MIME/content types and file limits; prevent archive extraction/path traversal.
- Apply Content Security Policy and safe rendering to SVG/HTML/subtitle/metadata inputs; avoid unsanitized injection.
- Bound decoder and worker resource use; cancel jobs and free GPU memory on project close/device loss.
- Handle permission revocation, quota exhaustion and corrupted caches without losing the user project.
- Never store auth tokens in committed configuration. Use opt-in, least-privilege credentials if cloud export or AI services are later offered.
- Protect desktop bridge APIs from arbitrary filesystem reads, shell execution and untrusted local web content.
- Run dependency audits and inspect license conflicts before shipping.
- Provide clear consent and disclosure for analytics, remote transcription, cloud effects and model downloads.

## AI and commercial cost

The core editor must remain functional offline and without a paid API. Optional cloud connectors or hosted models require explicit enablement, cost transparency, token protection, and safe permissions. Locally hosted models may need downloads, RAM/VRAM and separate weight-license approval.

## Project-wide ownership

Brand name, artwork, new independently authored code license, contributor policy, and company ownership are **not yet decided** by the documentation in this repository. Do not insert a Jan Building MIT LICENSE without the owner's distribution decision; preserve upstream notices if code is later reused.