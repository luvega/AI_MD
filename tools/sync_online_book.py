from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"
BOOK_DIR = ROOT / "book"
DOCS_DIR = BOOK_DIR / "docs"
CHAPTERS_OUT = DOCS_DIR / "chapters"
ASSETS_OUT = DOCS_DIR / "assets"

CHAPTER_COUNT = 12
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
    markdown = markdown.replace(
        f"chapters/{chapter_id}/assets/",
        f"../assets/{chapter_id}/",
    )
    markdown = markdown.replace(
        f".\\chapters\\{chapter_id}\\assets\\",
        f"..\\assets\\{chapter_id}\\",
    )
    markdown = markdown.replace(
        f"chapters\\{chapter_id}\\assets\\",
        f"..\\assets\\{chapter_id}\\",
    )
    markdown = re.sub(
        r"(?<![./\w-])assets/",
        f"../assets/{chapter_id}/",
        markdown,
    )
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


def publish_chapter(chapter_number: int) -> tuple[str, str]:
    chapter_id = f"chapter-{chapter_number:02d}"
    src = CHAPTERS_DIR / chapter_id / "正文.md"
    if not src.exists():
        raise FileNotFoundError(src)

    text = src.read_text(encoding="utf-8")
    title = first_heading(text)
    text = strip_author_material(text)
    text = rewrite_paths(text, chapter_id)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    dest = CHAPTERS_OUT / f"{chapter_id}.md"
    dest.write_text(text, encoding="utf-8")

    assets_src = CHAPTERS_DIR / chapter_id / "assets"
    if assets_src.exists():
        assets_dest = ASSETS_OUT / chapter_id
        shutil.copytree(assets_src, assets_dest, ignore=shutil.ignore_patterns("*.md"))
        sanitize_published_assets(assets_dest)

    return chapter_id, title


def sanitize_published_assets(path: Path) -> None:
    text_suffixes = {
        ".csv",
        ".md",
        ".py",
        ".sh",
        ".svg",
        ".tsv",
        ".txt",
        ".yaml",
        ".yml",
    }
    for file_path in path.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in text_suffixes:
            continue
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        text = text.replace("06_原始学习素材", "local_raw_sources_not_published")
        text = text.replace("book/docs", "published_docs")
        text = text.replace("book/site", "published_site")
        file_path.write_text(text, encoding="utf-8")


def write_index(chapters: list[tuple[str, str]]) -> None:
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


def main() -> None:
    safe_rmtree(CHAPTERS_OUT)
    safe_rmtree(ASSETS_OUT)
    CHAPTERS_OUT.mkdir(parents=True, exist_ok=True)
    ASSETS_OUT.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "stylesheets").mkdir(parents=True, exist_ok=True)

    chapters = [publish_chapter(i) for i in range(1, CHAPTER_COUNT + 1)]
    write_index(chapters)
    print(f"Published {len(chapters)} chapters to {DOCS_DIR}")


if __name__ == "__main__":
    main()
