# Phase 9 — Demo, Hardening, and Delivery

## Objective

Provide a one-command replayable demonstration and package a review-ready PR with verified evidence.

## Prerequisite

Phases 0–8 are green, including verified raw-video eval generation.

## Files

- Create `demo_spatiotemporal_qa.py`
- Create `temporal_memory_answerer.py` and `test_temporal_memory_answerer.py`
- Create `docs/development/spatiotemporal_video_qa.md`
- Do not add a console entry point unless maintainers request it.

## Demo modes

- `synthetic`: fixed three-object transition, bundle, controls, report.
- `replay`: observation JSONL → bundle → supplied predictions → report.
- `video`: video → observations → replay pipeline → generated evals.
- `candidate`: feed the same video to DimOS `TemporalMemory`, call `query` with public questions only, persist predictions, and score them.

## Real bot contract

- Use the existing `TemporalMemory.query(question: str) -> str` `@skill` as the first real candidate.
- Before questions, the adapter streams the same source video into `TemporalMemory` and verifies processing through its state/query readiness signals.
- The adapter then receives public `Question` records and normalizes explicit yes/no answers through the Phase 6 runner.
- The candidate may use its own VLM-derived temporal state and graph, but never canonical teacher observations/boxes, geometry-teacher relation intervals, evidence, or answers.
- Default tests use a fake query callable; the final manual harness executes the real `TemporalMemory` path.
- Always-yes, final-frame, and oracle controls remain diagnostics and cannot satisfy actual-bot acceptance.

## Output contract

```text
run/
├── observations.jsonl
├── benchmark/
│   ├── manifest.json
│   ├── public/...
│   └── oracle/...
├── predictions.jsonl
└── evaluation_report.json
```

`observations.jsonl` and the evidence-bearing report are teacher/private artifacts even though the demo places them under one run root. Only source-video context plus `benchmark/public/` enter the candidate path.

## Documentation requirements

- Exact commands and prerequisites.
- Image-plane limitation.
- Oracle provenance and ambiguity policy.
- Candidate/oracle isolation.
- How to run the actual `TemporalMemory` candidate on the same video.
- Replay workflow.
- Expected synthetic control results.
- How to inspect one failure and its evidence IDs.
- Known limitations and future deeper `WorldBelief` or robot-execution evaluation.

## Final presentation sequence

1. Show one short fixed-camera video with a few uniquely identifiable objects and at least one relation transition.
2. Run video ingestion and show sampled evidence frames with detected identities and boxes.
3. Show the automatically generated public test set: at least 12 balanced spatial-at-time and before/after questions.
4. Show that answers/evidence remain in a separate private oracle bundle.
5. Run the same video through the real DimOS `TemporalMemory` candidate and ask only the public questions.
6. Show its typed predictions and the exact spatial-versus-temporal score report.
7. Open one correct and one incorrect/invalid result and trace each to predicate, expected answer, frame IDs/timestamps, supporting boxes/intervals, and source-video hash. If the actual bot is perfect, label an injected invalid prediction as a harness diagnostic rather than bot output.
8. Replay saved observations and prove the generated eval artifacts are byte-identical.

## Hardening

1. Run every documented command from clean output roots.
2. Compare repeated canonical artifacts.
3. Execute H6 end to end, including real `TemporalMemory` predictions and scoring.
4. Run H7.
5. Inspect diff for unrelated changes, secrets, absolute paths, binaries, model assets, videos, generated output, or `__init__.py`.
6. Run final parallel spec, quality/security, and test-adequacy reviews.
7. Fix accepted findings through failing regression tests.
8. Rerun H6 and H7 after the final change.
9. Verify each commit is independently green.
10. Push once; inspect actual remote CI before claiming success.

## PR

Title:

```text
feat(benchmark): generate spatial and temporal QA from video
```

Evidence includes targeted/full test results, static checks, replay hashes, one failure diagnostic, raw-video artifact counts, and the real `TemporalMemory` candidate report.

## Final acceptance

- ≥3 objects and ≥1 relation transition.
- ≥12 balanced spatial/temporal questions.
- Byte-identical regeneration and replay.
- No public oracle leakage.
- Complete prediction diagnostics.
- A raw video automatically produces the eval bundle.
- The real-video run itself has at least three consistent identities, one transition, both question families, and recorded continuity/drop statistics.
- A real `TemporalMemory` candidate answers the generated public questions and receives a scored report.
- Repository gates pass.
- Physical actions and world-frame relationships remain explicitly out of scope.

## Reviews

Clean-shell documentation reviewer plus final three-way review.

## Stop condition

Do not open/push a PR while local H7 or documented replay fails.

## Commit

```text
docs(benchmark): add the spatiotemporal QA demo
```
