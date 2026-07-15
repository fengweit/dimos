# Quality and Harness Gates

## H0 — RED evidence

Every production behavior has a test that was observed failing for the expected reason before implementation.

## H1 — Focused tests

```bash
uv run pytest dimos/benchmark/spatiotemporal/test_<module>.py -v
```

No model, LFS, network, credentials, worker, or hardware.

## H2 — Package tests

```bash
uv run pytest dimos/benchmark/spatiotemporal -v
```

Must be deterministic and warning-free.

## H3 — Invariant/metamorphic harness

Use deterministic generated examples; add no new property-testing dependency.

- Observation-order invariance.
- Horizontal mirror: `left-of ↔ right-of`.
- Vertical mirror: `above ↔ below`.
- Timestamp translation preserves temporal answers.
- Object-ID renaming preserves answer structure.
- Inverse predicates remain consistent.
- Ambiguous geometry never becomes a negative fact.
- Repeated generation is byte-identical.

## H4 — Replay and leakage harness

- Generate twice in separate temporary roots and compare canonical bytes/hashes.
- Copy `public/` alone and load it successfully.
- Scan public keys and values for teacher observations/boxes, answers, evidence, confidence, oracle paths, and absolute private paths.
- Reject missing references, duplicate IDs, absolute paths, traversal, and hash mismatch.
- Prove scoring requires separately supplied oracle data.

## H5 — Adapter harness

- Fake detector with real DimOS `Image` values.
- Exact sampling timestamps and box normalization.
- Dropped detection never creates a false inverse.
- Cleanup on success and exception.
- Default tests never instantiate YOLO-E.

## H6 — Real-video smoke

Manual/self-hosted only:

1. Resolve a local/LFS video.
2. Run prompted YOLO-E tracking.
3. Save canonical observations.
4. Replay observations through the hermetic core.
5. Generate at least 12 questions or return an actionable insufficiency report.
6. Regenerate from observations and compare canonical artifacts.
7. Verify the video produced at least three consistent identities, at least one spatial transition, both spatial and temporal questions, and identity continuity/drop statistics.
8. Feed the same source video—not teacher observations—to the real DimOS `TemporalMemory` candidate.
9. Verify video ingestion completed before invoking `TemporalMemory.query` with public question text only.
10. Persist predictions and score them with the separately loaded private oracle.
11. Inspect one correct evidence trace and one incorrect/invalid trace; if the actual candidate has no non-correct case, use a clearly labeled diagnostic mutation rather than misrepresenting bot output.
12. Read back the observations, generated evals, bot predictions, and report before reporting success.

## H7 — Repository gate

```bash
uv run ruff format --check dimos/benchmark/spatiotemporal
uv run ruff check dimos/benchmark/spatiotemporal
uv run mypy
source .venv/bin/activate
pre-commit run --all-files
uv run pytest --numprocesses=3 -m 'not (self_hosted or mujoco or self_hosted_large)'
```

## Required adversarial cases

- Values immediately below, at, and above every geometric threshold.
- Same object on both sides of a relation.
- Duplicate identity at one timestamp.
- Out-of-order observations.
- Missing frames and long gaps.
- Overlapping and touching temporal intervals.
- Always-yes predictions.
- Missing, invalid, duplicate, and unknown predictions.
- Public bundle containing a deliberately injected private field.
- Bundle path traversal and corrupted hash.
