# 第 3 章 AI 多组分对接与虚拟筛选

## 本章导读

本章进入药物设计工作流中最常见、也最容易被误读的一层：分子对接与虚拟筛选。对接的输出通常是一组 pose 和 score，虚拟筛选的输出通常是一张排序表，但这些都不是“发现了药物”的证据。它们只是把大量候选压缩成较小集合，并为后续可视化、MD、亲和力计算、合成可行性和实验验证提供优先级。

“AI 多组分对接”在课程中有两个含义。第一，它指传统 docking 流程正在被 AI 模型、机器学习 scoring、结构预测、MSA、GPU 加速和自动化批处理重塑。第二，它指实际体系往往不再是简单的单蛋白-单小分子，而可能包含蛋白、肽、核酸、小分子、金属离子、辅因子、修饰残基、多个链或多个候选靶点。多组分越复杂，越需要明确每个输入对象的角色和边界。

本章的核心态度是审慎使用 docking。分子对接非常适合大规模初筛、口袋假设、构象生成和候选优先级排序，但它的评分函数通常不足以直接给出真实亲和力。2025 年关于 AI-powered docking 的 benchmark 也提醒我们：AI docking 方法在 pose prediction 和 virtual screening 中有潜力，但评价必须回到特定任务、数据集、decoy 设计和筛选目标，而不是简单比较一个分数。课程的目标不是让读者迷信某个工具，而是建立可复核的筛选漏斗。

## 学习目标

完成本章后，读者应能把一次虚拟筛选拆成受体准备、配体准备、口袋定义、对接运行、结果筛选、结构复核和后续验证七个部分；能解释构象搜索和评分函数的区别；能记录 docking box、受体处理、配体质子化、软件版本、随机种子、输出 pose 和筛选阈值；能说明为什么 docking score 不能被直接写成 Kd、IC50 或功能活性；能根据项目需求选择传统 docking、GPU 加速 docking、机器学习 docking、蛋白-肽 docking 或复合物预测辅助筛选。

读者还需要掌握多组分输入的风险。对于含金属离子、辅因子、修饰残基、关键水分子或核酸的体系，简单删除“杂原子”可能会破坏真实口袋；对于蛋白-肽或蛋白-蛋白界面，传统小分子 docking 的评分和采样假设可能不适用；对于 AI 结构预测产生的受体模型，低置信度 loop、口袋构象和模板偏差会影响筛选结果。每一次对接都应该回答：输入结构是否适合对接，搜索空间是否合理，候选库是否与研究问题匹配，输出是否经过人工复核。

## 知识图谱入口

本章来源于 `01_课程章节索引/章节精读/第03章_AI多组分对接与虚拟筛选精读.md`。方法来源包括 `02_方法笔记/AI多组分对接与虚拟筛选.md` 和 `02_方法笔记/MSA与Uni-Dock补充.md`。文献入口是 `03_文献笔记/分子对接与虚拟筛选.md`，实验入口是 `04_实验记录/模板_对接虚拟筛选记录.md`，证据边界入口是 `07_研究工作台/证据与claims矩阵.md`。

本章在知识图谱中连接三类实体：方法实体、研究对象实体和证据实体。方法实体包括 docking、virtual screening、MSA、Uni-Dock、Dockey、AI-powered docking、protein-peptide docking 和 machine-learning docking。研究对象实体包括受体、配体、口袋、肽、蛋白界面、分子库和筛选面板。证据实体包括 docking score、pose、interaction pattern、hit list、decoy benchmark、MD 复核和实验验证。一个合格的图谱节点不应只写“做了 docking”，而要能追溯到“用什么受体、什么配体库、什么 box、什么 score、哪些候选、为什么保留或淘汰”。

本章也为第 8 章的正向虚拟筛选案例铺垫。第 8 章中的 UXS1、APE1、IDO1 和其他文献案例可以作为范文学习，但不能写成本项目结果。本章负责建立通用漏斗，第 8 章负责把漏斗放入研究问题和项目池。

### Imagegen 知识图谱

![第 3 章知识图谱](../assets/imagegen/chapter-03-knowledge-map.png){ loading=lazy }

| 编号 | 正文权威标签 |
|:---:|:---|
| 1 | 受体准备 |
| 2 | 配体库 |
| 3 | box 定义 |
| 4 | 打分 |
| 5 | 重评分 |
| 6 | 筛选规则 |
| 7 | 实验候选 |

这张图由 Imagegen 生成，用于帮助读者把本章对象、方法和证据关系先组织成可记忆结构。图中只保留短标题和编号，精确术语、参数和边界以上表及正文为准。

## 核心概念

对接的三要素是受体、配体和搜索空间。受体决定口袋环境，配体决定化学空间，搜索空间决定算法探索范围。受体准备包括结构来源、链选择、缺失残基、质子化、金属离子、辅因子、水分子和电荷处理；配体准备包括结构格式、质子化、互变异构、手性、构象和能量最小化；搜索空间来自共晶配体、保守位点、突变位点、口袋预测或盲对接。三者任何一个不合理，最终 score 都缺少解释价值。

构象搜索和评分函数是不同问题。构象搜索试图找到可能的结合姿态，评分函数试图对姿态或候选排序。一个方法可能 pose prediction 很强，但 virtual screening enrichment 不一定强；也可能能区分已知 active 和 decoy，却在新靶点、新化学空间或蛋白-肽体系中失效。因此结果解释应分开写：pose 是否合理，score 是否有排序价值，候选是否值得进入下一轮。

虚拟筛选是漏斗，不是终点。通常先用快速过滤处理分子库，例如去重、理化性质、PAINS、反应性基团、药物相似性或合成可行性；再用对接或机器学习模型进行初筛；再对 top hits 做 pose 复核、重打分、MD、MM-GBSA/FEP、Boltz2 或实验验证。课程中反复强调“不要只看 docking score”，是因为 score 是漏斗中的一个信号，而不是最终证据。

多组分体系要求角色定义。蛋白、小分子、肽、核酸、金属、辅因子、糖基化或修饰残基在结构中有不同物理意义。比如金属配位可能决定活性位点几何，关键水分子可能参与桥接氢键，辅因子可能改变口袋形状，肽段可能有较大柔性。把这些组分无差别删除，会让对接变成错误假设。

MSA 与 AI 结构预测的关系也需要进入对接思维。对于某些复合物或蛋白结构预测任务，MSA 深度、数据库、E-value 和 pairing 策略会影响模型结构。第 3 章的 MSA 与 Uni-Dock 补充材料提醒我们：结构预测和 docking 正在连接，但这种连接不是自动可靠的。若受体结构来自预测模型，必须在对接前检查关键口袋的局部置信度和构象合理性。

## 方法流程

第一步是定义筛选问题。你要筛选的是小分子抑制剂、激动剂、蛋白-肽结合、PPI 界面调节剂，还是反向虚拟筛选中的潜在靶点？候选库是商业库、天然产物库、已上市药物库、内部化合物、肽库还是突变体面板？目标是找到可采购 hit、解释机制、优先级排序，还是生成课题假设？问题定义不同，后续受体、配体、box、score 和验证标准都不同。

第二步是受体准备。先选择结构来源：实验结构优先检查分辨率、配体、缺失残基和生物学装配；预测结构优先检查 pLDDT/PAE、口袋 loop 和模板偏差；复合物模型优先检查链相对方向和界面置信度。然后决定保留哪些水、离子、金属、辅因子和修饰。接着处理质子化、电荷、氢原子、缺失原子和格式转换。所有处理步骤都必须写入实验记录。

第三步是配体准备。对小分子库，先统一 ID、SMILES/SDF、盐形式、质子化、互变异构、手性和 3D 构象；对肽或蛋白片段，明确序列、构象来源、端基处理和柔性；对大规模筛选，生成 manifest 表记录每个分子的来源、处理状态和失败原因。不要让“格式转换成功”掩盖化学状态错误。

第四步是定义搜索空间。共晶配体口袋、已知活性位点、保守 motif、突变热点、AlphaFold/Chimera 口袋预测或盲对接，都可以作为来源。但 box 应该记录中心、尺寸、坐标系、来源和理由。box 太小会错过合理姿态，box 太大会增加噪声。对于多口袋或全蛋白筛选，可以分区运行并分别解释结果。

第五步是运行 docking 或 virtual screening。记录软件、版本、参数、exhaustiveness、num modes、seed、CPU/GPU、分子库数量、失败数量和输出路径。若使用 Dockey、Uni-Dock 或其他批量工具，需要保留配置、输入列表和输出汇总。若使用 AI-powered docking，记录模型版本、输入格式、是否使用模板、是否进行重打分和 benchmark 背景。

第六步是结果复核。先检查 top hits 是否有明显空间冲突、扭曲构象、错误电荷、穿越蛋白或脱离口袋；再检查相互作用是否与已知活性位点、保守残基或机制假设一致；再做聚类、去重和理化性质过滤；最后决定哪些候选进入 MD、亲和力计算或实验。复核结果应写成表格，包含保留理由和淘汰理由。

第七步是把结果放入证据层。对接输出可以支持“候选 A 在模型口袋中形成合理 pose”或“候选库中若干分子值得复核”，但不能单独支持“候选 A 是强效抑制剂”。如果要形成 claim，需要补文献、MD、自由能、实验或其他证据。`07_研究工作台/证据与claims矩阵.md` 是本项目记录这类边界的入口。

## 代码案例与软件操作

![第 3 章流程解释图](../assets/imagegen/chapter-03-flow-docking-funnel.png){ loading=lazy }

**受体-配体-box-score-filter 漏斗图** 的编号含义如下：

| 编号 | 流程节点 |
|:---:|:---|
| 1 | receptor |
| 2 | ligands |
| 3 | box |
| 4 | score |
| 5 | rescore |
| 6 | filter |
| 7 | shortlist |

本节对应软件/界面：**Uni-Dock / Vina-style dry-run**。场景是：用最小受体和 3 个配体验证 box、输入格式、输出表和筛选阈值，而不是直接跑全库。

=== "可复制代码"

    ```bash
    set -euo pipefail
    mkdir -p outputs logs
    cat > inputs/box.tsv <<'BOX'
    cx	cy	cz	sx	sy	sz
    12.4	-3.2	8.6	22	22	22
    BOX
    unidock --receptor inputs/receptor.pdbqt --ligand_index inputs/ligands.txt \
      --center_x 12.4 --center_y -3.2 --center_z 8.6 \
      --size_x 22 --size_y 22 --size_z 22 \
      --dir outputs > logs/unidock-dry-run.log 2>&1
    ```

=== "配套文件"

    完整示例文件：[`chapter-03-docking-dry-run.sh`](../assets/code/chapter-03-docking-dry-run.sh)

![第 3 章软件操作截图](../assets/screenshots/chapter-03-docking-funnel.png){ loading=lazy }

| 步骤 | 操作 |
|:---:|:---|
| 1 | 准备受体、配体和 box 参数表。 |
| 2 | 先跑 1 receptor x 3 ligands 的 dry-run。 |
| 3 | 把 score、pose 文件和过滤理由写入 manifest。 |

!!! warning "常见错误"
    docking score 只能做排序线索，不能写成结合自由能或实验 IC50。

## 关键文献与 BibTeX key

<!-- refs:start -->

!!! quote "`du_dockey_2023`"
    **Nature 风格引用：** Du, L., Geng, C., Zeng, Q., Huang, T., Tang, J., Chu, Y. et al. Dockey: a modern integrated tool for large-scale molecular docking and virtual screening. Briefings in Bioinformatics 24, bbad047 (2023). https://doi.org/10.1093/bib/bbad047

    **DOI/URL：** `10.1093/bib/bbad047`

    **BibTeX key：** `du_dockey_2023`

    **Zotero item key：** `UOUH33GQ`

    **本章用途：** 对接/虚拟筛选流程、评分解释和文献案例边界。

!!! quote "`agrawal_benchmarking_2019`"
    **Nature 风格引用：** Agrawal, P., Singh, H., Srivastava, H. K., Singh, S., Kishore, G. & Raghava, G. P. S. Benchmarking of different molecular docking methods for protein-peptide docking. BMC Bioinformatics 19, 426 (2019). https://doi.org/10.1186/s12859-018-2449-y

    **DOI/URL：** `10.1186/s12859-018-2449-y`

    **BibTeX key：** `agrawal_benchmarking_2019`

    **Zotero item key：** `T2O1ECSF`

    **本章用途：** 对接/虚拟筛选流程、评分解释和文献案例边界。

!!! quote "`crampon_machine-learning_2022`"
    **Nature 风格引用：** Crampon, K., Giorkallos, A., Deldossi, M., Baud, S. & Steffenel, L. A. Machine-learning methods for ligand–protein molecular docking. Drug Discovery Today 27, 151–164 (2022). https://doi.org/10.1016/j.drudis.2021.09.007

    **DOI/URL：** `10.1016/j.drudis.2021.09.007`

    **BibTeX key：** `crampon_machine-learning_2022`

    **Zotero item key：** `R2W3SF5S`

    **本章用途：** 对接/虚拟筛选流程、评分解释和文献案例边界。

!!! quote "`gu_benchmarking_2025`"
    **Nature 风格引用：** Gu, S., Shen, C., Zhang, X., Sun, H., Cai, H., Luo, H. et al. Benchmarking AI-powered docking methods from the perspective of virtual screening. Nature Machine Intelligence 7, 509–520 (2025). https://doi.org/10.1038/s42256-025-00993-0

    **DOI/URL：** `10.1038/s42256-025-00993-0`

    **BibTeX key：** `gu_benchmarking_2025`

    **Zotero item key：** `57K986LK`

    **本章用途：** 对接/虚拟筛选流程、评分解释和文献案例边界。

<!-- refs:end -->
## 实验/练习入口

练习一：完成一次 docking dry-run。选择一个受体和一个小分子，写清结构来源、配体来源、box 来源、软件版本、参数和输出路径。运行可以是真实小任务，也可以是计划型 dry-run；关键是记录字段完整。最后用 PyMOL 或 Chimera 复核 top pose，并写出保留或淘汰理由。

练习二：建立一个小型虚拟筛选 manifest。准备 10-20 个候选分子，记录 ID、SMILES/SDF、来源、处理状态、失败原因、docking score、pose 文件、人工复核状态和下一步。练习目标是理解批量任务的表格治理，而不是追求分数。

练习三：比较两个口袋定义。用同一受体和同一配体库，分别以共晶配体口袋和盲对接/预测口袋定义 box，比较 top hits、pose 合理性和复核结果。写出 box 改变如何影响筛选结果。

练习四：把一个 docking 结果转成 claim。用 `候选 X 在受体 Y 的 Z 口袋中得到合理 pose` 这种保守表述，列出支持证据、反证风险、需要补充的 MD/自由能/实验和不能声称的结论。这个练习直接服务第 8 章的项目池。

## 使用边界与常见误读

第一，docking score 不是 Kd、IC50 或活性。不同软件的 score 量纲、函数和标定不同，不能跨工具、跨靶点、跨分子系列随意比较。即使同一工具内部，也要结合 pose、化学合理性和实验背景解释。

第二，top pose 不是唯一真实构象。对接算法只在设定搜索空间和评分函数下给出候选姿态，真实体系还受到蛋白柔性、水、离子、质子化、诱导适配和构象选择影响。后续 MD 和自由能计算是补充，不是可选装饰。

第三，AI docking 不是自动更准确。AI 模型可能在公开 benchmark 上表现好，但在新靶点、新化学空间、金属配位、共价配体、膜蛋白、PPI 或低质量结构上仍可能失效。使用 AI-powered docking 时应记录模型版本和适用边界。

第四，文献案例不能直接迁移为本项目结果。第 8 章补充 PDF 中的 APE1、IDO1、UXS1 等虚拟筛选案例，可以作为流程学习材料，但不能把其 hit、靶点或机制写成本项目已经完成的结果。在线书籍必须清楚标注“文献案例”“课程范文”“方法假设”和“本项目运行结果”。

## 延伸阅读与下一步

完成本章后，读者应能完成一个可复核的 docking dry-run，并知道 score 的证据边界。下一章进入 AI 采样、分子模拟与 MD 结果解释，重点是检查候选 pose 或结构模型在动态体系中是否稳定，以及如何从轨迹中提取代表构象和结构证据。建议在进入 [第 4 章](chapter-04.md) 前，先从本章练习中选出一个 top pose，准备把它作为 MD 或亲和力计算的输入。

本章还会在第 5 章和第 8 章继续使用。第 5 章会讨论如何把对接候选进一步转化为亲和力或自由能判断；第 8 章会把对接放入寻靶、正向虚拟筛选、PPI 筛选和蛋白设计整合路线中。对接不是终点，而是研究漏斗中成本较低、召回较强、但必须严格复核的一层。[返回首页](../index.md)。
