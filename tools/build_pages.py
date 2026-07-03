#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 aham-ppt / aham-survey / aham-voice 生成统一品牌落地页（GitHub Pages，docs/）。
Aham UI v6.1 视觉。每个仓库自带 docs/index.html + docs/banner.png（社交图副本）。
运行：python3 tools/build_pages.py [仓库名]
"""
import shutil
from pathlib import Path

DOCS = "/Users/lichengbao/Documents"
NAV = [("aham-ui", "Aham UI"), ("aham-survey", "Aham Survey"),
       ("aham-voice", "Aham Voice"), ("aham-ppt", "Aham PPT")]

SITES = {
    "aham-ppt": dict(dir="aham-ppt", name="Aham PPT", tag="克制的 AI PPT 制作技能", type="Claude Skill",
        sub="把零散素材做成方案级 / 报告级的专业 PPT。八步法 · 三档风格 · 原生可编辑 PPTX。",
        feats=[("八阶段流水线", "规范加载 → 材料解析 → 论点提炼 → … → 质检交付，不是排版美化"),
               ("原生可编辑 PPTX", "每个元素都是 PPT 原生形状 / 文本框，双击即改"),
               ("43 版式参数化", "21 个版式函数 + 9 类图表 + 结构 / 标注组件，坐标由函数冻结"),
               ("换成你的品牌", "改 tokens 主色 + 字体 + 品牌名，四步适配")],
        ctas=[("在 GitHub 查看", "https://github.com/li599198347-svg/aham-ppt", 1),
              ("历史样张（v2.5.2）", "https://github.com/li599198347-svg/aham-ppt/tree/v2.5.2/examples", 0),
              ("Releases", "https://github.com/li599198347-svg/aham-ppt/releases", 0)],
        shots=[("shots/consulting-tree.png", "驱动树 · 肘线分解 + 圈注 + 自洽校验"),
               ("shots/consulting-dots.png", "点阵去向 · 细分条 + 圈注"),
               ("shots/consulting-chain.png", "链式递减 · 节点链 + So-What 收口")],
        shot_wide=("shots/consulting-skin.png", "同一真源一键换肤 · Aham 蓝 ⇄ 黑·白·金三国色（v2.5 世界杯样张）")),
    "aham-survey": dict(dir="aham-survey", name="Aham Survey", tag="现场调研工具（macOS）", type="macOS App",
        sub="把现场对话做成可交付的结构化调研报告。结构化问卷 · 本地录音转写 · 自行配置 LLM Key 的 AI。",
        feats=[("项目制调研", "按客户 / 项目建调研，进行中 / 草稿 / 已完成 / 已归档"),
               ("行业 + 部门模板", "按调研范围（ERP / MES / WMS / PLM…）自动匹配部门与题目"),
               ("本地语音", "录音 + 本地 ASR 转写 + 说话人识别，一键填入当前题"),
               ("AI 增强（自行配置 LLM Key）", "记录润色、追问建议、文档分析、AI 搜索；支持主流 LLM")],
        ctas=[("在 GitHub 查看", "https://github.com/li599198347-svg/aham-survey", 1),
              ("下载（Releases）", "https://github.com/li599198347-svg/aham-survey/releases", 0)]),
    "aham-voice": dict(dir="aham-voice", name="Aham Voice", tag="录音转写与会议纪要（macOS）", type="macOS App",
        sub="把录音做成会议纪要，隐私留在本机。本地离线转写 · 说话人分离 · 纪要走你自己的模型。",
        feats=[("全本地离线转写", "FunASR + VAD + 标点 + 说话人分离（CAM++）+ 声学情绪"),
               ("AI 会议纪要", "云端大模型（OpenAI 兼容接口，比如 DeepSeek 等），Key 仅存本机"),
               ("单机开箱即用", "无登录、无多用户、无外部集成；DMG 内置全部模型"),
               ("热词与声纹", "热词手动 / txt 批量导入，声纹管理")],
        ctas=[("在 GitHub 查看", "https://github.com/li599198347-svg/aham-voice", 1),
              ("下载 DMG（Releases）", "https://github.com/li599198347-svg/aham-voice/releases", 0)]),
}

def nav_html(cur):
    parts = []
    for repo, label in NAV:
        if repo == cur:
            parts.append(f'<b>{label}</b>')
        else:
            parts.append(f'<a href="https://github.com/li599198347-svg/{repo}">{label}</a>')
    return ' <span class="sep">·</span> '.join(parts)

def page(repo, c):
    feats = "\n".join(
        f'<div class="feat"><div class="ft">{t}</div><div class="fd">{d}</div></div>' for t, d in c["feats"])
    ctas = "\n".join(
        f'<a class="btn {"pri" if p else "sec"}" href="{u}">{t}{" ↗" if not p else ""}</a>' for t, u, p in c["ctas"])
    shots_html = ""
    if c.get("shots"):
        cells = "\n".join(
            f'<figure class="shot"><img src="{p}" alt="{cap}" loading="lazy"><figcaption>{cap}</figcaption></figure>'
            for p, cap in c["shots"])
        if c.get("shot_wide"):
            p, cap = c["shot_wide"]
            cells += f'\n<figure class="shot wide"><img src="{p}" alt="{cap}" loading="lazy"><figcaption>{cap}</figcaption></figure>'
        shots_html = f'<h2 class="sh">样张</h2>\n  <div class="shots">\n{cells}\n  </div>\n  '
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{c['name']} — {c['tag']}</title>
<meta name="description" content="{c['sub']}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap">
<style>
  :root{{--w:#fff;--p:#F3F3F3;--line:#E7E7E7;--i1:#262626;--i2:#6E6E6E;--i3:#9B9B9B;--acc:#336EE8;--accp:#164EC3;
    --sans:'Inter','PingFang SC','Microsoft YaHei',sans-serif;--mono:'JetBrains Mono',Consolas,monospace;}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--w);color:var(--i1);font-family:var(--sans);line-height:1.6;-webkit-font-smoothing:antialiased}}
  .wrap{{max-width:880px;margin:0 auto;padding:32px 24px 72px}}
  nav{{font-size:14px;color:var(--i2);display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
  nav .d{{width:11px;height:11px;border-radius:3px;background:var(--acc);display:inline-block;margin-right:4px}}
  nav a{{color:var(--i2);text-decoration:none}} nav b{{color:var(--i1)}} nav .sep{{color:#C4C4C4}}
  .hero{{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:16px;margin:28px 0 24px}}
  h1{{font-size:30px;font-weight:700;letter-spacing:-.3px;margin:0 0 6px}}
  .sub{{font-size:17px;color:var(--i2);margin:0 0 24px;max-width:640px}}
  .cta{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:40px}}
  .btn{{display:inline-flex;align-items:center;font-size:15px;font-weight:600;text-decoration:none;border-radius:8px;padding:10px 18px}}
  .btn.pri{{background:var(--acc);color:#fff}} .btn.pri:hover{{background:var(--accp)}}
  .btn.sec{{background:var(--p);color:var(--i1)}}
  .feats{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:48px}}
  .feat{{background:var(--p);border-radius:12px;padding:18px 20px}}
  .feat .ft{{font-weight:600;font-size:16px}} .feat .fd{{color:var(--i2);font-size:14px;margin-top:6px}}
  .sh{{font-size:20px;font-weight:700;margin:0 0 16px}}
  .shots{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:48px}}
  .shot{{margin:0}} .shot.wide{{grid-column:1/-1}}
  .shot img{{width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:10px}}
  .shot figcaption{{font-size:12px;color:var(--i3);margin-top:6px}}
  footer{{border-top:1px solid var(--line);padding-top:20px;color:var(--i3);font-size:13px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}}
  footer a{{color:var(--i3);text-decoration:none}}
  @media(max-width:680px){{.feats{{grid-template-columns:1fr}}.shots{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
  <nav><span class="d"></span>{nav_html(repo)}</nav>
  <img class="hero" src="banner.png" alt="{c['name']} — {c['tag']}">
  <h1>{c['name']}</h1>
  <p class="sub">{c['sub']}</p>
  <div class="cta">
{ctas}
  </div>
  <div class="feats">
{feats}
  </div>
  {shots_html}<footer>
    <span>Aham · 把灵光一现，做成能用的 AI 工具</span>
    <span><a href="https://github.com/li599198347-svg/{repo}">github.com/li599198347-svg/{repo}</a></span>
  </footer>
</div></body></html>
"""

import sys
ONLY = sys.argv[1] if len(sys.argv) > 1 else None
for repo, c in SITES.items():
    if ONLY and repo != ONLY:
        continue
    repo_dir = Path(DOCS) / c["dir"]
    docs = repo_dir / "docs"; docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(page(repo, c), encoding="utf-8")
    shutil.copy(repo_dir / "assets" / "social-preview.png", docs / "banner.png")
    print(f"  {repo}: docs/index.html + docs/banner.png")
print("done")
