# Phase 7 — Canonical Observation Replay

## Objective

Decouple expensive perception from deterministic evaluation through strict observation JSONL.

## Prerequisite

Phase 6 scoring is green.

## Files

- Create `observation_io.py`, `test_observation_io.py`
- Modify bundle/demo code only as required by tests.

## TDD behaviors

1. Read valid observation JSONL.
2. Malformed record reports line number/path.
3. Duplicate identity/timestamp follows frozen policy.
4. Ordering follows frozen policy.
5. Write canonical observation JSONL.
6. Read-write-read equality.
7. Replay yields the same intervals/questions/bundle as in-memory input.
8. Unknown fields fail under strict models.
9. Empty input returns actionable insufficiency, not an empty-success benchmark.

## Hard harness

H0–H4. Compare in-memory and replay-generated canonical bytes/hashes.

## Reviews

Serialization/reproducibility reviewer, then code-quality review.

## Deliverable

A private canonical teacher-observation file that completely isolates model inference from benchmark generation. It is replay input for benchmark authors, not candidate context.

## Stop condition

Stop if replay differs from in-memory generation.

## Commit

```text
feat(benchmark): replay canonical object observations
```
