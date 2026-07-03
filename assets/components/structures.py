# -*- coding: utf-8 -*-
"""structures.py · 咨询结构版式层（v2.7，Wave 1–3）

承接 2026-07《版式库全量对标评估》与两批版式调研的落地实现：
矩阵 / 树 / 泳道 / 分层网格类"AI 徒手画不对齐"的结构版式，全部参数化。

—— 共享引擎（评估建议的一次投入多处复用）：
   · grid_cells()  网格对齐引擎 → raci_matrix / service_blueprint 复用
   · issue_tree()  内置树对齐（分层对齐 + 父节点居中于子组）→ G-01 正式 issue tree
   · 标注记号 milestone()/gate()/flag_line() → 路线图与 charts.fte_ramp 共用
—— 视觉硬约束同 charts.py / consulting.py：灰阶为主 + 至多一个 #336EE8 高亮；
   无渐变/阴影/饼图/红绿；数字 mono；正负与状态靠「符号+文字」双通道。
—— PPTX 兼容（designer-rules 约束1–7）：箭头 line+polygon；禁 text/ellipse rotate
   （竖排能力条用「单字逐个 <text> 纵向堆叠」实现，非旋转）；✓ 用 consulting.check()。
—— API 约定：传外框 (x,y,w,h)，返回 SVG 字符串，坐标自包含；chrome 不归本层。
"""
import math
from components import T, L, MONO, SANS, ACC, INK1, INK2, INK3, INK4, LINE, PANEL
from consulting import leader, _arrhead

GRAY_A = INK3
GRAY_B = "#C8C8C8"


# ============================================================ 共享引擎与记号

def grid_cells(x, y, w, h, rows, cols, label_w=0, header_h=0):
    """网格对齐引擎：返回 (cell(r,c)->(cx,cy,cw,ch), 网格线 svg)。
    label_w 左侧行标签列宽、header_h 顶部表头行高，均不计入 cell 区。"""
    gx, gy = x + label_w, y + header_h
    gw, gh = w - label_w, h - header_h
    cw, ch = gw / cols, gh / rows

    def cell(r, c):
        return (gx + c * cw, gy + r * ch, cw, ch)

    s = ""
    for r in range(rows + 1):
        s += L(gx, gy + r * ch, gx + gw, gy + r * ch, LINE, 1)
    for c in range(cols + 1):
        s += L(gx + c * cw, gy, gx + c * cw, gy + gh, LINE, 1)
    return cell, s


def milestone(cx, cy, label=None, r=7, c=INK1):
    """里程碑菱形（路线图轴头 / 图内标记通用）。"""
    pts = f"{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}"
    s = f'<polygon points="{pts}" fill="{c}"/>'
    if label:
        s += T(cx, cy - r - 6, label, 9.5, INK1, w=700, anchor="middle")
    return s


def gate(cx, base_y, label=None, decision=None, size=9, c=INK1):
    """stage-gate 决策门三角（顶点朝上，坐落于轴线 base_y）。"""
    pts = f"{cx},{base_y-size} {cx+size*0.9},{base_y} {cx-size*0.9},{base_y}"
    s = f'<polygon points="{pts}" fill="{c}"/>'
    if label:
        s += T(cx, base_y + 14, label, 9.5, INK1, w=700, anchor="middle")
    if decision:
        s += T(cx, base_y + 27, decision, 9, INK2, anchor="middle")
    return s


def flag_line(x, y0, y1, label=None, c=INK1, dash="4,2"):
    """竖向标志虚线（Today 线 / 波次分界线通用）。label 画在线底端下方。"""
    s = L(x, y0, x, y1, c, 1.2, dash=dash)
    if label:
        s += T(x, y1 + 14, label, 9.5, c, w=700, anchor="middle")
    return s


def mini_table(x, y, w, cols, rows, align=None, hi_col=None, row_h=32, fs=12):
    """三线表小表（推算页/盘点页用）。cols=[表头]；rows=[[c1,c2,..],..]；
    align 每列 'l'/'r'（缺省：末列外全部 l）；hi_col 该列数据用 ACC。
    返回 (svg, 总高)。数字请调用方直接传字符串（本函数不做格式化）。"""
    n = len(cols)
    align = align or (["l"] * (n - 1) + ["r"])
    cw = w / n
    s = L(x, y, x + w, y, INK1, 1.5)                      # 顶线
    for i, cname in enumerate(cols):
        tx = x + i * cw + (6 if align[i] == "l" else cw - 6)
        s += T(tx, y + row_h * 0.68, cname, fs - 1, INK2, w=700,
               anchor=("start" if align[i] == "l" else "end"))
    s += L(x, y + row_h, x + w, y + row_h, INK3, 1)        # 头分隔线
    for r, row in enumerate(rows):
        ry = y + row_h * (r + 1)
        for i, val in enumerate(row):
            tx = x + i * cw + (6 if align[i] == "l" else cw - 6)
            col = ACC if (hi_col == i) else INK1
            fam = MONO if align[i] == "r" else SANS
            s += T(tx, ry + row_h * 0.68, val, fs, col, w=(700 if hi_col == i else None),
                   fam=fam, anchor=("start" if align[i] == "l" else "end"))
    bot = y + row_h * (len(rows) + 1)
    s += L(x, bot, x + w, bot, INK1, 1.5)                  # 底线
    return s, bot - y


def bridge_arrow(x, y, w, label, sub=None):
    """推算桥箭头：左表→右表之间的粗箭头 + 显式乘数标注（推算页的灵魂）。"""
    s = L(x, y, x + w - 14, y, INK1, 3)
    s += _arrhead(x, y, x + w, y, INK1, 12)
    s += T(x + w / 2, y - 12, label, 19, INK1, w=700, fam=MONO, anchor="middle")
    if sub:
        s += T(x + w / 2, y + 22, sub, 10.5, INK2, anchor="middle")
    return s


def footnote_band(x, y, w, notes=None, note=None, source=None, fs=9.5, lh=15):
    """方法论脚注带（编号脚注 + Note + Source 三件套，BCG 式）。
    返回 (svg, 总高)。放内容区底部、chrome 页脚之上；来源行给了 source 才画。"""
    s = L(x, y, x + w, y, LINE, 1)
    yy = y + lh
    for i, t in enumerate(notes or []):
        s += T(x, yy, f"{i+1}. {t}", fs, INK3)
        yy += lh
    if note:
        s += T(x, yy, f"注：{note}", fs, INK3)
        yy += lh
    if source:
        s += T(x, yy, f"来源：{source}", fs, INK3)
        yy += lh
    return s, yy - y


# ============================================================ S-02 高阶：组合矩阵

def portfolio_matrix(x, y, w, h, items, xlab=("低", "高"), ylab=("低", "高"),
                     axis_names=("维度X", "维度Y"), quads=None, migrations=None,
                     grid=2, size_label="规模", hi=None):
    """组合矩阵散点气泡版（S-02 高阶）。四象限/九宫格 + 气泡（面积∝size）+ 迁移箭头。
    items=[(name, xv, yv, size)]，xv/yv ∈ 0–100；quads=象限策略标签（len=grid²，
    行序自上而下、列序自左向右）；migrations=[(item_i, txv, tyv)] 当前→目标虚线箭头；
    grid=2 经典 2×2，grid=3 为 GE-McKinsey 九宫格变体。"""
    pad_l, pad_b, pad_t, pad_r = 30, 34, 14, 14
    px, pyt = x + pad_l, y + pad_t
    pw, ph = w - pad_l - pad_r, h - pad_t - pad_b
    vx = lambda v: px + pw * (v / 100.0)
    vy = lambda v: pyt + ph * (1 - v / 100.0)

    s = f'<rect x="{px}" y="{pyt}" width="{pw}" height="{ph}" fill="#FFFFFF" stroke="{INK3}" stroke-width="1"/>'
    for g in range(1, grid):                         # 象限分隔线
        gv = 100.0 * g / grid
        s += L(vx(gv), pyt, vx(gv), pyt + ph, INK4, 1, dash="5,4")
        s += L(px, vy(gv), px + pw, vy(gv), INK4, 1, dash="5,4")
    if quads:                                        # 象限策略标签（角位固定）
        qw, qh = pw / grid, ph / grid
        for r in range(grid):
            for c in range(grid):
                s += T(px + c * qw + 10, pyt + r * qh + 18, quads[r * grid + c],
                       10.5, INK4, w=700)
    # 轴与端点标签
    s += T(px - 4, pyt + ph + 18, xlab[0], 10, INK3)
    s += T(px + pw, pyt + ph + 18, xlab[1], 10, INK3, anchor="end")
    s += T(px - 8, pyt + ph + 4, ylab[0], 10, INK3, anchor="end")
    s += T(px - 8, pyt + 12, ylab[1], 10, INK3, anchor="end")
    s += T(px + pw / 2, pyt + ph + 18, axis_names[0], 10.5, INK2, w=700, anchor="middle")
    s += T(px - 18, pyt + ph / 2, axis_names[1], 10.5, INK2, w=700, anchor="end")

    smax = max(it[3] for it in items) or 1.0
    if migrations:                                   # 迁移箭头（先画，压在气泡下）
        for (idx, txv, tyv) in migrations:
            _, xv, yv, sz = items[idx]
            r0 = 10 + 24 * math.sqrt(items[idx][3] / smax)
            x0, y0, x1, y1 = vx(xv), vy(yv), vx(txv), vy(tyv)
            ang = math.atan2(y1 - y0, x1 - x0)
            s += leader(x0 + r0 * math.cos(ang), y0 + r0 * math.sin(ang),
                        x1, y1, c=INK2, sw=1.4, dash="5,3")
            s += f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="7" fill="none" stroke="{INK2}" stroke-width="1.4" stroke-dasharray="3,2"/>'
    for i, (name, xv, yv, sz) in enumerate(items):   # 气泡：面积 ∝ size
        r = 10 + 24 * math.sqrt(sz / smax)
        col = ACC if hi == i else (GRAY_A if i % 2 == 0 else GRAY_B)
        s += f'<circle cx="{vx(xv):.1f}" cy="{vy(yv):.1f}" r="{r:.1f}" fill="{col}" opacity="0.88"/>'
        if r >= 22:
            s += T(vx(xv), vy(yv) + 4, name, 11, "#FFFFFF", w=700, anchor="middle")
        else:
            s += T(vx(xv) + r + 5, vy(yv) + 4, name, 11, INK1, w=700)
    s += T(px + pw, pyt - 3, f"气泡面积 ∝ {size_label}", 9.5, INK4, anchor="end")
    return s


# ============================================================ A-03 高阶：标准 RACI

def raci_matrix(x, y, w, h, tasks, roles, cells, legend=True):
    """标准 RACI 矩阵（A-03 高阶）：行=任务/交付物，列=角色，格=R/A/C/I。
    强制校验「每行恰好一个 A」（PMBOK/Cornell IT 规范），违反抛 ValueError。
    字母即语义通道；灰阶权重 A>R>C>I 为第二通道。"""
    for r, row in enumerate(cells):
        if len(row) != len(roles):
            raise ValueError(f"RACI 第 {r+1} 行列数 {len(row)} ≠ 角色数 {len(roles)}")
        bad = [v for v in row if v not in ("R", "A", "C", "I", "")]
        if bad:
            raise ValueError(f"RACI 第 {r+1} 行含非法标记 {bad}（仅允许 R/A/C/I/空）")
        if row.count("A") != 1:
            raise ValueError(f"RACI 第 {r+1} 行「{tasks[r]}」有 {row.count('A')} 个 A——"
                             f"每行必须恰好一个 Accountable")
    label_w, header_h = 230, 40
    leg_h = 30 if legend else 0
    cell_fn, _ = grid_cells(x, y, w, h - leg_h, len(tasks), len(roles), label_w, header_h)
    s = ""
    for c, role in enumerate(roles):                 # 表头
        cx0, _, cw, _ = cell_fn(0, c)
        s += T(cx0 + cw / 2, y + header_h * 0.64, role, 12, INK1, w=700, anchor="middle")
    s += L(x, y + header_h, x + w, y + header_h, INK1, 1.5)
    for r, task in enumerate(tasks):                 # 行标签 + 斑马底
        _, cy0, _, ch = cell_fn(r, 0)
        if r % 2 == 1:
            s += f'<rect x="{x}" y="{cy0}" width="{w}" height="{ch}" fill="{PANEL}"/>'
        s += T(x + 8, cy0 + ch / 2 + 4.5, task, 12, INK1)
        s += L(x, cy0 + ch, x + w, cy0 + ch, LINE, 1)
    for r in range(len(tasks)):                      # 芯片
        for c in range(len(roles)):
            v = cells[r][c]
            if not v:
                continue
            cx0, cy0, cw, ch = cell_fn(r, c)
            ccx, ccy, cr = cx0 + cw / 2, cy0 + ch / 2, min(ch * 0.36, 15)
            if v == "A":
                s += f'<circle cx="{ccx:.1f}" cy="{ccy:.1f}" r="{cr}" fill="{INK1}"/>'
                s += T(ccx, ccy + 4.5, "A", 13, "#FFFFFF", w=700, fam=MONO, anchor="middle")
            elif v == "R":
                s += f'<circle cx="{ccx:.1f}" cy="{ccy:.1f}" r="{cr}" fill="{GRAY_A}"/>'
                s += T(ccx, ccy + 4.5, "R", 13, "#FFFFFF", w=700, fam=MONO, anchor="middle")
            elif v == "C":
                s += f'<circle cx="{ccx:.1f}" cy="{ccy:.1f}" r="{cr}" fill="#FFFFFF" stroke="{INK2}" stroke-width="1.6"/>'
                s += T(ccx, ccy + 4.5, "C", 12.5, INK2, w=700, fam=MONO, anchor="middle")
            else:
                s += f'<circle cx="{ccx:.1f}" cy="{ccy:.1f}" r="{cr}" fill="#FFFFFF" stroke="{INK4}" stroke-width="1.4" stroke-dasharray="3,2"/>'
                s += T(ccx, ccy + 4.5, "I", 12.5, INK3, w=700, fam=MONO, anchor="middle")
    if legend:
        ly = y + h - leg_h + 18
        lx = x + 4
        for mark, txt in (("A", "最终负责·每行唯一"), ("R", "负责执行"),
                          ("C", "需咨询"), ("I", "需知会")):
            s += T(lx, ly, mark, 11, INK1, w=700, fam=MONO)
            s += T(lx + 14, ly, txt, 10.5, INK2)
            lx += 14 + len(txt) * 11.5 + 26
    return s


# ============================================================ G-01 高阶：issue tree

def issue_tree(x, y, w, h, root, branches, hyp_tag="假设"):
    """正式 issue tree（G-01 替换）：左根右叶两级，分层严格对齐，
    父节点纵向居中于子组，分支组间以虚线分隔（MECE 视觉分组），
    末端可标「假设/待验证」。branches=[(分支名, [叶 或 (叶, is_hyp)])]，
    分支 3–5 个、每支叶 ≤4（超出请拆页）。"""
    n_b = len(branches)
    leaves = [[(lf, False) if isinstance(lf, str) else lf for lf in b[1]] for b in branches]
    n_leaf = sum(len(g) for g in leaves)
    grp_gap = 20
    leaf_gap = 8
    leaf_h = min(46, (h - grp_gap * (n_b - 1) - leaf_gap * (n_leaf - n_b)) / n_leaf)
    rw, bw_, lw = 170, 210, w - 170 - 210 - 2 * 56   # 根/支/叶列宽，肘线区各 56
    bx0, lx0 = x + rw + 56, x + rw + 56 + bw_ + 56

    s = ""
    yy = y
    b_centers = []
    for gi, grp in enumerate(leaves):
        g_top = yy
        for (lf, hyp) in grp:
            if hyp:
                s += f'<rect x="{lx0}" y="{yy:.1f}" width="{lw}" height="{leaf_h:.1f}" rx="5" fill="#FFFFFF" stroke="{INK3}" stroke-width="1.3" stroke-dasharray="5,3"/>'
                s += T(lx0 + lw - 8, yy + 13, hyp_tag, 9, INK2, w=700, anchor="end")
            else:
                s += f'<rect x="{lx0}" y="{yy:.1f}" width="{lw}" height="{leaf_h:.1f}" rx="5" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.3"/>'
            s += T(lx0 + 12, yy + leaf_h / 2 + 4.5, lf, 12, INK2)
            s += L(bx0 + bw_, yy + leaf_h / 2, lx0, yy + leaf_h / 2, INK4, 1.2)
            yy += leaf_h + leaf_gap
        g_bot = yy - leaf_gap
        bc = (g_top + g_bot) / 2
        b_centers.append(bc)
        bh = min(52, g_bot - g_top)
        s += f'<rect x="{bx0}" y="{bc-bh/2:.1f}" width="{bw_}" height="{bh:.1f}" rx="6" fill="#FFFFFF" stroke="{INK1}" stroke-width="1.6"/>'
        s += T(bx0 + bw_ / 2, bc + 4.5, branches[gi][0], 13, INK1, w=700, anchor="middle")
        if gi < n_b - 1:                              # MECE 组间分隔
            sep = yy - leaf_gap / 2 + grp_gap / 2
            s += L(bx0 - 20, sep, x + w, sep, INK4, 1, dash="2,4")
        yy += grp_gap - leaf_gap
    rc = (b_centers[0] + b_centers[-1]) / 2           # 根居中于分支带
    rh = 66
    s += f'<rect x="{x}" y="{rc-rh/2:.1f}" width="{rw}" height="{rh}" rx="6" fill="{INK1}"/>'
    s += T(x + rw / 2, rc + 5, root, 14, "#FFFFFF", w=700, anchor="middle")
    xm = x + rw + 28
    for bc in b_centers:                              # 根→支肘线（横-竖-横）
        s += L(x + rw, rc, xm, rc, INK1, 1.5)
        s += L(xm, rc, xm, bc, INK1, 1.5)
        s += L(xm, bc, bx0, bc, INK1, 1.5)
    return s


# ============================================================ E-04 高阶：分层架构

def arch_layers(x, y, w, h, layers, pillars=None, iface_labels=None, hi_layer=None):
    """完整分层架构（E-04 高阶）：水平分层（层高∝weight）+ 层内模块网格
    + 跨层纵向能力条（cross-cutting）+ 层间接口标记。
    layers 自上而下 [(层名, [模块...], weight)]；pillars=[能力条名(≤4字)]。"""
    label_w = 118
    pil_w, pil_gap = 54, 10
    pz = (pil_w + pil_gap) * len(pillars) if pillars else 0
    bw = w - label_w - pz
    gap = 12
    tw = sum((ly[2] if len(ly) > 2 else 1) for ly in layers)
    avail = h - gap * (len(layers) - 1)
    s = ""
    yy = y
    bands = []
    for i, ly in enumerate(layers):
        name, mods = ly[0], ly[1]
        wt = ly[2] if len(ly) > 2 else 1
        bh = avail * wt / tw
        bands.append((yy, bh))
        hl = (i == hi_layer)
        s += f'<rect x="{x+label_w}" y="{yy:.1f}" width="{bw}" height="{bh:.1f}" rx="6" fill="{PANEL}" stroke="{ACC if hl else LINE}" stroke-width="{1.8 if hl else 1.2}"/>'
        s += T(x + label_w - 12, yy + bh / 2 + 5, name, 13.5, INK1, w=700, anchor="end")
        if mods:                                      # 层内模块网格（等宽，最多两行）
            per_row = min(len(mods), max(3, math.ceil(len(mods) / 2)))
            rows = math.ceil(len(mods) / per_row)
            mh = min(40, (bh - 10 * (rows + 1)) / rows)
            mw = (bw - 12 * (per_row + 1)) / per_row
            for mi, m in enumerate(mods):
                r_, c_ = divmod(mi, per_row)
                mx = x + label_w + 12 + c_ * (mw + 12)
                my = yy + (bh - rows * mh - (rows - 1) * 10) / 2 + r_ * (mh + 10)
                s += f'<rect x="{mx:.1f}" y="{my:.1f}" width="{mw:.1f}" height="{mh:.1f}" rx="5" fill="#FFFFFF" stroke="{INK4}" stroke-width="1.1"/>'
                s += T(mx + mw / 2, my + mh / 2 + 4.5, m, 12, INK1, anchor="middle")
        if i < len(layers) - 1:                       # 层间接口标记（上下双三角）
            iy = yy + bh + gap / 2
            icx = x + label_w + bw / 2
            s += f'<polygon points="{icx-5},{iy-2} {icx+5},{iy-2} {icx},{iy-8}" fill="{INK3}"/>'
            s += f'<polygon points="{icx-5},{iy+2} {icx+5},{iy+2} {icx},{iy+8}" fill="{INK3}"/>'
            if iface_labels and i < len(iface_labels) and iface_labels[i]:
                s += T(icx + 12, iy + 4, iface_labels[i], 9.5, INK3)
        yy += bh + gap
    if pillars:                                       # 纵向能力条：单字堆叠，非 rotate
        top, bot = bands[0][0], bands[-1][0] + bands[-1][1]
        for pi, pname in enumerate(pillars):
            px0 = x + label_w + bw + pil_gap + pi * (pil_w + pil_gap)
            s += f'<rect x="{px0:.1f}" y="{top:.1f}" width="{pil_w}" height="{bot-top:.1f}" rx="6" fill="#FFFFFF" stroke="{INK1}" stroke-width="1.5"/>'
            chars = list(str(pname))
            ch_gap = 22
            cy0 = (top + bot) / 2 - (len(chars) - 1) * ch_gap / 2
            for ci, ch in enumerate(chars):
                s += T(px0 + pil_w / 2, cy0 + ci * ch_gap + 5, ch, 13, INK1, w=700, anchor="middle")
    return s


# ============================================================ A-90 泳道路线图

def swimlane_roadmap(x, y, w, h, lanes, total_units, today=None, milestones=None,
                     deps=None, unit_label="月", legend=True,
                     mode="gantt", bucket_names=None):
    """阶段×泳道路线图（A-90）：时间刻度头 + 3–6 泳道 + 状态色块 +
    里程碑菱形（轴头，跨泳道可见）+ Today 线 + 可选跨泳道依赖（≤2 条）。
    lanes=[(泳道名, [(块名, start, dur, status)])]，status ∈ committed/planned/proposed。
    时长按调研纪律取近似值（如半月粒度），不假装精确。
    v2.8 三渲染模式（调研建议 mode="gantt"|"chevron"|"phase_bucket"）：
    - gantt（默认）：精确时间轴 + 矩形块，行为与 v2.7 完全一致；
    - chevron：块画雪佛龙箭头形，强调相位推进而非精确日期（复用 chevron 形语言）；
    - phase_bucket：BCG 达拉斯式相位分桶——日期不确定时用桶名列
      （默认五桶：立即行动/速赢/战略优先/中期举措/长期机会）代替时间轴，
      start/dur 为桶索引与跨桶数；比假装精确更诚实，故禁 today/milestones。"""
    if mode not in ("gantt", "chevron", "phase_bucket"):
        raise ValueError("mode 仅支持 gantt / chevron / phase_bucket")
    if mode == "phase_bucket":
        if today is not None or milestones:
            raise ValueError("phase_bucket 无精确时间轴，不支持 today/milestones")
        bucket_names = bucket_names or ["立即行动", "速赢", "战略优先", "中期举措", "长期机会"]
        total_units = len(bucket_names)
    label_w, head_h = 128, 34
    leg_h = 26 if legend else 0
    px, pyt = x + label_w, y + head_h
    pw, ph = w - label_w, h - head_h - leg_h
    ux = lambda u: px + (u / total_units) * pw
    n = len(lanes)
    lane_h = ph / n
    s = ""
    if mode == "phase_bucket":                        # 桶名列头 + 列分隔
        bw_ = pw / total_units
        for k, bn in enumerate(bucket_names):
            s += T(px + (k + 0.5) * bw_, y + 14, bn, 11, INK1, w=700, anchor="middle")
            s += L(px + k * bw_, pyt, px + k * bw_, pyt + ph, LINE, 0.8)
        s += L(px + pw, pyt, px + pw, pyt + ph, LINE, 0.8)
    else:
        grid = max(1, round(total_units / 6))
        u = 0
        while u <= total_units + 1e-9:                # 刻度头
            s += L(ux(u), pyt, ux(u), pyt + ph, LINE, 0.8, dash="2,3")
            s += T(ux(u), y + 12, f"{int(u)}{unit_label}", 9.5, INK3, fam=MONO, anchor="middle")
            u += grid
    for (mu, ml) in (milestones or []):               # 里程碑：轴头菱形+右侧标签
        s += milestone(ux(mu), y + head_h - 10, None, r=6)
        s += T(ux(mu) + 10, y + head_h - 6, ml, 9.5, INK1, w=700)
    style = {"committed": (GRAY_A, None, "#FFFFFF"),
             "planned":   (GRAY_B, None, INK1),
             "proposed":  ("#FFFFFF", INK3, INK1)}
    for i, (lname, bars) in enumerate(lanes):
        ly = pyt + i * lane_h
        if i % 2 == 1:
            s += f'<rect x="{x}" y="{ly:.1f}" width="{w}" height="{lane_h:.1f}" fill="{PANEL}" opacity="0.6"/>'
        s += T(x + 6, ly + lane_h / 2 + 4.5, lname, 12.5, INK1, w=700)
        bh = min(lane_h * 0.5, 26)
        for (bl, st, du, status) in bars:
            fill, stroke, tc = style.get(status, style["planned"])
            bx, bwd = ux(st), (du / total_units) * pw
            extra = f' stroke="{stroke}" stroke-width="1.4" stroke-dasharray="5,3"' if stroke else ""
            y0, y1_ = ly + lane_h / 2 - bh / 2, ly + lane_h / 2 + bh / 2
            if mode == "chevron":                     # 雪佛龙块：右端箭头，非首块左端凹口
                aa = min(12, bwd * 0.25); ym = (y0 + y1_) / 2
                pts = [(bx, y0), (bx + bwd - aa, y0), (bx + bwd, ym), (bx + bwd - aa, y1_), (bx, y1_)]
                if st > 1e-9: pts.append((bx + aa, ym))
                pstr = " ".join(f"{a_:.1f},{b_:.1f}" for a_, b_ in pts)
                s += f'<polygon points="{pstr}" fill="{fill}"{extra}/>'
            elif mode == "phase_bucket":              # 桶内块：内缩避让列线
                s += f'<rect x="{bx+4:.1f}" y="{y0:.1f}" width="{bwd-8:.1f}" height="{bh:.1f}" rx="3" fill="{fill}"{extra}/>'
            else:
                s += f'<rect x="{bx:.1f}" y="{y0:.1f}" width="{bwd:.1f}" height="{bh:.1f}" rx="4" fill="{fill}"{extra}/>'
            if len(str(bl)) * 12 < bwd - 10:
                s += T(bx + bwd / 2, ly + lane_h / 2 + 4, bl, 11, tc, w=700, anchor="middle")
            else:
                s += T(bx + bwd + 6, ly + lane_h / 2 + 4, bl, 10.5, INK2)
        s += L(x, ly + lane_h, x + w, ly + lane_h, LINE, 1)
    for (li, uu, lj, uv) in (deps or []):             # 跨泳道依赖（少用，≤2 条）
        yA = pyt + li * lane_h + lane_h / 2 + 14
        yB = pyt + lj * lane_h + lane_h / 2
        x0, x1 = ux(uu), ux(uv)
        s += L(x0, yA, x0, yB, INK2, 1.2, dash="3,3")
        if abs(x1 - x0) > 4:
            s += L(x0, yB, x1 - 8, yB, INK2, 1.2, dash="3,3")
            s += _arrhead(x0, yB, x1, yB, INK2, 7)
        else:
            s += _arrhead(x0, yB - 10, x0, yB, INK2, 7)
    if today is not None:
        s += flag_line(ux(today), y + head_h - 6, pyt + ph, "今日")
    if legend:
        lx, lyg = x + label_w, y + h - 8
        for status, nm in (("committed", "已承诺"), ("planned", "计划中"), ("proposed", "拟议")):
            fill, stroke, _ = style[status]
            extra = f' stroke="{stroke}" stroke-width="1.2" stroke-dasharray="4,3"' if stroke else ""
            s += f'<rect x="{lx}" y="{lyg-10}" width="18" height="10" rx="2" fill="{fill}"{extra}/>'
            s += T(lx + 24, lyg, nm, 10, INK2)
            lx += 24 + len(nm) * 11 + 24
    return s


# ============================================================ G-92 服务蓝图

def service_blueprint(x, y, w, h, steps, rows, arrows=None):
    """服务蓝图（G-92 · Shostack 1984 / Zeithaml–Bitner / NN/g 规范）：
    固定 5 泳道（物理证据/客户行为/前台行为/后台行为/支持流程）+
    3 条分界线（互动线/可见性线/内部互动线）。rows = 5 个列表，与 steps 列对齐，
    每格一个动词短语（或 None 留空）。arrows=[(row_i,col, row_j,col)] 依赖箭头（少用）。"""
    LANES = [("物理证据", "Physical Evidence"), ("客户行为", "Customer Actions"),
             ("前台行为", "Frontstage"), ("后台行为", "Backstage"),
             ("支持流程", "Support Processes")]
    # 分界线画在第 k 条泳道顶部：客户|前台=互动线，前台|后台=可见性线，后台|支持=内部互动线
    BOUNDS = {2: "互动线", 3: "可见性线", 4: "内部互动线"}
    if len(rows) != 5:
        raise ValueError(f"服务蓝图固定 5 泳道，收到 {len(rows)} 行")
    for ri, row in enumerate(rows):
        if not isinstance(row, (list, tuple)) or any(c is not None and not isinstance(c, str) for c in row):
            raise ValueError(f"服务蓝图第 {ri+1} 泳道须为字符串/None 列表（泳道名由函数内置，勿传 (名, 列表) 元组）")
    label_w, head_h = 148, 32
    px, pyt = x + label_w, y + head_h
    pw, ph = w - label_w, h - head_h
    ncol = len(steps)
    cw, lh = pw / ncol, ph / 5

    def cpos(r, c):
        return px + c * cw, pyt + r * lh

    s = ""
    for c, st in enumerate(steps):                     # 旅程步骤表头
        s += T(px + c * cw + cw / 2, y + head_h * 0.62, st, 11.5, INK1, w=700, anchor="middle")
    s += L(x, pyt, x + w, pyt, INK1, 1.5)
    for r, (cn, en) in enumerate(LANES):
        ly = pyt + r * lh
        if r % 2 == 1:
            s += f'<rect x="{x}" y="{ly:.1f}" width="{w}" height="{lh:.1f}" fill="{PANEL}" opacity="0.55"/>'
        s += T(x + 6, ly + lh / 2 - 3, cn, 12, INK1, w=700)
        s += T(x + 6, ly + lh / 2 + 12, en, 8.5, INK3)
        for c in range(ncol):
            val = rows[r][c] if c < len(rows[r]) else None
            if not val:
                continue
            cx0, cy0 = cpos(r, c)
            mw, mh = cw - 14, min(lh - 14, 44)
            s += f'<rect x="{cx0+7:.1f}" y="{cy0+(lh-mh)/2:.1f}" width="{mw:.1f}" height="{mh:.1f}" rx="5" fill="#FFFFFF" stroke="{INK4}" stroke-width="1.1"/>'
            s += T(cx0 + cw / 2, cy0 + lh / 2 + 4, val, 10.5, INK1, anchor="middle")
        if r in BOUNDS:                                # 分界线（虚线 + 右端标签）
            by = pyt + r * lh
            s += L(x, by, x + w, by, INK2, 1.4, dash="7,4")
            s += T(x + w - 4, by - 5, BOUNDS[r], 9.5, INK2, w=700, anchor="end")
        elif r > 0:
            s += L(px, pyt + r * lh, x + w, pyt + r * lh, LINE, 1)
    for (ri, ci, rj, cj) in (arrows or []):            # 依赖箭头（跨线即 moment of truth）
        x0 = px + ci * cw + cw / 2
        x1 = px + cj * cw + cw / 2
        y0 = pyt + ri * lh + lh / 2 + 22
        y1 = pyt + rj * lh + lh / 2 - 26
        s += L(x0, y0, x0, (y0 + y1) / 2, INK3, 1.2) + L(x0, (y0 + y1) / 2, x1, (y0 + y1) / 2, INK3, 1.2)
        s += L(x1, (y0 + y1) / 2, x1, y1 - 2, INK3, 1.2) + _arrhead(x1, y1 - 10, x1, y1, INK3, 7)
    return s


# ============================================================ G-93 剖面金字塔

def layered_pyramid(x, y, w, h, layers, takeaways=None, hi_layer=None):
    """剖面金字塔（G-93 · Bain Elements of Value / Keller CBBE 形态）：
    梯形分层 + 层内切格；可选右侧逐层 takeaway（引线 + 短句，Minto 式）。
    layers 自上而下 [(层名, [格...])]；与 G-03 纯层级金字塔、charts.funnel
    定量漏斗划界：本版式=定性层级 × 层内多要素。"""
    n = len(layers)
    ta_w = 300 if takeaways else 0
    cx0 = x + (w - ta_w) / 2                          # 金字塔中轴
    top_w, bot_w = (w - ta_w) * 0.34, (w - ta_w) * 0.92
    gap = 8
    lh = (h - gap * (n - 1)) / n
    s = ""
    for i, (name, cells_) in enumerate(layers):
        wt = top_w + (bot_w - top_w) * (i / n)         # 本层顶宽
        wb = top_w + (bot_w - top_w) * ((i + 1) / n)   # 本层底宽
        yt, yb = y + i * (lh + gap), y + i * (lh + gap) + lh
        hl = (i == hi_layer)
        pts = f"{cx0-wt/2:.1f},{yt:.1f} {cx0+wt/2:.1f},{yt:.1f} {cx0+wb/2:.1f},{yb:.1f} {cx0-wb/2:.1f},{yb:.1f}"
        s += f'<polygon points="{pts}" fill="{PANEL if i%2 else "#FFFFFF"}" stroke="{ACC if hl else INK4}" stroke-width="{1.8 if hl else 1.2}"/>'
        s += T(cx0 - wt / 2 + 10, yt + 16, name, 11, INK2, w=700)
        if cells_:                                     # 层内切格（限宽于顶边内侧）
            iw = wt - 36
            m = len(cells_)
            mw = (iw - 8 * (m - 1)) / m
            mh = min(30, lh - 30)
            for mi, cell in enumerate(cells_):
                mx = cx0 - iw / 2 + mi * (mw + 8)
                my = yt + (lh - mh) / 2 + 6
                s += f'<rect x="{mx:.1f}" y="{my:.1f}" width="{mw:.1f}" height="{mh}" rx="4" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.1"/>'
                s += T(mx + mw / 2, my + mh / 2 + 4, cell, 10.5, INK1, anchor="middle")
        if takeaways and i < len(takeaways) and takeaways[i]:
            tx = x + w - ta_w + 34
            ty = yt + lh / 2
            s += leader(cx0 + (wt + wb) / 4 + 6, ty, tx - 8, ty, c=INK3, sw=1.2)
            s += T(tx, ty + 4, takeaways[i], 11.5, INK1, w=700)
    return s


# ============================================================ G-91 论证阶梯

def argument_ladder(x, y, w, h, steps, conclusion, layout="horizontal"):
    """论证阶梯（G-91 · Minto 金字塔原理单页化）：2–4 个 MECE 论点
    逐级累加、收敛到结论框。steps=[(论点, 论据一句)]。
    layout='horizontal' 左→右 buildup（默认，贴合阅读动线）/'vertical' 纵向阶梯。"""
    n = len(steps)
    s = ""
    if layout == "horizontal":
        cw_ = 176
        con_w = w - 0.62 * w - 30                      # 结论框区
        area_w = w - con_w - 40
        sw_ = min(cw_, (area_w - 24 * (n - 1)) / n)
        rise = min(46, (h - 120) / max(n - 1, 1))
        base = y + h - 116
        for i, (tt, ev) in enumerate(steps):
            sx = x + i * (sw_ + 24)
            sy = base - i * rise
            s += f'<rect x="{sx:.1f}" y="{sy:.1f}" width="{sw_:.1f}" height="96" rx="6" fill="#FFFFFF" stroke="{INK1}" stroke-width="1.5"/>'
            s += f'<circle cx="{sx+18:.1f}" cy="{sy+20:.1f}" r="10" fill="{INK1}"/>'
            s += T(sx + 18, sy + 24.5, str(i + 1), 11, "#FFFFFF", w=700, fam=MONO, anchor="middle")
            s += T(sx + 34, sy + 25, tt, 13, INK1, w=700)
            s += T(sx + 12, sy + 50, ev, 10.5, INK2)
            s += L(sx, sy + 96, sx + sw_, sy + 96, INK1, 3)   # 台阶踏面
            if i < n - 1:
                ax = sx + sw_ + 2
                s += leader(ax, sy + 48, ax + 20, sy - rise + 48, c=GRAY_A, sw=1.8)
        ccx = x + w - con_w
        ccy = base - (n - 1) * rise - 10
        chh = 118
        s += leader(x + (n - 1) * (sw_ + 24) + sw_ + 4, ccy + chh / 2 - 4,
                    ccx - 8, ccy + chh / 2 - 4, c=INK1, sw=2.2)
        s += f'<rect x="{ccx:.1f}" y="{ccy:.1f}" width="{con_w:.1f}" height="{chh}" rx="8" fill="{INK1}"/>'
        s += T(ccx + 18, ccy + 30, "结论", 10.5, "#C8C8C8", w=700, ls=2)
        s += T(ccx + 18, ccy + 62, conclusion, 15, "#FFFFFF", w=700)
        s += T(x, y + h - 4, "因为 " + " · ".join(f"{i+1}" for i in range(n)) + "，所以结论（分支间 MECE）", 9.5, INK4)
    else:
        sh = min(78, (h - 96) / n)
        lad_w = w * 0.44
        for i, (tt, ev) in enumerate(steps):
            sy = y + i * (sh + 10)
            s += f'<rect x="{x}" y="{sy:.1f}" width="{lad_w:.1f}" height="{sh:.1f}" rx="6" fill="#FFFFFF" stroke="{INK1}" stroke-width="1.5"/>'
            s += f'<circle cx="{x+20:.1f}" cy="{sy+sh/2:.1f}" r="10" fill="{INK1}"/>'
            s += T(x + 20, sy + sh / 2 + 4.5, str(i + 1), 11, "#FFFFFF", w=700, fam=MONO, anchor="middle")
            s += T(x + 38, sy + sh / 2 - 4, tt, 13, INK1, w=700)
            s += T(x + 38, sy + sh / 2 + 15, ev, 10.5, INK2)
            s += leader(x + lad_w + 4, sy + sh / 2, x + lad_w + 54,
                        y + h / 2 - 12 + (0 if n < 2 else (i - (n - 1) / 2) * 8),
                        c=GRAY_A, sw=1.6)
        ccx = x + lad_w + 64
        s += f'<rect x="{ccx:.1f}" y="{y+h/2-72:.1f}" width="{w-lad_w-64:.1f}" height="120" rx="8" fill="{INK1}"/>'
        s += T(ccx + 18, y + h / 2 - 42, "结论", 10.5, "#C8C8C8", w=700, ls=2)
        s += T(ccx + 18, y + h / 2 - 10, conclusion, 15, "#FFFFFF", w=700)
    return s


# ============================================================ 降级：同心弧（定性）

def concentric_arcs(x, y, w, h, rings):
    """半圆同心弧（降级工具·仅定性层级叙事）。数据可视化学界批评径向布局
    面积随半径平方夸大外圈——本函数**不接受数值**，只接受 ≤5 个定性标签，
    等距弧 + 水平引线到右侧标签列，并强制绘制「弧径不代表数值」提示。
    定量规模序列请改用 charts.hbar 或 charts.marimekko（V-94）。"""
    if len(rings) > 5:
        raise ValueError("同心弧限 ≤5 层（超出不可读）；定量场景请用 hbar/marimekko")
    ccx, ccy = x + w * 0.36, y + h - 26
    r_max = min(h - 60, w * 0.34)
    r_step = r_max / len(rings)
    s = ""
    for i, lab in enumerate(rings):
        r = r_step * (i + 1) - r_step * 0.25
        col = INK1 if i == 0 else (GRAY_A if i % 2 == 1 else GRAY_B)
        s += (f'<path d="M {ccx-r:.1f} {ccy:.1f} A {r:.1f} {r:.1f} 0 0 1 {ccx+r:.1f} {ccy:.1f}" '
              f'fill="none" stroke="{col}" stroke-width="{max(10, r_step*0.42):.1f}"/>')
        ang = math.radians(38)                         # 右上方引出
        exx, exy = ccx + r * math.cos(ang), ccy - r * math.sin(ang)
        ly_ = y + 18 + (len(rings) - 1 - i) * 26       # 外环对顶行，引线互不交叉
        s += L(exx, exy, x + w * 0.72, ly_, INK4, 1) + L(x + w * 0.72, ly_, x + w * 0.78, ly_, INK4, 1)
        s += T(x + w * 0.78 + 6, ly_ + 4, lab, 12, INK1, w=700)
    s += L(ccx - r_max - 6, ccy, ccx + r_max + 6, ccy, INK3, 1)
    s += T(x + w - 4, y + h - 4, "定性层级示意 · 弧径不代表数值", 9.5, INK4, anchor="end")
    return s


# ============================================================ v4.0 新增（调研落地批）
def harvey_table(x, y, w, h, dims, items, legend=True):
    """S-16 Harvey Balls 评估表：行=评估对象，列=维度，格=0–4 五档填充圆。
    dims=[维度名] 2–6 列；items=[(对象名, [评分 0–4 ×len(dims)])] 2–8 行。
    来源：Harvey L. Poppel @ Booz Allen Hamilton, 1970s（调研報告候选1）。
    与 S-13 勾选盘点分工：二值完成态→S-13；程度梯度→本表。"""
    if not 2 <= len(dims) <= 6:
        raise ValueError("S-16 维度列限 2–6，收到 %d" % len(dims))
    if not 2 <= len(items) <= 8:
        raise ValueError("S-16 评估行限 2–8，收到 %d" % len(items))
    for nm, scores in items:
        if len(scores) != len(dims):
            raise ValueError(f"S-16 「{nm}」评分数 {len(scores)} ≠ 维度数 {len(dims)}")
        if any(not 0 <= s <= 4 for s in scores):
            raise ValueError(f"S-16 「{nm}」评分须 0–4 五档")
    name_w = 220
    col_w = (w - name_w) / len(dims)
    row_h = min(56, (h - 40 - (30 if legend else 0)) / len(items))
    s = f'<rect x="{x}" y="{y}" width="{w:.0f}" height="40" fill="{INK1}"/>'
    s += T(x + 16, y + 26, "评估对象", 12, "#FFFFFF", 700)
    for j, d in enumerate(dims):
        s += T(x + name_w + (j + 0.5) * col_w, y + 26, d, 12, "#FFFFFF", 700, anchor="middle")
    r = min(13, row_h * 0.32)
    for i, (nm, scores) in enumerate(items):
        ry = y + 40 + i * row_h
        if i % 2:
            s += f'<rect x="{x}" y="{ry:.1f}" width="{w:.0f}" height="{row_h:.1f}" fill="{PANEL}"/>'
        s += T(x + 16, ry + row_h / 2 + 5, nm, 13, INK1, 700)
        for j, sc in enumerate(scores):
            cx, cy = x + name_w + (j + 0.5) * col_w, ry + row_h / 2
            s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{INK1}" stroke-width="1.5"/>'
            if sc == 4:
                s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r-2:.1f}" fill="{INK1}"/>'
            elif sc > 0:  # 扇形：12 点起顺时针 sc/4 圆
                a = sc / 4 * 2 * math.pi
                x1, y1 = cx, cy - (r - 2)
                x2, y2 = cx + (r - 2) * math.sin(a), cy - (r - 2) * math.cos(a)
                s += (f'<path d="M {cx:.1f} {cy:.1f} L {x1:.1f} {y1:.1f} '
                      f'A {r-2:.1f} {r-2:.1f} 0 {1 if sc > 2 else 0} 1 {x2:.1f} {y2:.1f} Z" fill="{INK1}"/>')
        s += L(x, ry + row_h, x + w, ry + row_h, LINE, 0.5)
    if legend:
        ly = y + 40 + len(items) * row_h + 20
        s += T(x, ly + 4, "图例", 11, INK2, 700)
        for k in range(5):
            cx = x + 70 + k * 96
            s += f'<circle cx="{cx}" cy="{ly:.1f}" r="9" fill="none" stroke="{INK1}" stroke-width="1.2"/>'
            if k == 4:
                s += f'<circle cx="{cx}" cy="{ly:.1f}" r="7" fill="{INK1}"/>'
            elif k > 0:
                a = k / 4 * 2 * math.pi
                s += (f'<path d="M {cx} {ly:.1f} L {cx} {ly-7:.1f} A 7 7 0 {1 if k > 2 else 0} 1 '
                      f'{cx + 7*math.sin(a):.1f} {ly - 7*math.cos(a):.1f} Z" fill="{INK1}"/>')
            s += T(cx + 16, ly + 4, ["无", "弱", "中", "较强", "全面"][k], 11, INK2)
    return s


def value_chain(x, y, w, h, primary, support, margin_label="利润"):
    """E-05 Porter 价值链：顶部支持活动横条 + 底部主活动雪佛龙带 + 右端利润尖角。
    primary=[(名, 注 或 None)] 3–6 段主活动；support=[名] 2–4 条支持活动。
    来源：Michael E. Porter, *Competitive Advantage*, Free Press, 1985（调研报告候选5）。"""
    if not 3 <= len(primary) <= 6:
        raise ValueError("E-05 主活动限 3–6 段（Porter 原型 5 段），收到 %d" % len(primary))
    if not 2 <= len(support) <= 4:
        raise ValueError("E-05 支持活动限 2–4 条（Porter 原型 4 条），收到 %d" % len(support))
    tip_w = min(150, w * 0.14)                       # 利润尖角水平深度
    sup_h = (h * 0.42) / len(support)
    body_w = w - tip_w
    s = ""
    for i, nm in enumerate(support):                 # 支持活动横条
        sy = y + i * sup_h
        s += (f'<rect x="{x}" y="{sy:.1f}" width="{body_w:.1f}" height="{sup_h-4:.1f}" '
              f'fill="{PANEL}" stroke="{INK3}" stroke-width="1"/>')
        s += T(x + 16, sy + sup_h / 2 + 3, nm, 13, INK2, 700)
    py = y + h * 0.42 + 12
    ph = h - (py - y)
    seg_w = body_w / len(primary)
    aa = 16
    for i, (nm, note) in enumerate(primary):         # 主活动雪佛龙带
        px = x + i * seg_w
        pts = [(px, py), (px + seg_w - aa, py), (px + seg_w, py + ph / 2),
               (px + seg_w - aa, py + ph), (px, py + ph)]
        if i > 0:
            pts.append((px + aa, py + ph / 2))
        pstr = " ".join(f"{a_:.1f},{b_:.1f}" for a_, b_ in pts)
        s += f'<polygon points="{pstr}" fill="{INK1 if i == len(primary)-1 else PANEL}" stroke="{INK3}" stroke-width="1"/>'
        dark = i == len(primary) - 1
        s += T(px + seg_w / 2, py + ph / 2 - 4, nm, 13, "#FFFFFF" if dark else INK1, 700, anchor="middle")
        if note:
            s += T(px + seg_w / 2, py + ph / 2 + 18, note, 10.5, "#C4C4C4" if dark else INK2, anchor="middle")
    mx = x + body_w                                   # 利润尖角（贯通全高）
    s += (f'<polygon points="{mx:.1f},{y} {mx+tip_w:.1f},{y+h/2:.1f} {mx:.1f},{y+h}" '
          f'fill="none" stroke="{INK1}" stroke-width="1.5"/>')
    s += T(mx + tip_w * 0.42, y + h / 2 + 5, margin_label, 13, INK1, 700, anchor="middle")
    return s


def fishbone(x, y, w, h, effect, bones):
    """G-04 鱼骨图（Ishikawa 因果图）：水平主骨 → 右端结果框；大骨上下交替斜出，
    子因水平短线沿大骨排布（文字不旋转，约束7）。
    bones=[(类别名, [子因 ≤4])] 3–6 根；effect=结果/问题。
    来源：Kaoru Ishikawa，1960s 普及（川崎造船所质量管理；ASQ 七大质量工具，调研报告候选6）。
    与 G-01 分工：MECE 逻辑分解→G-01；制造业质量/工序归因（6M 语言）→本图。"""
    if not 3 <= len(bones) <= 6:
        raise ValueError("G-04 大骨限 3–6 根（6M 惯例上限），收到 %d" % len(bones))
    for nm, subs in bones:
        if len(subs) > 4:
            raise ValueError(f"G-04 「{nm}」子因限 ≤4，收到 {len(subs)}")
    head_w = 150
    spine_y = y + h / 2
    sx0, sx1 = x + 20, x + w - head_w - 12
    s = L(sx0, spine_y, sx1, spine_y, INK1, 2.5)
    s += f'<polygon points="{sx1},{spine_y-7} {sx1+12},{spine_y} {sx1},{spine_y+7}" fill="{INK1}"/>'
    s += f'<rect x="{x+w-head_w}" y="{spine_y-34:.1f}" width="{head_w}" height="68" rx="4" fill="{INK1}"/>'
    for i, ln in enumerate(effect if isinstance(effect, (list, tuple)) else [effect]):
        s += T(x + w - head_w / 2, spine_y - 2 + i * 20 + (0 if isinstance(effect, str) else -8), ln, 13.5, "#FFFFFF", 700, anchor="middle")
    top = [b for i, b in enumerate(bones) if i % 2 == 0]
    bot = [b for i, b in enumerate(bones) if i % 2 == 1]
    reach = h / 2 - 44
    for group, sign in ((top, -1), (bot, 1)):
        n = len(group)
        for k, (nm, subs) in enumerate(group):
            bx1 = sx0 + (k + 1) * (sx1 - sx0 - 60) / (n + 0.35)   # 大骨与主骨交点
            bx0 = bx1 - reach * 0.72                                # 45° 斜骨起点
            by0 = spine_y + sign * reach
            s += L(bx0, by0, bx1, spine_y, INK2, 1.8)
            s += T(bx0, by0 + (-10 if sign < 0 else 20), nm, 13, INK1, 700, anchor="middle")
            for j, sub in enumerate(subs):                          # 子因水平短线（沿斜骨等距）
                f = (j + 1) / (len(subs) + 1)
                jx = bx0 + f * (bx1 - bx0)
                jy = by0 + f * (spine_y - by0)
                s += L(jx, jy, jx + 64, jy, INK3, 1)
                s += T(jx + 70, jy + 4, sub, 11, INK2)
    return s


def impact_effort(x, y, w, h, items, quads=None, x_axis="投入 / 难度 →", y_axis="↑ 影响 / 价值"):
    """A-04 Impact-Effort 优先级矩阵（2×2 快赢矩阵）：举措按 (impact, effort) 落位。
    items=[(名, impact 0–10, effort 0–10, hi?)] 2–12 项；
    quads 默认（速赢, 重大项目, 填空任务, 吃力不讨好）按（高I低E, 高I高E, 低I低E, 低I高E）。
    来源：无单一可考原版（通用优先级工具族，可上溯艾森豪威尔矩阵；1990s 进入战略咨询工作坊——调研报告候选2）。
    与 S-02 portfolio_matrix 分工：资产组合气泡落位→S-02；举措优先级点落位→本表。"""
    if not 2 <= len(items) <= 12:
        raise ValueError("A-04 举措数限 2–12，收到 %d" % len(items))
    for it in items:
        if not (0 <= it[1] <= 10 and 0 <= it[2] <= 10):
            raise ValueError(f"A-04 「{it[0]}」impact/effort 须 0–10")
    quads = quads or ("速赢 Quick Wins", "重大项目", "填空任务", "吃力不讨好")
    mx, my = x + (w - 40) / 2 + 40, y + (h - 36) / 2
    px, pw, ph = x + 40, w - 40, h - 36
    s = f'<rect x="{px}" y="{y}" width="{pw:.0f}" height="{ph:.0f}" fill="#FFFFFF" stroke="{INK3}" stroke-width="1.2"/>'
    s += L(mx, y, mx, y + ph, INK4, 0.8, dash="4,3") + L(px, my, px + pw, my, INK4, 0.8, dash="4,3")
    QP = [(px + pw * 0.25, y + 22), (px + pw * 0.75, y + 22),
          (px + pw * 0.25, y + ph - 10), (px + pw * 0.75, y + ph - 10)]
    for (qx, qy), qn in zip(QP, quads):
        s += T(qx, qy, qn, 11, INK3, 700, ls=1, anchor="middle")
    s += T(px + pw / 2, y + ph + 26, x_axis, 12, INK2, anchor="middle")
    s += T(x + 12, y + 14, y_axis, 12, INK2)
    for it in items:
        nm, imp, eff, hi = (it + (False,))[:4]
        cx = px + eff / 10 * (pw - 40) + 20
        cy = y + ph - (imp / 10 * (ph - 40) + 20)
        c = ACC if hi else INK1
        s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{c}"/>'
        s += T(cx + 12, cy + 4, nm, 12, INK1, 700 if hi else 400)
    return s


def competitive_arc(x, y, w, h, vendors, bands=None, x_axis="战略前瞻 →", y_axis="↑ 当前能力"):
    """S-17 竞争格局定位图（弧带型，去品牌化）：双轴散点 + 右上角同心弧带分档 + 气泡大小=市场存在感。
    vendors=[(名, x 0–10, y 0–10, size 1–3, hi?)] 3–12 家；bands 默认（领导者, 强劲表现者, 竞争者）由外弧到内。
    来源：版式结构对标 Forrester Wave（Forrester Research, 2002 年 7 月官方发布：Current offering=Y 轴、
    Strategy=X 轴、Market presence=点大小——调研报告候选3）。**商标纪律**：Magic Quadrant / Forrester Wave
    为注册商标，本函数仅实现通用"双轴+弧带+气泡"结构，禁用品牌名称/专有措辞/专有配色。
    与 S-02 portfolio_matrix 分工：自有资产组合→S-02；外部竞品/供应商格局→本图。"""
    if not 3 <= len(vendors) <= 12:
        raise ValueError("S-17 厂商数限 3–12，收到 %d" % len(vendors))
    for vd in vendors:
        if not (0 <= vd[1] <= 10 and 0 <= vd[2] <= 10 and 1 <= vd[3] <= 3):
            raise ValueError(f"S-17 「{vd[0]}」坐标须 0–10 / size 1–3")
    bands = bands or ("领导者", "强劲表现者", "竞争者")
    px, pw, ph = x + 44, w - 44, h - 36
    cx0, cy0 = px + pw, y                     # 弧心=绘图区右上角
    s = f'<rect x="{px}" y="{y}" width="{pw:.0f}" height="{ph:.0f}" fill="#FFFFFF" stroke="{INK3}" stroke-width="1.2"/>'
    rmax = min(pw, ph) * 0.96
    for k, bn in enumerate(bands):            # 同心 1/4 弧带（外→内），灰阶递浅
        r = rmax * (1 - k * 0.30)
        s += (f'<path d="M {cx0 - r:.1f} {cy0} A {r:.1f} {r:.1f} 0 0 0 {cx0} {cy0 + r:.1f}" '
              f'fill="none" stroke="{INK4}" stroke-width="1" stroke-dasharray="5,4"/>')
        s += T(cx0 - r + 10, cy0 + 20, bn, 11, INK3, 700, ls=1)
    s += T(px + pw / 2, y + ph + 26, x_axis, 12, INK2, anchor="middle")
    s += T(x + 10, y + 14, y_axis, 12, INK2)
    for vd in vendors:
        nm, vx, vy, sz, hi = (tuple(vd) + (False,))[:5]
        cx = px + vx / 10 * (pw - 44) + 22
        cy = y + ph - (vy / 10 * (ph - 44) + 22)
        r = 6 + sz * 4
        c = ACC if hi else INK2
        s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{c}" opacity="0.85"/>'
        s += T(cx, cy + r + 15, nm, 11.5, INK1, 700 if hi else 400, anchor="middle")
    s += T(px + pw - 8, y + ph - 10, "气泡大小 = 市场存在感（示意三档）", 10.5, INK3, anchor="end")
    return s


def decision_tree(x, y, w, h, decision, options):
    """A-05 决策树（含概率与收益）：左侧方形决策节点 → 2–4 选项分支；选项可带概率子分支
    （圆形机会节点 → ≤3 个 (情形, 概率, 收益)）或直接收益；期望值 EV 由**调用方传入**，
    函数绝不计算（同 price_table 合计纪律：数字可复算性归内容层）。
    options=[(选项名, payoff字符串 或 [(情形, 概率, 收益)], ev字符串 或 None, hi?)]。
    来源：John F. Magee, "Decision Trees for Decision Making," HBR, 1964-07（调研报告候选8）。
    与 A/B 选择直排页分工：静态两选一→直排；多阶段+概率+期望值→本图。"""
    if not 2 <= len(options) <= 4:
        raise ValueError("A-05 选项限 2–4 支，收到 %d" % len(options))
    for op in options:
        if isinstance(op[1], (list, tuple)) and len(op[1]) > 3:
            raise ValueError(f"A-05 「{op[0]}」概率分支限 ≤3")
    n = len(options)
    dx, dy = x + 20, y + h / 2
    s = f'<rect x="{dx}" y="{dy-30:.1f}" width="150" height="60" rx="3" fill="{INK1}"/>'
    for i, ln in enumerate(decision if isinstance(decision, (list, tuple)) else [decision]):
        s += T(dx + 75, dy + 5 + (i - (0 if isinstance(decision, str) else 0.5)) * 18, ln, 13, "#FFFFFF", 700, anchor="middle")
    row_h = h / n
    bx = dx + 150
    for i, op in enumerate(options):
        nm, payoff, ev, hi = (tuple(op) + (None, False))[:4]
        oy = y + (i + 0.5) * row_h
        mx = bx + 130
        s += f'<path d="M {bx} {dy:.1f} L {bx+40} {dy:.1f} L {bx+70} {oy:.1f} L {mx} {oy:.1f}" fill="none" stroke="{INK2 if not hi else ACC}" stroke-width="1.6"/>'
        s += T(bx + 76, oy - 10, nm, 12.5, INK1, 700)
        if isinstance(payoff, (list, tuple)):         # 机会节点 + 概率分支
            ccx = mx + 26
            s += f'<circle cx="{ccx}" cy="{oy:.1f}" r="12" fill="none" stroke="{INK1}" stroke-width="1.6"/>'
            m = len(payoff)
            for j, (case, p, po) in enumerate(payoff):
                jy = oy + (j - (m - 1) / 2) * min(52, row_h / m)
                s += L(ccx + 12, oy, ccx + 64, jy, INK3, 1.1)
                s += T(ccx + 70, jy + 4, f"{case} · p={p}", 11, INK2)
                s += T(x + w - 16, jy + 4, po, 12.5, INK1, 700, fam=MONO, anchor="end")
        else:
            s += T(x + w - 16, oy + 4, payoff, 12.5, INK1, 700, fam=MONO, anchor="end")
        if ev:
            s += T(bx + 76, oy + 22, "EV " + ev + "（口径见脚注）", 11, "#6E6E6E", fam=MONO)
    return s
