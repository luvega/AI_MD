# AIDD dry-run 数据流程

P31 将第 3/5/6/8 章的代码案例从“单个命令示例”补强为“可输出记录字段的教学 dry-run”。这些脚本用于训练输入检查、候选分级、QC 字段和证据边界，不代表已经完成 docking、Boltz2、RFdiffusion/RFD3、Chai-1 或实验验证。

## 依赖层级

| 层级 | 说明 | 适用场景 |
|:---|:---|:---|
| 无依赖 fallback | 只用 Python 标准库，生成示例 TSV。 | 课堂演示、模板字段说明、CI 轻量检查。 |
| RDKit/datamol | 解析 SMILES、标准化分子并计算基础描述符。 | 化合物库初筛和虚拟筛选输入清洗。 |
| medchem | 对候选库做成药性规则和结构警报复核。 | lead-like / fragment-like / alert triage。 |
| MDAnalysis/OpenMM | 轨迹、RMSD/RMSF、接触和代表构象分析。 | 真实 MD 结果解释；本页不生成轨迹结论。 |
| DiffDock / docking 工具 | 生成或解析 pose 与 confidence。 | pose 线索；不输出亲和力或实验活性。 |

## 脚本入口

| 章节 | 脚本 | 默认输出 | 主要字段 | 证据边界 |
|:---|:---|:---|:---|:---|
| 第 3 章 | [`chapter-03-aidd-triage-dry-run.py`](../assets/code/chapter-03-aidd-triage-dry-run.py) | `outputs/chapter-03-aidd-triage.tsv` | `parse_status`, `rule_of_five_pass`, `alert_status`, `pose_qc_passed`, `filter_reason` | 只做候选和输入 triage，不产生 docking score。 |
| 第 5 章 | [`chapter-05-affinity-calibration-dry-run.py`](../assets/code/chapter-05-affinity-calibration-dry-run.py) | `outputs/chapter-05-affinity-calibration.tsv` | `calibration_available`, `rank_bucket`, `interpretation`, `boundary_note` | 只解释预测表，不把预测值改写成实验 Kd/IC50。 |
| 第 6 章 | [`chapter-06-design-qc-dry-run.py`](../assets/code/chapter-06-design-qc-dry-run.py) | `outputs/chapter-06-design-qc.tsv` | `motif_rmsd`, `refold_rmsd`, `pae_interface`, `interface_qc_passed`, `discard_reason` | 只做计算候选 QC，不说明可表达、可折叠或可结合。 |
| 第 8 章 | [`chapter-08-workbench-priority-dry-run.py`](../assets/code/chapter-08-workbench-priority-dry-run.py) | `outputs/chapter-08-workbench-priority.tsv` | `evidence_maturity`, `priority_score`, `decision`, `boundary_note` | 强制区分文献案例、dry-run、本地计算和实验结果。 |

## 运行示例

```powershell
python book\docs\assets\code\chapter-03-aidd-triage-dry-run.py --out outputs\chapter-03-aidd-triage.tsv
python book\docs\assets\code\chapter-05-affinity-calibration-dry-run.py --out outputs\chapter-05-affinity-calibration.tsv
python book\docs\assets\code\chapter-06-design-qc-dry-run.py --out outputs\chapter-06-design-qc.tsv
python book\docs\assets\code\chapter-08-workbench-priority-dry-run.py --out outputs\chapter-08-workbench-priority.tsv
```

## 回写规则

| 输出字段 | 回写位置 | 写作边界 |
|:---|:---|:---|
| `pose_qc_passed`, `filter_reason` | `04_实验记录/模板_对接虚拟筛选记录.md` | docking score 和 pose 只作为排序/构象线索。 |
| `calibration_available`, `rank_bucket` | `04_实验记录/模板_Boltz2亲和力记录.md` | predicted affinity 只能作为模型读数。 |
| `interface_qc_passed`, `discard_reason` | `04_实验记录/模板_RFdiffusion骨架生成记录.md` | 生成结构必须经回折叠和界面复核。 |
| `evidence_maturity`, `decision` | `04_实验记录/模板_Chai1互作蛋白虚拟筛选记录.md` 与研究工作台 | 文献案例不能写成本项目结果。 |

## 下一步

1. 若脚本从 fallback 升级到 RDKit/datamol/medchem 实际处理，应记录环境、版本、输入库来源和失败项。
2. 若进入 MD 或 DiffDock 真实运行，应先建立正式实验记录，再把可复述结论写回章节或研究工作台。
3. 所有真实结果都需要保留输入、参数、输出路径、QC 失败理由和待验证项。
