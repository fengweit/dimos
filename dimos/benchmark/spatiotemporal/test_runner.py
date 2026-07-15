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

"""Tests for parsing candidate answers into typed prediction outcomes."""

import pytest

from dimos.benchmark.spatiotemporal.models import PredictionStatus
from dimos.benchmark.spatiotemporal.runner import parse_candidate_prediction

QUESTION_ID = "question_4ef1579875e841ec7602de2e9cfc95f0bfdfb5e8d2e38ca798f462f8f72eda1e"


@pytest.mark.parametrize(
    ("raw_answer", "expected", "expected_status", "expected_prediction"),
    (
        (True, True, PredictionStatus.CORRECT, True),
        (False, True, PredictionStatus.INCORRECT, False),
        ("yes", True, PredictionStatus.CORRECT, True),
        ("no", False, PredictionStatus.CORRECT, False),
        (None, True, PredictionStatus.MISSING, None),
        ("true", True, PredictionStatus.INVALID, None),
        ("yes, definitely", True, PredictionStatus.INVALID, None),
    ),
)
def test_parses_only_boolean_and_explicit_yes_no_answers(
    raw_answer: str | bool | None,
    expected: bool,
    expected_status: PredictionStatus,
    expected_prediction: bool | None,
) -> None:
    status, prediction = parse_candidate_prediction(QUESTION_ID, raw_answer, expected)

    assert status is expected_status
    if expected_prediction is None:
        assert prediction is None
    else:
        assert prediction is not None
        assert prediction.question_id == QUESTION_ID
        assert prediction.answer is expected_prediction
