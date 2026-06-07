---
title: "知识库维护报告 2026-05-31 P21 GitHub Pages 部署配置"
created: 2026-05-31
type: maintenance-report
status: complete
topics: [type/project, status/complete, maintenance, github-pages, online-book, mkdocs]
wiki_role: maintenance
source_count: 6
last_reviewed: 2026-05-31
source_files: [".github/workflows/deploy-book.yml", "book/mkdocs.yml", "book/book_map.toml", "tools/validate_online_book.py", "book/docs/index.md", "00_项目说明/知识库维护报告-2026-05-31-P20-在线书籍骨架.md"]
zotero_items: ["TPR3JY6N", "QXKW6K78", "YUMKNHSK", "Y4ARSYCQ", "V6Y5EEZL"]
bibtex_keys: ["yang_w_past_2026", "sui_targeting_2026", "shen_structure-based_2026", "tomarchio_reproducible_2026", "zhu_novo_2026"]
related: ["../index.md", "../log.md", "P40_旧版在线图书删除记录.md", "知识库维护报告-2026-05-31-P20-在线书籍骨架.md"]
claims: [p21_github_pages_deploy_2026_05_31]
relations:
  - type: updates
    target: "../index.md"
  - type: updates
    target: "../log.md"
  - type: updates
    target: "P40_旧版在线图书删除记录.md"
  - type: extends
    target: "知识库维护报告-2026-05-31-P20-在线书籍骨架.md"
---

# 知识库维护报告 2026-05-31 P21 GitHub Pages 部署配置

## 本轮目标

把 P20 在线书籍骨架接入 GitHub Pages 自动部署，目标仓库为 `https://github.com/luvega/AI_MD.git`，发布 URL 为 `https://luvega.github.io/AI_MD/`。

## 新增和更新

| 文件 | 说明 |
|:---|:---|
| `.github/workflows/deploy-book.yml` | GitHub Actions workflow：安装依赖、运行在线书籍测试、校验 `book_map.toml`、执行 MkDocs strict build，并上传 `book/site` 到 Pages。 |
| `book/mkdocs.yml` | 新增 `site_url: "https://luvega.github.io/AI_MD/"`。 |
| `00_项目说明/知识库使用说明.md` | 增加 GitHub Pages 远端、站点 URL、workflow 路径和推送前校验要求。 |
| `index.md` / `log.md` / `00_项目说明/_index.md` | 增加 P21 部署配置入口。 |

## GitHub 设置要求

在 GitHub 仓库页面完成一次性设置：

1. 打开 `Settings -> Pages`。
2. `Build and deployment -> Source` 选择 `GitHub Actions`。
3. 推送 `master` 后在 `Actions` 标签页查看 `Deploy online book`。
4. 部署成功后访问 `https://luvega.github.io/AI_MD/`。

## 推送前校验

本地推送前至少运行：

```powershell
python -m unittest tests.test_validate_online_book
python tools/validate_online_book.py --map book/book_map.toml --book-root book/docs
python -m mkdocs build -f book/mkdocs.yml --strict
```

## 边界

- `book/site/` 是构建产物，保留在 `.gitignore`，不提交。
- workflow 只发布在线书籍静态站点，不发布原始 PDF、压缩包、Office 文件或 Zotero PDF。
- 首版仍是课程讲义骨架；公开传播前需要单独做版权、图表和路径脱敏审查。
