---
title: "Wiki 与 Book 分轨规则"
created: 2026-06-09
type: project-doc
status: active
topics: [llm-wiki, online-book, workflow-boundary, update-vault]
source_files: ["CLAUDE.md", "AGENTs.md", "00_项目说明/LLM Wiki运行手册.md", ".claude/skills/update-vault/SKILL.md", ".claude/skills/wiki-lint/SKILL.md"]
related: ["LLM Wiki运行手册.md", "Codex技能调用矩阵.md", "知识库使用说明.md", "../index.md"]
wiki_role: concept
source_count: 5
last_reviewed: 2026-06-09
claims:
  - "AI_MD Wiki 维护默认不更新在线书 book；Book 写作和发布必须由用户显式触发。"
relations:
  - type: depends_on
    target: "../CLAUDE.md"
  - type: applies_to
    target: "../.claude/skills/update-vault/SKILL.md"
  - type: applies_to
    target: "../.claude/skills/wiki-lint/SKILL.md"
  - type: supports
    target: "LLM Wiki运行手册.md"
  - type: supports
    target: "../AGENTs.md"
---

# Wiki 与 Book 分轨规则

## 为什么分轨

AI_MD 同时有知识库和在线教材两层。知识库用于保存来源、方法、文献、实验记录、索引、维护报告和研究工作台；在线书用于面向课程学习者发布教材正文。

两者不能混在同一个默认更新流程里。Wiki 更新频繁，强调完整性和可追踪；Book 更新更接近正式写作和发布，要求读者视角、章节结构、图表授权和公开发布边界。

## 两条工作轨

| 工作轨 | 主要任务 | 默认可写范围 | 典型验证 |
|:---|:---|:---|:---|
| Wiki 轨 | 资料整理、方法卡、文献笔记、实验记录、附件索引、维护验收 | `00_项目说明/`、`01_课程章节索引/`、`02_方法笔记/`、`03_文献笔记/`、`04_实验记录/`、`05_附件索引/`、`07_研究工作台/`、`references/`、`index.md`、`log.md` | `validate_llm_wiki.py`、`tools/audit_raw_sources.py`、`tools/graph_health.py` |
| Book 轨 | 章节正文写作、在线书同步、MkDocs 构建、GitHub Pages 发布 | `大纲.md`、`chapters/chapter-XX/本章大纲.md`、`chapters/chapter-XX/正文.md`、`chapters/chapter-XX/assets/`、`book/`、`.github/workflows/deploy-book.yml` | `tools/sync_online_book.py`、`tools/validate_online_book.py`、`python -m mkdocs build -f book\mkdocs.yml --strict` |

## 默认禁止

当任务是 Wiki 维护、`/update-vault`、`wiki-lint`、文献补强、附件索引、OCR/全文提取复核、方法卡整理或实验记录时，默认禁止：

- 修改 `book/`。
- 修改 `chapters/chapter-XX/正文.md`。
- 运行 `python tools\sync_online_book.py`。
- 运行 `python tools\validate_online_book.py`。
- 运行 MkDocs build。
- 把 `book/docs` 页面当作 wiki 或章节正文来源。

如果发现 wiki 更新影响教材正文，只写成待办，例如“Book 轨待办：第 8 章 AI 亲和力模型段落需要补充 PLANET/GAABind 文献锚点”。不要顺手改正文。

## Book 轨显式触发词

只有用户明确出现以下意图时，才进入 Book 轨：

- “更新在线书”
- “同步 book”
- “构建/发布 MkDocs”
- “发布到 GitHub Pages”
- “写第 X 章正文”
- “修改 `chapters/chapter-XX/正文.md`”
- “把这部分写进教材”

进入 Book 轨后，先读 `AGENTs.md`，再读 `大纲.md` 和对应 `chapters/chapter-XX/本章大纲.md`。正文完成后，才按需同步 `book/docs`。

## 推荐流程

Wiki 轨：

1. 读 `CLAUDE.md`、`index.md`、相关 `_index.md`。
2. 更新 wiki 笔记、索引、文献映射或维护报告。
3. 追加 `log.md`。
4. 运行 LLM Wiki 校验、raw 审计和图谱健康检查。
5. 报告 Book 轨待办，但不更新在线书。

Book 轨：

1. 用户明确触发 Book 任务。
2. 读 `AGENTs.md`、`大纲.md`、对应本章大纲和来源材料。
3. 更新 `chapters/chapter-XX/正文.md` 或章节资产。
4. 用户要求同步时运行 `sync_online_book.py`。
5. 用户要求发布/验收时运行在线书校验和 MkDocs build。
6. 将结果回写维护报告和 `log.md`。
