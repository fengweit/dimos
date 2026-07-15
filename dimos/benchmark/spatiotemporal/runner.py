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

"""Candidate evaluation runner helpers."""

from dimos.benchmark.spatiotemporal.models import (
    Prediction,
    PredictionStatus,
    QuestionId,
)


def parse_candidate_prediction(
    question_id: QuestionId,
    raw_answer: str | bool | None,
    expected: bool,
) -> tuple[PredictionStatus, Prediction | None]:
    """Parse one candidate answer and classify it against private truth."""
    if raw_answer is None:
        return PredictionStatus.MISSING, None
    if isinstance(raw_answer, bool):
        answer = raw_answer
    elif raw_answer == "yes":
        answer = True
    elif raw_answer == "no":
        answer = False
    else:
        return PredictionStatus.INVALID, None

    prediction = Prediction(question_id=question_id, answer=answer)
    status = PredictionStatus.CORRECT if answer is expected else PredictionStatus.INCORRECT
    return status, prediction
