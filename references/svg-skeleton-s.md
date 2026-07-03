# SVG Skeleton · S系版式骨架（结构（Structure））

> Phase 7 按版式 ID 读取本文件。S 系两类实现路径：**参数化**（调 `layouts.py` / `structures.py` / `charts.py`，返回内容区 body，由 `themes.chrome` 包裹）与**栅格直排**（按 `grid-system.md §三` 坐标 + `svg-skeleton-common.md` 构件直排）。均不逐坐标手画。

---


## S-02 2×2 四格

**用途**：双维度定性分类，四象限各给标题+要点。
**适用场景**：定性四分（打法/人群/策略象限）。**带数据落位/气泡/迁移箭头 → 高阶变体**。
**用法**：定性轻量四格 v4.0 起走直排（grid §3.2/3.4 分栏 + 卡片构件，纪律：象限语义两轴可判定）。高阶 `structures.portfolio_matrix(x, y, w, h, items, axis_names, quads, migrations, size_label, hi)`——气泡面积∝规模、可选迁移箭头。
**来源**：2×2 矩阵谱系源自 BCG 增长份额矩阵（原版气泡面积=业务规模，对标评估）；GE-McKinsey 3×3 九宫格一手出处为 McKinsey 官方 "Enduring Ideas: The GE–McKinsey nine-box matrix"（McKinsey Quarterly, 2008-09, Kevin Coyne；1970 年代初为 GE 开发——调研报告候选4）。轻量定性格为通用简化，无单一可考原版。
**语义预设（v4.0，不占 ID）**：① Power-Interest 利益相关者格——axis=(利益, 权力)、quads=(密切管理/保持满意/保持知情/监控)，出处 Aubrey L. Mendelow, Proc. 2nd ICIS, Cambridge MA, 1991（调研报告候选7）；② 四象限竞争定位——外部竞品落位（结构对标 Gartner 1994 公开使用的四象限，**商标纪律同 S-17**：禁品牌名与专有措辞）。
**纪律**：两轴必须正交且可判定；高阶变体落位口径必须在页内写明（示意换算须标注）。

---





## S-07 HERO · 结论+N 支撑（参数化）

**用途**：金字塔原理的直接可视化——深墨结论区先行，N 张支撑卡并列。
**适用场景**：核心结论+证据的强论证页；纯宣言无证据 → 直排 §宣言页。
**用法**：`layouts.hero(conclusion_lines, supports)`——supports=[(标签, 标题, [描述 1–3 行])]，**N 硬拦 2/3/4**（grid §3.6 仅定义 HERO-2/3/4 三档栅格）；结论 1–2 行。选版式时记 `S-07(N=2/3/4)`。
**来源**：结论先行+并列支撑=金字塔原理的版式化——Barbara Minto, *The Minto Pyramid Principle: Logic in Writing, Thinking and Problem Solving*，现行权威版 **1996**（前序 1981/1987；叙事引入即其 SCQ Framework™，调研报告来源升级表——弃用 1978 说）；三档栅格为本库 grid 设计。
**纪律**：结论必须是断言句；支撑各自独立（MECE 倾向）；N>4 拆页或改 S-09。

---


## S-09 KPI 看板

**用途**：≤6 个关键数字的速览格。
**适用场景**：纯数字速览 → 轻量；**正式经营看板（值+基准+趋势）→ 高阶**。
**用法**：纯数字速览 v4.0 起走直排（grid §四 KPI 网格坐标直排）。高阶 `charts.kpi_card(x, y, w, h, label, value, benchmark, trend, unit, bench_label, hi)` × N 栅格排布（2×3：卡 384×224，x=40/448/856（缝 24，右缘恰 1240），y=130/378）。
**来源**：高阶依据 Stephen Few《Information Dashboard Design》——KPI 不应是孤立数字格（值+对比基准+迷你趋势）；**品牌适配（有意偏离 Few）**：状态色改 +/− 号与达标/未达文字双通道（brand 禁红绿）。轻量格为通用简化。
**纪律**：`hi=True` 唯一蓝高亮 ≤1 张；基准口径页内写明。

---


## S-13 勾选式现状盘点（组合配方）

**用途**：成就盘点三栏——对勾列 + 论据 bullet + 右侧 KPI 期比小表。
**适用场景**：阶段性成果汇报/复盘开场。
**用法**：组合配方（无单一函数）：`consulting.check` 对勾 + bullet 层 + `structures.mini_table`（hi_col 高亮当期列）+ `consulting.sowhat` 收束。
**来源**：调研1 明确记载**未找到单一可核查一手原版**（推导自 MBB 盘点页惯例）。
**纪律**：勾选项必须已完成（进行中不打勾）；期比表口径与页脚来源对齐。

---

## S-14 团队页（参数化 · v3.2）

**用途**：团队/组织介绍——人像占位 + 姓名/职务网格。
**适用场景**：客户方案的团队资质页、项目组介绍页。
**用法**：`layouts.team_grid(members)`——members=[(姓名, 职务, 一句话)] **2–8 人**（函数强制）；N≤4 单行、5–8 两行×4 列，列坐标等分冻结（同 grid §3 等分纪律，右缘 1240）。照片区为 `components.placeholder` 占位框，**等真实照片替换，不硬编假头像**。
**来源**：B2B 方案团队页通用惯例（无单一可核查原版，与 S-13 同为惯例推导）。
**纪律**：职务名实事求是（不虚衔）；note 一句话 ≤18 字；照片未到位就交付占位框并在交付说明注明。

---

## S-15 报价/条款页（参数化 · v3.2）

**用途**：报价明细 / 商务条款三线表。
**适用场景**：客户方案的报价页、付款条款页。
**用法**：`layouts.price_table(rows, header, total, total_label, note)`——rows=[(项目, 说明, 金额字符串)] **1–8 行**（函数强制）；`total` 合计**由调用方算好传入**（函数绝不求和——金额口径/币种/税别只能来自材料，不得推算）；note 放口径说明（如「含税 / 报价有效期 30 天」）。
**来源**：brand §4 表格规范（只横线、数字右对齐 mono、表头/合计加粗）的表格式落地。
**纪律**：金额必须与《项目基线》/信息清单一致并标来源；含税/不含税口径必须在 note 写明；超 8 行拆页或并入附录。

---

## S-16 Harvey Balls 评估表（参数化 · structures.py · v4.0）

**用途**：行=评估对象 × 列=维度的五档填充圆评估表，一眼看清程度梯度。
**适用场景**：供应商选型、能力成熟度评估、竞品功能对比。二值完成态 → S-13；定量指标 → S-09。
**用法**：`structures.harvey_table(x, y, w, h, dims, items, legend=True)`——dims 2–6 列、items 2–8 行、评分 0–4（均函数强制）；图例默认必配。
**来源**：Harvey L. Poppel 于 1970 年代在 Booz Allen Hamilton 发明（又称 Booz Balls），为 AT&T/IBM/Xerox 等客户简化复杂评估而创；MBB 及 Consumer Reports（1979–2016 产品评级）广泛使用（调研报告候选1，Wikipedia "Harvey balls" / Braithwaite Communications）。
**纪律**：评分口径（0–4 各档判据）必须页内或脚注写明；综合列如有须可复算。

---

## S-17 竞争格局定位图（参数化 · structures.py · v4.0）

**用途**：双轴散点 + 右上同心弧带分档 + 气泡大小=市场存在感的外部竞争格局图。
**适用场景**：竞品/供应商格局定位（打单讲竞争故事）。自有资产组合 → S-02 高阶。
**用法**：`structures.competitive_arc(x, y, w, h, vendors, bands, x_axis, y_axis)`——vendors=[(名, x, y, size 1–3, hi?)] 3–12 家（函数强制）；bands 默认（领导者/强劲表现者/竞争者）。
**来源**：版式结构对标 Forrester Wave（Forrester Research 2002-07 官方发布：Current offering=Y、Strategy=X、Market presence=点大小——调研报告候选3）；四象限型（Gartner 1994 公开使用）由 S-02 portfolio_matrix 预设覆盖。
**纪律**：**商标纪律**——Magic Quadrant / Forrester Wave 为注册商标，页面禁用品牌名称、专有分档措辞与专有配色，只用通用结构；落位依据（评分口径）必须页内注明或标"演示编排"。
