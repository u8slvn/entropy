from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import shutil

from collections import defaultdict
from pathlib import Path
from typing import Any


FILE_EXT = ".entropy"

ROOT = Path(__file__).parent.parent.resolve()
DEFAULT_DIR = ROOT / "story"
OUTPUT = ROOT / "entropy/story"

uuid_cache = {}


def generate_uuid(value: str) -> str:
    """
    Generate unique ID for a given string. If the given string is "end" return it as is,
    "end" is used to mark the end of a chapter.
    """
    if value == "end":
        return value

    return hashlib.md5(value.encode()).hexdigest()


def save_story_file(filename: str, content: Any):
    """Save story file to destination dir."""
    filepath = OUTPUT / f"{filename}{FILE_EXT}"
    with open(filepath, "w") as file:
        json.dump(content, file, indent=4)
    print(f'"{filepath}" generated.')


def parse_chapter_data(chapter_data: list[list[dict[str, Any]]]):
    """Parse each chapter data and transform it."""
    rv = {}
    for scene_data in chapter_data:
        for node_data in scene_data:
            node_data["uuid"] = generate_uuid(node_data["uuid"])
            node_data["next_uuid"] = generate_uuid(node_data["next_uuid"])

            if "entrypoint" in node_data:
                rv["entrypoint"] = node_data["uuid"]
                del node_data["entrypoint"]

    nodes = list(itertools.chain.from_iterable(chapter_data))
    rv["nodes"] = {node["uuid"]: node for node in nodes}

    return rv


def is_json_file(filepath: Path) -> bool:
    """Check if the given filepath is a JSON file."""
    return filepath.is_file() and filepath.suffix == ".json"


def load_chapters_data(story_path: Path) -> dict[str, list[dict[str:Any]]]:
    """
    Walk through the given directory and load every directory within as chapters.
    All the JSON files from each chapter directories are loaded and concatenate
    together.
    """
    chapters_data = defaultdict(list)

    chapters = [item for item in story_path.iterdir() if item.is_dir()]
    for chapter in chapters:
        scenes = [file for file in chapter.iterdir() if is_json_file(file)]

        for scene in scenes:
            with open(scene, "r") as scene_data:
                chapters_data[chapter.name].append(json.load(scene_data))

    return chapters_data


def build_story(dir_path: Path) -> None:
    """Build story files."""
    chapters_data = load_chapters_data(dir_path)

    main_content = {}
    for chapter_name, chapter_data in chapters_data.items():
        chapter_content = parse_chapter_data(chapter_data)

        # Save generated nodes to chapter config file.
        save_story_file(chapter_name, chapter_content.pop("nodes"))

        main_content[chapter_name] = chapter_content

    # Save index chapter file.
    save_story_file("index", main_content)


def dir_path_arg(value: str) -> Path:
    """
    Check if the given string argument is a valid directory path and return it as
    Path if true.
    """
    path = Path(value)
    if path.is_dir():
        return path
    raise argparse.ArgumentTypeError(f"Story builder: '{value}' is not a valid path.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=dir_path_arg, default=DEFAULT_DIR)
    parsed_args = parser.parse_args()

    # Cleanup output dir before generating the story files.
    shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(exist_ok=True)

    build_story(parsed_args.path)
