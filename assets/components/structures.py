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
