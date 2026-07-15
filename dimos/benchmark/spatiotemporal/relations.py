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

"""Image-plane relation derivation."""

from dataclasses import dataclass
from math import isfinite

from dimos.benchmark.spatiotemporal.models import ObjectObservation, SpatialPredicate


@dataclass(frozen=True)
class SpatialRelationCandidate:
    """A temporary accepted relation backed by two observations."""

    subject: ObjectObservation
    predicate: SpatialPredicate
    object: ObjectObservation
    margin: float


def derive_left_of(
    subject: ObjectObservation,
    object_: ObjectObservation,
    margin: float,
) -> SpatialRelationCandidate | None:
    """Derive an accepted left-of candidate when evidence is sufficient."""
    if not isfinite(margin) or not 0.0 <= margin <= 1.0:
        raise ValueError("margin must be finite and within [0, 1]")
    subject_sample = (subject.episode_id, subject.frame_id, subject.timestamp_s)
    object_sample = (object_.episode_id, object_.frame_id, object_.timestamp_s)
    if subject_sample != object_sample:
        raise ValueError("relations require observations from the same sample")
    if subject.object_id == object_.object_id:
        return None
    if subject.box.x_max + margin < object_.box.x_min:
        return SpatialRelationCandidate(
            subject=subject,
            predicate=SpatialPredicate.LEFT_OF,
            object=object_,
            margin=margin,
        )
    return None
