# 已填交付示例

## 研究计划示例：3HTB 小批次

问题：同一受体和网格下能否复现 JZ4 的已知 pose，并完整记录三分子批次？
已有依据：公开 3HTB 的 JZ4 auth chain A residue 167；JZ4/IPH/BNZ 来自 CCD。来源与准备见第 3 章。
第一轮：先跑一个 JZ4，再运行三配体，CPU=2、seed=20261002、exhaustiveness=16、9 poses。
已有输出：Vina 1.2.7 批次完成；JZ4 score=-7.190 kcal/mol，晶体坐标系无拟合、对称性重原子 RMSD=0.4946 Å。
下一步：人工检查三个 pose、关键接触和化学状态；若用于研究，再安排结合或功能实验并设适当参照。
停止条件：晶体参照或输入身份不一致时先修复；基础作业暂不扩大配体库。

## 方法比较示例：三分子同协议表

比较问题：同一准备、网格和 Vina 协议下，三个配体输出和 pose 检查怎样记录？
输入：一个干燥刚性受体和三个 CCD 中性配体状态；详细文件和协议保存于第 3–4 章。
执行：Vina 1.2.7、同一 seed、CPU 数和搜索强度。
观察：JZ4/IPH/BNZ 模式 1 score 分别为 -7.190/-5.943/-5.662 kcal/mol，三项 completed。
需要补的比较：人工检查每个 pose；JZ4 可与晶体参照比较，IPH/BNZ 在本练习中没有同靶标晶体 pose 参照。
解释与验证：表格比较计算流程与 pose；实际结合排序另需实验。

## 执行记录示例：PDL1 CPU 序列

任务 ID：pdl1-mpnn-seed37。
输入：Foundry 官方 PDL1 final model 的 PDB 转换件；A=77、B=114；输入 SHA256 为 4a6d772bf58f9b0d67038db6a1122292862fe2d242bb1cb1aca03f265288855e。
环境：Windows Python 3.13，PyTorch 2.6.0+cu124；子进程隐藏 CUDA，只使用 CPU 两线程。
模型：ProteinMPNN 提交 8907e6671bfbfc92303b5f79c4b5e6ce47cdef57，v_48_020，temp=0.1，seed=37，2 samples，固定 B、设计 A。
结果：返回码 0；两条 77 aa 序列 score=1.0529/0.9849；完整过程 12.918 秒，官方生成日志 5.4829 秒。
排错：第一次官方脚本把 Windows 反斜杠绝对路径当目标名，产生无效输出名；wrapper 用 as_posix 传参后完成。
回折叠：两条实际序列的 A+B 输入已用 Boltz 2.2.1、GPU 3070、seed=37、3 次 recycling、200 步采样、每条 1 个样本完成；两链均 msa:empty，两个候选 completed。
几何检查：A 内部拟合 RMSD=1.72/1.40 Å；按 B 拟合后的 A RMSD=16.38/4.81 Å。两条的 complex pLDDT=0.9087/0.9261，六个 hotspot 都存在 4.5 Å 内几何接触，却仍需区分整体取向。
下一步：候选 1 退回界面复核，候选 2 优先结构检查；安排独立预测与实验验证。
验证：先同候选回折叠与界面复核，再安排表达、纯化、结合及功能测试。
