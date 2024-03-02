from __future__ import annotations

import itertools
import json

from pathlib import Path


ROOT = Path(__file__).parent.parent.resolve()
STORY = ROOT / "story"
OUTPUT = ROOT / "entropy/story"

OUTPUT.mkdir(exist_ok=True)

for chapter in STORY.glob("*"):
    json_files = []
    for filepath in chapter.glob("*.json"):
        with open(filepath, "r") as file:
            json_files.append(json.load(file))

    with open(OUTPUT / f"{chapter.name}.json", "w") as file:
        json.dump(list(itertools.chain.from_iterable(json_files)), file, indent=4)
