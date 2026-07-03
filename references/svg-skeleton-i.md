# SVG Skeleton · I系版式骨架（震撼（Impact））

> Phase 7 按版式 ID 读取本文件。I 系为**整页型参数化版式**：调 `layouts.py` 函数生成完整页
> （自带极简页脚），坐标由函数冻结，不手画、不改坐标。

---

## I-01 大数字页（参数化 · layouts.py）

**用途**：单一核心数字整页锚定注意力——强结论的开场、章节冲击位或收束。

**适用场景**：一个数字足以立住论点时（规模/增速/缺口/纪录）。多指标并列 → S-09；数字需要图形证明 → V 系。

**用法**：`layouts.bignumber(sec, big, assertion, source, page, compare_anchor=None, support2=None, warning=None, evidence=None)`
- 基础变体（`evidence=None`）：大数字 180px + 断言 + **对比锚点（必填，函数强制）** + 可选补充行与红色警示行。
- 带证据变体（`evidence=(右列标题, [(标签, 说明)×3])`）：大数字 170px 左置 + 右列**固定 3 条**支撑（函数强制）。
- 示例：`bignumber("PART 01 / I-01", "104", "史上最大规模：单届 104 场", src, "4 / 54", compare_anchor="2022 年 64 场 → +62.5%", evidence=("WHY IT MATTERS", [("48 支参赛队","…"),("39 天赛期","…"),("16 座城市","…")]))`

**来源**：MBB 通用惯例——"以单一统计做整页主视觉锚定注意力"见诸多家对 McKinsey 公开 deck 的归纳（Analyst Academy 拆解、SketchBubble《McKinsey-Style Guide》"Full-slide graphs…explain a single statistic"、ChatSlide 将 big numbers 列为 bullet 替代首选）；**无单一可考原版**。

**纪律**：对比锚点必填——同比/目标/行业基准三选一，禁止数字悬空（对标评估 P2）；页脚来源必填，大数字页尤其不许省。

---

## I-05 时间窗警告（参数化 · layouts.py）

**用途**：用"过去—现在—未来"三节点时间轴 + 大号窗口期制造紧迫感。

**适用场景**：决策窗口/倒计时/截止压力叙事。多里程碑排期 → S-03；多泳道 → A-90。

**用法**：`layouts.time_window(sec, past, now, now_tag, future, warning_title, warning_desc, window, window_label, source, page)`——三节点固定（版式语义即三态）；紧迫性由红色"当前"节点 + 警示标题**双通道**表达，窗口数字保持墨色（brand 禁染红绿）。

**来源**：通用商务惯例（倒计时/机会窗口页型），**无单一可考原版**；三节点轴 + 双通道紧迫表达为本库设计决策。

**纪律**：窗口数字须可复算（如"距 X 日 N 天"给出基准日）；警示语写事实不写恐吓。

---

## I-90 链式递减（参数化 · consulting.py）

**用途 / 适用场景**：存活/淘汰、收敛到 1 的链式叙事；数据转化漏斗走 `charts.funnel`（phase-05 §2.5 映射）。

**用法**：`consulting.chain_steps(x, y, vals, step=110, r=18, deltas=None, cap=None)`，末端胶囊承接收敛结果。

**来源**：MBB 咨询密集页形体语言（v2.5 调研批次），无单一可考原版。

**纪律（组合配方）**：元素级版式，禁单元素占满内容区——主视觉 chain_steps + 必配辅助层 ≥1（出局分布堆叠条 / 机制注解面板 / watermark 大数字）+ 标注层 + So-What；配额见 `svg-skeleton-common.md §咨询密集层 D`。
