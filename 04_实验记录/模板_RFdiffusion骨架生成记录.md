---
title: "模板：RFdiffusion 骨架生成记录"
created: 2026-05-30
type: experiment-record
status: draft
topics: [type/experiment, status/draft, topic/rfdiffusion, topic/protein-design, chapter/6]
source_files: ["02_方法笔记/RFdiffusion与蛋白设计.md"]
zotero_items: ["UKX5E6IB", "ZYFCZKMH", "EBQ7CNVI"]
bibtex_keys: ["watson_novo_2023", "ahern_atom_2025", "bennett_atomically_2025"]
related: ["../02_方法笔记/RFdiffusion与蛋白设计.md", "../03_文献笔记/RFdiffusion蛋白设计.md"]
---

# 模板：RFdiffusion 骨架生成记录

## 任务定义

- 任务 ID：待填。
- 任务类型：de novo fold / motif scaffolding / enzyme active-site scaffolding / binder / antibody。
- 目标：待填。
- 目标结构：待填。
- 目标链和保留组分：待填。

## 约束和输入

| 项目 | 内容 | 检查点 |
|:---|:---|:---|
| 输入 PDB/mmCIF | 待填 | 链 ID、残基编号、配体/金属保留规则 |
| motif/active site | 待填 | 固定残基和原子几何是否正确 |
| hotspot/interface | 待填 | 是否来自可靠结构或实验信息 |
| contig map | 待填 | 长度、固定段、可变段是否符合任务 |
| seed | 待填 | 可复现 |
| num_designs | 待填 | 与筛选资源匹配 |

## 运行记录

| 字段 | 值 |
|:---|:---|
| RFdiffusion/RFD3 版本 | 待填 |
| checkpoint | 待填 |
| 命令或 YAML 路径 | 待填 |
| 输出目录 | 待填 |
| 运行平台 | 待填 |

## 骨架 QC

| design_id | pdb_path | motif_rmsd | clash | interface_contacts | secondary_structure | qc_status | decision |
|:---|:---|---:|:---|:---|:---|:---|:---|
| 待填 | 待填 | 待填 | pass/review/fail | 待填 | 待填 | pass/review/fail | 保留/淘汰 |

## 结论

- 保留设计：待填。
- 淘汰原因：待填。
- 下一步：ProteinMPNN / LigandMPNN / AlphaFold/Boltz 回折叠 / MD / 实验。
