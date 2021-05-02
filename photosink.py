import re
import os
import json
import pathlib
import shutil
from pathlib import Path


ROOT_PATH = Path().cwd().resolve()
ALBUM_PATH = Path(ROOT_PATH, "albums")
OUTPUT_PATH = Path("./_site").resolve()


def main() -> None:
    root_path = Path(ALBUM_PATH)
    traverse_dir(root_path)
    shutil.copyfile("./templates/index.html", str(Path(OUTPUT_PATH, "index.html")))


def traverse_dir(path: Path) -> None:
    # Traverse child directories
    dir = {}
    dir["name"] = path.name
    dir["albums"] = []
    dir["images"] = []
    out_path = str(path).replace(str(ALBUM_PATH), str(OUTPUT_PATH))
    if not os.path.exists(out_path):
        print(f"Creating {out_path}")
        os.makedirs(out_path)
    for node in [node for node in path.iterdir() if node.is_dir()]:
        dir["albums"].append(node.name)
        traverse_dir(node)
    # Handle images
    for node in [node for node in path.iterdir() if not node.is_dir()]:
        if re.search("\.jpe?g$", str(node.name), re.IGNORECASE):
            resize_image(node, Path(out_path))
            dir["images"].append(node.name)
    with open(str(Path(out_path, "index.json")), "w") as fd:
        fd.write(json.dumps(dir))


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
