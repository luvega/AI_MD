# 第 2 章 结构来源、PyMOL 与 Chimera 可视化

## 本章导读

结构图容易给读者强烈直观印象，但图像质量并不等于结构证据质量。因此，本章首先界定这一问题场景，再说明需要记录哪些输入、动作、输出和质量控制信息。

本章训练读者区分实验结构、预测结构和可视化结果，并把链、配体、口袋、缺失区域和置信度写清楚。这里的重点不是追求单个软件操作的完整覆盖，而是让读者形成可复查的判断链：对象是什么、依据来自哪里、结果能支持什么、仍然不能说明什么。

第 3 章的 docking box、第 4 章的 MD 初始结构、第 5 章的多组分预测和第 6 章的设计约束都依赖本章的结构复核。因此，本章的正文采用“概念定义 -> 流程执行 -> 边界判断 -> 下一步交接”的组织方式。

## 学习目标

完成本章后，读者应能够：

- 能区分 PDB/mmCIF 实验结构、AlphaFold 预测结构和经人工处理的工作结构。
- 能在 PyMOL/ChimeraX 中检查链 ID、配体、活性位点、缺失残基和水/金属离子。
- 能说明结构叠合、局部口袋视图和截图在证据链中的边界。
- 能把一张结构图写成可追溯的图注和实验记录字段。

这些目标既面向课堂学习，也面向后续研究记录；如果不能在记录中复述这些要点，相关结果不宜进入项目结论。

## 知识图谱入口

本章的图谱入口连接结构来源、可视化工具和证据审查。图像展示的是分析对象，正文表格才是结构来源和判断标准。

在线书籍页面只引用整理后的 wiki、方法卡、文献笔记和资源页，不直接嵌入原始 PDF 或课件图表。需要追溯来源时，应回到 `book/book_map.toml`、章节精读笔记和相关 Zotero/BibTeX 记录。

| 来源类型 | 路径 |
|:---|:---|
| 章节来源 | `01_课程章节索引/章节精读/第02章_PyMOL与Chimera可视化精读.md` |
| 方法来源 | `02_方法笔记/PyMOL与Chimera可视化.md` |
| 文献来源 | `03_文献笔记/AlphaFold结构预测.md` |

### Imagegen 知识图谱

![第 2 章知识图谱](../assets/imagegen/chapter-02-knowledge-map.png){ loading=lazy }

| 编号 | 正文权威标签 |
|:---:|:---|
| 1 | PDB/mmCIF 来源 |
| 2 | AlphaFold 预测结构 |
| 3 | 链与配体 |
| 4 | 活性位点 |
| 5 | 结构叠合 |
| 6 | 证据边界 |

这张图由 Imagegen 生成，用于帮助读者把本章对象、方法和证据关系先组织成可记忆结构。图中只保留短标题和编号，精确术语、参数和边界以上表及正文为准。

## 核心概念

本节只保留支撑后续判断的核心概念。每个概念都应能回答一个具体问题：它约束什么输入、影响什么输出、需要怎样记录。

| 概念 | 教材化定义 |
|:---|:---|
| 结构来源 | 结构来源决定证据等级；实验结构、预测结构和处理后结构必须分开记录。 |
| 链与配体 | 链 ID、配体名、辅因子和金属离子是后续口袋定义和对接准备的关键字段。 |
| 活性位点 | 活性位点应由共晶配体、功能残基、文献或预测口袋共同约束，而不是只凭视觉中心选择。 |
| 结构叠合 | 结构叠合用于比较构象和模型差异，不能自动证明功能等价。 |
| 截图记录 | 截图应记录视角、对象、颜色、选择命令和来源，避免成为不可复现的装饰图。 |

阅读本节时，应优先检查这些概念能否落到文件、参数、图像、表格或记录字段上。不能落地的说法，在后续研究写作中应作为背景描述，而不是证据。

## 方法流程

本章流程按“输入 -> 动作 -> 输出 -> QC”的顺序组织。这样做的目的，是让每一步都能被复查，而不是只留下一个最终截图或分数。

| 步骤 | 输入 | 动作 | 输出 | QC/边界 |
|:---:|:---|:---|:---|:---|
| 1 | 结构文件 | 确认来源、分辨率/置信度和下载日期。 | 结构来源记录。 | PDB ID 或模型来源可追溯。 |
| 2 | 链和配体 | 检查链 ID、配体、缺失区域和非标准残基。 | 结构 QC 表。 | 关键对象已命名。 |
| 3 | 局部口袋 | 围绕配体或功能残基建立局部视图。 | 口袋截图。 | 选择半径和残基列表明确。 |
| 4 | 叠合比较 | 比较实验结构、预测结构或同源结构。 | 叠合视图。 | RMSD/局部差异不被过度解释。 |
| 5 | 输出记录 | 保存会话、命令、图片和人工判断。 | 可复现结构记录。 | 图注说明来源和边界。 |

执行时应先完成小样例或 dry-run，再扩大到批量任务。任何失败样本、低置信度结果或人工排除理由，都应保留在 manifest 或实验记录中。

## 代码案例与软件操作

![第 2 章流程解释图](../assets/imagegen/chapter-02-flow-structure-review.png){ loading=lazy }

**PyMOL/ChimeraX 结构复核流程图** 的编号含义如下：

| 编号 | 流程节点 |
|:---:|:---|
| 1 | 导入结构 |
| 2 | 检查链 ID |
| 3 | 定位配体/残基 |
| 4 | 叠合模型 |
| 5 | 导出视图 |
| 6 | 记录判断 |

本节用于训练 **2 章 结构来源、PyMOL 与 Chimera 可视化** 的最小复现意识。该示例演示 PyMOL 中最小活性位点复核流程；真实任务应补充结构来源、选择半径和人工判断。

=== "可复制代码"

    ```pymol
    load inputs/receptor.pdb, receptor
    hide everything
    show cartoon, receptor
    color slate, receptor
    select active_site, byres receptor within 5 of resn LIG
    show sticks, active_site
    png outputs/receptor_active_site.png, dpi=220
    ```

=== "配套文件"

    完整示例文件：[`chapter-02-structure-review.pml`](../assets/code/chapter-02-structure-review.pml)

![第 2 章软件操作截图](../assets/screenshots/chapter-02-pymol-review.png){ loading=lazy }

| 步骤 | 操作 |
|:---:|:---|
| 1 | 加载 PDB/mmCIF 或 AlphaFold 结构。 |
| 2 | 检查链、配体、缺失残基、金属离子和水分子。 |
| 3 | 保存会话、截图和人工判断。 |

!!! warning "常见错误"
    不要把 AlphaFold 预测结构当作实验结构；图注必须写清结构来源和置信度边界。

## 关键文献与 BibTeX key

<!-- refs:start -->

!!! quote "`jumper_highly_2021`"
    **Nature 风格引用：** Jumper, J., Evans, R., Pritzel, A., Green, T., Figurnov, M., Ronneberger, O. et al. Highly accurate protein structure prediction with AlphaFold. Nature (2021). https://doi.org/10.1038/s41586-021-03819-2

    **DOI/URL：** `10.1038/s41586-021-03819-2`

    **BibTeX key：** `jumper_highly_2021`

    **Zotero item key：** `UYRXX2U2`

    **本章用途：** 结构来源、预测模型边界与可视化复核的文献锚点。

!!! quote "`abramson_accurate_2024`"
    **Nature 风格引用：** Abramson, J., Adler, J., Dunger, J., Evans, R., Green, T., Pritzel, A. et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. Nature (2024). https://doi.org/10.1038/s41586-024-07487-w

    **DOI/URL：** `10.1038/s41586-024-07487-w`

    **BibTeX key：** `abramson_accurate_2024`

    **Zotero item key：** `PE42AXJX`

    **本章用途：** 结构来源、预测模型边界与可视化复核的文献锚点。

!!! quote "`akdel_structural_2022`"
    **Nature 风格引用：** Akdel, M., Pires, D. E. V., Porta Pardo, E., Jänes, J., Zalevsky, A. O., Mészáros, B. et al. A structural biology community assessment of AlphaFold2 applications. Nature Structural \& Molecular Biology 29, 1056-1067 (2022). https://doi.org/10.1038/s41594-022-00849-w

    **DOI/URL：** `10.1038/s41594-022-00849-w`

    **BibTeX key：** `akdel_structural_2022`

    **Zotero item key：** `5GOGPC63`

    **本章用途：** 结构来源、预测模型边界与可视化复核的文献锚点。

<!-- refs:end -->
## 实验/练习入口

本章练习强调可复查记录，而不是追求一次性完成复杂工具链。建议按以下顺序完成：

1. 选择一个 PDB 或 AlphaFold 结构，写出结构来源、链 ID、配体和置信度/分辨率。
2. 用 PyMOL 或 ChimeraX 导出一张口袋图，并记录选择命令。
3. 比较一个实验结构和一个预测结构，只描述观察到的差异，不直接推断活性变化。

完成练习后，应能把结果写入 `04_实验记录/` 或 `07_研究工作台/` 的对应页面。不能写入记录的练习，只能算操作尝试。

## 使用边界与常见误读

本节采用保守表述阶梯：预测、评分、可视化和文献案例通常只能写成“提示”“支持”或“可能一致”，除非有直接实验或严格验证，否则不写成“证明”。

| 易误读对象 | 稳健表述 | 写作处理 |
|:---|:---|:---|
| 漂亮结构图 | 不能替代结构证据。 | 图注必须写清来源、处理步骤和置信度边界。 |
| 预测结构 | 适合提出结构假设。 | 不能默认等同于实验结构或共晶复合物。 |
| 局部叠合 | 提示局部构象差异。 | 功能解释仍需文献、实验或后续计算支持。 |
| 截图 | 是教学和记录材料。 | 不能作为唯一 provenance。 |

写作时，如果一个结论只能由模型分数、单次截图或文献案例间接支持，应主动补上“仍需验证”“适用于该模型/该输入”“不等同于本项目结果”等边界。

## 延伸阅读与下一步

完成本章后，建议按以下路径进入下一轮学习或研究任务：

1. 把结构复核结果转入第 3 章 docking 的 receptor/box 记录。
2. 对需要动态解释的结构进入第 4 章 MD 或 AI 采样。
3. 对多组分结构假设进入第 5 章 Boltz2 或第 6 章蛋白设计流程。

[返回首页](../index.md)。
