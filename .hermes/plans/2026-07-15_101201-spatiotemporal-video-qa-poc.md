# Spatiotemporal Video QA POC

> Architecture index. Implementation runs through one small checklist at a time in the [micro-spec index](spatiotemporal-video-qa-specs/steps/README.md).

## Goal

Take a short fixed-camera video, automatically derive deterministic image-plane spatial and temporal questions, have a real DimOS `TemporalMemory` candidate answer those public questions, and produce an evidence-linked exact evaluation report.

## Non-negotiable constraints

- Image-plane truth only: `left-of`, `right-of`, `above`, `below`.
- Temporal truth only: strict `before` and `after` over non-overlapping intervals.
- Boolean answers only in v1.
- Ambiguous geometry is unknown, never false.
- Public questions and private oracle answers are physically separate.
- Detector boxes and canonical teacher observations are private provenance; the real candidate receives the source video and public questions, not teacher-derived observations.
- No LLM-generated labels or LLM judge.
- No new dependency, robot-action `Module`, new `Blueprint`, hosted service, or model training. A thin adapter invoking the existing `TemporalMemory` module/skill is required.
- No default test may require video, model weights, LFS, network, credentials, or hardware.
- The final presentation must run raw video-to-eval generation and one real DimOS candidate; synthetic controls are not a substitute.
- No `__init__.py` files.
- Production behavior is implemented with RED-GREEN-REFACTOR.

## Execution protocol

Before implementation, read:

1. [`execution-protocol.md`](spatiotemporal-video-qa-specs/execution-protocol.md)
2. [`quality-gates.md`](spatiotemporal-video-qa-specs/quality-gates.md)
3. Only the earliest incomplete [micro-spec](spatiotemporal-video-qa-specs/steps/README.md).

Each micro-spec is one reviewable commit and one immediate remote push. Phase specs below remain cross-cutting contracts; workers load one only at a phase-boundary step. A failed checklist blocks all later steps.

| Phase | Contract | Micro-steps | Replayable result |
|---|---|---|---|
| 0 | [`00-foundation.md`](spatiotemporal-video-qa-specs/00-foundation.md) | complete | Clean baseline and frozen contracts |
| 1 | [`01-tracer-and-contracts.md`](spatiotemporal-video-qa-specs/01-tracer-and-contracts.md) | 01a–01d | One observation → question → score |
| 2 | [`02-spatial-oracle.md`](spatiotemporal-video-qa-specs/02-spatial-oracle.md) | 02a–02b | Four robust image-plane predicates |
| 3 | [`03-temporal-intervals.md`](spatiotemporal-video-qa-specs/03-temporal-intervals.md) | 03a–03b | Replayable relation history |
| 4 | [`04-question-generation.md`](spatiotemporal-video-qa-specs/04-question-generation.md) | 04a–04b | Deterministic spatial/temporal cases |
| 5 | [`05-bundles.md`](spatiotemporal-video-qa-specs/05-bundles.md) | 05a–05b | Immutable public/oracle bundle |
| 6 | [`06-scoring-and-runner.md`](spatiotemporal-video-qa-specs/06-scoring-and-runner.md) | 06a–06b | Typed predictions and diagnostic report |
| 7 | [`07-observation-replay.md`](spatiotemporal-video-qa-specs/07-observation-replay.md) | 07a–07b | Saved observations reproduce the bundle |
| 8 | [`08-video-generation.md`](spatiotemporal-video-qa-specs/08-video-generation.md) | 08a–08c | Raw video → canonical observations → evals |
| 9 | [`09-demo-and-delivery.md`](spatiotemporal-video-qa-specs/09-demo-and-delivery.md) | 09a–09c | Real candidate and one-command demo |

## Recommended execution boundary

Phases 0–7 establish the hermetic core. Phases 8–9 are mandatory for the final presentation. If native detector track IDs are unavailable, the approved POC fallback is a constrained scene with at most one instance per prompted class, making normalized class identity stable. We must fix the adapter or re-record the scene rather than finish without video.

## Final acceptance summary

- At least three objects and one relation transition in the synthetic episode.
- At least 12 balanced spatial and temporal questions.
- Stable IDs and byte-identical regeneration.
- Saved observations reproduce the same benchmark bundle.
- No answer/evidence/private provenance in the public package.
- Correct/incorrect/missing/invalid predictions are diagnosed.
- A raw video generates the canonical observations and eval bundle.
- The existing `TemporalMemory.query` skill answers the public questions without access to oracle records.
- Ruff, strict mypy, pre-commit, and default pytest suite pass.
- Real-video claims are made only from verified artifacts.
