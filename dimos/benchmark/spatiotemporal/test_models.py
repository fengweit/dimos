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

"""Tests for strict spatiotemporal QA contracts."""

from pydantic import ValidationError
import pytest

from dimos.benchmark.spatiotemporal.models import (
    BoundingBox2D,
    ObjectObservation,
    Question,
    QuestionKind,
    SpatialPredicate,
)


def test_bounding_box_accepts_only_strict_normalized_valid_bounds() -> None:
    box = BoundingBox2D(x_min=0.1, y_min=0.2, x_max=0.4, y_max=0.8)

    assert box.model_dump() == {
        "x_min": 0.1,
        "y_min": 0.2,
        "x_max": 0.4,
        "y_max": 0.8,
    }

    invalid_payloads = (
        {"x_min": 0.4, "y_min": 0.2, "x_max": 0.4, "y_max": 0.8},
        {"x_min": 0.5, "y_min": 0.2, "x_max": 0.4, "y_max": 0.8},
        {"x_min": 0.1, "y_min": 0.8, "x_max": 0.4, "y_max": 0.8},
        {"x_min": -0.1, "y_min": 0.2, "x_max": 0.4, "y_max": 0.8},
        {"x_min": 0.1, "y_min": 0.2, "x_max": 1.1, "y_max": 0.8},
        {"x_min": float("nan"), "y_min": 0.2, "x_max": 0.4, "y_max": 0.8},
        {"x_min": "0.1", "y_min": 0.2, "x_max": 0.4, "y_max": 0.8},
    )
    for payload in invalid_payloads:
        with pytest.raises(ValidationError):
            BoundingBox2D.model_validate(payload)

    with pytest.raises(ValidationError):
        BoundingBox2D.model_validate(
            {
                "x_min": 0.1,
                "y_min": 0.2,
                "x_max": 0.4,
                "y_max": 0.8,
                "unexpected": True,
            }
        )
    with pytest.raises(ValidationError):
        box.x_min = 0.0


def test_object_observation_rejects_invalid_identity_time_and_confidence() -> None:
    observation = ObjectObservation(
        episode_id="episode_1",
        frame_id=12,
        timestamp_s=0.5,
        object_id="mug_1",
        label="mug",
        box=BoundingBox2D(x_min=0.1, y_min=0.2, x_max=0.3, y_max=0.4),
        confidence=0.9,
    )

    assert observation.object_id == "mug_1"

    invalid_overrides = (
        {"episode_id": ""},
        {"frame_id": -1},
        {"timestamp_s": float("inf")},
        {"object_id": ""},
        {"object_id": "mu\u0301g"},
        {"label": ""},
        {"confidence": -0.1},
        {"confidence": 1.1},
    )
    payload = observation.model_dump()
    for override in invalid_overrides:
        with pytest.raises(ValidationError):
            ObjectObservation.model_validate(payload | override)


def test_object_observation_allows_finite_negative_timestamp_translation() -> None:
    observation = ObjectObservation(
        episode_id="episode_1",
        frame_id=12,
        timestamp_s=-0.5,
        object_id="mug_1",
        label="mug",
        box=BoundingBox2D(x_min=0.1, y_min=0.2, x_max=0.3, y_max=0.4),
        confidence=0.9,
    )

    assert observation.timestamp_s == -0.5


def test_question_rejects_malformed_id_and_non_nfc_object_identity() -> None:
    payload = {
        "question_id": "question_4ef1579875e841ec7602de2e9cfc95f0bfdfb5e8d2e38ca798f462f8f72eda1e",
        "episode_id": "episode_1",
        "text": "Is the mug left of the laptop at the end?",
        "question_kind": QuestionKind.SPATIAL,
        "predicate": SpatialPredicate.LEFT_OF,
        "object_ids": ("obj_red", "obj_blue"),
    }

    assert Question.model_validate(payload).object_ids == ("obj_red", "obj_blue")
    with pytest.raises(ValidationError):
        Question.model_validate(payload | {"question_id": "question_1"})
    with pytest.raises(ValidationError):
        Question.model_validate(payload | {"question_id": f"question_{'0' * 64}"})
    with pytest.raises(ValidationError):
        Question.model_validate(payload | {"object_ids": ("mu\u0301g_1", "laptop_1")})
    with pytest.raises(ValidationError):
        Question.model_validate(payload | {"object_ids": ("\ud800", "laptop_1")})
    with pytest.raises(ValidationError):
        Question.model_validate(payload | {"object_ids": ("obj_red", "obj_red")})
