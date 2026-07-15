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

"""Exact scoring for typed spatiotemporal predictions."""

from dimos.benchmark.spatiotemporal.models import OracleAnswer, Prediction, Question, QuestionResult


def score_prediction(
    question: Question,
    oracle: OracleAnswer,
    prediction: Prediction,
) -> QuestionResult:
    """Score one typed prediction against separately supplied private truth."""
    if len({question.question_id, oracle.question_id, prediction.question_id}) != 1:
        raise ValueError("question IDs must match for scoring")
    return QuestionResult(
        question_id=question.question_id,
        expected=oracle.expected,
        predicted=prediction.answer,
        correct=prediction.answer is oracle.expected,
    )
