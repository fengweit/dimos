# Phase 4 — Deterministic Question Generation

## Objective

Generate balanced boolean spatial and temporal cases from proven relation intervals.

## Prerequisite

Phase 3 is committed and interval replay is deterministic.

## Files

- Modify `models.py`, `questions.py`, `utilities.py`
- Expand `test_questions.py`, `test_utilities.py`

## Question families

Spatial:

- Relation at episode start.
- Relation at episode end.
- Contrastive inverse false case only when inverse truth is proven.

Temporal:

- Relation A occurred before B.
- Relation B occurred after A.
- Reversed-order negative only for strictly non-overlapping intervals.

## Generation rules

- Controlled templates only.
- Stable IDs from schema version plus canonical executable contract.
- Stable sort before output.
- Balance true/false where evidence supports both.
- Missing evidence never creates a false answer.
- Touching/overlapping intervals generate no order question.
- No duplicate physical contract with alternate wording in v1.
- Report accepted/rejected counts by reason.

## TDD sequence

1. Start-state positive.
2. End-state positive.
3. Proven inverse negative.
4. Strict before positive.
5. Strict after positive.
6. Reversed-order negative.
7. Overlap/touch rejection.
8. Stable IDs and input-order invariance.
9. Balance and duplicate checks.
10. Generation statistics.

## Hard harness

H0–H3. Repeated byte equality, inverse consistency, timestamp shift, and template/label nuisance checks.

## Reviews

Dataset-bias/template-leakage reviewer, then code-quality review.

## Deliverable

At least 12 deterministic generated cases from one synthetic episode.

## Stop condition

Stop if a label is inferable from template alone, IDs drift, or a negative derives from absence.

## Commit

```text
feat(benchmark): generate spatial and temporal questions
```
