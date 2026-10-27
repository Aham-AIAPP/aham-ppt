# SVG Skeleton · I系版式骨架（震撼（Impact））

> **参考素材（2026-10-27 起移出主流程）**：本文件属于旧的 SVG 路线，主流程不再加载。
> 文中「唯一权威」「必须」「不可改动」「坐标冻结」「节奏约束」一类要求不再约束版式设计。
> 版式按 `design-principles.md` 设计，页面按 `html-slides.md` 写。需要某种结构的画法时可查本文件。

> Phase 7 按版式 ID 读取本文件。I 系为**整页型参数化版式**：调 `layouts.py` 函数生成完整页
> （自带极简页脚），坐标由函数冻结，不手画、不改坐标。

---



## I-90 链式递减（参数化 · consulting.py）

**用途 / 适用场景**：存活/淘汰、收敛到 1 的链式叙事；数据转化漏斗走 `charts.funnel`（phase-05 §2.5 映射）。

**用法**：`consulting.chain_steps(x, y, vals, step=110, r=18, deltas=None, cap=None)`，末端胶囊承接收敛结果。

**来源**：MBB 咨询密集页形体语言（v2.5 调研批次），无单一可考原版。

**纪律（组合配方）**：元素级版式，禁单元素占满内容区——主视觉 chain_steps + 必配辅助层 ≥1（出局分布堆叠条 / 机制注解面板 / watermark 大数字）+ 标注层 + So-What；配额见 `svg-skeleton-common.md §咨询密集层 D`。
