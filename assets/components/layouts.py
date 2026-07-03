# -*- coding: utf-8 -*-
"""layouts.py — 整页型手画版式的参数化层（坐标冻结，替代"照抄骨架"人工流程）。

范围：I/T 系整页版式（自带极简页脚，返回完整 SVG）。
内容区型版式（S/E/V/A/G 手画）见本模块后续批次；参数化结构版式见 structures.py。
纪律：坐标一律取自各系骨架规范（svg-skeleton-*.md 历史冻结值），函数内为唯一真源；
内容数量数据驱动，仅在有依据处硬校验（CONTRIBUTING §教训固化机制）。
"""
from components import T, L, P, MONO, ACC, INK1, INK2, INK3, INK4, LINE, PANEL, placeholder

_DK1, _DK2, _DK3 = "#FFFFFF", "#A8A8A8", "#787878"   # 深底三级字


def _as_lines(v, where):
    """行列表参数防呆：str 会被逐字迭代成竖排——一律显式拦截。"""
    if isinstance(v, str):
        raise ValueError(f"{where} 需要行列表（list[str]），收到 str——请写成 [\"{v[:10]}…\"]")
    return v

def _page(body, bg="#FFFFFF"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">'
            f'<rect width="1280" height="720" fill="{bg}"/>{body}</svg>')


def _secpath(text, dark=False):
    return T(40, 40, text, 10, _DK3 if dark else INK3, ls=2)


def _minifoot(source, page, dark=False):
    c = _DK3 if dark else INK3
    return (T(40, 708, "来源：" + source, 10, c) +
            T(1240, 708, page, 10, c, fam=MONO, anchor="end"))


# ============================================================ I-01 大数字页
def bignumber(sec, big, assertion, source, page,
              compare_anchor=None, support2=None, warning=None, evidence=None):
    """I-01 大数字页（两变体）。
    - 基础变体（evidence=None）：compare_anchor **必填**——大数字必须带对比锚点
      （同比/目标/行业基准三选一），禁止数字悬空（对标评估 P2 纪律）。
    - 带证据变体（evidence=(right_header, [(label, desc)×3])）：右列固定 3 条支撑；
      compare_anchor/support2 变为可选补充行。
    warning 可选（红色警示行，仅基础变体位）。"""
    if evidence is None:
        if not compare_anchor:
            raise ValueError("I-01 基础变体 compare_anchor 必填（大数字禁止悬空）")
        b = _secpath(sec)
        b += T(140, 380, big, 180, INK1, 700)
        b += L(140, 410, 420, 410, INK1, 1.2)
        b += T(140, 456, assertion, 30, INK1, 700)
        b += T(140, 506, compare_anchor, 14, INK2)
        if support2:
            b += T(140, 530, support2, 14, INK2)
        if warning:
            b += T(140, 610, warning, 13, "#9E3D31", ls=1)
        return _page(b + _minifoot(source, page))
    rh, items = evidence
    if len(items) != 3:
        raise ValueError("I-01 带证据变体固定 3 条支撑（右列三段栅格）")
    b = _secpath(sec)
    b += T(140, 380, big, 170, INK1, 700)
    b += L(140, 400, 440, 400, INK1, 1.5)
    b += T(140, 440, assertion, 28, INK1, 700)
    b += L(800, 140, 800, 610, LINE, 1)
    b += T(860, 170, rh, 13, "#9E3D31", ls=2)
    b += L(860, 192, 1000, 192, "#9E3D31", 1.8)
    for i, (la, de) in enumerate(items):
        y = 234 + i * 98
        b += T(860, y, la, 14, INK1, 700) + T(860, y + 24, de, 13, INK1)
        if i < 2:
            b += L(860, y + 56, 1200, y + 56, LINE, 0.5)
    if compare_anchor:
        b += T(140, 500, compare_anchor, 14, INK2)
    if support2:
        b += T(140, 526, support2, 14, INK2)
    return _page(b + _minifoot(source, page))


# ============================================================ I-05 时间窗警告
def time_window(sec, past, now, now_tag, future, warning_title, warning_desc,
                window, window_label, source, page):
    """I-05 时间窗警告：过去/现在/未来三节点固定（版式语义即三态），
    紧迫性靠红色"当前"节点 + 警示标题双通道，窗口数字保持墨色（brand 禁染红绿）。"""
    b = _secpath(sec)
    b += L(100, 200, 1180, 200, INK4, 1.5)
    b += f'<circle cx="200" cy="200" r="8" fill="{INK3}"/>'
    b += T(200, 234, past, 12, INK3, anchor="middle")
    b += '<circle cx="640" cy="200" r="20" fill="#9E3D31"/>'
    b += T(640, 207, now, 13, "#FFFFFF", 700, anchor="middle")
    b += T(640, 250, now_tag, 13, "#9E3D31", 700, anchor="middle")
    b += (f'<circle cx="1080" cy="200" r="8" fill="{INK4}" stroke="{INK3}"'
          f' stroke-width="1" stroke-dasharray="3,3"/>')
    b += T(1080, 234, future, 12, INK3, anchor="middle")
    b += T(640, 360, warning_title, 34, INK1, 700, anchor="middle")
    b += T(640, 404, warning_desc, 15, INK2, anchor="middle")
    b += T(640, 510, window, 60, INK1, 700, anchor="middle")
    b += T(640, 558, window_label, 14, INK3, anchor="middle")
    return _page(b + _minifoot(source, page))


# ============================================================ T-01 深色引言页
def quote_page(line1, line2, sub, attribution, source, page):
    """T-01 深色引言页（章节间过渡）。与 themes.quote_dark（C 档金句页，
    大引号+居中）为两个不同页型，不互相替代。深底上唯一蓝点缀=顶部短线。
    引语来源纪律：真实语录须可考；自撰声明句须在 attribution 注明"本演示自撰"。"""
    b = f'<rect x="80" y="80" width="40" height="2" fill="{ACC}"/>'
    b += T(120, 310, line1, 36, _DK1, 700)
    if line2:
        b += T(120, 360, line2, 36, _DK1, 700)
    if sub:
        b += T(120, 440, sub, 22, _DK2)
    if attribution:
        b += T(1200, 640, "—— " + attribution, 13, _DK2, anchor="end")
    return _page(b + _minifoot(source, page, dark=True), bg="#1C1C1C")


# ============================================================ T-02 白底大字宣言
def declaration(sec, line1, line2, sub_note, source, page):
    """T-02 白底大字宣言：居中双行 44px + 灰短线 + 副注。"""
    b = _secpath(sec)
    b += T(640, 310, line1, 44, INK1, 700, anchor="middle")
    if line2:
        b += T(640, 366, line2, 44, INK1, 700, anchor="middle")
    b += L(580, 410, 700, 410, INK3, 2.5)
    if sub_note:
        b += T(640, 456, sub_note, 16, INK2, anchor="middle")
    return _page(b + _minifoot(source, page))


# ============================================================ T-03 章节承接页
def bridge(sec, prev_title, prev_summary, next_title, next_intro, nav, source, page):
    """T-03 章节承接：左"刚讲完"（灰）/ 右"即将进入"（墨），中竖分隔，底部导航。"""
    b = _secpath(sec)
    b += T(100, 200, "JUST COMPLETED", 11, INK3, ls=3) + L(100, 220, 220, 220, INK3, 1)
    b += T(100, 270, prev_title, 22, INK3, 700) + T(100, 310, prev_summary, 14, INK2)
    b += L(520, 160, 520, 560, LINE, 0.5)
    b += T(580, 200, "NEXT PART", 11, INK1, ls=3) + L(580, 220, 700, 220, INK3, 1.5)
    b += T(580, 320, next_title, 36, INK1, 700) + T(580, 380, next_intro, 16, INK2)
    if nav:
        b += T(640, 650, nav, 11, INK3, anchor="middle")
    return _page(b + _minifoot(source, page))


# ============================================================ S 系（内容区型：返回 body，由 themes.chrome 包裹）
def quad_cards(quads):
    """S-02 轻量 2×2 四格（定性）。quads=[(title, [bullets])×4] **固定 4 格**（版式语义）；
    每格 bullets 1–4 条。带数据落位/气泡 → structures.portfolio_matrix（S-02 高阶）。"""
    if len(quads) != 4:
        raise ValueError("S-02 四格版式固定 4 格（象限语义），收到 %d" % len(quads))
    POS = [(40, 100, 590), (646, 100, 594), (40, 398, 590), (646, 398, 594)]
    b = ""
    for (tt, bl), (x, y, w) in zip(quads, POS):
        b += P(x, y, w, 282, PANEL, r=4)
        b += T(x + 16, y + 28, tt, 14, INK1, 700)
        b += L(x + 16, y + 36, x + w - 16, y + 36, INK3, 1.5)
        for j, t_ in enumerate(bl[:4]):
            b += f'<rect x="{x+16}" y="{y+50+j*24}" width="3" height="14" rx="1" fill="{INK3}"/>'
            b += T(x + 26, y + 60 + j * 24, t_, 13, INK1)
    return b


def milestone_axis(nodes):
    """S-03 轻量单轴时间线。nodes=[(编号, 日期, 标题, 描述1, 描述2)] **3–5 个**，
    轴 y=240 等距分布（3 节点时精确复现骨架 cx=200/570/940）。多泳道 → A-90。"""
    n = len(nodes)
    if not 3 <= n <= 5:
        raise ValueError("S-03 节点数限 3–5（少于 3 不成轴，多于 5 改 A-90 泳道），收到 %d" % n)
    b = L(80, 240, 1200, 240, INK3, 2)
    for i, (m, dt, tt, d1, d2) in enumerate(nodes):
        cx = 200 + i * (740 / (n - 1))
        b += f'<circle cx="{cx:.0f}" cy="240" r="20" fill="{INK1}"/>'
        b += T(cx, 246, m, 13, "#FFFFFF", 700, anchor="middle")
        b += T(cx, 210, dt, 12, INK3, anchor="middle")
        b += P(cx - 60, 290, 120, 120, PANEL, r=3, stroke=LINE, sw=0.5)
        b += T(cx, 318, tt, 13, INK1, 700, anchor="middle")
        b += T(cx, 342, d1, 12, INK2, anchor="middle")
        b += T(cx, 362, d2, 12, INK2, anchor="middle")
    return b


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


def versus(left_header, right_header, left_rows, right_rows):
    """S-08 VS 对照：左灰右墨、行行水平对齐、中缝虚线 + VS。行数 **3–5** 且左右等长。"""
    if len(left_rows) != len(right_rows):
        raise ValueError("S-08 左右行数必须相等（%d vs %d）" % (len(left_rows), len(right_rows)))
    if not 3 <= len(left_rows) <= 5:
        raise ValueError("S-08 对照行数限 3–5，收到 %d" % len(left_rows))
    b = T(320, 160, left_header, 13, INK3, ls=4, anchor="middle")
    b += T(960, 160, right_header, 13, INK1, ls=4, anchor="middle")
    b += L(640, 180, 640, 650, LINE, 0.5, dash="4,4") + T(628, 410, "VS", 20, INK4)
    for j, (lr, rr) in enumerate(zip(left_rows, right_rows)):
        y = 200 + j * 80
        b += P(60, y, 520, 60, PANEL, r=3) + T(80, y + 36, lr, 14, INK2)
        b += P(660, y, 520, 60, PANEL, r=3) + T(680, y + 36, rr, 14, INK1, 700)
    return b


def kpi_six(cards):
    """S-09 轻量数字速览（2×3 手排格）。cards=[(label, value, desc)] **≤6**，按行填充。
    正式经营看板（值+基准+sparkline）→ charts.kpi_card（S-09 高阶）。"""
    if not 1 <= len(cards) <= 6:
        raise ValueError("S-09 轻量格限 1–6 张，收到 %d" % len(cards))
    POS = [(40, 120, 373), (453, 120, 373), (866, 120, 374),
           (40, 320, 373), (453, 320, 373), (866, 320, 374)]  # 等分 373/373/374·缝40·右缘1240（v3.1）
    b = ""
    for (la, v, de), (x, y, w) in zip(cards, POS):
        b += P(x, y, w, 160, PANEL, r=4)
        b += T(x + 16, y + 28, la, 12, INK3)
        b += T(x + 16, y + 90, v, 44, INK1, 700, fam=MONO)
        b += T(x + 16, y + 146, de, 12, INK2)
    return b


def full_panel(title, bullets=None, body=""):
    """S-12 全版铺满容器：面板 + 标题 + 分隔线，内容二选一——
    bullets（简易 1–12 条，y=162 起步 34）或 body（自由 SVG 片段，调用方负责 FULL 区内排布）。"""
    if bullets and body:
        raise ValueError("S-12 bullets 与 body 二选一")
    b = P(40, 100, 1200, 580, PANEL, r=4)
    b += T(56, 132, title, 14, INK1, 700)
    b += L(56, 142, 1224, 142, INK3, 1.5)
    for j, t_ in enumerate((bullets or [])[:12]):
        b += f'<rect x="56" y="{162+j*34}" width="3" height="14" rx="1" fill="{INK3}"/>'
        b += T(68, 172 + j * 34, t_, 14, INK1)
    return b + body


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


# ============================================================ A·G 系（内容区型）
def three_steps(steps):
    """A-01 下一步三步决策：**固定 3 步**（版式语义），末步深色+蓝条收束。
    steps=[(时间标注, 行动, [细节 1–3 行])×3]。"""
    if len(steps) != 3:
        raise ValueError("A-01 固定 3 步（多步排期改 A-90 / S-03），收到 %d" % len(steps))
    b = ""
    for i, (tm, ac, ds) in enumerate(steps):
        x, dark = 40 + i * 410, (i == 2)
        if dark:
            b += f'<rect x="{x}" y="160" width="380" height="400" rx="4" fill="{INK1}"/>'
            b += f'<rect x="{x}" y="160" width="4" height="400" fill="{ACC}"/>'
            tc1, tc2, tc3 = "#C4C4C4", "#FFFFFF", "#FFFFFF"
        else:
            b += P(x, 160, 380, 400, PANEL, r=4) + f'<rect x="{x}" y="160" width="4" height="400" fill="{INK1}"/>'
            tc1, tc2, tc3 = INK1, INK1, INK2
        b += T(x + 20, 192, f"STEP 0{i+1} · {tm}", 11, tc1, ls=3)
        b += T(x + 20, 236, ac, 22, tc2, 700)
        for j, d in enumerate(_as_lines(ds, 'desc 行')[:3]):
            b += T(x + 20, 268 + j * 24, d, 13, tc3)
    return b


def option_ab(a, b_, a_tag="OPTION A · 推荐", b_tag="OPTION B · 备选"):
    """A-02 是/否选择矩阵：A（推荐，墨条）/ B（备选，灰条降调）两选项 + 各自 pros/cons。
    a / b_ = (标题, 描述1, 描述2, pros, cons)。pros/cons 语义色为骨架冻结值。"""
    at, ad1, ad2, ap, ac_ = a
    bt, bd1, bd2, bp, bc = b_
    s = P(40, 140, 1200, 220, PANEL, r=4) + f'<rect x="40" y="140" width="5" height="220" fill="{INK1}"/>'
    s += T(62, 174, a_tag, 11, INK1, ls=3)
    s += T(62, 222, at, 28, INK1, 700)
    s += T(62, 260, ad1, 14, INK2) + T(62, 284, ad2, 14, INK2)
    s += T(1180, 222, ap, 13, "#5A7A60", anchor="end") + T(1180, 252, ac_, 13, "#9E3D31", anchor="end")
    s += T(640, 392, "或者", 13, INK3, anchor="middle")
    s += L(100, 392, 500, 392, LINE, 0.5) + L(780, 392, 1180, 392, LINE, 0.5)
    s += P(40, 410, 1200, 220, PANEL, r=4) + f'<rect x="40" y="410" width="5" height="220" fill="{INK3}"/>'
    s += T(62, 444, b_tag, 11, INK3, ls=3)
    s += T(62, 492, bt, 28, INK2, 700)
    s += T(62, 530, bd1, 14, INK3) + T(62, 554, bd2, 14, INK3)
    s += T(1180, 492, bp, 13, "#5A7A60", anchor="end") + T(1180, 522, bc, 13, "#9E3D31", anchor="end")
    return s


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


def pillars(items):
    """G-02 支柱并立：**2–4 柱**（默认语义 3），柱内 tag+大标题+要点 ≤4 + 底部深墨结论块。
    items=[(标题, 眉标, [要点], 结论)]；3 柱时精确复现骨架坐标（x=40/455/870，w=370）。"""
    n = len(items)
    if not 2 <= n <= 4:
        raise ValueError("G-02 支柱数限 2–4，收到 %d" % n)
    w = {2: 577, 3: 370, 4: 277}[n]
    b = ""
    for i, (tt, tag, pts, con) in enumerate(items):
        x = 40 + i * ((1200 - w) / (n - 1))
        b += P(x, 130, w, 520, PANEL, r=4) + f'<rect x="{x:.0f}" y="130" width="5" height="520" fill="{INK1}"/>'
        cx = x + w / 2
        b += T(cx, 170, tag, 11, INK1, ls=2, anchor="middle")
        b += T(cx, 230, tt, 34, INK1, 700, anchor="middle")
        b += L(x + 25, 250, x + w - 25, 250, INK4, 0.5)
        for j, p_ in enumerate(pts[:4]):
            b += f'<rect x="{x+25:.0f}" y="{268+j*32}" width="3" height="14" rx="1" fill="{INK3}"/>'
            b += T(x + 36, 279 + j * 32, p_, 13, INK1)
        b += f'<rect x="{x+15:.0f}" y="570" width="{w-30:.0f}" height="60" rx="3" fill="{INK1}"/>'
        b += T(cx, 606, con, 13, "#FFFFFF", 700, anchor="middle")
    return b


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
