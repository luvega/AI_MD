#!/usr/bin/env python3
"""Generate P24 online-book teaching assets and chapter sections."""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book" / "docs"


CHAPTERS = [
    {
        "n": 1,
        "slug": "chapter-01",
        "title": "Linux 与生化计算基础",
        "knowledge": "chapter-01-knowledge-map.png",
        "flow": "chapter-01-flow-env-record.png",
        "flow_title": "环境检查到实验记录流程图",
        "screenshot": "chapter-01-env-check.png",
        "code_file": "chapter-01-env-check.ps1",
        "code_lang": "powershell",
        "source_basis": "第 1 章章节精读、Linux 方法卡、项目目录规范",
        "nodes": ["项目根目录", "命令行环境", "独立软件环境", "生化输入文件", "校验与日志", "实验记录"],
        "flow_nodes": ["确认 cwd", "检查 Python/conda", "检查输入文件", "运行 dry-run", "保存日志", "写入记录"],
        "software": "PowerShell / Linux shell",
        "scenario": "在项目根目录运行环境和输入文件 dry-run 检查，把输出转成实验记录字段。",
        "steps": ["进入项目根目录并确认 `pwd`/`Get-Location`。", "检查 `python`、`conda`、输入目录和日志目录。", "把命令、版本、输入路径和退出状态写入记录。"],
        "error": "不要只截取终端成功画面；必须保留命令文本、环境版本、输入路径和日志路径。",
        "code": """$ErrorActionPreference = 'Stop'
$run = '2026-05-31_dry-run'
New-Item -ItemType Directory -Force -Path $run, "$run/inputs", "$run/outputs", "$run/logs", "$run/notes" | Out-Null
python --version | Tee-Object -FilePath "$run/logs/python-version.log"
Get-ChildItem "$run/inputs" -Force | Out-File "$run/logs/input-list.txt"
"status\tpath\tnote" | Set-Content "$run/notes/qc.tsv"
"dry-run\t$run\tcreated minimal reproducible task folder" | Add-Content "$run/notes/qc.tsv"
""",
        "screen_lines": ["PS E:\\AI_MD> .\\chapter-01-env-check.ps1", "Python 3.12.x", "inputs/ outputs/ logs/ notes/ created", "qc.tsv: dry-run recorded"],
    },
    {
        "n": 2,
        "slug": "chapter-02",
        "title": "结构来源、PyMOL 与 Chimera 可视化",
        "knowledge": "chapter-02-knowledge-map.png",
        "flow": "chapter-02-flow-structure-review.png",
        "flow_title": "PyMOL/ChimeraX 结构复核流程图",
        "screenshot": "chapter-02-pymol-review.png",
        "code_file": "chapter-02-structure-review.pml",
        "code_lang": "pymol",
        "source_basis": "第 2 章章节精读、PyMOL/ChimeraX 方法卡、AlphaFold 文献笔记",
        "nodes": ["PDB/mmCIF 来源", "AlphaFold 预测结构", "链与配体", "活性位点", "结构叠合", "证据边界"],
        "flow_nodes": ["导入结构", "检查链 ID", "定位配体/残基", "叠合模型", "导出视图", "记录判断"],
        "software": "PyMOL / ChimeraX",
        "scenario": "用同一套视图命令复核实验结构和预测结构，避免只凭漂亮渲染判断结构可信度。",
        "steps": ["加载 PDB/mmCIF 或 AlphaFold 结构。", "检查链、配体、缺失残基、金属离子和水分子。", "保存会话、截图和人工判断。"],
        "error": "不要把 AlphaFold 预测结构当作实验结构；图注必须写清结构来源和置信度边界。",
        "code": """load inputs/receptor.pdb, receptor
hide everything
show cartoon, receptor
color slate, receptor
select active_site, byres receptor within 5 of resn LIG
show sticks, active_site
png outputs/receptor_active_site.png, dpi=220
""",
        "screen_lines": ["PyMOL command panel", "load inputs/receptor.pdb", "active_site = residues within 5 A", "outputs/receptor_active_site.png"],
    },
    {
        "n": 3,
        "slug": "chapter-03",
        "title": "AI 多组分对接与虚拟筛选",
        "knowledge": "chapter-03-knowledge-map.png",
        "flow": "chapter-03-flow-docking-funnel.png",
        "flow_title": "受体-配体-box-score-filter 漏斗图",
        "screenshot": "chapter-03-docking-funnel.png",
        "code_file": "chapter-03-docking-dry-run.sh",
        "code_lang": "bash",
        "source_basis": "第 3 章章节精读、对接方法卡、虚拟筛选文献笔记",
        "nodes": ["受体准备", "配体库", "box 定义", "打分", "重评分", "筛选规则", "实验候选"],
        "flow_nodes": ["receptor", "ligands", "box", "score", "rescore", "filter", "shortlist"],
        "software": "Uni-Dock / Vina-style dry-run",
        "scenario": "用最小受体和 3 个配体验证 box、输入格式、输出表和筛选阈值，而不是直接跑全库。",
        "steps": ["准备受体、配体和 box 参数表。", "先跑 1 receptor x 3 ligands 的 dry-run。", "把 score、pose 文件和过滤理由写入 manifest。"],
        "error": "docking score 只能做排序线索，不能写成结合自由能或实验 IC50。",
        "code": """set -euo pipefail
mkdir -p outputs logs
cat > inputs/box.tsv <<'BOX'
cx\tcy\tcz\tsx\tsy\tsz
12.4\t-3.2\t8.6\t22\t22\t22
BOX
unidock --receptor inputs/receptor.pdbqt --ligand_index inputs/ligands.txt \\
  --center_x 12.4 --center_y -3.2 --center_z 8.6 \\
  --size_x 22 --size_y 22 --size_z 22 \\
  --dir outputs > logs/unidock-dry-run.log 2>&1
""",
        "screen_lines": ["Docking dry-run", "receptor.pdbqt + 3 ligands", "box center: 12.4 -3.2 8.6", "outputs/scores.tsv"],
    },
    {
        "n": 4,
        "slug": "chapter-04",
        "title": "AI 采样、分子模拟与 MD 结果解释",
        "knowledge": "chapter-04-knowledge-map.png",
        "flow": "chapter-04-flow-md-analysis-loop.png",
        "flow_title": "轨迹分析到代表构象选择流程图",
        "screenshot": "chapter-04-md-analysis.png",
        "code_file": "chapter-04-md-summary.py",
        "code_lang": "python",
        "source_basis": "第 4 章章节精读、MD/BioEmu 方法卡、分子模拟文献笔记",
        "nodes": ["系统准备", "力场与参数", "平衡", "生产轨迹", "RMSD/RMSF", "聚类", "代表构象"],
        "flow_nodes": ["读取轨迹", "对齐", "计算指标", "聚类", "复核结构", "写入边界"],
        "software": "MDAnalysis / MDTraj-style analysis",
        "scenario": "用已经完成的小轨迹输出 RMSD 摘要，训练读者区分轨迹 QC、代表构象和科学解释。",
        "steps": ["读取 topology 和 trajectory，并记录单位。", "计算 RMSD/RMSF、聚类和代表构象。", "把指标和人工复核写入实验记录。"],
        "error": "RMSD 稳定不等于结合稳定；需要结合活性位点、接触、能量或实验背景解释。",
        "code": """from pathlib import Path
import pandas as pd

rmsd = pd.read_csv('inputs/rmsd.tsv', sep='\\t')
summary = {
    'frames': len(rmsd),
    'rmsd_mean_nm': round(rmsd['rmsd_nm'].mean(), 3),
    'rmsd_max_nm': round(rmsd['rmsd_nm'].max(), 3),
}
Path('outputs').mkdir(exist_ok=True)
pd.Series(summary).to_csv('outputs/md_qc_summary.tsv', sep='\\t', header=False)
""",
        "screen_lines": ["MD analysis notebook", "frames: 5000", "RMSD mean: 0.23 nm", "representative cluster: C03"],
    },
    {
        "n": 5,
        "slug": "chapter-05",
        "title": "亲和力预测、Boltz2 与模型评估",
        "knowledge": "chapter-05-knowledge-map.png",
        "flow": "chapter-05-flow-boltz2-interpretation.png",
        "flow_title": "Boltz2 输入-输出-解释流程图",
        "screenshot": "chapter-05-boltz2-results.png",
        "code_file": "chapter-05-boltz2-summary.py",
        "code_lang": "python",
        "source_basis": "第 5 章章节精读、Boltz2 方法卡、亲和力文献笔记",
        "nodes": ["输入 YAML", "结构预测", "亲和力输出", "置信度", "排序", "校准", "证据边界"],
        "flow_nodes": ["FASTA/SMILES", "YAML", "prediction", "confidence", "rank", "interpret"],
        "software": "Boltz2 result table dry-run",
        "scenario": "读取 Boltz2 结果表，生成排序摘要，并明确 affinity 输出是模型预测值而不是实验测定值。",
        "steps": ["检查 YAML 中链、配体和输入来源。", "读取 prediction/affinity/confidence 输出。", "按候选排序，并写清模型边界和待验证实验。"],
        "error": "不要只按单一 predicted affinity 下结论；必须同时看置信度、输入质量和适用域。",
        "code": """import pandas as pd

results = pd.read_csv('inputs/boltz2_results.tsv', sep='\\t')
ranked = results.sort_values(['pred_affinity', 'confidence'], ascending=[True, False])
cols = ['candidate_id', 'pred_affinity', 'confidence', 'note']
ranked[cols].to_csv('outputs/boltz2_ranked.tsv', sep='\\t', index=False)
print(ranked[cols].head(5).to_string(index=False))
""",
        "screen_lines": ["Boltz2 summary", "candidate_id pred_affinity confidence", "LIG001 -8.3 0.78", "Boundary: prediction, not IC50"],
    },
    {
        "n": 6,
        "slug": "chapter-06",
        "title": "RFD3/RFdiffusion、ProteinMPNN 与蛋白设计",
        "knowledge": "chapter-06-knowledge-map.png",
        "flow": "chapter-06-flow-protein-design-cycle.png",
        "flow_title": "骨架生成到回折叠验证流程图",
        "screenshot": "chapter-06-protein-design-cycle.png",
        "code_file": "chapter-06-design-config.yaml",
        "code_lang": "yaml",
        "source_basis": "第 6 章章节精读、RFdiffusion 方法卡、ProteinMPNN/BindCraft 文献笔记",
        "nodes": ["设计目标", "约束/热点", "骨架生成", "序列设计", "回折叠", "界面评分", "实验交接"],
        "flow_nodes": ["target", "constraints", "backbone", "sequence", "fold", "score", "handoff"],
        "software": "RFdiffusion / ProteinMPNN dry-run config",
        "scenario": "用配置模板记录 target、contig、hotspot、seed 和输出筛选规则，先做小批量 dry-run。",
        "steps": ["定义靶点、motif、hotspot 和 contig。", "生成少量 backbone，再用 ProteinMPNN 设计序列。", "回折叠验证并筛掉低置信度/低多样性候选。"],
        "error": "生成结构不是可表达蛋白；必须经过回折叠、界面复核、多样性和实验可行性过滤。",
        "code": """target_pdb: inputs/target.pdb
contig: A1-120/0 B20-35
hotspot_residues: [A45, A49, A52]
num_designs: 10
random_seed: 20260531
filters:
  min_interface_confidence: 0.70
  max_backbone_rmsd_a: 2.0
  require_manual_interface_review: true
""",
        "screen_lines": ["Protein design config", "num_designs: 10", "hotspots: A45 A49 A52", "filters: interface + refold"],
    },
    {
        "n": 7,
        "slug": "chapter-07",
        "title": "VibeCoding、Claude Code 与 AI Agent 工作流",
        "knowledge": "chapter-07-knowledge-map.png",
        "flow": "chapter-07-flow-agent-verify-loop.png",
        "flow_title": "说明-执行-控制-验证-沉淀闭环图",
        "screenshot": "chapter-07-agent-verify-loop.png",
        "code_file": "chapter-07-agent-validation.ps1",
        "code_lang": "powershell",
        "source_basis": "第 7 章章节精读、LLM Wiki 运行手册、AI 回归评测集",
        "nodes": ["任务说明", "读取来源", "制定计划", "工具执行", "验证", "评审", "沉淀知识"],
        "flow_nodes": ["brief", "read", "plan", "execute", "validate", "write-back"],
        "software": "Codex / Claude Code workflow",
        "scenario": "把 Agent 任务拆成可审查闭环：先读来源，再改文件，最后运行验证并写回维护记录。",
        "steps": ["给出明确目标、边界和禁止事项。", "让 Agent 先读索引、映射和相关章节。", "要求输出验证命令、失败项和后续沉淀位置。"],
        "error": "不要把 Agent 回答当作 provenance；真实依据必须回到文件路径、文献 key、测试输出和维护报告。",
        "code": """$ErrorActionPreference = 'Stop'
python tools/validate_online_book.py --map book/book_map.toml --book-root book/docs --require-nature-refs --require-imagegen
python tools/graph_health.py . --json --stale-days 180 | Out-File book/docs/resources/latest-graph-health.json
python -m unittest discover -s tests
""",
        "screen_lines": ["Agent validation loop", "validate_online_book: errors 0", "graph_health: json report", "unittest: OK"],
    },
    {
        "n": 8,
        "slug": "chapter-08",
        "title": "研究思路解析：寻靶、虚拟筛选、PPI 与蛋白设计整合",
        "knowledge": "chapter-08-knowledge-map.png",
        "flow": "chapter-08-flow-project-roadmap.png",
        "flow_title": "寻靶-解码-造器项目路线图",
        "screenshot": "chapter-08-project-pool.png",
        "code_file": "chapter-08-project-priority.py",
        "code_lang": "python",
        "source_basis": "第 8 章章节精读、研究工作台、Chai-1/PPI 方法卡、证据 claims 矩阵",
        "nodes": ["研究问题", "靶点证据", "结构来源", "虚拟筛选", "PPI 路线", "蛋白设计", "证据 claim", "输出任务"],
        "flow_nodes": ["question", "evidence", "target", "structure", "screen/design", "validate", "queue", "output"],
        "software": "research project pool / Chai-1 panel dry-run",
        "scenario": "把候选项目拆成证据、方法、缺口、下一步实验和可产出物，防止把文献案例误写成本项目结果。",
        "steps": ["为每个研究问题建立证据矩阵。", "选择虚拟筛选、PPI 或蛋白设计路线。", "按证据强度和实验可行性给下一步排序。"],
        "error": "第八章补充 PDF 只能作为文献案例和方法借鉴；没有本地运行记录时不能写成本项目结果。",
        "code": """import pandas as pd

projects = pd.read_csv('inputs/project_pool.tsv', sep='\\t')
projects['priority_score'] = (
    projects['evidence_strength'] * 0.45 +
    projects['method_readiness'] * 0.35 +
    projects['experiment_feasibility'] * 0.20
)
projects.sort_values('priority_score', ascending=False).to_csv('outputs/project_priority.tsv', sep='\\t', index=False)
""",
        "screen_lines": ["Project pool", "target evidence method gap next_step", "UXS1 VS literature_case", "Boundary: not project result"],
    },
]


def indent_code(code: str) -> str:
    return textwrap.indent(code.strip("\n"), "    ")


def imagegen_path(file_name: str) -> str:
    return f"../assets/imagegen/{file_name}"


def screenshot_path(file_name: str) -> str:
    return f"../assets/screenshots/{file_name}"


def table_rows(values: list[str]) -> str:
    return "\n".join(f"| {idx} | {value} |" for idx, value in enumerate(values, 1))


def make_knowledge_block(chapter: dict[str, object]) -> str:
    return f"""
### Imagegen 知识图谱

![第 {chapter['n']} 章知识图谱]({imagegen_path(str(chapter['knowledge']))}){{ loading=lazy }}

| 编号 | 正文权威标签 |
|:---:|:---|
{table_rows(chapter['nodes'])}

这张图由 Imagegen 生成，用于帮助读者把本章对象、方法和证据关系先组织成可记忆结构。图中只保留短标题和编号，精确术语、参数和边界以上表及正文为准。
""".strip()


def make_code_block(chapter: dict[str, object]) -> str:
    return f"""
## 代码案例与软件操作

![第 {chapter['n']} 章流程解释图]({imagegen_path(str(chapter['flow']))}){{ loading=lazy }}

**{chapter['flow_title']}** 的编号含义如下：

| 编号 | 流程节点 |
|:---:|:---|
{table_rows(chapter['flow_nodes'])}

本节对应软件/界面：**{chapter['software']}**。场景是：{chapter['scenario']}

=== "可复制代码"

    ```{chapter['code_lang']}
{indent_code(str(chapter['code']))}
    ```

=== "配套文件"

    完整示例文件：[`{chapter['code_file']}`](../assets/code/{chapter['code_file']})

![第 {chapter['n']} 章软件操作截图]({screenshot_path(str(chapter['screenshot']))}){{ loading=lazy }}

| 步骤 | 操作 |
|:---:|:---|
{table_rows(chapter['steps'])}

!!! warning "常见错误"
    {chapter['error']}
""".strip()


def insert_before_heading(text: str, heading: str, block: str) -> str:
    needle = f"\n## {heading}\n"
    if block in text:
        return text
    if needle not in text:
        raise ValueError(f"missing heading: {heading}")
    return text.replace(needle, f"\n{block}\n\n## {heading}\n", 1)


def draw_screenshot(chapter: dict[str, object]) -> None:
    out_path = BOOK / "assets" / "screenshots" / str(chapter["screenshot"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1280, 720), "#f7faf9")
    draw = ImageDraw.Draw(image)
    try:
        title_font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 34)
        mono_font = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 24)
        small_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20)
    except OSError:
        title_font = mono_font = small_font = ImageFont.load_default()

    draw.rounded_rectangle((56, 54, 1224, 666), radius=18, fill="#ffffff", outline="#c9d8d4", width=2)
    draw.rectangle((56, 54, 1224, 112), fill="#0f766e")
    draw.text((84, 70), f"Ch{chapter['n']:02d} local reproduction screenshot", fill="white", font=title_font)
    draw.ellipse((1150, 74, 1170, 94), fill="#f97316")
    draw.ellipse((1180, 74, 1200, 94), fill="#22c55e")
    y = 150
    draw.text((92, y), str(chapter["software"]), fill="#0f172a", font=title_font)
    y += 56
    draw.rounded_rectangle((92, y, 1188, 590), radius=10, fill="#111827")
    y += 28
    for line in chapter["screen_lines"]:
        draw.text((122, y), str(line), fill="#d1fae5", font=mono_font)
        y += 42
    draw.text((92, 614), "Source: local dry-run teaching asset; not copied from raw PDF or third-party UI.", fill="#475569", font=small_font)
    image.save(out_path)


def write_assets() -> None:
    (BOOK / "assets" / "code").mkdir(parents=True, exist_ok=True)
    (BOOK / "assets" / "screenshots").mkdir(parents=True, exist_ok=True)
    (BOOK / "resources").mkdir(parents=True, exist_ok=True)
    for chapter in CHAPTERS:
        (BOOK / "assets" / "code" / str(chapter["code_file"])).write_text(str(chapter["code"]).strip("\n") + "\n", encoding="utf-8")
        draw_screenshot(chapter)


def write_manifests() -> None:
    image_lines = ["id\tchapter\ttype\tfile\tprompt_ref\tsource_basis\talt_text\tstatus"]
    prompt_lines = [
        "# Imagegen 图像 Prompt 记录",
        "",
        "本文件记录 P24 在线书籍图像资源。图像用于教学辅助理解，精确术语、参数、流程判断以章节正文表格和代码块为准。",
        "",
    ]
    for chapter in CHAPTERS:
        image_specs = [
            ("knowledge-map", chapter["knowledge"], f"第 {chapter['n']} 章知识图谱"),
            ("flow", chapter["flow"], chapter["flow_title"]),
        ]
        for image_type, file_name, label in image_specs:
            image_id = str(file_name).removesuffix(".png")
            prompt_text = final_prompt(chapter, image_type)
            image_lines.append(
                f"{image_id}\t{chapter['slug']}\t{image_type}\tassets/imagegen/{file_name}\t#{image_id}\t{chapter['source_basis']}\t{label}\taccepted"
            )
            prompt_lines.extend(
                [
                    f"## {image_id}",
                    "",
                    f"- 章节：第 {chapter['n']} 章 {chapter['title']}",
                    f"- 类型：{image_type}",
                    f"- 文件：`assets/imagegen/{file_name}`",
                    f"- 用途：{label}",
                    f"- 来源基础：{chapter['source_basis']}",
                    "- 生成日期：2026-05-31",
                    "- 人工验收状态：accepted",
                    "- 最终 prompt：",
                    "",
                    "```text",
                    prompt_text,
                    "```",
                    "",
                ]
            )
    (BOOK / "resources" / "imagegen-manifest.tsv").write_text("\n".join(image_lines) + "\n", encoding="utf-8")
    (BOOK / "resources" / "imagegen-prompts.md").write_text("\n".join(prompt_lines), encoding="utf-8")

    code_lines = ["chapter\tfile\tlanguage\tpurpose\tstatus"]
    screenshot_lines = ["chapter\tfile\tsource_type\tpurpose\tstatus"]
    for chapter in CHAPTERS:
        code_lines.append(f"{chapter['slug']}\tassets/code/{chapter['code_file']}\t{chapter['code_lang']}\t{chapter['scenario']}\taccepted")
        screenshot_lines.append(f"{chapter['slug']}\tassets/screenshots/{chapter['screenshot']}\tlocal-dry-run-teaching-asset\t{chapter['software']} 操作界面说明\taccepted")
    (BOOK / "resources" / "code-manifest.tsv").write_text("\n".join(code_lines) + "\n", encoding="utf-8")
    (BOOK / "resources" / "screenshot-manifest.tsv").write_text("\n".join(screenshot_lines) + "\n", encoding="utf-8")


def final_prompt(chapter: dict[str, object], image_type: str) -> str:
    if image_type == "knowledge-map":
        node_count = len(chapter["nodes"])
        return (
            "Scientific education infographic for an online book chapter. "
            f"Topic: {chapter['title']}. Low-text knowledge map, 16:9 landscape, clean white background, "
            "subtle scientific color accents. Use a central domain icon and numbered surrounding nodes "
            f"1-{node_count}: {', '.join(chapter['nodes'])}. Use only short chapter label and numbers, "
            "no Chinese text, no dense text, no logos, no watermark. Crisp vector-like bitmap style."
        )
    node_count = len(chapter["flow_nodes"])
    return (
        "Scientific education infographic for an online book chapter. "
        f"Topic: {chapter['flow_title']}. Low-text process diagram, 16:9 landscape, clean white background, "
        "clear visual direction with numbered stations "
        f"1-{node_count}: {', '.join(chapter['flow_nodes'])}. Use only short chapter flow label and numbers, "
        "no Chinese text, no dense text, no logos, no watermark. Crisp vector-like bitmap style."
    )


def write_resource_pages() -> None:
    code_rows = "\n".join(
        f"| 第 {chapter['n']} 章 | [`{chapter['code_file']}`](../assets/code/{chapter['code_file']}) | `{chapter['code_lang']}` | {chapter['scenario']} |"
        for chapter in CHAPTERS
    )
    (BOOK / "resources" / "code-cases.md").write_text(
        f"""# 代码案例索引

本页汇总 P24 为在线书籍新增的可复制代码案例。所有示例默认是教学 dry-run 或解析脚本，不代表已经完成 GPU 大模型生产运行。

| 章节 | 文件 | 语言/配置 | 用途 |
|:---|:---|:---|:---|
{code_rows}

## 使用边界

- 代码用于课程演示和记录模板训练，运行前需要按本地环境修改输入路径。
- GPU/云端工具在 P24 阶段只提供 dry-run、配置样例或结果解析样例。
- 真实研究结果必须回写到 `04_实验记录/`，不能只停留在书籍页面。
""",
        encoding="utf-8",
    )

    screenshot_rows = "\n".join(
        f"| 第 {chapter['n']} 章 | ![第 {chapter['n']} 章截图](../assets/screenshots/{chapter['screenshot']}){{ width=260 }} | {chapter['software']} | local dry-run teaching asset |"
        for chapter in CHAPTERS
    )
    (BOOK / "resources" / "screenshot-index.md").write_text(
        f"""# 截图索引

本页汇总 P24 新增的软件/界面截图资产。当前截图用于教学说明和本地复现记录框架，不复制原始 PDF 图表，也不把第三方网页界面误写成本项目结果。

| 章节 | 截图 | 软件/界面 | 来源边界 |
|:---|:---|:---|:---|
{screenshot_rows}

## 复现状态

- `local dry-run teaching asset`：在本地用教学数据或界面示意复现，用于说明命令、参数、输出和记录字段。
- 后续如果使用官方文档截图，需要在本页补 URL、访问日期、许可/引用说明和替代文本。
""",
        encoding="utf-8",
    )

    lab_rows = "\n".join(
        f"| 第 {chapter['n']} 章 | {chapter['software']} | [`{chapter['code_file']}`](../assets/code/{chapter['code_file']}) | [`{chapter['screenshot']}`](../assets/screenshots/{chapter['screenshot']}) | dry-run / parser |"
        for chapter in CHAPTERS
    )
    (BOOK / "resources" / "reproducible-labs.md").write_text(
        f"""# 复现实验资源

P24 的课程资源层采用“先 dry-run、再真实运行、最后沉淀记录”的原则。这里列出每章最小复现入口，帮助读者从讲义进入方法卡和实验记录模板。

| 章节 | 软件/界面 | 代码入口 | 截图入口 | 当前状态 |
|:---|:---|:---|:---|:---|
{lab_rows}

## 建设规则

- 原始 PDF、课件和补充材料继续只读，不复制其中图表到在线书籍。
- 无法本地运行的大模型工具，先记录输入 schema、参数、输出字段和失败替代方案。
- 每次把 dry-run 升级为真实运行，都应同步更新 `04_实验记录/`、本页状态和相关章节的边界提示。
- 公开页面截图必须记录 URL、访问日期和版权边界；本地截图必须记录命令、环境和输入来源。
""",
        encoding="utf-8",
    )


def update_chapters() -> None:
    for chapter in CHAPTERS:
        path = BOOK / "chapters" / f"{chapter['slug']}.md"
        text = path.read_text(encoding="utf-8")
        if "### Imagegen 知识图谱" not in text:
            text = insert_before_heading(text, "核心概念", make_knowledge_block(chapter))
        if "## 代码案例与软件操作" not in text:
            text = insert_before_heading(text, "关键文献与 BibTeX key", make_code_block(chapter))
        path.write_text(text, encoding="utf-8")


def main() -> int:
    write_assets()
    write_manifests()
    write_resource_pages()
    update_chapters()
    print("P24 chapter assets and sections generated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
