---
title: "AI_MD LLM Wiki 操作日志"
created: 2026-05-30
type: project-doc
status: active
topics: [type/project, status/active, llm-wiki, log]
wiki_role: maintenance
source_count: 37
last_reviewed: 2026-06-08
source_files: ["VERSION", "CLAUDE.md", "index.md", "00_项目说明/版本记录.md", "00_项目说明/P41_十二章在线图书重建报告.md", "book/mkdocs.yml", "tools/sync_online_book.py", "tools/validate_online_book.py", "tests/test_online_book_publish.py", ".github/workflows/deploy-book.yml", "00_项目说明/知识库维护报告-2026-05-31-P12-新增原始素材全库更新.md", "00_项目说明/知识库维护报告-2026-05-31-P13-第八章计算思路解析摄入.md", "00_项目说明/知识库维护报告-2026-05-31-P14-文献锚定.md", "00_项目说明/知识库维护报告-2026-05-31-P15-P19-研究知识图谱工作台.md", "00_项目说明/知识库维护报告-2026-05-31-P20-在线书籍骨架.md", "00_项目说明/知识库维护报告-2026-05-31-P21-GitHub-Pages部署配置.md", "00_项目说明/知识库维护报告-2026-05-31-P22-第一版验收.md", "00_项目说明/知识库维护报告-2026-05-31-P24-在线书籍引用代码图像增强.md", "00_项目说明/知识库维护报告-2026-05-31-P25-在线书籍正文润色与结构重排.md", "00_项目说明/知识库维护报告-2026-05-31-P26-原始素材目录本地保留.md", "00_项目说明/P26_Codex技能集成报告.md", "00_项目说明/P27_Codex项目规则迁移报告.md", "00_项目说明/P28_重点章节Codex审稿报告.md", "00_项目说明/P29_文献与引用补强报告.md", "00_项目说明/P30_图示与版面升级报告.md", "00_项目说明/P31_数据分析与AIDD dry-run报告.md", "00_项目说明/P32_文献候选正式化报告.md", "00_项目说明/P33_Zotero正式锚点补齐报告.md", "00_项目说明/P34_中文教材可读性增强报告.md", "00_项目说明/P35_中文教材去模板化与版本更新报告.md", "00_项目说明/book-stage-reports/p34-readability-report.md", "00_项目说明/book-stage-reports/p35-detemplate-report.md", "00_项目说明/book-stage-reports/p39-reviewer-revision-report.md", "tools/audit_book_readability.py", "tools/audit_book_review_readiness.py", "tests/test_audit_book_readability.py", "tests/test_audit_book_review_readiness.py", "00_项目说明/Codex技能调用矩阵.md"]
zotero_items: ["TPR3JY6N", "QXKW6K78", "YUMKNHSK", "Y4ARSYCQ", "V6Y5EEZL", "5286JS9F", "T2M6L289", "UIPWC5CR"]
bibtex_keys: ["yang_w_past_2026", "sui_targeting_2026", "shen_structure-based_2026", "tomarchio_reproducible_2026", "zhu_novo_2026", "chai_discovery_chai-1_2024", "butcher_novo_2025", "pacesa_bindcraft_2025"]
related: ["index.md", "00_项目说明/LLM Wiki运行手册.md"]
claims: [p11_schema_enhancement_2026_05_30, p12_reusable_skill_2026_05_30, p12_new_raw_ingest_2026_05_31, p13_chapter_8_ingest_2026_05_31, p14_literature_anchoring_2026_05_31, p15_entity_layer_2026_05_31, p16_claim_layer_2026_05_31, p17_research_workbench_2026_05_31, p18_ai_eval_suite_2026_05_31, p19_output_views_2026_05_31, p20_online_book_skeleton_2026_05_31, p21_github_pages_deploy_2026_05_31, p22_first_version_acceptance_2026_05_31, p24_online_book_reference_code_imagegen_2026_05_31, p25_online_book_academic_polish_2026_05_31, p26_raw_sources_git_exclusion_2026_05_31, p26_codex_skills_integration_2026_06_02, p27_codex_project_rules_migration_2026_06_02, p28_high_risk_chapter_review_2026_06_02, p29_literature_reinforcement_2026_06_02, p30_mermaid_schematics_2026_06_02, p31_aidd_dry_run_2026_06_02, p32_literature_upgrade_2026_06_02, p33_zotero_anchoring_2026_06_02, v0_7_0_release_2026_06_02, p34_book_readability_2026_06_02, p35_book_detemplate_2026_06_02, v0_8_0_release_2026_06_02, p39_reviewer_revision_2026_06_06, v0_9_3_release_2026_06_06, p41_online_book_rebuild_2026_06_08, v1_0_0_release_2026_06_08]
relations:
  - type: depends_on
    target: "CLAUDE.md"
  - type: updates
    target: "index.md"
  - type: updates
    target: "C:/Users/xsui/.codex/skills/building-llm-wiki/SKILL.md"
  - type: updates
    target: "00_项目说明/知识库维护报告-2026-05-31-P12-新增原始素材全库更新.md"
  - type: updates
    target: "00_项目说明/知识库维护报告-2026-05-31-P13-第八章计算思路解析摄入.md"
  - type: updates
    target: "00_项目说明/知识库维护报告-2026-05-31-P14-文献锚定.md"
  - type: updates
    target: "00_项目说明/知识库维护报告-2026-05-31-P15-P19-研究知识图谱工作台.md"
  - type: updates
    target: "00_项目说明/知识库维护报告-2026-05-31-P20-在线书籍骨架.md"
  - type: updates
    target: "00_项目说明/知识库维护报告-2026-05-31-P21-GitHub-Pages部署配置.md"
  - type: updates
    target: "00_项目说明/知识库维护报告-2026-05-31-P22-第一版验收.md"
  - type: updates
    target: "00_项目说明/知识库维护报告-2026-05-31-P24-在线书籍引用代码图像增强.md"
  - type: updates
    target: "00_项目说明/知识库维护报告-2026-05-31-P25-在线书籍正文润色与结构重排.md"
  - type: updates
    target: "00_项目说明/知识库维护报告-2026-05-31-P26-原始素材目录本地保留.md"
  - type: updates
    target: "00_项目说明/P26_Codex技能集成报告.md"
  - type: updates
    target: "00_项目说明/P27_Codex项目规则迁移报告.md"
  - type: updates
    target: "00_项目说明/P28_重点章节Codex审稿报告.md"
  - type: updates
    target: "00_项目说明/P29_文献与引用补强报告.md"
  - type: updates
    target: "00_项目说明/P30_图示与版面升级报告.md"
  - type: updates
    target: "00_项目说明/P31_数据分析与AIDD dry-run报告.md"
  - type: updates
    target: "00_项目说明/P32_文献候选正式化报告.md"
  - type: updates
    target: "00_项目说明/P33_Zotero正式锚点补齐报告.md"
  - type: updates
    target: "00_项目说明/P34_中文教材可读性增强报告.md"
  - type: updates
    target: "00_项目说明/P35_中文教材去模板化与版本更新报告.md"
  - type: supports
    target: "00_项目说明/P40_旧版在线图书删除记录.md"
  - type: updates
    target: "00_项目说明/P41_十二章在线图书重建报告.md"
  - type: updates
    target: "00_项目说明/版本记录.md"
  - type: updates
    target: "00_项目说明/Codex技能调用矩阵.md"
---

# AI_MD LLM Wiki 操作日志

本文件为追加式日志。新条目格式固定为：

`## [YYYY-MM-DD] operation | title`

允许的 `operation`：`ingest`、`query`、`update`、`lint`、`zotero`、`ocr`、`git`、`maintenance`。

## [2026-06-08] update | P41 十二章在线图书重建

- 从 `大纲.md` 和 `chapters/chapter-01/正文.md` 至 `chapters/chapter-12/正文.md` 重建 `book/` 发布层；本轮不复制 `本章大纲.md`。
- 新增 `tools/sync_online_book.py`、`tools/validate_online_book.py`、`tests/test_online_book_publish.py` 和 `.github/workflows/deploy-book.yml`，恢复 GitHub Pages 自动构建发布。
- 在线教材采用蓝白配色，发布页过滤原始素材路径、旧 `book/docs`/`book/site` 路径、阶段报告入口和待作者确认项。
- 新增 `00_项目说明/P41_十二章在线图书重建报告.md`，项目版本更新为 `v1.0.0`。

## [2026-06-06] maintenance | 旧版在线图书删除

- 删除旧版 `book/` 在线教材工程，包含旧 `book/docs/` 源页面、`book/site/` 本地构建、MkDocs 配置、章节映射、旧资源页和图像资产。
- 删除 `.github/workflows/deploy-book.yml`，停止旧 GitHub Pages workflow 继续依赖已删除的发布层。
- 删除旧书专用脚本和测试：`validate_online_book.py`、`polish_book_chapters.py`、`update_book_references.py`、`apply_p24_book_assets.py`、`audit_book_*` 及对应 `tests/test_*book*.py`。
- 更新 `大纲.md`、`AGENTs.md`、`CLAUDE.md` 和根索引，把当前生成入口切换到 `chapters/` 12 章工作区；新增 `00_项目说明/P40_旧版在线图书删除记录.md`。

## [2026-06-06] maintenance | v0.9.3 项目版本更新

- 更新根 `VERSION` 为 `v0.9.3`，将在线书籍版本更新为 `v0.9.3-p39-reviewer-revision`。
- 更新 `00_项目说明/版本记录.md`、根索引和在线书籍首页，记录 P39 审稿导向教材修订范围。
- 修复 `00_项目说明/book-stage-reports/_index.md` 的乱码索引，并把 P39 报告加入维护报告目录。

## [2026-06-06] update | P39 审稿导向教材修订

- 使用 `academic-research-suite / academic-paper-reviewer` 审稿框架和中文学术写作边界，对 `book/docs/chapters/chapter-01.md` 至 `chapter-08.md` 做审稿导向修订。
- 为每章 `关键文献` 增加 `文献使用说明`，并为第 3/5/6/8 章增加 `案例走读`。
- 新增 `tools/audit_book_review_readiness.py` 和 `tests/test_audit_book_review_readiness.py`，检查模板句残留、文献使用说明、案例走读和高风险边界。
- 本轮不新增实验结果、不重做 Imagegen 图、不显示 BibTeX key 或 Zotero item key，阶段报告只保存在 `00_项目说明/book-stage-reports/`。

## [2026-06-02] maintenance | v0.8.0 项目版本更新

- 更新根 `VERSION` 为 `v0.8.0`，将在线书籍版本更新为 `v0.8-p35-detemplated`。
- 更新 `00_项目说明/版本记录.md`，记录 P35 后的发布范围、验收命令和 P36 真实小样本运行目标。
- 同步根索引、项目说明索引、在线书籍首页和 MkDocs 资源导航。

## [2026-06-02] update | P38 在线教材报告页迁出

- 将 P25、P34、P35、P36 和 P37 阶段性报告从 `book/docs/resources/` 迁出到 `00_项目说明/book-stage-reports/`。
- 从 `book/mkdocs.yml` 课程资源导航和 `book/docs/index.md` 资源表中移除阶段性报告入口，在线教材内容层只保留读者资源页。
- 新增 `00_项目说明/book-stage-reports/_index.md` 和 `00_项目说明/P38_在线教材报告页迁出报告.md`，项目版本更新为 `v0.9.2`。
- 保留阶段性报告作为项目维护资料，不修改章节正文、引用、代码、图片、截图或原始素材边界。

## [2026-06-02] update | P37 图注编号解释合并

- 将 `book/docs/chapters/chapter-01.md` 至 `chapter-08.md` 中知识图谱和流程图下方的编号解释表合并进对应图注。
- 删除独立的 `编号 | 正文权威标签`、`编号 | 流程节点` 表格和“图中编号节点与下表对应”提示，使图注承担图意、编号含义和边界说明。
- 增强 `tools/audit_book_figures.py`，新增独立编号表残留检查，并要求 `图X.1` / `图X.3` 图注包含内联编号说明。
- 新增 `00_项目说明/book-stage-reports/p37-caption-compaction-report.md` 和 `00_项目说明/P37_图注编号解释合并报告.md`，项目版本更新为 `v0.9.1`。

## [2026-06-02] update | P36 图注与图示出版规范化

- 将 `book/docs/chapters/chapter-01.md` 至 `chapter-08.md` 的 32 个图位统一为 `图X.Y` 编号体系，覆盖 Imagegen 知识图谱、Mermaid 结构图、Imagegen 流程图和软件截图。
- 为每张图补充图下注释和 alt text，图注说明对象、阅读顺序、来源边界和“不代表实验结果”等限制。
- 将 `book/docs/resources/screenshot-index.md` 改为截图文件链接索引，避免资源页出现未编号图片。
- 新增 `tools/audit_book_figures.py` 与 `tests/test_audit_book_figures.py`，图注审计结果为 8 章、32 图位、errors 0。
- 新增 `00_项目说明/book-stage-reports/p36-figure-caption-report.md` 与 `00_项目说明/P36_图注与图示出版规范化报告.md`，并将项目版本更新为 `v0.9.0`。

## [2026-06-02] update | P35 中文教材去模板化

- 对 `book/docs/chapters/chapter-01.md` 至 `chapter-08.md` 做章节专属化修订，减少跨章模板句。
- 增强 `tools/audit_book_readability.py`，让 repeated sentences 只统计正文句子，排除标题、表格、列表、代码块、引用区和图片链接残留。
- 新增 `00_项目说明/book-stage-reports/p35-detemplate-report.md` 和 `00_项目说明/P35_中文教材去模板化与版本更新报告.md`。
- P35 可读性审计结果：每章正文最小值 4078，平均值 4375.5，重点区块最小值 365，prose-only 重复句 0，errors 0。

## [2026-06-02] update | P34 中文教材可读性增强

- 采用中等扩写和教材讲解风格，重写 `book/docs/chapters/chapter-01.md` 至 `chapter-08.md` 的导读、核心概念、方法流程、代码案例解释、使用边界和延伸阅读。
- 新增 `00_项目说明/book-stage-reports/p34-readability-report.md` 和 `00_项目说明/P34_中文教材可读性增强报告.md`，记录外部写作规则提炼、章节改写策略、边界保护和需作者确认项。
- 新增 `tools/audit_book_readability.py` 与 `tests/test_audit_book_readability.py`，可统计章节可读性正文长度、重点区块长度、重复模板句和过强表述。
- 本轮不新增科学事实、不新增文献、不重做 Imagegen 图；保留引用列表、代码块、图片路径、DOI、BibTeX/Zotero provenance 和 `06_原始学习素材/` 本地只读边界。

## [2026-06-02] maintenance | v0.7.0 项目版本更新

- 新增根 `VERSION`，将 AI_MD 当前项目版本固定为 `v0.7.0`。
- 更新 `book/book_map.toml` 为 `v0.7-p33-zotero-anchored`，并把在线书籍首页说明更新为第四版。
- 新增 `00_项目说明/版本记录.md`，记录发布范围、验收命令、GitHub Pages 地址和下一版 P34 目标。
- 同步根索引、项目说明索引、文献索引、实体索引和 P32/P33 文献锚点说明，保持 Chai-1、RFdiffusion3/RFD3 与 BindCraft Nature 2025 的正式 Zotero/BibTeX provenance。

## [2026-06-02] update | P26 Codex skills 全局精选集成

- 从 `K-Dense-AI/scientific-agent-skills` commit `93124850ef08487e423165554c54f0b333d5631d` 安装 21 个精选全局 Codex skills 到 `C:\Users\xsui\.codex\skills`。
- 明确 AI_MD 仓库不再向 `.claude/skills/` 添加第三方 skill 副本；新增专业能力走全局 Codex skills。
- 新增 `00_项目说明/P26_Codex技能集成报告.md`、`00_项目说明/Codex技能调用矩阵.md` 和 `tools/install_ai_md_codex_skills.ps1`。
- 更新 `CLAUDE.md`、`00_项目说明/插件与Skills调用说明.md`、根索引和项目说明索引。

## [2026-06-02] update | P27 Codex 项目规则迁移

- 将 `.claude/skills` 中的 AI_MD 自有规则生成并安装为 7 个 `ai-md-*` 全局 Codex skills。
- 新增 `tools/install_ai_md_project_codex_skills.ps1`，用于从历史项目规则重建全局 Codex skills。
- 新增 `00_项目说明/P27_Codex项目规则迁移报告.md`，记录迁移映射、边界和 P28-P31 使用方式。
- 更新 `CLAUDE.md`、`Codex技能调用矩阵.md`、`插件与Skills调用说明.md`、根索引和项目说明索引。

## [2026-06-02] update | P28 重点章节 Codex 审稿

- 使用 `peer-review`、`scientific-critical-thinking` 和 `scientific-writing` 原则审查第 3/5/6/8 章高风险表述。
- 新增 `00_项目说明/P28_重点章节Codex审稿报告.md`，记录 docking score、predicted affinity、RFdiffusion/RFD3、ProteinMPNN、Chai-1 aggregate score 和文献案例的证据边界。
- 本轮不改章节正文、不新增引用、不新增实验结果；P28 作为 P29 文献复核、P30 图示升级和 P31 dry-run 的交接基线。
- 更新根索引、项目说明索引和 `Codex技能调用矩阵.md`。

## [2026-06-02] update | P29 文献与引用补强

- 复核第 3/5/6/8 章 `book_map.toml` required BibTeX key、章节关键文献区、`references.bib` 和 `zotero-map.tsv`。
- 新增 `references/literature-audit-2026-06-02-P29.tsv`，记录 21 个章节-引用关系均有正式映射。
- 新增 `references/zotero-candidates-2026-06-02-P29.tsv`，记录 Chai-1、RFD3/RFdiffusion3 和 BindCraft Nature 2025 正式版本候选。
- 新增 `00_项目说明/P29_文献与引用补强报告.md`，并同步更新文献候选笔记、claims 矩阵、根索引、项目说明索引和 `Codex技能调用矩阵.md`。

## [2026-06-02] update | P30 图示与版面升级

- 为第 1-8 章新增 Mermaid 结构图，作为 Imagegen 辅助图之外的可版本化 source of truth。
- 新增 `book/docs/resources/mermaid-schematics.md`，记录每章 Mermaid 图和 scientific-schematics prompt。
- 更新 `book/mkdocs.yml`，启用 Mermaid custom fence，并把新资源页加入课程资源导航。
- 扩展 `tools/validate_online_book.py` 和 `tests/test_validate_online_book.py`，新增 `--require-mermaid` 校验和 accessibility 测试。
- 新增 `00_项目说明/P30_图示与版面升级报告.md`，并同步更新根索引、项目说明索引和 `Codex技能调用矩阵.md`。

## [2026-06-02] update | P31 数据分析与 AIDD dry-run

- 使用 `datamol`、`rdkit`、`medchem`、`molecular-dynamics` 和 `diffdock` 的工作流边界，补强第 3/5/6/8 章 AIDD dry-run。
- 新增 `book/docs/resources/aidd-dry-runs.md` 和 4 个 Python dry-run 脚本，覆盖 ligand triage、亲和力解释、设计 QC 和项目优先级。
- 更新第 3/5/6/8 章代码案例说明、课程资源导航和复现实验资源页。
- 更新对接、Boltz2、RFdiffusion、Chai-1 实验记录模板，新增 `pose_qc_passed`、`calibration_available`、`interface_qc_passed` 和 `evidence_maturity` 等字段。
- 新增 `00_项目说明/P31_数据分析与AIDD dry-run报告.md`，并同步更新根索引、项目说明索引和 `Codex技能调用矩阵.md`。

## [2026-06-02] update | P32 文献候选正式化

- 将 P29 候选中的 Chai-1、RFdiffusion3/RFD3 和 BindCraft Nature 2025 提升为正式 BibTeX 条目，写入 `references/references.bib`。
- 新增 `references/literature-upgrades-2026-06-02-P32.tsv`，记录 DOI、venue、正式 BibTeX key、升级状态和 Zotero 待补边界。
- 更新 `references/zotero-map.tsv`、`book/book_map.toml`、第 6/8 章引用区和附录 C，使正式引用列表使用 `chai_discovery_chai-1_2024`、`butcher_novo_2025` 和 `pacesa_bindcraft_2025`。
- 新增 Chai-1 文献笔记，补强 RFdiffusion 与 BindCraft 文献笔记、Chai-1 方法卡和 claims 矩阵。
- 本地 Zotero API 未运行且未找到 `zotero.exe`，因此不伪造 item key；映射表暂用 `待补正式锚点`，后续 P33 可在 Zotero Desktop 可用后补正式条目。

## [2026-06-02] update | P33 Zotero 正式锚点补齐

- 从 `E:\Program Files\Zotero\zotero.exe` 启动 Zotero 9.0.4，确认 Local API 和 Connector 可用。
- 使用 `zotero://select/library/collections/WOJHNDDE` 切换到 `AI药物设计_蛋白与多肽` 集合，并通过 Connector 导入 Chai-1，获得 item key `5286JS9F`。
- 检索确认 RFdiffusion3/RFD3 已有重复 Zotero 条目 `T2M6L289` 和 `5IA9AEAN`；本项目选择 `T2M6L289` 作为 canonical。
- 检索确认 BindCraft Nature 2025 已有 Zotero 条目 `UIPWC5CR`；旧 preprint `QCD2DXXI` 继续对应 `pacesa_bindcraft_2024`。
- 更新 `references/zotero-map.tsv`、`references/references.bib`、`references/literature-upgrades-2026-06-02-P32.tsv`、新增 `references/zotero-upgrades-2026-06-02-P33.tsv`，并同步文献笔记、claims 矩阵、根索引和项目说明索引。

## [2026-05-31] update | P24 在线书籍引用、代码和 Imagegen 图像增强

- 为 8 个在线书籍章节新增 Imagegen 知识图谱、流程解释图、代码案例、软件操作截图、步骤表和常见错误提示。
- 新增课程资源页：代码案例索引、截图索引、Imagegen prompt 记录和复现实验资源。
- 新增 `tools/update_book_references.py`，自动生成 Nature 风格引用卡片和附录 C；补齐 `du_dockey_2023`、`agrawal_benchmarking_2019` 的 DOI/期刊元数据。
- 扩展 `tools/validate_online_book.py`，加入 `--require-nature-refs` 与 `--require-imagegen` 验收项。

## [2026-05-31] update | P25 在线书籍正文润色与结构重排

- 使用 research-paper-writing 和 academic-chinese-style 原则，对 8 个在线书籍主章节做教材化结构重排。
- 新增 `tools/polish_book_chapters.py`、`book/docs/resources/style-guide.md` 和 `00_项目说明/book-stage-reports/polish-report.md`。
- 每章补充 reverse outline、claim-evidence map、来源路径表和更明确的证据边界。
- 保留引用卡片、代码块、图片链接、BibTeX key、Zotero item key 和 DOI/URL，不处理未跟踪 torrent 文件。

## [2026-05-31] git | P26 原始素材目录本地保留、不上传内容

- 更新 `.gitignore`，`06_原始学习素材/` 只保留 `.gitkeep` 占位，目录内容不再上传 GitHub。
- 从 Git 索引移除已追踪的 raw source 文件，保留本地文件不删除。
- 更新 `CLAUDE.md`、总索引和使用说明，明确 raw 目录为本地 source of truth。

## [2026-05-30] bootstrap | AI_MD LLM Wiki Agent 落地

- 按 Karpathy LLM Wiki 模式建立 AI_MD 专用第二大脑规则。
- 新增根 `index.md`、根 `log.md`、LLM Wiki 说明、运行手册、概念关系规范。
- 明确 `ai-md-router` 总调度、`takenote` 知识写入、`update-vault` 维护验收的联用关系。

## [2026-05-30] update | 扩展本地 LLM Wiki skills

- 新增 `ingest-source`、`query-wiki`、`wiki-lint`。
- 更新 `ai-md-router`、`takenote`、`update-vault`、`zotero-literature-link`，纳入 LLM Wiki Agent 工作流。

## [2026-05-30] git | 初始化本地版本史

- 执行 `git init` 并做首次本地提交。
- 不配置 remote，不 push。
- `.gitignore` 忽略易变 Obsidian workspace、缓存、临时文件和大型不可变二进制原始资料，不忽略核心 Markdown、BibTeX、TSV、skills 或原始资料索引。

## [2026-05-30] lint | LLM Wiki / update-vault 验收

- 验证根索引、目录索引、skills、BibTeX 映射、Markdown 链接和 Git 状态。
- 结果以本轮最终验证输出为准。

## [2026-05-30] maintenance | P9 LLM Wiki Agent落地报告

- 新增 `00_项目说明/知识库维护报告-2026-05-30-P9-LLM-Wiki-Agent落地.md`。
- 把根 `index.md`、`log.md`、LLM Wiki 说明文档和新增 skills 纳入 `00_项目说明/_index.md`、Obsidian 入口和使用说明。

## [2026-05-30] lint | P10 wiki-lint 健康检查

- 执行 P10 高层健康检查，覆盖 managed Markdown、生成式 PDF 提取页面、附件索引、Markdown 链接和 Zotero/BibTeX 映射。
- 修复 `references/zotero-map.tsv` 和 `references/zotero-candidates-2026-05-30.tsv` 未进入附件清单的问题。
- 维护报告写入 `00_项目说明/知识库维护报告-2026-05-30-P10-wiki-lint健康检查.md`。

## [2026-05-30] update | P11 schema 增强

- 只做 schema 增强，不扩写研究内容。
- 给核心方法卡、文献笔记、LLM Wiki 规则页和 P9/P10 维护报告补 `wiki_role`、`claims` 和 typed `relations`。
- 新增 `00_项目说明/知识库维护报告-2026-05-30-P11-schema增强.md`。

## [2026-05-30] maintenance | 提炼 LLM Wiki 建库方法为全局 skill

- 新增全局 Codex skill：`C:/Users/xsui/.codex/skills/building-llm-wiki/`。
- 将 AI_MD 已验证的 raw sources / wiki / schema 三层建库法、`index.md`/`log.md`/`_index.md` 规则、typed relations、Zotero/BibTeX provenance 和本地 skill 分工提炼为可复用流程。
- 附带通用校验脚本：`scripts/validate_llm_wiki.py`，用于检查受管 Markdown 链接、typed relation 目标和 Zotero/BibTeX 映射。

## [2026-05-31] ingest | P12 新增原始素材全库更新

- 按 building-llm-wiki 三层结构重新摄入 `06_原始学习素材/`，把第四章、第五章、第六章和第八章新增素材纳入资料索引与附件清单。
- 提取 `06_原始学习素材/第六章/第六七章RFD3多组分设计.pdf`，生成全文、分页 Markdown、OCR 低文本页和提取报告。
- 新增第 06/07 章章节精读，更新章节索引、方法卡、根索引、PDF/OCR 总览和 P12 维护报告。

## [2026-05-31] ingest | P13 第八章计算思路解析摄入

- 解包 `06_原始学习素材/第八章/第八章思路解析.zip` 到 `06_原始学习素材/第八章/解包/第八章思路解析/`。
- 提取第八章主 PDF 和 4 份补充 PDF，生成全文、分页 Markdown、质量报告；主 PDF 14 个低文本页补 OCR。
- 新增第 08 章章节精读、`Chai1互作蛋白虚拟筛选.md` 方法卡和 Chai-1 实验记录模板，并同步索引、附件清单、PDF/OCR 总览和 P13 维护报告。

## [2026-05-31] zotero | P14 第六章/第八章文献锚定

- 第六章新增 Nature PDF 选择 Zotero canonical 条目 `TPR3JY6N`，写入 BibTeX key `yang_w_past_2026`；重复条目 `G3TSIVRB` 仅在报告中记录，不进入映射。
- 第八章 4 份补充 PDF 导入 Zotero：`QXKW6K78` / `sui_targeting_2026`、`YUMKNHSK` / `shen_structure-based_2026`、`Y4ARSYCQ` / `tomarchio_reproducible_2026`、`V6Y5EEZL` / `zhu_novo_2026`。
- 同步更新 `references/references.bib`、`references/zotero-map.tsv`、章节-文献锚点矩阵、相关方法/文献笔记、附件索引和 P14 维护报告。

## [2026-05-31] update | P15-P19 研究知识图谱与个人工作台

- 新增 `07_研究工作台/`，包含实体索引、证据与 claims 矩阵、研究问题与项目池、阅读队列、实验队列、输出视图和 AI 回归评测集。
- 新增 `tools/graph_health.py` 与 `tests/test_graph_health.py`，用于统计实体数、typed relations、孤立页、过期 `last_reviewed`、缺 BibTeX 的 Zotero 映射和文献笔记 key 缺口。
- 同步更新根索引、使用说明、`CLAUDE.md` 和 P15-P19 维护报告，明确后续目标从堆资料转向可查询、可推理、可执行的研究知识图谱。

## [2026-05-31] update | P20 在线书籍分章节骨架

- 新增 `book/` MkDocs Material 工程，包含 `mkdocs.yml`、`requirements.txt`、`book_map.toml`、8 个主章节页面和 5 个附录页面。
- 新增 `tools/validate_online_book.py` 与 `tests/test_validate_online_book.py`，校验章节必填区块、来源路径、BibTeX key、书内链接和禁止 raw source 链接。
- 同步更新根索引、使用说明、`CLAUDE.md` 和 P20 维护报告，明确在线书籍是课程讲义骨架，不复制原始 PDF 或图表。

## [2026-05-31] update | P21 GitHub Pages 部署配置

- 将在线书籍站点 URL 固定为 `https://luvega.github.io/AI_MD/`。
- 新增 `.github/workflows/deploy-book.yml`，在 `master` 推送或手动触发时运行测试、在线书籍校验、MkDocs strict build，并通过 GitHub Pages 发布 `book/site`。
- 记录远端仓库为 `https://github.com/luvega/AI_MD.git`；Pages 需要在 GitHub 仓库设置中选择 GitHub Actions 作为发布源。

## [2026-05-31] maintenance | P22 第一版验收

- 运行 `python -m unittest discover -s tests`，4 个单元测试通过。
- 运行 `python tools/validate_online_book.py --map book/book_map.toml --book-root book/docs`，在线书籍校验 `errors: 0`。
- 运行 `python -m mkdocs build -f book/mkdocs.yml --strict`，MkDocs strict build 成功生成 `book/site`。
- 运行 `validate_llm_wiki.py`，LLM Wiki 校验 `warnings: []`、`errors: []`。
- 确认 GitHub Pages 最新 workflow 成功，`https://luvega.github.io/AI_MD/` 首页返回 HTTP 200。

## [2026-05-31] update | P23 在线书籍第二版长文

- 将 `book/docs/chapters/chapter-01.md` 至 `chapter-08.md` 从第一版导航骨架扩写为第二版课程讲义正文，8 章均超过 5000 字符。
- 更新 `book/docs/index.md` 和 `book/book_map.toml`，将在线书籍版本标记为 `v0.2-course-text`。
- 增强 `tools/validate_online_book.py`，新增 `--min-chapter-chars`；补充单元测试覆盖章节长度门槛。
- 新增 `00_项目说明/知识库维护报告-2026-05-31-P23-在线书籍第二版长文.md`，记录章节长度、引用边界和验收结果。

## [2026-06-06] update | 第 4 章分子对接与虚拟筛选正文

- 按 `大纲.md` 和 `chapters/chapter-04/本章大纲.md`，新增 `chapters/chapter-04/正文.md`，并同步更新在线教材 `book/docs/chapters/chapter-04.md`。
- 同步调整 `book/book_map.toml` 与 `book/mkdocs.yml` 的第 4 章标题、来源材料和 BibTeX key，正文采用原始第三章对接素材、章节精读、方法卡、文献笔记、实验模板和 claims 矩阵。
- 本轮未复制原始 PDF、课件截图、Office 文件或压缩包；在线页暂复用已验收的对接类教学图、dry-run 脚本和截图资源，后续可再生成第 4 章专属资源。

## [2026-06-06] update | 第 3 章结构准备正文

- 按 `大纲.md` 和 `chapters/chapter-03/本章大纲.md` 将在线教材第 3 章重写为“结构建模、结合位点与体系准备”，聚焦对接前结构来源、位点假设、体系组分和 QC 清单。
- 同步更新 `book/book_map.toml` 与 `book/mkdocs.yml` 中第 3 章标题和关键文献映射；原始课件与 OCR 摘要只作为本地来源，不直接链接到在线教材。

## [2026-06-06] update | 第 3 章正文生成区重建

- 根据作者确认项，将第 3 章标题固定为“结构建模、结合位点与体系准备”，并明确本章只处理 docking 前准备；docking 运行、打分排序和虚拟筛选解释后移到第 4 章。
- 更新 `chapters/chapter-03/本章大纲.md`，把待确认项改为已确认项，并将后续写作入口从旧 `book/docs/` 改为当前 `chapters/chapter-03/正文.md`。
- 新增 `chapters/chapter-03/正文.md`、`chapters/chapter-03/assets/component_manifest_example.tsv` 和 `chapters/chapter-03/assets/chapter-03-structure-prep-map.svg`，用于第三章正文、练习模板和本章专属教学图。
- 本轮不调用已删除的旧 MkDocs 发布层和旧在线教材校验脚本；使用当前项目保留的图谱健康检查、单元测试和 diff 空白检查。

## [2026-06-08] update | 第 5 章分子动力学模拟基础流程正文

- 按 `大纲.md` 和更新后的 `chapters/chapter-05/本章大纲.md`，新增 `chapters/chapter-05/正文.md`，聚焦 GROMACS 文件、拓扑、系统准备、EM/NVT/NPT/production 和复杂体系参数边界。
- 新增 `chapters/chapter-05/assets/code/chapter-05-gromacs-file-check.py`，用于教学 dry-run 检查 `protein.pdb`、`topol.top` 和基础 `.mdp` 文件清单；生成示例输出 `chapter-05-gromacs-file-check-demo.tsv`。
- 本轮确认当前 Git 工作区中的 `06_原始学习素材/` 只有 `.gitkeep`，因此正文只使用已整理的章节精读、方法笔记、文献笔记、实验模板、claims 矩阵和 `references.bib`，不引用缺失原始课件页码或截图。
- 验收执行了第 5 章 dry-run、禁用套话检查、段落长度检查、`python -m unittest discover -s tests` 和 `python tools/graph_health.py . --json --stale-days 180`；图谱健康报告仍有既有 `missing_last_reviewed` 与孤立页提示。

## [2026-06-08] update | 第 4 章分子对接与虚拟筛选正文重建

- 按 `AGENTs.md` 新规则更新 `大纲.md` 和 `chapters/chapter-04/本章大纲.md`，将 4.2 从 `SurDock/Transform-AF3` 调整为 `SurfDock 与复合物结构预测`。
- 基于原始对接素材、全文提取、方法卡、文献笔记、实验记录模板和 claims 矩阵，重写 `chapters/chapter-04/正文.md`；正文不再引用旧 `book/` 发布层或第 3 章复用资源。
- 新增第 4 章专属资源：`chapters/chapter-04/assets/imagegen/` 两张教学 PNG、`assets/screenshots/chapter-04-unidock-dry-run.png`、`assets/code/chapter-04-unidock-dry-run.sh`、示例 manifest 和 `asset_manifest.tsv`。
- 本轮统一工具名来源：`SurfDock` 采用 Nature Methods 论文与 GitHub 仓库写法；`Transform-AF3` 未检索到可确认主来源，保留为待作者确认项，不进入正式工具清单。
- 验收执行了段落长度检查、禁用套话/旧路径检查、资源路径存在性检查、dry-run 脚本试运行、图片人工抽查和 `git diff --check`。

## [2026-06-08] update | 第 9 章生成式蛋白设计基础正文

- 按 `AGENTs.md`、`大纲.md` 和更新后的 `chapters/chapter-09/本章大纲.md`，新增 `chapters/chapter-09/正文.md`。
- 正文基于 `06_原始学习素材/第六七章RFD3多组分设计.md`、`06_原始学习素材/第六章/全文提取/第六七章RFD3多组分设计/全文.md` 和 `extraction-report.md`，聚焦 RFdiffusion 系列、RFD3 输入配置、hotspot 选择、pLDDT/PAE/iPAE/RMSD 指标边界和随机骨架 dry-run 练习。
- 本轮保持第 9 章与第 10 章边界：binder、短肽、迷你蛋白、核酸抑制剂、理论酶和 ProteinMPNN / LigandMPNN 闭环只作为下一章入口，不在第 9 章展开。
- 验收执行了禁用套话和旧发布层路径检查、段落长度检查、连续纯文字段落检查和章节标题完整性检查；软件安装仓库、`rc-foundry[all]`、checkpoint 路径和完整运行命令仍需按当前版本复核。

## [2026-06-09] maintenance | P42 原始素材更新后全项目重建

- 按 `building-llm-wiki` 三层规则重新审计 `06_原始学习素材/`：当前 raw 文件 1076 个，PDF 14 个，12 个 PDF 已有提取报告，2 个补充 PDF 保留为附件/文献锚点，后续按需提取。
- 新增 `tools/audit_raw_sources.py`，并补齐 `06_原始学习素材/_index.md` 与 `05_附件索引/附件清单.md` 中 8 个根级课程 Markdown 原文入口；关键附件索引缺口 0，根级 Markdown 来源索引缺口 0。
- 修正 `CLAUDE.md`、`AGENTs.md`、`大纲.md` 和第 5 章来源声明：旧版内容不完整的 `book/` 已删除；当前 `book/` 只从 12 章 `正文.md` 同步生成，不能反向作为正文来源。
- 重新运行 `python tools\sync_online_book.py`，同步 12 章发布层，并通过在线书校验、pytest、MkDocs strict build、LLM Wiki 校验、raw-source 审计和图谱健康检查。
- 新增 `00_项目说明/P42_原始素材更新后全项目重建报告.md`，项目版本更新为 `v1.0.1`。

## [2026-06-09] maintenance | P43 Wiki 与 Book 分轨保护

- 新增 `00_项目说明/Wiki与Book分轨规则.md` 和 `00_项目说明/P43_Wiki与Book分轨保护报告.md`，把 LLM Wiki / 知识库轨与 Book / 在线教材轨分开。
- 更新 `CLAUDE.md`、`AGENTs.md`、`00_项目说明/LLM Wiki运行手册.md`、`00_项目说明/Codex技能调用矩阵.md`、`00_项目说明/插件与Skills调用说明.md`、`00_项目说明/知识库使用说明.md` 和本地 `.claude/skills/`，明确 Wiki 轨默认不更新 `book/` 或 `chapters/chapter-XX/正文.md`。
- 本轮不运行 `tools\sync_online_book.py`、`tools\validate_online_book.py` 或 MkDocs build；只运行 Wiki/schema 级验收。
- 项目版本更新为 `v1.0.2`，在线书版本保持 `v1.0.1-source-refresh`。
