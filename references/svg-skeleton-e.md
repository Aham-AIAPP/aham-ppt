# SVG Skeleton · E系版式骨架（说明（Explain））

> Phase 7 按版式 ID 读取本文件。参数化版式返回内容区 body，由 `themes.chrome` 包裹。

---


## E-02 概念曲线（参数化 · layouts.py）

**用途**：单条三段概念曲线（爬升→平台→冲顶虚线）+ 当前位置 + 右侧结论——定性趋势叙事。
**适用场景**：概念性阶段判断（在哪个阶段/接下来如何）；**量化数据 → V 系 charts**；多条 S 曲线错峰 → E-91。
**用法**：`layouts.concept_curve(y_label, x_label, stage_labels×3, current_label, conclusion_lines, right_descs)`——三段形态与语义色（绿爬升/褐平台/灰虚冲顶、红当前点）为骨架冻结值；**恰好 3 段标签**（函数强制）。
**来源**：通用商务惯例（成熟度/关注度概念曲线），无单一可考原版；三段配色为本库设计。
**纪律**：页内必须标注"概念示意，非量化"；当前点断言须有依据。

---

## E-03 流程示意（参数化 · layouts.py）

**用途**：3–6 段线性流程框 + 箭头，末段深色收束。
**适用场景**：单线流程；带量的阶段链 → E-90 雪佛龙；两选一判断 → 直排 §A/B 选择；多阶段带概率 → A-05 决策树。
**用法**：`layouts.stage_flow(stages, dark_last=True)`——stages=[(眉标, 名称)] **3–6 段**（函数强制）；4 段时精确复现骨架坐标；箭头 line+polygon（约束7 禁 marker）。
**来源**：通用流程图惯例。
**纪律**：段间必须是先后关系（并列 → 直排三栏）。

---

## E-04 分层架构

**用途**：层级结构表达。
**适用场景**：**概念三层（战略/管理/执行式）→ 轻量**；**真实 IT/系统架构（层内多模块、跨层能力条）→ 高阶**。
**用法**：轻量 `layouts.tri_layer(layers)`——**固定 3 层**（函数强制），深→中→浅 + 层间下行箭头。
高阶 `structures.arch_layers(x, y, w, h, layers, pillars, iface_labels, hi_layer)`——layers 自上而下 [(层名, [模块…], 层高权重)]，层内模块等宽网格自动对齐；pillars 纵向能力条（单字逐 text 纵排，非 rotate）；iface_labels 层间接口标记。
**来源**：高阶依据 TOGAF 四域/经典分层 + 层内组件对上层提供服务（对标评估）；轻量为通用简化。
**纪律**：轻量层名 ≤8 字；高阶应用层权重最大（如 1.6）。

---

## E-90 雪佛龙阶段链（参数化 · consulting.py）

**用途**：带量的阶段推进链（每段名+数值+副注），可 hi 单段。
**适用场景**：阶段×数量叙事（各段场次/产能/人数）；无量纯流程 → E-03。
**用法**：`consulting.chevron_flow(x, y, w, h, stages, hi)`——stages=[(名, 量, 副注)]。
**来源**：MBB 咨询密集页形体语言（v2.5 调研批次），无单一可考原版。
**纪律（组合配方）**：元素级版式——主视觉 + 辅助层 ≥1 + 标注层 + So-What（common §D 配额）。

---

## E-91 三地平线（参数化 · charts.py）

**用途**：3–4 条 S 曲线错峰叠加——并行管理的增长/接力叙事。
**适用场景**：三地平线/技术接力/业务梯队；单条概念曲线 → E-02。
**用法**：`charts.horizon_curves(x, y, w, h, horizons, hi)`——horizons=[(名, 注)] **3–4 条**（函数硬拦，标准形态依据）。**不带刻度**（概念图不假装量化）。
**来源**：Three Horizons 框架——Mehrdad Baghai, Stephen Coley, David White, *The Alchemy of Growth*, Perseus, 1999（一手原书）；机构佐证 McKinsey 官方 "Enduring Ideas: The three horizons of growth"（McKinsey Quarterly, 2009——调研报告来源升级表）；官方语义为三层**并行管理**而非先后接棒。
**纪律**：横轴不标年份刻度；每线配一句注。

---

## E-05 价值链条带图（参数化 · structures.py · v4.0）

**用途**：Porter 价值链——顶部支持活动横条 + 底部主活动雪佛龙带 + 右端利润尖角。
**适用场景**：企业内部价值活动分解、成本/差异化来源定位（制造业售前"我们切入哪些环节"）。分层系统架构 → E-04；纯流程 → E-03。
**用法**：`structures.value_chain(x, y, w, h, primary, support, margin_label)`——primary=[(名, 注或 None)] 3–6 段、support=[名] 2–4 条（Porter 原型 5+4，函数强制区间）。
**来源**：Michael E. Porter, *Competitive Advantage: Creating and Sustaining Superior Performance*, Free Press, 1985；另见 Porter & Millar, HBR 1985（调研报告候选5，一手书籍）。
**纪律**：主活动必须按物流方向排序（入向→运营→出向→营销→服务的次序语义）；高亮段 ≤1。
