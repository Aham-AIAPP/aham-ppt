# 图表 SVG 实现模板

对应 brand.md 第7.5节的图表规范，提供各图表类型的精确SVG绘制代码。
**图表类型选择规则和颜色语义以 brand.md 7.5节为准，本文件只管「怎么画」。**

> **图表配色（硬规则）**：所有数据元素**灰阶** `#9B9B9B`（主）/ `#C8C8C8`（次），**至多一个 `#336EE8` 蓝**高亮当前/重点项；坐标轴 `#E7E7E7`、刻度标签 `#6E6E6E`、网格线 `#F3F3F3`。**绝不多色**、无 3D/阴影/渐变、**无饼图/环形图**。阈值只染**文字**，不铺整行整列底色。**所有面型数据元素（柱/条/梯形/堆叠段/图例块）带 1px `#6E6E6E` 描边**（WCAG 1.4.11 非文字对比通道，charts.py 已内置 `EDGE`，手画模板须自行加上）。下方模板里的柱/条/线默认填 `#9B9B9B`，把要强调的那一个改成 `#336EE8`。

---

## ⭐ v3 · 图表优先调用 charts.py 组件（不再逐坐标手画）

**所有图表一律优先调用 `assets/components/charts.py` 的参数化函数**：一行生成、坐标自动计算、已内置 brand §7.5 合规（灰阶 + 至多一个蓝、无红绿多色、Y 轴从 0）与 PPTX 兼容（只用 rect/line/text/circle，均已实测转为可编辑形状）。下方手画模板仅在组件未覆盖某类型时作兜底。

已验证可用（`from charts import bar, hbar, line, waterfall, funnel, gantt, bullet, stacked, slope`）：
- `bar(x,y,w,h,data,hi_index=None,unit="",money=False,title=None,target=None)` — 纵向柱状（对比/排名）
- `hbar(x,y,w,h,data,hi_index=None,money=False,title=None)` — 横向柱状（排名/长标签）
- `line(x,y,w,h,values,xlabels,hi_last=True,target=None,unit="",money=False,title=None)` — 折线趋势
- `waterfall(x,y,w,h,items,hi_index=None,money=False,title=None)` — 瀑布拆解；`items=[(label,value,'total'|'delta'),...]`

约定：`data=[(label,value),...]`；`hi_index` 用唯一蓝高亮重点项；正负/目标靠位置 + 符号 + 灰阶，不用红绿。
- `funnel(x,y,w,h,stages,hi_index=None,money=False,title=None)` — 漏斗（转化收窄）；`stages=[(label,value),...]`
- `gantt(x,y,w,h,tasks,total_units,today=None,unit_label="",title=None)` — 甘特（分期排期）；`tasks=[(name,start,dur[,hi]),...]`，today 画今日竖虚线
- `bullet(x,y,w,h,metrics,hi_index=None,money=False,title=None)` — 子弹（实际 vs 目标）；`metrics=[(label,actual,target,max),...]`
- `stacked(x,y,w,h,data,seriesnames,hi_series=None,unit="",money=False,title=None)` — 堆叠柱（构成变化，≤4段）；`data=[(label,[v1,v2,...]),...]`
- `slope(x,y,w,h,items,label_left="前",label_right="后",hi_index=None,money=False,title=None)` — 坡度（前后对比）；`items=[(name,vleft,vright),...]`

以上 **9 个图表组件均已渲染 + 转换实测**（元素 0 跳过、转为可编辑形状；rect/line/text/circle/polygon 全覆盖）。

---

## 图表区坐标系统

图表通常嵌入内容页的某个卡片内，或直接占用内容区（D系版式）。

```
图表区内部坐标（相对于宿主卡片）：
  坐标轴原点偏移：左侧轴标签区 w=60，底部轴标签区 h=40
  实际绘图区：x=宿主x+60，y=宿主y+20，w=宿主w-80，h=宿主h-70
  轴线：x轴 y=绘图区底边，y轴 x=绘图区左边
  轴颜色：stroke="#9B9B9B" stroke-width="0.5"
  网格线（水平）：stroke="#E7E7E7" stroke-width="0.5" stroke-dasharray="2,2"
```

---

## 图表底部信息分层（硬性规定）

图表下缘最多容纳**两层**信息（如 X 轴标签 + 一层标注）。需要第三层（图例/门标注/决策语等）时必须重新分配：图例移**右上角与标题同行**；多行标注合并为单行。charts.py 的 fte_ramp 即按此实现（图例右上、门名与决策合并一行）。

## 纵向柱状图模板

适用：数量对比/排名（≤12个数据点）

```svg
<!-- 以宿主卡片为 cx=卡片x，cy=卡片y，cw=卡片w，ch=卡片h 为参数 -->

<!-- Y轴（强制从0开始） -->
<line x1="[cx+60]" y1="[cy+20]" x2="[cx+60]" y2="[cy+ch-50]"
      stroke="#9B9B9B" stroke-width="0.5"/>
<!-- X轴 -->
<line x1="[cx+60]" y1="[cy+ch-50]" x2="[cx+cw-20]" y2="[cy+ch-50]"
      stroke="#9B9B9B" stroke-width="0.5"/>

<!-- 水平网格线（3~5条，等间距） -->
<line x1="[cx+60]" y1="[grid_y]" x2="[cx+cw-20]" y2="[grid_y]"
      stroke="#E7E7E7" stroke-width="0.5" stroke-dasharray="2,2"/>

<!-- Y轴刻度标签 -->
<text x="[cx+54]" y="[grid_y+4]" text-anchor="end"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#9B9B9B">[value]</text>

<!-- 数据柱（每根柱）：默认灰 #9B9B9B，要强调的那一根改 #336EE8 -->
<rect x="[bar_x]" y="[bar_y]" width="[bar_w]" height="[bar_h]"
      fill="#9B9B9B"/>
<!-- 柱顶数值标注（数字 mono） -->
<text x="[bar_x+bar_w/2]" y="[bar_y-6]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" font-weight="bold"
      fill="#262626">[value]</text>
<!-- X轴标签 -->
<text x="[bar_x+bar_w/2]" y="[cy+ch-32]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#6E6E6E">[label]</text>

<!-- Callout（当callout_needed=true时，圈出关键柱） -->
<rect x="[target_x-4]" y="[target_y-4]"
      width="[target_w+8]" height="[target_h+8]"
      rx="2" fill="none" stroke="#9B9B9B" stroke-width="1.5"/>
<rect x="[callout_bx]" y="[callout_by]" width="[callout_bw]" height="24"
      rx="3" fill="#F3F3F3" stroke="#9B9B9B" stroke-width="1"/>
<text x="[callout_bx+callout_bw/2]" y="[callout_by+16]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" font-weight="bold"
      fill="#262626">[annotation]</text>
<line x1="[callout_connect_x]" y1="[callout_by+24]"
      x2="[callout_connect_x]" y2="[target_y-4]"
      stroke="#9B9B9B" stroke-width="0.5" stroke-dasharray="3,2"/>
```

**柱宽计算规则：**
```
n = 数据点数量
plot_w = 绘图区宽度（cw - 80）
bar_w = plot_w / n * 0.6    （柱宽=间隔的0.6倍）
bar_gap = plot_w / n * 0.4
bar_x[i] = cx+60 + i * (plot_w/n) + bar_gap/2
```

**多系列分组柱状图：**
同一分组内各系列色按 brand.md 2.4节顺序排列，组内无间距，组间间距=单柱宽。

---

## 横向柱状图模板

适用：排名展示、长标签场景（≤8项）

```svg
<!-- X轴（从0开始） -->
<line x1="[cx+120]" y1="[cy+ch-30]" x2="[cx+cw-20]" y2="[cy+ch-30]"
      stroke="#9B9B9B" stroke-width="0.5"/>
<!-- 每条横柱：默认灰 #9B9B9B，要强调的那一条改 #336EE8 -->
<rect x="[cx+120]" y="[bar_y]" width="[bar_w]" height="[bar_h]"
      fill="#9B9B9B"/>
<!-- 右侧数值标注 -->
<text x="[cx+120+bar_w+6]" y="[bar_y+bar_h/2+4]"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="12" font-weight="bold"
      fill="#262626">[value]</text>
<!-- 左侧标签 -->
<text x="[cx+114]" y="[bar_y+bar_h/2+4]" text-anchor="end"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="12" fill="#6E6E6E">[label]</text>
```

---

## 折线图模板

适用：趋势变化（时间序列）

```svg
<!-- 坐标轴（同纵向柱状图，但Y轴起点可不为0） -->
<!-- Y轴标注范围说明（当不从0开始时必须） -->
<text x="[cx+60]" y="[cy+16]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="10" fill="#9B9B9B">▲</text>
<text x="[cx+58]" y="[cy+28]" text-anchor="end"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="10" fill="#9B9B9B">[y_max]</text>

<!-- 折线（polyline） -->
<polyline points="[x1,y1 x2,y2 x3,y3 ...]"
          fill="none" stroke="#9B9B9B" stroke-width="2" stroke-linejoin="round"/>
<!-- 数据节点 -->
<circle cx="[xi]" cy="[yi]" r="4" fill="#262626" stroke="#FFFFFF" stroke-width="1.5"/>
<!-- 节点数值（关键节点标注，非全部） -->
<text x="[xi]" y="[yi-10]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" font-weight="bold"
      fill="#262626">[value]</text>

<!-- 目标线（如有） -->
<line x1="[cx+60]" y1="[target_y]" x2="[cx+cw-20]" y2="[target_y]"
      stroke="#5A7A60" stroke-width="1.5" stroke-dasharray="6,3"/>
<text x="[cx+cw-18]" y="[target_y-4]" text-anchor="end"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#5A7A60">目标</text>

<!-- 基准线（如有） -->
<line x1="[cx+60]" y1="[baseline_y]" x2="[cx+cw-20]" y2="[baseline_y]"
      stroke="#9B9B9B" stroke-width="1" stroke-dasharray="4,3"/>
```

---

## 瀑布图模板

适用：KPI→子项贡献拆解，成本/收益分解

```svg
<!-- 基线 -->
<line x1="[cx+60]" y1="[baseline_y]" x2="[cx+cw-20]" y2="[baseline_y]"
      stroke="#9B9B9B" stroke-width="0.5"/>

<!-- 起始/结果总量柱（深墨 #262626） -->
<rect x="[bar0_x]" y="[bar0_y]" width="[bar_w]" height="[bar0_h]" fill="#262626"/>

<!-- 增量柱（灰阶；正负靠位置 + 符号区分，不用红绿）：正向 #9B9B9B / 负向 #C8C8C8 -->
<!-- 正向增量 -->
<rect x="[bar_x]" y="[float_y]" width="[bar_w]" height="[delta_h]" fill="#9B9B9B"/>
<!-- 负向增量（更浅灰区分） -->
<rect x="[bar_x]" y="[float_y]" width="[bar_w]" height="[delta_h]" fill="#C8C8C8"/>
<!-- 浮动连接虚线 -->
<line x1="[prev_bar_x+bar_w]" y1="[prev_top_y]" x2="[bar_x]" y2="[prev_top_y]"
      stroke="#E7E7E7" stroke-width="0.5" stroke-dasharray="2,2"/>

<!-- 结果总量柱（深墨 #262626） -->
<rect x="[bar_last_x]" y="[bar_last_y]" width="[bar_w]" height="[bar_last_h]" fill="#262626"/>

<!-- 柱顶数值 -->
<text x="[bar_x+bar_w/2]" y="[bar_y-6]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" font-weight="bold"
      fill="#262626">[±value]</text>
```

---

## 甘特图模板

适用：项目实施计划（配合直排时间线 / A-90 泳道 / V 系数据页）

```svg
<!-- 时间刻度表头 -->
<rect x="[cx+240]" y="[cy+44]" width="[月宽]" height="30" fill="#F3F3F3"/>
<text x="[月中心x]" y="[cy+64]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="12" fill="#262626">[月份]</text>

<!-- 任务行背景（奇偶交替） -->
<rect x="[cx+240]" y="[row_y]" width="[plot_w]" height="44"
      fill="[奇行#FFFFFF / 偶行#F3F3F3]"/>

<!-- 任务条（默认灰 #9B9B9B；当前/重点一期可用唯一蓝 #336EE8，至多一个，不要每期一色） -->
<rect x="[task_x]" y="[row_y+10]" width="[task_w]" height="24"
      rx="3" fill="[默认#9B9B9B；重点期#336EE8]"/>
<text x="[task_x+task_w/2]" y="[row_y+26]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#FFFFFF">[task_name]</text>

<!-- 里程碑（菱形） -->
<polygon points="[mx],[my-10] [mx+10],[my] [mx],[my+10] [mx-10],[my]"
         fill="#262626"/>
<text x="[mx]" y="[my-14]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="10" fill="#262626">[milestone]</text>

<!-- 左侧任务名称 -->
<text x="[cx+230]" y="[row_y+26]" text-anchor="end"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="12" fill="#262626">[task_name]</text>
```

---

## KPI 指标卡模板（单个组件）

适用：S-09 KPI 看板，也可内嵌于其他版式

```svg
<!-- 卡片底（无边框无阴影；优先不画卡、直接留白排版，需成块才用面板） -->
<rect x="[cx]" y="[cy]" width="[cw]" height="[ch]"
      rx="12" fill="#F3F3F3"/>
<!-- 指标名称 -->
<text x="[cx+16]" y="[cy+30]"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="13" fill="#9B9B9B">[metric_name]</text>
<!-- 核心数字（mono · 墨色；唯一关键指标可用 #336EE8，绝不用红绿染数字） -->
<text x="[cx+16]" y="[cy+ch/2+18]"
      font-family="'JetBrains Mono', Consolas, monospace" font-size="40" font-weight="bold"
      fill="#262626">[value]</text>
<text x="[cx+16+数字宽+6]" y="[cy+ch/2+12]"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="14" fill="#9B9B9B">[unit]</text>
<!-- 同比/环比 = 6px 状态点 + 文字（达标#5A7A60 / 预警#8A7333 / 风险#9E3D31 / 中性#9B9B9B） -->
<circle cx="[cx+21]" cy="[cy+ch-19]" r="3.5" fill="[status_color]"/>
<text x="[cx+34]" y="[cy+ch-14]"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="13" fill="#6E6E6E">[趋势文字 · 如 同比 −3.1 pt]</text>
```

---

## 2×2 四象限模板

适用：S-02 2×2 矩阵 / 风险评估矩阵

```svg
<!-- 背景区 -->
<rect x="[cx]" y="[cy]" width="[cw]" height="[ch]" fill="#FFFFFF"/>
<!-- 纵轴 -->
<line x1="[cx+cw/2]" y1="[cy+20]" x2="[cx+cw/2]" y2="[cy+ch-40]"
      stroke="#9B9B9B" stroke-width="1"/>
<!-- 横轴 -->
<line x1="[cx+20]" y1="[cy+ch/2]" x2="[cx+cw-20]" y2="[cy+ch/2]"
      stroke="#9B9B9B" stroke-width="1"/>
<!-- 轴端箭头 -->
<!-- 轴标签 -->
<text x="[cx+cw/2]" y="[cy+14]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#6E6E6E">[y_high_label]</text>
<text x="[cx+cw/2]" y="[cy+ch-26]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#6E6E6E">[y_low_label]</text>
<text x="[cx+cw-18]" y="[cy+ch/2+14]" text-anchor="end"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#6E6E6E">[x_high_label]</text>
<text x="[cx+22]" y="[cy+ch/2+14]"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" fill="#6E6E6E">[x_low_label]</text>
<!-- 象限标题（左上角） -->
<text x="[各象限左上角x+8]" y="[各象限左上角y+20]"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="13" font-weight="bold"
      fill="#262626">[quadrant_title]</text>
<!-- 内容项 -->
<rect x="[item_x-4]" y="[item_y-14]" width="[item_w+8]" height="20"
      rx="3" fill="#F3F3F3"/>
<text x="[item_x]" y="[item_y]"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="12" fill="#262626">[item_text]</text>
```

---

## Callout 标注模板（通用，可叠加在任何图表上）

```svg
<!-- 1. 圈框（圈住目标元素） -->
<rect x="[target_x-6]" y="[target_y-6]"
      width="[target_w+12]" height="[target_h+12]"
      rx="3" fill="none" stroke="#9B9B9B" stroke-width="1.5"/>

<!-- 2. 连接线（虚线，从气泡到圈框） -->
<line x1="[bubble_cx]" y1="[bubble_bottom_y]"
      x2="[circle_cx]" y2="[target_y-6]"
      stroke="#9B9B9B" stroke-width="0.5" stroke-dasharray="3,2"/>

<!-- 3. 标注气泡 -->
<rect x="[bubble_x]" y="[bubble_y]" width="[bubble_w]" height="26"
      rx="3" fill="#F3F3F3" stroke="#9B9B9B" stroke-width="1"/>
<text x="[bubble_x+bubble_w/2]" y="[bubble_y+17]" text-anchor="middle"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="11" font-weight="bold"
      fill="#262626">[annotation_text]</text>
```

**位置决策规则（优先级从高到低）：**
1. 图表右上角空白区（最常用）
2. 目标元素正上方
3. 目标元素右侧
4. 不得遮挡其他数据点或轴标签
