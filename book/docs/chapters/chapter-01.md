# 第 1 章 Linux、计算环境与生化文件基础

你将在电脑上建立一个课程目录，下载公开蛋白结构，并运行一个检查文件的短脚本。完成后，你应能回答三个问题：命令在哪个系统运行，输入文件在哪里，怎样让另一位同学复查这次操作。

第 1–4 章基础练习使用 Windows 和 CPU。第 5 章开始的 Linux 计算使用 WSL2。结构预测和蛋白设计的大规模推理列为选学，先完成文件检查、参数阅读和结果分析。

下面是本章最终目录。文件名相同，后续章节便能直接接着操作。

```text
ai-md/
├─ inputs/       原始公开输入
├─ outputs/      本次运行结果
├─ logs/         运行文字记录
├─ scripts/      保存后的脚本
└─ notes/        自己的判断和问题
```

## 1.1 Linux 系统介绍与安装

操作系统负责运行程序、管理文件和分配计算资源。Windows 和 Linux 是不同操作系统；Ubuntu 是一种 Linux 发行版。终端是输入文字命令的窗口，shell 负责解释这些命令。Windows 的 PowerShell 和 Ubuntu 的 Bash 使用不同语法。

先在 Windows 开始菜单打开 PowerShell。输入下面的命令，确认你正在使用 PowerShell。命令中的提示符不需要输入。

```powershell
$PSVersionTable.PSVersion
```

本书按任务选择运行位置。

| 运行位置 | 本书用途 | 文件和环境在哪里 |
|---|---|---|
| Windows + PowerShell | 下载、文件检查、可视化、CPU Vina | Windows 目录和 Windows Python 环境 |
| WSL2 + Ubuntu | GROMACS 等 Linux 必修计算 | Ubuntu 文件系统和 Linux 环境 |
| 课程 Linux 服务器 | 需要更多资源的选学任务 | 服务器目录和服务器环境 |

WSL2 可以在 Windows 上运行 Linux。准备进入第 5 章前，按 [Microsoft 安装说明](https://learn.microsoft.com/en-us/windows/wsl/install) 检查系统支持情况。在管理员 PowerShell 中输入 `wsl --install -d Ubuntu`，按提示重启；首次打开 Ubuntu 时建立 Linux 用户和密码。输入密码时终端不显示字符，这是正常行为。已经装好 WSL 的学生先查看状态，不必重复安装。

```powershell
wsl --list --verbose
```

列表中 Ubuntu 的 VERSION 应为 2。随后从开始菜单打开 Ubuntu，输入下面两行。`pwd` 显示当前位置，`uname` 显示 Linux 系统信息。

```bash
pwd
uname -a
```

本章还需要 Python 3.12。已有 Python 的学生先输入 `py -3.12 --version`；找不到时，从 [Python 官方下载页](https://www.python.org/downloads/windows/) 安装 Python install manager，再重新打开 PowerShell。使用管理器安装 3.12 并检查；已经能运行 3.12 的学生跳过安装。安装器和旧版 launcher 的区别见 [Windows 官方说明](https://docs.python.org/3/using/windows.html)。

```powershell
py install 3.12
py -3.12 --version
```

先完成 Windows 基础练习，WSL 安装可在进入分子动力学前完成。

## 1.2 Linux 目录结构与路径管理

路径说明文件的位置。`C:\coursework\ai-md\inputs\3htb.pdb` 是 Windows 绝对路径；在 `ai-md` 目录内，`inputs/3htb.pdb` 是相对路径。相对路径从当前目录开始寻找文件。错误目录常使正确命令报“文件不存在”。

当前工作目录决定相对文件路径从哪里开始。`PATH` 则是系统查找程序时依次搜索的目录列表；输入 `python` 或 `gmx` 这样的程序名时会用到它。已安装却提示找不到命令，先确认程序位置、安装环境和 PATH；输入完整可执行文件路径可以直接调用该程序。

在 PowerShell 中建立课程目录，再进入它。以后本书的 Windows 命令默认从这个目录运行。

```powershell
New-Item -ItemType Directory -Force C:\coursework\ai-md
Set-Location C:\coursework\ai-md
New-Item -ItemType Directory -Force inputs,outputs,logs,scripts,notes
Get-Location
Get-ChildItem
```

你应看到五个子目录。可选择其他位置，但记录你的实际项目目录，避免将文件散放在下载目录中。

打开在线书的“练习资源”页，下载第 1 章 ZIP，将解压目标选为 `C:\coursework`。解压后应看到 `C:\coursework\AI_MD_practice\chapter-01\assets`。这个目录保存课程资源；本书的输入、输出和脚本仍放在 `C:\coursework\ai-md` 工作区。后续章节 ZIP 也解压到同一位置。

| ZIP 内资源位置（相对于工作区） | 本章工作位置 |
|---|---|
| `../AI_MD_practice/chapter-01/assets/code/check_files.py` | `scripts/check_files.py` |
| `../AI_MD_practice/chapter-01/assets/code/requirements-teaching.txt` | `scripts/requirements-teaching.txt` |
| `../AI_MD_practice/chapter-01/assets/environment_record.tsv` | `notes/environment_record.tsv` |

在工作区的 PowerShell 中复制。`..` 表示上一级目录，这里先回到 `C:\coursework`，再找到同级的 `AI_MD_practice`。逐文件下载的学生可在浏览器保存时直接选择右列位置。

```powershell
Copy-Item ../AI_MD_practice/chapter-01/assets/code/check_files.py scripts/
Copy-Item ../AI_MD_practice/chapter-01/assets/code/requirements-teaching.txt scripts/
Copy-Item ../AI_MD_practice/chapter-01/assets/environment_record.tsv notes/
```

第 1 章 ZIP 包含上述本章文件，结构文件在 1.3 从 RCSB 下载。

| 项目 | Windows 示例 | WSL 示例 |
|---|---|---|
| 课程目录 | `C:\coursework\ai-md` | `/mnt/c/coursework/ai-md` |
| Linux 用户目录 | 无对应固定位置 | `~`，通常位于 `/home/用户名` |
| 当前目录 | `Get-Location` | `pwd` |
| 文件列表 | `Get-ChildItem` | `ls` |
| 进入目录 | `Set-Location inputs` | `cd inputs` |

在 WSL 中，Windows 的 C 盘挂载在 `/mnt/c`。进入同一个文件夹后，数据文件可以共用，Python 环境分别建立。不要让 Windows 程序使用 Linux 的虚拟环境，或反过来使用。Linux 任务量较大时，将计算目录放在 Linux 用户目录中，运行结束后再复制需要的结果到 Windows。

```bash
cd /mnt/c/coursework/ai-md
ls inputs
mkdir -p ~/ai-md-md/inputs ~/ai-md-md/outputs ~/ai-md-md/logs
```

Linux 文件名区分大小写。`3HTB.pdb` 与 `3htb.pdb` 可是两个文件。本书保存为小写 `3htb.pdb`，后面沿用这一名称。`~` 表示当前 Linux 用户目录，`/root` 是管理员 root 的目录，普通课程练习不使用它。

## 1.3 常用命令与文本查看

命令通常由程序名、选项和对象组成。下面先下载一个真实结构，再查看文件头。3HTB 是含有 2-propylphenol 配体的 T4 lysozyme L99A/M102Q 晶体结构，后续三章继续使用它。

```powershell
Invoke-WebRequest -Uri https://files.rcsb.org/download/3HTB.pdb -OutFile inputs/3htb.pdb
Get-Item inputs/3htb.pdb
Get-Content inputs/3htb.pdb -TotalCount 12
```

文件开头应有 `HEADER`、`TITLE` 等记录，而非网页的 `<html>`。网络下载失败时，可从 [公开课程文件](../assets/chapter-03/data/3htb/3htb.pdb) 保存同名文件到 `inputs`。结构出处见 [RCSB 3HTB](https://www.rcsb.org/structure/3HTB)。

常用动作可以这样对应。

| 动作 | PowerShell | Bash |
|---|---|---|
| 查看前 12 行 | `Get-Content file.txt -TotalCount 12` | `head -n 12 file.txt` |
| 查看最后 20 行 | `Get-Content file.txt -Tail 20` | `tail -n 20 file.txt` |
| 找关键词 | `Select-String -Path file.txt -Pattern ERROR` | `grep ERROR file.txt` |
| 复制文件 | `Copy-Item input.pdb inputs/` | `cp input.pdb inputs/` |
| 建目录 | `New-Item -ItemType Directory outputs/run-01` | `mkdir -p outputs/run-01` |

先下载 [check_files.py](../assets/chapter-01/code/check_files.py)，放入 `scripts`。用 Python 3.12 运行它，它会统计文件大小、哈希和 PDB 记录数。哈希是根据文件内容计算出的标识，内容发生变化，哈希通常也会改变。

```powershell
py -3.12 scripts/check_files.py --inputs inputs --out outputs/file-check
Get-Content outputs/file-check/input_inventory.tsv
Get-Content outputs/file-check/environment.json
```

成功时输出目录中有两个文件。`input_inventory.tsv` 每行对应一个输入，`environment.json` 记录 Python 和系统类型。脚本只统计记录，不修改输入。对于当前官方 3HTB 文件，蛋白 `ATOM` 记录为 1364，包含替代位置；`HETATM` 记录为 244。第 3 章将解释怎样从这些记录准备计算体系。

现在做一次路径对照。先进入 `notes`，用同样相对路径运行，观察 Python 找不到脚本；再回到上一级，重新运行并确认结果。

```powershell
Set-Location notes
py -3.12 scripts/check_files.py --inputs inputs --out outputs/file-check
Set-Location ..
py -3.12 scripts/check_files.py --inputs inputs --out outputs/file-check
```

排错时先核对当前目录和文件名，再看错误末行。不要一看到错误便重新安装所有软件。`sudo` 提升 Linux 权限，`chmod` 修改文件权限，两者都不是通用修复命令。本章的下载和文件清单练习无需管理员权限。

## 1.4 Conda、pip、CUDA 与基础环境搭建

Python 环境包含解释器和当前项目使用的包。RDKit 处理分子，Meeko 准备对接输入，Gemmi 处理结构数据；它们属于依赖。不同任务可能需要不同版本，用独立环境可以减少版本冲突。

本书 Windows CPU 路线使用 Python 自带的 `venv`。在课程目录创建 `.venv-win` 后，直接调用其中的 Python，无需修改 PowerShell 执行策略。

```powershell
py -3.12 -m venv .venv-win
.\.venv-win\Scripts\python.exe --version
.\.venv-win\Scripts\python.exe scripts/check_files.py --inputs inputs --out outputs/file-check-venv
```

[venv 官方文档](https://docs.python.org/3/library/venv.html) 说明环境与解释器的关系。后续命令写出的解释器路径表示“使用本项目环境”，应保留这部分。

第 3–4 章需要化学和绘图包。下载 [requirements-teaching.txt](../assets/chapter-01/code/requirements-teaching.txt) 到 `scripts`，再安装和检查。固定依赖来自本书实际验证环境；更新版本后应另存记录。

```powershell
.\.venv-win\Scripts\python.exe -m pip install -r scripts/requirements-teaching.txt
.\.venv-win\Scripts\python.exe -m pip check
.\.venv-win\Scripts\python.exe -m pip freeze > logs/python-packages.txt
```

`pip check` 应没有依赖冲突。安装失败时保留最后的错误文字、Python 版本和包名。`No matching distribution` 常与版本或平台不匹配有关；网络超时先检查下载连接。通过 `python -m pip` 安装，可确保安装到这一个 Python 环境中。[pip 官方指南](https://pip.pypa.io/en/stable/user_guide/) 提供命令说明。

| 工具 | 管理什么 | 本书使用方式 |
|---|---|---|
| venv | Python 虚拟环境 | Windows 基础练习主线 |
| pip | Python 包 | 向指定环境安装包 |
| Conda | 环境和跨语言依赖 | 个别工具按官方要求选用；不与主线重复安装 |
| apt | Ubuntu 系统软件包 | WSL 中安装 Linux 工具时使用 |
| CUDA 和显卡驱动 | NVIDIA GPU 计算软件栈 | GPU 选学任务再按工具要求配置 |

CPU Vina 和本书的文件、轨迹分析练习无需 CUDA。GPU 任务开始前才检查 `nvidia-smi`、显存和模型所需框架。驱动版本、CUDA 工具包版本与框架自带运行库是不同项目，不能只凭一个版本号判断全部兼容性。

## 1.5 Jupyter、VS Code 与 SSH 远程工作

编辑器用于写文件，Python 解释器负责执行。用 VS Code 打开课程目录，创建 `scripts/hello.py`，输入下面两行并保存。也可用其他纯文本编辑器，文件后缀必须为 `.py`，不能变成 `.py.txt`。

```python
from pathlib import Path
print(Path("inputs/3htb.pdb").is_file())
```

在 PowerShell 中运行。输出 `True` 说明当前目录下找到了指定文件。

```powershell
.\.venv-win\Scripts\python.exe scripts/hello.py
```

Jupyter notebook 适合交互试算，一个单元执行后便能查看结果。它的 kernel 是执行单元的 Python 进程。使用 notebook 时核对所选解释器，并从上到下重新运行；只保留屏幕结果，可能漏掉先前单元留下的变量。

| 工作方式 | 初学者要核对什么 |
|---|---|
| 保存脚本后运行 | 文件已保存；终端位于项目目录；解释器正确 |
| notebook | kernel 正确；所有单元按顺序运行；结果可以重新生成 |
| VS Code Remote | 文件和终端确实在远程主机；环境路径属于该主机 |
| SSH | 主机、账户、端口由课程管理员提供；连接后先确认目录 |

SSH 用于登录远程电脑。得到真实账户后，管理员通常会提供形如 `ssh 用户名@主机地址` 的命令；这类字段需要替换，不应直接照抄示例。连接后运行 `pwd` 和 `python --version`，才能知道远端位置与环境。远端运行的结果保存在远端，下载后才能用本地可视化软件打开。

本书前四章无需远程账户。长计算的任务提交、后台运行和资源限制，应按课程服务器规则执行。

## 1.6 氨基酸、蛋白质与分子间相互作用

蛋白质由氨基酸残基连接形成。结构文件用残基名称、残基编号和链 ID 指明每个原子属于哪个分子片段。`ALA` 是丙氨酸三字母名，`CA` 在蛋白记录中通常表示主链 α 碳；原子名称与元素符号并非总是同一回事。

打开 3HTB 时，先识别下面几个对象。它们的坐标保存在同一个文件中，但后续处理方式不同。

| 对象 | 在 3HTB 中的记录 | 后续用途 |
|---|---|---|
| 蛋白 | auth 链 A；SEQRES 164 个残基，坐标含 163 个 | 可视化和受体准备 |
| JZ4 | auth 链 A，残基 167 | 晶体参考配体，定义口袋和重对接比较 |
| PO4 | 残基 165、166 | 磷酸根组分，准备时逐项记录 |
| BME | 残基 168 | 非蛋白组分，准备时逐项记录 |
| HOH | 残基 169–388 | 结构中的水分子 |

非共价相互作用包括氢键、静电、色散等。氢键涉及供体、氢原子、受体和合适几何；疏水效应涉及非极性分子与水环境的关系。计算软件通常通过几何条件、经验函数或物理模型处理这些因素，不能仅靠图上的两条线识别全部相互作用。

第 2 章先测量原子距离、观察邻近残基。第 3 章才决定采用哪种化学状态和组分。保持这一顺序，可以把“看见了什么”和“计算输入用了什么”对应起来。

## 1.7 PDB、SDF、MOL2 等文件格式

格式决定文件保存哪些信息，也决定软件能读取什么。蛋白坐标和小分子化学结构有不同需求，改扩展名不会完成格式转换。

| 格式 | 常见内容 | 初学者的检查重点 |
|---|---|---|
| FASTA | 序列和序列标题 | 字母、长度、是否含缺失或非法字符 |
| PDB / mmCIF | 原子坐标、链、残基及结构信息 | 模型、链编号、缺失、替代位置、配体 |
| SDF | 小分子原子、键、坐标和属性 | 键级、手性、形式电荷、3D 坐标 |
| MOL2 | 原子、键及类型等信息 | 类型约定和电荷来源是否适合目标软件 |
| SMILES | 分子的文字表示 | 键、环、手性、电荷；一般不包含 3D 坐标 |
| XYZ | 元素和坐标 | 缺少键和残基语义时，需补充来源 |
| PDBQT | 对接所需原子类型、电荷和配体扭转信息 | 必须由准备过程生成，不能只改 PDB 后缀 |

PDB 中 `ATOM` 多用于标准聚合物原子，`HETATM` 多用于非标准残基、水和小分子；这两类记录不能直接等同于“保留”和“删除”。mmCIF 是 PDB 档案的主要格式，具有更完整的字段与标识。3HTB 本章使用旧式 PDB 文件，以便初学者直接阅读固定列。

小分子优先从有键信息的 SDF 开始准备。晶体配体坐标用于姿势比较，CCD 的理想坐标用于独立准备；二者用途不同，第 3 章会分别保存。查看格式时还要记录来源和处理步骤，避免把转换后的文件误当原始结构。

## 1.8 生化计算数据库与硬件要求

本书主线先使用结构数据库和化学组分字典。查询蛋白序列、预测结构或更大的化合物集合时，再增加其他数据库。

| 需求 | 官方入口 | 记录内容 |
|---|---|---|
| 实验结构 | [RCSB PDB](https://www.rcsb.org/) | PDB ID、方法、分辨率、链、配体、下载日期 |
| 蛋白序列与注释 | [UniProt](https://www.uniprot.org/) | accession、物种、序列版本 |
| 预测蛋白结构 | [AlphaFold DB](https://alphafold.ebi.ac.uk/) | 模型 ID、序列、置信度和版本 |
| PDB 中的小分子组分 | [RCSB CCD](https://www.rcsb.org/ligand/JZ4) | CCD ID、名称、SMILES、形式电荷 |
| 化合物信息 | [PubChem](https://pubchem.ncbi.nlm.nih.gov/) | CID、结构、来源和下载规则 |

CPU 是通用处理器，GPU 适合部分并行计算。内存保存运行中的数据，磁盘保存文件，显存属于 GPU。本书实际的三分子 CPU Vina 练习每个分子用数秒至十余秒；这个数字对应本书记录中的一个小体系，学生电脑的速度会不同。先完成小批次，记录时间和磁盘占用，再决定是否扩大任务。

本章交付四项内容。

- `inputs/3htb.pdb`，能看到正常 PDB 文件头。
- `outputs/file-check/input_inventory.tsv` 和 `environment.json`，记录不为空。
- 保存后的 `scripts/hello.py`，运行输出 `True`。
- 填好的 [environment_record.tsv](../assets/chapter-01/environment_record.tsv)，注明实际系统、解释器和状态。

这些记录可以交给同学复跑。对照练习中，再说明错误目录如何导致失败，以及你怎样修正路径。

## 本章方法适用范围与结果解释

文件存在、脚本返回成功、记录数正确，说明本次文件和运行过程可以继续核对；它们不评价蛋白结构或化学状态是否适合研究问题。数据库中的实验结构、预测模型和计算输出分别保留其来源。接触距离是几何观察，后续的结合、机制和药效判断还需要相应方法与实验。第 2 章将使用同一个 3HTB 文件，把文件清单落实为可查看的链、配体和口袋。
