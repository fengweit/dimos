# Phase 0 — Foundation

## Objective

Establish a clean reproducible baseline and freeze v1 semantics before production code.

## Prerequisites

- Branch `feat/spatiotemporal-video-qa` exists.
- Implementation index and specs are committed.

## Actions

1. Confirm `git status --short --branch` is clean.
2. Fetch `origin`; record `origin/main` and branch base SHAs.
3. Verify repository-pinned `uv`; do not install Git LFS until Phase 8.
4. Run neighboring pure tests and strict mypy once; record pre-existing failures.
5. Dispatch contract, geometry, and repository-standard reviewers in parallel.
6. Consolidate findings and freeze:
   - out-of-order input policy;
   - duplicate timestamp policy;
   - strict temporal-boundary policy;
   - ID canonicalization inputs;
   - uncertainty-margin units.

## Recommended frozen defaults

- Canonically sort by `(timestamp_s, frame_id, object_id)`.
- Reject duplicate object identity at one timestamp.
- `before` requires `first.end_s < second.start_s`; equality is unknown.
- Use normalized image coordinates and normalized margins.
- Derive stable IDs from schema version plus canonical contract bytes.

## Harness

Baseline only; no feature tests yet.

## Deliverable

A session record of base SHA, environment, baseline results, reviewer findings, and frozen decisions.

## Stop condition

Do not start Phase 1 while any semantic choice above is unresolved.

## Commit

None.
