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

"""Tests for image-plane relation derivation."""

import pytest

from dimos.benchmark.spatiotemporal import relations
from dimos.benchmark.spatiotemporal.models import BoundingBox2D, ObjectObservation, SpatialPredicate
from dimos.benchmark.spatiotemporal.relations import derive_left_of


def _observation(object_id: str, label: str, box: BoundingBox2D) -> ObjectObservation:
    return ObjectObservation(
        episode_id="episode_1",
        frame_id=12,
        timestamp_s=0.5,
        object_id=object_id,
        label=label,
        box=box,
        confidence=0.9,
    )


def test_accepts_left_of_relation_only_above_strict_margin() -> None:
    mug = _observation(
        "mug_1",
        "mug",
        BoundingBox2D(x_min=0.1, y_min=0.2, x_max=0.3, y_max=0.5),
    )
    laptop = _observation(
        "laptop_1",
        "laptop",
        BoundingBox2D(x_min=0.5, y_min=0.2, x_max=0.8, y_max=0.6),
    )

    relation = derive_left_of(mug, laptop, margin=0.1)

    assert relation is not None
    assert relation.subject is mug
    assert relation.predicate is SpatialPredicate.LEFT_OF
    assert relation.object is laptop
    assert relation.margin == 0.1
    assert derive_left_of(mug, laptop, margin=0.2 - 1e-12) is not None
    assert derive_left_of(mug, laptop, margin=0.2) is None
    assert derive_left_of(mug, laptop, margin=0.2 + 1e-12) is None


def test_right_of_is_left_of_with_arguments_swapped() -> None:
    mug = _observation(
        "mug_1",
        "mug",
        BoundingBox2D(x_min=0.1, y_min=0.2, x_max=0.3, y_max=0.5),
    )
    laptop = _observation(
        "laptop_1",
        "laptop",
        BoundingBox2D(x_min=0.5, y_min=0.2, x_max=0.8, y_max=0.6),
    )

    relation = relations.derive_right_of(laptop, mug, margin=0.1)

    assert relation is not None
    assert relation.subject is laptop
    assert relation.predicate is SpatialPredicate.RIGHT_OF
    assert relation.object is mug
    assert relations.derive_right_of(mug, laptop, margin=0.1) is None


def test_vertical_predicates_are_strict_inverses() -> None:
    lamp = _observation(
        "lamp_1",
        "lamp",
        BoundingBox2D(x_min=0.2, y_min=0.1, x_max=0.5, y_max=0.3),
    )
    table = _observation(
        "table_1",
        "table",
        BoundingBox2D(x_min=0.1, y_min=0.6, x_max=0.9, y_max=0.8),
    )

    above = relations.derive_above(lamp, table, margin=0.2)
    below = relations.derive_below(table, lamp, margin=0.2)

    assert above is not None
    assert above.predicate is SpatialPredicate.ABOVE
    assert below is not None
    assert below.predicate is SpatialPredicate.BELOW
    assert relations.derive_above(table, lamp, margin=0.2) is None
    assert relations.derive_below(lamp, table, margin=0.2) is None
    assert relations.derive_above(lamp, table, margin=0.3) is None
    assert relations.derive_below(table, lamp, margin=0.3) is None


def test_rejects_invalid_margin_and_cross_sample_comparisons() -> None:
    mug = _observation(
        "mug_1",
        "mug",
        BoundingBox2D(x_min=0.1, y_min=0.2, x_max=0.3, y_max=0.5),
    )
    laptop = _observation(
        "laptop_1",
        "laptop",
        BoundingBox2D(x_min=0.5, y_min=0.2, x_max=0.8, y_max=0.6),
    )

    for invalid_margin in (-0.1, 1.1, float("nan"), float("inf")):
        with pytest.raises(ValueError, match="margin"):
            derive_left_of(mug, laptop, margin=invalid_margin)

    for update in (
        {"episode_id": "episode_2"},
        {"frame_id": 13},
        {"timestamp_s": 0.6},
    ):
        other_sample = laptop.model_copy(update=update)
        with pytest.raises(ValueError, match="same sample"):
            derive_left_of(mug, other_sample, margin=0.1)


def test_same_object_identity_never_produces_a_relation() -> None:
    left = _observation(
        "mug_1",
        "mug",
        BoundingBox2D(x_min=0.1, y_min=0.2, x_max=0.3, y_max=0.5),
    )
    right = _observation(
        "mug_1",
        "mug",
        BoundingBox2D(x_min=0.5, y_min=0.2, x_max=0.8, y_max=0.6),
    )

    assert derive_left_of(left, right, margin=0.1) is None
