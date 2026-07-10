#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aham-ppt 版式总览长图（1080 宽，Aham UI v6.1 风格）→ assets/shots/layout-catalog.png。
版式增减后重跑本脚本即可更新 README 配图。
数据源：references/layout-library.md + svg-skeleton-*.md 来源栏（如实转录，不虚构）。"""
from pathlib import Path

SANS = "Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif"
MONO = "'JetBrains Mono', Consolas, monospace"
INK1, INK2, INK3, INK4 = "#262626", "#6E6E6E", "#9B9B9B", "#C4C4C4"
LINE, PANEL, ACC = "#E7E7E7", "#F3F3F3", "#336EE8"
W, MX = 1080, 56  # 画布宽 / 左右边距

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def T(x, y, s, size=14, fill=INK1, w=None, fam=SANS, anchor="start", ls=None):
    a = f' font-weight="{w}"' if w else ""
    an = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}"{a}{an}{l}>{esc(s)}</text>'

# (系, 名称, 叙事功能, [(ID, 版式名, 用途, 来源)])
FAMS = [
("I", "Impact · 震撼", "冲击型密集页（大数字/宣言页已退库直排）", [
 ("I-90", "链式递减", "收敛 / 淘汰 / 漏斗到 1", "MBB 密集页形体语言"),
]),
("S", "Structure · 结构", "并列要点、矩阵、时间轴、对比", [
 ("S-02", "2×2 矩阵", "定性四象限；定量落位 + 迁移箭头用高阶变体（GE 九宫格）", "BCG 增长份额矩阵谱系"),
 ("S-07", "HERO 结论+支撑", "结论先行 + 2/3/4 条证据支撑（支撑数硬拦）", "Minto 金字塔原理 1996 版"),
 ("S-09", "KPI 看板", "速览用轻量六格；正式经营看板用「值+基准+趋势」卡", "Stephen Few 仪表盘设计"),
 ("S-13", "勾选式现状盘点", "成就清单 + 论据 + KPI 期比（年度回顾 / investor day 页型）", "MBB 盘点页惯例（推导）"),
 ("S-14", "团队页", "人像占位 + 姓名/职务网格，2–8 人硬拦（照片占位不硬编）", "B2B 方案团队页惯例（推导）"),
 ("S-15", "报价/条款页", "报价明细三线表，1–8 行硬拦；合计由调用方传入，函数绝不求和", "brand 表格规范的表格式落地"),
 ("S-16", "Harvey Balls 评估表", "供应商选型 / 成熟度五档评估（0–4 硬拦 + 图例）", "Poppel @ Booz Allen 1970s"),
 ("S-17", "竞争格局定位图", "双轴 + 弧带 + 气泡（去品牌化；商标纪律）", "结构对标 Forrester Wave 2002"),
]),
("E", "Explain · 说明", "图文结合、流程、概念曲线、架构", [
 ("E-02", "概念曲线", "单条趋势 / 阶段跃升 / 当前位置", "通用惯例 · 配色为本库设计"),
 ("E-03", "流程示意", "实施步骤、执行流程、价值链", "通用流程图惯例"),
 ("E-04", "架构层次", "轻量三层概念；真实 IT 架构用高阶变体（制造业售前核心）", "TOGAF 四域分层"),
 ("E-05", "价值链条带图", "主活动雪佛龙带 + 支持条 + 利润尖角", "Porter 1985"),
 ("E-90", "雪佛龙阶段链", "阶段推进且每段带一个量", "MBB 密集页形体语言"),
 ("E-91", "三地平线", "3–4 条 S 曲线错峰接力（时间×价值）", "Baghai/Coley/White 1999"),
]),
("V", "Evidence · 证据", "数据图表、趋势、量化对比", [
 ("V-02", "单大图表", "一张图表就是核心证据（15 类图表 charts.py 直调）", "Zelazny 五图体系"),
 ("V-03", "趋势折线", "洞察直接标在图上（引线贴数据点，≤3 处）", "Knaflic《用数据讲故事》"),
 ("V-04", "双图对比", "两组完整图表并排对比", "同 V-03（Knaflic 标注纪律）"),
 ("V-05", "小倍数网格", "4–12 个同构小图（共享尺度函数强制）", "Tufte 1983"),
 ("V-90", "流向带", "多来源汇成一个总量，带宽∝数值（守恒纪律）", "Sankey 谱系单层简化"),
 ("V-91", "哑铃对比", "两时点 / 两方案逐指标对比（按差值排序）", "dumbbell 连线点图惯例"),
 ("V-92", "点阵机制", "名额 / 晋级 / 配额类规则", "waffle · 点阵谱系"),
 ("V-93", "推算逻辑双栏", "小样本推总体：抽样表 → 显式乘数桥 → 外推表", "BCG 达拉斯推算页（最强单一原型）"),
 ("V-94", "Marimekko", "规模 × 构成双维度市场地图（列宽∝总量）", "Hartigan & Kleiner 1981"),
]),
("A", "Action · 动作", "决策、下一步、责任与路线", [
 ("A-03", "责任矩阵", "轻量行动清单；正式分工用标准 RACI（每行唯一 A）", "RACI 无单一发明人 · 1970s 通行"),
 ("A-04", "Impact-Effort 矩阵", "举措优先级排序（速赢象限）", "通用优先级工具族，无单一原版"),
 ("A-05", "决策树", "多阶段 + 概率 + 期望值（EV 不代算）", "Magee, HBR 1964"),
 ("A-90", "阶段×泳道路线图", "3–6 条 workstream + Today 线，甘特/相位/分桶三模式", "BCG 分桶 + 泳道最佳实践调研"),
 ("A-91", "FTE 人力爬坡", "波次堆叠人力随时间爬坡 + stage-gate 决策门", "Cooper Stage-Gate 1988"),
]),
("G", "Graph · 结构图", "树状分解、支柱、金字塔", [
 ("G-01", "issue tree", "定性问题分解：分层严格对齐 + 分支 MECE 分隔", "麦肯锡 issue tree 规范"),
 ("G-04", "鱼骨图", "制造业质量根因（6M；子因水平文字）", "Ishikawa 1960s · ASQ"),
 ("G-03", "层级金字塔", "纯层级堆叠（3–5 层，纯层名）", "通用商务惯例"),
 ("G-90", "驱动树", "指标数学分解且节点带数值（可选算子 ×÷+−）", "DuPont/ROIC 分解 + VDMN"),
 ("G-91", "论证阶梯", "2–4 个 MECE 论点逐级累加收敛到结论", "Minto 金字塔原理"),
 ("G-92", "服务蓝图", "服务旅程前后台拆解：固定 5 泳道 + 3 分界线", "Shostack 1984 · HBR 原始文献"),
 ("G-93", "剖面金字塔", "定性层级 × 层内多要素切格 + 逐层 takeaway", "Bain 价值要素金字塔 2016"),
]),
]

e = []
y = 0
# ── 页眉 ──
y += 64
e.append(f'<rect x="{MX}" y="{y-11}" width="11" height="11" rx="3" fill="{ACC}"/>')
e.append(T(MX+22, y, "Aham PPT · 版式库", 15, INK1, 600))
e.append(T(W-MX, y, "v4.0 · 全量参数化", 13, INK3, fam=MONO, anchor="end"))
y += 22
e.append(f'<line x1="{MX}" y1="{y}" x2="{W-MX}" y2="{y}" stroke="{LINE}" stroke-width="1"/>')
# ── 标题 ──
y += 66
e.append(T(MX, y, "36 个版式，每一个都有出处", 34, INK1, 700))
y += 18
e.append(f'<rect x="{MX}" y="{y}" width="84" height="3" rx="1.5" fill="{ACC}"/>')
# 统计行
y += 46
stats = [("36", "内容版式"), ("6", "叙事系"), ("3", "特殊页"), ("15", "类数据图表"), ("14", "标注/异形 API")]  # 发版前对照组件实数，见 CONTRIBUTING 发版清单
sx = MX
for num, lab in stats:
    e.append(T(sx, y, num, 30, INK1, 700, fam=MONO))
    nw = len(num) * 19 + 8
    e.append(T(sx + nw, y, lab, 13, INK3))
    sx += nw + len(lab) * 13 + 40
# 引言
y += 40
for ln in ["版式按叙事功能分 6 系；全部参数化——坐标由函数冻结。16 个通用页型（大数字/宣言/两三栏等）已退库走栅格直排。",
           "来源两档如实标注：可考原型注明出处；查不到的明确标「通用惯例 / 本库自设计」，不虚构。"]:
    e.append(T(MX, y, ln, 14, INK2)); y += 24
y += 12

# ── 7 个系 ──
for fam, name, narr, rows in FAMS:
    y += 34
    e.append(T(MX, y, fam, 26, INK4, 700, fam=MONO))
    e.append(T(MX+44, y, name, 17, INK1, 600))
    e.append(T(MX+44+len(name)*17+16, y, narr, 13, INK3))
    e.append(T(W-MX, y, f"{len(rows)} 个", 13, INK3, fam=MONO, anchor="end"))
    y += 14
    e.append(f'<line x1="{MX}" y1="{y}" x2="{W-MX}" y2="{y}" stroke="{LINE}" stroke-width="1.2"/>')
    for i, (lid, lname, use, src) in enumerate(rows):
        y += 30
        e.append(T(MX, y, lid, 13, INK2, 600, fam=MONO))
        e.append(T(MX+64, y, lname, 15, INK1, 600))
        e.append(T(W-MX, y, src, 12, INK3, anchor="end"))
        y += 21
        e.append(T(MX+64, y, use, 13, INK2))
        y += 9
        if i < len(rows) - 1:
            e.append(f'<line x1="{MX+64}" y1="{y}" x2="{W-MX}" y2="{y}" stroke="{LINE}" stroke-width="0.6"/>')
    y += 8

# ── 版式之外：特殊页 + 标注层 ──
y += 36
e.append(f'<rect x="{MX}" y="{y-24}" width="{W-2*MX}" height="118" rx="12" fill="{PANEL}"/>')
e.append(T(MX+24, y+6, "版式之外", 15, INK1, 600))
y += 32
e.append(T(MX+24, y, "SPC 特殊页 · 3 个　封面 / 分隔 / 结尾——A 克制 · B 现代专业 · C 高表现三档皮肤（themes.py），共用同一份内容。", 13, INK2))
y += 26
e.append(T(MX+24, y, "标注层 D　椭圆圈注 / 引线 / 水印 / So-What / 线画对勾——可叠加到任意版式上，带密度与配额纪律。", 13, INK2))
y += 60

# ── 页脚 ──
e.append(f'<line x1="{MX}" y1="{y}" x2="{W-MX}" y2="{y}" stroke="{LINE}" stroke-width="1"/>')
y += 26
e.append(T(MX, y, "来源标注转录自各版式骨架文件「来源」栏 · 完整纪律见 references/", 11, INK3))
e.append(T(W-MX, y, "github.com/Aham-AIAPP/aham-ppt", 11, INK3, fam=MONO, anchor="end"))
y += 40

H = y
svg = (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
       f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>' + "".join(e) + '</svg>')

OUT = Path(__file__).resolve().parent.parent / "assets" / "shots"

from playwright.sync_api import sync_playwright
F = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
     'family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap">')
html = (f'<!doctype html><html><head><meta charset="utf-8">{F}'
        f'<style>html,body{{margin:0;padding:0}}svg{{display:block}}</style></head><body>{svg}</body></html>')
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": min(H, 1200)}, device_scale_factor=2)
    pg.set_content(html, wait_until="networkidle")
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
    pg.screenshot(path=str(OUT / "layout-catalog.png"), full_page=True)
    b.close()
print(f"H={H}px → {OUT}/layout-catalog.png")
