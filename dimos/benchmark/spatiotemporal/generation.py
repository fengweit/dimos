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

"""Deterministic public question generation from accepted relation facts."""

from collections.abc import Sequence

from dimos.benchmark.spatiotemporal.models import Question, QuestionKind, RelationFact
from dimos.benchmark.spatiotemporal.utilities import SCHEMA_VERSION, stable_id


def generate_spatial_questions(facts: Sequence[RelationFact]) -> tuple[Question, ...]:
    """Generate one answer-free public question per accepted spatial relation."""
    if len({fact.episode_id for fact in facts}) > 1:
        raise ValueError("spatial questions must be generated from one episode")

    questions: dict[str, Question] = {}
    for fact in facts:
        object_ids = (fact.subject_id, fact.object_id)
        question_id = stable_id(
            "question",
            {
                "object_ids": object_ids,
                "predicate": fact.predicate.value,
                "question_kind": QuestionKind.SPATIAL.value,
                "reference_ids": (),
                "schema_version": SCHEMA_VERSION,
            },
        )
        questions.setdefault(
            question_id,
            Question(
                question_id=question_id,
                episode_id=fact.episode_id,
                text=f"Is {fact.subject_id} {fact.predicate.value.replace('-', ' ')} {fact.object_id}?",
                question_kind=QuestionKind.SPATIAL,
                predicate=fact.predicate,
                object_ids=object_ids,
            ),
        )
    return tuple(questions[question_id] for question_id in sorted(questions))
