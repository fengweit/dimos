# Phase 8 — Raw Video Eval Generation

## Objective

Convert a real short video into canonical tracked observations, then invoke the already-verified replay pipeline to generate evals.

## Status

Mandatory final-presentation phase, started only after the core is green. Do not weaken truth quality merely to claim video support.

## Prerequisites

- Phases 0–7 committed and H0–H4 green.
- Git LFS/model assets available for manual smoke.
- An approved identity strategy is verified: native track IDs, or the constrained one-instance-per-prompt-class POC policy.

## Files

- Create `video_adapter.py`, `test_video_adapter.py`
- Create `yoloe_adapter.py`, `test_yoloe_adapter.py` only after identity feasibility passes.

## Architecture

```text
OpenCV video sampling
→ DimOS Image
→ narrow detector protocol
→ stable ID + label + confidence + pixel box
→ normalized ObjectObservation JSONL
→ Phase 7 replay
→ generated public/oracle eval bundle
```

Keep heavy YOLO-E imports inside adapter execution. Use existing `Yoloe2DDetector` in `PROMPT` mode and `process_image` when tracking IDs are required. Always clean up in `finally`.

## Identity feasibility gate

Inspect `Detection2DBBox.from_ultralytics_result` and prove a track ID survives conversion. Identity strategies are allowed in this order:

1. Preserve native Ultralytics track IDs with the smallest tested adapter or fix.
2. For the deliberately simple POC video, enforce at most one visible instance per prompted class and use normalized class identity across frames.

The fallback validates uniqueness per sampled frame and fails on duplicate class instances. Do not introduce a naive nearest-center tracker. Prepared observations alone do not satisfy the final video presentation.

## Default TDD behaviors

1. Exact frame-sampling timestamps.
2. Pixel-to-normalized box conversion.
3. Fake detector produces stable observations.
4. Missing/corrupt video is actionable.
5. Dropped detection does not create inverse truth.
6. Cleanup on success and exception.
7. Default test never loads YOLO-E or LFS assets.

## Manual smoke

Run H6. Save observations first; all later eval generation must replay from that saved file. Require at least 12 retained questions or emit insufficiency statistics.

## Reviews

Perception API before code; lifecycle and dropped-track adversary after code.

## Deliverable

Actual raw video → canonical observations → deterministic eval bundle.

## Stop condition

Neither approved identity strategy is valid, real execution is not reproducible, or model-derived ambiguity contaminates geometry labels. Resolve this by fixing the adapter or re-recording a constrained video; do not drop the video milestone.

## Commit

```text
feat(benchmark): adapt tracked video detections to observations
```
