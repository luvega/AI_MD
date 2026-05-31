# 第 6 章 RFD3/RFdiffusion、ProteinMPNN 与蛋白设计

## 本章导读

前五章主要围绕“已有靶点和候选分子如何建模、筛选和评价”展开；第六章把研究问题推进到“能否设计新的蛋白结构、序列或 binder”。这一步是 AI 辅助药物设计和生物工程中最具想象力的方向之一，也是最需要边界管理的方向之一。RFdiffusion、RFD3、ProteinMPNN、LigandMPNN、BindCraft 和 BoltzDesign 类方法让设计流程大幅提速，但生成一个看起来合理的结构并不等于获得可表达、可折叠、可结合、可功能化的分子。

本章的主线是把蛋白设计拆成任务定义、结构生成、序列设计、回折叠验证、界面/功能复核、亲和力/动态评估和实验可行性七层。RFdiffusion/RFD3 更偏向从约束和结构分布中生成骨架或复合物；ProteinMPNN/LigandMPNN 更偏向在骨架、配体或界面环境中设计序列；BindCraft 类流程强调把 AlphaFold2/结构预测和优化循环组合成 binder 设计管线。每一层都必须记录输入、参数、随机种子、模型版本和淘汰理由。

本章也吸收了第六章新增 Nature 综述 `yang_w_past_2026`，用于把 de novo protein design 放入更长的历史脉络中。现代扩散模型并不是从零出现的，它接续了理性设计、Rosetta 能量函数、结构预测、序列设计和实验筛选的长期发展。课程的重点不是追逐工具名，而是理解设计假设如何被逐层验证。

## 学习目标

完成本章后，读者应能区分 fold design、motif scaffolding、binder design、ligand binder design、enzyme active-site scaffolding、nucleic-acid binder 和 protein redesign 等任务；能解释 RFdiffusion/RFD3、ProteinMPNN、LigandMPNN 和 BindCraft 在流程中的位置；能写出一个设计任务的输入约束，包括 PDB/mmCIF、链 ID、motif 残基、hotspot、contig、目标界面、配体/核酸/金属和设计数量；能解释为什么设计输出必须经过回折叠、界面复核、稳定性判断、亲和力/MD 评估和实验可行性检查。

读者还应形成蛋白设计结果的证据分层意识。一个 RFD3 或 RFdiffusion 输出可以支持“模型生成了满足约束的候选骨架”；ProteinMPNN 输出可以支持“在该骨架上生成了若干序列候选”；AlphaFold/Boltz 回折叠可以支持“部分候选可能折回目标结构”；界面接触和亲和力预测可以支持“候选值得进入下一轮复核”；只有实验表达、纯化、结合或功能数据才能支持更强结论。

## 知识图谱入口

本章来源于 `01_课程章节索引/章节精读/第06章_RFD3多组分设计精读.md`，方法来源是 `02_方法笔记/RFdiffusion与蛋白设计.md`，文献入口包括 `03_文献笔记/RFdiffusion蛋白设计.md`、`03_文献笔记/ProteinMPNN序列设计.md` 和 `03_文献笔记/BindCraft与LigandMPNN.md`。实验入口包括 `04_实验记录/模板_RFdiffusion骨架生成记录.md`、`04_实验记录/模板_ProteinMPNN序列设计记录.md` 和 `04_实验记录/模板_BindCraft_LigandMPNN设计记录.md`。

在知识图谱中，本章连接方法实体、设计对象实体和验证实体。方法实体包括 RFdiffusion、RFD3、RFdiffusion2、ProteinMPNN、LigandMPNN、BindCraft、BoltzDesign 和回折叠模型；设计对象包括目标蛋白、binder、motif、hotspot、ligand、nucleic acid、enzyme active site、antibody 和 peptide；验证实体包括 pLDDT、pTM/ipTM、PAE、motif RMSD、interface contacts、clashes、unsatisfied polar atoms、hydrophobic exposure、aggregation risk、expression feasibility 和 experimental assay。

本章和第 8 章关系紧密。第 8 章中的 BabA binder 文献案例 `zhu_novo_2026` 是 protein design 在研究路线中的应用范文，但它不是 AI_MD 已完成实验。第六章负责建立设计流程，第八章负责把流程放入课题设计。

### Imagegen 知识图谱

![第 6 章知识图谱](../assets/imagegen/chapter-06-knowledge-map.png){ loading=lazy }

| 编号 | 正文权威标签 |
|:---:|:---|
| 1 | 设计目标 |
| 2 | 约束/热点 |
| 3 | 骨架生成 |
| 4 | 序列设计 |
| 5 | 回折叠 |
| 6 | 界面评分 |
| 7 | 实验交接 |

这张图由 Imagegen 生成，用于帮助读者把本章对象、方法和证据关系先组织成可记忆结构。图中只保留短标题和编号，精确术语、参数和边界以上表及正文为准。

## 核心概念

任务定义决定设计空间。Fold design 关注从零生成稳定折叠；motif scaffolding 关注把关键功能 motif 放入新骨架；binder design 关注目标界面互补；ligand binder design 关注小分子口袋和配体环境；enzyme scaffolding 关注催化几何、底物定位和活性位点；nucleic-acid binder 关注碱基、骨架、电荷和特异性。不同任务不能套用同一评价标准。

RFdiffusion/RFD3 属于生成骨架或复合物假设的层级。RFdiffusion 在 de novo 结构与功能设计中展示了扩散模型的能力；RFD3 则进一步强调全原子、多组分和复合物交互，适合讨论蛋白、小分子、核酸、抗体、酶和 binder 的统一设计框架。但生成模型输出仍然是候选，而不是最终蛋白。

ProteinMPNN 和 LigandMPNN 负责序列设计。骨架本身没有可表达序列，序列设计需要根据结构环境给出氨基酸选择。ProteinMPNN 面向 backbone-conditioned sequence design，LigandMPNN 进一步考虑 ligand 或 atomic context。它们解决的是“这个结构上放什么序列更可能折叠/结合”，不是“这个设计已经有效”。

回折叠验证是设计流程的中间质控。设计序列需要用 AlphaFold2、AlphaFold3、Boltz、ESMFold 或其他模型回折叠，看是否回到目标骨架、motif 是否保持、界面是否形成、PAE 是否合理。回折叠失败的候选应淘汰或回到设计参数，而不是通过挑选最好看的图继续解释。

界面和功能复核比整体折叠更严格。Binder 需要检查界面面积、形状互补、电荷、疏水核心、未满足极性、聚集风险和目标表位；enzyme design 需要检查催化原子几何、底物方向、过渡态假设和 QM/DFT 边界；nucleic-acid binder 需要检查碱基识别、电荷屏蔽、脱靶风险和细胞环境。整体 pLDDT 高不能替代功能位点复核。

## 方法流程

第一步是定义设计任务。用一句话写清“设计什么、绑定谁、实现什么功能、使用哪些约束、输出如何验证”。例如“针对目标蛋白 A 的表位 B 设计一个 80-120 aa binder，优先保留 hotspot 残基附近接触，并用回折叠和界面复核筛选候选”。任务定义越清楚，后续 contig、hotspot 和评价标准越容易建立。

第二步是准备输入和约束。记录目标结构来源、链 ID、保留或删除的配体/核酸/金属、水和修饰；记录 motif 残基、hotspot、目标界面、设计长度、contig、对称性、固定残基、排除区域和设计数量。若输入来自预测结构，必须记录置信度和不确定区域。

第三步是运行 RFdiffusion/RFD3 或相关生成模型。记录模型版本、checkpoint、配置、seed、num_designs、输出目录和失败信息。输出后先检查骨架是否满足长度、motif、界面和几何约束，明显失败候选应立即淘汰，不进入序列设计。

第四步是序列设计。用 ProteinMPNN、LigandMPNN 或其他序列设计工具，为合格骨架生成多个序列。记录 temperature、固定残基、omit AA、设计数量、FASTA 输出和打分。序列设计后要检查低复杂度、聚集倾向、异常电荷、表达风险和是否破坏功能 motif。

第五步是回折叠和结构复核。对设计序列做 AlphaFold/Boltz 回折叠或复合物预测，检查 pLDDT、pTM/ipTM、PAE、motif RMSD、interface contacts、clashes 和目标相对方向。只有能回到目标骨架且界面合理的候选，才适合进入更高成本评估。

第六步是亲和力、动态和实验可行性评估。候选可进入第 5 章的 Boltz2/亲和力预测、第 4 章的 MD/AI 采样、第 3 章的 docking 或界面重打分。最终还要考虑表达系统、蛋白长度、二硫键、修饰、纯化、稳定性、免疫原性和实验 assay。设计流程的终点不是文件夹里的 PDB，而是可验证的分子假设。

第七步是记录淘汰原因。蛋白设计通常会生成大量失败候选。失败候选的价值在于告诉你约束是否太强、界面是否错误、序列是否不稳定、回折叠是否失败或目标表位是否不适合。实验记录模板必须保留淘汰原因，避免只展示少数成功图。

## 代码案例与软件操作

![第 6 章流程解释图](../assets/imagegen/chapter-06-flow-protein-design-cycle.png){ loading=lazy }

**骨架生成到回折叠验证流程图** 的编号含义如下：

| 编号 | 流程节点 |
|:---:|:---|
| 1 | target |
| 2 | constraints |
| 3 | backbone |
| 4 | sequence |
| 5 | fold |
| 6 | score |
| 7 | handoff |

本节对应软件/界面：**RFdiffusion / ProteinMPNN dry-run config**。场景是：用配置模板记录 target、contig、hotspot、seed 和输出筛选规则，先做小批量 dry-run。

=== "可复制代码"

    ```yaml
    target_pdb: inputs/target.pdb
    contig: A1-120/0 B20-35
    hotspot_residues: [A45, A49, A52]
    num_designs: 10
    random_seed: 20260531
    filters:
      min_interface_confidence: 0.70
      max_backbone_rmsd_a: 2.0
      require_manual_interface_review: true
    ```

=== "配套文件"

    完整示例文件：[`chapter-06-design-config.yaml`](../assets/code/chapter-06-design-config.yaml)

![第 6 章软件操作截图](../assets/screenshots/chapter-06-protein-design-cycle.png){ loading=lazy }

| 步骤 | 操作 |
|:---:|:---|
| 1 | 定义靶点、motif、hotspot 和 contig。 |
| 2 | 生成少量 backbone，再用 ProteinMPNN 设计序列。 |
| 3 | 回折叠验证并筛掉低置信度/低多样性候选。 |

!!! warning "常见错误"
    生成结构不是可表达蛋白；必须经过回折叠、界面复核、多样性和实验可行性过滤。

## 关键文献与 BibTeX key

<!-- refs:start -->

!!! quote "`watson_novo_2023`"
    **Nature 风格引用：** Watson, J. L., Juergens, D., Bennett, N. R., Trippe, B. L., Yim, J., Eisenach, H. E. et al. De novo design of protein structure and function with RFdiffusion. Nature (2023). https://doi.org/10.1038/s41586-023-06415-8

    **DOI/URL：** `10.1038/s41586-023-06415-8`

    **BibTeX key：** `watson_novo_2023`

    **Zotero item key：** `UKX5E6IB`

    **本章用途：** 蛋白设计流程、约束条件和验证标准的文献锚点。

!!! quote "`ahern_atom_2025`"
    **Nature 风格引用：** Ahern, W., Yim, J., Tischer, D., Salike, S., Woodbury, S. M., Kim, D. et al. Atom level enzyme active site scaffolding using RFdiffusion2. bioRxiv (2025). https://doi.org/10.1101/2025.04.09.648075

    **DOI/URL：** `10.1101/2025.04.09.648075`

    **BibTeX key：** `ahern_atom_2025`

    **Zotero item key：** `ZYFCZKMH`

    **本章用途：** 蛋白设计流程、约束条件和验证标准的文献锚点。

!!! quote "`bennett_atomically_2025`"
    **Nature 风格引用：** Bennett, N. R., Watson, J. L., Ragotte, R. J., Borst, A. J., See, D. L., Weidle, C. et al. Atomically accurate de novo design of antibodies with RFdiffusion. Nature (2025). https://doi.org/10.1038/s41586-025-09721-5

    **DOI/URL：** `10.1038/s41586-025-09721-5`

    **BibTeX key：** `bennett_atomically_2025`

    **Zotero item key：** `EBQ7CNVI`

    **本章用途：** 蛋白设计流程、约束条件和验证标准的文献锚点。

!!! quote "`dauparas_robust_2022`"
    **Nature 风格引用：** Dauparas, J., Anishchenko, I., Bennett, N., Bai, H., Ragotte, R. J., Milles, L. F. et al. Robust deep learning–based protein sequence design using ProteinMPNN. Science (2022). https://doi.org/10.1126/science.add2187

    **DOI/URL：** `10.1126/science.add2187`

    **BibTeX key：** `dauparas_robust_2022`

    **Zotero item key：** `V2WLND5M`

    **本章用途：** 蛋白设计流程、约束条件和验证标准的文献锚点。

!!! quote "`pacesa_bindcraft_2024`"
    **Nature 风格引用：** Pacesa, M., Nickel, L., Schmidt, J., Pyatova, E., Schellhaas, C., Kissling, L. et al. BindCraft: one-shot design of functional protein binders. bioRxiv (2024). https://doi.org/10.1101/2024.09.30.615802

    **DOI/URL：** `10.1101/2024.09.30.615802`

    **BibTeX key：** `pacesa_bindcraft_2024`

    **Zotero item key：** `QCD2DXXI`

    **本章用途：** 蛋白设计流程、约束条件和验证标准的文献锚点。

!!! quote "`dauparas_atomic_2025`"
    **Nature 风格引用：** Dauparas, J., Lee, G. R., Pecoraro, R., An, L., Anishchenko, I., Glasscock, C. et al. Atomic context-conditioned protein sequence design using LigandMPNN. Nature Methods (2025). https://doi.org/10.1038/s41592-025-02626-1

    **DOI/URL：** `10.1038/s41592-025-02626-1`

    **BibTeX key：** `dauparas_atomic_2025`

    **Zotero item key：** `UN6R4C6J`

    **本章用途：** 蛋白设计流程、约束条件和验证标准的文献锚点。

!!! quote "`yang_w_past_2026`"
    **Nature 风格引用：** Yang, W., Wang, S., Lee, G. R., Zhang, J. Z., Courbet, A., Juergens, D. et al. The past, present and future of de novo protein design. Nature 652, 1139-1152 (2026). https://doi.org/10.1038/s41586-026-10328-7

    **DOI/URL：** `10.1038/s41586-026-10328-7`

    **BibTeX key：** `yang_w_past_2026`

    **Zotero item key：** `TPR3JY6N`

    **本章用途：** 蛋白设计流程、约束条件和验证标准的文献锚点。

<!-- refs:end -->
## 实验/练习入口

练习一：写一个 RFdiffusion/RFD3 设计任务卡。选择一个目标蛋白或教学案例，定义任务类型、目标结构、链 ID、hotspot、contig、设计长度、候选数量和验证标准。不要先跑工具，先确认任务定义是否清楚。

练习二：填写 ProteinMPNN 序列设计模板。给定一个骨架，写出固定残基、temperature、候选数量、FASTA 输出、打分字段和淘汰标准。重点是理解序列设计不是随机生成，而是条件化在骨架和约束上的选择。

练习三：设计一个回折叠复核表。表格至少包含候选 ID、pLDDT、pTM/ipTM、PAE、motif RMSD、interface contact、clash、unsatisfied polar、hydrophobic exposure、aggregation risk、保留/淘汰和理由。这个表可以直接服务真实项目。

练习四：把 protein design 结果写成保守 claim。示例：“候选 B 在模型层面满足骨架和界面约束，回折叠结果支持进入亲和力和表达可行性复核；当前不能声称其已结合目标或具有功能。”要求列出后续实验和计算。

## 使用边界与常见误读

第一，生成结构不是最终设计。RFdiffusion/RFD3 输出只是候选骨架或复合物假设，需要序列设计、回折叠、界面复核、亲和力评估和实验验证。

第二，pLDDT 高不等于 binder 成功。整体结构可信并不保证界面正确、表位合理、结合强、可表达或有功能。界面指标和实验 assay 必须单独评估。

第三，不能只展示成功候选。设计项目中失败候选同样重要，因为它们揭示约束、参数和目标选择的问题。研究工作台应记录失败原因。

第四，理论酶和核酸/小分子 binder 更需要功能边界。催化几何、底物方向、量子化学假设、脱靶、细胞递送和实验验证都不能被结构图替代。

第五，文献案例不能写成本项目结果。第六章新增 Nature 综述和第八章 BabA binder PDF 是课程与文献锚点，除非本项目真实运行并记录了对应实验，否则不能声称“本项目已设计出 binder”。

## 延伸阅读与下一步

完成本章后，读者应能把蛋白设计从工具演示转化为可审查流程。下一章进入 VibeCoding、Claude Code 与 AI Agent 工作流，主题从分子设计转向项目执行：如何让 AI Agent 读取知识库、调用 skills、维护文献锚点、生成实验记录并持续验证。建议在进入 [第 7 章](chapter-07.md) 前，先用本章模板写一个 protein design dry-run，不要求真实运行，但要把约束和验证标准写清楚。

本章也为第 8 章研究整合提供下游能力。真实研究问题往往不是单独做 docking 或单独做 protein design，而是把靶点发现、结构复核、虚拟筛选、亲和力评估、蛋白设计和实验队列组合起来。蛋白设计是强有力的“造器”方法，但只有进入证据链和实验验证，才可能成为研究结果。[返回首页](../index.md)。
