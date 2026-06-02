# 代码案例索引

本页汇总在线书籍的可复制代码案例。所有示例默认是教学 dry-run 或解析脚本，不代表已经完成 GPU 大模型生产运行。

| 章节 | 文件 | 语言/配置 | 用途 |
|:---|:---|:---|:---|
| 第 1 章 | [`chapter-01-env-check.ps1`](../assets/code/chapter-01-env-check.ps1) | `powershell` | 在项目根目录运行环境和输入文件 dry-run 检查，把输出转成实验记录字段。 |
| 第 2 章 | [`chapter-02-structure-review.pml`](../assets/code/chapter-02-structure-review.pml) | `pymol` | 用同一套视图命令复核实验结构和预测结构，避免只凭漂亮渲染判断结构可信度。 |
| 第 3 章 | [`chapter-03-docking-dry-run.sh`](../assets/code/chapter-03-docking-dry-run.sh) | `bash` | 用最小受体和 3 个配体验证 box、输入格式、输出表和筛选阈值，而不是直接跑全库。 |
| 第 3 章 | [`chapter-03-aidd-triage-dry-run.py`](../assets/code/chapter-03-aidd-triage-dry-run.py) | `python` | 用 RDKit/datamol 可选依赖或 fallback 生成候选 triage 表，固化 `pose_qc_passed` 和 `filter_reason` 字段。 |
| 第 4 章 | [`chapter-04-md-summary.py`](../assets/code/chapter-04-md-summary.py) | `python` | 用已经完成的小轨迹输出 RMSD 摘要，训练读者区分轨迹 QC、代表构象和科学解释。 |
| 第 5 章 | [`chapter-05-boltz2-summary.py`](../assets/code/chapter-05-boltz2-summary.py) | `python` | 读取 Boltz2 结果表，生成排序摘要，并明确 affinity 输出是模型预测值而不是实验测定值。 |
| 第 5 章 | [`chapter-05-affinity-calibration-dry-run.py`](../assets/code/chapter-05-affinity-calibration-dry-run.py) | `python` | 把预测表转换成 `calibration_available`、`rank_bucket` 和边界说明，不把模型值写成实验结果。 |
| 第 6 章 | [`chapter-06-design-config.yaml`](../assets/code/chapter-06-design-config.yaml) | `yaml` | 用配置模板记录 target、contig、hotspot、seed 和输出筛选规则，先做小批量 dry-run。 |
| 第 6 章 | [`chapter-06-design-qc-dry-run.py`](../assets/code/chapter-06-design-qc-dry-run.py) | `python` | 用 motif RMSD、回折叠 RMSD、界面接触和 PAE 生成设计 QC 表。 |
| 第 7 章 | [`chapter-07-agent-validation.ps1`](../assets/code/chapter-07-agent-validation.ps1) | `powershell` | 把 Agent 任务拆成可审查闭环：先读来源，再改文件，最后运行验证并写回维护记录。 |
| 第 8 章 | [`chapter-08-project-priority.py`](../assets/code/chapter-08-project-priority.py) | `python` | 把候选项目拆成证据、方法、缺口、下一步实验和可产出物，防止把文献案例误写成本项目结果。 |
| 第 8 章 | [`chapter-08-workbench-priority-dry-run.py`](../assets/code/chapter-08-workbench-priority-dry-run.py) | `python` | 按 `evidence_maturity` 区分文献案例、dry-run、本地计算和实验结果。 |

## 使用边界

- 代码用于课程演示和记录模板训练，运行前需要按本地环境修改输入路径。
- GPU/云端工具在 P24 阶段只提供 dry-run、配置样例或结果解析样例。
- P31 新增脚本优先输出记录字段和 QC 决策，不替代真实 docking、MD、DiffDock、Boltz2 或蛋白设计运行。
- 真实研究结果必须回写到 `04_实验记录/`，不能只停留在书籍页面。
