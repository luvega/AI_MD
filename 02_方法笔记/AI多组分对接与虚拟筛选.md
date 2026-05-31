---
title: "AI 多组分对接与虚拟筛选"
created: 2026-05-30
type: method-note
status: active
topics: [type/method, status/active, topic/docking, chapter/3]
source_files: ["06_原始学习素材/第03章_AI多组分对接与虚拟筛选/原始PDF/第三章AI多组分对接与正-反-互作虚拟筛选.pdf", "06_原始学习素材/第03章_AI多组分对接与虚拟筛选/全文提取/第三章AI多组分对接与正-反-互作虚拟筛选/全文.md", "06_原始学习素材/第八章/解包/第八章思路解析/正向虚拟筛选/一区14.1Advanced Science - 2026.pdf", "06_原始学习素材/第八章/解包/第八章思路解析/正向虚拟筛选/三区3.9正向虚拟筛选.pdf", "06_原始学习素材/第八章/解包/第八章思路解析/正向虚拟筛选/基于已有数据微调的机器学习的AI虚拟筛选.pdf"]
zotero_items: ["UOUH33GQ", "T2O1ECSF", "R2W3SF5S", "57K986LK", "QXKW6K78", "YUMKNHSK", "Y4ARSYCQ"]
bibtex_keys: ["du_dockey_2023", "agrawal_benchmarking_2019", "crampon_machine-learning_2022", "gu_benchmarking_2025", "sui_targeting_2026", "shen_structure-based_2026", "tomarchio_reproducible_2026"]
related: ["../01_课程章节索引/章节精读/第03章_AI多组分对接与虚拟筛选精读.md", "../03_文献笔记/分子对接与虚拟筛选.md", "../04_实验记录/模板_对接虚拟筛选记录.md", "MSA与Uni-Dock补充.md"]
wiki_role: method
source_count: 9
last_reviewed: 2026-05-31
claims: [du_dockey_2023, agrawal_benchmarking_2019, crampon_machine-learning_2022, gu_benchmarking_2025, sui_targeting_2026, shen_structure-based_2026, tomarchio_reproducible_2026]
relations:
  - type: derived_from
    target: "../06_原始学习素材/第03章_AI多组分对接与虚拟筛选/全文提取/第三章AI多组分对接与正-反-互作虚拟筛选/全文.md"
  - type: supports
    target: "../03_文献笔记/分子对接与虚拟筛选.md"
  - type: applies_to
    target: "../04_实验记录/模板_对接虚拟筛选记录.md"
  - type: depends_on
    target: "PyMOL与Chimera可视化.md"
---

# AI 多组分对接与虚拟筛选

第三章是项目中的对接和筛选主线，覆盖多组分对接、正反互作虚拟筛选和相关输入准备。本方法卡把课件流程落成可执行记录规范：受体、配体、搜索空间、评分、top pose 复核和筛选表必须同时保存。

## 知识库落点

- 课程 PDF 已归档到 `06_原始学习素材/第03章_AI多组分对接与虚拟筛选/`；补充压缩包统一保留在 `06_原始学习素材/第三章/`。
- 对接方法总结写入本笔记。
- 具体靶点、配体、参数和结果应写入 `04_实验记录/`，优先使用 `模板_对接虚拟筛选记录.md`。
- 文献依据见 `03_文献笔记/分子对接与虚拟筛选.md`。

## 可执行流程

1. 定义任务：确认是单靶点 docking、批量虚拟筛选、蛋白-肽 docking、多组分复合物还是反向筛选。
2. 准备受体：选择 PDB/mmCIF 来源，记录链 ID、保留/删除水分子、金属、辅因子、修饰残基、缺失环区和质子化假设。
3. 准备配体：记录 SMILES/SDF/MOL2/PDBQT 来源，生成 3D 构象，检查质子化、互变异构、手性、电荷和能量最小化状态。
4. 定义 box：来自共晶配体、活性位点残基、保守位点、突变位点或盲对接；记录 center、size、单位和依据。
5. 运行对接：记录软件、版本、参数、随机种子、exhaustiveness/num_modes、输入列表和输出目录。
6. 结果排序：保留原始 score、排名、pose 文件、相互作用摘要和任何重打分结果。
7. top pose 复核：用 PyMOL/Chimera 检查空间冲突、关键相互作用、配体构象、口袋合理性和水/金属/辅因子处理。
8. 后续分流：通过的候选进入 MD、MM-GBSA/FEP、Boltz2 或实验验证；不通过的候选记录淘汰原因。

## 受体准备检查表

| 检查项 | 必填记录 | 合格标准 |
|:---|:---|:---|
| 结构来源 | PDB/mmCIF/预测模型路径、版本、链 ID | 来源可追踪，链和生物装配明确 |
| 缺失区域 | 缺失残基、loop、末端、低置信区 | 不在口袋核心，或已说明补建方式 |
| 水和辅因子 | 删除/保留规则，关键水、金属、辅因子 ID | 与已知机制或共晶结构一致 |
| 质子化/电荷 | pH、工具、关键 His/Asp/Glu/Lys 状态 | 活性位点电荷假设明确 |
| 输出格式 | PDB/PDBQT/mmCIF 路径 | 能被 docking 软件直接读取 |

## 配体准备检查表

| 检查项 | 必填记录 | 合格标准 |
|:---|:---|:---|
| 配体来源 | SMILES/SDF/MOL2/数据库 ID | ID、结构和批次可追踪 |
| 化学状态 | 质子化、互变异构、手性、电荷 | 与 pH 和实验条件一致 |
| 3D 构象 | 构象生成工具、数量、最小化方法 | 无明显键长/角度异常 |
| 文件格式 | SDF/MOL2/PDBQT 输出路径 | 原子名、电荷、键级未丢失 |
| 批量清单 | ligand_id、source、input_path、prepared_path | 可重新筛选同一批次 |

## Box 与参数记录

| 字段 | 说明 |
|:---|:---|
| `box_center_x/y/z` | 搜索空间中心坐标，保留单位和来源 |
| `box_size_x/y/z` | 搜索空间尺寸；应覆盖口袋、关键残基和配体运动余量 |
| `box_basis` | 共晶配体、口袋残基、盲对接或文献位点 |
| `exhaustiveness` | 搜索强度；批量初筛和精筛应区分 |
| `num_modes` | 每个配体保留姿态数 |
| `seed` | 随机种子；没有种子时记录“未固定” |

## Score 与复核规则

- score 只能用于同一软件、同一参数、同一受体准备流程下的候选排序。
- 不同 docking 软件或不同 score 不能直接横向比较；需要重打分或结构复核。
- top pose 必须同时满足：无严重空间冲突、关键相互作用合理、配体构象可信、口袋方向可解释。
- 蛋白-肽 docking 不应只看全局 score，应额外看肽链构象、界面接触、疏水/电荷互补和是否有非物理拉伸。
- 多组分体系要明确每个组分是否参与打分；未参与的链、金属或辅因子不能在解释中被当作已建模因素。

## 文献依据扩展

- `du_dockey_2023` 支撑大规模 docking/虚拟筛选工具化流程，适合放在受体、配体、box 和结果表规范之前作为流程入口。
- `crampon_machine-learning_2022` 用于解释机器学习 docking/重打分的角色：它可以帮助排序或补充分数，但不能省略输入准备和 pose 复核。
- `gu_benchmarking_2025` 用于 AI-powered docking 的 benchmark 视角，提醒第三章把 score、top pose 和后续验证分开记录。
- `agrawal_benchmarking_2019` 用于蛋白-肽 docking 边界，肽链构象和界面接触必须单独复核。
- `sui_targeting_2026`、`shen_structure-based_2026` 和 `tomarchio_reproducible_2026` 是第八章补充 PDF 的正式锚点，分别覆盖机制驱动靶点筛选、APE1 结构口袋虚拟筛选、scaffold-aware ML + ensemble docking + MD 的可复现筛选框架。

## Top Pose 复核表

| ligand_id | rank | score | pose_path | 关键相互作用 | 冲突 | 构象合理性 | 处理结论 |
|:---|---:|---:|:---|:---|:---|:---|:---|
| LIG001 | 1 | 待填 | `outputs/LIG001_pose1.pdbqt` | H-bond/盐桥/疏水待填 | 无/有 | 合理/可疑 | 保留/淘汰/重跑 |

## 筛选结果表模板

| batch_id | target | ligand_id | source | score | rank | pose_path | interaction_summary | qc_status | next_step |
|:---|:---|:---|:---|---:|---:|:---|:---|:---|:---|
| dock-YYYYMMDD | targetA | LIG001 | 待填 | 待填 | 1 | 待填 | 待填 | pass/review/fail | MD/MM-GBSA/Boltz2/实验 |

## 质量门槛

- `pass`：输入来源明确，box 合理，score 排名靠前，结构复核无严重问题。
- `review`：score 有潜力，但质子化、关键水/金属、构象或口袋定义仍需复核。
- `fail`：输入错误、姿态穿模、关键相互作用缺失、配体构象非物理或无法解释。

## 记录模板入口

- 新建实验记录时复制 `../04_实验记录/模板_对接虚拟筛选记录.md`。
