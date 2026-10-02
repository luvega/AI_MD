# AI 辅助药物设计：从分子建模到研究工作台

这本书面向第一次接触分子建模的药学、药物化学和生命科学学生。准备一台 Windows 电脑，从查看结构开始，逐步完成一次对接、短模拟和结果分析。每章都有可以亲手完成的任务，进阶计算另作安排。

## 从这里开始

1. 打开[第 1 章](chapters/chapter-01.md)，建立练习目录，认清命令应在哪个窗口输入。
2. 按[第 2 章](chapters/chapter-02.md)下载 3HTB 结构，找到配体 JZ4，保存自己的口袋图。
3. 完成[第 3 章](chapters/chapter-03.md)准备后，进入[第 4 章](chapters/chapter-04.md)运行 CPU 对接，检查输出 pose。
4. 继续[第 5 章](chapters/chapter-05.md)的短模拟，并在[第 6 章](chapters/chapter-06.md)整理轨迹、绘图。

需要 Linux 的计算在 WSL2 的 Ubuntu 窗口完成。桌面分子软件的命令输入其自身命令栏。安装每种工具前，先确认这一章要用它完成哪个任务。

## 下载练习 {#practice-download}

[练习资源页](resources.md)每章提供一个压缩包，说明、输入、脚本和已有结果放在一起，所需的前置文件也已包含。

1. 选择正在学习的章节，点击“下载本章资源”。
2. 在 Windows 中右键压缩包，选择“全部提取”，把目标文件夹改为 `C:\coursework`。
3. 检查解压目录。例如第 4 章应出现 `C:\coursework\AI_MD_practice\chapter-04\assets`；打开本章说明，再按正文操作。

多章解压到同一个 `C:\coursework` 即可，保留 `AI_MD_practice` 下的章节目录。第 1–4 章会把需要的文件复制到 `C:\coursework\ai-md` 工作目录；后续章节在各自的 `assets` 目录运行。WSL2 中对应资源位置是 `/mnt/c/coursework/AI_MD_practice`。

下载完成后先阅读该章的练习说明。运行时从练习目录开始，保留日志和自己的输出。对照练习会让你改变一个条件，再检查差异。

## 必修与选学

| 学习阶段 | 必修任务 | 完成后继续 |
|---|---|---|
| 第 1—4 章 | 环境与文件、结构查看、输入准备、CPU 小规模对接 | 多分子批量、PPI 与 GPU 筛选 |
| 第 5—8 章 | 短 MD、轨迹图、自由能结果读取、AI 输出字段分析 | 完整自由能重算和模型推理 |
| 第 9—11 章 | 官方骨架与序列阅读、候选检查、批处理故障恢复 | GPU 生成、回折叠与更大批次 |
| 第 12 章 | 写出自己的项目路线卡 | 根据课题安排计算和实验 |

## 章节目录

- [第 1 章 Linux、计算环境与生化文件基础](chapters/chapter-01.md)
- [第 2 章 PyMOL、ChimeraX 与结构可视化](chapters/chapter-02.md)
- [第 3 章 结构建模、结合位点与体系准备](chapters/chapter-03.md)
- [第 4 章 分子对接与虚拟筛选](chapters/chapter-04.md)
- [第 5 章 分子动力学模拟基础流程](chapters/chapter-05.md)
- [第 6 章 轨迹分析、构象解释与 AI 采样](chapters/chapter-06.md)
- [第 7 章 结合自由能与 MM/PBSA 计算](chapters/chapter-07.md)
- [第 8 章 AI 亲和力预测与模型评估](chapters/chapter-08.md)
- [第 9 章 生成式蛋白设计基础](chapters/chapter-09.md)
- [第 10 章 RFD3、ProteinMPNN 与多类型设计任务](chapters/chapter-10.md)
- [第 11 章 VibeCoding、Claude Code 与 AI Agent 工作流](chapters/chapter-11.md)
- [第 12 章 研究思路解析与项目工作台](chapters/chapter-12.md)
