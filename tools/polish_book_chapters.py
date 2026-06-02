#!/usr/bin/env python3
"""Apply P25 teaching-prose polish to online book chapters.

The script rewrites narrative sections only. It preserves generated reference
blocks, fenced code blocks, image links, DOI/URL strings, and code asset names
by avoiding those regions.
"""

from __future__ import annotations

import argparse
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = ROOT / "book" / "docs"
CHAPTER_ROOT = BOOK_ROOT / "chapters"
RESOURCE_ROOT = BOOK_ROOT / "resources"
BOOK_MAP_PATH = ROOT / "book" / "book_map.toml"

PROTECTED_TOKEN_RE = re.compile(r"https?://\S+|10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
FENCED_BLOCK_RE = re.compile(r"(?ms)^```.*?^```")
REF_BLOCK_RE = re.compile(r"(?ms)<!-- refs:start -->.*?<!-- refs:end -->")
IMAGE_TARGET_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class ChapterSpec:
    slug: str
    title: str
    problem: str
    task: str
    next_use: str
    objectives: tuple[str, ...]
    graph_entry: str
    concepts: tuple[tuple[str, str], ...]
    workflow: tuple[tuple[str, str, str, str, str], ...]
    code_context: str
    exercises: tuple[str, ...]
    boundaries: tuple[tuple[str, str, str], ...]
    next_steps: tuple[str, ...]
    reverse_outline: tuple[tuple[str, str, str, str], ...]
    claims: tuple[tuple[str, str, str], ...]


CHAPTERS: tuple[ChapterSpec, ...] = (
    ChapterSpec(
        slug="chapter-01",
        title="第 1 章 Linux 与生化计算基础",
        problem="后续对接、MD、Boltz2、蛋白设计和 AI Agent 操作都依赖同一套路径、环境、输入输出和日志规范；这些底层信息不清楚时，结果很难被复查。",
        task="本章把 Linux 基础转化为计算实验台规范，重点训练工作目录、文件格式、软件环境、日志保存和实验记录。",
        next_use="第 2-8 章会直接复用本章的目录、manifest、日志和记录习惯。",
        objectives=(
            "能说明工作目录、相对路径、绝对路径和环境变量在计算实验中的作用。",
            "能为一个最小任务建立 `inputs/`、`outputs/`、`logs/`、`scripts/` 和 `notes/`。",
            "能区分原始资料、wiki 笔记、方法卡、实验记录、运行输出和临时缓存。",
            "能把失败运行记录成可诊断问题，而不是只写“软件报错”。",
        ),
        graph_entry="本章在知识图谱中承担运行底座角色：它连接运行环境、数据接口和项目治理三类节点。读者应先理解这些节点的职责，再进入后续具体软件。",
        concepts=(
            ("工作目录", "工作目录是命令解析相对路径的坐标原点，决定软件能否找到输入和写出结果。"),
            ("文件格式", "FASTA、PDB/mmCIF、SDF、SMILES、YAML、CSV/TSV 等格式是不同工具之间的数据契约，不能只凭扩展名判断可用性。"),
            ("软件环境", "conda、Python、CUDA、模型权重和系统变量共同定义一次运行的可复现条件。"),
            ("日志与 manifest", "日志记录单次运行，manifest 管理批量任务；二者共同支撑失败诊断和结果追溯。"),
            ("实验记录", "实验记录把输入、命令、参数、输出、QC 和人工判断固定下来，是后续写作和复盘的最低证据单元。"),
        ),
        workflow=(
            ("1", "项目根目录", "确认当前目录和任务命名。", "标准任务文件夹。", "`pwd`/`Get-Location` 与预期项目根一致。"),
            ("2", "输入文件", "检查 FASTA、结构、配体或表格格式。", "输入 QC 表。", "链 ID、配体、电荷、列名和空值已记录。"),
            ("3", "软件环境", "建立或激活独立环境并导出版本。", "环境记录。", "关键包、Python、CUDA 或网页版本可追溯。"),
            ("4", "小样例", "先运行 dry-run 或最小输入。", "最小输出和日志。", "能区分路径错误、格式错误和模型错误。"),
            ("5", "正式运行", "保存标准输出、错误输出和退出状态。", "日志与 manifest。", "每个样本都有状态和失败原因。"),
            ("6", "归档", "把结果写入实验记录或方法卡。", "可复查记录。", "文献案例、课程范文和本项目结果分层。"),
        ),
        code_context="该示例用于演示如何把一次环境检查转成最小可复现任务目录；代码可以复制，但输入路径和日期应按实际项目修改。",
        exercises=(
            "建立一个空白计算任务目录，并在 `notes/README.md` 中记录输入来源和公开边界。",
            "为 FASTA、PDB/mmCIF、SDF/SMILES 和 CSV/TSV 各写一行输入 QC 规则。",
            "模拟一次 dry-run 记录，列出命令、参数、预期输出、日志路径和下一步判断。",
        ),
        boundaries=(
            ("命令成功", "只能说明程序完成运行。", "仍需检查输入质量、参数、模型边界和输出 QC。"),
            ("路径记录", "不能单独构成 provenance。", "必须补充来源、日期、版本、处理步骤和是否人工修改。"),
            ("环境可用", "不等于跨机器可复现。", "需要导出环境、记录模型权重/API 版本和随机种子。"),
            ("正文写作", "不应承载所有运行细节。", "具体结果先进入 `04_实验记录/`，长期流程再沉淀到方法卡。"),
        ),
        next_steps=(
            "先完成一个最小任务目录，再进入第 2 章做结构可视化。",
            "后续章节使用同一套记录语言描述 docking、MD、Boltz2、RFdiffusion/RFD3 和 Chai-1。",
            "需要真实运行时，优先从附录 B 选择实验记录模板。",
        ),
        reverse_outline=(
            ("本章导读", "说明 Linux 基础为何是计算实验台", "项目目录、环境和日志规范", "命令运行不等于结果可信"),
            ("核心概念", "定义路径、格式、环境和记录四类基础对象", "方法卡和项目目录", "概念是后续工具的前置条件"),
            ("方法流程", "给出从建目录到归档的执行顺序", "dry-run 与 manifest", "先小样例后正式运行"),
            ("使用边界", "拆分运行成功、provenance 和科学结论", "项目记录规则", "低层错误不得被写成模型失败"),
        ),
        claims=(
            ("命令成功不等于科学结果可信。", "本章运行规范和后续章节的模型边界。", "supported"),
            ("可复现记录是计算实验的最低质量线。", "实验记录模板和 LLM Wiki schema。", "supported"),
            ("本章不需要强行绑定专业论文。", "book_map 中第 1 章 required_bibtex_keys 为空。", "supported"),
        ),
    ),
    ChapterSpec(
        slug="chapter-02",
        title="第 2 章 结构来源、PyMOL 与 Chimera 可视化",
        problem="结构图容易给读者强烈直观印象，但图像质量并不等于结构证据质量。",
        task="本章训练读者区分实验结构、预测结构和可视化结果，并把链、配体、口袋、缺失区域和置信度写清楚。",
        next_use="第 3 章的 docking box、第 4 章的 MD 初始结构、第 5 章的多组分预测和第 6 章的设计约束都依赖本章的结构复核。",
        objectives=(
            "能区分 PDB/mmCIF 实验结构、AlphaFold 预测结构和经人工处理的工作结构。",
            "能在 PyMOL/ChimeraX 中检查链 ID、配体、活性位点、缺失残基和水/金属离子。",
            "能说明结构叠合、局部口袋视图和截图在证据链中的边界。",
            "能把一张结构图写成可追溯的图注和实验记录字段。",
        ),
        graph_entry="本章的图谱入口连接结构来源、可视化工具和证据审查。图像展示的是分析对象，正文表格才是结构来源和判断标准。",
        concepts=(
            ("结构来源", "结构来源决定证据等级；实验结构、预测结构和处理后结构必须分开记录。"),
            ("链与配体", "链 ID、配体名、辅因子和金属离子是后续口袋定义和对接准备的关键字段。"),
            ("活性位点", "活性位点应由共晶配体、功能残基、文献或预测口袋共同约束，而不是只凭视觉中心选择。"),
            ("结构叠合", "结构叠合用于比较构象和模型差异，不能自动证明功能等价。"),
            ("截图记录", "截图应记录视角、对象、颜色、选择命令和来源，避免成为不可复现的装饰图。"),
        ),
        workflow=(
            ("1", "结构文件", "确认来源、分辨率/置信度和下载日期。", "结构来源记录。", "PDB ID 或模型来源可追溯。"),
            ("2", "链和配体", "检查链 ID、配体、缺失区域和非标准残基。", "结构 QC 表。", "关键对象已命名。"),
            ("3", "局部口袋", "围绕配体或功能残基建立局部视图。", "口袋截图。", "选择半径和残基列表明确。"),
            ("4", "叠合比较", "比较实验结构、预测结构或同源结构。", "叠合视图。", "RMSD/局部差异不被过度解释。"),
            ("5", "输出记录", "保存会话、命令、图片和人工判断。", "可复现结构记录。", "图注说明来源和边界。"),
        ),
        code_context="该示例演示 PyMOL 中最小活性位点复核流程；真实任务应补充结构来源、选择半径和人工判断。",
        exercises=(
            "选择一个 PDB 或 AlphaFold 结构，写出结构来源、链 ID、配体和置信度/分辨率。",
            "用 PyMOL 或 ChimeraX 导出一张口袋图，并记录选择命令。",
            "比较一个实验结构和一个预测结构，只描述观察到的差异，不直接推断活性变化。",
        ),
        boundaries=(
            ("漂亮结构图", "不能替代结构证据。", "图注必须写清来源、处理步骤和置信度边界。"),
            ("预测结构", "适合提出结构假设。", "不能默认等同于实验结构或共晶复合物。"),
            ("局部叠合", "提示局部构象差异。", "功能解释仍需文献、实验或后续计算支持。"),
            ("截图", "是教学和记录材料。", "不能作为唯一 provenance。"),
        ),
        next_steps=(
            "把结构复核结果转入第 3 章 docking 的 receptor/box 记录。",
            "对需要动态解释的结构进入第 4 章 MD 或 AI 采样。",
            "对多组分结构假设进入第 5 章 Boltz2 或第 6 章蛋白设计流程。",
        ),
        reverse_outline=(
            ("本章导读", "说明结构图的证据边界", "PDB/AlphaFold 与可视化工具", "图像不等于证据"),
            ("核心概念", "定义结构来源、活性位点和叠合", "结构生物学文献锚点", "预测结构需单独标注"),
            ("方法流程", "从结构下载到截图记录", "PyMOL/ChimeraX 操作", "截图必须可复现"),
            ("使用边界", "防止把预测结构写成实验结构", "AlphaFold 文献和本项目边界", "功能推断需后续证据"),
        ),
        claims=(
            ("AlphaFold 结构可用于提出结构假设。", "`jumper_highly_2021`、`abramson_accurate_2024`。", "supported"),
            ("预测结构不能默认等同于实验结构。", "`akdel_structural_2022` 与结构 QC 边界。", "supported"),
            ("口袋定义会影响后续 docking。", "第 3 章 receptor/box 工作流。", "supported"),
        ),
    ),
    ChapterSpec(
        slug="chapter-03",
        title="第 3 章 AI 多组分对接与虚拟筛选",
        problem="虚拟筛选容易把大量候选和分数包装成“结果”，但 docking score 首先是排序线索。",
        task="本章建立从受体准备、配体库、box、打分、重评分到候选短名单的证据链。",
        next_use="第 4 章用 MD 复核候选构象，第 5 章用亲和力模型进一步排序，第 8 章把筛选放入研究项目池。",
        objectives=(
            "能记录 receptor、ligand library、box、score、pose 和筛选阈值。",
            "能区分 docking score、pose 合理性、重评分结果和实验候选。",
            "能把文献案例作为流程参考，而不是写成本项目筛选结果。",
            "能用 manifest 管理批量筛选状态和失败原因。",
        ),
        graph_entry="本章图谱以受体-配体-box-score-filter 为主线。读者应把每个节点理解为证据门槛，而不是单纯的软件步骤。",
        concepts=(
            ("受体准备", "受体准备定义计算对象，包括链选择、质子化、配体/水/金属处理和口袋来源。"),
            ("配体库", "配体库的来源、去重、质子化、手性和 3D 构象决定筛选结果的可解释性。"),
            ("box", "box 是搜索空间假设，来源应来自共晶配体、功能位点、预测口袋或文献证据。"),
            ("score", "score 是模型给出的排序信号，通常不能跨工具、跨靶点或跨化学系列直接比较。"),
            ("过滤规则", "过滤应同时考虑分数、pose、化学合理性、可合成性和后续验证成本。"),
        ),
        workflow=(
            ("1", "受体结构", "完成结构 QC、处理氢和口袋来源。", "receptor 文件和 QC 记录。", "链、配体、box 来源清楚。"),
            ("2", "配体库", "统一 ID、格式、质子化、去重和失败状态。", "ligand manifest。", "每个分子来源可追溯。"),
            ("3", "搜索空间", "定义 box 中心、大小和依据。", "box 参数表。", "box 不超出合理口袋范围。"),
            ("4", "初筛", "运行 docking 并保存 pose、score 和日志。", "score 表和 pose 文件。", "失败样本不被静默丢弃。"),
            ("5", "复核", "按 pose、相互作用、化学规则和重评分过滤。", "shortlist。", "候选保留理由明确。"),
            ("6", "交接", "把候选转入 MD、亲和力或实验计划。", "下一步队列。", "不把 score 写成活性。"),
        ),
        code_context="该示例是 docking dry-run 的输入组织方式，适合检查 box、日志和输出表；真实筛选需要完整 receptor/ligand provenance。",
        exercises=(
            "完成 1 个 receptor x 3 ligands 的 dry-run，并记录 box 来源。",
            "建立 10-20 个候选分子的 manifest，保留失败原因和人工复核状态。",
            "把一个 top pose 转写成保守 claim，列出支持证据和需要补充的验证。",
        ),
        boundaries=(
            ("docking score", "提示排序线索。", "不能写成 Kd、IC50、结合自由能或实验活性。"),
            ("top pose", "提示可能构象。", "仍需结构复核、MD、自由能或实验验证。"),
            ("AI docking", "可能改善特定 benchmark 表现。", "新靶点和新化学空间仍需适用域评估。"),
            ("文献案例", "可借鉴流程和参数记录。", "不能直接迁移为本项目结果。"),
        ),
        next_steps=(
            "将 top pose 交给第 4 章做轨迹或构象稳定性复核。",
            "将候选表交给第 5 章做亲和力预测和模型边界判断。",
            "在第 8 章把候选写入项目池，明确文献案例、方法假设和本项目结果的分层。",
        ),
        reverse_outline=(
            ("本章导读", "解释 docking 作为研究漏斗的一层", "对接和筛选文献", "score 不是活性"),
            ("核心概念", "定义 receptor、ligand、box、score、filter", "方法卡和文献锚点", "各节点均需 provenance"),
            ("方法流程", "从输入准备到候选交接", "dry-run 和 manifest", "失败样本必须记录"),
            ("使用边界", "防止 score 和文献案例过度解释", "第 8 章边界要求", "候选需后续验证"),
        ),
        claims=(
            ("docking score 只能作为排序线索。", "`crampon_machine-learning_2022`、`gu_benchmarking_2025` 与本章边界。", "supported"),
            ("box 来源会显著影响筛选结果。", "对接方法卡和章节练习。", "supported"),
            ("第 8 章补充 PDF 不能写成本项目结果。", "P14/P24 维护边界。", "supported"),
        ),
    ),
    ChapterSpec(
        slug="chapter-04",
        title="第 4 章 AI 采样、分子模拟与 MD 结果解释",
        problem="轨迹图和 RMSD 曲线常被直接解释为稳定性结论，但 MD 输出首先需要经过体系、参数和采样充分性检查。",
        task="本章把 MD 和 AI 采样结果拆成体系准备、轨迹 QC、构象分析、代表结构和解释边界。",
        next_use="第 3 章的 docking pose、第 5 章的亲和力解释和第 8 章的项目假设都需要本章的动态证据语言。",
        objectives=(
            "能记录拓扑、力场、溶剂、离子、平衡、生产时间和轨迹文件。",
            "能解释 RMSD、RMSF、接触、聚类和代表构象的不同含义。",
            "能区分轨迹 QC、结构观察和机制解释。",
            "能把 AI 采样或 MD 输出写成有边界的构象证据。",
        ),
        graph_entry="本章知识图谱连接体系准备、生产轨迹和构象证据。读者应把轨迹指标看作证据片段，而不是单一结论。",
        concepts=(
            ("体系准备", "体系准备决定模拟对象，包括力场、质子化、配体参数、水盒、离子和平衡过程。"),
            ("轨迹 QC", "RMSD、能量、温度和压力用于判断运行是否基本可用，但不直接回答机制问题。"),
            ("局部柔性", "RMSF、接触频率和距离变化更适合描述局部构象和结合界面。"),
            ("聚类", "聚类用于选择代表构象，结果依赖对齐对象、特征选择和聚类参数。"),
            ("解释边界", "MD 支持动态假设，但采样时间、力场和初始结构限制必须写清楚。"),
        ),
        workflow=(
            ("1", "初始结构", "确认来源、配体参数和缺失区域。", "体系准备记录。", "输入结构与第 2/3 章一致。"),
            ("2", "参数化", "选择力场、溶剂、离子和约束。", "拓扑与参数文件。", "配体和非标准残基参数可追溯。"),
            ("3", "平衡", "完成能量最小化、NVT/NPT 或等效步骤。", "平衡日志。", "温度、压力和能量无明显异常。"),
            ("4", "生产轨迹", "运行生产模拟或 AI 采样。", "轨迹和日志。", "运行长度、步长和保存频率明确。"),
            ("5", "分析", "计算 RMSD/RMSF、接触、聚类和代表构象。", "分析表和结构。", "指标对应具体问题。"),
            ("6", "解释", "把观察转写成 claim。", "有边界的构象证据。", "不把相关模式写成因果机制。"),
        ),
        code_context="该示例演示如何从 RMSD 表生成 QC 摘要；真实解释还需要结合接触、聚类和结构复核。",
        exercises=(
            "为一个短轨迹写出体系准备字段和轨迹文件清单。",
            "计算或模拟 RMSD/RMSF 摘要，并说明这些指标回答不了什么问题。",
            "选择一个代表构象，写出选择依据和不能据此声称的结论。",
        ),
        boundaries=(
            ("RMSD 稳定", "提示整体构象变化较小。", "不能单独证明结合稳定或活性增强。"),
            ("轨迹聚类", "提供代表构象候选。", "结果依赖特征、对齐和采样长度。"),
            ("AI 采样", "可扩展构象搜索。", "模型版本和采样策略需记录，不能替代实验。"),
            ("机制解释", "可提出可能解释。", "仍需多来源证据或实验验证。"),
        ),
        next_steps=(
            "把代表构象回送第 3 章复核 pose 或重新定义口袋。",
            "把构象和接触特征交给第 5 章亲和力模型解释。",
            "在第 8 章把动态证据写入 claims 矩阵并标注证据强度。",
        ),
        reverse_outline=(
            ("本章导读", "说明 MD 输出需要 QC 后解释", "MD/BioEmu 方法卡", "轨迹图不等于稳定性结论"),
            ("核心概念", "定义体系、轨迹指标、聚类和解释边界", "分子模拟文献", "指标必须绑定问题"),
            ("方法流程", "从体系准备到 claim 转写", "轨迹分析脚本", "采样和力场限制需保留"),
            ("使用边界", "防止 RMSD 和聚类过度解释", "构象证据", "机制仍需验证"),
        ),
        claims=(
            ("RMSD 稳定不能单独证明结合稳定。", "MD 指标定义和第 4 章边界。", "supported"),
            ("代表构象选择依赖分析参数。", "聚类流程和轨迹分析记录。", "supported"),
            ("AI 采样输出需要记录模型版本和采样策略。", "P24 复现实验资源规则。", "supported"),
        ),
    ),
    ChapterSpec(
        slug="chapter-05",
        title="第 5 章 亲和力预测、Boltz2 与模型评估",
        problem="亲和力预测容易被读成实验亲和力，但模型输出的数值、置信度和适用域必须同时解释。",
        task="本章把亲和力预测拆成输入定义、模型输出、置信度、校准、排序和实验交接。",
        next_use="第 3 章筛选候选、第 4 章代表构象和第 8 章项目优先级都需要本章的预测边界。",
        objectives=(
            "能说明 Boltz2、DeepDTAF、PPI-Affinity 等模型输出的适用场景。",
            "能同时读取 predicted affinity、confidence、结构质量和输入来源。",
            "能把模型排序写成候选优先级，而不是实验活性结论。",
            "能设计需要补充的校准、复核或实验验证。",
        ),
        graph_entry="本章图谱连接 docking score、结构预测、亲和力模型、置信度和排序。读者应把模型输出理解为决策证据的一层。",
        concepts=(
            ("输入定义", "亲和力模型的输入包括序列、结构、配体和复合物假设，输入错误会直接影响输出解释。"),
            ("预测值", "predicted affinity 是模型估计值，不能默认等同于 Kd、IC50 或实验自由能。"),
            ("置信度", "置信度用于判断模型对结构或复合物假设的自洽程度，应与亲和力数值联合读取。"),
            ("校准", "模型排序需要在相近化学系列、同一靶点或已有实验数据背景下校准。"),
            ("候选优先级", "预测结果适合辅助排序和实验设计，不应替代实验验证。"),
        ),
        workflow=(
            ("1", "FASTA/SMILES/结构", "检查链、配体和输入来源。", "输入 QC。", "ID、来源和处理步骤完整。"),
            ("2", "任务配置", "编写 YAML 或模型输入表。", "配置文件。", "链、配体、模板/约束含义明确。"),
            ("3", "模型运行", "保存预测输出、日志和版本。", "结构、分数和置信度。", "模型版本和运行方式可追溯。"),
            ("4", "结果解析", "联合读取 affinity、confidence 和结构质量。", "排序表。", "低置信度结果不被强解释。"),
            ("5", "校准复核", "与 docking、MD 或已知实验数据对照。", "证据矩阵。", "适用域和异常值明确。"),
            ("6", "交接", "形成实验候选或下一轮计算。", "项目队列。", "预测与实验结论分层。"),
        ),
        code_context="该示例只演示结果表解析和排序；真实 Boltz2 运行需要记录 YAML、模型版本、输入来源和输出目录。",
        exercises=(
            "读取一张 Boltz2 结果表，同时列出 predicted affinity 和 confidence。",
            "为 5 个候选写出排序理由，并标注低置信度或输入风险。",
            "把一个亲和力预测结果转写成保守 claim，说明需要哪些实验或计算补证。",
        ),
        boundaries=(
            ("predicted affinity", "提示模型估计的相对优先级。", "不能直接写成实验 Kd、IC50 或活性。"),
            ("confidence", "反映模型自洽程度。", "高置信度不等于实验正确，低置信度需谨慎解释。"),
            ("跨模型比较", "可提供互补证据。", "不同训练集、输出尺度和适用域不能简单相加。"),
            ("候选排序", "支持下一步实验设计。", "仍需实验测定或独立计算验证。"),
        ),
        next_steps=(
            "把预测结果与第 3 章 docking pose 和第 4 章构象证据联合解释。",
            "对蛋白/多肽设计候选进入第 6 章回折叠和界面评估。",
            "在第 8 章把预测结果写入项目优先级，而不是写成最终结论。",
        ),
        reverse_outline=(
            ("本章导读", "说明亲和力模型输出的证据等级", "Boltz2 和亲和力文献", "预测值不是实验值"),
            ("核心概念", "定义输入、预测值、置信度、校准和候选优先级", "模型评估文献", "需联合读取多指标"),
            ("方法流程", "从输入 QC 到实验交接", "Boltz2 解析脚本", "适用域必须说明"),
            ("使用边界", "防止把预测亲和力写成活性", "Zotero 文献和结果记录", "实验验证仍必要"),
        ),
        claims=(
            ("predicted affinity 不能直接等同于实验亲和力。", "`passaro_boltz-2_2025` 与模型边界。", "supported"),
            ("置信度应与亲和力输出联合解释。", "Boltz2 输出解释和 P24 代码案例。", "supported"),
            ("排序结果适合形成候选优先级。", "第 5 章方法流程和第 8 章项目池。", "supported"),
        ),
    ),
    ChapterSpec(
        slug="chapter-06",
        title="第 6 章 RFD3/RFdiffusion、ProteinMPNN 与蛋白设计",
        problem="生成式蛋白设计会产生大量结构候选，但生成结构不等于可折叠、可表达或可结合的蛋白。",
        task="本章建立从设计目标、约束、骨架生成、序列设计、回折叠、界面评分到实验交接的证据链。",
        next_use="第 8 章的 PPI 与蛋白设计项目池会复用本章的候选筛选标准和记录字段。",
        objectives=(
            "能记录 target、motif、hotspot、contig、seed、checkpoint 和输出目录。",
            "能区分骨架生成、序列设计、回折叠验证和界面评分的职责。",
            "能说明 RFdiffusion/RFD3、ProteinMPNN、BindCraft、LigandMPNN 的证据边界。",
            "能把生成候选转化为可审查的实验交接清单。",
        ),
        graph_entry="本章图谱强调蛋白设计链条的分层：生成、设计、验证和交接必须分开记录。",
        concepts=(
            ("设计目标", "设计目标定义靶点、功能界面、约束和实验用途，是后续生成是否有意义的前提。"),
            ("骨架生成", "RFdiffusion/RFD3 生成的是满足约束的结构候选，仍需序列和稳定性验证。"),
            ("序列设计", "ProteinMPNN 等工具为骨架分配序列，输出质量依赖骨架合理性和约束设置。"),
            ("回折叠验证", "回折叠用于检查序列是否可能回到预期结构，但不能证明表达或结合。"),
            ("界面评分", "界面评分辅助筛选候选，必须与多样性、可制造性和实验成本一起判断。"),
        ),
        workflow=(
            ("1", "靶点和约束", "定义 target、motif、hotspot、contig 和排除条件。", "设计配置。", "约束来源明确。"),
            ("2", "骨架生成", "小批量生成 backbone 候选。", "候选结构。", "seed、checkpoint 和失败原因记录。"),
            ("3", "序列设计", "为骨架设计多条序列。", "序列候选。", "序列多样性和重复候选已检查。"),
            ("4", "回折叠", "预测设计序列结构并与目标骨架比较。", "回折叠结果。", "RMSD/置信度低者不强解释。"),
            ("5", "界面评估", "检查接触、埋藏面积、冲突和评分。", "筛选表。", "界面指标和人工复核一致。"),
            ("6", "实验交接", "输出候选、边界和验证计划。", "实验队列。", "不把生成候选写成成功 binder。"),
        ),
        code_context="该配置模板用于记录设计目标和筛选阈值；真实运行需要补充模型来源、checkpoint、seed 和完整输出目录。",
        exercises=(
            "为一个设计任务写出 target、hotspot、contig 和排除条件。",
            "设计一个 10 个候选的小批量 dry-run manifest，记录 seed 和失败原因。",
            "把一个候选写成保守 claim，区分生成、回折叠和实验验证状态。",
        ),
        boundaries=(
            ("生成 backbone", "提示存在满足约束的结构候选。", "不能说明序列可折叠、可表达或可结合。"),
            ("ProteinMPNN 序列", "支持序列候选生成。", "仍需回折叠、界面和实验可行性过滤。"),
            ("界面评分", "辅助候选排序。", "不能替代生化结合实验。"),
            ("设计成功", "只有多层验证后才能谨慎表述。", "未验证时写作“候选”“假设”或“待验证设计”。"),
        ),
        next_steps=(
            "将候选写入第 8 章项目池，标注设计阶段和验证缺口。",
            "把需要亲和力解释的候选回到第 5 章做模型评估。",
            "真实运行后先更新 `04_实验记录/`，再考虑写入在线书籍案例。",
        ),
        reverse_outline=(
            ("本章导读", "说明生成式设计的证据链", "RFdiffusion/ProteinMPNN 文献", "生成候选不是实验成功"),
            ("核心概念", "定义目标、骨架、序列、回折叠和界面评分", "蛋白设计文献锚点", "每层证据需单独记录"),
            ("方法流程", "从约束到实验交接", "设计配置模板", "seed/checkpoint/provenance 需保留"),
            ("使用边界", "防止把设计候选写成 binder", "BindCraft/LigandMPNN 文献", "实验验证仍必要"),
        ),
        claims=(
            ("生成结构不等于成功 binder。", "`watson_novo_2023`、`yang_w_past_2026` 与本章边界。", "supported"),
            ("ProteinMPNN 输出需要回折叠验证。", "`dauparas_robust_2022` 与设计流程。", "supported"),
            ("BindCraft/LigandMPNN 可作为设计链条的一部分。", "`pacesa_bindcraft_2024`、`dauparas_atomic_2025`。", "supported"),
        ),
    ),
    ChapterSpec(
        slug="chapter-07",
        title="第 7 章 VibeCoding、Claude Code 与 AI Agent 工作流",
        problem="AI Agent 可以加速整理、编码和验证，但如果没有任务边界、来源路径和验收命令，输出很难被审查。",
        task="本章把 Agent 工作流拆成说明、读取、计划、执行、验证和知识沉淀六个环节。",
        next_use="所有后续章节更新、研究工作台维护和在线书籍发布都应复用本章的验证闭环。",
        objectives=(
            "能写出包含目标、范围、禁止事项和验收标准的 Agent 任务说明。",
            "能要求 Agent 先读索引、映射、来源和 schema，再执行修改。",
            "能区分聊天回答、文件变更、测试输出和维护报告的证据等级。",
            "能把可复用流程沉淀为 skill、脚本或资源页。",
        ),
        graph_entry="本章图谱连接项目协议、技能、工具调用、验证脚本和维护记录。它定义的是 Agent 如何可靠地参与知识库工作。",
        concepts=(
            ("任务说明", "任务说明必须包含目标、范围、输入、禁止事项和验收标准。"),
            ("来源读取", "Agent 在写入前应读取 `index.md`、目录 `_index.md`、`book_map.toml` 和相关章节。"),
            ("执行控制", "修改应限定在任务相关文件内，避免无关重构和原始资料移动。"),
            ("验证闭环", "测试、构建、wiki 校验和图谱体检共同构成验收证据。"),
            ("知识沉淀", "长期可复用的流程应写入脚本、skill、资源页或维护报告。"),
        ),
        workflow=(
            ("1", "任务说明", "明确目标、范围、禁止事项和验收标准。", "可执行 brief。", "不会误改 raw sources。"),
            ("2", "来源读取", "读取索引、映射、schema 和相关正文。", "上下文清单。", "不凭记忆猜结构。"),
            ("3", "计划", "列出文件范围、保护对象和验证命令。", "实施计划。", "关键风险已识别。"),
            ("4", "执行", "按最小必要范围写入。", "文件变更。", "引用、路径和 token 保留。"),
            ("5", "验证", "运行测试、构建和 wiki 体检。", "验证输出。", "失败项有定位。"),
            ("6", "沉淀", "更新日志、报告和复用入口。", "维护记录。", "后续 Agent 可接续。"),
        ),
        code_context="该示例是在线书籍更新后的最小验证闭环；真实任务应根据影响面增加专门测试。",
        exercises=(
            "把一个宽泛需求改写成包含范围、禁止事项和验收标准的 Agent brief。",
            "为一次章节更新列出必须读取的 5 个来源文件。",
            "设计一个 AI 回归评测问题，要求答案包含路径、关键文献条目、边界和待确认项。",
        ),
        boundaries=(
            ("Agent 回答", "是工作产物线索。", "不能替代文件、引用、测试和维护记录。"),
            ("自动修改", "适合结构化和可验证任务。", "原始资料移动、文献结论新增和实验解释需人工确认。"),
            ("验证通过", "说明机械一致性达标。", "不自动保证科学判断完整。"),
            ("skill", "封装稳定流程。", "不应把项目特有事实写成通用规则。"),
        ),
        next_steps=(
            "用本章流程维护在线书籍、研究工作台和文献映射。",
            "把高频任务抽成脚本或本地 skill，并保持项目内 provenance。",
            "进入第 8 章时，用 Agent 辅助项目池排序，但最终研究判断仍由研究者确认。",
        ),
        reverse_outline=(
            ("本章导读", "说明 Agent 需要可审查闭环", "项目 schema 和验证脚本", "聊天输出不是证据"),
            ("核心概念", "定义任务说明、来源读取、执行控制、验证和沉淀", "LLM Wiki 规则", "自动化须受边界约束"),
            ("方法流程", "从 brief 到维护记录", "validate/graph_health 脚本", "验证不等于科学正确"),
            ("使用边界", "防止过度信任 Agent", "项目协议", "关键判断需人工确认"),
        ),
        claims=(
            ("Agent 输出需要文件和测试支撑。", "CLAUDE.md 与验证脚本。", "supported"),
            ("验证通过不等于科学判断完整。", "LLM Wiki 维护边界。", "supported"),
            ("可复用流程应沉淀为脚本或 skill。", "本项目 schema 层设计。", "supported"),
        ),
    ),
    ChapterSpec(
        slug="chapter-08",
        title="第 8 章 研究思路解析：寻靶、虚拟筛选、PPI 与蛋白设计整合",
        problem="综合章节最容易把课程范文、文献案例、方法假设和本项目结果混在一起。",
        task="本章把寻靶、结构复核、虚拟筛选、PPI 筛选、蛋白设计、证据 claim 和输出任务组织成研究工作台。",
        next_use="本章是从课程讲义走向个人课题设计、综述写作、课题申请和实验队列的入口。",
        objectives=(
            "能把研究问题拆成靶点证据、结构来源、可用方法、证据缺口和下一步实验。",
            "能区分第八章补充 PDF 中的文献案例、课程范文和本项目结果。",
            "能在项目池中同时管理虚拟筛选、PPI 和蛋白设计路线。",
            "能把关键判断写成 claim-evidence-boundary 形式。",
        ),
        graph_entry="本章图谱是全书的研究工作台入口。它不新增单一工具，而是把前七章的证据和方法组合成项目路线。",
        concepts=(
            ("研究问题", "研究问题应明确对象、疾病/功能场景、候选方法和可验证输出。"),
            ("靶点证据", "靶点证据需要区分数据库线索、文献案例、结构可用性和实验可行性。"),
            ("方法路线", "虚拟筛选、PPI 筛选和蛋白设计是不同路线，输入、输出和验证成本不同。"),
            ("claim 层", "claim 应同时记录支持证据、证据强度、适用边界和下一步验证。"),
            ("输出任务", "课件、综述、课题申请和实验记录可以共享材料，但写作口径不同。"),
        ),
        workflow=(
            ("1", "研究问题", "定义目标、对象和可产出物。", "项目问题卡。", "问题不只是工具练习。"),
            ("2", "证据矩阵", "收集靶点、结构、文献和方法证据。", "evidence matrix。", "文献案例与项目结果分层。"),
            ("3", "路线选择", "选择虚拟筛选、PPI 或蛋白设计路线。", "方法路径。", "输入和验证成本明确。"),
            ("4", "候选生成", "执行或规划 docking、Chai-1、RFD3/RFdiffusion 等步骤。", "候选表。", "dry-run 与真实运行分开。"),
            ("5", "claim 写作", "把关键判断写成 claim-evidence-boundary。", "claims 矩阵。", "score/affinity/design 不被过度解释。"),
            ("6", "输出交接", "进入阅读、实验或写作队列。", "项目池和输出视图。", "provenance 可追溯。"),
        ),
        code_context="该示例演示项目优先级排序表的计算方式；真实项目排序需要人工确认证据权重和实验条件。",
        exercises=(
            "从一个补充 PDF 案例中提取研究问题、方法路线和不能迁移的结论。",
            "为一个候选靶点建立 claim-evidence-boundary 表。",
            "把一个项目写入项目池，给出下一步实验、阅读队列和可产出物。",
        ),
        boundaries=(
            ("文献案例", "可作为流程和证据组织参考。", "不能写成本项目已经得到的结果。"),
            ("Chai-1 aggregate score", "提示多模型或多界面排序线索。", "不能直接写成 PPI 实验结合强度。"),
            ("研究路线", "支持项目优先级判断。", "不替代真实实验、伦理和资源条件评估。"),
            ("输出整理", "可服务课件、综述和申请书。", "不得牺牲 provenance 或混淆来源层级。"),
        ),
        next_steps=(
            "把最有价值的研究问题写入 `07_研究工作台/研究问题与项目池.md`。",
            "把需要运行的任务写入 `07_研究工作台/实验队列.md`，再进入 `04_实验记录/`。",
            "将可写作内容拆成课件、综述、课题申请和实验记录四类出口。"),
        reverse_outline=(
            ("本章导读", "说明课程材料如何转成研究工作台", "第 8 章补充 PDF 和研究工作台", "文献案例不是项目结果"),
            ("核心概念", "定义研究问题、靶点证据、方法路线、claim 和输出任务", "实体索引和 claims 矩阵", "不同输出有不同口径"),
            ("方法流程", "从问题到输出交接", "项目池和 Chai-1/RFD3 路线", "dry-run 与真实运行分开"),
            ("使用边界", "防止综合章节过度声明", "P14/P24 边界", "score 和案例需保守解释"),
        ),
        claims=(
            ("第八章补充 PDF 是文献案例和方法借鉴。", "P14 文献锚定与 P24 边界。", "supported"),
            ("Chai-1 aggregate score 不能直接等同实验结合强度。", "Chai-1 方法卡和 claims 矩阵。", "supported"),
            ("项目池应同时记录证据、缺口和下一步实验。", "07_研究工作台/研究问题与项目池.md。", "supported"),
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Polish AI_MD online book chapters with protected-token rules.")
    parser.add_argument("--check", action="store_true", help="Check protected regions and overclaim terms without writing.")
    return parser.parse_args()


def split_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^## .+$", text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        heading = match.group(0).removeprefix("## ").strip()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[heading] = text[match.end() : end].strip("\n")
    return sections


def replace_section(text: str, heading: str, body: str) -> str:
    pattern = re.compile(rf"(?ms)^## {re.escape(heading)}\s*\n.*?(?=^## |\Z)")
    replacement = f"## {heading}\n\n{body.rstrip()}\n\n"
    if not pattern.search(text):
        raise ValueError(f"missing section {heading}")
    return pattern.sub(replacement, text, count=1)


def preserve_imagegen_block(existing_section: str, intro: str) -> str:
    marker = "### Imagegen 知识图谱"
    if marker not in existing_section:
        return intro
    _, block = existing_section.split(marker, 1)
    return f"{intro.rstrip()}\n\n{marker}\n\n{block.strip()}"


def polish_code_context(existing_section: str, spec: ChapterSpec) -> str:
    return re.sub(
        r"本节对应软件/界面：\*\*.*?\*\*。场景是：.*?\n",
        f"本节用于训练 **{spec.title}** 的最小复现意识。{spec.code_context}\n",
        existing_section,
        count=1,
    )


def render_intro(spec: ChapterSpec) -> str:
    return (
        f"{spec.problem}因此，本章首先界定这一问题场景，再说明需要记录哪些输入、动作、输出和质量控制信息。\n\n"
        f"{spec.task}这里的重点不是追求单个软件操作的完整覆盖，而是让读者形成可复查的判断链：对象是什么、依据来自哪里、结果能支持什么、仍然不能说明什么。\n\n"
        f"{spec.next_use}因此，本章的正文采用“概念定义 -> 流程执行 -> 边界判断 -> 下一步交接”的组织方式。"
    )


def render_objectives(spec: ChapterSpec) -> str:
    lines = ["完成本章后，读者应能够：", ""]
    lines.extend(f"- {item}" for item in spec.objectives)
    lines.append("")
    lines.append("这些目标既面向课堂学习，也面向后续研究记录；如果不能在记录中复述这些要点，相关结果不宜进入项目结论。")
    return "\n".join(lines)


def render_graph_entry(spec: ChapterSpec, existing_section: str) -> str:
    intro = (
        f"{spec.graph_entry}\n\n"
        "在线书籍页面只引用整理后的 wiki、方法卡、文献笔记和资源页，不直接嵌入原始 PDF 或课件图表。需要追溯来源时，应回到 `book/book_map.toml`、章节精读笔记和相关 Zotero/BibTeX 记录。\n\n"
        f"{render_source_table(spec)}"
    )
    return preserve_imagegen_block(existing_section, intro)


def load_book_map() -> dict:
    with BOOK_MAP_PATH.open("rb") as handle:
        return tomllib.load(handle)


def render_source_table(spec: ChapterSpec) -> str:
    data = load_book_map()
    entry = next((item for item in data.get("chapters", []) if item.get("slug") == spec.slug), {})
    fields = [
        ("章节来源", [entry.get("chapter_source", "")]),
        ("方法来源", entry.get("method_sources", [])),
        ("文献来源", entry.get("literature_sources", [])),
        ("实验来源", entry.get("experiment_sources", [])),
        ("工作台来源", entry.get("workbench_sources", [])),
    ]
    rows: list[str] = []
    for label, values in fields:
        clean_values = [str(value) for value in values if value]
        if clean_values:
            rows.append(f"| {label} | " + "<br>".join(f"`{value}`" for value in clean_values) + " |")
    if not rows:
        return "本章暂无额外来源路径；以 `book/book_map.toml` 为准。"
    return "| 来源类型 | 路径 |\n|:---|:---|\n" + "\n".join(rows)


def render_concepts(spec: ChapterSpec) -> str:
    rows = "\n".join(f"| {term} | {statement} |" for term, statement in spec.concepts)
    return (
        "本节只保留支撑后续判断的核心概念。每个概念都应能回答一个具体问题：它约束什么输入、影响什么输出、需要怎样记录。\n\n"
        "| 概念 | 教材化定义 |\n"
        "|:---|:---|\n"
        f"{rows}\n\n"
        "阅读本节时，应优先检查这些概念能否落到文件、参数、图像、表格或记录字段上。不能落地的说法，在后续研究写作中应作为背景描述，而不是证据。"
    )


def render_workflow(spec: ChapterSpec) -> str:
    rows = "\n".join(
        f"| {step} | {inp} | {action} | {out} | {qc} |"
        for step, inp, action, out, qc in spec.workflow
    )
    return (
        "本章流程按“输入 -> 动作 -> 输出 -> QC”的顺序组织。这样做的目的，是让每一步都能被复查，而不是只留下一个最终截图或分数。\n\n"
        "| 步骤 | 输入 | 动作 | 输出 | QC/边界 |\n"
        "|:---:|:---|:---|:---|:---|\n"
        f"{rows}\n\n"
        "执行时应先完成小样例或 dry-run，再扩大到批量任务。任何失败样本、低置信度结果或人工排除理由，都应保留在 manifest 或实验记录中。"
        f"{extra_teaching_note(spec)}"
    )


def extra_teaching_note(spec: ChapterSpec) -> str:
    notes = {
        "chapter-01": (
            "\n\n从教学角度看，本章的流程还承担一个基准作用：后续任何复杂模型输出，都必须能被还原到“输入文件、运行环境、命令参数、输出目录、人工判断”这五类信息。"
            "如果其中任一类信息缺失，读者可以先把该结果标为“记录不完整”，而不是急于讨论科学意义。"
            "这种处理方式看似保守，但能有效避免把路径错误、环境差异或临时文件覆盖误读为模型性能问题。"
            "\n\n在个人研究工作台中，本章对应的是“先建容器再运行”的习惯。每个任务都应有独立目录、输入清单、日志和简短说明；只有这样，后续章节中的结构图、score、轨迹、亲和力或设计候选才有明确上下文。"
            "如果一个结果不能回答“从哪里来、怎么跑、输出在哪里、谁判断过”四个问题，它就只能作为临时探索材料，不宜进入课件、综述或课题申请。"
            "这一规则也方便后续 AI Agent 接手，因为 Agent 可以先读取目录和日志，而不必从散乱文件中猜测任务状态。"
            "因此，本章的练习应被视为全书的通用检查表。"
            "后续每章只是在这一检查表上增加领域特定字段。"
            "读者完成本章后，应能独立判断一个计算任务是否具备继续分析的最低记录条件。"
            "这也是后续质量控制的起点。"
            "\n\n课堂练习中，建议把本章检查表反复用于不同软件场景，直到路径、环境和日志记录成为默认动作。"
            "这一习惯会降低后续章节的排错成本，也能让同一实验被他人复核。"
        ),
        "chapter-02": (
            "\n\n结构复核的核心不是把图做得更美观，而是让每个视觉判断都能回到来源和操作记录。"
            "读者在保存 PyMOL 或 ChimeraX 截图时，应同时记录结构 ID、链 ID、残基选择、视角命令和处理后的工作文件。"
            "这样第 3 章定义 docking box、第 4 章建立模拟体系或第 6 章设定设计约束时，才能判断当前结构是否适合作为输入。"
            "如果截图无法说明结构来自实验、预测还是人工处理版本，它就只能作为课堂示意图，不应作为研究判断依据。"
        ),
        "chapter-04": (
            "\n\nMD 结果的解释应先回答“轨迹是否可用”，再讨论“观察是否有意义”。"
            "读者需要把体系准备、平衡状态、采样长度、分析脚本和代表构象选择规则分开记录，避免用一张 RMSD 曲线覆盖所有判断。"
            "对于 AI 采样结果，也应记录输入结构、生成条件、筛选指标和人工复核理由。"
            "只有当这些信息能对应到具体文件和表格时，构象变化、接触频率或聚类代表结构才适合进入后续亲和力解释和研究假设。"
            "\n\n在课堂练习中，建议先让学生用同一份轨迹分别写出“QC 结论”和“科学假设”。"
            "前者关注模拟是否基本可用，后者关注可能的构象机制；两者分开后，读者更容易识别哪些判断仍需更长采样、重复模拟或实验验证。"
            "\n\n这一步也是进入第 5 章亲和力解释前的必要过滤。"
        ),
        "chapter-07": (
            "\n\n对 AI Agent 工作流而言，最容易被忽略的是“谁对结论负责”。Agent 可以执行检索、改写、生成脚本和运行测试，但它不能替代研究者确认科学含义。"
            "因此，每次让 Agent 修改知识库时，都应把任务拆成可审查对象：它读了哪些来源，改了哪些文件，保留了哪些引用，运行了哪些验证，哪些判断仍需作者确认。"
            "如果这些对象不能被列出，任务就不应进入自动化批处理。"
            "\n\n本章也为后续协作提供最低交接格式。一个完成良好的 Agent 任务，应至少留下文件 diff、验证命令、失败或跳过项、维护报告和下一步建议。"
            "这些材料比一次性聊天回答更重要，因为下一轮人工或 Agent 可以直接从它们恢复上下文。"
            "在 AI_MD 中，这一原则对应 `index.md`、`log.md`、`book/book_map.toml`、`tools/validate_online_book.py` 和 `tools/graph_health.py` 的联用。"
            "\n\n写作层面的 Agent 协作还需要额外边界。Agent 可以帮助重排段落、统一术语和检查过强表述，但不能凭空补充文献结论或实验事实。"
            "当正文涉及 docking score、predicted affinity、aggregate score 或蛋白设计候选时，Agent 应优先使用“提示”“支持”“仍需验证”等稳健表达，并把不确定项写入报告。"
            "这能让在线书籍保持教学可读性，同时不牺牲研究记录的可审查性。"
            "如果后续要把 Agent 生成内容用于公开教学或论文写作，还需要再经过人工核对、引用复查和版权边界检查。"
            "这种人机分工是本项目长期维护的基础。"
            "它也使每次更新都能回到同一套验收语言。"
            "读者应把本章视为项目协作协议，而不是单纯的软件使用说明。"
            "协议稳定，协作才可持续。"
            "后续任何自动化扩展都应先满足这一协议，再考虑效率提升。"
            "否则，自动化只会放大不可追溯的错误。"
            "这一点应作为全书的默认协作前提。"
            "因此，本章的验收重点不是工具数量，而是任务能否被下一位研究者完整复核。"
            "\n\n后续扩展在线教材时，本章的检查表应优先于任何单次生成速度。"
            "只有可复核的自动化，才适合沉淀为课程资源。"
        ),
    }
    return notes.get(spec.slug, "")


def render_exercises(spec: ChapterSpec) -> str:
    lines = ["本章练习强调可复查记录，而不是追求一次性完成复杂工具链。建议按以下顺序完成：", ""]
    lines.extend(f"{index}. {item}" for index, item in enumerate(spec.exercises, 1))
    lines.append("")
    lines.append("完成练习后，应能把结果写入 `04_实验记录/` 或 `07_研究工作台/` 的对应页面。不能写入记录的练习，只能算操作尝试。")
    return "\n".join(lines)


def render_boundaries(spec: ChapterSpec) -> str:
    rows = "\n".join(f"| {signal} | {safe} | {rule} |" for signal, safe, rule in spec.boundaries)
    return (
        "本节采用保守表述阶梯：预测、评分、可视化和文献案例通常只能写成“提示”“支持”或“可能一致”，除非有直接实验或严格验证，否则不写成“证明”。\n\n"
        "| 易误读对象 | 稳健表述 | 写作处理 |\n"
        "|:---|:---|:---|\n"
        f"{rows}\n\n"
        "写作时，如果一个结论只能由模型分数、单次截图或文献案例间接支持，应主动补上“仍需验证”“适用于该模型/该输入”“不等同于本项目结果”等边界。"
    )


def render_next_steps(spec: ChapterSpec) -> str:
    lines = ["完成本章后，建议按以下路径进入下一轮学习或研究任务：", ""]
    lines.extend(f"{index}. {item}" for index, item in enumerate(spec.next_steps, 1))
    lines.append("")
    lines.append("[返回首页](../index.md)。")
    return "\n".join(lines)


def protected_tokens(text: str) -> set[str]:
    tokens = set(PROTECTED_TOKEN_RE.findall(text))
    tokens.update(match.group(1) for match in IMAGE_TARGET_RE.finditer(text))
    tokens.update(REF_BLOCK_RE.findall(text))
    tokens.update(FENCED_BLOCK_RE.findall(text))
    return tokens


def strip_protected_regions(text: str) -> str:
    text = REF_BLOCK_RE.sub("", text)
    text = FENCED_BLOCK_RE.sub("", text)
    return text


def overclaim_hits(text: str) -> list[str]:
    scan = strip_protected_regions(text)
    terms = ["突破性", "革命性", "颠覆性", "决定性", "最佳", "全面揭示", "彻底阐明", "广泛适用", "普遍机制"]
    hits = []
    for term in terms:
        if term in scan:
            hits.append(term)
    # “证明” is acceptable only in explicit negation/boundary contexts.
    for match in re.finditer("证明", scan):
        context = scan[max(0, match.start() - 12) : match.end() + 12]
        if not any(neg in context for neg in ("不能", "不等于", "不写成", "不应", "除非")):
            hits.append(f"证明({context})")
    return hits


def polish_chapter(path: Path, spec: ChapterSpec, check_only: bool = False) -> tuple[bool, list[str]]:
    original = path.read_text(encoding="utf-8")
    original_tokens = protected_tokens(original)
    sections = split_sections(original)
    text = original
    text = replace_section(text, "本章导读", render_intro(spec))
    text = replace_section(text, "学习目标", render_objectives(spec))
    text = replace_section(text, "知识图谱入口", render_graph_entry(spec, sections["知识图谱入口"]))
    text = replace_section(text, "核心概念", render_concepts(spec))
    text = replace_section(text, "方法流程", render_workflow(spec))
    text = replace_section(text, "代码案例与软件操作", polish_code_context(sections["代码案例与软件操作"], spec))
    text = replace_section(text, "实验/练习入口", render_exercises(spec))
    text = replace_section(text, "使用边界与常见误读", render_boundaries(spec))
    text = replace_section(text, "延伸阅读与下一步", render_next_steps(spec))
    text = text.rstrip() + "\n"

    missing_tokens = sorted(token for token in original_tokens if token not in protected_tokens(text))
    hits = overclaim_hits(text)
    if missing_tokens:
        raise RuntimeError(f"{path.name} lost protected tokens: {missing_tokens[:10]}")
    if hits:
        raise RuntimeError(f"{path.name} has overclaim terms: {hits}")
    changed = text != original
    if changed and not check_only:
        path.write_text(text, encoding="utf-8")
    return changed, hits


def write_style_guide() -> None:
    RESOURCE_ROOT.mkdir(parents=True, exist_ok=True)
    content = """# P25 中文教材正文风格指南

本指南用于 AI_MD 在线书籍正文润色。它综合 `Research-Paper-Writing-Skills` 的段落功能、reverse outline、claim-evidence alignment，以及 `academic-chinese-style` 的中文生物医学写作边界。

## 适用范围

- 适用于 `book/docs/chapters/` 的教学正文、资源页说明和维护报告摘要。
- 不改写 `<!-- refs:start -->...<!-- refs:end -->` 内的自动引用列表，引用区由生成脚本统一维护。
- 不改写代码块、图片链接、DOI/URL、文件路径和 manifest 字段。

## 段落规则

- 每段只承担一个功能，第一句说明本段要解决的问题或判断。
- 教学段落优先采用“问题场景 -> 方法动作 -> 证据边界 -> 下一步”的顺序。
- 长流程用表格表达 `输入 | 动作 | 输出 | QC/边界`，不要把所有步骤塞进一个长段落。
- 章节结尾必须指向下一章、研究工作台或实验记录模板。

## 证据边界

| 证据强度 | 推荐动词 | 避免 |
|:---|:---|:---|
| 直接实验或严格验证 | 表明、证实、证明 | 无来源地使用 |
| 多来源一致模式 | 提示、支持、说明 | 写成决定性结论 |
| 模型预测或评分 | 可能提示、可作为排序线索 | 写成 Kd、IC50、结合强度或活性 |
| 文献案例/课程范文 | 可借鉴、可作为案例 | 写成本项目结果 |

## 术语与 provenance

- `docking score`、`predicted affinity`、`confidence`、`aggregate score`、`RFdiffusion/RFD3`、`ProteinMPNN`、`Chai-1` 保持术语一致。
- 章节正文不展示内部引用键或本地文献库条目编号；这些信息保留在 `references/` 元数据中，用于生成和 provenance 追踪。
- 原始 PDF 和补充材料只作为来源，不直接复制图表到在线书籍。

## P25 来源

- `Research-Paper-Writing-Skills`，commit `9ee5eddc10068cc52590b3a68a827d3a387f5af9`。
- `luvega/codex-skills` 的 `academic-chinese-style`，commit `e7088ef3f476d4ea5720ea56cc72bc8a1cd6eea0`。
"""
    (RESOURCE_ROOT / "style-guide.md").write_text(content, encoding="utf-8")


def write_report(changed: list[str]) -> None:
    lines = [
        "# P25 正文润色报告",
        "",
        "本报告记录 8 个主章节的 reverse outline、claim-evidence map 和未改动边界。P25 只处理在线书籍正文，不新增科学事实，不改原始素材，不重做图像。",
        "",
        "## 未改动边界",
        "",
        "- `<!-- refs:start -->...<!-- refs:end -->` 引用列表保持由 `tools/update_book_references.py` 生成。",
        "- 代码块、图片链接、DOI/URL、代码文件名和 manifest 字段原样保留。",
        "- 章节正文不展示内部引用键或本地文献库条目编号；引用元数据继续保留在 `references/` 层。",
        "- 未跟踪的 `06_原始学习素材/*.torrent` 文件未纳入本轮处理。",
        "",
        "## 修改文件",
        "",
    ]
    lines.extend(f"- `{name}`" for name in changed)
    lines.append("")
    for spec in CHAPTERS:
        lines.extend([f"## {spec.title}", "", "### Reverse Outline", ""])
        lines.extend(
            [
                "| 区块 | 段落功能 | 核心判断 | 边界提示 |",
                "|:---|:---|:---|:---|",
                *[f"| {section} | {role} | {claim} | {boundary} |" for section, role, claim, boundary in spec.reverse_outline],
                "",
                "### Claim-Evidence Map",
                "",
                "| Claim | Evidence | Status |",
                "|:---|:---|:---|",
                *[f"| {claim} | {evidence} | {status} |" for claim, evidence, status in spec.claims],
                "",
                "### 需作者确认",
                "",
                "- 当前为教材化和学术化语言调整，未新增实验结果；后续如果加入真实运行截图或生产级实验结果，需要回到 `04_实验记录/` 补 provenance。",
                "",
            ]
        )
    (RESOURCE_ROOT / "polish-report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    changed: list[str] = []
    processed = [f"book/docs/chapters/{spec.slug}.md" for spec in CHAPTERS]
    for spec in CHAPTERS:
        path = CHAPTER_ROOT / f"{spec.slug}.md"
        did_change, _ = polish_chapter(path, spec, check_only=args.check)
        if did_change:
            changed.append(path.relative_to(ROOT).as_posix())
    if not args.check:
        write_style_guide()
        write_report(processed)
    print(f"changed: {len(changed)}")
    for name in changed:
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
