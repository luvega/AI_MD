# 第 8 章 研究思路解析：寻靶、虚拟筛选、PPI 与蛋白设计整合

## 本章导读

第八章是全书的整合章。前七章分别训练了环境、结构、对接、MD、亲和力、蛋白设计和 Agent 工作流；本章要回答的是：如何把这些能力组织成一个面向真实研究问题的路线。一个好的 AIDD 项目不是简单把工具串起来，而是从疾病、生物机制、靶点、结构、候选分子、互作网络、实验条件和产出目标中选择最小可执行路径。

本章尤其强调“文献案例、课程范文、方法假设和本项目结果”四层分离。第八章补充资料中包含 UXS1/metformin、APE1、IDO1 scaffold-aware ML + docking + MD、BabA de novo binder 设计等文献案例，也包含 Chai-1 批量互作蛋白筛选脚本。这些材料非常适合学习研究设计，但不能被写成 AI_MD 已经完成的实验结果。在线书籍必须明确：文献案例提供方法参照，本地脚本提供可执行模板，真实项目结果必须来自 `04_实验记录/` 和用户确认。

从个人专业研究人员的角度，本章的目标是把课程资料转成研究工作台。研究工作台不只是资料汇总，而应包含研究问题、候选靶点、可用方法、已有证据、缺口、下一步实验和可产出物。AI Agent 可以辅助检索、整理和生成模板，但最终问题选择、实验条件和结论边界仍由研究者负责。

## 学习目标

完成本章后，读者应能把一个研究方向拆成“寻靶、解码、造器”三层：寻靶负责从疾病机制、多组学、文献和筛选中确定关键对象；解码负责用结构、对接、MD、亲和力和互作预测解释机制；造器负责设计小分子、多肽、蛋白 binder、诊断工具或工程化系统。读者应能为一个项目写出研究问题、候选靶点、输入数据、方法组合、证据边界、下一步实验和预期产出。

读者还应能分析第八章的四类案例。UXS1/metformin 案例体现机制驱动靶点和正向虚拟筛选；APE1 案例体现结构口袋、百万级库筛选、pose 复核和 MD/MM-GBSA；IDO1 案例体现 scaffold-aware machine learning、applicability domain、ensemble docking 和可复现框架；BabA binder 案例体现 RFdiffusion3、ProteinMPNN、回折叠、对接/MD 与实验验证的整合。读者需要从这些案例中抽取方法结构，而不是复制结论。

## 知识图谱入口

本章来源于 `01_课程章节索引/章节精读/第08章_计算思路解析精读.md`。方法来源包括 `02_方法笔记/Chai1互作蛋白虚拟筛选.md`、`02_方法笔记/AI多组分对接与虚拟筛选.md` 和 `02_方法笔记/RFdiffusion与蛋白设计.md`。文献入口包括 `03_文献笔记/分子对接与虚拟筛选.md` 和 `03_文献笔记/RFdiffusion蛋白设计.md`。工作台入口包括 `07_研究工作台/实体索引.md`、`07_研究工作台/证据与claims矩阵.md` 和 `07_研究工作台/研究问题与项目池.md`。

本章在知识图谱中是最高层的“项目编排”节点。它把靶点、分子、蛋白、方法、文献、实验模板、claims 和输出任务连接起来。一个成熟的研究图谱不应只回答“第几章讲了什么”，还应回答“某个靶点关联哪些资料”“哪些方法能用于 PPI 筛选”“哪些文献支持正向虚拟筛选流程”“哪些 claim 证据强度不足”“下一步最小实验是什么”。

本章正式 BibTeX key 包括 `sui_targeting_2026`、`shen_structure-based_2026`、`tomarchio_reproducible_2026`、`zhu_novo_2026` 和 `yang_w_past_2026`。它们分别支撑 UXS1、APE1、IDO1、BabA binder 和 de novo protein design 综述案例。Chai-1 当前以技术报告和本地脚本作为方法背景，正式 Zotero/BibTeX 锚点后续可继续补齐。

### Imagegen 知识图谱

![第 8 章知识图谱](../assets/imagegen/chapter-08-knowledge-map.png){ loading=lazy }

| 编号 | 正文权威标签 |
|:---:|:---|
| 1 | 研究问题 |
| 2 | 靶点证据 |
| 3 | 结构来源 |
| 4 | 虚拟筛选 |
| 5 | PPI 路线 |
| 6 | 蛋白设计 |
| 7 | 证据 claim |
| 8 | 输出任务 |

这张图由 Imagegen 生成，用于帮助读者把本章对象、方法和证据关系先组织成可记忆结构。图中只保留短标题和编号，精确术语、参数和边界以上表及正文为准。

## 核心概念

寻靶是研究路线的起点。靶点可以来自疾病机制、基因表达、突变、依赖性筛选、代谢通路、蛋白互作、表型筛选、文献假设或反向虚拟筛选。一个靶点进入计算流程前，应写清为什么选择它：是否有疾病相关性，是否有结构信息，是否有配体或抗体先例，是否可实验验证，是否有用户自己的专业兴趣和资源。

解码是把靶点转化为机制解释。结构可视化回答目标长什么样；docking 回答候选如何可能结合；MD 和 AI 采样回答构象是否稳定或是否存在多状态；亲和力预测回答候选排序是否值得复核；PPI 预测回答互作假设是否可形成界面；claims 矩阵回答证据强度是否足够。解码层的任务不是生成漂亮图，而是把机制链条写清楚。

造器是从理解走向设计。小分子筛选、多肽设计、protein binder、enzyme scaffold、diagnostic binder、合成生物学元件或材料蛋白，都属于“造器”层。第六章的 RFdiffusion/RFD3 和 ProteinMPNN 是造器方法，第五章的 Boltz2/亲和力是造器后的评价方法，第四章的 MD 是动态复核方法。造器结果必须进入实验可行性评估，不能停在模型图。

证据分层是本章的核心规范。课程范文是教学材料，文献案例是外部研究结果，方法假设是可执行计划，本项目结果是本地实际运行和记录。四者都可以出现在同一章，但不能混写。比如 APE1 PDF 可以教我们如何组织结构虚拟筛选流程，但不能让 AI_MD 直接声称“本项目筛选到了 APE1 抑制剂”。

项目池是个人研究工作台的组织方式。每个项目应包含问题、候选靶点、数据输入、方法组合、已有证据、关键缺口、下一步实验、风险、输出形式和优先级。AI Agent 可以帮助填充路径和引用，但研究者需要判断可行性和价值。第八章的真正产出不是一篇综述，而是一组能启动的研究任务。

## 方法流程

第一步是定义研究问题。问题应足够具体，例如“某肿瘤代谢依赖是否可通过某酶靶点调节”“某天然产物可能作用于哪些蛋白”“某 PPI 是否能用蛋白设计干预”“某结构口袋是否适合正向虚拟筛选”。模糊问题会导致方法堆叠，具体问题才能导向最小路径。

第二步是建立实体表。列出靶点、蛋白、配体、小分子库、通路、疾病、文献、软件、实验模板和输出目标。实体表应链接到 `07_研究工作台/实体索引.md`，并标记实体类型：`target`、`molecule`、`method`、`model/software`、`paper`、`experiment-template` 或 `chapter`。实体化后，AI 才能回答“UXS1 关联哪些资料”这类查询。

第三步是选择方法组合。正向虚拟筛选通常需要靶点结构、口袋定义、分子库、docking、pose 复核、MD/自由能和实验验证；反向虚拟筛选需要从小分子出发寻找潜在靶点，并用文献、生信和结构证据过滤；PPI 筛选可用 Chai-1、AlphaFold3、Boltz 或其他复合物预测辅助排序；protein design 可用 RFdiffusion/RFD3、ProteinMPNN、回折叠和界面复核。

第四步是建立证据链。每个关键判断都应写成 claim：支持文献、来源页、适用边界、证据强度和待确认项。例如“Chai-1 aggregate score 可作为互作候选排序信号”可以成立，但边界是“不能当真实 Kd 或功能活性”。再如“APE1 文献案例提供正向虚拟筛选流程参照”可以成立，但边界是“不是本项目筛选结果”。

第五步是选择最小可执行实验。一个项目不应从最大规模任务开始。可以先做结构来源核对、一个 docking dry-run、一个 Boltz2 输入样例、一个 Chai-1 小面板、一个 RFdiffusion 约束设计 dry-run 或一个文献复核表。最小任务成功后再扩大规模。这样能降低资源消耗和解释风险。

第六步是定义输出。不同项目可能输出课件案例、综述段落、课题申请、实验记录、候选清单、图谱节点、计算 notebook 或真实实验计划。输出不同，证据要求不同。课件可以讲方法，课题申请需要可行性，论文需要严谨结果，实验计划需要材料和步骤。

## 代码案例与软件操作

![第 8 章流程解释图](../assets/imagegen/chapter-08-flow-project-roadmap.png){ loading=lazy }

**寻靶-解码-造器项目路线图** 的编号含义如下：

| 编号 | 流程节点 |
|:---:|:---|
| 1 | question |
| 2 | evidence |
| 3 | target |
| 4 | structure |
| 5 | screen/design |
| 6 | validate |
| 7 | queue |
| 8 | output |

本节对应软件/界面：**research project pool / Chai-1 panel dry-run**。场景是：把候选项目拆成证据、方法、缺口、下一步实验和可产出物，防止把文献案例误写成本项目结果。

=== "可复制代码"

    ```python
    import pandas as pd

    projects = pd.read_csv('inputs/project_pool.tsv', sep='\t')
    projects['priority_score'] = (
        projects['evidence_strength'] * 0.45 +
        projects['method_readiness'] * 0.35 +
        projects['experiment_feasibility'] * 0.20
    )
    projects.sort_values('priority_score', ascending=False).to_csv('outputs/project_priority.tsv', sep='\t', index=False)
    ```

=== "配套文件"

    完整示例文件：[`chapter-08-project-priority.py`](../assets/code/chapter-08-project-priority.py)

![第 8 章软件操作截图](../assets/screenshots/chapter-08-project-pool.png){ loading=lazy }

| 步骤 | 操作 |
|:---:|:---|
| 1 | 为每个研究问题建立证据矩阵。 |
| 2 | 选择虚拟筛选、PPI 或蛋白设计路线。 |
| 3 | 按证据强度和实验可行性给下一步排序。 |

!!! warning "常见错误"
    第八章补充 PDF 只能作为文献案例和方法借鉴；没有本地运行记录时不能写成本项目结果。

## 关键文献与 BibTeX key

<!-- refs:start -->

!!! quote "`sui_targeting_2026`"
    **Nature 风格引用：** Sui, Q., Chen, Z., Shan, G., Hu, Z., Jin, X., Liang, J. et al. Targeting UXS1-Dependent Glucuronate Detoxification Potentiates Metformin's Anti-Tumor Efficacy in Lung Adenocarcinoma. Advanced Science, e10542 (2026). https://doi.org/10.1002/advs.202510542

    **DOI/URL：** `10.1002/advs.202510542`

    **BibTeX key：** `sui_targeting_2026`

    **Zotero item key：** `QXKW6K78`

    **本章用途：** 第八章研究路线中的文献案例与方法借鉴。

!!! quote "`shen_structure-based_2026`"
    **Nature 风格引用：** Shen, T., Shen, H., Kong, Y., Qiang, W., Yu, X. & Wang, J. Structure-based virtual screening identifies novel small-molecule inhibitors targeting the endonuclease active site of APE1. Scientific Reports (2026). https://doi.org/10.1038/s41598-026-51975-0

    **DOI/URL：** `10.1038/s41598-026-51975-0`

    **BibTeX key：** `shen_structure-based_2026`

    **Zotero item key：** `YUMKNHSK`

    **本章用途：** 对接/虚拟筛选流程、评分解释和文献案例边界。

!!! quote "`tomarchio_reproducible_2026`"
    **Nature 风格引用：** Tomarchio, E. G., Buccheri, R. & Rescifina, A. A Reproducible Hierarchical Virtual Screening Framework Integrating Scaffold-Aware Machine Learning, Ensemble Docking, and Molecular Dynamics: Application to IDO1. Journal of Chemical Information and Modeling (2026). https://doi.org/10.1021/acs.jcim.6c00967

    **DOI/URL：** `10.1021/acs.jcim.6c00967`

    **BibTeX key：** `tomarchio_reproducible_2026`

    **Zotero item key：** `Y4ARSYCQ`

    **本章用途：** 对接/虚拟筛选流程、评分解释和文献案例边界。

!!! quote "`zhu_novo_2026`"
    **Nature 风格引用：** Zhu, Y., Isaha, M. B. & Zhang, X. De novo design of binder proteins targeting Helicobacter pylori adhesin BabA. bioRxiv (2026). https://doi.org/10.64898/2026.05.24.727452

    **DOI/URL：** `10.64898/2026.05.24.727452`

    **BibTeX key：** `zhu_novo_2026`

    **Zotero item key：** `V6Y5EEZL`

    **本章用途：** 第八章研究路线中的文献案例与方法借鉴。

!!! quote "`yang_w_past_2026`"
    **Nature 风格引用：** Yang, W., Wang, S., Lee, G. R., Zhang, J. Z., Courbet, A., Juergens, D. et al. The past, present and future of de novo protein design. Nature 652, 1139-1152 (2026). https://doi.org/10.1038/s41586-026-10328-7

    **DOI/URL：** `10.1038/s41586-026-10328-7`

    **BibTeX key：** `yang_w_past_2026`

    **Zotero item key：** `TPR3JY6N`

    **本章用途：** 蛋白设计流程、约束条件和验证标准的文献锚点。

<!-- refs:end -->
## 实验/练习入口

练习一：从项目池选择一个问题。打开 [附录 A](../appendices/research-workbench.md)，选择一个研究问题，填写问题、候选靶点、可用结构、候选分子或蛋白面板、可用方法、已有文献和下一步最小任务。

练习二：拆解一个文献案例。任选 UXS1、APE1、IDO1 或 BabA 案例，把它拆成研究问题、输入、方法、输出、验证和边界六列。特别标出哪些内容可借鉴，哪些不能迁移到本项目。

练习三：设计一个 Chai-1 PPI dry-run。选择一个 query protein 和 3-5 个 target proteins，写清 FASTA 来源、批量建模脚本、aggregate score、界面复核、PAE/置信度、保留/淘汰标准和后续验证。注意：aggregate score 只能排序，不能当真实亲和力。

练习四：生成一个 protein design 项目卡。以 BabA 案例为参考，但换成用户自己的目标或教学目标，写出设计任务、目标结构、hotspot、RFdiffusion/RFD3 输入、ProteinMPNN 输出、回折叠复核、亲和力/MD 复核和实验可行性。标注哪些是计划，哪些是真实结果。

练习五：为一个项目写 claim 矩阵。至少包含三个 claim：一个靶点证据 claim，一个结构/对接 claim，一个下一步实验 claim。每条 claim 都要有支持来源、证据强度、边界和待确认项。

## 使用边界与常见误读

第一，第八章补充 PDF 是文献案例和课程范文，不是 AI_MD 已完成实验。任何从这些 PDF 中提取的 hit、靶点、分子或结论，都必须标记为外部文献结果。

第二，研究路线不是工具堆叠。把 AlphaFold、docking、MD、Boltz2、Chai-1 和 RFdiffusion 全部列上，不等于项目更强。真正的路线应从问题出发，选择最小必要方法，并为每一步设定退出标准。

第三，Chai-1 aggregate score 不能当 Kd 或功能活性。它可以辅助候选排序，但需要界面接触、置信度、结构可解释性、文献支持和实验验证。

第四，AI 生成的研究建议需要用户专业判断。用户的药物化学、多肽、蛋白设计和虚拟筛选背景决定哪些问题值得做、哪些材料可获得、哪些实验能落地。AI 可以补索引和草案，不能替代研究决策。

第五，输出导向不能牺牲 provenance。课件、综述、课题申请和实验记录都可以从本章生成，但必须保留路径、BibTeX key、文献边界和本项目结果状态。

## 延伸阅读与下一步

完成本章后，读者应能把整套 AI_MD 知识库转化为研究工作台，而不是只把它当课程笔记。下一步建议从三件事中选择一件：第一，完善 [附录 A](../appendices/research-workbench.md) 中的一个项目；第二，从 [附录 B](../appendices/experiment-templates.md) 选择一个最小 dry-run；第三，用 [附录 D](../appendices/ai-eval.md) 的问题测试 AI 是否能正确返回路径、BibTeX key、边界和下一步建议。

本章也是在线书籍第二版的出口。第 1-7 章提供方法，第 8 章提供研究组织方式。后续 P16/P17/P18/P19 类更新可以围绕 claim 层、项目池、AI 回归评测和输出视图继续扩展。对于个人研究者来说，最重要的不是把所有资料读完，而是能在 3 分钟内找到某个研究问题对应的资料、方法、文献和下一步实验模板。[返回首页](../index.md)。
