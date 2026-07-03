# SVG Skeleton · A系版式骨架（行动（Action））

> Phase 7 按版式 ID 读取本文件。参数化版式返回内容区 body，由 `themes.chrome` 包裹。

---

## A-01 下一步三步决策（参数化 · layouts.py）

**用途**：三步行动卡并列，末步深色收束——把结论落成时间化的动作。
**适用场景**：会后行动/近期计划；多步长排期 → A-90 / S-03。
**用法**：`layouts.three_steps(steps)`——steps=[(时间标注, 行动, [细节 1–3 行])] **固定 3 步**（函数强制，版式语义即三步），末步自动深色+蓝条。
**来源**：通用商务惯例（next steps 三步式），无单一可考原版。
**纪律**：每步必须有时间标注与可执行动词。

---

## A-02 是/否选择矩阵（参数化 · layouts.py）

**用途**：A（推荐）/ B（备选）两选项对置 + 各自 pros/cons，请求单选决策。
**适用场景**：二选一决策页；多方案对比 → S-08 / S-02。
**用法**：`layouts.option_ab(a, b_, a_tag, b_tag)`——a / b_ = (标题, 描述×2, pros, cons)；B 选项自动降调（灰条+降墨）。pros/cons 语义色为骨架冻结值（绿/绛）。
**来源**：通用商务惯例（option A/B 决策页），无单一可考原版。
**纪律**：两选项必须互斥；推荐位固定 A（阅读起点）。

---

## A-03 责任清单

**用途**：行动分工表。
**适用场景**：**简版三列清单（行动/责任方/截止）→ 轻量**；**标准 RACI（多角色权责矩阵）→ 高阶**。
**用法**：轻量 `layouts.action_table(actions)`——actions=[(行动, 细节, 责任方, 截止)] **3–6 行**（函数强制）。
高阶 `structures.raci_matrix(x, y, w, h, tasks, roles, cells)`——**每行恰好一个 A 由函数强制校验**（违反抛错）。
**来源**：RACI 规范——每行唯一 Accountable（PMBOK 惯例/Wikipedia/康奈尔大学模板，对标评估）；轻量清单为通用简化。
**纪律**：截止时间必须具体到日；R 可多个、A 恰一个。

---

## A-90 阶段×泳道路线图（参数化 · structures.py）

**用途**：3–6 条并行 workstream 的时间/相位路线图 + Today 线 + 状态 + 里程碑。
**适用场景**：多线并行排期与决策会评审。
**用法**：`structures.swimlane_roadmap(x, y, w, h, lanes, total_units, today, milestones, deps, unit_label, legend, mode, bucket_names)`——三渲染模式：
- `mode="gantt"`（默认）：精确时间轴 + 矩形块；
- `mode="chevron"`：块画雪佛龙形，强调相位推进而非精确日期；
- `mode="phase_bucket"`：BCG 达拉斯式相位分桶（默认五桶 立即行动/速赢/战略优先/中期举措/长期机会，对应 Immediate Actions / Quick Wins / Strategic Priorities / Medium-term Initiatives / Long-term Opportunities），**禁 today/milestones**（函数强制）——日期不确定时比假装精确更诚实。
lanes=[(泳道名, [(块名, start, dur, status)])]，status ∈ committed/planned/proposed。
**来源**：调研1——泳道 3–6 最佳、Today 线、Committed/Planned/Proposed 状态防过度承诺、NHS England API 交付流程为实例；分桶五相位=BCG 达拉斯公开报告。
**纪律**：块长四舍五入到半月粒度（近似比假装精确诚实）；日期完全不确定 → `mode="phase_bucket"`；执行层细节放附录。

---

## A-91 FTE 爬坡（参数化 · charts.py）

**用途**：分波次的人力/资源爬坡（堆叠面积/柱）+ 决策门。
**适用场景**：投入爬坡与 stage-gate 决策叙事。
**用法**：`charts.fte_ramp(x, y, w, h, periods, waves, wave_names, gates, unit)`——**时间点 ≥10 自动切堆叠面积、<10 用堆叠柱**（调研纪律内置）；gates=[(期索引, 门名, 决策)]。
**来源**：调研1——stacked area + wave 虚线 + stage-gate 三角；<10 期退化为 column 的纪律；Stage-Gate 概念源 Cooper 1988/1990。
**纪律**：图例右上（图表底部 ≤2 层，chart-impl 硬性规定）；波次与门必须有口径来源或标注演示编排。
