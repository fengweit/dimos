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

"""End-to-end tracer for the first spatiotemporal QA behavior."""

from dimos.benchmark.spatiotemporal.models import BoundingBox2D, ObjectObservation, Prediction
from dimos.benchmark.spatiotemporal.questions import (
    build_spatial_oracle_answer,
    build_spatial_question,
)
from dimos.benchmark.spatiotemporal.relations import derive_left_of
from dimos.benchmark.spatiotemporal.scoring import score_prediction
from dimos.benchmark.spatiotemporal.utilities import canonical_model_json


def test_observations_flow_to_public_question_private_oracle_and_score() -> None:
    mug = ObjectObservation(
        episode_id="episode_1",
        frame_id=12,
        timestamp_s=0.5,
        object_id="obj_red",
        label="mug",
        box=BoundingBox2D(x_min=0.1, y_min=0.2, x_max=0.3, y_max=0.5),
        confidence=0.9,
    )
    laptop = ObjectObservation(
        episode_id="episode_1",
        frame_id=12,
        timestamp_s=0.5,
        object_id="obj_blue",
        label="laptop",
        box=BoundingBox2D(x_min=0.5, y_min=0.2, x_max=0.8, y_max=0.6),
        confidence=0.9,
    )

    relation = derive_left_of(mug, laptop, margin=0.1)
    assert relation is not None
    question = build_spatial_question(relation)
    oracle = build_spatial_oracle_answer(question, relation)
    prediction = Prediction(question_id=question.question_id, answer=True)
    result = score_prediction(question, oracle, prediction)

    assert result.correct is True
    assert canonical_model_json(question) == canonical_model_json(question)
    assert "expected" not in question.model_dump()
    assert "evidence_frame_ids" not in question.model_dump()
