from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


KEY_ATTACHMENT_EXTENSIONS = {
    ".7z",
    ".cif",
    ".docx",
    ".html",
    ".inp",
    ".json",
    ".mdp",
    ".mp4",
    ".opju",
    ".opx",
    ".pdf",
    ".py",
    ".rar",
    ".tar",
    ".tgz",
    ".top",
    ".tsv",
    ".txt",
    ".xlsx",
    ".xyz",
    ".zip",
}

INDEX_CANDIDATES = (
    "05_附件索引/附件清单.md",
    "06_原始学习素材/_index.md",
    "01_课程章节索引/第1-8章资料索引.md",
)


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def load_index_text(root: Path) -> str:
    chunks: list[str] = []
    for relative_path in INDEX_CANDIDATES:
        path = root / relative_path
        if path.exists():
            chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(chunks)


def read_report_source(report_path: Path) -> str:
    try:
        text = report_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""
    for line in text.splitlines():
        if line.startswith("| Source PDF |"):
            return line.split("`", 2)[1] if "`" in line else ""
    return ""


def audit(root: Path) -> dict:
    raw_dir = root / "06_原始学习素材"
    if not raw_dir.exists():
        return {"errors": [f"Missing raw source directory: {raw_dir}"]}

    files = sorted(path for path in raw_dir.rglob("*") if path.is_file())
    by_extension = Counter(path.suffix.lower() or "[no_ext]" for path in files)
    by_top_level: dict[str, Counter] = defaultdict(Counter)
    for path in files:
        relative = path.relative_to(raw_dir)
        top_level = relative.parts[0] if relative.parts else "."
        by_top_level[top_level][path.suffix.lower() or "[no_ext]"] += 1

    reports = sorted(raw_dir.rglob("extraction-report.md"))
    report_by_source: dict[str, Path] = {}
    for report in reports:
        source = read_report_source(report)
        if source:
            report_by_source[source.replace("\\", "/")] = report

    pdfs = sorted(raw_dir.rglob("*.pdf"))
    pdf_rows = []
    for pdf in pdfs:
        relative_pdf = rel(pdf, root)
        report = report_by_source.get(relative_pdf)
        if not report:
            # Fallback for older reports: match by PDF stem in the extraction directory.
            matches = [
                candidate
                for candidate in reports
                if pdf.stem in candidate.as_posix()
            ]
            report = max(matches, key=lambda p: p.stat().st_mtime) if matches else None
        pdf_rows.append(
            {
                "pdf": relative_pdf,
                "bytes": pdf.stat().st_size,
                "mtime": pdf.stat().st_mtime,
                "report": rel(report, root) if report else "",
                "report_mtime": report.stat().st_mtime if report else 0,
                "needs_reextract": (not report) or pdf.stat().st_mtime > report.stat().st_mtime,
            }
        )

    index_text = load_index_text(root)
    key_files = [
        path
        for path in files
        if path.suffix.lower() in KEY_ATTACHMENT_EXTENSIONS
    ]
    missing_key_index = [
        rel(path, root)
        for path in key_files
        if rel(path, root) not in index_text
    ]
    root_markdown_files = sorted(
        path for path in raw_dir.glob("*.md") if path.name != "_index.md"
    )
    missing_root_markdown_index = [
        rel(path, root)
        for path in root_markdown_files
        if rel(path, root) not in index_text
    ]

    return {
        "root": str(root),
        "raw_dir": rel(raw_dir, root),
        "total_files": len(files),
        "by_extension": dict(by_extension.most_common()),
        "by_top_level": {
            top: dict(counter.most_common())
            for top, counter in sorted(by_top_level.items())
        },
        "pdf_count": len(pdfs),
        "pdfs": pdf_rows,
        "extracted_pdf_count": sum(1 for row in pdf_rows if row["report"]),
        "pdfs_needing_reextract": [
            row["pdf"] for row in pdf_rows if row["needs_reextract"]
        ],
        "key_attachment_count": len(key_files),
        "missing_key_attachment_index": missing_key_index,
        "root_markdown_count": len(root_markdown_files),
        "missing_root_markdown_index": missing_root_markdown_index,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    result = audit(root)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Raw source files: {result.get('total_files', 0)}")
        print(f"PDFs: {result.get('pdf_count', 0)}")
        print(f"Key attachment index gaps: {len(result.get('missing_key_attachment_index', []))}")
        print(f"Root Markdown index gaps: {len(result.get('missing_root_markdown_index', []))}")
    return 0 if not result.get("missing_key_attachment_index") else 1


if __name__ == "__main__":
    raise SystemExit(main())
