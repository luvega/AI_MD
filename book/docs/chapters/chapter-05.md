# 第 5 章 分子动力学模拟基础流程

## 本章导读

第 4 章得到一个静态构象。要继续观察原子怎样随时间移动，需要先把结构、力场、溶剂和运行条件装配成一个完整体系。本章从公开蛋白 1AKI 开始，不加入小分子。这样可以先学会检查输入和日志，再处理配体参数。

这次练习采用 AMBER99SB/TIP3P，完成能量最小化、20 ps NVT、20 ps NPT 和 100 ps MD。已经准备好的五份参数文件可以直接下载；每一步的输入、输出和停止条件都要核对。

| 你要完成的操作 | 交付文件 | 怎么核对 |
|---|---|---|
| 选择蛋白链并生成拓扑 | protein.pdb、protein.gro、topol.top | 链、残基、原子数量与处理记录一致 |
| 加盒、水和离子 | system.gro、更新的 topol.top | 分子数量与坐标中的组分对应 |
| 分阶段运行 | em/nvt/npt/md 的日志、坐标和 checkpoint | 上一步正常结束后再使用其输出 |
| 把结果交给第 6 章 | md.tpr、md.xtc、md.edr、命令记录 | 轨迹可读，时间范围与参数一致 |

## 练习目录

从[练习资源页](https://luvega.github.io/AI_MD/resources/)下载本章压缩包，解压到 `C:/coursework`。以下命令从 `C:/coursework/AI_MD_practice` 开始。先进入本章目录，后续 Python 命令都从这里运行，结果写入 `outputs`。

```bash
cd chapter-05/assets
```

## 5.1 分子模拟基本概念、软件和力场

先做一个预测。如果只给 GROMACS 一个 PDB，软件能否知道每个原子的电荷、原子类型、键和非键相互作用参数？PDB 主要描述坐标与结构标识，力场和拓扑还需要另行提供。`pdb2gmx` 会根据它认识的标准残基生成这些信息。

MD 按给定势能函数计算力，并用数值积分更新坐标和速度。时间步长决定一次更新跨越多少时间；总时长等于步数乘以步长。本练习的 `dt = 0.002` ps、`nsteps = 50000`，相乘得到 100 ps，即 0.1 ns。

| 对象 | 本练习的选择 | 你要亲手检查的字段 |
|---|---|---|
| 蛋白力场 | GROMACS 自带 amber99sb | pdb2gmx 的 `-ff` 与生成的 include |
| 水模型 | TIP3P | `-water tip3p` 与拓扑水模型 |
| 盐浓度 | 0.15 mol/L，并中和净电荷 | genion 的 `-conc`、`-neutral` 与离子数量 |
| 温度、压力 | 300 K、1 bar | MDP 的 ref-t、ref-p |
| 约束 | 与氢原子相连的共价键长度约束 | constraints、LINCS 设置 |

把水模型改成另一种以后，不能只修改记录表。需要重新生成匹配的拓扑和坐标。先用本章一致的参数完成一次练习，再在新目录比较更改参数的影响。

## 5.2 GROMACS 文件类型：gro、xtc、mdp、top、itp

先按下列命令进入下载包的本章目录，再把 [1AKI 练习包说明](../assets/chapter-05/practice/1aki/README.md) 打开。不要立即运行；先找出结构、参数、脚本各放在哪里。

| 扩展名 | 读什么 | 由谁生成或提供 |
|---|---|---|
| pdb | 输入坐标、链、残基与组分 | 公开数据库；本练习保留原下载文件 |
| gro | 坐标与盒矢量 | pdb2gmx、solvate、genion、mdrun |
| mdp | 积分、温压控制、输出频率 | 本章提供完整文件 |
| top / itp | 分子与力场参数、分子数量、引用文件 | pdb2gmx 或经过核验的参数化工具 |
| tpr | 本次运行合并后的输入 | grompp |
| xtc | 压缩坐标轨迹 | mdrun |
| edr / log | 能量及运行日志 | mdrun |
| cpt | 续算状态，包括运行步数等 | mdrun |
| ndx | 具名原子组 | make_ndx 或 select |

对照练习。把一份 `md.xtc` 单独放进空目录，再尝试分析。你缺少原子名称、质量、连接关系及参考结构。把与它对应的 `md.tpr` 放回来，才能确定每帧坐标表示哪些原子。

## 5.3 拓扑文件组成

运行 `pdb2gmx` 后，用文本编辑器打开 `topol.top`。先定位 `#include`，再看文件末尾 `[ system ]` 与 `[ molecules ]`。被引用的 `.itp` 也是输入，不能只打包顶层 `.top`。

| 位置 | 你在找什么 | 常见错法 |
|---|---|---|
| forcefield.itp 引用 | 参数来自哪个力场 | 换力场后仍引用旧配体参数 |
| 蛋白分子定义 | 原子、电荷、键和相关参数 | 为通过预处理而手动删掉未知原子 |
| posre.itp 与 POSRES | 哪些原子受到位置限制 | 生产阶段仍保留未说明的限制 |
| 水与离子引用 | 水模型、NA/CL 参数 | 坐标加了离子，拓扑没有更新 |
| `[ molecules ]` | 每种分子的数量和排列 | 原子总数相同却组分或顺序不对应 |

本练习的 `solvate` 和 `genion` 都带 `-p topol.top`，会更新分子计数。比较处理前后文件末尾，记下水分子和离子数量的变化。若 `grompp` 报坐标与拓扑原子数不符，先查这个对应关系。

## 5.4 GROMACS、Sobtop、Multiwfn、ORCA 安装

Windows 学生先按第 1 章完成 Python 和目录操作。计算主线使用 Ubuntu/WSL2；已有经过核验的原生 Windows GROMACS 也可以执行同一流程。本次教材验证使用官方 v2025.5 源码构建的原生 Windows CPU 版本，实际报告为 2025.5-dev。安装路径与学生的软件源版本可以不同，均须保存版本报告。

在已经配置好的 Ubuntu 终端中，先安装 GROMACS 与 Linux Python 环境，再建立虚拟环境。以下步骤依据 [Ubuntu 软件包](https://packages.ubuntu.com/en/noble/gromacs)、[Ubuntu Python 教程](https://documentation.ubuntu.com/ubuntu-for-developers/tutorials/python-use/)与 [Python venv 文档](https://docs.python.org/3/library/venv.html)。

```bash
sudo apt update
sudo apt install gromacs python3-venv
python3 -m venv ~/.venvs/ai-md
source ~/.venvs/ai-md/bin/activate
python --version
python -m pip install matplotlib mdtraj
gmx --version
```

`sudo` 提示密码时输入 Ubuntu 用户密码，屏幕不显示字符。虚拟环境激活后，后文的 `python` 指向 Linux 环境；不要复用 Windows 的 `.venv-win`。重新打开终端后先执行 `source ~/.venvs/ai-md/bin/activate`。若 pip 提示 externally-managed-environment，先检查是否激活成功，不向系统 Python 强装依赖。

练习下载目录若在 Windows 的 `C:\coursework\AI_MD_practice`，Ubuntu 中对应 `/mnt/c/coursework/AI_MD_practice`。下面示范进入目录；换盘符或位置后相应修改路径。

```bash
cd /mnt/c/coursework/AI_MD_practice/chapter-05/assets
```

将版本输出保存到自己的运行记录。提示找不到命令时先查安装或 PATH；修改 MDP 无法解决安装错误。软件源提供什么版本就记录什么版本，自行构建按 [GROMACS 官方安装说明](https://manual.gromacs.org/current/install-guide/index.html) 保留配置。

| 工具 | 在本章的用途 | 什么时候才需要 |
|---|---|---|
| GROMACS | 建体系、预处理、运行和提取能量 | 1AKI 主线必需 |
| Sobtop | 小分子拓扑准备的可选入口 | 第 5.9 节开始处理非标准配体时 |
| Multiwfn | 波函数分析、电荷等辅助工作 | 已选定电荷计算方案时 |
| ORCA | 量子化学计算的可选入口 | 需要量化计算且有明确方法设置时 |

1AKI 不需要安装后三个工具。先完成纯蛋白练习，再按配体参数方案选择工具，可以减少同时排查安装、化学结构和拓扑的困难。

## 5.5 分子模拟基本流程

从下列链接取完整参数，不要从正文中的片段拼出 MDP。[ions.mdp](../assets/chapter-05/practice/1aki/mdp/ions.mdp)、[em.mdp](../assets/chapter-05/practice/1aki/mdp/em.mdp)、[nvt.mdp](../assets/chapter-05/practice/1aki/mdp/nvt.mdp)、[npt.mdp](../assets/chapter-05/practice/1aki/mdp/npt.mdp)、[md.mdp](../assets/chapter-05/practice/1aki/mdp/md.mdp)。

| 阶段 | 输入状态 | 操作目的 | 本练习设置 |
|---|---|---|---|
| EM | 加水加离子的坐标 | 降低不合理接触带来的大力 | steep，最多 5000 步，emtol 1000 |
| NVT | EM 坐标 | 保持体积，进行温度控制 | 20 ps，蛋白位置限制 |
| NPT | NVT 坐标与 checkpoint | 加入压力控制 | 20 ps，保留蛋白位置限制 |
| MD | NPT 坐标与 checkpoint | 解除 POSRES 后保存轨迹 | 100 ps，每 1 ps 写一帧 XTC |

先检查执行脚本的工作目录规则，再运行 [run-md.py](../assets/chapter-05/practice/1aki/run-md.py)。下面命令从本章 assets 目录执行，`run-1aki` 必须是空目录或尚不存在的目录。

```bash
python practice/1aki/run-md.py --gmx gmx --work outputs/run-1aki --threads 4
```

Windows 原生版本可以把 `--gmx gmx` 换成 `--gmx "C:/your-tools/gromacs/bin/gmx.exe"`；将路径替换为自己已经核验的文件。脚本每次只启动一个阶段，保存该阶段日志，遇到错误就停止。

为了理解脚本怎样交接文件，按下表在运行目录核对实际命令。`genion` 的交互输入为组名 `SOL`，不要把组号从另一台电脑照抄过来。

| 顺序 | 核心命令 | 输出检查 |
|---|---|---|
| 1 | `gmx pdb2gmx -f protein.pdb -o protein.gro -p topol.top -ignh -ff amber99sb -water tip3p` | 力场、水模型、端基、二硫键与原子数 |
| 2 | `gmx editconf -f protein.gro -o box.gro -d 1.0 -bt dodecahedron` | 盒尺寸与距边界距离 |
| 3 | `gmx solvate -cp box.gro -cs spc216.gro -o solv.gro -p topol.top` | 水分子计数 |
| 4 | `gmx grompp -f ions.mdp -c solv.gro -p topol.top -o ions.tpr` | 电荷提示与预处理是否通过 |
| 5 | `gmx genion -s ions.tpr -o system.gro -p topol.top -pname NA -nname CL -neutral -conc 0.15 -seed 20261002` | 替换 SOL，核对离子与水数量 |

`-cs spc216.gro` 提供初始水坐标；水的相互作用参数由拓扑的 TIP3P 引用决定。不能仅看坐标模板名就把本练习记录成 SPC 力场。

进入 EM 后，按照以下命令关系核对。全部在运行目录执行，每个 `grompp` 正常结束后才启动相应 `mdrun`。下面按 MPI library 为 none 的版本写命令；若版本报告 thread_mpi，mdrun 可另加 `-ntmpi 1`。提供的脚本会自动判断。

```bash
gmx grompp -f em.mdp -c system.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em -ntomp 4 -nb cpu
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt -ntomp 4 -nb cpu
gmx grompp -f npt.mdp -c nvt.gro -r em.gro -t nvt.cpt -p topol.top -o npt.tpr
gmx mdrun -deffnm npt -ntomp 4 -nb cpu
gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr
gmx mdrun -deffnm md -ntomp 4 -nb cpu
gmx check -f md.xtc
```

NPT 与 MD 通过 `-t` 读取上一步 checkpoint；NVT 用固定随机种子生成初速度。`-r em.gro` 是位置限制参考坐标，生产 MDP 不再定义 POSRES。打开五份 MDP，把这些差别逐项圈出来。

| 实际现象 | 先检查什么 | 本次练习怎么处理 |
|---|---|---|
| grompp 报 unknown residue | 原子与残基名称、力场支持范围 | 回到结构准备，保留错误日志 |
| 坐标与拓扑数量不符 | topol.top 的 molecules 与当前 gro | 找到最后一次改组分的步骤 |
| 预处理出现 warning | 完整警告文字和对应参数 | 查明原因后修改；不加 maxwarn 跳过 |
| LINCS warning 或能量异常 | 初始接触、约束、步长、参数 | 停止运行，先核对 EM 和输入 |
| 模拟中断 | checkpoint 与此前运行参数 | 在复制的续算目录使用匹配 cpt，不覆盖原记录 |

本次独立验证的 15 条命令均退出 0。EM 在 409 步达到 Fmax < 1000 kJ·mol⁻¹·nm⁻¹，实际最大力为 966.43744；生产轨迹含 0–100 ps 的 101 帧。核对 [运行记录](../assets/chapter-05/practice/1aki/verified-run/run-record.json)与[轨迹检查](../assets/chapter-05/practice/1aki/verified-run/trajectory-check.stdout.log)，再在自己的结果中找到对应数字。

提交时附 `command-log.tsv`，并指出每一步退出码。达到最大步数与达到力阈值是两种不同 EM 结束原因。温度、压力、密度曲线的读取放在第 6 章；暂不运行的学生可直接下载该章匹配的完整轨迹与输入，先练分析。

## 5.6 蛋白结构预处理

先用第 2 章学过的可视化工具打开原始 1AKI，再打开脚本生成的 `protein.pdb`。脚本仅保留 A 链 ATOM，选择空白或 A alternate location。这个选择是本练习的确定规则；换蛋白时必须重新判断哪些组分需要留下。

| 对照对象 | 要记录的变化 | 自己动手检查 |
|---|---|---|
| 原始 PDB → protein.pdb | 链、HETATM、水、替代构象 | 数清留下的链，定位是否有缺失残基 |
| protein.pdb → protein.gro | 氢原子、端基、残基名称 | 查看 pdb2gmx 日志与结构 |
| solv.gro → system.gro | 水被离子替换 | 对照 genion 日志和拓扑末尾 |

不要把“删掉所有 HETATM”当作日后预处理规则。先在复制的练习目录故意保留一个力场不认识的组分，预测程序会在哪一步停止；运行后对照报错，说明是化学组分未参数化还是文件损坏。不要把这个改错目录混入正式结果。

## 5.7 蛋白、多肽和蛋白复合物模拟

完成 1AKI 后，选学可打开第 10 章公开的 [PDL1 A/B 复合物模型](../assets/chapter-10/data/pdl1_test_0_model_0.pdb)，先练习链与组分检查。第 4 章必修的 3HTB/JZ4 是蛋白–小分子体系，不能把它当成蛋白–蛋白输入。列出每条链、末端状态、二硫键和链间接触，再决定参数准备顺序。

| 体系 | 与 1AKI 相比新增的问题 | 下一步操作 |
|---|---|---|
| 单链蛋白 | 缺环、缺侧链、质子化状态 | 核对缺失区与建模来源 |
| 多肽 | 端基、序列、二硫键及较大柔性 | 确认是否封端，给末端标注 |
| 蛋白复合物 | 链定义、接触面、限制方案 | 检查两条链是否都进入拓扑与盒 |

对照练习。在两个副本中分别保留所有链与只留一条链，比较生成的拓扑。用文件中的组分差别说明哪一份代表你要研究的复合物。

## 5.8 蛋白-金属离子体系模拟

金属先按功能区分。溶液中的游离离子、结构金属和参与催化的金属不能自动使用同一处理方式。打开结构，记录元素、可能价态、配位原子和距离，再决定参数来源。

| 准备字段 | 可以怎样核对 | 缺失时停在哪一步 |
|---|---|---|
| 金属元素与价态 | 结构条目、实验注释、化学环境 | 参数选择前 |
| 配位残基与几何 | 第 2 章距离测量与结构检查 | 体系处理前 |
| 非键或键合模型 | 对应力场/参数文档及适用体系 | 拓扑生成前 |
| 参数和限制来源 | 原始文件、版本与生成记录 | grompp 前 |

练习只交付金属准备表。把金属删掉后程序可能更容易通过，但体系已经改变；请在表中写明删除改变了哪些接触和组分，再决定是否保留这种建模假设。

## 5.9 蛋白-小分子体系模拟

3HTB/JZ4 已在前两章完成查看和对接。此时可以继续使用公开结构做参数准备，但 Vina 的 PDBQT 不能直接代替 MD 小分子拓扑。配体的电荷、键、原子类型和参数还需要与蛋白力场配合。

| 顺序 | 操作 | 检查产物 |
|---|---|---|
| 1 | 从公开 SDF 核对 JZ4 化学结构 | 名称、SMILES、质子化状态、电荷 |
| 2 | 选择与蛋白参数方案兼容的小分子力场 | 方法与版本记录 |
| 3 | 生成配体参数和坐标 | ligand.itp 与配体原子顺序 |
| 4 | 合并复合物坐标与拓扑 | 配体原子数、include、molecules |
| 5 | grompp 后再做 EM | 预处理日志与大力位置 |

本章不把未生成的 JZ4 参数写成已运行结果。作业先比较晶体配体与对接配体的重原子顺序、氢原子和净电荷；记录还缺哪份参数。准备齐全后才能沿用 5.5 的分阶段流程。

## 5.10 蛋白-核酸、多配体和修饰残基体系

复杂体系先列清组分，再查支持范围。核酸需要核对糖、碱基、端基和序列；多配体需要逐种写拓扑；修饰残基需要明确原子、键、电荷与参数来源。

| 体系 | 最先检查的对应关系 | 可交付的准备结果 |
|---|---|---|
| 蛋白–DNA/RNA | 链与序列、端基、所选核酸参数 | 组分表与参数引用 |
| 多配体 | 每种配体坐标、拓扑及数量 | 文件对应表 |
| 共价修饰或非标准残基 | 键连接、质子与残基模板 | 化学结构和参数待办 |
| 金属/辅因子共同存在 | 配位与其他组分是否相互影响 | 分别核验后合并的体系说明 |

章末交付。1AKI 输入与原始下载来源、五份 MDP、命令记录、日志，以及与 `md.tpr` 匹配的 `md.xtc`。再填写一张复杂体系准备表，指出自己尚未解决的参数问题。第 6 章用真实轨迹检查图像与数值是否对应。

## 本章方法范围

这次短运行确认的是所记录环境下的建体系、阶段运行和文件交接过程。20 ps 平衡与 100 ps MD 不能代替针对研究问题设计的充分平衡、采样与重复运行；一段轨迹或顺利结束的日志也不能证明结合亲和力、药效或机制。复杂组分未完成参数核验时，应保留准备结果和待办，不继续把它标为已完成模拟。
