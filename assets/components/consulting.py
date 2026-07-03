# -*- coding: utf-8 -*-
"""consulting.py · 咨询密集异形层（v2.5，D 层）

把「AI 方形大卡片味」的病根——等宽矩形阵 + 外框容器——替换为咨询惯用的异形
与标注语言：雪佛龙链 / 锥形流向带 / 哑铃 / 点阵 / 驱动树肘线 / 链式递减，
外加可叠在任意版式上的标注层（椭圆圈注 / 引线 / 水印 / 线画对勾 / So-What 条）。

—— 视觉硬约束（brand.md 同源）：灰阶 INK3/#C8C8C8 为主，ACC 蓝仅单点缀
   （单个高亮段/行/带或单个关键数字）；无渐变/阴影/饼图/多色。
—— PPTX 兼容（svg_to_pptx 实测结论，2026-07 FIFA26 版式实战）：
   · 禁在 <text>/<ellipse> 上用 translate+rotate 组合变换——实测转换后位置漂移；
     D 层不提供竖排方案。页眉/页脚/页面框架归 skeleton-common 与 themes.py，D 层禁止改动 chrome，只作用于内容区。
   · 箭头永远 line + polygon（marker 静默丢失）。
   · ✓/✗ 属 lint_svg tofu 高危字符，用 check() 线画对勾替代。
   · 细分段标注文字若含「名称+数值」务必自带空格（曾出 "1/44" 事故），
     并用 tick_label(level=0/1) 错层避让。
—— API 约定同 charts.py：传外框 (x,y,w,h)，返回 SVG 字符串，坐标自包含。
"""
from components import T, L, esc, MONO, ACC, INK1, INK2, INK3, INK4, LINE, PANEL
import math

GRAY_A = INK3        # 主灰
GRAY_B = "#C8C8C8"   # 次灰


def _arrhead(x1, y1, x2, y2, c=INK3, head=8):
    ang = math.atan2(y2 - y1, x2 - x1)
    p2x, p2y = x2 - head*math.cos(ang-0.42), y2 - head*math.sin(ang-0.42)
    p3x, p3y = x2 - head*math.cos(ang+0.42), y2 - head*math.sin(ang+0.42)
    return f'<polygon points="{x2:.1f},{y2:.1f} {p2x:.1f},{p2y:.1f} {p3x:.1f},{p3y:.1f}" fill="{c}"/>'


def leader(x1, y1, x2, y2, c=INK2, sw=1.4, head=7, dash=None):
    """引线箭头：把图表元素牵到旁注/编号动作。line+polygon，永不使用 marker。"""
    ang = math.atan2(y2-y1, x2-x1)
    bx, by = x2-head*math.cos(ang), y2-head*math.sin(ang)
    return L(x1, y1, bx, by, c, sw, dash=dash) + _arrhead(x1, y1, x2, y2, c, head)


def mark_ellipse(cx, cy, rx, ry, c=INK1, sw=2):
    """手绘感椭圆圈注（禁 rotate；倾斜观感靠 rx/ry 比例，不靠变换）。"""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{c}" stroke-width="{sw}"/>'


def watermark(x, y, text, size=220, c=INK1, op=0.035, fam=MONO):
    """大号淡水印（数字/短词）。务必最先绘制，压在所有内容底下。"""
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
            f'font-weight="900" fill="{c}" opacity="{op}" text-anchor="middle">{esc(text)}</text>')


def check(x, y, scale=1.0, c=INK1, sw=2.4):
    """线画对勾，替代 ✓（tofu 高危字符）。锚点 (x,y) 为拐点。"""
    a = 7*scale; b = 13*scale
    return (L(x-a, y-a*0.85, x, y, c, sw) + L(x, y, x+b, y-b*1.15, c, sw))


def tick_label(cx, y_top, text, level=0, c=INK2, fs=9.5, tick=8):
    """细分段的错层小标注：短竖线 + 微字。level 0/1 交替避让。
    text 请自带空格分隔名称与数值（教训：曾拼出 "1/44"）。"""
    ly = y_top - (tick + level*14)
    return (L(cx, y_top-1, cx, ly+3, INK4, 1) +
            T(cx, ly, text, fs, c, w=700, anchor="middle"))


def sowhat(x, y, w, h, label, text, dark=False):
    """So-What 锚点条（结论压底）。dark=True 深墨底白字，否则灰面板。"""
    if dark:
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{INK1}"/>'
        s += T(x+22, y+h/2+5, label, 12.5, "#FFFFFF", w=700)
        s += T(x+96, y+h/2+5, text, 13, "#FFFFFF")
    else:
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PANEL}"/>'
        s += T(x+22, y+h/2+5, label, 12.5, INK1, w=700)
        s += T(x+96, y+h/2+5, text, 13, INK1)
    return s


def chevron_flow(x, y, w, h, stages, gap=4, tip=None, hi=None):
    """雪佛龙阶段链。stages=[(name, big, sub)]；hi 段白底描边、大数字用 ACC（唯一蓝点缀）。"""
    n = len(stages); tip = tip or h*0.22
    cw = (w - gap*(n-1)) / n
    s = ""
    for i, (nm, big, sub) in enumerate(stages):
        x0 = x + i*(cw+gap)
        pts = (f'{x0},{y} {x0+cw-tip},{y} {x0+cw},{y+h/2} '
               f'{x0+cw-tip},{y+h} {x0},{y+h} {x0+tip},{y+h/2}')
        if hi == i:
            s += f'<polygon points="{pts}" fill="#FFFFFF" stroke="{INK1}" stroke-width="2.5"/>'
            tc, nc = INK1, ACC
        else:
            s += f'<polygon points="{pts}" fill="{INK1}"/>'
            tc, nc = "#FFFFFF", "#FFFFFF"
        cxm = x0 + cw/2 + tip*0.25
        s += T(cxm, y+h*0.28, nm, 13, tc, w=700, anchor="middle")
        s += T(cxm, y+h*0.66, str(big), h*0.30, nc, w=700, fam=MONO, anchor="middle")
        if sub:
            s += T(cxm, y+h*0.88, sub, 10, tc, anchor="middle")
    return s


def flow_bands(x, y, w, h, sources, target, hi=None, bar_w=110, tgt_w=140):
    """锥形流向带（sankey-lite）：左源块→右汇总块，带宽 ∝ 数值。
    sources=[(label, value)]；target=(big, sub)。hi 源用 ACC。"""
    total = sum(v for _, v in sources)
    gapy = 8
    unit = (h - gapy*(len(sources)-1)) / total
    tx = x + w - tgt_w
    th = min(h, max(90, h*0.72)); ty = y + (h-th)/2
    s = f'<rect x="{tx}" y="{ty}" width="{tgt_w}" height="{th}" rx="8" fill="{INK1}"/>'
    s += T(tx+tgt_w/2, ty+th/2-4, str(target[0]), 34, "#FFFFFF", w=700, fam=MONO, anchor="middle")
    s += T(tx+tgt_w/2, ty+th/2+22, target[1], 11.5, "#FFFFFF", anchor="middle")
    yy = y; tgt_y = ty + 6; usable = th - 12
    for i, (lab, v) in enumerate(sources):
        hh = v*unit
        col = ACC if hi == i else (GRAY_A if i % 2 == 0 else GRAY_B)
        s += f'<rect x="{x}" y="{yy}" width="{bar_w}" height="{hh}" rx="2" fill="{col}"/>'
        s += T(x-10, yy+hh/2+4, lab, 11.5, INK1, w=700, anchor="end")
        if hh >= 16:
            s += T(x+bar_w/2, yy+hh/2+4, str(v), 11.5, "#FFFFFF", w=700, fam=MONO, anchor="middle")
        else:
            s += T(x+bar_w+8, yy+hh/2+4, str(v), 10.5, col, w=700, fam=MONO)
        thh = hh * usable / (total*unit)   # 汇入带宽与源块同比例
        s += (f'<polygon points="{x+bar_w},{yy} {tx},{tgt_y} {tx},{tgt_y+thh} '
              f'{x+bar_w},{yy+hh}" fill="{col}" opacity="0.28"/>')
        yy += hh + gapy; tgt_y += thh
    return s


def dumbbell_rows(x, y, w, rows, row_h=62, hi=None):
    """哑铃行：每行独立比例尺的 a→b 对比。rows=[(label, a, b, delta)]。"""
    s = ""
    for i, (lab, a, b, delta) in enumerate(rows):
        yy = y + i*row_h + row_h/2
        mx = max(a, b)
        x0 = x + 96; x1 = x + w - 20
        xa = x0 + (x1-x0) * (a/mx) * 0.55
        s += T(x, yy+5, lab, 13.5, INK1, w=700)
        s += L(xa, yy, x1, yy, LINE, 3)
        s += L(xa, yy, x1-12, yy, GRAY_A, 3) + _arrhead(xa, yy, x1-10, yy, GRAY_A, 9)
        s += f'<circle cx="{xa}" cy="{yy}" r="8" fill="none" stroke="{GRAY_B}" stroke-width="3"/>'
        s += T(xa, yy-16, str(a), 13, INK2, w=700, fam=MONO, anchor="middle")
        dot = ACC if hi == i else INK1
        s += f'<circle cx="{x1}" cy="{yy}" r="9" fill="{dot}"/>'
        s += T(x1, yy-18, str(b), 15, INK1, w=700, fam=MONO, anchor="middle")
        s += T((xa+x1)/2, yy-9, delta, 10.5, INK2, w=700, anchor="middle")
    return s


def dot_matrix(x, y, cols, rows, gap=26, r=8, col_labels=None):
    """点阵机制图。rows=[(label, mode)]，mode∈ solid/dim/ring。"""
    s = ""
    if col_labels:
        for c in range(cols):
            s += T(x+c*gap, y-14, col_labels[c], 9.5, INK3, w=700, anchor="middle")
    for ri, (lab, mode) in enumerate(rows):
        yy = y + ri*gap
        s += T(x-18, yy+4, lab, 10.5, INK2, anchor="end")
        for c in range(cols):
            xx = x + c*gap
            if mode == "solid":
                s += f'<circle cx="{xx}" cy="{yy}" r="{r}" fill="{GRAY_A}"/>'
            elif mode == "dim":
                s += f'<circle cx="{xx}" cy="{yy}" r="{r}" fill="{INK4}"/>'
            else:
                s += (f'<circle cx="{xx}" cy="{yy}" r="{r}" fill="#FFFFFF" '
                      f'stroke="{INK2}" stroke-width="2.2" stroke-dasharray="3 2"/>')
    return s


def driver_node(x, y, w, h, big, sub, kind="branch"):
    """驱动树节点。kind: root(深墨)/branch(描边)/leaf(细边灰字)。"""
    if kind == "root":
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{INK1}"/>'
        s += T(x+w/2, y+h/2-2, str(big), h*0.42, "#FFFFFF", w=700, fam=MONO, anchor="middle")
        s += T(x+w/2, y+h/2+h*0.30, sub, 12, "#FFFFFF", w=700, anchor="middle")
    elif kind == "branch":
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#FFFFFF" stroke="{INK1}" stroke-width="1.6"/>'
        s += T(x+w/2, y+h/2-2, str(big), h*0.36, INK1, w=700, fam=MONO, anchor="middle")
        s += T(x+w/2, y+h/2+h*0.30, sub, 11.5, INK2, w=700, anchor="middle")
    else:
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.4"/>'
        s += T(x+w/2, y+h/2+4, sub, 12, INK2, anchor="middle")
    return s


def driver_elbow(x1, y1, x2, y2, c=INK1, sw=1.6):
    """驱动树肘线（横-竖-横三段直线，PPTX 原生 line）。"""
    xm = (x1+x2)/2
    return L(x1, y1, xm, y1, c, sw) + L(xm, y1, xm, y2, c, sw) + L(xm, y2, x2, y2, c, sw)


def chain_steps(x, y, vals, step=110, r=18, deltas=None, cap=None):
    """链式递减：圆节点+箭头（存活/收敛类叙事）。首节点白底 ACC 描边（唯一蓝）。
    cap=('文案') 末端深墨胶囊。返回 svg 字符串。"""
    s = ""
    for i, v in enumerate(vals):
        cx = x + i*step
        if i == 0:
            s += f'<circle cx="{cx}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="{ACC}" stroke-width="2.6"/>'
            s += T(cx, y+5, str(v), 13, INK1, w=700, fam=MONO, anchor="middle")
        else:
            s += f'<circle cx="{cx}" cy="{y}" r="{r}" fill="{INK1}"/>'
            s += T(cx, y+5, str(v), 13, "#FFFFFF", w=700, fam=MONO, anchor="middle")
        if i < len(vals)-1:
            s += L(cx+r+4, y, cx+step-r-12, y, GRAY_A, 2.2) + _arrhead(cx+r+4, y, cx+step-r-10, y, GRAY_A, 8)
            if deltas:
                s += T(cx+step/2, y-12, str(deltas[i]), 10, INK2, w=700, fam=MONO, anchor="middle")
    if cap:
        ex = x + (len(vals)-1)*step + r + 18
        s += f'<rect x="{ex}" y="{y-17}" width="104" height="34" rx="17" fill="{INK1}"/>'
        s += T(ex+52, y+5, cap, 12.5, "#FFFFFF", w=700, anchor="middle")
    return s


# -------------------------------------------------------------------- v2.7 追加
def driver_op(cx, cy, op, r=11, c=INK1):
    """驱动树算子记号（G-90 可选专业度升级）：在肘线汇合处标 ×/÷/+/- 运算。
    纯线画（圆 + line/圆点），不用文字字形，规避 tofu。
    注意（对标评估实证）：真实咨询驱动树仅 ~4% 显式建模算子——默认不加，
    仅当页面主论点就是「公式分解」时使用。op ∈ 'x' '/' '+' '-'。"""
    op = {"×": "x", "÷": "/", "−": "-"}.get(op, op)
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{c}" stroke-width="1.6"/>'
    a = r * 0.48
    if op == "x":
        s += L(cx - a, cy - a, cx + a, cy + a, c, 2) + L(cx - a, cy + a, cx + a, cy - a, c, 2)
    elif op == "+":
        s += L(cx - a, cy, cx + a, cy, c, 2) + L(cx, cy - a, cx, cy + a, c, 2)
    elif op == "-":
        s += L(cx - a, cy, cx + a, cy, c, 2)
    elif op == "/":
        s += L(cx - a, cy, cx + a, cy, c, 2)
        s += f'<circle cx="{cx}" cy="{cy-a*0.95:.1f}" r="1.8" fill="{c}"/>'
        s += f'<circle cx="{cx}" cy="{cy+a*0.95:.1f}" r="1.8" fill="{c}"/>'
    else:
        raise ValueError("op 仅支持 'x' '/' '+' '-'")
    return s
