# -*- coding: utf-8 -*-
"""图表组件库 charts.py（自包含，通用）。

把 chart-impl.md 的手画图表固化成参数化函数：一行调用 = 一张合规专业图表，
不再逐坐标手画。供 V 系（证据/图表版式）与任意需要数据可视化的内容页调用。

—— 严格遵守 brand.md §7.5 / §2.4 图表画法（硬约束）：
   · 数据元素灰阶 #9B9B9B(主) / #C8C8C8(次)，至多一个 #336EE8 高亮“当前/重点项”
   · 坐标轴 #E7E7E7、刻度标签 #6E6E6E / #9B9B9B
   · 无 3D / 阴影 / 渐变 / 饼图 / 环形图；绝不多色（不用红绿区分正负）
   · 正负、阈值靠 “浮动位置 + 数值符号(+/-) + 文字” 区分（双通道），不靠颜色
   · 所有数字等宽 mono；柱状图 Y 轴从 0 起
—— PPTX 兼容：只用 <rect>/<line>/<text>，箭头(如需)用 <polygon>；不用 <marker>/<g rotate>。
   坐标自包含：传入图表外框 (x,y,w,h)，函数内部自动留轴/标签边距。
—— 复用 components.py 的原子函数与颜色常量，不在本文件写死品牌色。
"""
from components import T, L, MONO, ACC, INK1, INK2, INK3, INK4, LINE

BAR_MAIN = INK3        # 数据柱默认灰
BAR_SUB = "#C8C8C8"    # 次级灰（§2.4 允许的次灰）
BAR_TOTAL = INK1       # 瀑布图总量柱（深墨，作锚点）
EDGE = ' stroke="#6E6E6E" stroke-width="1"'  # 面型数据元素轮廓通道（WCAG 1.4.11 非文字对比 3:1；灰面本身 2.78/1.67 不达标）


def _fmt(v, money=False):
    """数值格式：整数加千分位；非整保留 1 位小数。货币加 ¥。"""
    if money:
        return f"\u00a5{v:,.0f}"
    if abs(v - round(v)) < 1e-9:
        return f"{int(round(v)):,}"
    return f"{v:,.1f}"


def waterfall(x, y, w, h, items, hi_index=None, unit="", money=False, title=None):
    """瀑布图：展示某指标从起点到终点的逐项增减拆解。

    items: [(label, value, kind), ...]
        kind='total' → 绝对总量柱（从 0 基线起，深墨；用于期初/期末/小计锚点）
        kind='delta' → 增量柱（浮动；value 带正负号，正=上增、负=下减）
    hi_index: 用唯一蓝(#336EE8)高亮第 i 根柱（强调关键贡献项），None 则全灰。
    unit:   左上角单位说明（如“综合产能指数(基准=100)”）。
    money:  数值是否按 ¥ 千分位格式。
    title:  图表小标题（可选）。
    """
    pad_l = 58
    pad_b = 34
    pad_t = 30 if title else 16
    px = x + pad_l
    pyt = y + pad_t
    pw = w - pad_l - 14
    ph = h - pad_t - pad_b
    n = len(items)
    if n == 0:
        return ""

    # 逐柱累计，得到每根柱的底/顶绝对值 (b0, b1)
    cum = 0.0
    bars = []  # (label, kind, b0, b1, val)
    vmax = 0.0
    for (label, val, kind) in items:
        if kind == "total":
            b0, b1 = 0.0, float(val)
            cum = float(val)
        else:  # delta
            b0, b1 = cum, cum + float(val)
            cum = cum + float(val)
        vmax = max(vmax, b0, b1)
        bars.append((label, kind, b0, b1, float(val)))
    if vmax <= 0:
        vmax = 1.0

    def vy(v):  # 值 -> 像素 y
        return pyt + ph - (v / vmax) * ph

    s = []
    if title:
        s.append(T(x, y + 16, title, 15, INK1, 700))
    if unit:
        s.append(T(px, pyt - 4, unit, 10, INK2))

    # 水平网格 + Y 刻度（3 档）
    for g in range(1, 4):
        gv = vmax * g / 3.0
        gy = vy(gv)
        s.append(L(px, gy, px + pw, gy, LINE, 0.5, dash="2,2"))
        s.append(T(px - 8, gy + 4, _fmt(gv, money), 10, INK3, anchor="end", fam=MONO))

    # Y 轴 + 0 基线
    s.append(L(px, pyt, px, pyt + ph, INK3, 0.6))
    s.append(L(px, pyt + ph, px + pw, pyt + ph, INK3, 0.6))

    slot = pw / n
    bw = slot * 0.56
    gap = slot * 0.44

    prev_b1_py = None
    prev_x_right = None
    for i, (label, kind, b0, b1, val) in enumerate(bars):
        bx = px + i * slot + gap / 2
        ytop = vy(max(b0, b1))
        ybot = vy(min(b0, b1))
        bh = max(ybot - ytop, 1.5)
        if i == hi_index:
            fill = ACC
        elif kind == "total":
            fill = BAR_TOTAL
        else:
            fill = BAR_MAIN
        s.append(f'<rect x="{bx:.1f}" y="{ytop:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{fill}"{EDGE}/>')

        # 浮动连接虚线：从上一柱的“结束累计”高度，水平连到当前柱左侧
        if prev_b1_py is not None:
            s.append(L(prev_x_right, prev_b1_py, bx, prev_b1_py, INK4, 0.6, dash="3,2"))

        # 数值标注（delta 带符号；total 无符号）
        if kind == "delta":
            txt = ("+" if val >= 0 else "-") + _fmt(abs(val), money)
        else:
            txt = _fmt(val, money)
        s.append(T(bx + bw / 2, ytop - 6, txt, 11, INK1, 700, anchor="middle", fam=MONO))

        # X 轴标签（过长自动两行：以空格或全角空格简单折）
        s.append(T(bx + bw / 2, pyt + ph + 18, label, 11, INK2, anchor="middle"))

        prev_b1_py = vy(b1)
        prev_x_right = bx + bw

    return "".join(s)


def bar(x, y, w, h, data, hi_index=None, unit="", money=False, title=None, target=None):
    """纵向柱状图（分类对比/排名，Y 轴从 0 起）。data=[(label,value),...]。
    hi_index 用蓝高亮一项；target 画目标参考虚线（深灰，不用绿）。"""
    pad_l, pad_b, pad_t = 52, 34, (30 if title else 16)
    px = x + pad_l; pyt = y + pad_t; pw = w - pad_l - 14; ph = h - pad_t - pad_b
    n = len(data)
    if n == 0: return ""
    vmax = max([v for _, v in data] + ([target] if target else []))
    if vmax <= 0: vmax = 1.0
    def vy(v): return pyt + ph - (v / vmax) * ph
    s = []
    if title: s.append(T(x, y + 16, title, 15, INK1, 700))
    if unit: s.append(T(px, pyt - 4, unit, 10, INK2))
    for g in range(1, 4):
        gv = vmax * g / 3.0; gy = vy(gv)
        s.append(L(px, gy, px + pw, gy, LINE, 0.5, dash="2,2"))
        s.append(T(px - 8, gy + 4, _fmt(gv, money), 10, INK3, anchor="end", fam=MONO))
    s.append(L(px, pyt, px, pyt + ph, INK3, 0.6))
    s.append(L(px, pyt + ph, px + pw, pyt + ph, INK3, 0.6))
    slot = pw / n; bw = slot * 0.56; gap = slot * 0.44
    for i, (label, val) in enumerate(data):
        bx = px + i * slot + gap / 2; ytop = vy(val); bh = max(pyt + ph - ytop, 1.5)
        fill = ACC if i == hi_index else BAR_MAIN
        s.append(f'<rect x="{bx:.1f}" y="{ytop:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{fill}"{EDGE}/>')
        s.append(T(bx + bw / 2, ytop - 6, _fmt(val, money), 11, INK1, 700, anchor="middle", fam=MONO))
        s.append(T(bx + bw / 2, pyt + ph + 18, label, 11, INK2, anchor="middle"))
    if target:
        ty = vy(target)
        s.append(L(px, ty, px + pw, ty, INK2, 1, dash="5,3"))
        s.append(T(px + pw, ty - 5, f"目标 {_fmt(target, money)}", 10, INK2, anchor="end"))
    return "".join(s)


def hbar(x, y, w, h, data, hi_index=None, money=False, title=None):
    """横向柱状图（排名/长标签，≤8项）。data=[(label,value),...] 自上而下。"""
    pad_l = 140; pad_t = (30 if title else 8); pad_r = 70
    px = x + pad_l; pyt = y + pad_t; pw = w - pad_l - pad_r; ph = h - pad_t - 8
    n = len(data)
    if n == 0: return ""
    vmax = max(v for _, v in data) or 1.0
    s = []
    if title: s.append(T(x, y + 16, title, 15, INK1, 700))
    rowh = ph / n; bh = min(rowh * 0.5, 26)
    for i, (label, val) in enumerate(data):
        cy = pyt + i * rowh + rowh / 2; bw = (val / vmax) * pw
        fill = ACC if i == hi_index else BAR_MAIN
        s.append(T(x + pad_l - 12, cy + 4, label, 12.5, INK2, anchor="end"))
        s.append(f'<rect x="{px:.1f}" y="{cy - bh/2:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{fill}"{EDGE}/>')
        s.append(T(px + bw + 8, cy + 4, _fmt(val, money), 12, INK1, 700, fam=MONO))
    return "".join(s)


def line(x, y, w, h, values, xlabels, hi_last=True, unit="", money=False, title=None, target=None, ymin=None):
    """折线趋势图（时间序列）。values 单系列；折线用 <line> 段（转换器明确支持）。
    数据点用 <circle>；hi_last 末点高亮蓝；target 画目标虚线。默认 Y 从 0。"""
    pad_l = 52; pad_b = 30; pad_t = (30 if title else 16)
    px = x + pad_l; pyt = y + pad_t; pw = w - pad_l - 16; ph = h - pad_t - pad_b
    n = len(values)
    if n < 2: return ""
    vmax = max(values + ([target] if target else []))
    vlo = 0 if ymin is None else ymin
    rng = (vmax - vlo) or 1.0
    def vy(v): return pyt + ph - ((v - vlo) / rng) * ph
    def vx(i): return px + pw * (i / (n - 1))
    s = []
    if title: s.append(T(x, y + 16, title, 15, INK1, 700))
    if unit: s.append(T(px, pyt - 4, unit, 10, INK2))
    for g in range(0, 4):
        gv = vlo + rng * g / 3.0; gy = vy(gv)
        s.append(L(px, gy, px + pw, gy, LINE, 0.5, dash="2,2"))
        s.append(T(px - 8, gy + 4, _fmt(gv, money), 10, INK3, anchor="end", fam=MONO))
    s.append(L(px, pyt, px, pyt + ph, INK3, 0.6))
    s.append(L(px, pyt + ph, px + pw, pyt + ph, INK3, 0.6))
    for i in range(n - 1):
        s.append(L(vx(i), vy(values[i]), vx(i + 1), vy(values[i + 1]), INK1, 2))
    if target:
        ty = vy(target); s.append(L(px, ty, px + pw, ty, INK2, 1, dash="5,3"))
        s.append(T(px + pw, ty - 5, f"目标 {_fmt(target, money)}", 10, INK2, anchor="end"))
    for i, v in enumerate(values):
        cx = vx(i); cy = vy(v); last = (i == n - 1)
        col = ACC if (hi_last and last) else INK1
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="{col}"/>')
        if last or i == 0:
            s.append(T(cx, cy - 10, _fmt(v, money), 11, col, 700, anchor="middle", fam=MONO))
        s.append(T(cx, pyt + ph + 18, xlabels[i], 10, INK2, anchor="middle"))
    return "".join(s)


def funnel(x, y, w, h, stages, hi_index=None, money=False, title=None):
    """漏斗图（转化/收窄流程）。stages=[(label,value),...] 自上而下递减。
    用居中梯形(polygon)逐级收窄；级间标转化率。灰阶交替 + 可一个蓝高亮。"""
    pad_t = 30 if title else 8
    py0 = y + pad_t
    ph = h - pad_t - 8
    n = len(stages)
    if n == 0:
        return ""
    vmax = max(v for _, v in stages) or 1.0
    seg_h = ph / n * 0.7
    gap = ph / n * 0.3
    cx = x + w * 0.40
    maxw = w * 0.50
    s = []
    if title:
        s.append(T(x, y + 16, title, 15, INK1, 700))
    prev_val = None
    for i, (label, val) in enumerate(stages):
        topw = (val / vmax) * maxw
        nxtval = stages[i + 1][1] if i + 1 < n else val
        botw = (nxtval / vmax) * maxw
        yt = py0 + i * (seg_h + gap)
        yb = yt + seg_h
        fill = ACC if i == hi_index else (BAR_MAIN if i % 2 == 0 else BAR_SUB)
        pts = (f"{cx-topw/2:.1f},{yt:.1f} {cx+topw/2:.1f},{yt:.1f} "
               f"{cx+botw/2:.1f},{yb:.1f} {cx-botw/2:.1f},{yb:.1f}")
        s.append(f'<polygon points="{pts}" fill="{fill}"{EDGE}/>')
        s.append(T(x + w * 0.70, yt + seg_h / 2 - 3, label, 12.5, INK1, 600))
        s.append(T(x + w * 0.70, yt + seg_h / 2 + 15, _fmt(val, money), 13, INK1, 700, fam=MONO))
        if prev_val is not None and prev_val > 0:
            rate = val / prev_val * 100
            s.append(T(cx, yt - gap / 2 + 4, f"{rate:.0f}%", 10.5, INK2, anchor="middle", fam=MONO))
        prev_val = val
    return "".join(s)


def gantt(x, y, w, h, tasks, total_units, today=None, unit_label="", title=None):
    """甘特图（分期排期）。tasks=[(name,start,dur[,hi]),...]，start/dur 以 total_units 为轴总长。
    hi=True 高亮蓝；today 画今日竖虚线。只用 rect/line/text。"""
    pad_l = 150
    pad_t = 30 if title else 8
    pad_b = 24
    px = x + pad_l
    pyt = y + pad_t
    pw = w - pad_l - 16
    ph = h - pad_t - pad_b
    n = len(tasks)
    if n == 0 or total_units <= 0:
        return ""
    def ux(u):
        return px + (u / total_units) * pw
    s = []
    if title:
        s.append(T(x, y + 16, title, 15, INK1, 700))
    rowh = ph / n
    barh = min(rowh * 0.52, 22)
    grid = max(1, round(total_units / 6))
    u = 0
    while u <= total_units + 0.01:
        gx = ux(u)
        s.append(L(gx, pyt - 4, gx, pyt + ph, LINE, 0.5, dash="2,2"))
        s.append(T(gx, pyt - 8, f"{int(u)}", 9.5, INK3, anchor="middle", fam=MONO))
        u += grid
    for i, t in enumerate(tasks):
        name, start, dur = t[0], t[1], t[2]
        hi = t[3] if len(t) > 3 else False
        cy = pyt + i * rowh + rowh / 2
        bx = ux(start)
        bw = (dur / total_units) * pw
        fill = ACC if hi else BAR_MAIN
        s.append(T(x + pad_l - 12, cy + 4, name, 12, INK2, anchor="end"))
        s.append(f'<rect x="{bx:.1f}" y="{cy-barh/2:.1f}" width="{bw:.1f}" height="{barh:.1f}" rx="3" fill="{fill}"{EDGE}/>')
        s.append(T(bx + bw + 6, cy + 4, f"{dur}{unit_label}", 10, INK2, fam=MONO))
    if today is not None:
        tx = ux(today)
        s.append(L(tx, pyt - 6, tx, pyt + ph, INK1, 1.2, dash="4,2"))
        s.append(T(tx, pyt + ph + 14, "今日", 9.5, INK1, 600, anchor="middle"))
    return "".join(s)


def bullet(x, y, w, h, metrics, hi_index=None, money=False, title=None):
    """子弹图（多指标 实际 vs 目标）。metrics=[(label,actual,target,max),...]。
    背景=max(浅灰)，实际条=灰(或蓝高亮重点行)，目标=黑竖线。达标与否靠条末是否过目标线(双通道)，不用红绿。"""
    pad_l = 150
    pad_t = 30 if title else 8
    pad_r = 72
    px = x + pad_l
    pyt = y + pad_t
    pw = w - pad_l - pad_r
    ph = h - pad_t - 8
    n = len(metrics)
    if n == 0:
        return ""
    s = []
    if title:
        s.append(T(x, y + 16, title, 15, INK1, 700))
    rowh = ph / n
    barh = min(rowh * 0.42, 18)
    for i, (label, actual, target, mx) in enumerate(metrics):
        cy = pyt + i * rowh + rowh / 2
        mx = mx or 1.0
        s.append(f'<rect x="{px:.1f}" y="{cy-barh/2:.1f}" width="{pw:.1f}" height="{barh:.1f}" fill="{LINE}"/>')
        aw = min(actual / mx, 1.0) * pw
        fill = ACC if i == hi_index else BAR_MAIN
        s.append(f'<rect x="{px:.1f}" y="{cy-barh/2:.1f}" width="{aw:.1f}" height="{barh:.1f}" fill="{fill}"{EDGE}/>')
        tx = px + min(target / mx, 1.0) * pw
        s.append(L(tx, cy - barh / 2 - 4, tx, cy + barh / 2 + 4, INK1, 1.8))
        s.append(T(x + pad_l - 12, cy + 4, label, 12, INK2, anchor="end"))
        s.append(T(px + pw + 8, cy + 4, _fmt(actual, money), 11.5, INK1, 700, fam=MONO))
    return "".join(s)


def stacked(x, y, w, h, data, seriesnames, hi_series=None, unit="", money=False, title=None):
    """堆叠柱状图（构成随时间变化，≤4段）。data=[(label,[v1,v2,...]),...]；seriesnames=[...]。
    段用灰阶明度区分，可一个蓝高亮某 series。Y 从 0，柱顶标合计，底部图例。"""
    pad_l = 52; pad_b = 46; pad_t = 30 if title else 16
    px = x + pad_l; pyt = y + pad_t; pw = w - pad_l - 14; ph = h - pad_t - pad_b
    n = len(data)
    if n == 0: return ""
    totals = [sum(vals) for _, vals in data]
    vmax = max(totals) or 1.0
    def vy(v): return pyt + ph - (v / vmax) * ph
    grays = ["#C8C8C8", INK3, INK2, INK1]   # 4 级灰阶（白名单内：#C8C8C8/#9B9B9B/#6E6E6E/#262626）
    s = []
    if title: s.append(T(x, y + 16, title, 15, INK1, 700))
    if unit: s.append(T(px, pyt - 4, unit, 10, INK2))
    for g in range(1, 4):
        gv = vmax * g / 3.0; gy = vy(gv)
        s.append(L(px, gy, px + pw, gy, LINE, 0.5, dash="2,2"))
        s.append(T(px - 8, gy + 4, _fmt(gv, money), 10, INK3, anchor="end", fam=MONO))
    s.append(L(px, pyt, px, pyt + ph, INK3, 0.6))
    s.append(L(px, pyt + ph, px + pw, pyt + ph, INK3, 0.6))
    slot = pw / n; bw = slot * 0.56; gap = slot * 0.44
    for i, (label, vals) in enumerate(data):
        bx = px + i * slot + gap / 2; ybase = pyt + ph
        for k, v in enumerate(vals):
            segh = (v / vmax) * ph
            col = ACC if k == hi_series else grays[k % len(grays)]
            s.append(f'<rect x="{bx:.1f}" y="{ybase-segh:.1f}" width="{bw:.1f}" height="{segh:.1f}" fill="{col}"{EDGE}/>')
            ybase -= segh
        s.append(T(bx + bw / 2, pyt + ph + 18, label, 11, INK2, anchor="middle"))
        s.append(T(bx + bw / 2, vy(totals[i]) - 6, _fmt(totals[i], money), 10.5, INK1, 700, anchor="middle", fam=MONO))
    lx = px; ly = y + h - 20
    for k, nm in enumerate(seriesnames):
        col = ACC if k == hi_series else grays[k % len(grays)]
        s.append(f'<rect x="{lx:.1f}" y="{ly:.1f}" width="11" height="11" rx="2" fill="{col}"{EDGE}/>')
        s.append(T(lx + 16, ly + 9.5, nm, 10.5, INK2))
        lx += 16 + len(nm) * 13 + 20
    return "".join(s)


def slope(x, y, w, h, items, label_left="前", label_right="后", hi_index=None, money=False, title=None):
    """坡度图（两个时点的前后对比）。items=[(name,vleft,vright),...] 每项一条线连左右两点。
    线 + 端点 circle + 标签，可一个蓝高亮重点项。"""
    pad_t = 34 if title else 20; pad_b = 16
    pyt = y + pad_t; ph = h - pad_t - pad_b
    lx = x + w * 0.30; rx = x + w * 0.70
    n = len(items)
    if n == 0: return ""
    allv = [v for _, vl, vr in items for v in (vl, vr)]
    vmax = max(allv); vmin = min(allv); rng = (vmax - vmin) or 1.0
    def vy(v): return pyt + ph - ((v - vmin) / rng) * ph
    s = []
    if title: s.append(T(x, y + 16, title, 15, INK1, 700))
    s.append(T(lx, pyt - 12, label_left, 11, INK2, 600, anchor="middle"))
    s.append(T(rx, pyt - 12, label_right, 11, INK2, 600, anchor="middle"))
    s.append(L(lx, pyt, lx, pyt + ph, LINE, 0.6))
    s.append(L(rx, pyt, rx, pyt + ph, LINE, 0.6))
    for i, (name, vl, vr) in enumerate(items):
        yl = vy(vl); yr = vy(vr)
        col = ACC if i == hi_index else INK2
        sw = 2.4 if i == hi_index else 1.4
        s.append(L(lx, yl, rx, yr, col, sw))
        s.append(f'<circle cx="{lx:.1f}" cy="{yl:.1f}" r="3.5" fill="{col}"/>')
        s.append(f'<circle cx="{rx:.1f}" cy="{yr:.1f}" r="3.5" fill="{col}"/>')
        tc = INK1 if i == hi_index else INK2
        s.append(T(lx - 10, yl + 4, f"{name} {_fmt(vl, money)}", 11, tc, anchor="end"))
        s.append(T(rx + 10, yr + 4, _fmt(vr, money), 11, tc, 700, fam=MONO))
    return "".join(s)


# ==================================================================== v2.7 追加
# 依据 2026-07 版式库对标评估 + 两批版式调研（Wave 1–3）。追加式扩展：
# 上方 9 个既有图表函数一行未动。

def sparkline(x, y, w, h, values, hi_last=True, baseline=None):
    """迷你趋势线（无轴无标签，Few 式 KPI 卡内嵌用；也可独立点缀表格行）。"""
    n = len(values)
    if n < 2:
        return ""
    vmax, vmin = max(values), min(values)
    rng = (vmax - vmin) or 1.0
    vy = lambda v: y + h - ((v - vmin) / rng) * h
    vx = lambda i: x + w * (i / (n - 1))
    s = []
    if baseline is not None and vmin <= baseline <= vmax:
        s.append(L(x, vy(baseline), x + w, vy(baseline), INK4, 0.8, dash="3,2"))
    for i in range(n - 1):
        s.append(L(vx(i), vy(values[i]), vx(i + 1), vy(values[i + 1]), INK2, 1.6))
    col = ACC if hi_last else INK1
    s.append(f'<circle cx="{vx(n-1):.1f}" cy="{vy(values[-1]):.1f}" r="3.2" fill="{col}"/>')
    return "".join(s)


def kpi_card(x, y, w, h, label, value, benchmark=None, trend=None, unit="",
             bench_label="目标", money=False, hi=False):
    """Few 式 KPI 卡（S-09 高阶）：当前值 + 对比基准 + 迷你 sparkline + 状态。
    依据 Stephen Few《Information Dashboard Design》：KPI 不应是孤立数字格。
    品牌适配：Few 原文的「状态色」在本体系改为**符号+文字双通道**
    （+/- 号 + 达标/未达字样）——brand 图表铁律禁红绿。"""
    bc = ACC if hi else LINE
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{bc}" stroke-width="{1.8 if hi else 1.2}"/>'
    if hi:
        s += f'<rect x="{x}" y="{y}" width="3" height="{h}" rx="1.5" fill="{ACC}"/>'
    s += T(x + 16, y + 24, label, 12, INK2, w=600)
    vtxt = _fmt(value, money) + (f" {unit}" if unit else "")
    s += T(x + 16, y + 58, vtxt, 27, (ACC if hi else INK1), w=700, fam=MONO)
    if benchmark is not None:
        d = value - benchmark
        sign = "+" if d >= 0 else "-"
        status = "达标" if d >= 0 else "未达"
        s += T(x + 16, y + 80, f"{bench_label} {_fmt(benchmark, money)}", 10.5, INK3, fam=MONO)
        s += T(x + w - 16, y + 80, f"{sign}{_fmt(abs(d), money)} {status}", 11,
               INK1, w=700, fam=MONO, anchor="end")
    if trend:
        s += sparkline(x + 16, y + h - 38, w - 32, 24, trend, hi_last=hi,
                       baseline=benchmark)
    return s


def marimekko(x, y, w, h, columns, seriesnames, wlabel, mode="pct",
              hi_series=None, money=False, title=None):
    """Marimekko / Mekko 市场地图（V-94）：列宽 ∝ 列总量、列内分段构成，
    面积 ∝ 绝对值，gap=0（Mekko 视觉判据）。columns=[(列名, [段值...], 列宽量?)]，
    列宽量缺省 = sum(段值)；mode='pct' 列高统一 100% / 'abs' 列高 ∝ 列合计
    （Bar Mekko，此时列宽量必须显式给出）。wlabel（列宽代表什么量）**必填并画出**。
    纪律（调研）：≤7 列、≤4 段；时间序列/需精确比较勿用。"""
    if len(columns) > 7:
        raise ValueError("Marimekko 限 ≤7 列（列宽变化的哈哈镜效应随列数放大）")
    if len(seriesnames) > 4:
        raise ValueError("Marimekko 限 ≤4 段（灰阶只有 4 级）")
    pad_l = 46 if mode == "abs" else 40
    pad_b, pad_t = 52, (30 if title else 18)
    px, pyt = x + pad_l, y + pad_t
    pw, ph = w - pad_l - 14, h - pad_t - pad_b
    widths, sums = [], []
    for colm in columns:
        segs = colm[1]
        cw_v = colm[2] if (len(colm) > 2 and colm[2] is not None) else sum(segs)
        if mode == "abs" and (len(colm) < 3 or colm[2] is None):
            raise ValueError("mode='abs'（Bar Mekko）时每列须显式给列宽量（第 3 元）")
        widths.append(float(cw_v))
        sums.append(float(sum(segs)))
    wtot = sum(widths) or 1.0
    smax = max(sums) or 1.0
    grays = ["#C8C8C8", INK3, INK2, INK1]
    s = []
    if title:
        s.append(T(x, y + 16, title, 15, INK1, 700))
    if mode == "pct":
        for gv, gl in ((0, "0"), (0.5, "50%"), (1.0, "100%")):
            gy = pyt + ph * (1 - gv)
            s.append(L(px, gy, px + pw, gy, LINE, 0.6, dash="2,2"))
            s.append(T(px - 6, gy + 4, gl, 9.5, INK2, anchor="end", fam=MONO))
    else:
        for g in range(1, 4):
            gv = smax * g / 3.0
            gy = pyt + ph * (1 - g / 3.0)
            s.append(L(px, gy, px + pw, gy, LINE, 0.6, dash="2,2"))
            s.append(T(px - 6, gy + 4, _fmt(gv, money), 9.5, INK3, anchor="end", fam=MONO))
    cx = px
    for i, colm in enumerate(columns):
        label, segs = colm[0], colm[1]
        cw_ = pw * widths[i] / wtot
        colh = ph if mode == "pct" else ph * sums[i] / smax
        ybase = pyt + ph
        denom = sums[i] or 1.0
        for k, v in enumerate(segs):
            segh = colh * (v / denom)
            col = ACC if k == hi_series else grays[k % len(grays)]
            s.append(f'<rect x="{cx:.1f}" y="{ybase-segh:.1f}" width="{cw_:.1f}" height="{segh:.1f}" fill="{col}"{EDGE}/>')
            if segh >= 18 and cw_ >= 44:
                s.append(T(cx + cw_ / 2, ybase - segh / 2 + 4, f"{v/denom*100:.0f}%",
                           9.5, "#FFFFFF", 700, anchor="middle", fam=MONO))
            ybase -= segh
        s.append(L(cx, pyt + ph - colh, cx, pyt + ph, "#FFFFFF", 1))   # 列间白细线（gap=0）
        s.append(T(cx + cw_ / 2, pyt + ph - colh - 6, _fmt(widths[i], money), 10.5,
                   INK1, 700, anchor="middle", fam=MONO))
        s.append(T(cx + cw_ / 2, pyt + ph + 16, label, 10.5, INK2, anchor="middle"))
        s.append(T(cx + cw_ / 2, pyt + ph + 30, f"{widths[i]/wtot*100:.0f}%", 9,
                   INK2, anchor="middle", fam=MONO))
        cx += cw_
    s.append(L(px, pyt + ph, px + pw, pyt + ph, INK3, 0.8))
    lx = px
    ly = y + h - 8
    for k, nm in enumerate(seriesnames):
        col = ACC if k == hi_series else grays[k % len(grays)]
        s.append(f'<rect x="{lx:.1f}" y="{ly-10}" width="11" height="11" rx="2" fill="{col}"{EDGE}/>')
        s.append(T(lx + 16, ly, nm, 10.5, INK2))
        lx += 16 + len(nm) * 12 + 20
    s.append(T(px + pw, ly, f"列宽 ∝ {wlabel}", 9.5, INK4, anchor="end"))
    return "".join(s)


def fte_ramp(x, y, w, h, periods, waves, wave_names, gates=None, unit="FTE",
             title=None, force=None):
    """FTE 人力爬坡（A-91）：波次堆叠 + stage-gate 决策门 + 波次分界虚线。
    periods=[期名]；waves=[[各期值] × 波次]（自底向上叠）；
    gates=[(期位置, 门名, 决策语)]，位置以期序 0..n-1 连续值计。
    选型纪律（Datawrapper）：时间点 <10 自动用堆叠柱，≥10 用堆叠面积；
    force='area'/'column' 可覆盖。"""
    from structures import gate as _gate, flag_line as _flag
    n = len(periods)
    if any(len(row) != n for row in waves):
        raise ValueError("每个波次的取值个数必须等于期数")
    mode = force or ("area" if n >= 10 else "column")
    pad_l, pad_b, pad_t = 52, 56, (30 if title else 18)
    px, pyt = x + pad_l, y + pad_t
    pw, ph = w - pad_l - 16, h - pad_t - pad_b
    totals = [sum(wv[i] for wv in waves) for i in range(n)]
    vmax = max(totals) or 1.0
    vy = lambda v: pyt + ph - (v / vmax) * ph
    grays = ["#C8C8C8", INK3, INK2, INK1]
    s = []
    if title:
        s.append(T(x, y + 16, title, 15, INK1, 700))
    s.append(T(px, pyt - 6, unit, 10, INK2))
    for g in range(1, 4):
        gv = vmax * g / 3.0
        s.append(L(px, vy(gv), px + pw, vy(gv), LINE, 0.5, dash="2,2"))
        s.append(T(px - 8, vy(gv) + 4, _fmt(gv), 10, INK3, anchor="end", fam=MONO))
    s.append(L(px, pyt, px, pyt + ph, INK3, 0.6))
    s.append(L(px, pyt + ph, px + pw, pyt + ph, INK3, 0.6))
    if mode == "area":
        ux = lambda i: px + pw * (i / (n - 1))
        cum = [0.0] * n
        for k, wv in enumerate(waves):
            lower = cum[:]
            cum = [cum[i] + wv[i] for i in range(n)]
            pts = " ".join(f"{ux(i):.1f},{vy(cum[i]):.1f}" for i in range(n))
            pts += " " + " ".join(f"{ux(i):.1f},{vy(lower[i]):.1f}" for i in range(n - 1, -1, -1))
            s.append(f'<polygon points="{pts}" fill="{grays[k % 4]}" opacity="0.92"/>')
        step = max(1, n // 8)
        for i in range(0, n, step):
            s.append(T(ux(i), pyt + ph + 16, periods[i], 9.5, INK2, anchor="middle"))
        pk = totals.index(max(totals))
        anc = "end" if pk > n * 0.8 else ("start" if pk < n * 0.2 else "middle")
        s.append(T(ux(pk), vy(totals[pk]) - 8, f"峰值 {_fmt(totals[pk])}", 10.5, INK1, 700,
                   anchor=anc, fam=MONO))
        gx = ux
    else:
        slot = pw / n
        bw_ = slot * 0.56
        for i in range(n):
            bx = px + i * slot + slot * 0.22
            ybase = pyt + ph
            for k, wv in enumerate(waves):
                segh = (wv[i] / vmax) * ph
                s.append(f'<rect x="{bx:.1f}" y="{ybase-segh:.1f}" width="{bw_:.1f}" height="{segh:.1f}" fill="{grays[k % 4]}"{EDGE}/>')
                ybase -= segh
            s.append(T(bx + bw_ / 2, vy(totals[i]) - 6, _fmt(totals[i]), 10, INK1, 700,
                       anchor="middle", fam=MONO))
            s.append(T(bx + bw_ / 2, pyt + ph + 16, periods[i], 9.5, INK2, anchor="middle"))
        gx = lambda u: px + (u + 0.5) * (pw / n)
    for (gu, gl, gd) in (gates or []):
        s.append(_flag(gx(gu), pyt, pyt + ph, None, c=INK2, dash="5,4"))
        lab = f"{gl} · {gd}" if gd else gl
        s.append(_gate(gx(gu), pyt + ph + 32, lab, None, size=8))
    lx = x + w - 16                                   # 图例右上（底部留给轴标/门标）
    for k in range(len(wave_names) - 1, -1, -1):
        nm = wave_names[k]
        lx -= len(nm) * 12 + 4
        s.append(T(lx, y + 16, nm, 10.5, INK2))
        lx -= 15
        s.append(f'<rect x="{lx:.1f}" y="{y+6}" width="11" height="11" rx="2" fill="{grays[k % 4]}"{EDGE}/>')
        lx -= 18
    return "".join(s)


def horizon_curves(x, y, w, h, horizons=None, xlab="时间", ylab="价值", hi=2):
    """三地平线 S 曲线族（E-91 · McKinsey Three Horizons，Baghai/Coley/White 1999）：
    3 条错峰递高的 S 曲线（接力/衰减与再生），非装饰山丘。
    horizons=[(名, 注)]×3（缺省 H1/H2/H3 标准语）；hi 高亮第 i 条（默认 H3）。
    仅表达概念形态，无刻度——函数强制绘制「概念示意」标注。
    纯里程碑阶段链请用 E-90 雪佛龙，勿用本版式。"""
    import math
    horizons = horizons or [("地平线 1", "守住核心业务"),
                            ("地平线 2", "壮大新兴业务"),
                            ("地平线 3", "培育未来期权")]
    if len(horizons) not in (3, 4):
        raise ValueError("三地平线标准形态为 3 条曲线（至多 4）")
    pad_l, pad_b, pad_t = 34, 36, 14
    px, pyt = x + pad_l, y + pad_t
    pw, ph = w - pad_l - 20, h - pad_t - pad_b
    s = []
    s.append(L(px, pyt + ph, px + pw - 8, pyt + ph, INK3, 1.2))
    s.append(f'<polygon points="{px+pw},{pyt+ph} {px+pw-9},{pyt+ph-4} {px+pw-9},{pyt+ph+4}" fill="{INK3}"/>')
    s.append(L(px, pyt + ph, px, pyt + 8, INK3, 1.2))
    s.append(f'<polygon points="{px},{pyt} {px-4},{pyt+9} {px+4},{pyt+9}" fill="{INK3}"/>')
    s.append(T(px + pw, pyt + ph + 18, xlab, 10.5, INK2, 700, anchor="end"))
    s.append(T(px - 6, pyt + 4, ylab, 10.5, INK2, 700, anchor="end"))
    m = len(horizons)
    cols = [BAR_SUB, INK3, INK1, INK2]
    for k, (nm, note) in enumerate(horizons):
        t0 = 0.16 + 0.30 * k                # S 中点右移（接力）
        amp = 0.42 + (0.50 / max(m - 1, 1)) * k   # 峰值递高
        col = ACC if k == hi else cols[k % 4]
        pts = []
        N = 44
        for j in range(N + 1):
            t = j / N
            v = amp / (1.0 + math.exp(-11.0 * (t - t0)))
            pts.append((px + pw * 0.965 * t, pyt + ph - v * ph * 0.94))
        d = "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts)
        s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{2.6 if k == hi else 2}"/>')
        lx_, ly_ = pts[-1]
        s.append(T(lx_ + 4, ly_ - 8, nm, 12, (ACC if k == hi else INK1), 700))
        s.append(T(lx_ + 4, ly_ + 8, note, 9.5, INK2))
    s.append(T(px + 4, pyt + ph - 6, "概念示意 · 无刻度", 9, INK4))
    return "".join(s)


def small_multiples(x, y, w, h, kind, datasets, cols=None, unit="", shared_max=None):
    """V-05 小倍数网格（small multiples）：同图型、同坐标尺度的 4–12 个小图网格，
    只让数据变、设计不变。kind="line"|"bar"；datasets=[(标题, [数值])]；
    **全格共享同一 Y 尺度**（函数强制取全局最大值，Tufte 定义的核心纪律）。
    来源：Edward Tufte, *The Visual Display of Quantitative Information*, Graphics Press, 1983
    （调研报告候选10）。与 V-04 双图对比分工：2 图深对比→V-04；6+ 同构横扫→本图。"""
    if kind not in ("line", "bar"):
        raise ValueError("V-05 kind 仅支持 line / bar")
    n = len(datasets)
    if not 4 <= n <= 12:
        raise ValueError("V-05 小图数限 4–12（少于 4 用 V-04/单图），收到 %d" % n)
    L_ = max(len(vals) for _, vals in datasets)
    if any(len(vals) != L_ for _, vals in datasets):
        raise ValueError("V-05 各小图数据点数必须一致（同构才可比）")
    cols = cols or (4 if n > 9 else 3 if n > 4 else 2)
    rows = -(-n // cols)
    gm = shared_max if shared_max is not None else max(max(vals) for _, vals in datasets)
    if gm <= 0:
        raise ValueError("V-05 全局最大值须 >0")
    cw, ch = (w - (cols - 1) * 24) / cols, (h - (rows - 1) * 20) / rows
    s = ""
    for i, (tt, vals) in enumerate(datasets):
        gx = x + (i % cols) * (cw + 24)
        gy = y + (i // cols) * (ch + 20)
        s += f'<rect x="{gx:.1f}" y="{gy:.1f}" width="{cw:.1f}" height="{ch:.1f}" fill="#FFFFFF" stroke="{LINE}" stroke-width="1"/>'
        s += T(gx + 10, gy + 20, tt, 11.5, INK1, 700)
        ax, ay = gx + 10, gy + 30
        aw, ah = cw - 20, ch - 48
        s += L(ax, ay + ah, ax + aw, ay + ah, INK3, 1)
        if kind == "bar":
            bw = aw / L_ * 0.62
            for j, v in enumerate(vals):
                bx = ax + (j + 0.19) * aw / L_
                bh = v / gm * ah
                s += f'<rect x="{bx:.1f}" y="{ay+ah-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{INK2}"{EDGE}/>'
        else:
            pts = " ".join(f"{ax + j*aw/(L_-1):.1f},{ay+ah - v/gm*ah:.1f}" for j, v in enumerate(vals))
            s += f'<polyline points="{pts}" fill="none" stroke="{INK1}" stroke-width="1.8"/>'
        s += T(gx + cw - 10, gy + 20, f"{vals[-1]:g}{unit}", 11, INK2, fam=MONO, anchor="end")
    s += T(x, y + h + 18, f"全部小图共享同一纵轴尺度（0–{gm:g}{unit}）", 10.5, "#6E6E6E")
    return s
