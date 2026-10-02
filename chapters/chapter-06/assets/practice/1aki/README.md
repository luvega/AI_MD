# 1AKI 真实短轨迹与分析

本目录来自第 5 章公开 [1AKI](https://www.rcsb.org/structure/1AKI) 输入的独立 GROMACS 运行，未使用课程轨迹。EM、20 ps NVT、20 ps NPT 和 100 ps MD 已完成；15 条运行命令、26 条 GROMACS 分析命令均退出 0。原始生产轨迹包含 0–100 ps 的 101 帧，每 1 ps 一帧。

实际构建使用官方 GROMACS v2025.5 源码，版本报告为 2025.5-dev；原生 Windows CPU、SIMD NONE、MPI none、4 个 OpenMP 线程。参数为 amber99sb/TIP3P、300 K、1 bar，完整设置与输入 SHA256 见 `run-record.json`。全体系 23873 个原子，蛋白 1960 个原子，129 个 C-alpha。

## 先找到文件

| 文件或目录 | 作用 |
|---|---|
| md.tpr、md.xtc、md.cpt | 匹配的完整生产输入、原始轨迹与 checkpoint |
| nvt.edr、npt.edr、md.edr | 温度、压力、密度与能量数据 |
| run-inputs | protein.pdb、system/em/nvt/npt 坐标、拓扑、位置限制、阶段 checkpoint 与五份实际 MDP |
| run-logs | 实际阶段日志、运行命令和轨迹检查 |
| md-whole/center/fit.xtc | 分子完整、居中与拟合后的全体系轨迹 |
| md-reference0.pdb、md-last.pdb | 0 ps 与 100 ps 全体系参考 |
| analysis-commands.tsv、analysis-record.json | 分析命令、原子组、版本、输入校验值 |
| rmsd/rmsf/gyrate/sasa 等 XVG | 原始分析数值与轴信息 |
| pca-2d.xvg、eigenvalues.xvg、eigenvectors.trr | 真实 PCA 投影与基底 |
| cluster.log、representative-first-cluster.pdb | 簇成员与 11 ps 的 Protein 代表构象 |
| fel.xpm、sham.log | GROMACS sham 的真实输出 |
| pca-frequency | 从相同 PC1/PC2 重新统计的频数、相对值、图与记录 |
| dccm | 对齐 C-alpha 位移得到的 129×129 矩阵、图与记录 |
| figures | 原始曲线、参考对照、RMSF、氢键/DSSP 与温压密度图 |

`topol.top` 仍引用 GROMACS 自带 amber99sb.ff 文件。重新预处理需要安装相应力场文件；读取已配对的 tpr/xtc 不需要自行补造拓扑。完整原始和处理后轨迹都保留，不把 Protein-only 轨迹套入全体系 tpr。

## 从下载目录开始

下面命令从下载目录（例如 C:/coursework/ai-md/downloads）开始，进入 chapter-06/assets。Ubuntu/WSL 先激活第 5.4 节的 Linux venv；在 Ubuntu 中示例路径为 `/mnt/c/coursework/ai-md/downloads`。Windows 原生环境使用第 1 章配置的 Python。

```bash
cd chapter-06/assets
python code/plot-xvg.py practice/1aki/rmsd-ca.xvg practice/1aki/gyrate.xvg --outdir outputs/full
python code/plot-xvg.py practice/1aki/rmsd-ca.xvg --xmin 50 --xmax 100 --outdir outputs/last-half
```

脚本保留真实行数、SHA256、区间与原始标签，不平滑。裁剪前有 101 个时间点，50–100 ps 包含端点时应为 51 个。先预测，再运行并核对记录。

已装 GROMACS 后，可从完整数据重提取。输出目录须为空或不存在。当前原生氢键/DSSP 接口可用时加 `--native-secondary`；旧版先完成基础步骤，不加该选项。

Ubuntu 软件源可能提供旧 GROMACS，无法读包内 2025.5 TPR。出现版本报错时，从配套输入重建本机分析文件；不读取新版 cpt、不重跑轨迹，原始生产 tpr 保留。以下命令从 chapter-06/assets 执行。

```bash
mkdir -p outputs/local-tpr
cd practice/1aki/run-inputs
gmx grompp -f md.mdp -c npt.gro -p topol.top -o ../../../outputs/local-tpr/analysis-local.tpr -po ../../../outputs/local-tpr/processed.mdp
cd ../../..
python code/analyze-md.py --gmx gmx --run practice/1aki --tpr outputs/local-tpr/analysis-local.tpr --out outputs/analysis-local
```

重建文件只用于分析，不能当作带 checkpoint 的生产续算输入。遇到警告或原子数/顺序不符先停止，不用 maxwarn。`analysis-local-rebuild-record.json` 记录当前 2025.5-dev 的实际验证，预处理无警告、23873 个残基/原子标识及顺序一致，完整替代输入分析成功；Ubuntu 旧版本未在本机实际执行。

版本可直接读取原始 tpr 时才运行下面第一条命令。PCA 频数图与 DCCM 则用已配对的公开文件，依照本章 Python 环境运行。

```bash
python code/analyze-md.py --gmx gmx --run practice/1aki --out outputs/analysis
python code/plot-pca-frequency.py --input practice/1aki/pca-2d.xvg --outdir outputs/pca-frequency --bins 8 --temperature 300
python code/calculate-dccm.py --trajectory practice/1aki/md-fit.xtc --topology practice/1aki/md-reference0.pdb --outdir outputs/dccm
```

## 核对真实结果

PCA 两列没有时间列，sham 用 `-notime`。8×8 频数网格的计数和为 101，占据 33 格；空格标为未采样，未补伪计数。Python 图独立统计频数，未沿用 XPM 的颜色。gromos 聚类在 C-alpha RMSD cutoff 0.10 nm 下得到 1 簇，101 成员；代表时间 11 ps，Protein PDB 含 1960 原子。

RMSD 的 C-alpha 与 Backbone 选择、生产起始坐标参考（md.tpr）与 100 ps 参考分别保留；C-alpha RMSD 均值为 0.0775405584 nm，Protein Rg 均值为 1.4252086931 nm，SASA 均值为 69.9023564356 nm²，GLU35–ASP52 C-alpha 距离均值为 0.9821980198 nm。均值区间为 0–100 ps。氢键计数为 92–115，DSSP 每帧标签总数为 129。

本机绝对工作路径在公开文本中规范为 RUN、ANALYSIS、GMX、GMX_DATA；GROMACS 随机追加的题外引用句已去掉。坐标、轨迹、能量、数值行和运行状态均未改写。记录中的输入校验值对应包内文件，图从这些公开 XVG 重新生成。

100 ps 数据用于操作、原子选择、文件对应与绘图练习。它不构成充分平衡、构象状态收敛、真实功能耦联或结合亲和力的证据。BioEmu 与长时独立重复未在本包运行。
