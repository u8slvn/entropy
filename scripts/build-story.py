from __future__ import annotations

import itertools
import json

from pathlib import Path


ROOT = Path(__file__).parent.parent.resolve()
STORY = ROOT / "story"
OUTPUT = ROOT / "entropy/story"

OUTPUT.mkdir(exist_ok=True)

print(f"Building story from '{STORY}'...")

mainfile = STORY / "main.json"
with open(mainfile, "r") as file:
    main = json.load(file)

for key, value in main.items():
    nodes = []
    chapter_dir = STORY.joinpath(key)
    for filepath in chapter_dir.glob("*"):
        with open(filepath, "r") as file:
            nodes.append(json.load(file))

    output_file = f"{chapter_dir.name}.json"
    with open(OUTPUT / output_file, "w") as file:
        json.dump(list(itertools.chain.from_iterable(nodes)), file, indent=4)
        print(f"  * {chapter_dir.name} built.")
    value["configfile"] = output_file

with open(OUTPUT / "main.json", "w") as file:
    print("  * Chapters config built.")
    json.dump(main, file, indent=4)


def build_story() -> None: ...


if __name__ == "__main__":
    build_story()
