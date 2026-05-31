---
title: "AI_MD LLM Wiki 操作日志"
created: 2026-05-30
type: project-doc
status: active
topics: [type/project, status/active, llm-wiki, log]
wiki_role: maintenance
source_count: 8
last_reviewed: 2026-05-31
source_files: ["CLAUDE.md", "index.md", "00_项目说明/知识库维护报告-2026-05-31-P12-新增原始素材全库更新.md", "00_项目说明/知识库维护报告-2026-05-31-P13-第八章计算思路解析摄入.md", "00_项目说明/知识库维护报告-2026-05-31-P14-文献锚定.md", "00_项目说明/知识库维护报告-2026-05-31-P15-P19-研究知识图谱工作台.md", "00_项目说明/知识库维护报告-2026-05-31-P20-在线书籍骨架.md", "00_项目说明/知识库维护报告-2026-05-31-P21-GitHub-Pages部署配置.md"]
zotero_items: ["TPR3JY6N", "QXKW6K78", "YUMKNHSK", "Y4ARSYCQ", "V6Y5EEZL"]
bibtex_keys: ["yang_w_past_2026", "sui_targeting_2026", "shen_structure-based_2026", "tomarchio_reproducible_2026", "zhu_novo_2026"]
related: ["index.md", "00_项目说明/LLM Wiki运行手册.md"]
claims: [p11_schema_enhancement_2026_05_30, p12_reusable_skill_2026_05_30, p12_new_raw_ingest_2026_05_31, p13_chapter_8_ingest_2026_05_31, p14_literature_anchoring_2026_05_31, p15_entity_layer_2026_05_31, p16_claim_layer_2026_05_31, p17_research_workbench_2026_05_31, p18_ai_eval_suite_2026_05_31, p19_output_views_2026_05_31, p20_online_book_skeleton_2026_05_31, p21_github_pages_deploy_2026_05_31]
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
---

# AI_MD LLM Wiki 操作日志

本文件为追加式日志。新条目格式固定为：

`## [YYYY-MM-DD] operation | title`

允许的 `operation`：`ingest`、`query`、`update`、`lint`、`zotero`、`ocr`、`git`、`maintenance`。

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
