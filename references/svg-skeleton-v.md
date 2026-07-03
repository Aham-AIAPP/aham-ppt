# SVG Skeleton · V系版式骨架（证据（Verify））

> Phase 7 按版式 ID 读取本文件。V 系=数据证据页：主视觉一律调 `charts.py` / `consulting.py` / `structures.py` 参数化生成，不手画。

---

## V-02 单大图表

**用途**：一张图占满 FULL 区，用数据本身说话。
**适用场景**：单一数据故事；两组数据对照 → V-04。
**用法**：FULL 区（40,100,1200,580 排版目标；红线底 y=690）**直调 charts.py**（bar/hbar/line/waterfall/funnel/stacked/slope/marimekko…按 phase-05 §2.5 图型映射）；来源走 chrome 页脚，图内补充注可置 (56,656)。无包装函数（charts 即其参数化实现）。
**来源**：图表选型体系=Gene Zelazny（McKinsey 视觉传达总监）, *Say It With Charts: The Executive's Guide to Visual Communication*, McGraw-Hill, 初版 **1985**（后 1991/1996/2001 版）——五类比较 Component/Item/Time Series/Frequency Distribution/Correlation（调研报告来源升级表）；瀑布图由 McKinsey 于 1990s 普及（调研报告：Wikipedia "Waterfall chart"，业界亦称 McKinsey chart）；各图型纪律见 chart-impl。
**纪律**：一页一个数据故事；标题写结论不写图名。

---

## V-03 图上直接标注（参数化）

**用途**：趋势图 + 关键点图上标注（leader 引线/椭圆圈注），替代"图旁文字块"。
**适用场景**：需要点出拐点/峰值/异常的趋势叙事。
**用法**：charts 主图 + `consulting.leader / mark_ellipse` 标注层 + 可选 `sowhat` 底条。标注配额：椭圆 ≤1、引线 ≤2。
**来源**：Knaflic《Storytelling with Data》"Label data directly" pp.176–181（对标评估）。
**纪律**：标注文字是判断句（"扩军年才跳档"），不是数值复读。

---

## V-04 双图对比

**用途**：两图并排互证 + 图上标差异。
**适用场景**：两口径互相印证（量×率）；同轴两序列 → 单图双线。
**用法**：TWO-EQ 两区各直调 charts + 图上 leader 标差异（每图 ≤1 处）+ 底部一句口径注。无包装函数。
**来源**：同 V-03（图上标注纪律，Knaflic）。
**纪律**：两图必须同源同口径，差异标图上、**不另立文字块**。

---

## V-90 流向带（参数化 · consulting.py）

**用途**：多源汇成总量的锥形流向（sankey-lite），带宽∝数值。
**适用场景**：构成汇聚叙事（N 类来源 → 总量）；精确流转矩阵不适用（本件为单层汇聚）。
**用法**：`consulting.flow_bands(x, y, w, h, sources, target, hi)`——sources=[(名, 值)] 数量数据驱动；带宽与源块高严格 ∝ 数值（v2.6 实测 10:6:3:1）。
**来源**：Sankey 谱系的单层简化（v2.5 调研批次）；带宽∝值为 Sankey 定义性纪律。
**纪律（组合配方）**：主视觉 + 辅助清单/注解 + So-What。

---

## V-91 哑铃对比（参数化 · consulting.py）

**用途**：期际/组间的逐指标两点对比（A→B + 差值标签）。
**适用场景**：两期多指标对照；连续趋势 → line。
**用法**：`consulting.dumbbell_rows(x, y, w, rows, row_h, hi)`——rows=[(指标, a, b, 差值)]。
**来源**：dumbbell/连线点图惯例（v2.5 调研批次）。
**纪律**：差值标签写含义（+0.57）非复读两端。

---

## V-92 点阵机制图（参数化 · consulting.py）

**用途**：名额/席位机制的点阵表达（实心/空心/淡三态）。
**适用场景**：配额、晋级、覆盖类机制说明。
**用法**：`consulting.dot_matrix(x, y, cols, rows, gap, r, col_labels)`——rows=[(行名, solid|ring|dim)]。
**来源**：waffle/点阵谱系（v2.5 调研批次）。
**纪律（组合配方）**：必配机制注解面板（点阵不自解释）。

---

## V-93 推算逻辑双栏（组合配方）

**用途**：左"已知抽样"→ 乘数桥 →右"外推结论"+ 敏感区间 + 方法论脚注带。
**适用场景**：以小见大的量级推算（市场规模/全程估算）。
**用法**：组合：`structures.mini_table`（左右各一，hi_col 高亮结论列）+ `structures.bridge_arrow`（乘数桥）+ 敏感区间行 + `structures.footnote_band`（编号脚注+口径声明）。
**来源**：BCG 达拉斯公开报告推算页（调研1：136 dogs/235 miles、乘数链 0.77×1,751×6.45x≈8,700、第三方敏感值 7,100）——本库最强的单一可考原型。
**纪律**：外推必须给敏感区间与口径声明（"量级判断，非预测承诺"）；乘数每步可复算。

---

## V-94 Marimekko（参数化 · charts.py）

**用途**：列宽∝总量 × 段高∝构成的双维一图。
**适用场景**：规模×构成同时表达；**时间序列勿用**（列宽变化产生"哈哈镜"畸变）。
**用法**：`charts.marimekko(x, y, w, h, cols, series, wlabel, mode, hi_series)`——cols=[(名, [段值], 列总)]，**≤7 列 / ≤4 段**（函数硬拦）；mode="pct"|"abs"（abs=Bar Mekko）。
**来源**：mosaic/Marimekko——Hartigan & Kleiner 1981 学术源；Aon 2025 Investor Day Slide 69 为在用实例（调研2，文本标签已核实、系品牌叙事图）。
**纪律**：≤7 列硬拦依据=哈哈镜效应随列数放大（调研2）；近似拆分必须页内标注。

---

## V-05 小倍数网格（参数化 · charts.py · v4.0）

**用途**：同图型、**同坐标尺度**的 4–12 个小图网格——只让数据变化、设计不变，跨类别/跨期系统比较。
**适用场景**：多产线/多区域/多期的同构横扫。2 图深对比 → V-04；单一数据故事 → V-02。
**用法**：`charts.small_multiples(x, y, w, h, kind, datasets, cols, unit, shared_max)`——kind="line"|"bar"；datasets=[(标题, 数值列)] 4–12 格且各格点数一致（函数强制）；**全局共享 Y 尺度由函数强制**（Tufte 定义的核心纪律），底部自动注明尺度声明。
**来源**：Edward Tufte, *The Visual Display of Quantitative Information*, Graphics Press, 1983（调研报告候选10，一手书籍；普及者）。
**纪律**：禁各格独立缩放（那是误导性对比）；末值标签统一右上。
