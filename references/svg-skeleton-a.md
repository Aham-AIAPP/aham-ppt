# SVG Skeleton · A系版式骨架（行动（Action））

> Phase 7 按版式 ID 读取本文件。参数化版式返回内容区 body，由 `themes.chrome` 包裹。

---



## A-03 责任清单

**用途**：行动分工表。
**适用场景**：**简版三列清单（行动/责任方/截止）→ 轻量**；**标准 RACI（多角色权责矩阵）→ 高阶**。
**用法**：轻量 `layouts.action_table(actions)`——actions=[(行动, 细节, 责任方, 截止)] **3–6 行**（函数强制）。
高阶 `structures.raci_matrix(x, y, w, h, tasks, roles, cells)`——**每行恰好一个 A 由函数强制校验**（违反抛错）。
**来源**：RACI **无单一可考发明人**——可上溯 1950s 线性责任图、1970s「责任分配矩阵」命名、1980s 与 GDPM 关联（调研报告来源升级表）；「每行唯一 Accountable」为 PMBOK 惯例/康奈尔模板等通行规范。轻量清单为通用简化。
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

---

## A-04 Impact-Effort 优先级矩阵（参数化 · structures.py · v4.0）

**用途**：举措按 影响×投入 落位的 2×2 快赢矩阵，回答"一堆举措先做哪些"。
**适用场景**：行动方案优先级排序（转型举措/整改清单）。资产组合气泡落位 → S-02 高阶；利益相关者管理 → S-02 预设 Power-Interest。
**用法**：`structures.impact_effort(x, y, w, h, items, quads, x_axis, y_axis)`——items=[(名, impact 0–10, effort 0–10, hi?)] 2–12 项（函数强制）；quads 默认（速赢/重大项目/填空任务/吃力不讨好）。
**来源**：**无单一可考原版**——通用优先级工具族，灵感常上溯艾森豪威尔矩阵，1990s 经精益/敏捷进入战略咨询工作坊（调研报告候选2，如实标注）。
**纪律**：落位分值必须给口径（评分依据或"团队工作坊共识"）；hi 唯一蓝 ≤2。

---

## A-05 决策树（参数化 · structures.py · v4.0）

**用途**：方形决策节点 → 选项分支 → 圆形机会节点（概率）→ 收益叶 + 期望值的序贯决策图。
**适用场景**：多阶段、带不确定性的投资/实施决策。静态两选一 → 直排 §A/B 选择。
**用法**：`structures.decision_tree(x, y, w, h, decision, options)`——options=[(选项, payoff字符串 或 [(情形, 概率, 收益)≤3], ev, hi?)] 2–4 支（函数强制）；**EV 由调用方传入，函数绝不计算**（同 S-15 合计纪律）。
**来源**：John F. Magee, "Decision Trees for Decision Making," *Harvard Business Review*, 1964-07（HBR #64410）；同年另有 "How to Use Decision Trees in Capital Investments"（调研报告候选8，一手 HBR）。
**纪律**：概率之和=1 且页内可见；EV 可复算（口径入脚注带 footnote_band）；收益数字须有来源或标"演示编排"。
