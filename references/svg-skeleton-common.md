# SVG Skeleton · 通用骨架代码库（Aham UI v6.1）

> 本文件包含所有版式共用的骨架：Chrome框架、卡片骨架、状态、箭头。
> Phase 7 每页设计时必须加载本文件。
> **视觉取值唯一来源：brand.md / tokens.css。底永远纯白，蓝只点缀。**

---

## 设计语言速记（每页都遵守）

- **底永远 `#FFFFFF`**，无顶部蓝条、无色块墙、无渐变、无图片满铺。
- **三层灰**：内容/底 `#FFFFFF` · 面板 `#F3F3F3`(极少) · 线/选中 `#E7E7E7`。
- **墨四级**：`#262626` 主 / `#6E6E6E` 次 / `#9B9B9B` 三(占位/页脚) / `#C4C4C4` 四(最弱线)。
- **蓝 `#336EE8` 只点缀**：品牌点 / 主操作 / 选中下划线 / 推荐标 / **单个**高亮数据点 / 封面·关键页短装饰条。蓝若第一眼注意到就超标。
- **无衬线**：`Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif`；数字 mono `'JetBrains Mono', Consolas, monospace`。层级靠字号+字重。
- **卡片无边框无阴影**；分块优先留白 + `#E7E7E7` 细横线；成块才用 `#F3F3F3` 面板。
- **状态 = 6px 点 + 文字**；表格只横线、数字右对齐 mono。

---

## Chrome骨架（标准内容页，先复制此段）

```svg
<svg width="1280" height="720" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

<!-- ① 页眉：Section 路径（左） + 品牌（右，唯一蓝点） -->
<text x="40" y="24" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" letter-spacing="1" fill="#9B9B9B">[section_path]</text>
<rect x="1188" y="16" width="9" height="9" rx="2" fill="#336EE8"/>
<text x="1240" y="24" text-anchor="end" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="12" font-weight="600" fill="#262626">[brand_name]</text>
<line x1="40" y1="32" x2="1240" y2="32" stroke="#E7E7E7" stroke-width="1"/>

<!-- ② Action Title（整句结论 · 无衬线 bold · 无蓝竖线） -->
<text x="40" y="78" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="32" font-weight="700" fill="#262626">[title]</text>
<line x1="40" y1="94" x2="1240" y2="94" stroke="#E7E7E7" stroke-width="1"/>

<!-- ③ 内容区（在此处插入版式内容） -->
<!-- CONTENT_AREA: x=40 y=100 w=1200 h=590 -->

<!-- ④ 页脚 -->
<line x1="40" y1="690" x2="1240" y2="690" stroke="#E7E7E7" stroke-width="1"/>
<text x="40" y="709" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#6E6E6E">来源：[source] · [date]</text>
<text x="1240" y="709" text-anchor="end" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#6E6E6E">[page_index] / [total_pages]</text>

<!-- ⑤ 可选·关键页品牌点缀：左下蓝短条（全页仅此一处蓝面） -->
<!-- <rect x="40" y="672" width="84" height="2" fill="#336EE8"/> -->
</svg>
```

**双行标题时，替换②为：**
```svg
<text x="40" y="60" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="22" font-weight="700" fill="#262626">[title_line_1]</text>
<text x="40" y="86" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="22" font-weight="700" fill="#262626">[title_line_2]</text>
<line x1="40" y1="94" x2="1240" y2="94" stroke="#E7E7E7" stroke-width="1"/>
```

**极简Chrome（impact / transition 类）：**
```svg
<svg width="1280" height="720" viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
<text x="40" y="40" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#9B9B9B" letter-spacing="2">[section_path]</text>
<!-- CONTENT_AREA -->
<text x="40" y="700" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#9B9B9B">来源：[source]</text>
<text x="1240" y="700" text-anchor="end" font-family="'JetBrains Mono', Consolas, monospace" font-size="11" fill="#9B9B9B">[page_index]</text>
</svg>
```

---

## 卡片骨架（在内容区内使用 · 优先留白，成块才用面板）

### 默认：无卡片，靠留白 + 细横线分块
```svg
<!-- 区块标题 -->
<text x="[x]" y="[y]" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="20" font-weight="600" fill="#262626">[block_title]</text>
<!-- 区块下细横线（分隔，不画框） -->
<line x1="[x]" y1="[y+14]" x2="[x2]" y2="[y+14]" stroke="#E7E7E7" stroke-width="1"/>
```

### 面板卡（需要明显成块时，无边框无阴影）
```svg
<rect x="[cx]" y="[cy]" width="[cw]" height="[ch]" rx="12" fill="#F3F3F3"/>
<!-- 卡片标题（墨色，非蓝） -->
<text x="[cx+16]" y="[cy+30]" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="15" font-weight="600" fill="#262626">[card_title]</text>
<!-- Bullet（• 点 + 文字，起始 y=cy+58，间距 26） -->
<circle cx="[cx+19]" cy="[itemY-4]" r="3" fill="#9B9B9B"/>
<text x="[cx+32]" y="[itemY]" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="14" fill="#262626">[bullet_1]</text>
```

### 强调 / Callout（用面板 + 左侧蓝细条点缀，**不铺蓝底**）
```svg
<rect x="[cx]" y="[cy]" width="[cw]" height="[ch]" rx="12" fill="#F3F3F3"/>
<rect x="[cx]" y="[cy]" width="3" height="[ch]" rx="1.5" fill="#336EE8"/>
<text x="[cx+18]" y="[cy+30]" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="15" font-weight="600" fill="#262626">[callout_title]</text>
```

### 数据来源标注（有 data_points 时必须，右下角）
```svg
<text x="[cx+cw-16]" y="[cy+ch-12]" text-anchor="end" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="9" fill="#9B9B9B">来源：[source]，[date]</text>
```

---

## 状态：6px 点 + 文字（绝不 pill / 徽章 / 色块 / 红黄绿灯）

```svg
<circle cx="[x]" cy="[y-4]" r="3.5" fill="[状态色]"/>
<text x="[x+13]" y="[y]" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="13" fill="#6E6E6E">[达标/预警/风险/进行中]</text>
```
状态色：达标 `#5A7A60` · 预警 `#8A7333` · 风险 `#9E3D31` · 中性/进行中 `#9B9B9B`。
**颜色+文字双通道**：颜色之外，文字本身必须能区分（达标/预警/风险），去色后仍可辨。

---

## 数字 / KPI（mono · 墨色，关键时才一个蓝）

```svg
<!-- 标签 -->
<text x="[x]" y="[y]" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="15" fill="#9B9B9B">[label]</text>
<!-- 数值（等宽，墨色；唯一关键数可用 #336EE8） -->
<text x="[x]" y="[y+50]" font-family="'JetBrains Mono', Consolas, monospace" font-size="50" font-weight="700" fill="#262626">[value]</text>
<text x="[x+数字宽]" y="[y+50]" font-family="Inter, sans-serif" font-size="22" fill="#9B9B9B">[unit]</text>
```

---

## 箭头（替代 marker，用 polygon · 中性灰）

```svg
<line x1="[x1]" y1="[y]" x2="[x2-12]" y2="[y]" stroke="#9B9B9B" stroke-width="2"/>
<polygon points="[x2-12],[y-6] [x2],[y] [x2-12],[y+6]" fill="#9B9B9B"/>
```

---

## 咨询密集层 D（consulting.py / structures.py）· 三原则 / 标注层 / 纪律

> **形体 API**（chevron_flow / flow_bands / dumbbell_rows / dot_matrix / driver_node+elbow / chain_steps）见各系骨架文件末尾的 90 段章节：`E-90 / V-90 / V-91 / V-92 / G-90 / I-90`；**结构版式**（矩阵/树/泳道/分层网格）见 `S-13 / E-91 / V-93 / V-94 / A-90 / A-91 / G-91 / G-92 / G-93` 及 S-02/S-09/A-03/G-01/E-04 的高阶变体。本节是可叠加**任意版式**的横切部分：三原则、标注层 API、密度与标注纪律。
> 代码真源 `assets/components/consulting.py` + `assets/components/structures.py`（矩阵/树/泳道/分层结构层）+ `charts.py`（kpi_card/marimekko/fte_ramp/horizon_curves/sparkline）——均为参数化函数，不逐坐标手画。

### 降「AI 方形大卡片味」三原则

AI 生成 deck 的公认短板是结构纪律、行动标题与视觉层级（Slideworks 五工具实测评述，2026）。形体语言是补「视觉层级」的直接抓手。三原则（均有出处）：

1. **图表即主角，裸摊白底**——密集页不许给图表再套卡片/外框容器；标题陈述结论、图表即证明（BCG "smart simplicity"，Deckary《BCG Presentation Style》）。公共 pptx 规范同向："标题下强调线 / 边缘色条是 AI 生成幻灯片的标志"。本文件上方的"卡片无边框无阴影"在 D 层收紧为：**图表区禁任何外框**。
2. **异形替代等宽矩形阵**——chevron 时间轴、瀑布为"桥/差值"类默认、Mekko/100% 堆叠替代饼图、2×2 / 散点 / 甘特为 MBB 常备图谱（Deckary《McKinsey Slides》图谱清单；PopAi 版式清单 "Project Timeline (Chevron Style)"、"'So What?' Box"）。等宽矩形阵只在内容本身同构时使用。
3. **标注层 + 跨区连接**——椭圆圈注关键数、引线把图表元素牵到编号动作/旁注、So-What 锚点条、大号淡水印；高密度靠严格栅格对齐维持可读（Deckary："grid-aligned layouts… calm and easy to read even when a slide is information-dense"）。

### 标注层 API（可叠加任意版式）

| 函数 | 用途 |
|---|---|
| `mark_ellipse(cx,cy,rx,ry)` | 手绘感椭圆圈注（禁 rotate） |
| `leader(x1,y1,x2,y2)` | 引线箭头（line+polygon） |
| `watermark(x,y,text,size)` | 大号淡水印，**最先绘制** |
| `sowhat(x,y,w,h,label,text,dark)` | So-What 锚点条（灰面板或深墨） |
| `tick_label(cx,y_top,text,level)` / `check(x,y)` | 细段错层小标注 / 线画对勾（替 ✓） |
| `structures.footnote_band(x,y,w,notes,note,source)` | 方法论脚注带（编号脚注+注+来源三件套，BCG 式）——任何"推算/抽样/外推"页通用，放内容区底部、chrome 页脚之上 |
| `structures.milestone(cx,cy)` / `gate(cx,y)` / `flag_line(x,y0,y1)` | 里程碑菱形 / stage-gate 三角 / 竖向标志虚线（Today 线、波次分界）——路线图与爬坡图共用记号 |

### 密度与标注纪律

**密度纪律（防「一页一组件」式过简）：**
- 单个 X-90 元素**禁止**独占内容区；每页 = 1 主视觉 + ≥1 辅助层 + 标注层 + So-What（各 90 段章节列了本版式的组合配方）。
- 相关元素允许同页并用（如 点阵＋堆叠条、哑铃＋拆解条、链＋分布条）；数据图表可与 charts.py 同页混排。
- 内容区（40/100/1200/590）留白靠栅格分配，不靠"整块空着"。

**标注层配额：**
- 每页 ≤1 处椭圆圈注、≤2 条引线；水印 op ≤ 0.04 且最先绘制；So-What 全页至多 1 条。
- **chrome 红线**：页眉/页脚/左缘留白归本文件与 themes.py，D 层元素不得进入 x<40 或页眉页脚区。
- **蓝的记账**：hi 参数与 ACC 文字合并计入 brand「单点缀」——全页至多一个蓝语义。

### 降级工具：同心弧（定性叙事专用）

`structures.concentric_arcs(x, y, w, h, rings)`——半圆同心弧**只做定性层级叙事**（≤5 层标签，不接受数值），
函数强制绘制「定性层级示意 · 弧径不代表数值」。原因（调研核实）：径向布局面积随半径平方增长、
系统性夸大外圈，Zelazny 五图体系无此图型；Aon 2025 Investor Day Slide 69 那页是真实的品牌叙事图，
不是严谨数据图。**定量规模序列 → charts.hbar 或 V-94 Marimekko**（速查表已反引导）。
雷达图**不提供**——理由与替代见 `layout-library.md §不提供的图型`。

### 冒烟基线

组件级：每个参数化函数须有渲染断言 + 负向测试；页级：`tools/lint_svg.py` 预检 + SVG→PPTX 形状数比对；改动回归：成品页像素 diff。机制与门槛见 `CONTRIBUTING.md §验证`。
