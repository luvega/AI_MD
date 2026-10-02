# 1AKI 独立短程模拟

输入来自 RCSB PDB 的公开条目 [1AKI](https://www.rcsb.org/structure/1AKI)，下载文件为 `input/1aki.pdb`。运行脚本只保留 A 链的 ATOM 记录，选择空白或 A alternate location；本练习不沿用课程的结构文件或轨迹。

采用 GROMACS 自带 `amber99sb` 与 TIP3P。程序重新生成氢原子，建立距蛋白至少 1.0 nm 的十二面体盒，加入水与中和离子，并设置 0.15 mol/L 盐浓度。五份 MDP 是完整参数文件，不是待填写模板。NVT 20 ps、NPT 20 ps、生产格式 MD 100 ps；温度 300 K，压力 1 bar，MD 步长 2 fs，每 1 ps 写入一帧 XTC。

先从练习下载目录进入 chapter-05/assets。Ubuntu/WSL 用户按第 5.4 节安装 GROMACS 与 python3-venv，并激活独立 Linux 环境；已有原生 Windows GROMACS 的用户使用自己的 Windows Python 环境。

```bash
source ~/.venvs/ai-md/bin/activate
cd /mnt/c/coursework/ai-md/downloads/chapter-05/assets
```

这个示例对应 Windows 的 C:/coursework/ai-md/downloads，下载位置不同时修改路径。Linux 环境不要使用 Windows 的 .venv-win。确认 `gmx --version` 与 `python --version` 后再运行。

```bash
python practice/1aki/run-md.py --gmx gmx --work outputs/run-1aki --threads 4
```

`--work` 必须是新目录或空目录。Windows 的 `--gmx` 可以填写 `gmx.exe` 的绝对路径；Linux/WSL 使用 `gmx`。不要在模拟中途覆盖同一目录。每一步保存标准输出日志与 `command-log.tsv`，遇到非零退出码即停止，脚本不使用 `-maxwarn`。

若 `pdb2gmx` 提示需要选择端基、质子化状态或发现未知残基，应先阅读日志并核对结构，不能通过重复回车或增大容错继续运行。这个脚本只服务于已经核对的 1AKI A 链，不是处理所有蛋白的通用预处理程序。

完成后应保留输入、五份 MDP、拓扑、EM/NVT/NPT/MD 日志、`md.tpr`、`md.xtc`、`md.edr` 和 `md.cpt`。运行时间会随 CPU 与软件版本变化；100 ps 只用于练习文件交接和分析流程。

本次独立验证已完成。`verified-run` 保存实际版本、15 条命令退出码、EM 收敛数值和轨迹检查。官方 GROMACS v2025.5 源码构建后报告 2025.5-dev，使用原生 Windows CPU、SIMD NONE、MPI none、4 个 OpenMP 线程。EM 在 409 步达到 Fmax 966.43744 kJ·mol⁻¹·nm⁻¹，低于设置的 1000；最终 XTC 为 0–100 ps、101 帧。

匹配的完整轨迹、生产输入、阶段衔接文件和真实分析位于[第 6 章数据目录](https://luvega.github.io/AI_MD/assets/chapter-06/practice/1aki/)。不运行模拟也可以先用这些数据练习分析。公开文本仅将本机工作路径替换为 RUN/ANALYSIS/GMX 等标识，并去掉 GROMACS 随机附加的题外引用句，数值没有修改。
