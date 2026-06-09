---
name: ai-md-router
description: 当用户提出 AI_MD 项目的宽泛整理、继续推进、下一步计划、插件/skill 调用、章节到文献/方法/实验的跨模块任务时使用。
---

# ai-md-router

为 AI_MD 项目选择最小必要插件、skill 和本地资料入口。它是 LLM Wiki Agent 的总调度入口：先判断任务类型，再选择 ingest、query、lint、takenote、zotero 或 update 工作流。

## 必读入口

1. `CLAUDE.md`
2. `index.md`
3. `00_项目说明/插件与Skills调用说明.md`
4. 与任务相关目录的 `_index.md`

## 路由规则

| 任务类型 | 先用本地 skill | 必要插件/外部 skill |
|:---|:---|:---|
| 新来源摄入、处理新增资料、整合维护报告 | `ingest-source`，再由 `takenote` 写入，`update-vault` 验收 | PDF 时可用 `pdf`；DOCX 时可用 `doc`；PPTX 时可用 `pptx-extractor` |
| 基于 wiki 提问、跨章节综合、可沉淀答案 | `query-wiki` | 必要时 `takenote` 沉淀答案 |
| Wiki 健康检查、孤立页、重复概念、矛盾候选 | `wiki-lint` | 底层联动 `update-vault` |
| 记录想法、整理附件、写方法/实验/项目笔记 | `takenote` | 必要时按来源类型调用工具 |
| Zotero 检索、文献候选、BibTeX、引用映射 | `zotero-literature-link` | `Zotero`；必要时用 `Life Science Research` 交叉验证 PubMed/PMC |
| 重建索引、断链、附件遗漏、OCR/章节覆盖检查 | `update-vault` | 必要时用 `pdf` 或本地 shell 验证 |
| 在线书、章节正文、MkDocs、GitHub Pages、同步发布层 | 进入 Book 轨，先读 `AGENTs.md`、`大纲.md` 和对应本章大纲 | 只有用户明确触发时才运行 `sync_online_book.py`、`validate_online_book.py` 或 MkDocs |
| 远程网页、课程页面、浏览器态资料 | 本 skill 先路由 | 用户点名 `@chrome` 或需要浏览器态时用 `Chrome` |
| 生命科学外部证据、数据库、PubMed/PDB/UniProt/AlphaFold | 本 skill 先路由 | `Life Science Research` 及其具体数据库 skill |
| 宽泛“继续整理” | 本 skill 制定 P0/P1/P2/P3 风格小阶段 | 根据阶段调用上面的最小集合 |

## 执行边界

- 不写入 Zotero，除非用户明确要求。
- 不复制 Zotero PDF，除非用户明确要求。
- 不移动原始资料，除非用户明确确认；PDF 课件归档规则以 `CLAUDE.md` 为准。
- 候选文献先进入 `references/zotero-candidates-YYYY-MM-DD.tsv`，正式确认后才进入 `references/zotero-map.tsv`。
- 写入内容后追加 `log.md`，再用 `update-vault` 做范围内验收。
- 完成前至少运行一次验证：索引覆盖、Markdown 断链、BibTeX key、章节/附件覆盖按任务范围检查。
- Wiki 任务默认不触碰 `book/` 或 `chapters/chapter-XX/正文.md`；教材正文和在线发布层必须由用户显式触发。

## 下一步默认优先级

1. `ingest-source`：新增来源时走摄入、写入、验收闭环。
2. `query-wiki`：跨章节问题先查 wiki，再决定是否沉淀。
3. `wiki-lint`：周期性检查 LLM Wiki 健康度，并联动 `update-vault`。
