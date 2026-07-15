# Phase 6 — Scoring and Candidate Runner

## Objective

Accept typed bot predictions and produce exact diagnostic metrics without exposing oracle data to candidate code.

## Prerequisite

Phase 5 bundle separation and leakage harness pass.

## Files

- Modify `models.py`, `scoring.py`
- Create `runner.py`, `test_runner.py`
- Expand `test_scoring.py`

## Candidate boundary

Use a small protocol with two explicit steps: ingest a `PublicEpisodeContext` containing the source video reference/hash, then answer public `Question` records. The actual `TemporalMemory` adapter ingests the video through its normal image stream before any queries. It never receives canonical teacher observations, boxes, relation intervals, evidence, or answers. Accept boolean or tightly normalized `yes`/`no`; every other text is invalid, never guessed.

## TDD behaviors

1. Correct result.
2. Incorrect result.
3. Missing prediction.
4. Invalid prediction.
5. Duplicate prediction fails.
6. Unknown question ID fails.
7. Per-family/per-predicate counts.
8. Episode macro and global micro summaries.
9. Empty denominator is explicit, not 100%.
10. Stable report ordering/serialization.
11. Candidate exception follows a tested diagnostic policy.
12. Candidate invocation receives public episode/video context and questions.
13. Candidate invocation cannot receive teacher observations, boxes, intervals, evidence, or `OracleAnswer`.
14. Every private `QuestionResult` links question contract, prediction/status, expected answer, evidence frame IDs/timestamps, supporting boxes or interval IDs, and source-video hash.

## Harness controls

- Always-yes control demonstrates label balance.
- Final-frame-only control fails historical questions.
- Full-relation oracle control is an upper-bound sanity check, clearly labeled non-bot.

## Hard harness

H0–H4. Assert the controls produce distinct expected profiles.

## Reviews

Evaluation-method reviewer for denominators and leakage, then code-quality review.

## Deliverable

Replayable `predictions.jsonl` and a private `evaluation_report.json` with aggregate metrics and per-question evidence traces.

## Stop condition

Stop if candidate code lacks source-video context, sees teacher/private records, or metrics hide missing/invalid responses.

## Commit

```text
feat(benchmark): score typed spatiotemporal answers
```
