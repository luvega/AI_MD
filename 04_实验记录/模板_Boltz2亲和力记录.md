---
title: "Boltz2亲和力记录模板"
created: 2026-05-30
type: experiment-record
status: draft
topics: [type/experiment, status/draft, topic/boltz2, topic/affinity, chapter/5]
source_files: []
zotero_items: ["FF4V8LYV", "CRM22UDT", "PE42AXJX"]
bibtex_keys: ["passaro_boltz-2_2025", "cho_boltzdesign1_2025", "abramson_accurate_2024"]
related: ["../02_方法笔记/Boltz2亲和力预测.md", "../02_方法笔记/亲和力模型综述.md", "../01_课程章节索引/章节精读/第05章_AI多组分亲和力计算精读.md"]
---
# Boltz2亲和力记录模板

## 任务摘要

- 任务 ID：
- 目标体系：
- 任务类型：结构预测 / 复合物预测 / 亲和力预测 / 候选排序
- 运行日期：
- 模型/软件版本：
- 运行平台：

## 输入 YAML

```yaml
version: 1
sequences:
  - protein:
      id: A
      sequence: ""
      msa: ""
      templates: []
  - ligand:
      id: LIG
      smiles: ""
properties:
  - affinity:
      binder: LIG
output:
  out_dir: ""
```

## 输入字段

| 字段 | 值 | 说明 |
|:---|:---|:---|
| protein.id |  | 链 ID |
| protein.sequence |  | 序列来源 |
| msa |  | MSA 路径或自动生成说明 |
| templates |  | 模板路径或空 |
| ligand.id |  | 配体 ID |
| ligand representation |  | SMILES/CCD/结构文件 |
| affinity binder |  | 与 ligand.id 一致 |
| yaml_path |  | 输入 YAML 路径 |

## 输出文件

| 文件 | 路径 | 说明 |
|:---|:---|:---|
| 原始 JSON |  |  |
| summary.json |  |  |
| CIF |  |  |
| pLDDT TSV |  |  |
| 可视化图 |  |  |

## 核心指标

| 指标 | 数值 | 解释 |
|:---|---:|:---|
| confidence_scores |  | 整体置信度 |
| ptm_scores |  | 结构拓扑可信度 |
| iptm_scores |  | 界面可信度 |
| complex_plddt_scores |  | 复合物局部置信度 |
| complex_iplddt_scores |  | 界面局部置信度 |
| affinity_probability_binary |  | 结合倾向概率 |
| affinity_pic50 |  | 亲和力排序读数 |

## 结构复核

| 检查项 | 结果 | 说明 |
|:---|:---|:---|
| 链和配体位置 | pass/review/fail |  |
| 口袋合理性 | pass/review/fail |  |
| 界面低置信区域 | pass/review/fail |  |
| 配体构象 | pass/review/fail |  |
| 关键相互作用 | pass/review/fail |  |

## 亲和力解释

- `affinity_pic50`：
- `affinity_probability_binary`：
- 与 docking/MD/实验的一致性：
- 不确定性：
- 可比较范围：

## 结论等级

- `pass`：结构和界面置信度足够，亲和力读数可用于候选排序。
- `review`：亲和力有信号，但输入、结构或界面指标需要复核。
- `fail`：输入错误、结构不合理、界面低置信或亲和力读数不可解释。

## 下一步

- 进入候选列表：
- 需要补充的结构图：
- 需要复核的输入：
- 后续验证：MD / docking 对照 / MM-GBSA / 实验
