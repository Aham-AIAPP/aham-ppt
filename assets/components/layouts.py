# -*- coding: utf-8 -*-
"""layouts.py — 版式库内容区型版式的参数化层（坐标冻结）。

范围：S/E/A/G 系保留版式（hero/concept_curve/stage_flow/tri_layer/action_table/
pyramid_light/team_grid/price_table）。整页型 I·T 系与纯栅格版式已于 v4.0 移出版式库，
走 AI 通用能力直排，规范见 references/grid-composition.md。
纪律：内容数量数据驱动，仅在有依据处硬校验（CONTRIBUTING §教训固化机制）。
"""
from components import T, L, P, MONO, INK1, INK2, INK3, INK4, LINE, PANEL, placeholder

_DK1, _DK2, _DK3 = "#FFFFFF", "#A8A8A8", "#787878"   # 深底三级字


def _as_lines(v, where):
    """行列表参数防呆：str 会被逐字迭代成竖排——一律显式拦截。"""
    if isinstance(v, str):
        raise ValueError(f"{where} 需要行列表（list[str]），收到 str——请写成 [\"{v[:10]}…\"]")
    return v











def hero(conclusion_lines, supports):
    """S-07 HERO：深墨结论区 + N 张支撑卡。supports **硬拦 N=2/3/4**
    （依据 grid-system §3.6 仅定义 HERO-2/3/4 三档栅格）。
    supports=[(label, title, [desc 行×1–3])]。conclusion_lines=1–2 行。"""
    n = len(supports)
    if n not in (2, 3, 4):
        raise ValueError("S-07 支撑数硬拦 2/3/4（grid §3.6 三档栅格），收到 %d" % n)
    COLS = {2: [(40, 592), (648, 592)],
            3: [(40, 389), (445, 389), (850, 390)],
            4: [(40, 288), (344, 288), (648, 288), (952, 288)]}[n]
    b = f'<rect x="40" y="100" width="1200" height="255" rx="4" fill="{INK1}"/>'
    b += T(56, 136, "CORE FINDING", 11, "#A8A8A8", ls=3)
    for i, ln in enumerate(_as_lines(conclusion_lines, 'conclusion_lines')[:2]):
        b += T(56, 188 + i * 40, ln, 26, "#FFFFFF", 700)
    fs_t, fs_d, pad = (22, 13, 20) if n < 4 else (18, 12, 18)
    for (la, tt, ds), (x, w) in zip(supports, COLS):
        b += P(x, 371, w, 309, PANEL, r=4) + f'<rect x="{x}" y="371" width="4" height="309" fill="{INK1}"/>'
        b += T(x + pad, 403, la, 11, INK1, ls=2)
        b += T(x + pad, 440 if n < 4 else 436, tt, fs_t, INK1, 700, fam=MONO)
        y0 = 470 if n < 4 else 464
        for j, d in enumerate(_as_lines(ds, 'desc 行')[:3]):
            b += T(x + pad, y0 + j * 24, d, fs_d, INK2)
    return b





# ============================================================ E 系（内容区型）
def concept_curve(y_label, x_label, stage_labels, current_label, conclusion_lines, right_descs):
    """E-02 概念曲线（示意，非量化）：三段固定形态曲线（爬升实线→平台→冲顶虚线，
    语义色为骨架冻结值）+ 当前位置红点 + 右侧结论。stage_labels 固定 3 段标签。
    多条 S 曲线错峰（三地平线）→ charts.horizon_curves（E-91）。"""
    if len(stage_labels) != 3:
        raise ValueError("E-02 三段曲线形态固定，需恰好 3 个阶段标签，收到 %d" % len(stage_labels))
    b = L(140, 560, 140, 180, INK1, 2) + L(140, 560, 820, 560, INK1, 2)
    b += T(60, 178, y_label, 12, INK2, anchor="middle") + T(830, 566, x_label, 12, INK2)
    b += '<path d="M 160 540 Q 220 520, 280 460 T 380 390" stroke="#5A7A60" stroke-width="4.5" fill="none"/>'
    b += '<path d="M 380 390 Q 450 360, 510 352 T 580 370" stroke="#8A7333" stroke-width="4.5" fill="none"/>'
    b += '<path d="M 580 370 Q 650 330, 720 280" stroke="#9B9B9B" stroke-width="4.5" fill="none" stroke-dasharray="6,4"/>'
    b += '<circle cx="580" cy="370" r="11" fill="#9E3D31"/>'
    b += L(580, 360, 580, 272, "#9E3D31", 1.2, dash="3,3")
    b += T(558, 252, current_label, 12, "#9E3D31", 700)
    for (x, c), la in zip([(270, "#5A7A60"), (460, "#8A7333"), (650, INK1)], stage_labels):
        b += T(x, 592, la, 14, c, 700)
    for i, ln in enumerate(_as_lines(conclusion_lines, 'conclusion_lines')[:2]):
        b += T(900, 290 + i * 36, ln, 24, INK1, 700)
    b += L(900, 344, 1224, 344, LINE, 0.5)
    for j, d in enumerate(_as_lines(right_descs, 'right_descs')[:2]):
        b += T(900, 372 + j * 24, d, 13, INK2)
    return b


def stage_flow(stages, dark_last=True):
    """E-03 流程示意：3–6 段方框 + line+polygon 箭头（禁 marker），末段默认深色收束。
    stages=[(眉标, 名称)]；4 段时精确复现骨架坐标（x=80 起步 262，框 200×100，y=260）。"""
    n = len(stages)
    if not 3 <= n <= 6:
        raise ValueError("E-03 阶段数限 3–6，收到 %d" % n)
    w = 200 if n <= 4 else (986 - 32 * (n - 1)) / n
    step = (986 - w) / (n - 1)
    b = ""
    for i, (tag, nm) in enumerate(stages):
        x = 80 + i * step
        last = dark_last and i == n - 1
        if last:
            b += f'<rect x="{x:.0f}" y="260" width="{w:.0f}" height="100" rx="4" fill="{INK1}"/>'
            tc1, tc2 = "#C4C4C4", "#FFFFFF"
        else:
            b += P(x, 260, w, 100, PANEL, r=4, stroke=INK3, sw=1.5)
            tc1, tc2 = INK1, INK1
        b += T(x + w / 2, 296, tag, 11, tc1, 700, ls=2, anchor="middle")
        b += T(x + w / 2, 326, nm, 14, tc2, 700, anchor="middle")
        if i < n - 1:
            x1 = x + w
            b += L(x1, 310, x1 + step - w - 12, 310, INK3, 2)
            b += f'<polygon points="{x1+step-w-12:.0f},304 {x1+step-w:.0f},310 {x1+step-w-12:.0f},316" fill="{INK1 if i < n-2 or not dark_last else INK1}"/>'
    return b


def tri_layer(layers):
    """E-04 轻量三层（概念）：**固定 3 层**深→中→浅 + 层间下行箭头。
    layers=[(眉标, 名称)×3]。层内多模块 / 跨层能力条的真实架构 → structures.arch_layers（E-04 高阶）。"""
    if len(layers) != 3:
        raise ValueError("E-04 轻量固定 3 层（>3 层或层内多模块改 arch_layers），收到 %d" % len(layers))
    FILL = [(INK1, "#C4C4C4", "#FFFFFF"), (INK2, "#C4C4C4", "#FFFFFF"), ("#C8C8C8", INK2, INK1)]
    YS = [140, 307, 474]
    ARROW = [(250, INK1), (417, INK3)]
    b = ""
    for i, ((tag, nm), y, (f, c1, c2)) in enumerate(zip(layers, YS, FILL)):
        b += f'<rect x="240" y="{y}" width="800" height="110" rx="4" fill="{f}"/>'
        b += T(640, y + 38, tag, 11, c1, ls=3, anchor="middle")
        b += T(640, y + 72, nm, 22, c2, 700, anchor="middle")
        if i < 2:
            ay, col = ARROW[i]
            b += L(640, ay, 640, ay + 45, INK3, 2)
            b += f'<polygon points="634,{ay+45} 640,{ay+57} 646,{ay+45}" fill="{col}"/>'
    return b




def action_table(actions):
    """A-03 轻量行动清单：深墨表头（行动/责任方/截止）+ **3–6 行**。
    actions=[(行动, 细节, 责任方, 截止)]；正式 RACI → structures.raci_matrix（A-03 高阶）。"""
    if not 3 <= len(actions) <= 6:
        raise ValueError("A-03 清单行数限 3–6（更多拆页或改 RACI），收到 %d" % len(actions))
    s = f'<rect x="40" y="120" width="1200" height="44" fill="{INK1}"/>'
    s += T(60, 148, "行动事项", 12, "#FFFFFF", 700) + T(680, 148, "责任方", 12, "#FFFFFF", 700) + T(980, 148, "截止时间", 12, "#FFFFFF", 700)
    for j, (a1, a2, ow, dl) in enumerate(actions):
        y = 164 + j * 60
        s += f'<rect x="40" y="{y}" width="1200" height="60" fill="#FFFFFF"/>'
        s += L(40, y + 60, 1240, y + 60, LINE, 0.5)
        s += T(60, y + 28, a1, 14, INK1, 700) + T(60, y + 48, a2, 11, INK2)
        s += T(680, y + 34, ow, 13, INK1) + T(980, y + 34, dl, 13, "#9E3D31", 700)
    return s



def pyramid_light(layers):
    """G-03 纯层级金字塔：**3–5 层**梯形（深→浅），每层 tag+标题，可选右侧虚线引注。
    layers=[(眉标, 标题, 右注 或 None)]；4 层时精确复现骨架 polygon 坐标。
    每层带多要素切格 / 逐层 takeaway → structures.layered_pyramid（G-93）。"""
    n = len(layers)
    if not 3 <= n <= 5:
        raise ValueError("G-03 层数限 3–5（复杂剖面改 G-93），收到 %d" % n)
    FILLS = {3: [INK1, INK2, "#C8C8C8"],
             4: [INK1, INK2, "#C8C8C8", "#E7E7E7"],
             5: [INK1, INK2, "#A8A8A8", "#C8C8C8", "#E7E7E7"]}[n]
    h = (458 - 6 * (n - 1)) / n
    tl = [440.0]
    for i in range(1, n):
        tl.append(tl[-1] - (30 if i == 1 else 40))
    # 4 层引线为骨架冻结的不规则精确值；其它层数用规则值
    LEAD4 = [(875, 1000, 1010), (915, 1000, 1010), (955, 1000, 1010), (990, 1000, 1010)]
    b, leads = "", []
    for i, ((tag, tt, desc), f) in enumerate(zip(layers, FILLS)):
        y0 = 120 + i * (h + 6)
        l0, r0 = tl[i], 1280 - tl[i]
        l1 = tl[i + 1] if i + 1 < n else tl[i] - 40
        r1 = 1280 - l1
        b += f'<polygon points="{l0:.0f},{y0:.0f} {r0:.0f},{y0:.0f} {r1:.0f},{y0+h:.0f} {l1:.0f},{y0+h:.0f}" fill="{f}"/>'
        dark = f in (INK1, INK2, "#A8A8A8")
        b += T(640, y0 + h * 45 / 110, tag, 11, "#C4C4C4" if dark else INK2, ls=2, anchor="middle")
        b += T(640, y0 + h * 80 / 110, tt, 22 if i == 0 else 20, "#FFFFFF" if dark else INK1, 700, anchor="middle")
        if desc:
            ym = y0 + h / 2
            x1, x2, tx = LEAD4[i] if n == 4 else ((r0 + r1) / 2 + 5, 1000, 1010)
            leads.append((x1, x2, tx, ym, desc))
    for (x1, x2, tx, ym, desc) in leads:
        b += L(x1, ym, x2, ym, INK4, 0.5, dash="3,3")
        b += T(tx, ym + 5, desc, 12, INK2)
    return b


# ============================================================
#  S-14 团队页 / S-15 报价页（v3.2 新增，补齐客户方案缺口）
# ============================================================

def _eq_cols(k, total=1200, gutter=16, x0=40):
    """等分列引擎：均分 + 余数摊给末列 1px 级（与 grid §3 等分纪律一致，右缘恰 x0+total）。"""
    w0 = (total - gutter * (k - 1)) // k
    rem = (total - gutter * (k - 1)) - w0 * k
    cols, x = [], x0
    for i in range(k):
        w = w0 + (rem if i == k - 1 else 0)
        cols.append((x, w)); x += w + gutter
    return cols


def team_grid(members):
    """S-14 团队页（人像占位 + 职务网格）。members=[(name, title, note)] **2–8 人**（函数强制）。
    照片一律 components.placeholder 占位——等真实照片替换，不硬编假头像（同 SKILL 附·工程预检 4）。
    N≤4 单行；5–8 人两行×4 列。坐标等分冻结（389/389/390、288×4 同源算法）。"""
    n = len(members)
    if not 2 <= n <= 8:
        raise ValueError("S-14 团队页限 2–8 人，收到 %d" % n)
    rows = [members] if n <= 4 else [members[:4], members[4:]]
    b = ""
    for ri, row in enumerate(rows):
        cols = _eq_cols(len(row) if n <= 4 else 4)
        y0 = 130 if n <= 4 else (110 if ri == 0 else 400)
        ph_h = 300 if n <= 4 else 150
        for (name, title, note), (x, w) in zip(row, cols):
            b += placeholder(x, y0, w, ph_h, label="成员照片")
            ty = y0 + ph_h + 34
            b += T(x, ty, name, 18, INK1, 700)
            b += T(x, ty + 24, title, 12, INK2, 600)
            if note:
                b += T(x, ty + 46, note, 11, INK2)
    return b


def price_table(rows, header=("项目", "说明", "金额"), total=None, total_label="合计", note=""):
    """S-15 报价/条款页（三线表）。rows=[(item, desc, amount_str)] **1–8 行**（函数强制）。
    金额为**字符串**由调用方算好传入（含币种/千分位，绝不由函数求和——不猜数、不编数）。
    表格纪律：只横线无竖线、数字右对齐 mono、表头/合计加粗（brand §4 表格规范）。"""
    if not 1 <= len(rows) <= 8:
        raise ValueError("S-15 报价表限 1–8 行，收到 %d" % len(rows))
    x0, x1, rh = 40, 1240, 52
    cx_item, cx_desc, cx_amt = 56, 380, 1224
    y = 140
    b = f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{INK1}" stroke-width="1.5"/>'
    b += T(cx_item, y + 33, header[0], 13, INK1, 700)
    b += T(cx_desc, y + 33, header[1], 13, INK1, 700)
    b += T(cx_amt, y + 33, header[2], 13, INK1, 700, anchor="end")
    y += rh
    b += L(x0, y, x1, y)
    for item, desc, amt in rows:
        b += T(cx_item, y + 33, item, 14, INK1, 600)
        b += T(cx_desc, y + 33, desc, 12, INK2)
        b += T(cx_amt, y + 33, amt, 14, INK1, 600, fam=MONO, anchor="end")
        y += rh
        b += L(x0, y, x1, y)
    if total is not None:
        b += T(cx_item, y + 33, total_label, 14, INK1, 700)
        b += T(cx_amt, y + 33, total, 15, INK1, 700, fam=MONO, anchor="end")
        y += rh
    b += f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{INK1}" stroke-width="1.5"/>'
    if note:
        b += T(x0, y + 28, note, 11, INK2)
    return b
