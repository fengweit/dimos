# Phase 2 — Robust Spatial Oracle

## Objective

Support four image-plane predicates with explicit unknown/ambiguity behavior.

## Prerequisite

Phase 1 is committed and H0–H2 green.

## Files

- Modify `models.py`, `relations.py`
- Expand `test_models.py`, `test_relations.py`

## Semantics

- `left-of(A,B)`: `center_x(B) - center_x(A) > horizontal_margin`.
- `right-of`: proven inverse.
- `above(A,B)`: `center_y(B) - center_y(A) > vertical_margin`; image y points down.
- `below`: proven inverse.
- Inside/equal to a margin is unknown, not false.

Configuration owns margins, minimum confidence, and coordinate convention. No magic constants.

## TDD behaviors

Implement one RED/GREEN cycle per item:

1. `right-of` inverse.
2. `above` image-axis semantics.
3. `below` inverse.
4. Horizontal ambiguity rejection.
5. Vertical ambiguity rejection.
6. Invalid/degenerate/out-of-range boxes rejected.
7. Low-confidence observation rejected.
8. Same object on both sides rejected.
9. Duplicate object observation follows the Phase 0 policy.
10. Labels do not affect geometry.

## Hard harness

H0–H3. Seeded boundary sweeps immediately below, at, and above margins. Horizontal/vertical mirror tests and input-order invariance are mandatory.

## Reviews

Adversarial geometry review, then code-quality review.

## Deliverable

Deterministically accepted frame facts plus rejection counts by reason.

## Stop condition

Stop if any mirror/inverse invariant fails or unknown candidates are emitted as false.

## Commit

```text
feat(benchmark): derive robust image-plane relations
```
