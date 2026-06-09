---
title: "P43 Wiki 与 Book 分轨保护报告"
created: 2026-06-09
type: maintenance-report
status: active
topics: [llm-wiki, online-book, workflow-boundary, schema]
source_files: ["CLAUDE.md", "AGENTs.md", "index.md", "log.md", "VERSION", "00_项目说明/版本记录.md", "00_项目说明/Wiki与Book分轨规则.md", "00_项目说明/P42_原始素材更新后全项目重建报告.md", "00_项目说明/LLM Wiki运行手册.md", "00_项目说明/Codex技能调用矩阵.md", "00_项目说明/插件与Skills调用说明.md", "00_项目说明/知识库使用说明.md", ".claude/skills/update-vault/SKILL.md", ".claude/skills/wiki-lint/SKILL.md", ".claude/skills/ai-md-router/SKILL.md", ".claude/skills/ingest-source/SKILL.md", ".claude/skills/takenote/SKILL.md"]
related: ["Wiki与Book分轨规则.md", "P42_原始素材更新后全项目重建报告.md", "../index.md", "../log.md"]
wiki_role: maintenance
source_count: 17
last_reviewed: 2026-06-09
claims:
  - "P43 将 Wiki 维护和在线书 Book 写作分成两个显式工作轨；默认 Wiki 更新不会同步或修改 book。"
relations:
  - type: updates
    target: "../CLAUDE.md"
  - type: updates
    target: "../AGENTs.md"
  - type: updates
    target: "Wiki与Book分轨规则.md"
  - type: updates
    target: "../.claude/skills/update-vault/SKILL.md"
  - type: updates
    target: "../.claude/skills/wiki-lint/SKILL.md"
  - type: updates
    target: "../index.md"
  - type: updates
    target: "../log.md"
  - type: updates
    target: "版本记录.md"
  - type: supports
    target: "P42_原始素材更新后全项目重建报告.md"
---

# P43 Wiki 与 Book 分轨保护报告

## 本轮目标

用户要求把 wiki 的建立和重构，与在线书 `book` 的撰写区分开，避免更新 wiki 时同时更新 book 内容。

本轮只更新 schema、规则、说明和历史项目 skills，不同步 `book/docs`，不运行 `sync_online_book.py`，不修改章节正文。

## 主要更新

- 在 `CLAUDE.md` 新增“Wiki 与 Book 分轨规则”，把 LLM Wiki / 知识库轨和 Book / 在线教材轨分开。
- 在 `AGENTs.md` 明确：Wiki 维护、`/update-vault`、`wiki-lint`、附件索引、文献映射和方法卡更新不自动触发正文或 `book/` 更新。
- 新增 `00_项目说明/Wiki与Book分轨规则.md`，作为后续判断是否允许触碰 `book/` 的入口文档。
- 更新 `00_项目说明/LLM Wiki运行手册.md`、`Codex技能调用矩阵.md`、`插件与Skills调用说明.md` 和 `知识库使用说明.md`，把默认验证链路改为 Wiki 轨验证；Book 验证只在用户明确触发时执行。
- 更新 `.claude/skills/update-vault`、`wiki-lint`、`ai-md-router`、`ingest-source` 和 `takenote`，明确这些 skill 默认不修改 `book/`、`正文.md` 或运行在线书同步。

## 新默认行为

| 用户意图 | 默认轨道 | 是否更新 `book/` |
|:---|:---|:---|
| “继续整理知识库” | Wiki | 否 |
| `/update-vault` | Wiki | 否 |
| “补 Zotero 文献锚点” | Wiki | 否 |
| “补方法卡/实验记录” | Wiki | 否 |
| “检查 OCR/附件索引” | Wiki | 否 |
| “写第 8 章正文” | Book | 是，限对应章节 |
| “同步在线书/发布 book” | Book | 是，显式同步 |

## 验收口径

本轮只做 Wiki/schema 级验收：

| 命令 | 结果 |
|:---|:---|
| `python C:\Users\xsui\.codex\skills\building-llm-wiki\scripts\validate_llm_wiki.py . --raw-dir 06_原始学习素材` | warnings 0；errors 0；Zotero map 与 BibTeX 文件均存在 |
| `python tools\audit_raw_sources.py . --json` | raw 文件 1076 个；PDF 14 个；12 个已有提取报告；关键附件索引缺口 0；根级 Markdown 来源索引缺口 0 |
| `python tools\graph_health.py . --json --stale-days 180` | relation targets missing 0；Zotero keys missing in BibTeX 0；保留既有维护项：47 个缺 `last_reviewed`、5 个模板或 skill 页面孤立、1 个文献模板缺 key |
| `git diff --name-only -- book` | 无输出；本轮未修改 `book/` 发布层文件 |

本轮不运行：

- `tools/sync_online_book.py`
- `tools/validate_online_book.py`
- `python -m mkdocs build -f book\mkdocs.yml --strict`

## 待确认项

- 后续如果需要把 Wiki 中的新文献、新方法卡或新实验模板写进教材，应单独提出 Book 轨任务。
- 若需要更强保护，可以后续给 `sync_online_book.py` 增加命令行确认参数，例如 `--confirm-book-sync`。
