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

"""Tests for the one-command spatiotemporal video-QA demonstration."""

import inspect
from pathlib import Path

import cv2
import numpy as np
import pytest

from dimos.benchmark.spatiotemporal.demo import (
    TimestampScriptedPublicVlModel,
    _run_temporal_memory_candidate,
    _trim_video,
    run_demo,
)
from dimos.msgs.sensor_msgs.Image import Image


def test_scripted_candidate_answer_depends_only_on_public_question() -> None:
    model = TimestampScriptedPublicVlModel()
    image = Image.from_numpy(np.zeros((2, 2, 3), dtype=np.uint8))
    question = "Did relation_a happen before relation_b?"
    first = model.query(
        image,
        f'**Question:** {question}\n**Context:** {{"timestamp": 1}}',
    )
    second = model.query(
        image,
        f'**Question:** {question}\n**Context:** {{"timestamp": 999}}',
    )

    assert first == second
    assert first in {"yes", "no"}


@pytest.mark.parametrize("duration_s", [14, 31])
def test_demo_rejects_video_outside_constrained_duration(duration_s: int) -> None:
    with pytest.raises(ValueError, match="between 15 and 30 seconds"):
        run_demo(
            Path("not-opened.mp4"),
            Path("not-created"),
            duration_s=duration_s,
        )


def test_candidate_boundary_accepts_no_private_bundle() -> None:
    assert tuple(inspect.signature(_run_temporal_memory_candidate).parameters) == (
        "video",
        "questions",
        "output_root",
        "duration_s",
    )


def test_invalid_stride_has_no_output_side_effect(tmp_path: Path) -> None:
    output_root = tmp_path / "output"
    with pytest.raises(ValueError, match="stride must be positive"):
        run_demo(Path("not-opened.mp4"), output_root, frame_stride=0)
    assert not output_root.exists()


def test_demo_rejects_symlinked_output_root(tmp_path: Path) -> None:
    source = tmp_path / "source.mp4"
    source.write_bytes(b"not decoded")
    actual_output = tmp_path / "actual"
    actual_output.mkdir()
    linked_output = tmp_path / "linked"
    linked_output.symlink_to(actual_output, target_is_directory=True)

    with pytest.raises(ValueError, match="contains a symlink"):
        run_demo(source, linked_output)


def test_demo_rejects_source_target_alias(tmp_path: Path) -> None:
    output_root = tmp_path / "output"
    output_root.mkdir()
    source = output_root / "office_robot_25s.mp4"
    source.write_bytes(b"not decoded")

    with pytest.raises(ValueError, match="paths must differ"):
        run_demo(source, output_root)


def test_demo_rejects_symlinked_summary_artifact(tmp_path: Path) -> None:
    source = tmp_path / "source.mp4"
    source.write_bytes(b"not decoded")
    output_root = tmp_path / "output"
    output_root.mkdir()
    outside = tmp_path / "outside.json"
    (output_root / "summary.json").symlink_to(outside)

    with pytest.raises(ValueError, match="contains a symlink"):
        run_demo(source, output_root)
    assert not outside.exists()


def test_trim_rejects_hard_link_source_target_alias(tmp_path: Path) -> None:
    source = tmp_path / "source.mp4"
    source.write_bytes(b"must remain unchanged")
    target = tmp_path / "target.mp4"
    target.hardlink_to(source)

    with pytest.raises(ValueError, match="paths must differ"):
        _trim_video(source, target, 15.0)
    assert source.read_bytes() == b"must remain unchanged"


def test_trim_rejects_silent_video_writer_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source.mp4"
    source.write_bytes(b"source placeholder")
    target = tmp_path / "target.mp4"

    class SourceCapture:
        def __init__(self) -> None:
            self.reads = 0

        def isOpened(self) -> bool:
            return True

        def get(self, prop: int) -> float:
            return {
                cv2.CAP_PROP_FPS: 1.0,
                cv2.CAP_PROP_FRAME_WIDTH: 2.0,
                cv2.CAP_PROP_FRAME_HEIGHT: 2.0,
            }.get(prop, 0.0)

        def read(self) -> tuple[bool, np.ndarray | None]:
            self.reads += 1
            return True, np.zeros((2, 2, 3), dtype=np.uint8)

        def release(self) -> None:
            return None

    class VerificationCapture:
        def isOpened(self) -> bool:
            return True

        def read(self) -> tuple[bool, None]:
            return False, None

        def release(self) -> None:
            return None

    class SilentWriter:
        def isOpened(self) -> bool:
            return True

        def write(self, frame: np.ndarray) -> None:
            return None

        def release(self) -> None:
            return None

    captures = iter((SourceCapture(), VerificationCapture()))
    monkeypatch.setattr(cv2, "VideoCapture", lambda _: next(captures))
    monkeypatch.setattr(cv2, "VideoWriter", lambda *args: SilentWriter())

    with pytest.raises(RuntimeError, match="0 decodable frames"):
        _trim_video(source, target, 15.0)
