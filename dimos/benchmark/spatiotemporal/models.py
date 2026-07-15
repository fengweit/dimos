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

"""Strict data contracts for spatiotemporal video QA."""

from enum import StrEnum
from typing import Annotated, Self
import unicodedata

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator

from dimos.benchmark.spatiotemporal.utilities import SCHEMA_VERSION, stable_id


def _require_nfc(value: str) -> str:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ValueError("string fields must contain valid Unicode scalar values") from error
    if not unicodedata.is_normalized("NFC", value):
        raise ValueError("string fields must be NFC-normalized")
    return value


NonEmptyString = Annotated[str, Field(min_length=1), AfterValidator(_require_nfc)]
QuestionId = Annotated[
    str,
    Field(pattern=r"^question_[0-9a-f]{64}$"),
    AfterValidator(_require_nfc),
]


class SpatialPredicate(StrEnum):
    """Supported image-plane predicates."""

    LEFT_OF = "left-of"
    RIGHT_OF = "right-of"
    ABOVE = "above"
    BELOW = "below"


class QuestionKind(StrEnum):
    """Supported public question categories."""

    SPATIAL = "spatial"


class StrictFrozenModel(BaseModel):
    """Base for immutable benchmark records with no implicit coercion."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class BoundingBox2D(StrictFrozenModel):
    """A normalized image-plane bounding box."""

    x_min: float = Field(ge=0.0, le=1.0, allow_inf_nan=False)
    y_min: float = Field(ge=0.0, le=1.0, allow_inf_nan=False)
    x_max: float = Field(ge=0.0, le=1.0, allow_inf_nan=False)
    y_max: float = Field(ge=0.0, le=1.0, allow_inf_nan=False)

    @model_validator(mode="after")
    def validate_bounds(self) -> Self:
        """Reject empty or inverted boxes."""
        if self.x_min >= self.x_max or self.y_min >= self.y_max:
            raise ValueError("bounding box minimums must be below maximums")
        return self


class ObjectObservation(StrictFrozenModel):
    """One object's canonical observation in a sampled video frame."""

    episode_id: NonEmptyString
    frame_id: int = Field(ge=0)
    timestamp_s: float = Field(allow_inf_nan=False)
    object_id: NonEmptyString
    label: NonEmptyString
    box: BoundingBox2D
    confidence: float = Field(ge=0.0, le=1.0, allow_inf_nan=False)


class Question(StrictFrozenModel):
    """A public question with an executable, answer-free contract."""

    question_id: QuestionId
    episode_id: NonEmptyString
    text: NonEmptyString
    question_kind: QuestionKind
    predicate: SpatialPredicate
    object_ids: tuple[NonEmptyString, NonEmptyString]
    reference_ids: tuple[()] = ()

    @model_validator(mode="after")
    def validate_executable_contract(self) -> Self:
        """Reject self-relations and IDs that do not match public semantics."""
        if self.object_ids[0] == self.object_ids[1]:
            raise ValueError("spatial question object IDs must differ")
        expected_id = stable_id(
            "question",
            {
                "object_ids": self.object_ids,
                "predicate": self.predicate.value,
                "question_kind": self.question_kind.value,
                "reference_ids": self.reference_ids,
                "schema_version": SCHEMA_VERSION,
            },
        )
        if self.question_id != expected_id:
            raise ValueError("question ID does not match its executable contract")
        return self


class OracleAnswer(StrictFrozenModel):
    """A private expected answer and its teacher evidence."""

    question_id: QuestionId
    expected: bool
    evidence_frame_ids: tuple[int, ...]


class Prediction(StrictFrozenModel):
    """One candidate's typed Boolean answer."""

    question_id: QuestionId
    answer: bool


class QuestionResult(StrictFrozenModel):
    """Exact result for one question."""

    question_id: QuestionId
    expected: bool
    predicted: bool
    correct: bool
