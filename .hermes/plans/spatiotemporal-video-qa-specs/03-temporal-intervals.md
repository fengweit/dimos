# Phase 3 — Temporal Relation Intervals

## Objective

Fold frame-level facts into replayable intervals without interpreting missing evidence as negative evidence.

## Prerequisite

Phase 2 is committed and H0–H3 green.

## Files

- Modify `models.py`, `relations.py`
- Expand `test_relations.py`

## Durable contract

`RelationInterval` records episode, subject, predicate, object, start/end timestamps, support count, ordered evidence frame IDs, deterministic confidence, and provenance.

## TDD behaviors

1. Consecutive facts merge.
2. Start/end and evidence ordering are stable.
3. Minimum support is enforced.
4. A short missing gap follows configured policy.
5. A long gap splits intervals.
6. An ambiguous frame creates no inverse.
7. A proven inverse closes the prior interval and opens another.
8. Out-of-order input follows the Phase 0 policy.
9. Duplicate identity/timestamp fails with context.
10. Confidence aggregation is deterministic.

## Hard harness

H0–H3, timestamp-shift invariance, shuffled input, missing-frame sequences, and no overlapping inverse intervals for one object pair.

## Reviews

Interval-algebra reviewer, then code-quality reviewer.

## Deliverable

Canonical relation-interval JSONL for the synthetic movement episode.

## Stop condition

Stop if absence or ambiguity creates a negative fact, or inverse intervals overlap.

## Commit

```text
feat(benchmark): build temporal relation intervals
```
