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

"""Frozen callable boundaries for perception and candidate evaluation."""

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from pydantic import Field, model_validator

from dimos.benchmark.spatiotemporal.models import (
    BoundingBox2D,
    NonEmptyString,
    Question,
    StrictFrozenModel,
)
from dimos.msgs.sensor_msgs.Image import Image


class DetectedObject(StrictFrozenModel):
    """One detector result containing only perception-seam data."""

    object_id: NonEmptyString
    label: NonEmptyString
    box: BoundingBox2D
    confidence: float = Field(ge=0.0, le=1.0, allow_inf_nan=False)


class CandidateReadiness(StrictFrozenModel):
    """Candidate ingestion state with no teacher or oracle artifacts."""

    ready: bool
    ingested_frame_count: int = Field(ge=0)
    detail: NonEmptyString | None = None

    @model_validator(mode="after")
    def validate_readiness(self) -> "CandidateReadiness":
        if self.ready and self.ingested_frame_count == 0:
            raise ValueError("a ready candidate must ingest at least one frame")
        return self


class ObservationDetector(Protocol):
    """Narrow image-to-detections seam used by video sampling."""

    def detect(self, image: Image) -> Sequence[DetectedObject]: ...

    def close(self) -> None: ...


class CandidateAnswerer(Protocol):
    """Public-only video ingestion and question answering seam."""

    def ingest_video(self, video_path: Path) -> CandidateReadiness: ...

    def answer(self, question: Question) -> str | bool | None: ...

    def close(self) -> None: ...
