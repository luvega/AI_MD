---
title: "MD_BioEmu采样记录模板"
created: 2026-05-30
type: experiment-record
status: draft
topics: [type/experiment, status/draft, topic/molecular-dynamics, topic/bioemu, topic/sampling, chapter/4]
source_files: []
zotero_items: ["BR4AMZPF"]
bibtex_keys: ["chen_design_2024"]
related: ["../02_方法笔记/MD_BioEmu_AI采样.md", "../01_课程章节索引/章节精读/第04章_AI采样与分子模拟精读.md"]
---
# MD_BioEmu采样记录模板

## 任务摘要

- 任务 ID：
- 体系名称：
- 采样目标：稳定性 / 口袋开合 / 结合姿态 / 突变影响 / 构象聚类 / 自由能面
- 方法：MD / BioEmu / 其他 AI 采样 / 混合
- 运行日期：
- 操作者：

## 输入与体系组成

| 类别 | 路径或值 | 说明 |
|:---|:---|:---|
| 初始结构 |  | 实验结构/预测结构/对接姿态 |
| 蛋白链 |  | 链 ID 和长度 |
| 配体/核酸/金属 |  | ID、参数来源 |
| 修饰 |  | PTM、非标准残基、糖基化 |
| 质子化 |  | pH、工具、关键残基 |
| 溶剂/离子 |  | 水模型、box、盐浓度 |

## MD 参数

| 参数 | 值 |
|:---|:---|
| force_field |  |
| water_model |  |
| temperature |  |
| pressure |  |
| time_step |  |
| minimization |  |
| equilibration |  |
| production_time |  |
| trajectory_stride |  |
| random_seed |  |

## BioEmu/AI采样参数

| 参数 | 值 |
|:---|:---|
| model_version |  |
| input_sequence_or_structure |  |
| num_samples |  |
| conditioning |  |
| seed |  |
| output_dir |  |

## 轨迹或样本指标

| 指标 | 文件路径 | 主要结果 | 解释 |
|:---|:---|:---|:---|
| RMSD |  |  |  |
| RMSF |  |  |  |
| H-bond/contact |  |  |  |
| key distance |  |  |  |
| pocket volume |  |  |  |
| clustering |  |  |  |
| free-energy surface |  |  |  |

## 代表构象

| cluster_id | representative_path | population | key_features | next_step |
|:---|:---|---:|:---|:---|
|  |  |  |  | docking/MM-GBSA/Boltz2/结构图 |

## 结论等级

- `pass`：采样覆盖合理，关键构象/相互作用有支持，可进入下一步。
- `review`：采样有信号，但输入、参数或覆盖不足，需要补跑或复核。
- `fail`：体系准备错误、轨迹异常、AI 样本不可解释或与结构知识冲突。

## 结论

- 主要构象状态：
- 稳定性判断：
- 关键相互作用：
- 待补验证：
- 下一步：
