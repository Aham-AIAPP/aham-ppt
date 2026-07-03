#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""渲染双档主题样张（A 克制 / B 现代专业）到 assets/shots/，供 README「视觉档」节展示。
依赖 assets/components/themes.py + playwright。运行：python3 tools/build_theme_samples.py
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "assets" / "components"))
import themes  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

CH = [("01", "现状诊断", "基准对标与停机根因", "clipboard"),
      ("02", "改善方案", "选型对照与体系架构", "layers"),
      ("03", "实施路径", "90 天三阶段落地", "route"),
      ("04", "保障机制", "责任矩阵与复盘", "shield")]
COVER = dict(brand="Aham", title="三条产线运营诊断", subtitle="OEE 71%→85% 的 90 天改善路径",
             chapters=CH, meta_left="受众：工厂管理层 · 日期：2026-06-22", meta_right="机密 · 仅限内部")

SAMPLES = {
    "theme-a-cover": themes.cover("A", **COVER),
    "theme-b-cover": themes.cover("B", **COVER),
    "theme-c-cover": themes.cover_dark(**COVER),
    "theme-b-toc": themes.toc("B", CH),
    "theme-b-section": themes.section("B", "02", "改善方案", "选型对照与体系架构",
                                      items=[("grid", "方案选型对照"), ("layers", "三层体系架构"), ("route", "实施路线")]),
}

SHOTS = ROOT / "assets" / "shots"
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap">')
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=2)
    for name, svg in SAMPLES.items():
        html = (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}'
                '<style>html,body{margin:0;padding:0}svg{display:block}</style></head>'
                f'<body>{svg}</body></html>')
        pg.set_content(html, wait_until="networkidle")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(450)
        pg.screenshot(path=str(SHOTS / f"{name}.png"), clip={"x": 0, "y": 0, "width": 1280, "height": 720})
        print("shot:", name)
    b.close()
print("→", SHOTS)
