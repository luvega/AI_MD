---
title: "AI_MD LLM Wiki 总索引"
created: 2026-05-30
type: project-doc
status: active
topics: [type/project, status/active, llm-wiki, index]
wiki_role: synthesis
source_count: 0
last_reviewed: 2026-05-30
source_files: ["CLAUDE.md", "00_项目说明/LLM Wiki Agent说明.md"]
zotero_items: []
bibtex_keys: []
related: ["log.md", "00_项目说明/Obsidian入口.md", "00_项目说明/LLM Wiki运行手册.md"]
---

# AI_MD LLM Wiki 总索引

这是 AI_MD 第二大脑的内容型总索引。使用顺序：先读本页，再进入对应目录 `_index.md`，最后读取具体笔记或原始资料。

## 项目入口

| 入口 | 用途 |
|:---|:---|
| [CLAUDE.md](CLAUDE.md) | LLM Wiki Agent 的总 schema 和行为规则 |
| [log.md](log.md) | 追加式操作时间线 |
| [Obsidian 入口](00_项目说明/Obsidian入口.md) | 人类浏览入口 |
| [LLM Wiki Agent 说明](00_项目说明/LLM Wiki Agent说明.md) | Karpathy LLM Wiki 模式在本项目的落地说明 |
| [LLM Wiki 运行手册](00_项目说明/LLM Wiki运行手册.md) | ingest、query、lint、update、git 操作流程 |
| [概念关系规范](00_项目说明/概念关系规范.md) | typed relation 和 claims 规则 |
| [项目说明索引](00_项目说明/_index.md) | 项目说明和维护报告入口 |

## 章节索引

| 章节 | 入口 | 状态 |
|:---|:---|:---|
| 第 1-6 章资料 | [第1-6章资料索引](01_课程章节索引/第1-6章资料索引.md) | 已建主索引 |
| 第 1-5 章精读 | [章节精读索引](01_课程章节索引/章节精读/_index.md) | 已完成 |
| 章节-文献映射 | [章节-文献锚点矩阵](01_课程章节索引/章节精读/章节-文献锚点矩阵.md) | 已完成 |

## 方法线索引

| 方法线 | 入口 | 说明 |
|:---|:---|:---|
| Linux 与基础环境 | [Linux与生化基础](02_方法笔记/Linux与生化基础.md) | 环境、路径、文件格式 |
| 结构可视化 | [PyMOL与Chimera可视化](02_方法笔记/PyMOL与Chimera可视化.md) | 结构检查和出图 |
| 对接与虚拟筛选 | [AI多组分对接与虚拟筛选](02_方法笔记/AI多组分对接与虚拟筛选.md) | 受体、配体、box、score、top pose |
| MSA 与 Uni-Dock | [MSA与Uni-Dock补充](02_方法笔记/MSA与Uni-Dock补充.md) | 第三章补充 |
| MD/BioEmu/AI 采样 | [MD_BioEmu_AI采样](02_方法笔记/MD_BioEmu_AI采样.md) | 体系准备、轨迹指标、代表构象 |
| Boltz2 与亲和力 | [Boltz2亲和力预测](02_方法笔记/Boltz2亲和力预测.md) | YAML、置信度、亲和力解释 |
| 亲和力模型综述 | [亲和力模型综述](02_方法笔记/亲和力模型综述.md) | 模型选择和输出解释 |
| 蛋白设计 | [RFdiffusion与蛋白设计](02_方法笔记/RFdiffusion与蛋白设计.md) | RFdiffusion、ProteinMPNN、BindCraft、LigandMPNN |

## 文献与 Zotero

| 入口 | 用途 |
|:---|:---|
| [文献笔记索引](03_文献笔记/_index.md) | 核心文献笔记 |
| [Zotero 映射表](references/zotero-map.tsv) | Zotero item key、BibTeX key、主笔记、章节 |
| [BibTeX 文件](references/references.bib) | 正式引用条目 |
| [Zotero 候选表](references/zotero-candidates-2026-05-30.tsv) | 候选、正式提升和人工确认状态 |

## 实验记录

| 入口 | 用途 |
|:---|:---|
| [实验记录索引](04_实验记录/_index.md) | 已有结果和任务模板 |
| [Boltz2 结果 l6D9Z7](04_实验记录/Boltz2结果_l6D9Z7.md) | 当前最完整的运行结果样例 |
| [RFdiffusion 骨架生成模板](04_实验记录/模板_RFdiffusion骨架生成记录.md) | 第六章骨架生成记录 |
| [ProteinMPNN 序列设计模板](04_实验记录/模板_ProteinMPNN序列设计记录.md) | 第六章序列设计记录 |

## 原始资料和附件

| 入口 | 用途 |
|:---|:---|
| [附件清单](05_附件索引/附件清单.md) | PDF、压缩包、脚本、表格、JSON、CIF、TSV 等附件 |
| [PDF 全文提取总览](06_原始学习素材/PDF全文提取总览.md) | 6 份规范 PDF 的全文提取状态 |
| [OCR 质量收敛报告](06_原始学习素材/PDF OCR质量收敛报告.md) | 54 个低文本页 OCR 结果 |

## 维护报告

| 报告 | 用途 |
|:---|:---|
| [P7 update-vault 全库验收](00_项目说明/知识库维护报告-2026-05-30-P7-update-vault全库验收.md) | 附件、索引、断链、BibTeX、PDF/OCR 和章节精读验收 |
| [P8 第六章蛋白设计方法线](00_项目说明/知识库维护报告-2026-05-30-P8-第六章蛋白设计方法线.md) | 第六章 RFdiffusion/ProteinMPNN 方法线可执行化 |
| [P9 LLM Wiki Agent落地](00_项目说明/知识库维护报告-2026-05-30-P9-LLM-Wiki-Agent落地.md) | 根索引、日志、skill 联用和本地 Git 版本史 |

## 综合与开放问题

| 主题 | 当前状态 |
|:---|:---|
| 第 6 章运行结果 | 方法卡和模板已完成，`第六章/第六章RFD3_第七章.rar` 尚未解压运行 |
| Zotero 本地 API | 曾出现 HTTP 502；人工确认条目已在 P5 记录 |
| OCR 人工复核 | 仍有少数页面正式引用前建议对照原 PDF |
| Git 版本史 | 本轮启用本地 Git，不配置 remote、不 push |

## 最近日志摘要

- [2026-05-30] bootstrap | AI_MD LLM Wiki Agent 落地
- [2026-05-30] git | 初始化本地版本史
- [2026-05-30] lint | LLM Wiki / update-vault 验收
- [2026-05-30] maintenance | P9 LLM Wiki Agent落地报告

## 待确认项

- 是否把 Obsidian Dataview 查询、Web Clipper 设置和固定首页写入 `.obsidian/` 配置。
- 是否为本地 Git 版本史配置远程仓库；当前默认不配置 remote、不 push。
- 第六章压缩包资料是否进入实际运行阶段；当前只完成方法卡和实验记录模板。
