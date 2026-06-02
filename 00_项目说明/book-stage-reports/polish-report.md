# P25 正文润色报告

本报告记录 8 个主章节的 reverse outline、claim-evidence map 和未改动边界。P25 只处理在线书籍正文，不新增科学事实，不改原始素材，不重做图像。

## 未改动边界

- `<!-- refs:start -->...<!-- refs:end -->` 引用列表保持由 `tools/update_book_references.py` 生成。
- 代码块、图片链接、DOI/URL、代码文件名和 manifest 字段原样保留。
- 章节正文不展示内部引用键或本地文献库条目编号；引用元数据继续保留在 `references/` 层。
- 未跟踪的 `06_原始学习素材/*.torrent` 文件未纳入本轮处理。

## 修改文件

- `book/docs/chapters/chapter-01.md`
- `book/docs/chapters/chapter-02.md`
- `book/docs/chapters/chapter-03.md`
- `book/docs/chapters/chapter-04.md`
- `book/docs/chapters/chapter-05.md`
- `book/docs/chapters/chapter-06.md`
- `book/docs/chapters/chapter-07.md`
- `book/docs/chapters/chapter-08.md`

## 第 1 章 Linux 与生化计算基础

### Reverse Outline

| 区块 | 段落功能 | 核心判断 | 边界提示 |
|:---|:---|:---|:---|
| 本章导读 | 说明 Linux 基础为何是计算实验台 | 项目目录、环境和日志规范 | 命令运行不等于结果可信 |
| 核心概念 | 定义路径、格式、环境和记录四类基础对象 | 方法卡和项目目录 | 概念是后续工具的前置条件 |
| 方法流程 | 给出从建目录到归档的执行顺序 | dry-run 与 manifest | 先小样例后正式运行 |
| 使用边界 | 拆分运行成功、provenance 和科学结论 | 项目记录规则 | 低层错误不得被写成模型失败 |

### Claim-Evidence Map

| Claim | Evidence | Status |
|:---|:---|:---|
| 命令成功不等于科学结果可信。 | 本章运行规范和后续章节的模型边界。 | supported |
| 可复现记录是计算实验的最低质量线。 | 实验记录模板和 LLM Wiki schema。 | supported |
| 本章不需要强行绑定专业论文。 | book_map 中第 1 章 required_bibtex_keys 为空。 | supported |

### 需作者确认

- 当前为教材化和学术化语言调整，未新增实验结果；后续如果加入真实运行截图或生产级实验结果，需要回到 `04_实验记录/` 补 provenance。

## 第 2 章 结构来源、PyMOL 与 Chimera 可视化

### Reverse Outline

| 区块 | 段落功能 | 核心判断 | 边界提示 |
|:---|:---|:---|:---|
| 本章导读 | 说明结构图的证据边界 | PDB/AlphaFold 与可视化工具 | 图像不等于证据 |
| 核心概念 | 定义结构来源、活性位点和叠合 | 结构生物学文献锚点 | 预测结构需单独标注 |
| 方法流程 | 从结构下载到截图记录 | PyMOL/ChimeraX 操作 | 截图必须可复现 |
| 使用边界 | 防止把预测结构写成实验结构 | AlphaFold 文献和本项目边界 | 功能推断需后续证据 |

### Claim-Evidence Map

| Claim | Evidence | Status |
|:---|:---|:---|
| AlphaFold 结构可用于提出结构假设。 | `jumper_highly_2021`、`abramson_accurate_2024`。 | supported |
| 预测结构不能默认等同于实验结构。 | `akdel_structural_2022` 与结构 QC 边界。 | supported |
| 口袋定义会影响后续 docking。 | 第 3 章 receptor/box 工作流。 | supported |

### 需作者确认

- 当前为教材化和学术化语言调整，未新增实验结果；后续如果加入真实运行截图或生产级实验结果，需要回到 `04_实验记录/` 补 provenance。

## 第 3 章 AI 多组分对接与虚拟筛选

### Reverse Outline

| 区块 | 段落功能 | 核心判断 | 边界提示 |
|:---|:---|:---|:---|
| 本章导读 | 解释 docking 作为研究漏斗的一层 | 对接和筛选文献 | score 不是活性 |
| 核心概念 | 定义 receptor、ligand、box、score、filter | 方法卡和文献锚点 | 各节点均需 provenance |
| 方法流程 | 从输入准备到候选交接 | dry-run 和 manifest | 失败样本必须记录 |
| 使用边界 | 防止 score 和文献案例过度解释 | 第 8 章边界要求 | 候选需后续验证 |

### Claim-Evidence Map

| Claim | Evidence | Status |
|:---|:---|:---|
| docking score 只能作为排序线索。 | `crampon_machine-learning_2022`、`gu_benchmarking_2025` 与本章边界。 | supported |
| box 来源会显著影响筛选结果。 | 对接方法卡和章节练习。 | supported |
| 第 8 章补充 PDF 不能写成本项目结果。 | P14/P24 维护边界。 | supported |

### 需作者确认

- 当前为教材化和学术化语言调整，未新增实验结果；后续如果加入真实运行截图或生产级实验结果，需要回到 `04_实验记录/` 补 provenance。

## 第 4 章 AI 采样、分子模拟与 MD 结果解释

### Reverse Outline

| 区块 | 段落功能 | 核心判断 | 边界提示 |
|:---|:---|:---|:---|
| 本章导读 | 说明 MD 输出需要 QC 后解释 | MD/BioEmu 方法卡 | 轨迹图不等于稳定性结论 |
| 核心概念 | 定义体系、轨迹指标、聚类和解释边界 | 分子模拟文献 | 指标必须绑定问题 |
| 方法流程 | 从体系准备到 claim 转写 | 轨迹分析脚本 | 采样和力场限制需保留 |
| 使用边界 | 防止 RMSD 和聚类过度解释 | 构象证据 | 机制仍需验证 |

### Claim-Evidence Map

| Claim | Evidence | Status |
|:---|:---|:---|
| RMSD 稳定不能单独证明结合稳定。 | MD 指标定义和第 4 章边界。 | supported |
| 代表构象选择依赖分析参数。 | 聚类流程和轨迹分析记录。 | supported |
| AI 采样输出需要记录模型版本和采样策略。 | P24 复现实验资源规则。 | supported |

### 需作者确认

- 当前为教材化和学术化语言调整，未新增实验结果；后续如果加入真实运行截图或生产级实验结果，需要回到 `04_实验记录/` 补 provenance。

## 第 5 章 亲和力预测、Boltz2 与模型评估

### Reverse Outline

| 区块 | 段落功能 | 核心判断 | 边界提示 |
|:---|:---|:---|:---|
| 本章导读 | 说明亲和力模型输出的证据等级 | Boltz2 和亲和力文献 | 预测值不是实验值 |
| 核心概念 | 定义输入、预测值、置信度、校准和候选优先级 | 模型评估文献 | 需联合读取多指标 |
| 方法流程 | 从输入 QC 到实验交接 | Boltz2 解析脚本 | 适用域必须说明 |
| 使用边界 | 防止把预测亲和力写成活性 | Zotero 文献和结果记录 | 实验验证仍必要 |

### Claim-Evidence Map

| Claim | Evidence | Status |
|:---|:---|:---|
| predicted affinity 不能直接等同于实验亲和力。 | `passaro_boltz-2_2025` 与模型边界。 | supported |
| 置信度应与亲和力输出联合解释。 | Boltz2 输出解释和 P24 代码案例。 | supported |
| 排序结果适合形成候选优先级。 | 第 5 章方法流程和第 8 章项目池。 | supported |

### 需作者确认

- 当前为教材化和学术化语言调整，未新增实验结果；后续如果加入真实运行截图或生产级实验结果，需要回到 `04_实验记录/` 补 provenance。

## 第 6 章 RFD3/RFdiffusion、ProteinMPNN 与蛋白设计

### Reverse Outline

| 区块 | 段落功能 | 核心判断 | 边界提示 |
|:---|:---|:---|:---|
| 本章导读 | 说明生成式设计的证据链 | RFdiffusion/ProteinMPNN 文献 | 生成候选不是实验成功 |
| 核心概念 | 定义目标、骨架、序列、回折叠和界面评分 | 蛋白设计文献锚点 | 每层证据需单独记录 |
| 方法流程 | 从约束到实验交接 | 设计配置模板 | seed/checkpoint/provenance 需保留 |
| 使用边界 | 防止把设计候选写成 binder | BindCraft/LigandMPNN 文献 | 实验验证仍必要 |

### Claim-Evidence Map

| Claim | Evidence | Status |
|:---|:---|:---|
| 生成结构不等于成功 binder。 | `watson_novo_2023`、`yang_w_past_2026` 与本章边界。 | supported |
| ProteinMPNN 输出需要回折叠验证。 | `dauparas_robust_2022` 与设计流程。 | supported |
| BindCraft/LigandMPNN 可作为设计链条的一部分。 | `pacesa_bindcraft_2024`、`dauparas_atomic_2025`。 | supported |

### 需作者确认

- 当前为教材化和学术化语言调整，未新增实验结果；后续如果加入真实运行截图或生产级实验结果，需要回到 `04_实验记录/` 补 provenance。

## 第 7 章 VibeCoding、Claude Code 与 AI Agent 工作流

### Reverse Outline

| 区块 | 段落功能 | 核心判断 | 边界提示 |
|:---|:---|:---|:---|
| 本章导读 | 说明 Agent 需要可审查闭环 | 项目 schema 和验证脚本 | 聊天输出不是证据 |
| 核心概念 | 定义任务说明、来源读取、执行控制、验证和沉淀 | LLM Wiki 规则 | 自动化须受边界约束 |
| 方法流程 | 从 brief 到维护记录 | validate/graph_health 脚本 | 验证不等于科学正确 |
| 使用边界 | 防止过度信任 Agent | 项目协议 | 关键判断需人工确认 |

### Claim-Evidence Map

| Claim | Evidence | Status |
|:---|:---|:---|
| Agent 输出需要文件和测试支撑。 | CLAUDE.md 与验证脚本。 | supported |
| 验证通过不等于科学判断完整。 | LLM Wiki 维护边界。 | supported |
| 可复用流程应沉淀为脚本或 skill。 | 本项目 schema 层设计。 | supported |

### 需作者确认

- 当前为教材化和学术化语言调整，未新增实验结果；后续如果加入真实运行截图或生产级实验结果，需要回到 `04_实验记录/` 补 provenance。

## 第 8 章 研究思路解析：寻靶、虚拟筛选、PPI 与蛋白设计整合

### Reverse Outline

| 区块 | 段落功能 | 核心判断 | 边界提示 |
|:---|:---|:---|:---|
| 本章导读 | 说明课程材料如何转成研究工作台 | 第 8 章补充 PDF 和研究工作台 | 文献案例不是项目结果 |
| 核心概念 | 定义研究问题、靶点证据、方法路线、claim 和输出任务 | 实体索引和 claims 矩阵 | 不同输出有不同口径 |
| 方法流程 | 从问题到输出交接 | 项目池和 Chai-1/RFD3 路线 | dry-run 与真实运行分开 |
| 使用边界 | 防止综合章节过度声明 | P14/P24 边界 | score 和案例需保守解释 |

### Claim-Evidence Map

| Claim | Evidence | Status |
|:---|:---|:---|
| 第八章补充 PDF 是文献案例和方法借鉴。 | P14 文献锚定与 P24 边界。 | supported |
| Chai-1 aggregate score 不能直接等同实验结合强度。 | Chai-1 方法卡和 claims 矩阵。 | supported |
| 项目池应同时记录证据、缺口和下一步实验。 | 07_研究工作台/研究问题与项目池.md。 | supported |

### 需作者确认

- 当前为教材化和学术化语言调整，未新增实验结果；后续如果加入真实运行截图或生产级实验结果，需要回到 `04_实验记录/` 补 provenance。
