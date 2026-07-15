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

"""Public question and private oracle construction."""

from dimos.benchmark.spatiotemporal.models import OracleAnswer, Question, QuestionKind
from dimos.benchmark.spatiotemporal.relations import SpatialRelationCandidate, derive_left_of
from dimos.benchmark.spatiotemporal.utilities import SCHEMA_VERSION, stable_id


def build_spatial_question(relation: SpatialRelationCandidate) -> Question:
    """Build a public question from an accepted spatial relation."""
    accepted = derive_left_of(relation.subject, relation.object, relation.margin)
    if accepted is None or relation.predicate is not accepted.predicate:
        raise ValueError("question construction requires an accepted spatial relation")
    object_ids = (relation.subject.object_id, relation.object.object_id)
    question_id = stable_id(
        "question",
        {
            "object_ids": object_ids,
            "predicate": relation.predicate.value,
            "question_kind": QuestionKind.SPATIAL.value,
            "reference_ids": (),
            "schema_version": SCHEMA_VERSION,
        },
    )
    return Question(
        question_id=question_id,
        episode_id=relation.subject.episode_id,
        text=(f"Is the {relation.subject.label} left of the {relation.object.label} at the end?"),
        question_kind=QuestionKind.SPATIAL,
        predicate=relation.predicate,
        object_ids=object_ids,
    )


def build_spatial_oracle_answer(
    question: Question,
    relation: SpatialRelationCandidate,
) -> OracleAnswer:
    """Build the private expected answer for one accepted relation."""
    relation_question = build_spatial_question(relation)
    if (
        relation_question.question_id != question.question_id
        or relation_question.episode_id != question.episode_id
    ):
        raise ValueError("question does not match relation")
    return OracleAnswer(
        question_id=question.question_id,
        expected=True,
        evidence_frame_ids=(relation.subject.frame_id,),
    )
