from __future__ import annotations

import argparse

from pathlib import Path

import pytest

from scripts.build_story import dir_path_arg
from scripts.build_story import is_json_file
from scripts.build_story import load_chapters_data
from scripts.build_story import parse_chapter_data
from tests.scripts.conftest import DATAFIXTURES


@pytest.mark.parametrize(
    "filepath, result",
    (
        (DATAFIXTURES / "test-json.json", True),
        (DATAFIXTURES / "test-txt.txt", False),
    ),
)
def test_is_jon_file(filepath, result):
    assert is_json_file(filepath) is result


def test_dir_path_arg_returns_path():
    dir_path = str(DATAFIXTURES.joinpath("test_story"))

    assert isinstance(dir_path_arg(dir_path), Path)


def test_dir_path_arg_raises_with_wrong_path_arg():
    dir_path = "wrong-path"

    with pytest.raises(argparse.ArgumentTypeError):
        dir_path_arg(dir_path)


def test_load_chapters_data():
    story_dir = DATAFIXTURES / "test_story"

    result = load_chapters_data(story_dir)

    expected = {
        "test-chapter01": [
            [{"test": "test chapter 01 scene 01"}],
            [{"test": "test chapter 01 scene 02"}],
        ],
        "test-chapter02": [
            [{"test": "test chapter 02 scene 01"}],
        ],
    }
    assert result == expected


def test_parse_chapter_data():
    chapter_data = [
        [{"uuid": "node01", "next_uuid": "node02", "entrypoint": True}],
        [{"uuid": "node02", "next_uuid": "end"}],
    ]

    result = parse_chapter_data(chapter_data)

    expected = {
        "entrypoint": "705cc8c4aab2c0dfb3a3f280da16760d",
        "nodes": {
            "705cc8c4aab2c0dfb3a3f280da16760d": {
                "next_uuid": "f43c51286fe1559c6253e0b37ec045c6",
                "uuid": "705cc8c4aab2c0dfb3a3f280da16760d",
            },
            "f43c51286fe1559c6253e0b37ec045c6": {
                "next_uuid": "end",
                "uuid": "f43c51286fe1559c6253e0b37ec045c6",
            },
        },
    }

    assert result == expected
