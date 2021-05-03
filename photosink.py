import re
import os
import json
import pathlib
import shutil
import random
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT_PATH = Path().cwd().resolve()
ALBUM_PATH = Path(ROOT_PATH, "albums")
OUTPUT_PATH = Path("./_site").resolve()

j2env = Environment(
    loader=FileSystemLoader("./templates")
)

def main() -> None:
    root_path = Path(ALBUM_PATH)
    print(json.dumps(traverse_dir(root_path), indent=4))

def traverse_dir(path: Path):
    # Traverse child directories
    dir = {}
    dir["name"] = "Photos!" if (path == ALBUM_PATH) else path.name
    dir["albums"] = []
    dir["images"] = []
    out_path = str(path).replace(str(ALBUM_PATH), str(OUTPUT_PATH))
    if not os.path.exists(out_path):
        print(f"Creating {out_path}")
        os.makedirs(out_path)
    for node in [node for node in path.iterdir() if node.is_dir()]:
        dir["albums"].append(traverse_dir(node))
    # Handle images
    for node in [node for node in path.iterdir() if not node.is_dir()]:
        if re.search("\.jpe?g$", str(node.name), re.IGNORECASE):
            resize_image(node, Path(out_path))
            dir["images"].append(node.name)
    dir["thumb"] = dir["images"][0]
    with open(str(Path(out_path, "index.html")), "w") as fd:
        fd.write(j2env.get_template("index.html").render(name = dir["name"], albums=dir["albums"], images=dir["images"]))
    return dir


def resize_image(image: Path, out_path: Path) -> None:
    if re.search("\.jpe?g$", str(image), re.IGNORECASE):
        original_path = str(image)
        site_path = str(Path(out_path, image.name))
        if not os.path.exists(site_path) or os.path.getmtime(
            original_path
        ) > os.path.getmtime(site_path):
            print(f"Copying {original_path} -> {site_path}")
            shutil.copyfile(original_path, site_path)


if __name__ == "__main__":
    main()
