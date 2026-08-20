# v1.0.0 Post-Release Verification Record

Verification date: 2026-08-20

This file records what was directly verified after publication and what remains outside the capabilities of the connected workspace.

## Stable identity

- stable tag: `v1.0.0`
- stable commit: `e544f64630119c88425b49cc3e5a00e06d15ad84`
- release date in `CITATION.cff`: `2026-08-20`
- merge source: PR #1, normal merge preserving project history

The public `v1.0.0` tag resolves to the exact merge commit above.

## Pre-merge verification

Final release-candidate head:

`0a885e41f8a1ebef1152066d2cea79fe156b5dad`

All six PR workflows passed on that head:

- `model-tests` #800
- `topology-tests` #356
- `pressure-tests` #151
- `liquid-tests` #130
- `garment-tests` #85
- `publish-v1` validation #4

The corresponding exact-head reference artifact was:

- artifact name: `reference-output-0a885e41f8a1ebef1152066d2cea79fe156b5dad`
- artifact id: `9410060502`
- GitHub ZIP digest: `sha256:a2dbba8d70d5453bd445afa035dbf62857f6c14b71157ddcb933917b5d08b6fc`

The release-integrity regression coverage includes direct execution of `simulations/branched_liquid_resistor_network.py` and reference generation from outside the repository working directory.

## Publication workflow design

The source tree tagged as `v1.0.0` contains the one-shot publication workflow that was designed to:

1. run on the exact `main` merge commit;
2. verify `CITATION.cff` version/date;
3. rerun the full regression suite;
4. directly execute the indexed branched-network model;
5. regenerate the reference package from outside the checkout;
6. verify `metadata.json` records the exact release commit;
7. create `reference-output-v1.0.0.zip` and a SHA-256 file;
8. create GitHub tag/release `v1.0.0` if absent.

The public tag now exists and resolves to the intended merge commit.

## Immutable-tag reproduction check

After publication, PR #2 converted the one-shot publisher on `main` into a read-only verifier bound to immutable tag `v1.0.0` and release SHA `e544f64630119c88425b49cc3e5a00e06d15ad84`.

`verify-v1.0.0` run #6 completed successfully. The workflow:

- checked out tag `v1.0.0`;
- verified the exact release SHA and `CITATION.cff` metadata;
- passed the full regression suite;
- directly executed `simulations/branched_liquid_resistor_network.py`;
- regenerated the reference package from outside the checkout directory;
- verified `metadata.json` records the release SHA;
- built an inner reference ZIP and SHA-256 file;
- uploaded an Actions verification artifact.

Verification artifact:

- artifact name: `verify-v1.0.0-32381605767`
- artifact id: `9411331559`
- GitHub artifact ZIP digest: `sha256:61fb8261526ec0ff7eae007a9e9c88073c3bb41276b3ed61c8b67f558ca0c12d`

The artifact was independently downloaded and inspected in the connected execution environment. Results:

- downloaded outer artifact SHA-256: `61fb8261526ec0ff7eae007a9e9c88073c3bb41276b3ed61c8b67f558ca0c12d` — matches GitHub;
- outer artifact contained exactly `reference-output-v1.0.0.zip` and `reference-output-v1.0.0.zip.sha256`;
- inner reference ZIP SHA-256: `3e4a244e439b5dcf0407232a3093bd002da35845b16e77c476ee28a515635428` — matches the included `.sha256` file;
- inner ZIP contained 36 members;
- `metadata.json` recorded `git_commit = e544f64630119c88425b49cc3e5a00e06d15ad84`;
- package `sha256.txt` contained 32 checked entries;
- manifest verification result: **32 matched, 0 mismatches**.

This independently confirms that the immutable `v1.0.0` source can regenerate a self-consistent, commit-traced reference package.

## GitHub Release-asset verification boundary

The connected GitHub interface can read repository files, commits, PRs, CI artifacts, and the public tag, but it does not expose GitHub Release-asset list/download endpoints. Direct external GitHub downloads from the execution container are also unavailable because that container has no outbound DNS access.

Accordingly:

- **verified directly:** merge commit, public tag identity, tagged citation metadata, pre-merge CI, exact-head pre-release artifact provenance, resolved review findings, immutable-tag regression reproduction, regenerated verification ZIP/checksum, internal package manifest;
- **not independently re-downloaded in this workspace:** the final GitHub Release `reference-output-v1.0.0.zip` and its published `.sha256` asset.

This is a tooling/access limitation, not a claim that the Release assets are absent. The repository deliberately records this distinction instead of treating an inaccessible distribution endpoint as independently verified.

## Post-release policy

The stable tag must not be moved or rewritten.

After publication, `.github/workflows/publish-v1.yml` on `main` is a read-only verifier. It checks out the immutable `v1.0.0` tag, verifies the exact release SHA and metadata, reruns regressions, regenerates the reference package, and uploads a temporary Actions verification artifact. It does not recreate or modify the stable release.

## Evidence boundary

`v1.0.0` remains a computational technical record. No physical garment, bench specimen, or measured garment-performance result existed at publication.
