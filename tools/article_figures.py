#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公众号文章配图生成器（Aham PPT v2.0 发布）。
一次性发版脚本，与技能运行时无关。
统一用 Aham UI v6.1 视觉：三层灰 + 蓝是点缀 + 无衬线 + 数字 mono。
产出：封面 + 品牌矩阵 + 新旧对比 + 重型流水线，渲染成 2x PNG。
依赖：playwright（已装）。运行：python3 tools/article_figures.py
输出目录：默认 ./tools/out/article-figures/，可用环境变量 AHAM_OUT_DIR 覆盖。
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

SANS = "Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif"
MONO = "'JetBrains Mono', Consolas, monospace"
INK1, INK2, INK3, INK4 = "#262626", "#6E6E6E", "#9B9B9B", "#C4C4C4"
LINE, PANEL, ACC, ACC2 = "#E7E7E7", "#F3F3F3", "#336EE8", "#164EC3"
OK, WARN, RISK = "#5A7A60", "#8A7333", "#9E3D31"
# 旧版（v1.x）配色，仅用于"之前长这样"的对比缩略图
O_BLUE, O_BORDER, O_TINT, O_INK = "#1677FF", "#E2E2E2", "#E8F0FA", "#1A1A1A"

def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def T(x, y, s, size=14, fill=INK1, w=None, anchor=None, ff=SANS, ls=None):
    a = f' text-anchor="{anchor}"' if anchor else ""
    wt = f' font-weight="{w}"' if w else ""
    lss = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x}" y="{y}" font-family="{ff}" font-size="{size}"{wt}{a}{lss} fill="{fill}">{esc(s)}</text>'
def M(x, y, s, size=14, fill=INK1, w=None, anchor=None): return T(x, y, s, size, fill, w, anchor, ff=MONO)
def L(x1, y1, x2, y2, stroke=LINE, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
def R(x, y, w, h, fill, rx=None, stroke=None, sw=None):
    r = f' rx="{rx}"' if rx is not None else ""
    st = f' stroke="{stroke}" stroke-width="{sw or 1}"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}"{r} fill="{fill}"{st}/>'
def CIR(cx, cy, r, fill): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
def svg(body, w, h):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg">\n' + "\n".join(body) + "\n</svg>\n")

figs = {}  # name -> (svg, w, h)

# ════════════════ 封面 1410×600（≈2.35:1，公众号头图）════════════════
def cover():
    W, H = 1410, 600
    e = [R(0, 0, W, H, "#FFFFFF")]
    e += [R(80, 70, 14, 14, ACC, rx=3), T(106, 88, "Aham", 24, INK1, w=700),
          T(180, 88, "· 应用矩阵", 16, INK3)]
    e.append(T(80, 214, "克制的 AI 演示制作技能", 15, INK3, ls=3))
    e.append(T(76, 326, "Aham PPT", 96, INK1, w=700))
    e.append(R(556, 256, 92, 58, PANEL, rx=10))
    e.append(T(602, 296, "2.0", 30, ACC, w=700, anchor="middle"))
    e.append(T(80, 398, "把一堆素材，跑成完整方案。", 30, INK2))
    e.append(R(82, 426, 120, 4, ACC))
    # 右侧：新样式迷你看板缩略
    bx, by, bw, bh = 936, 150, 404, 300
    e.append(R(bx, by, bw, bh, "#FFFFFF", rx=12, stroke=LINE, sw=1))
    e.append(R(bx + 24, by + 26, 9, 9, ACC, rx=2))
    e.append(T(bx + 24, by + 56, "综合效率 71.2%", 15, INK1, w=600))
    e.append(L(bx + 24, by + 70, bx + bw - 24, by + 70))
    for i, (lab, val, c) in enumerate([("OEE", "71.2", RISK), ("达成", "86.4", WARN), ("良率", "93.5", OK)]):
        cx = bx + 24 + i * 122
        e.append(T(cx, by + 100, lab, 11, INK3))
        e.append(M(cx, by + 128, val, 26, INK1, w=700))
        e.append(CIR(cx + 4, by + 146, 3, c))
    e.append(L(bx + 24, by + 168, bx + bw - 24, by + 168))
    for i, (a, v, c) in enumerate([("冲压线 A", "82.0%", WARN), ("焊装线 B", "68.4%", RISK), ("总装线 C", "73.0%", WARN)]):
        ry = by + 196 + i * 30
        e.append(T(bx + 24, ry, a, 12, INK1))
        e.append(M(bx + bw - 80, ry, v, 12, INK1, anchor="end"))
        e.append(CIR(bx + bw - 44, ry - 4, 3, c))
        e.append(L(bx + 24, ry + 10, bx + bw - 24, ry + 10, LINE, 0.75))
    e.append(L(80, 520, W - 80, 520))
    e.append(T(80, 552, "v2.0 · 视觉层换血 · 三层灰 · 蓝是点缀 · 告别 AI 味三卡片", 15, INK3))
    e.append(M(W - 80, 552, "github.com/Aham-AIAPP/aham-ppt", 14, INK3, anchor="end"))
    return svg(e, W, H), W, H
figs["cover"] = cover()

# ════════════════ 品牌矩阵 1280×520 ════════════════
def brand():
    W, H = 1280, 520
    e = [R(0, 0, W, H, "#FFFFFF")]
    e += [R(60, 56, 13, 13, ACC, rx=3), T(84, 73, "Aham", 22, INK1, w=700)]
    e.append(T(60, 130, "把灵光一现，做成能用的 AI 工具", 32, INK1, w=700))
    e.append(T(60, 168, "Aham 来自 aha moment。每个工具只把一件事做利落。", 17, INK2))
    apps = [("Aham UI", "设计系统", "写一次规范，AI 产出处处一致", False),
            ("Aham Survey", "现场调研 · macOS", "聊一圈，调研结果自己长出来", False),
            ("Aham Voice", "录音转写 · macOS", "录一段会，纪要已经写好", False),
            ("Aham PPT", "演示制作技能", "丢一堆素材，幻灯片出来了", True)]
    cw = (W - 120 - 3 * 20) / 4
    for i, (name, cat, line, hi) in enumerate(apps):
        x = 60 + i * (cw + 20)
        e.append(R(x, 220, cw, 230, PANEL, rx=12))
        if hi:
            e.append(R(x, 220, 3, 230, ACC, rx=1.5))
            e.append(T(x + cw - 18, 252, "本文", 12, ACC, w=600, anchor="end"))
        e.append(M(x + 20, 268, f"0{i+1}", 18, INK4, w=700))
        e.append(T(x + 20, 320, name, 21, INK1, w=700))
        e.append(T(x + 20, 348, cat, 13, INK3))
        e.append(T(x + 20, 392, line, 14, INK2))
        if i < 3:
            e.append(T(x + cw + 4, 340, "·", 18, INK4, anchor="middle"))
    e.append(T(60, 496, "Aham PPT 是这一系列里专做「演示」的应用。", 14, INK3))
    return svg(e, W, H), W, H
figs["brand"] = brand()

# ════════════════ 新旧对比 1280×760 ════════════════
def before_after():
    W, H = 1280, 760
    e = [R(0, 0, W, H, "#FFFFFF")]
    e += [R(1188, 16, 9, 9, ACC, rx=2), T(1240, 24, "Aham", 12, INK1, w=600, anchor="end"),
          T(40, 24, "v2.0 · 这次主要换了视觉层", 11, INK3, ls=1), L(40, 32, 1240, 32)]
    e.append(T(40, 78, "从 AI 味三卡片，到「冷色的纸」", 32, INK1, w=700))
    e.append(L(40, 94, 1240, 94))
    # 标签
    e.append(T(60, 134, "旧 · v1.x", 16, RISK, w=700))
    e.append(T(60, 156, "整页铺蓝 · 三卡片并列 · 描边大卡", 13, INK3))
    e.append(T(670, 134, "新 · v2.0", 16, ACC, w=700))
    e.append(T(670, 156, "蓝只点缀 · 文档表 + 留白 · 无边框", 13, INK3))
    # ── 旧缩略（550×250 @ 60,176）AI 味
    ox, oy, ow, oh = 60, 176, 550, 250
    e.append(R(ox, oy, ow, oh, "#FFFFFF", rx=8, stroke=O_BORDER, sw=1))
    e.append(R(ox, oy, ow, 5, O_BLUE))  # 顶部蓝条
    e.append(R(ox + 20, oy + 26, 4, 22, O_BLUE))  # 蓝竖线
    e.append(T(ox + 32, oy + 44, "现状分析", 17, O_INK, w=700, ff="serif"))
    for i in range(3):  # 三卡片并列
        cx = ox + 20 + i * 172
        e.append(R(cx, oy + 64, 156, 150, "#FFFFFF", rx=4, stroke=O_BORDER, sw=1))
        e.append(T(cx + 12, oy + 88, ["效率", "停机", "质量"][i], 13, O_BLUE, w=700))
        for k in range(3):
            e.append(R(cx + 12, oy + 104 + k * 22, 3, 13, O_BLUE))
            e.append(L(cx + 22, oy + 110 + k * 22, cx + 140, oy + 110 + k * 22, O_BORDER, 1))
    e.append(R(ox + 20, oy + 222, ow - 40, 18, O_TINT, rx=3, stroke=O_BLUE, sw=1))  # 浅蓝callout
    # ── 新缩略（550×250 @ 670,176）
    nx, ny, nw, nh = 670, 176, 550, 250
    e.append(R(nx, ny, nw, nh, "#FFFFFF", rx=8, stroke=LINE, sw=1))
    e.append(T(nx + 24, ny + 40, "现状分析", 17, INK1, w=700))
    e.append(L(nx + 24, ny + 52, nx + nw - 24, ny + 52, LINE, 1))
    for i, (lab, val, c) in enumerate([("综合效率", "71.2", RISK), ("计划达成", "86.4", WARN), ("一次良率", "93.5", OK)]):
        cx = nx + 24 + i * 168
        e.append(T(cx, ny + 78, lab, 11, INK3))
        e.append(M(cx, ny + 104, val, 24, INK1, w=700))
        e.append(CIR(cx + 4, ny + 120, 3, c))
    e.append(L(nx + 24, ny + 140, nx + nw - 24, ny + 140, LINE, 1))
    for i, (a, v) in enumerate([("冲压线 A", "82.0%"), ("焊装线 B", "68.4%"), ("总装线 C", "73.0%")]):
        ry = ny + 166 + i * 26
        e.append(T(nx + 24, ry, a, 12, INK1))
        e.append(M(nx + nw - 30, ry, v, 12, INK1, anchor="end"))
        e.append(L(nx + 24, ry + 8, nx + nw - 24, ry + 8, LINE, 0.75))
    # ── 对比表
    e.append(L(40, 470, 1240, 470))
    cols = [("", 40), ("旧 · v1.x", 470), ("新 · v2.0", 860)]
    e.append(T(470, 506, "旧 · v1.x", 14, INK3, w=600))
    e.append(T(860, 506, "新 · v2.0", 14, ACC, w=600))
    e.append(L(40, 520, 1240, 520, LINE, 1.2))
    diffs = [("主色", "整页铺 #1677FF 科技蓝", "蓝是点缀，绝不铺底"),
             ("结构", "三大卡片并列（AI 味）", "文档式表格 + 留白分隔"),
             ("卡片", "描边大白卡 + 浅蓝 callout", "无边框无阴影，靠层差"),
             ("字体", "衬线标题 + 思源宋体", "单一无衬线 + 数字 mono"),
             ("状态", "色块 / 红黄绿灯", "6px 点 + 文字，双通道")]
    ry = 556
    for dim, old, new in diffs:
        e.append(T(40, ry, dim, 15, INK2, w=600))
        e.append(T(470, ry, old, 15, INK2))
        e.append(CIR(864, ry - 5, 3, ACC))
        e.append(T(880, ry, new, 15, INK1))
        e.append(L(40, ry + 16, 1240, ry + 16, LINE, 0.75))
        ry += 40
    return svg(e, W, H), W, H
figs["before-after"] = before_after()

# ════════════════ 重型流水线 1280×840 ════════════════
def workflow():
    W, H = 1280, 840
    e = [R(0, 0, W, H, "#FFFFFF")]
    e += [R(1188, 16, 9, 9, ACC, rx=2), T(1240, 24, "Aham", 12, INK1, w=600, anchor="end"),
          T(40, 24, "工作流 · 它不是排版工具", 11, INK3, ls=1), L(40, 32, 1240, 32)]
    e.append(T(40, 78, "重点不在「编辑幻灯片」，在把方案想清楚、讲明白", 32, INK1, w=700))
    e.append(L(40, 94, 1240, 94))
    # 输入/输出
    e.append(R(40, 124, 250, 56, PANEL, rx=10))
    e.append(T(60, 150, "输入", 12, INK3)); e.append(T(60, 168, "一堆素材：文字/数据/PDF", 13, INK1))
    e.append(R(990, 124, 250, 56, "#FFFFFF", rx=10, stroke=ACC, sw=1.5))
    e.append(T(1010, 150, "输出", 12, ACC)); e.append(T(1010, 168, "原生可编辑 PPT", 13, INK1, w=600))
    phases = [("01", "规范加载", "色值/字体/禁用清单"), ("02", "材料解析", "提取关键信息与证据"),
              ("03", "论点提炼", "金字塔原理"), ("04", "叙事骨架", "Ghost Deck 一页一句"),
              ("05", "大纲版式", "规划 Part 与版式"), ("06", "样稿确认", "与你对齐视觉方向"),
              ("07", "逐页设计", "SVG → 原生 PPTX"), ("08", "质检交付", "QC 清单逐项扫")]
    cw, gap, y0 = 278, 26, 220
    pos = []
    for i, (num, name, sub) in enumerate(phases):
        row, col = divmod(i, 4)
        x = 40 + col * (cw + gap); y = y0 + row * 196
        pos.append((x, y))
        e.append(R(x, y, cw, 150, PANEL, rx=12))
        e.append(M(x + 18, y + 42, num, 22, INK4, w=700))
        e.append(T(x + 70, y + 42, name, 19, INK1, w=600))
        e.append(L(x + 18, y + 62, x + cw - 18, y + 62, LINE, 1))
        e.append(T(x + 18, y + 96, sub, 14, INK2))
        if col < 3:  # 行内箭头
            ax = x + cw
            e.append(L(ax + 6, y + 75, ax + gap - 10, y + 75, INK3, 2))
            e.append(f'<polygon points="{ax+gap-10},{y+70} {ax+gap-2},{y+75} {ax+gap-10},{y+80}" fill="{INK3}"/>')
    # 行间折返箭头（行1末 → 行2首）
    x_end = pos[3][0] + cw / 2; x_start = pos[4][0] + cw / 2
    midy = y0 + 150 + 23
    e.append(L(x_end, y0 + 150, x_end, midy, INK3, 1.5))
    e.append(L(x_end, midy, x_start, midy, INK3, 1.5))
    e.append(L(x_start, midy, x_start, y0 + 196, INK3, 1.5))
    e.append(f'<polygon points="{x_start-5},{y0+196-8} {x_start},{y0+196} {x_start+5},{y0+196-8}" fill="{INK3}"/>')
    # 底部一句
    e.append(L(40, 690, 1240, 690))
    e.append(CIR(44, 731, 3, ACC))
    e.append(T(60, 737, "内置教练引擎（按你的水平自适应）、必问探测场景、质检协议——保证关键节点不漏、硬判断不被软化。", 16, INK1))
    e.append(T(60, 786, "v2.0 换的是上面这条流水线的「视觉层」；方法论内核、八阶段、触发方式都没变。", 15, INK3))
    return svg(e, W, H), W, H
figs["workflow"] = workflow()

# ════════════════ 渲染输出 ════════════════
# 默认写到仓库内 tools/out/（不锚定某人桌面）；可用 AHAM_OUT_DIR 覆盖。
OUTP = Path(os.environ.get("AHAM_OUT_DIR", Path(__file__).resolve().parent / "out" / "article-figures"))
OUTP.mkdir(parents=True, exist_ok=True)
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap">')
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, (s, w, h) in figs.items():
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        html = (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}'
                '<style>html,body{margin:0;padding:0}svg{display:block}</style></head>'
                f'<body>{s}</body></html>')
        pg.set_content(html, wait_until="networkidle")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(450)
        pg.screenshot(path=str(OUTP / f"{name}.png"), clip={"x": 0, "y": 0, "width": w, "height": h})
        pg.close()
        print("fig:", name, f"{w}x{h}")
    b.close()
print("→", OUTP)
