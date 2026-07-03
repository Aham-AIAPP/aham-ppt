# SVG Skeleton · T系版式骨架（过渡（Transition））

> Phase 7 按版式 ID 读取本文件。T 系为**整页型参数化版式**：调 `layouts.py` 函数生成完整页
> （自带极简页脚），坐标由函数冻结，不手画、不改坐标。

---

## T-01 深色引言页（参数化 · layouts.py）

**用途**：章节间的深色引言过渡——一句立场/判断，给观众换气位。

**适用场景**：章节转折、定调时刻。与 `themes.quote_dark`（C 档金句页，大引号+居中构图，无页脚）为**两个不同页型**，不互相替代：过渡引言 → 本版式；C 档独立金句页 → quote_dark。

**用法**：`layouts.quote_page(line1, line2, sub, attribution, source, page)`——深底 #1C1C1C，唯一蓝点缀为顶部短线；两行 36px 左对齐 + 副注 + 右下署名。

**来源**：通用商务惯例（深色引言/定调页），无单一可考原版。

**纪律**：真实语录必须可考（人名+出处）；自撰声明句必须在 attribution 注明"本演示自撰"，**禁止冒充名人语录**。

---

## T-02 白底大字宣言（参数化 · layouts.py）

**用途**：白底居中大字宣言——全 deck 最重的一句判断单独成页。

**适用场景**：核心主张的独立强调位。深色氛围 → T-01；带证据 → S-07。

**用法**：`layouts.declaration(sec, line1, line2, sub_note, source, page)`——居中双行 44px + 灰短线 + 副注。

**来源**：通用商务惯例（宣言页），无单一可考原版。

**纪律**：宣言必须是断言句（有立场、可被反驳），不是主题词。

---

## T-03 章节承接页（参数化 · layouts.py）

**用途**：章节间承接——左"刚讲完什么"（灰）/ 右"即将进入什么"（墨）+ 底部进度导航。

**适用场景**：多章 deck 的章间导航；单次分隔用 SPC-02（themes.section）即可，承接页额外提供"回顾+预告"。

**用法**：`layouts.bridge(sec, prev_title, prev_summary, next_title, next_intro, nav, source, page)`。

**来源**：呼应咨询叙事惯例——storyline 连续性与"recap → next"过渡为 MBB 通用做法（Slideworks/Deckary 对 MBB storyline 结构的归纳）；此双栏具体构图为本库设计，无单一可考原版。

**纪律**：左右两栏必须都是**内容概括**（讲了什么结论），不是章节名复读。
