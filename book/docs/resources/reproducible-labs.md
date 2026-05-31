# 复现实验资源

P24 的课程资源层采用“先 dry-run、再真实运行、最后沉淀记录”的原则。这里列出每章最小复现入口，帮助读者从讲义进入方法卡和实验记录模板。

| 章节 | 软件/界面 | 代码入口 | 截图入口 | 当前状态 |
|:---|:---|:---|:---|:---|
| 第 1 章 | PowerShell / Linux shell | [`chapter-01-env-check.ps1`](../assets/code/chapter-01-env-check.ps1) | [`chapter-01-env-check.png`](../assets/screenshots/chapter-01-env-check.png) | dry-run / parser |
| 第 2 章 | PyMOL / ChimeraX | [`chapter-02-structure-review.pml`](../assets/code/chapter-02-structure-review.pml) | [`chapter-02-pymol-review.png`](../assets/screenshots/chapter-02-pymol-review.png) | dry-run / parser |
| 第 3 章 | Uni-Dock / Vina-style dry-run | [`chapter-03-docking-dry-run.sh`](../assets/code/chapter-03-docking-dry-run.sh) | [`chapter-03-docking-funnel.png`](../assets/screenshots/chapter-03-docking-funnel.png) | dry-run / parser |
| 第 4 章 | MDAnalysis / MDTraj-style analysis | [`chapter-04-md-summary.py`](../assets/code/chapter-04-md-summary.py) | [`chapter-04-md-analysis.png`](../assets/screenshots/chapter-04-md-analysis.png) | dry-run / parser |
| 第 5 章 | Boltz2 result table dry-run | [`chapter-05-boltz2-summary.py`](../assets/code/chapter-05-boltz2-summary.py) | [`chapter-05-boltz2-results.png`](../assets/screenshots/chapter-05-boltz2-results.png) | dry-run / parser |
| 第 6 章 | RFdiffusion / ProteinMPNN dry-run config | [`chapter-06-design-config.yaml`](../assets/code/chapter-06-design-config.yaml) | [`chapter-06-protein-design-cycle.png`](../assets/screenshots/chapter-06-protein-design-cycle.png) | dry-run / parser |
| 第 7 章 | Codex / Claude Code workflow | [`chapter-07-agent-validation.ps1`](../assets/code/chapter-07-agent-validation.ps1) | [`chapter-07-agent-verify-loop.png`](../assets/screenshots/chapter-07-agent-verify-loop.png) | dry-run / parser |
| 第 8 章 | research project pool / Chai-1 panel dry-run | [`chapter-08-project-priority.py`](../assets/code/chapter-08-project-priority.py) | [`chapter-08-project-pool.png`](../assets/screenshots/chapter-08-project-pool.png) | dry-run / parser |

## 建设规则

- 原始 PDF、课件和补充材料继续只读，不复制其中图表到在线书籍。
- 无法本地运行的大模型工具，先记录输入 schema、参数、输出字段和失败替代方案。
- 每次把 dry-run 升级为真实运行，都应同步更新 `04_实验记录/`、本页状态和相关章节的边界提示。
- 公开页面截图必须记录 URL、访问日期和版权边界；本地截图必须记录命令、环境和输入来源。
