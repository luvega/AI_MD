---
title: "模板：Chai-1互作蛋白虚拟筛选记录"
created: 2026-05-31
type: experiment-record
status: draft
topics: [type/experiment, status/draft, topic/chai-1, topic/ppi, topic/virtual-screening, chapter/8]
source_files: ["02_方法笔记/Chai1互作蛋白虚拟筛选.md", "06_原始学习素材/第八章/解包/第八章思路解析/互作蛋白虚拟筛选/batch_predict.py", "06_原始学习素材/第八章/解包/第八章思路解析/互作蛋白虚拟筛选/score.py"]
zotero_items: []
bibtex_keys: []
related: ["../02_方法笔记/Chai1互作蛋白虚拟筛选.md", "../01_课程章节索引/章节精读/第08章_计算思路解析精读.md"]
wiki_role: experiment
source_count: 3
last_reviewed: 2026-05-31
claims: [p13_chai1_ppi_screening_2026_05_31]
relations:
  - type: applies_to
    target: "../02_方法笔记/Chai1互作蛋白虚拟筛选.md"
  - type: derived_from
    target: "../06_原始学习素材/第八章/解包/第八章思路解析/互作蛋白虚拟筛选/batch_predict.py"
---

# 模板：Chai-1互作蛋白虚拟筛选记录

## 任务定义

- 任务 ID：待填。
- Query 蛋白：待填。
- Target 集合：待填。
- 生物学问题：待填。
- 筛选目的：互作候选发现 / 排序 / 结构解释 / 后续实验设计。

## 输入文件

| 输入 | 路径 | 检查结果 |
|:---|:---|:---|
| query FASTA | 待填 | 单条序列；记录 header、长度、来源。 |
| target FASTA | 待填 | 多条序列；记录数量、去重和来源。 |
| Chai-1 脚本 | 待填 | 与 `batch_predict.py` 是否一致。 |
| scoring 脚本 | 待填 | 与 `score.py` 是否一致。 |

## 运行环境

| 字段 | 值 |
|:---|:---|
| 机器/平台 | 待填 |
| GPU | 待填 |
| CUDA | 待填 |
| Python 环境 | 待填 |
| `chai_lab` 版本 | 待填 |
| seed | 待填 |
| 输出目录 | 待填 |

## 参数

| 参数 | 值 | 说明 |
|:---|:---|:---|
| `num_trunk_recycles` | 待填 | 默认脚本为 3。 |
| `num_diffn_timesteps` | 待填 | 默认脚本为 200。 |
| `use_esm_embeddings` | 待填 | 默认脚本为 True。 |
| skip completed | 待填 | 是否跳过已有 `scores_summary.txt`。 |

## 结果汇总

| target | status | max_score | mean_score | best_model_idx | best_model_file | evidence_maturity | interface_qc_passed | decision |
|:---|:---|---:|---:|---:|:---|:---|:---|:---|
| 待填 | success/error/skipped | 待填 | 待填 | 待填 | 待填 | case-study/dry-run/validated-computation/experimental-result | pass/review/fail | 保留/复核/淘汰 |

## Top 模型复核

| target | chain_check | interface_contacts | clash | confidence_or_pae | biological_plausibility | note |
|:---|:---|:---|:---|:---|:---|:---|
| 待填 | pass/review/fail | 待填 | pass/review/fail | 待填 | pass/review/fail | 待填 |

## P31 工作台分级

| target | aggregate_score_boundary | evidence_maturity | candidate_priority | boundary_note |
|:---|:---|:---|:---|:---|
| 待填 | 排序线索，不是实验结合强度。 | case-study/dry-run/validated-computation/experimental-result | high/medium/low/review | 文献案例和本地结果必须分层记录。 |

## 结论

- Top 候选：待填。
- 失败项：待填。
- 下一步：结构可视化 / 界面突变设计 / docking / MD / wet-lab 验证。
