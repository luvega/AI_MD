---
title: "Chai-1互作蛋白虚拟筛选"
created: 2026-05-31
type: method-note
status: draft
topics: [type/method, status/draft, topic/ppi, topic/chai-1, topic/virtual-screening, chapter/8]
source_files: ["06_原始学习素材/第八章/解包/第八章思路解析/互作蛋白虚拟筛选/batch_predict.py", "06_原始学习素材/第八章/解包/第八章思路解析/互作蛋白虚拟筛选/score.py", "06_原始学习素材/第八章/全文提取/第八章计算思路解析/全文.md", "references/references.bib"]
zotero_items: ["待补正式锚点"]
bibtex_keys: ["chai_discovery_chai-1_2024"]
related: ["../01_课程章节索引/章节精读/第08章_计算思路解析精读.md", "../04_实验记录/模板_Chai1互作蛋白虚拟筛选记录.md", "../03_文献笔记/Chai1方法与PPI筛选.md", "AI多组分对接与虚拟筛选.md", "Boltz2亲和力预测.md"]
wiki_role: method
source_count: 4
last_reviewed: 2026-06-02
claims: [p13_chai1_ppi_screening_2026_05_31, chai_discovery_chai-1_2024]
relations:
  - type: derived_from
    target: "../06_原始学习素材/第八章/解包/第八章思路解析/互作蛋白虚拟筛选/batch_predict.py"
  - type: derived_from
    target: "../06_原始学习素材/第八章/解包/第八章思路解析/互作蛋白虚拟筛选/score.py"
  - type: applies_to
    target: "../04_实验记录/模板_Chai1互作蛋白虚拟筛选记录.md"
  - type: supports
    target: "../03_文献笔记/Chai1方法与PPI筛选.md"
  - type: extends
    target: "AI多组分对接与虚拟筛选.md"
---

# Chai-1互作蛋白虚拟筛选

## 本方法定位

本方法卡把第八章“互作蛋白虚拟筛选”脚本整理成可复现记录规范。它适合一个 query 蛋白对多个 target 蛋白做批量复合物建模和初筛排序。当前仓库只有脚本和课程资料，没有实际 Chai-1 运行输出。

P32 已补入 `chai_discovery_chai-1_2024` 作为正式 BibTeX 方法锚点。由于 Zotero Desktop 本地 API 不可用，Zotero item key 暂记为 `待补正式锚点`。

## 输入结构

| 输入 | 脚本默认路径 | 必填检查 |
|:---|:---|:---|
| Query FASTA | `PPIprotein/badian.fasta` | 只能有一条序列；记录 header、物种、长度和来源。 |
| Target FASTA | `PPIprotein/target.fasta` | 可多条序列；每条 target 需要唯一名称和来源。 |
| Chai-1 环境 | `chai_lab.chai1.run_inference` | 记录包版本、GPU、checkpoint/模型来源和 CUDA 环境。 |
| 输出根目录 | `/root/autodl-tmp/chai-outputs` | 每个 query-target 对应独立目录。 |

## 批量建模逻辑

`batch_predict.py` 会把 query 和每个 target 组合成 Chai-1 格式 FASTA，然后调用 `run_inference()`：

| 参数 | 脚本值 | 记录要求 |
|:---|:---|:---|
| `num_trunk_recycles` | `3` | 如果调整，必须记录原因。 |
| `num_diffn_timesteps` | `200` | 与运行时间和结果稳定性相关。 |
| `seed` | `42` | 用于复现。 |
| `device` | `cuda:0` | 记录 GPU 型号和显存。 |
| `use_esm_embeddings` | `True` | 记录是否启用。 |

脚本会跳过已经存在 `scores_summary.txt` 的输出目录；如果运行失败，会写入 `error.txt`。这意味着后续整理时必须区分成功建模、跳过、失败三类状态。

## 分数解析逻辑

`score.py` 遍历 `chai-outputs/` 下每个结果目录，读取 `scores_summary.txt` 中的 `Aggregate scores`，计算：

| 字段 | 解释 |
|:---|:---|
| `max_score` | 当前脚本默认排序字段；代表该 target 的最高 aggregate score。 |
| `mean_score` | 多个候选模型的平均分。 |
| `min_score` | 多个候选模型的最低分。 |
| `best_model_idx` | `max_score` 对应模型编号，用于定位 `pred.model_idx_<n>.cif`。 |
| `best_model_file` | 最佳模型 CIF 路径。 |

输出文件为 `chai_docking_score_rank.csv`，默认按 `max_score` 从高到低排序。

## QC 规则

- `aggregate_score` 只能作为候选排序信号，不能等同于真实 PPI 亲和力。
- Top target 必须打开最佳 CIF，检查链是否正确、界面是否真实接触、是否存在明显穿模或非物理拉伸。
- 需要结合模型置信度、PAE/界面区域可信度、界面残基、保守性、已知机制和后续实验可行性判断。
- 对失败项要保留 `error.txt`，不要直接从排序表中删除。

## 推荐记录输出

| 输出 | 用途 |
|:---|:---|
| `scores_summary.txt` | 单个 query-target 的原始 aggregate score 摘要。 |
| `pred.model_idx_*.cif` | 候选复合物结构。 |
| `chai_docking_score_rank.csv` | 批量排序结果。 |
| `error.txt` | 失败原因。 |
| 实验记录 | 使用 `../04_实验记录/模板_Chai1互作蛋白虚拟筛选记录.md`。 |
