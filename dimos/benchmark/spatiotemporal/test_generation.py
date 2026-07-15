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

"""Behavioral tests for dataset question generation."""

import pytest

from dimos.benchmark.spatiotemporal.generation import generate_spatial_questions
from dimos.benchmark.spatiotemporal.models import RelationFact, SpatialPredicate
from dimos.benchmark.spatiotemporal.utilities import SCHEMA_VERSION, stable_id


def test_generates_one_public_spatial_question_per_accepted_relation() -> None:
    relation_id = stable_id(
        "relation",
        {
            "object_ids": ("obj_red", "obj_blue"),
            "predicate": SpatialPredicate.LEFT_OF.value,
            "schema_version": SCHEMA_VERSION,
        },
    )
    facts = tuple(
        RelationFact(
            relation_id=relation_id,
            episode_id="episode_1",
            frame_id=frame_id,
            timestamp_s=timestamp_s,
            subject_id="obj_red",
            predicate=SpatialPredicate.LEFT_OF,
            object_id="obj_blue",
            evidence_frame_ids=(frame_id,),
        )
        for frame_id, timestamp_s in ((12, 0.5), (13, 0.6))
    )

    questions = generate_spatial_questions(facts)

    assert len(questions) == 1
    question = questions[0]
    assert (
        question.question_id
        == "question_4ef1579875e841ec7602de2e9cfc95f0bfdfb5e8d2e38ca798f462f8f72eda1e"
    )
    assert question.text == "Is obj_red left of obj_blue?"
    assert question.object_ids == ("obj_red", "obj_blue")
    public_record = question.model_dump(mode="json")
    assert (
        not {
            "relation_id",
            "frame_id",
            "timestamp_s",
            "evidence_frame_ids",
            "expected",
        }
        & public_record.keys()
    )


def test_rejects_facts_from_multiple_episodes() -> None:
    relation_id = stable_id(
        "relation",
        {
            "object_ids": ("obj_red", "obj_blue"),
            "predicate": SpatialPredicate.LEFT_OF.value,
            "schema_version": SCHEMA_VERSION,
        },
    )
    facts = tuple(
        RelationFact(
            relation_id=relation_id,
            episode_id=episode_id,
            frame_id=frame_id,
            timestamp_s=timestamp_s,
            subject_id="obj_red",
            predicate=SpatialPredicate.LEFT_OF,
            object_id="obj_blue",
            evidence_frame_ids=(frame_id,),
        )
        for episode_id, frame_id, timestamp_s in (
            ("episode_1", 12, 0.5),
            ("episode_2", 13, 0.6),
        )
    )

    with pytest.raises(ValueError, match="one episode"):
        generate_spatial_questions(facts)
