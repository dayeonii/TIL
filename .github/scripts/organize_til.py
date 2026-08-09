from pathlib import Path
import re
import shutil

ROOT = Path(".")
README = ROOT / "README.md"

INDEX_START = "<!-- TIL_INDEX_START -->"
INDEX_END = "<!-- TIL_INDEX_END -->"


def get_category(file_path):
    content = file_path.read_text(encoding="utf-8")

    match = re.search(
        r"^category:\s*(.+)$",
        content,
        re.MULTILINE
    )

    if not match:
        return None

    return match.group(1).strip()


def get_title(file_path):
    content = file_path.read_text(encoding="utf-8")

    match = re.search(
        r"^title:\s*(.+)$",
        content,
        re.MULTILINE
    )

    if match:
        return match.group(1).strip()

    return file_path.stem


def organize_til():
    for file_path in ROOT.glob("*.md"):
        # README는 TIL이 아니므로 제외
        if file_path.name == "README.md":
            continue

        category = get_category(file_path)

        # category가 없는 파일은 건너뜀
        if not category:
            continue

        category_dir = ROOT / category
        category_dir.mkdir(exist_ok=True)

        destination = category_dir / file_path.name

        shutil.move(str(file_path), str(destination))

        print(f"Moved: {file_path} -> {destination}")


if __name__ == "__main__":
    organize_til()