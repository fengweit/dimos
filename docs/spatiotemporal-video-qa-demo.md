# Spatiotemporal Video-QA Demo

This demo exercises the complete local teacher/candidate pipeline on a real repository video:

1. trims `assets/simple_demo.mp4` to a constrained 25-second clip;
2. samples real decoded OpenCV frames;
3. runs the repository YOLO-E 11s prompt model with persistent tracking;
4. writes canonical observations;
5. derives spatial facts and strict relation intervals;
6. generates public spatial and `before`/`after` questions plus a private oracle;
7. writes and reloads isolated public/oracle bundles in two roots;
8. verifies root-independent logical hashes;
9. ingests the public video into the real `TemporalMemory` module;
10. exercises TemporalMemory plumbing with a timestamp-scripted entity fixture and question-hash baseline that receive no private records; and
11. scores those predictions in a separate evaluator boundary that owns the private oracle.

The candidate function accepts only the video, public `Question` records, an output root, and duration; it never receives an `EvaluationBundle` or oracle records. The timestamp-scripted VLM fixture intentionally ignores image pixels and is not a claim of visual QA quality. It exists to exercise the real `TemporalMemory` accumulator, state, entity graph, query path, readiness lifecycle, and cleanup with real decoded frames. The teacher-side YOLO-E path is visually grounded and uses the actual model weights.

## Prerequisites

Install Git LFS and materialize the real assets and YOLO-E weights:

```bash
git lfs install --local
git lfs pull --include='assets/simple_demo.mp4,data/.lfs/models_yoloe.tar.gz'
uv run python -c "from dimos.utils.data import get_data; print(get_data('models_yoloe'))"
```

YOLO-E text prompting also needs Ultralytics CLIP:

```bash
uv pip install 'git+https://github.com/ultralytics/CLIP.git'
```

The first run may download the MobileCLIP text encoder into the Ultralytics user cache.

## One command

From the repository root:

```bash
uv run python -m dimos.benchmark.spatiotemporal.demo \
  --source-video assets/simple_demo.mp4 \
  --output-root .artifacts/spatiotemporal-video-qa \
  --duration-s 25 \
  --frame-stride 150
```

The command prints a JSON summary and writes the same data to:

```text
.artifacts/spatiotemporal-video-qa/summary.json
```

The output directory also contains:

- the constrained video;
- canonical `observations.jsonl` after two independent YOLO-E runs produce identical observations and statistics;
- two independently written public/oracle bundle roots; and
- an isolated TemporalMemory SQLite database and JSONL history.

## Verified reference run

The reference macOS CPU run produced:

- 750 decoded video frames over 25 seconds;
- 5 YOLO-E sampled frames;
- 8 detections across 4 native object IDs;
- 6 accepted relation facts and 6 relation intervals;
- 54 questions: 6 spatial and 48 temporal;
- identical public/oracle manifests across two output roots;
- logical bundle SHA-256 `ba4be04df7ed376925551bf998b6dce3fa08678665644ec0337c6eda6f9d62a9`;
- TemporalMemory readiness with 25 ingested frames, 5 analyzed windows, and 3 entities;
- two independent YOLO-E detector/tracker runs produced identical observations and statistics;
- 54 valid timestamp-scripted candidate answers with no missing/invalid outcomes and 26/54 exact matches; and
- two complete command invocations produced byte-identical summaries with SHA-256 `610c4bba46705d2ba61240e904faed732199c2fe75d8bb8be86d36a7463bf491`.

OpenCV may print a macOS warning about duplicate FFmpeg AVFoundation classes from the `cv2` and `av` wheels. The verified run completed successfully despite that warning.
