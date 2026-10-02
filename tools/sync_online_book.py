from __future__ import annotations

import re
import shutil
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"
BOOK_DIR = ROOT / "book"
DOCS_DIR = BOOK_DIR / "docs"
CHAPTERS_OUT = DOCS_DIR / "chapters"
ASSETS_OUT = DOCS_DIR / "assets"

CHAPTER_COUNT = 12
PUBLIC_ASSETS_MANIFEST = CHAPTERS_DIR / "public_assets.tsv"
ALLOWED_ASSET_SUFFIXES = {".md", ".txt", ".log", ".py", ".sh", ".ps1", ".csv", ".tsv", ".json", ".yaml", ".yml", ".svg", ".png", ".jpg", ".jpeg", ".pdb", ".cif", ".sdf", ".mol2", ".pdbqt", ".gro", ".top", ".itp", ".mdp", ".ndx", ".xtc", ".trr", ".tpr", ".cpt", ".edr", ".xvg", ".xpm", ".dat", ".npz", ".toml", ".cxc", ".pml", ".pse", ".fasta", ".fa", ".gz"}
ALLOWED_SOURCE_TYPES = {"independent_script", "independent_run", "original_diagram", "public_structure", "official_example", "teaching_constructed", "teaching_template", "legacy_reviewed"}
SOURCE_SECTION_HEADINGS = (
    "## 使用材料与来源边界",
    "## 材料使用说明",
)
AUTHOR_TODO_HEADINGS = (
    "## 待作者确认项",
    "## 待确认项",
)


def safe_rmtree(path: Path) -> None:
    resolved = path.resolve()
    root = ROOT.resolve()
    if root != resolved and root not in resolved.parents:
        raise RuntimeError(f"Refusing to delete outside workspace: {path}")
    if path.exists():
        shutil.rmtree(path)


def first_heading(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("Missing top-level heading")


def strip_section(markdown: str, heading: str) -> str:
    pattern = rf"(^|\n){re.escape(heading)}\n.*?(?=\n## |\Z)"
    return re.sub(pattern, "\n", markdown, flags=re.DOTALL)


def strip_chapter_02_source_table(markdown: str) -> str:
    pattern = (
        r"\n本章正文依据全书大纲、第二章本章大纲、.*?"
        r"(?=\n本章采用一个固定贯穿案例)"
    )
    return re.sub(pattern, "\n", markdown, flags=re.DOTALL)


def strip_author_material(markdown: str) -> str:
    for heading in SOURCE_SECTION_HEADINGS + AUTHOR_TODO_HEADINGS:
        markdown = strip_section(markdown, heading)
    markdown = strip_chapter_02_source_table(markdown)
    markdown = re.sub(
        r"\n本章待作者确认.*?(?=\n## |\Z)",
        "\n",
        markdown,
        flags=re.DOTALL,
    )
    return markdown


def rewrite_paths(markdown: str, chapter_id: str) -> str:
    # Only links move into the publication tree. Commands keep the directory
    # layout used by the student download helper.
    def rewrite_link(match: re.Match) -> str:
        href = match.group(2)
        if href.startswith("assets/"):
            href = f"../assets/{chapter_id}/" + href[len("assets/"):]
        else:
            href = re.sub(r"^(?:\.\./|chapters/)(chapter-\d{2})/assets/", r"../assets/\1/", href)
        return match.group(1) + href + match.group(3)

    markdown = re.sub(r"(!?\[[^\]]*\]\()([^\)]+)(\))", rewrite_link, markdown)
    markdown = markdown.replace(
        "06_原始学习素材/第五章/boltz2在线/boltz2_parsed/summary.json",
        "runs/chapter-08/boltz2_parsed/summary.json",
    )
    markdown = re.sub(
        r"06_原始学习素材/[^\s`|)]+",
        "本地原始素材目录（不随在线书发布）",
        markdown,
    )
    markdown = markdown.replace("06_原始学习素材/", "本地原始素材目录（不随在线书发布）/")
    return markdown


def render_chapter(chapter_number: int) -> tuple[str, str, str]:
    chapter_id = f"chapter-{chapter_number:02d}"
    src = CHAPTERS_DIR / chapter_id / "正文.md"
    if not src.exists():
        raise FileNotFoundError(src)

    text = src.read_text(encoding="utf-8")
    title = first_heading(text)
    text = strip_author_material(text)
    text = rewrite_paths(text, chapter_id)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    return chapter_id, title, text


def publish_chapter(chapter_number: int) -> tuple[str, str]:
    chapter_id, title, text = render_chapter(chapter_number)
    (CHAPTERS_OUT / f"{chapter_id}.md").write_text(text, encoding="utf-8")
    return chapter_id, title


def public_assets(manifest: Path = PUBLIC_ASSETS_MANIFEST) -> list[tuple[Path, Path]]:
    if not manifest.is_file():
        raise FileNotFoundError(f"Public asset allowlist is required: {manifest}")
    approved = []
    seen = set()
    with manifest.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            relative = row["file_path"].replace("\\", "/")
            path = Path(relative)
            if not re.fullmatch(r"(?:chapter-\d{2}|shared)/assets/.+", relative) or ".." in path.parts or path.is_absolute():
                raise ValueError(f"Invalid asset path: {relative}")
            source = (CHAPTERS_DIR / path).resolve()
            if CHAPTERS_DIR.resolve() not in source.parents or not source.is_file():
                raise ValueError(f"Missing or escaped asset: {relative}")
            if source.suffix.lower() not in ALLOWED_ASSET_SUFFIXES or (source.suffix == ".gz" and not relative.endswith(".cif.gz")):
                raise ValueError(f"Unsupported public asset type: {relative}")
            if row.get("source_type") not in ALLOWED_SOURCE_TYPES:
                raise ValueError(f"Unapproved source type: {relative}")
            if relative in seen:
                raise ValueError(f"Duplicate public asset: {relative}")
            seen.add(relative)
            expected_hash = row.get("sha256", "").strip()
            if not re.fullmatch(r"[0-9a-f]{64}", expected_hash) or not row.get("validation_status", "").strip():
                raise ValueError(f"Asset review record is incomplete: {relative}")
            if hashlib.sha256(source.read_bytes()).hexdigest() != expected_hash:
                raise ValueError(f"Asset changed after review: {relative}")
            dest = ASSETS_OUT / path.parts[0] / Path(*path.parts[2:])
            approved.append((source, dest))
    return approved


def publish_assets(approved: list[tuple[Path, Path]]) -> None:
    for source, destination in approved:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def write_index(chapters: list[tuple[str, str]]) -> None:
    student_index = CHAPTERS_DIR / "学习指南.md"
    if student_index.is_file():
        (DOCS_DIR / "index.md").write_text(student_index.read_text(encoding="utf-8"), encoding="utf-8")
        write_resources(chapters)
        return
    lines = [
        "# AI 辅助药物设计：从分子建模到研究工作台",
        "",
        "本在线图书整理自当前 12 章教材正文，面向药物化学、药学和生命科学方向的课程学习者。页面只发布 `chapters/chapter-XX/正文.md` 生成的读者内容，不发布各章写作大纲、原始课件、PDF、Office 文件、压缩包或本地原始学习素材。",
        "",
        "整本书采用蓝白配色：白色阅读背景、蓝色导航与链接、浅蓝提示框。正文中的计算分数、模型输出和文献案例均按候选证据处理，不能直接替代实验验证。",
        "",
        "## 章节目录",
        "",
    ]
    for chapter_id, title in chapters:
        lines.append(f"- [{title}](chapters/{chapter_id}.md)")
    lines.extend(
        [
            "",
            "## 阅读方式",
            "",
            "建议按章节顺序阅读。第 1-4 章建立环境、结构和对接基础；第 5-8 章处理模拟、自由能和 AI 亲和力预测；第 9-11 章进入生成式蛋白设计和 AI Agent 工作流；第 12 章把工具链收束到研究路线和项目工作台。",
            "",
        ]
    )
    (DOCS_DIR / "index.md").write_text("\n".join(lines), encoding="utf-8")


def write_resources(chapters: list[tuple[str, str]]) -> None:
    lines = ["# 练习资源", "", "按[首页下载步骤](index.md#practice-download)，将[练习下载器](assets/shared/get-practice.py)保存到课程目录，用 Python 下载整章及其配套文件。文件会保留章节目录，下载器逐项核对内容；你修改过的文件会保留。", "", "也可在下方逐文件下载。先阅读对应正文，再保存输入、脚本和模板。正式计算输出与构造练习数据在说明中分别标识。命令中的相对路径从该章指定目录开始。", ""]
    approved = public_assets()
    for chapter_id, title in chapters:
        files = [(source, dest) for source, dest in approved if dest.relative_to(ASSETS_OUT).parts[0] == chapter_id]
        lines.extend([f"## {title}", "", f"[阅读本章](chapters/{chapter_id}.md)", ""])
        for source, dest in files:
            relative = dest.relative_to(DOCS_DIR).as_posix()
            label = source.relative_to(CHAPTERS_DIR / chapter_id / "assets").as_posix()
            href = f"https://luvega.github.io/AI_MD/{relative}" if source.suffix == ".md" else relative
            lines.append(f"- [{label}]({href}){{download}}")
        lines.append("")
    (DOCS_DIR / "resources.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    approved = public_assets()
    safe_rmtree(CHAPTERS_OUT)
    safe_rmtree(ASSETS_OUT)
    CHAPTERS_OUT.mkdir(parents=True, exist_ok=True)
    ASSETS_OUT.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "stylesheets").mkdir(parents=True, exist_ok=True)

    chapters = [publish_chapter(i) for i in range(1, CHAPTER_COUNT + 1)]
    publish_assets(approved)
    write_index(chapters)
    print(f"Published {len(chapters)} chapters to {DOCS_DIR}")


if __name__ == "__main__":
    main()
