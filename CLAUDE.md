# CLAUDE.md

这个文件规定 Claude Code / Codex 在 `AI_MD` 学术知识库里的工作方式。

## 用途和背景

这是一位药物化学方向副教授的个人学术知识库，用来整理 AI 辅助药物设计课程资料、方法笔记、文献笔记、运行结果和后续研究想法。

我的简要背景：

- 副教授，药物化学方向。
- 研究方向：AI 辅助药物设计、多肽药物设计、分子建模、分子对接、分子动力学模拟、亲和力预测和蛋白设计。
- 当前主要课题：AI 辅助的分子建模、对接、分子动力学模拟、亲和力预测、蛋白/多肽设计及其在药物化学研究中的落地。
- 写作风格：自然流畅的中文，条列式，简洁直接，严谨的学术风格。
- 如需更完整的项目背景，先读 `00_项目说明/项目背景.md`。

这个项目是 AI 辅助分子建模、对接、分子模拟、亲和力预测和蛋白设计课程资料库。PDF 课件原件统一放入本地 `06_原始学习素材/`；该目录内容不上传 GitHub，Git 只保留空目录占位 `.gitkeep`。压缩包、脚本、表格和网页实验等非 PDF 原始资料保留在原章节目录或本地 raw 目录，新增 Markdown 文件负责索引、说明、方法笔记、文献笔记和实验记录。

- 主要用途：把课程资料、运行结果和 Zotero 文献连接成可检索、可复用、可继续扩展的 AI 原生知识库和 LLM Wiki 第二大脑。
- 当前资料：第一章到第八章课程 PDF/课件提取、第三章对接资料、第四章 MD/BioEmu/GROMACS/力场补充资料、第五章 Boltz2/亲和力/QM-MM/蒙特卡洛资料、第六章 RFD3/RFdiffusion 蛋白设计资料、第七章 VibeCoding/Claude Code 工具链资料、第八章计算思路解析、正向虚拟筛选、Chai-1 互作蛋白虚拟筛选和蛋白设计补充资料。
- Zotero 联动策略：只记录元数据、Zotero item key 和 BibTeX key，不批量复制 Zotero PDF。

## LLM Wiki Agent 架构

本项目采用 Karpathy LLM Wiki 模式的混合落地：

| 层 | 本项目位置 | 规则 |
|:---|:---|:---|
| Raw sources | 本地 `06_原始学习素材/`、`references/` | 原始资料是 source of truth，默认只读；`06_原始学习素材/` 内容不上传 GitHub |
| Wiki | `index.md`、`log.md`、`00_项目说明/`、`01_课程章节索引/`、`02_方法笔记/`、`03_文献笔记/`、`04_实验记录/`、`05_附件索引/`、`07_研究工作台/`、`book/docs/` | LLM 负责创建、更新、交叉引用和维护一致性 |
| Schema | `CLAUDE.md`、历史项目规则 `.claude/skills/`、全局 Codex skills、`00_项目说明/LLM Wiki运行手册.md`、`tools/graph_health.py`、`tools/validate_online_book.py`、`book/book_map.toml` | 约束 Agent 如何 ingest、query、lint、update 和验收 |

LLM Wiki Agent 是总调度器。`takenote` 负责写入知识，`update-vault` 负责验收知识库，`zotero-literature-link` 负责文献映射，`ingest-source`、`query-wiki`、`wiki-lint` 负责 LLM Wiki 层面的摄入、问答和健康检查。

## 目录结构

- `00_项目说明/`：项目背景、章节地图、使用说明和维护报告。
- `01_课程章节索引/`：第一章到第八章资料索引；`章节精读/` 保存第 1-8 章结构化精读笔记。
- `02_方法笔记/`：Linux/PyMOL/Chimera/对接/MSA/MD/BioEmu/Boltz2/RFdiffusion 等方法卡片。
- `03_文献笔记/`：从 Zotero 生成或链接的核心论文笔记。
- `04_实验记录/`：Boltz2 结果、QM-MM、蒙特卡洛和后续运行记录。
- `05_附件索引/`：压缩包、网盘链接、PDF、表格、脚本、JSON、CIF、TSV 等附件清单。
- `06_原始学习素材/`：本地集中保存 PDF 课件原件、重复 PDF 待确认区、逐页全文提取结果和低文本页 OCR 补充结果；GitHub 只保留 `.gitkeep` 占位，不上传目录内容。
- `07_研究工作台/`：知识图谱实体索引、证据与 claims 矩阵、个人研究问题/项目池、阅读队列、实验队列、输出视图和 AI 回归评测集。
- `book/`：MkDocs Material 在线书籍工程；`book/docs/` 是课程讲义页面，`book/book_map.toml` 是章节到 wiki 来源和 BibTeX key 的映射；`book/docs/resources/` 保存代码案例、截图索引、Imagegen prompt、复现实验资源、正文风格指南和润色报告。
- `references/`：`references.bib` 和 `zotero-map.tsv`。
- `tools/`：项目级体检和维护脚本；当前包含 `graph_health.py` 和 `validate_online_book.py`。
- `tests/`：项目级脚本测试；当前包含 `test_graph_health.py` 和 `test_validate_online_book.py`。
- `index.md`：LLM Wiki 内容型总索引。
- `log.md`：追加式操作时间线。
- `.claude/skills/`：历史项目内知识库规则来源；P27 已将这些规则生成并安装为 `ai-md-*` 全局 Codex skills。该目录保留用于兼容既有文档，但不再作为第三方 skill 的新增安装位置。

## 每次输入内容时的处理顺序

1. 分析主题、关键词、资料类型和可能对应章节。
2. 先读本文件；如果涉及项目边界、用户背景或资料组织，再读 `index.md`、`00_项目说明/项目背景.md` 和 `00_项目说明/知识库使用说明.md`。
3. 如果任务宽泛或跨模块，先读 `00_项目说明/插件与Skills调用说明.md`，用 `ai-md-router` 决定最小必要插件和 skill。
4. 进入相关子文件夹读取 `_index.md`，再读具体笔记；不要跳过索引直接猜文件。
5. 判断是新建还是更新；如果目标不明确或会改变原始资料位置，先问我。
6. 需要文献支撑时，优先查 `references/zotero-map.tsv` 和 `references/references.bib`；必要时再用 Zotero 检索。
7. 需要引用文献时，同时记录 Zotero item key 和 BibTeX key；不要把 Zotero item key 当作 BibTeX key。
8. 章节精读笔记应尽量包含 `## 文献锚点`，明确哪些文献支撑本章方法判断；没有合适论文时说明原因，不强行挂接。
9. 涉及研究决策时，先查 `07_研究工作台/实体索引.md` 和 `07_研究工作台/证据与claims矩阵.md`，区分课程资料、文献案例、项目结果和研究假设。
10. 新建或更新笔记时，必须使用统一 frontmatter，补齐标签、来源文件、引用键和相关链接。
11. 每次新建或更新笔记后，同步更新对应目录的 `_index.md`、必要时更新根 `index.md`，并向 `log.md` 追加条目。
12. 完成内容写入后运行或建议 `/update-vault` 验收；涉及图谱健康时运行 `python tools/graph_health.py . --json --stale-days 180`；涉及在线书籍时运行 `python tools/validate_online_book.py --map book/book_map.toml --book-root book/docs --require-nature-refs --require-imagegen --require-mermaid` 和 `mkdocs build -f book/mkdocs.yml --strict`；涉及正文润色时先运行或复查 `python tools/polish_book_chapters.py --check`。
13. 最后简要说明创建或更新了哪些文件、放在哪里、是否有待人工确认的信息。

## Codex skill / 插件联用规则

- 全局 Codex skills：新增第三方专业能力统一安装到 `C:/Users/xsui/.codex/skills/`。P26 已安装 scientific-agent-skills 精选集；调用矩阵见 `00_项目说明/Codex技能调用矩阵.md`。
- AI_MD 项目规则 Codex skills：P27 已将历史 `.claude/skills/` 迁移为 `ai-md-router`、`ai-md-ingest-source`、`ai-md-query-wiki`、`ai-md-takenote`、`ai-md-update-vault`、`ai-md-wiki-lint`、`ai-md-zotero-literature-link`。历史目录保留为来源和兼容层，不再新增第三方 skill。
- `ai-md-router`：LLM Wiki Agent 入口，先判断任务是 ingest、query、lint、takenote、zotero 还是 update。
- `ingest-source`：新来源摄入；识别来源和影响面后，交给 `takenote` 写入，再交给 `update-vault` 验收。
- `query-wiki`：基于 `index.md`、目录 `_index.md` 和具体页面回答；有长期价值的答案再交给 `takenote` 沉淀。
- `wiki-lint`：做高层健康检查；机械一致性检查由 `update-vault` 执行。
- `takenote`：只负责规范写入知识，不负责全库验收。
- `update-vault`：只负责维护验收和报告，不负责生成研究内容。
- `zotero-literature-link`：只负责文献检索、候选、BibTeX 和映射；内容落笔仍遵守 `takenote` 格式。
- 下一版在线教材正文、文献、图示和数据流程更新时，优先从 `scientific-writing`、`literature-review`、`citation-management`、`peer-review`、`scientific-critical-thinking`、`markdown-mermaid-writing`、`scientific-schematics`、`scientific-visualization`、`networkx`、`datamol`、`rdkit`、`medchem`、`molecular-dynamics` 和 `diffdock` 中选择最小必要集合。

## 分类型处理规则

- 课程资料：保留原始文件位置；PDF 课件统一归入本地 `06_原始学习素材/`，非 PDF 原始资料原则上只索引不移动；该目录内容不得加入 Git。
- 章节精读：放入 `01_课程章节索引/章节精读/`，必须连接原始课件、全文提取结果、方法卡和文献锚点。
- 方法笔记：放入 `02_方法笔记/`，必须写清适用场景、输入、可执行流程、输出、质量门槛、失败模式和文献依据。
- 文献笔记：放入 `03_文献笔记/`，必须包含 Zotero item key、BibTeX key、作者/年份/期刊或来源、核心发现、方法论、项目落点和使用边界。
- 实验记录：放入 `04_实验记录/`，必须记录输入、参数、输出文件、关键指标、质量检查、结论和下一步。
- 附件索引：放入 `05_附件索引/`，只记录路径、类型、用途和关联章节，不复制或重命名原始附件，除非我明确要求。
- 项目说明和维护报告：放入 `00_项目说明/`，用于记录阶段性整理、验证结果、边界和待人工确认项。
- 研究工作台：放入 `07_研究工作台/`，用于维护实体、claims、项目池、队列、输出视图和 AI 回归评测；不要把它写成新的长篇课件正文。
- 在线书籍：放入 `book/docs/`，面向课程讲义读者；章节正文、Nature 风格引用卡片、代码案例、Imagegen 图谱、流程图和截图资源必须保留来源边界，不复制原始 PDF、图片、压缩包或 Office 文件，不把文献案例写成本项目结果。
- 正文润色：优先遵守 `book/docs/resources/style-guide.md`；改写时保护引用卡片、代码块、图片链接、BibTeX key、Zotero item key、DOI/URL 和来源路径；高风险 claim 应写入 `00_项目说明/book-stage-reports/polish-report.md`。
- 综合索引和日志：根 `index.md` 和 `log.md` 用于 LLM Wiki 导航和演化记录。

## 搜索方式

先看根目录结构，再进入相关子文件夹读取 `_index.md`，最后读取具体笔记或原始资料。需要研究对象、方法边界或下一步实验时，优先读 `07_研究工作台/实体索引.md`、`07_研究工作台/证据与claims矩阵.md` 和 `07_研究工作台/研究问题与项目池.md`。需要全文搜索时优先用 `rg`。涉及文献时先查本地映射和 BibTeX，再查 Zotero；外部数据库只用于补证或交叉验证。

## 更新规则

- 每次创建或更新笔记后，同步更新对应文件夹的 `_index.md`。
- 重要 ingest、query、update、lint、zotero、ocr、git、maintenance 操作后追加 `log.md`。
- 更新文献映射后，同步检查 `references/references.bib`、`references/zotero-map.tsv`、相关文献笔记和章节锚点矩阵。
- 更新实体、claims、项目池或 AI 评测任务后，同步检查 `07_研究工作台/_index.md`，并运行 `tools/graph_health.py` 观察图谱健康信号。
- 更新在线书籍章节后，同步检查 `book/book_map.toml`、`book/mkdocs.yml`、`book/docs/`、`book/docs/resources/` 和 `tools/update_book_references.py`；需要重建引用区时运行该脚本，再运行在线书籍校验器与 MkDocs strict build。
- 如果 Zotero 导出异常但 DOI/出版社元数据可确认，可以建立人工确认 BibTeX，但必须在 `references.bib` 的 `note` 字段和维护报告中说明。
- 不移动、不删除、不重命名原始学习资料，除非我明确确认。
- 本项目允许启用本地 Git 版本史；默认只记录 Markdown wiki、schema、skills、BibTeX、TSV、脚本和结构化文本，不记录 `06_原始学习素材/` 目录内容，也不记录 PDF/RAR/ZIP/Office 等大型不可变原始资料。

## 笔记 frontmatter 模板

```yaml
---
title: ""
created: YYYY-MM-DD
type: method-note | literature-note | experiment-record | project-doc | attachment-index
status: draft | active | complete | archived
topics: []
source_files: []
zotero_items: []
bibtex_keys: []
related: []
wiki_role: source-summary | concept | method | literature | experiment | synthesis | maintenance
source_count: 0
last_reviewed: YYYY-MM-DD
claims: []
relations: []
---
```

本项目用 `topics` 数组承载标签；需要 Obsidian 图谱时优先依赖 `topics`、`related`、`relations`、根 `index.md` 和目录 `_index.md`。新增字段为可选字段，旧笔记可以逐步补齐。

## 标签规范

- `type/*`：`type/method`、`type/literature`、`type/experiment`、`type/project`、`type/attachment`
- `status/*`：`status/draft`、`status/active`、`status/complete`、`status/archived`
- `topic/*`：`topic/linux`、`topic/pymol`、`topic/chimera`、`topic/docking`、`topic/msa`、`topic/molecular-dynamics`、`topic/bioemu`、`topic/boltz2`、`topic/affinity`、`topic/rfdiffusion`、`topic/protein-design`
- `topic/*` 可按药物化学场景扩展：`topic/medicinal-chemistry`、`topic/peptide-drug`、`topic/structure-based-design`、`topic/free-energy`、`topic/protein-ligand`、`topic/protein-peptide`
- `chapter/*`：`chapter/1` 到 `chapter/6`

## 写作要求

- 自然流畅的中文，不用套话。
- 中英文之间加半角空格，例如 `Boltz2 亲和力预测`、`Zotero item key`。
- 路径、文件名、Zotero item key 和 BibTeX key 用反引号标注。
- 论文题名、期刊名、BibTeX key 和英文专有名词保留英文原文。
- 面向药物化学研究者写作，强调方法边界、输入假设、可复现性和药物发现场景下的解释限制。
- 只给已有笔记加链接，不凭空造链接。
- 没有证据时明确写“待确认”或“未检索到”，不要硬挂文献。

## Zotero 联动规则

- Zotero item key 是本地 Zotero 条目 ID，例如 `FF4V8LYV`。
- BibTeX key 是引用写作使用的 key，例如 `passaro_boltz-2_2025`。
- 两者都要记录；不要把 Zotero item key 当作 BibTeX key。
- 如果 Zotero 导出的 BibTeX key 重复或错误，可以在 `references.bib` 中建立本项目本地 alias，并在 `zotero-map.tsv` 中保留原 Zotero item key。
- 只读检索得到但尚未确认的文献先进入 `references/zotero-candidates-2026-05-30.tsv` 或后续候选表；确认后才提升到 `references/zotero-map.tsv`。
- 不复制 Zotero PDF；如确需全文处理，应先征求用户确认。

## 索引规则

每个目录保留 `_index.md`，表格列固定为：

| 文件 | 类型 | 一句话说明 | 关联原始文件 | 关联 Zotero 条目 |
|:---|:---|:---|:---|:---|

索引应优先写相对路径。PDF 课件原件统一位于本地 `06_原始学习素材/`；非 PDF 原始资料仍保留在原章节目录时，只在索引和笔记中引用路径。远端 GitHub 仓库不保证这些 raw 路径存在。

PDF 课件全文提取使用 `pdfplumber`/PyMuPDF；低文本页 OCR 使用本机 `C:\Program Files\Tesseract-OCR\tesseract.exe`、用户级语言包 `C:\Users\xsui\AppData\Local\Tesseract-OCR\tessdata` 和 `chi_sim+eng`。OCR 结果写入本地对应 PDF 提取目录的 `ocr/page-xxx.ocr.md`，并追加到 `全文.md`。OCR 收敛状态以本地 `06_原始学习素材/PDF OCR质量收敛报告.md` 为准；第 1-8 章课件结构化精读入口为 `01_课程章节索引/章节精读/_index.md`。
