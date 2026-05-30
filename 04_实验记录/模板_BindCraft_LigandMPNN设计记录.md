---
title: "模板：BindCraft 与 LigandMPNN 设计记录"
created: 2026-05-30
type: experiment-record
status: draft
topics: [type/experiment, status/draft, topic/protein-design, topic/structure-based-design, chapter/6]
source_files: ["02_方法笔记/RFdiffusion与蛋白设计.md"]
zotero_items: ["QCD2DXXI", "UN6R4C6J"]
bibtex_keys: ["pacesa_bindcraft_2024", "dauparas_atomic_2025"]
related: ["../02_方法笔记/RFdiffusion与蛋白设计.md", "../03_文献笔记/BindCraft与LigandMPNN.md"]
---

# 模板：BindCraft 与 LigandMPNN 设计记录

## 任务定义

- 任务 ID：待填。
- 任务类型：protein binder / ligand-aware sequence design / enzyme pocket redesign。
- 目标结构：待填。
- 配体、金属或辅因子：待填。
- 目标界面或口袋：待填。

## 输入和约束

| 项目 | 内容 | 检查点 |
|:---|:---|:---|
| target_path | 待填 | 链 ID 和生物装配 |
| binder/backbone_path | 待填 | 来源和 QC 状态 |
| ligand/cofactor | 待填 | CCD/SMILES/坐标和质子化 |
| fixed residues | 待填 | 功能位点是否保持 |
| interface constraints | 待填 | hotspot、距离或接触约束 |

## 运行参数

| 参数 | 值 |
|:---|:---|
| 工具 | BindCraft / LigandMPNN / 其他 |
| 版本或 commit | 待填 |
| seed | 待填 |
| num_designs | 待填 |
| output_dir | 待填 |

## 设计结果 QC

| design_id | model_path | sequence_path | interface_contacts | shape_complementarity | ligand_contact_ok | plddt_iptm | qc_status | decision |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 待填 | 待填 | 待填 | 待填 | 待填 | pass/review/fail | 待填 | pass/review/fail | 保留/淘汰 |

## 药物化学解释

- 结合界面是否支持后续亲和力优化：待填。
- 配体或小分子邻近残基是否化学合理：待填。
- 是否存在聚集、暴露疏水面或表达风险：待填。
- 是否进入 MD/BioEmu、Boltz2、对接或实验验证：待填。
