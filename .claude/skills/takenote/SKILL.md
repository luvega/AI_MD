---
name: takenote
description: 当用户想记录 AI_MD 项目想法、整理课程资料、摘要 PDF/附件、保存运行结果、写方法笔记、写文献笔记，或提到 /takenote、记一下、整理成笔记 时使用。
---

# takenote

把用户输入整理成 AI_MD 项目内的正式 Markdown 笔记，并同步维护索引。它是 LLM Wiki Agent 的原子写入器，不负责全库验收。

## 先读什么

1. 读取项目根目录 `CLAUDE.md`。
2. 读取根 `index.md`。
3. 根据输入类型读取相关目录的 `_index.md`。
4. 如果涉及文献，读取 `references/zotero-map.tsv` 和 `references/references.bib`。
5. 如果涉及原始课程资料，先通过 `05_附件索引/附件清单.md` 定位原始文件。

## 处理流程

1. 判断内容类型：方法笔记、文献笔记、实验记录、附件说明、项目说明。
2. 判断目标目录：
   - 方法和流程：`02_方法笔记/`
   - 文献：`03_文献笔记/`
   - 运行结果：`04_实验记录/`
   - 附件说明：`05_附件索引/`
   - 项目说明：`00_项目说明/`
3. 搜索目标目录 `_index.md`，判断新建还是更新。
4. 使用 `CLAUDE.md` 中的 frontmatter 模板。
5. `source_files` 必须记录原始项目路径；涉及 Zotero 时必须记录 `zotero_items` 和 `bibtex_keys`。
6. 必要时补充 `wiki_role`、`claims` 和 `relations`。
7. 更新目标目录 `_index.md`，必要时更新根 `index.md`。
8. 向 `log.md` 追加 `ingest`、`query` 或 `update` 记录。
9. 简要汇报创建或更新的文件、关联原始资料和关联文献，并建议后续运行 `update-vault`。

## 写作要求

- 中文、条列式、路径明确。
- 不移动原始资料。
- 不批量复制 Zotero PDF。
- 不确定分类时，先记录到最接近的现有目录，并在正文中标注“待确认”。
- 不替代 `update-vault` 做全库验收。
- 不更新教材正文或在线书发布层；如笔记内容应进入教材，写入“Book 轨待办”并等待用户确认。
