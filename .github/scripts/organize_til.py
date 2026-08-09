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


def organize_til():
    # 루트에 있는 Markdown 파일 중 README가 아닌 파일을 찾는다.
    for file_path in ROOT.glob("*.md"):
        if file_path.name == "README.md":
            continue

        category = get_category(file_path)

        if not category:
            continue

        category_dir = ROOT / category
        category_dir.mkdir(exist_ok=True)

        destination = category_dir / file_path.name

        shutil.move(str(file_path), str(destination))

        print(f"Moved: {file_path} -> {destination}")

    update_readme()


def update_readme():
    # 루트에 존재하는 디렉터리를 카테고리로 사용한다.
    categories = sorted(
        directory.name
        for directory in ROOT.iterdir()
        if directory.is_dir()
        and not directory.name.startswith(".")
    )

    index = "\n".join(
        f"- [{category}](./{category}/)"
        for category in categories
    )

    readme = README.read_text(encoding="utf-8")

    pattern = (
        re.escape(INDEX_START)
        + r".*?"
        + re.escape(INDEX_END)
    )

    replacement = (
        f"{INDEX_START}\n\n"
        f"{index}\n\n"
        f"{INDEX_END}"
    )

    updated_readme = re.sub(
        pattern,
        replacement,
        readme,
        flags=re.DOTALL
    )

    README.write_text(updated_readme, encoding="utf-8")


if __name__ == "__main__":
    organize_til()