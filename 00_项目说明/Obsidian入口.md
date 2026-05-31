---
title: "AI_MD Obsidian 入口"
created: 2026-05-30
type: project-doc
status: active
topics: [obsidian, navigation, type/project]
source_files: ["CLAUDE.md", "00_项目说明/知识库使用说明.md"]
zotero_items: []
bibtex_keys: []
related: ["知识库使用说明.md", "Obsidian模板/_index.md", "../01_课程章节索引/章节精读/章节-文献锚点矩阵.md"]
---

# AI_MD Obsidian 入口

## 当前工作台

| 入口 | 用途 |
|:---|:---|
| [LLM Wiki 总索引](../index.md) | 内容型总入口，汇总章节、方法、文献、实验、附件、维护报告和开放问题 |
| [操作时间线](../log.md) | 追加式记录 ingest、query、update、lint、zotero、ocr、git 和 maintenance |
| [LLM Wiki Agent说明](LLM%20Wiki%20Agent说明.md) | AI_MD 第二大脑的 raw sources / wiki / schema 架构说明 |
| [LLM Wiki运行手册](LLM%20Wiki运行手册.md) | ingest、query、lint、update、zotero 和 git 的执行步骤 |
| [概念关系规范](概念关系规范.md) | typed relations、claims 和关系记录规范 |
| [章节精读索引](../01_课程章节索引/章节精读/_index.md) | 第 1-8 章课件结构化精读笔记 |
| [章节-文献锚点矩阵](../01_课程章节索引/章节精读/章节-文献锚点矩阵.md) | 章节、方法卡、Zotero item 和 BibTeX key 的总映射 |
| [方法笔记索引](../02_方法笔记/_index.md) | Linux、可视化、对接、MD/BioEmu、Boltz2、RFdiffusion 等方法卡 |
| [文献笔记索引](../03_文献笔记/_index.md) | Zotero 文献笔记和候选补强状态 |
| [实验记录索引](../04_实验记录/_index.md) | Boltz2、QM-MM、蒙特卡洛和任务记录模板 |
| [附件索引](../05_附件索引/_index.md) | PDF、压缩包、脚本、表格、JSON、CIF、TSV 等附件清单 |
| [PDF 全文提取总览](../06_原始学习素材/PDF全文提取总览.md) | 原始课件全文提取、逐页文本和 OCR 入口 |
| [引用映射表](../references/zotero-map.tsv) | Zotero item key、BibTeX key、主笔记和章节映射 |
| [Obsidian 模板索引](Obsidian模板/_index.md) | 方法卡、文献笔记、实验记录、章节精读笔记模板 |

## 推荐浏览路径

1. 先从 [章节地图](章节地图.md) 判断当前资料属于哪一章。
2. 进入 [章节精读索引](../01_课程章节索引/章节精读/_index.md) 查看课件结构化内容。
3. 打开对应 [方法笔记索引](../02_方法笔记/_index.md) 中的方法卡，确认输入、输出、质量门槛和实验记录模板。
4. 需要论文支撑时查看 [章节-文献锚点矩阵](../01_课程章节索引/章节精读/章节-文献锚点矩阵.md) 和 [文献笔记索引](../03_文献笔记/_index.md)。
5. 产生新想法、运行结果或候选文献时，优先复制 [Obsidian 模板索引](Obsidian模板/_index.md) 中的模板。

## 标签使用

| 标签族 | 用途 | 示例 |
|:---|:---|:---|
| `type/*` | 文件类型 | `type/method`, `type/literature`, `type/experiment`, `type/project` |
| `status/*` | 状态 | `status/draft`, `status/active`, `status/complete` |
| `topic/*` | 方法或主题 | `topic/docking`, `topic/molecular-dynamics`, `topic/boltz2`, `topic/affinity` |
| `chapter/*` | 章节 | `chapter/1`, `chapter/3`, `chapter/5` |

## 维护规则

- 根 `index.md` 是内容索引，目录 `_index.md` 是局部索引，`log.md` 是时间线；三者需要同步维护。
- 新来源进入时走 `ingest-source -> takenote -> update-vault`。
- 基于知识库提问时走 `query-wiki`，有长期价值再沉淀。
- 周期健康检查走 `wiki-lint -> update-vault`。
- 新增笔记后同步更新所在目录 `_index.md`。
- 涉及 Zotero 时同时写 Zotero item key 和 BibTeX key。
- 原始 PDF 课件继续保留在 `06_原始学习素材/`，非 PDF 原始资料继续保留原章节目录。
- 不在未确认前创建 `.obsidian/` 配置，避免覆盖用户本地工作区偏好。
