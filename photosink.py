import pathlib
from pathlib import Path


def main() -> None:
    root_path = Path("./albums")
    traverse_dir(root_path)


def traverse_dir(path: Path) -> None:
    print(str(path))
    # Traverse child directories
    for node in [node for node in path.iterdir() if node.is_dir()]:
        if node.is_dir():
            traverse_dir(node)
    # Handle images
    for node in [node for node in path.iterdir() if not node.is_dir()]:
        print(node)


if __name__ == "__main__":
    main()
