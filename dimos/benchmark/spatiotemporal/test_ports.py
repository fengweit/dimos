# Copyright 2025-2026 Dimensional Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for frozen perception and candidate callable ports."""

from pathlib import Path

from pydantic import ValidationError
import pytest

from dimos.benchmark.spatiotemporal.models import BoundingBox2D, Question
from dimos.benchmark.spatiotemporal.ports import (
    CandidateAnswerer,
    CandidateReadiness,
    DetectedObject,
)


def test_detected_object_contains_only_perception_seam_data() -> None:
    detected = DetectedObject(
        object_id="track_7",
        label="mug",
        box=BoundingBox2D(x_min=0.1, y_min=0.2, x_max=0.3, y_max=0.4),
        confidence=0.9,
    )

    assert set(detected.model_dump()) == {"object_id", "label", "box", "confidence"}


def test_candidate_readiness_contains_no_teacher_or_oracle_data() -> None:
    readiness = CandidateReadiness(ready=True, ingested_frame_count=24, detail=None)

    dumped = readiness.model_dump()
    assert dumped == {"ready": True, "ingested_frame_count": 24, "detail": None}
    forbidden = {"observations", "boxes", "intervals", "answers", "evidence", "oracle"}
    assert forbidden.isdisjoint(dumped)
    with pytest.raises(ValidationError, match="at least one frame"):
        CandidateReadiness(ready=True, ingested_frame_count=0, detail=None)


def test_candidate_answerer_signature_is_expressible_without_private_records() -> None:
    class FakeCandidate:
        def ingest_video(self, video_path: Path) -> CandidateReadiness:
            assert video_path == Path("episode.mp4")
            return CandidateReadiness(ready=True, ingested_frame_count=1, detail=None)

        def answer(self, question: Question) -> str | bool | None:
            return None

        def close(self) -> None:
            return None

    candidate = FakeCandidate()
    typed_candidate: CandidateAnswerer = candidate
    assert typed_candidate.ingest_video(Path("episode.mp4")).ready is True
