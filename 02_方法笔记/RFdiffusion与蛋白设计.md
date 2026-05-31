---
title: "RFdiffusion 与蛋白设计"
created: 2026-05-30
type: method-note
status: active
topics: [type/method, status/active, topic/rfdiffusion, topic/protein-design, chapter/6]
source_files: ["06_原始学习素材/第六章/第六七章RFD3多组分设计.pdf", "06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/全文.md", "06_原始学习素材/第六章/补充资料/rfd3_disco/区别.html", "06_原始学习素材/第六章/补充资料/蛋白设计最新文献/s41586-026-10328-7(1).pdf", "06_原始学习素材/第八章/解包/第八章思路解析/蛋白设计/蛋白设计.pdf"]
zotero_items: ["UKX5E6IB", "ZYFCZKMH", "EBQ7CNVI", "V2WLND5M", "QCD2DXXI", "UN6R4C6J", "TPR3JY6N", "V6Y5EEZL"]
bibtex_keys: ["watson_novo_2023", "ahern_atom_2025", "bennett_atomically_2025", "dauparas_robust_2022", "pacesa_bindcraft_2024", "dauparas_atomic_2025", "yang_w_past_2026", "zhu_novo_2026"]
related: ["../03_文献笔记/RFdiffusion蛋白设计.md", "../03_文献笔记/ProteinMPNN序列设计.md", "../03_文献笔记/BindCraft与LigandMPNN.md", "../04_实验记录/模板_RFdiffusion骨架生成记录.md", "../04_实验记录/模板_ProteinMPNN序列设计记录.md", "../04_实验记录/模板_BindCraft_LigandMPNN设计记录.md"]
wiki_role: method
source_count: 11
last_reviewed: 2026-05-31
claims: [watson_novo_2023, ahern_atom_2025, bennett_atomically_2025, dauparas_robust_2022, pacesa_bindcraft_2024, dauparas_atomic_2025, yang_w_past_2026, zhu_novo_2026]
relations:
  - type: derived_from
    target: "../06_原始学习素材/第六章/第六七章RFD3多组分设计.pdf"
  - type: derived_from
    target: "../06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/全文.md"
  - type: supports
    target: "../03_文献笔记/RFdiffusion蛋白设计.md"
  - type: extends
    target: "../03_文献笔记/ProteinMPNN序列设计.md"
  - type: applies_to
    target: "../04_实验记录/模板_RFdiffusion骨架生成记录.md"
  - type: applies_to
    target: "../04_实验记录/模板_ProteinMPNN序列设计记录.md"
---

# RFdiffusion 与蛋白设计

第六章新增 PDF 指向 RFdiffusion/RFD3 与蛋白设计主题。知识库把这条方法线拆成四层：任务定义、骨架生成、序列设计、结构/功能复核。当前已有课件全文提取和 OCR，但尚未出现实际 RFD3 运行输出；后续任何实际运行都应按模板写入 `04_实验记录/`。

## 方法层次

- RFdiffusion：从结构约束生成蛋白骨架。
- RFdiffusion2：更细粒度地处理活性位点和原子级 scaffolding。
- RFD3/RFdiffusion3：面向全原子、多组分复合物设计，覆盖蛋白、小分子、核酸、binder 和理论酶等复杂约束场景。
- ProteinMPNN：给定骨架进行序列设计。
- BindCraft/LigandMPNN：面向功能 binder 或配体环境的设计流程。

## 可执行流程

1. 定义设计任务：de novo fold、motif scaffolding、enzyme active-site scaffolding、protein binder、antibody/binder、nucleic-acid binder 或 ligand-aware sequence design。
2. 准备目标结构：记录 PDB/mmCIF/预测模型路径、链 ID、保留链、配体/金属/辅因子、低置信区和需要固定的 motif。
3. 定义约束：记录 hotspot residues、contig map、固定残基、对称性、界面距离、活性位点几何或配体邻近残基。
4. 运行骨架生成：记录 RFdiffusion/RFD3/RFdiffusion2 版本、checkpoint、seed、num_designs、输入 PDB、contig 和输出目录。
5. 骨架初筛：按折叠合理性、motif RMSD、界面接触、二级结构、冲突、疏水核心和设计多样性过滤。
6. 序列设计：对保留骨架运行 ProteinMPNN 或 LigandMPNN，记录 temperature、num_seq_per_target、固定残基、配体/非蛋白原子上下文和输出 FASTA。
7. 结构回折叠验证：用 AlphaFold2/AlphaFold3/Boltz2 或同类工具验证设计序列，记录 pLDDT、pTM/ipTM、PAE、interface pLDDT、motif RMSD 和是否保持目标界面。
8. 功能复核：对 binder 看界面面积、氢键/盐桥/疏水接触、形状互补、电荷互补；对 enzyme scaffold 看活性位点几何、催化残基距离和底物方向；对 ligand-aware 设计看配体邻近残基构象。
9. 进入后续验证：合格设计进入 docking、MD/BioEmu、Boltz2/亲和力预测、表达可行性评估或实验合成；失败设计保留淘汰原因。

## 第六章课件锚点

| 主题 | 来源页 | 方法含义 |
|:---|:---|:---|
| 蛋白设计范式演进 | `06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-003.md` | 从 Rosetta/AlphaFold 过渡到生成式 AI |
| ProteinMPNN | `06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-016.md` | 骨架到序列的关键步骤 |
| RFdiffusion | `06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-018.md` | 扩散生成蛋白结构和功能 |
| RFdiffusion 演进 | `06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-021.md` | 从结构生成走向多分子体系生成 |
| RFD3/RFdiffusion3 | `06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-035.md` | 全原子、多组分复杂约束设计 |
| 核酸抑制剂设计 | `06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-081.md` | 转录因子/核酸药物场景 |
| 理论酶设计 | `06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/pages/page-094.md` | 酶 scaffold、QM/DFT 假设和几何复核 |

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
- `yang_w_past_2026`：第六章新增 Nature 综述锚点，用于把 de novo protein design 的历史、当前工具链和未来方向串到同一条方法谱系。
- `zhu_novo_2026`：第八章 BabA binder 范文锚点，用于教学拆解 RFdiffusion3、ProteinMPNN、回折叠、对接和 MD 的流程边界。
