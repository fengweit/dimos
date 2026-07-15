# Phase 1 — Contracts and Spatial Tracer Bullet

## Objective

Prove one observation becomes one public question, one private answer, and one scored prediction.

## Prerequisite

Phase 0 decisions are frozen.

## Files

- Create `dimos/benchmark/spatiotemporal/models.py`
- Create `dimos/benchmark/spatiotemporal/utilities.py`
- Create `dimos/benchmark/spatiotemporal/relations.py`
- Create `dimos/benchmark/spatiotemporal/questions.py`
- Create `dimos/benchmark/spatiotemporal/scoring.py`
- Create colocated `test_*.py` files for touched modules.

Do not add `__init__.py`.

## Minimal durable contracts

Use a strict frozen Pydantic base: `extra="forbid"`, `frozen=True`, `strict=True`.

- `BoundingBox2D`: normalized valid bounds.
- `ObjectObservation`: episode/frame/time/object/label/box/confidence.
- `SpatialPredicate`: start with `left-of`.
- `Question`: public text and executable contract; no oracle fields.
- `OracleAnswer`: private expected boolean and evidence.
- `Prediction` and one-question result.

Use frozen dataclasses only for temporary candidates.

## Vertical behavior

```text
mug box left of laptop box at final observation
→ accepted `mug_1 left-of laptop_1`
→ public “Is the mug left of the laptop at the end?”
→ private answer true with evidence frame
→ prediction true scores correct
```

## TDD sequence

1. RED/GREEN strict valid/invalid `BoundingBox2D`.
2. RED/GREEN one accepted `left-of` relation above margin.
3. RED/GREEN public question generation with stable ID.
4. RED/GREEN private answer stored separately.
5. RED/GREEN exact boolean scoring.
6. Serialize twice and assert identical JSON.

## Gates

H0–H2 plus targeted Ruff and mypy.

## Reviews

Contract compliance first; code-quality review second.

## Deliverable

One fully replayable in-memory tracer from observation to score.

## Stop condition

Stop if question construction requires oracle fields or if scoring can occur from the public record alone.

## Commit

```text
feat(benchmark): add a spatiotemporal QA tracer bullet
```
