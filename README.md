# AI 辅助药物设计

《AI 辅助药物设计：从分子建模到研究工作台》面向药学、药物化学和生命科学学生。课程从普通 Windows 电脑起步，逐步学习结构查看、CPU 对接、短分子动力学模拟、结果分析和蛋白设计工作流。

[阅读在线书](https://luvega.github.io/AI_MD/) · [下载练习](https://luvega.github.io/AI_MD/resources/)

## 学习路线

第 1—4 章从建目录走到一次真实对接。第 5—8 章进入模拟、轨迹、自由能结果和 AI 输出分析。第 9—11 章练习骨架、序列、候选筛选与批处理，第 12 章写出项目路线。每章安排基础任务和对照练习，高成本计算作为选学。

## 项目文件

| 位置 | 用途 |
|---|---|
| `大纲.md` | 全书 12 章结构与实践安排 |
| `chapters/` | 章节大纲、正文、审核后的公开资源 |
| `book/` | 由章节正文生成的在线书发布层 |
| `00_项目说明/` | 实施计划、逐章进度和验证记录 |
| `02_方法笔记/`、`03_文献笔记/` | 方法与文献资料 |

录播视频、课程 PPT、讲义 PDF 及其直接转制文件只留在本地备课。公开教材采用独立编写的文字、原创图示、公开数据或独立计算结果，教学构造样例另作标识。

## 本地构建

安装 `book/requirements.txt` 中的依赖后运行下列命令。发布资产由 `chapters/public_assets.tsv` 逐项审核，新增文件不会自动进入网站。

```text
python tools/sync_online_book.py
python tools/validate_online_book.py
python -m pytest -q
python -m mkdocs build -f book/mkdocs.yml --strict
```

当前教学改进与实跑状态见[实施记录](00_项目说明/在线书完善实施记录-2026-10-02.md)。

新增练习资源时，先审核来源、许可和实际输出，更新该章 `assets/provenance.tsv`，再运行 `python tools/refresh_public_assets.py` 刷新两份资源清单。文件修改后必须重新核对哈希；同步器会拒绝未审核或字节不一致的文件。

同步器同时生成 `book/docs/downloads/chapter-01.zip` 至 `chapter-12.zip`，并更新资源页的压缩包大小。每包从审核清单取文件，按 `shared/assets/practice-downloads.json` 的依赖表补齐配套章节，保留 `AI_MD_practice/chapter-XX/assets/` 目录。验收器检查 12 包齐备、成员路径、文件集合和原始字节；原始课程压缩包仍禁止发布。生成的 ZIP 不纳入 Git，GitHub Pages 工作流每次同步时重建。
