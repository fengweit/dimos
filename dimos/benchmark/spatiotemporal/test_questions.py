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

"""Tests for deterministic public question and private oracle construction."""

from dataclasses import replace

import pytest

from dimos.benchmark.spatiotemporal.models import (
    BoundingBox2D,
    ObjectObservation,
    QuestionKind,
    SpatialPredicate,
)
from dimos.benchmark.spatiotemporal.questions import (
    build_spatial_oracle_answer,
    build_spatial_question,
)
from dimos.benchmark.spatiotemporal.relations import SpatialRelationCandidate, derive_left_of


def _left_of_relation() -> SpatialRelationCandidate:
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
    return relation


def test_builds_answer_free_spatial_question_with_stable_id() -> None:
    question = build_spatial_question(_left_of_relation())

    assert (
        question.question_id
        == "question_4ef1579875e841ec7602de2e9cfc95f0bfdfb5e8d2e38ca798f462f8f72eda1e"
    )
    assert question.text == "Is the mug left of the laptop at the end?"
    assert question.question_kind is QuestionKind.SPATIAL
    assert question.predicate is SpatialPredicate.LEFT_OF
    assert question.object_ids == ("obj_red", "obj_blue")
    assert question.reference_ids == ()
    public_record = question.model_dump(mode="json")
    assert "expected" not in public_record
    assert "answer" not in public_record
    assert "evidence" not in public_record


def test_stores_expected_answer_and_evidence_only_in_private_record() -> None:
    relation = _left_of_relation()
    question = build_spatial_question(relation)

    oracle = build_spatial_oracle_answer(question, relation)

    assert oracle.question_id == question.question_id
    assert oracle.expected is True
    assert oracle.evidence_frame_ids == (12,)
    assert set(question.model_dump()) == {
        "question_id",
        "episode_id",
        "text",
        "question_kind",
        "predicate",
        "object_ids",
        "reference_ids",
    }


def test_rejects_forged_relation_candidate_during_question_construction() -> None:
    forged = replace(_left_of_relation(), margin=0.2)

    with pytest.raises(ValueError, match="accepted spatial relation"):
        build_spatial_question(forged)


def test_rejects_private_oracle_for_an_unrelated_relation() -> None:
    relation = _left_of_relation()
    question = build_spatial_question(relation)
    other_relation = derive_left_of(
        relation.subject.model_copy(update={"object_id": "obj_green"}),
        relation.object.model_copy(update={"object_id": "obj_yellow"}),
        relation.margin,
    )
    assert other_relation is not None

    with pytest.raises(ValueError, match="question does not match relation"):
        build_spatial_oracle_answer(question, other_relation)
