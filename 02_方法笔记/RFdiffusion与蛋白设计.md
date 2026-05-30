---
title: "RFdiffusion 与蛋白设计"
created: 2026-05-30
type: method-note
status: active
topics: [type/method, status/active, topic/rfdiffusion, topic/protein-design, chapter/6]
source_files: ["第六章/第六章RFD3_第七章.rar"]
zotero_items: ["UKX5E6IB", "ZYFCZKMH", "EBQ7CNVI", "V2WLND5M", "QCD2DXXI", "UN6R4C6J"]
bibtex_keys: ["watson_novo_2023", "ahern_atom_2025", "bennett_atomically_2025", "dauparas_robust_2022", "pacesa_bindcraft_2024", "dauparas_atomic_2025"]
related: ["../03_文献笔记/RFdiffusion蛋白设计.md", "../03_文献笔记/ProteinMPNN序列设计.md", "../03_文献笔记/BindCraft与LigandMPNN.md", "../04_实验记录/模板_RFdiffusion骨架生成记录.md", "../04_实验记录/模板_ProteinMPNN序列设计记录.md", "../04_实验记录/模板_BindCraft_LigandMPNN设计记录.md"]
---

# RFdiffusion 与蛋白设计

第六章资料包指向 RFdiffusion/RFD3 与蛋白设计主题。知识库把这条方法线拆成四层：任务定义、骨架生成、序列设计、结构/功能复核。当前资料包尚未解压运行，本方法卡先给出可执行记录规范，后续任何实际运行都应按模板写入 `04_实验记录/`。

## 方法层次

- RFdiffusion：从结构约束生成蛋白骨架。
- RFdiffusion2：更细粒度地处理活性位点和原子级 scaffolding。
- ProteinMPNN：给定骨架进行序列设计。
- BindCraft/LigandMPNN：面向功能 binder 或配体环境的设计流程。

## 可执行流程

1. 定义设计任务：de novo fold、motif scaffolding、enzyme active-site scaffolding、protein binder、antibody/binder 或 ligand-aware sequence design。
2. 准备目标结构：记录 PDB/mmCIF/预测模型路径、链 ID、保留链、配体/金属/辅因子、低置信区和需要固定的 motif。
3. 定义约束：记录 hotspot residues、contig map、固定残基、对称性、界面距离、活性位点几何或配体邻近残基。
4. 运行骨架生成：记录 RFdiffusion/RFD3/RFdiffusion2 版本、checkpoint、seed、num_designs、输入 PDB、contig 和输出目录。
5. 骨架初筛：按折叠合理性、motif RMSD、界面接触、二级结构、冲突、疏水核心和设计多样性过滤。
6. 序列设计：对保留骨架运行 ProteinMPNN 或 LigandMPNN，记录 temperature、num_seq_per_target、固定残基、配体/非蛋白原子上下文和输出 FASTA。
7. 结构回折叠验证：用 AlphaFold2/AlphaFold3/Boltz2 或同类工具验证设计序列，记录 pLDDT、pTM/ipTM、PAE、interface pLDDT、motif RMSD 和是否保持目标界面。
8. 功能复核：对 binder 看界面面积、氢键/盐桥/疏水接触、形状互补、电荷互补；对 enzyme scaffold 看活性位点几何、催化残基距离和底物方向；对 ligand-aware 设计看配体邻近残基构象。
9. 进入后续验证：合格设计进入 docking、MD/BioEmu、Boltz2/亲和力预测、表达可行性评估或实验合成；失败设计保留淘汰原因。

## 输入检查表

| 输入 | 必填记录 | 检查点 |
|:---|:---|:---|
| 任务类型 | fold/motif/enzyme/binder/ligand-aware | 决定后续约束和评分指标 |
| 目标结构 | PDB/mmCIF/预测模型路径、链 ID | 结构来源和生物装配明确 |
| motif/active site | 残基编号、原子、几何约束 | 编号与输入结构一致 |
| hotspot/interface | 热点残基、目标链、界面定义 | 不把低置信区当作稳定界面 |
| ligand/metal/cofactor | CCD/SMILES/坐标、保留规则 | LigandMPNN 或后续复核需要 |
| 设计参数 | checkpoint、seed、num_designs、contig | 可复现同一批设计 |

## 输出文件规范

| 输出 | 用途 | 是否必须保留 |
|:---|:---|:---|
| RFdiffusion 输出 PDB | 骨架生成原始结果 | 必须 |
| 设计参数 YAML/命令记录 | 复现运行 | 必须 |
| 骨架 QC 表 | 初筛、淘汰和排序 | 必须 |
| ProteinMPNN/LigandMPNN FASTA | 序列设计结果 | 必须 |
| 回折叠结构 | 验证设计序列能否形成目标构象 | 必须 |
| 界面/活性位点复核图 | 报告和人工判断 | 建议 |
| 失败案例表 | 调参依据 | 建议 |

## 质量门槛

- `pass`：motif 或界面保持良好，结构回折叠置信度高，关键相互作用合理，序列无明显表达/聚集风险，设计多样性可接受。
- `review`：整体折叠可用，但 motif RMSD、界面接触、活性位点几何、低置信区或序列性质仍需人工复核。
- `fail`：骨架断裂、motif 丢失、界面错位、回折叠失败、活性位点几何破坏、严重冲突或设计不可解释。

## 常见失败模式

- contig 或残基编号错位，导致固定 motif 不在预期位置。
- 目标链、生物装配或配体保留规则错误，导致设计面向了错误界面。
- 只看生成模型输出，不做 AlphaFold/Boltz 回折叠验证。
- ProteinMPNN 生成序列后没有保留固定残基或关键功能位点。
- binder 设计只看界面 score，不复核极性未满足、疏水暴露、电荷冲突和聚集风险。
- enzyme scaffold 只看 backbone RMSD，不检查催化原子几何和底物方向。

## 实验记录模板

- 骨架生成：`../04_实验记录/模板_RFdiffusion骨架生成记录.md`
- 序列设计：`../04_实验记录/模板_ProteinMPNN序列设计记录.md`
- Binder/ligand-aware 设计：`../04_实验记录/模板_BindCraft_LigandMPNN设计记录.md`

## 文献依据

- `watson_novo_2023`：RFdiffusion 主文献。
- `ahern_atom_2025`：RFdiffusion2 活性位点 scaffolding。
- `bennett_atomically_2025`：抗体和表位特异性 binder 设计扩展。
- `dauparas_robust_2022`：ProteinMPNN 序列设计。
- `pacesa_bindcraft_2024`、`dauparas_atomic_2025`：后续 binder 和 ligand-aware 设计。
