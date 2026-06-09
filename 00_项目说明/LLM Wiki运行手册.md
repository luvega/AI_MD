---
title: "LLM Wiki 运行手册"
created: 2026-05-30
type: project-doc
status: active
topics: [type/project, status/active, llm-wiki, workflow]
wiki_role: concept
source_count: 1
last_reviewed: 2026-05-30
source_files: ["CLAUDE.md", "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"]
zotero_items: []
bibtex_keys: []
related: ["LLM Wiki Agent说明.md", "概念关系规范.md", "../index.md", "../log.md"]
claims: [p9_llm_wiki_bootstrap_2026_05_30, p10_wiki_lint_2026_05_30]
relations:
  - type: depends_on
    target: "../CLAUDE.md"
  - type: applies_to
    target: "../.claude/skills/ingest-source/SKILL.md"
  - type: applies_to
    target: "../.claude/skills/query-wiki/SKILL.md"
  - type: applies_to
    target: "../.claude/skills/wiki-lint/SKILL.md"
---

# LLM Wiki 运行手册

## ingest：新增来源

1. `ai-md-router` 判断来源类型、目标章节和是否需要 Zotero/PDF/DOCX/PPTX 工具。
2. `ingest-source` 读取来源，列出要创建或更新的页面。
3. `takenote` 写入方法笔记、文献笔记、实验记录、附件说明或项目说明。
4. 更新对应 `_index.md`、根 `index.md` 和 `log.md`。
5. `update-vault` 验收索引、断链、附件、BibTeX、PDF/OCR 覆盖。
6. 如果新来源影响教材正文，只记录 Book 轨待办；不自动更新 `chapters/` 或 `book/`。

## query：基于 wiki 回答

1. 先读根 `index.md`。
2. 读相关目录 `_index.md` 和具体页面。
3. 回答时引用已有页面、原始资料路径、Zotero item key 或 BibTeX key。
4. 如果答案有长期价值，用 `takenote` 沉淀为综合笔记、方法补充或开放问题。
5. 写入后更新 `log.md`，并由 `update-vault` 验收。

## lint：健康检查

1. `wiki-lint` 检查孤立页、重复概念、过期声明、矛盾候选、缺少来源的 claims。
2. `update-vault` 检查附件覆盖、索引一致性、断链、BibTeX 映射、PDF/OCR 和章节精读覆盖。
3. 只报告问题，不删除原始资料。
4. 内容缺口交给 `takenote` 或 `zotero-literature-link` 处理。

## update：维护更新

1. 小范围更新优先用 `takenote`。
2. 文献更新先用 `zotero-literature-link`，再用 `takenote` 更新笔记。
3. 所有内容更新后追加 `log.md`。
4. 完成前运行 `update-vault`。

## book：在线书显式轨

Wiki 维护和 Book 写作默认分离。只有用户明确要求“更新在线书”“同步 book”“发布层”“MkDocs”“GitHub Pages”“写第 X 章正文”时，才进入 Book 轨。

Book 轨流程：

1. 先读 `AGENTs.md`、`大纲.md` 和对应 `chapters/chapter-XX/本章大纲.md`。
2. 只在确认正文任务后更新 `chapters/chapter-XX/正文.md` 或章节资产。
3. 只有在用户要求同步发布层时，才运行 `python tools\sync_online_book.py`。
4. 只有在用户要求校验或发布在线书时，才运行 `python tools\validate_online_book.py` 和 `python -m mkdocs build -f book\mkdocs.yml --strict`。
5. Book 轨更新完成后可回写 wiki 维护报告和 `log.md`，但不能把 `book/docs` 反向当作正文或 wiki 来源。

Wiki 轨禁止项：

- 不运行 `tools/sync_online_book.py`。
- 不改 `book/docs/`、`book/site/` 或 `.github/workflows/deploy-book.yml`。
- 不改 `chapters/chapter-XX/正文.md`。
- 不把文献补强、附件索引、OCR 修复或方法卡更新自动写进在线书。

## git：本地版本史

1. 本项目允许本地 Git。
2. 默认不配置 remote，不 push。
3. 提交前运行 LLM Wiki 验收。
4. `.gitignore` 忽略易变 workspace、缓存、临时文件，以及 PDF/RAR/ZIP/Office 等大型不可变原始资料。
5. 核心 Markdown、BibTeX、TSV、skills、脚本和结构化文本默认进入本地版本史。
