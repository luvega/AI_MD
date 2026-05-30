---
title: "Obsidian 模板索引"
created: 2026-05-30
type: project-doc
status: active
topics: [obsidian, templates, type/project]
source_files: ["CLAUDE.md"]
zotero_items: []
bibtex_keys: []
related: ["../Obsidian入口.md"]
---

# Obsidian 模板索引

这些模板用于手动复制到目标目录；本轮不创建 `.obsidian/` 配置，也不强制指定 Obsidian Templates 插件目录。

| 模板 | 用途 | 默认目标目录 |
|:---|:---|:---|
| [模板_方法卡.md](模板_方法卡.md) | 新增可执行方法笔记 | `02_方法笔记/` |
| [模板_文献笔记.md](模板_文献笔记.md) | 新增 Zotero 文献笔记 | `03_文献笔记/` |
| [模板_实验记录.md](模板_实验记录.md) | 新增运行或分析记录 | `04_实验记录/` |
| [模板_章节精读.md](模板_章节精读.md) | 新增课件结构化精读 | `01_课程章节索引/章节精读/` |

## 使用后检查

- 替换 `title`、`created`、`topics`、`source_files`、`zotero_items`、`bibtex_keys` 和 `related`。
- 更新目标目录 `_index.md`。
- 涉及引用时同步检查 `references/zotero-map.tsv` 和 `references/references.bib`。
