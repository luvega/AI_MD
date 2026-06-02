---
title: "P31 数据分析与 AIDD dry-run 报告"
created: 2026-06-02
type: maintenance-report
status: active
topics: [online-book, aidd, dry-run, data-analysis, p31]
source_files: ["book/docs/resources/aidd-dry-runs.md", "book/docs/assets/code/chapter-03-aidd-triage-dry-run.py", "book/docs/assets/code/chapter-05-affinity-calibration-dry-run.py", "book/docs/assets/code/chapter-06-design-qc-dry-run.py", "book/docs/assets/code/chapter-08-workbench-priority-dry-run.py", "04_实验记录/模板_对接虚拟筛选记录.md", "04_实验记录/模板_Boltz2亲和力记录.md", "04_实验记录/模板_RFdiffusion骨架生成记录.md", "04_实验记录/模板_Chai1互作蛋白虚拟筛选记录.md"]
zotero_items: []
bibtex_keys: []
related: ["P28_重点章节Codex审稿报告.md", "P30_图示与版面升级报告.md", "../book/docs/resources/aidd-dry-runs.md", "../book/docs/resources/code-cases.md", "../04_实验记录/_index.md"]
wiki_role: maintenance
source_count: 9
last_reviewed: 2026-06-02
claims:
  - "P31 已为第 3/5/6/8 章新增 AIDD dry-run 数据流程脚本和课程资源页。"
  - "P31 新增内容只输出教学记录字段和 QC 决策，不生成 docking、亲和力、蛋白设计或 PPI 实验结论。"
relations:
  - type: extends
    target: "P30_图示与版面升级报告.md"
  - type: updates
    target: "../book/docs/resources/aidd-dry-runs.md"
  - type: updates
    target: "../book/docs/resources/code-cases.md"
  - type: updates
    target: "../04_实验记录/模板_对接虚拟筛选记录.md"
  - type: updates
    target: "../04_实验记录/模板_Boltz2亲和力记录.md"
  - type: updates
    target: "../04_实验记录/模板_RFdiffusion骨架生成记录.md"
  - type: updates
    target: "../04_实验记录/模板_Chai1互作蛋白虚拟筛选记录.md"
---
# P31 数据分析与 AIDD dry-run 报告

## 更新结论

P31 已把第 3/5/6/8 章的 AIDD 实操从“单个命令或配置示例”补强为“可输出记录字段的教学 dry-run”。新增脚本覆盖候选化合物 triage、亲和力预测解释、蛋白设计 QC 和研究工作台优先级排序，并同步升级对应实验记录模板。

本轮严格保持证据边界：新增脚本不运行 GPU 大模型，不生成真实 docking pose、Boltz2 预测、RFdiffusion/RFD3 设计、Chai-1 互作结果或实验活性。脚本输出只用于训练记录格式、QC 字段和下一步决策。

## 使用的 Codex skills

| Skill | P31 用途 |
|:---|:---|
| `datamol` | 作为 SMILES 标准化和分子清洗的可选路径，脚本在未安装时 fallback。 |
| `rdkit` | 作为基础描述符、rule-of-five 和 SMILES 解析的可选路径。 |
| `medchem` | 固化药物化学 triage 字段和结构警报复核位置。 |
| `molecular-dynamics` | 明确真实 MD 只在有轨迹后解释；本轮不伪造轨迹结论。 |
| `diffdock` | 明确 AI 对接输出是 pose/confidence 线索，不是亲和力或实验活性。 |

## 新增资源

| 资源 | 用途 |
|:---|:---|
| `book/docs/resources/aidd-dry-runs.md` | 汇总依赖层级、脚本入口、输出字段和回写规则。 |
| `chapter-03-aidd-triage-dry-run.py` | 输出 `parse_status`、`rule_of_five_pass`、`alert_status`、`pose_qc_passed` 和 `filter_reason`。 |
| `chapter-05-affinity-calibration-dry-run.py` | 输出 `calibration_available`、`rank_bucket`、`interpretation` 和 `boundary_note`。 |
| `chapter-06-design-qc-dry-run.py` | 输出 `motif_rmsd`、`refold_rmsd`、`pae_interface`、`interface_qc_passed` 和 `discard_reason`。 |
| `chapter-08-workbench-priority-dry-run.py` | 输出 `evidence_maturity`、`priority_score`、`decision` 和 `boundary_note`。 |

## 模板升级

| 模板 | 新增重点 |
|:---|:---|
| 对接虚拟筛选记录 | AIDD triage 表、pose QC、过滤理由和候选处理说明。 |
| Boltz2 亲和力记录 | 预测校准、rank bucket、对照类型和模型边界。 |
| RFdiffusion 骨架生成记录 | seed、checkpoint、回折叠 RMSD、PAE、界面 QC 和淘汰理由。 |
| Chai-1 互作蛋白虚拟筛选记录 | evidence maturity、aggregate score 边界和项目优先级字段。 |

## 后续交接

1. 若后续安装 RDKit/datamol/medchem 并处理真实化合物库，应把环境、输入库、失败项和输出 TSV 回写到正式实验记录。
2. 若运行 DiffDock、Uni-Dock、Boltz2、RFdiffusion/RFD3、ProteinMPNN、Chai-1 或 MD，应先建立 `04_实验记录/` 真实记录，再把可复述结论写入在线书籍。
3. 第 3/5/6/8 章的高风险 claim 仍按 P28 边界处理：score、predicted affinity、aggregate score 和生成结构均不得直接写成实验结论。
