# -*- coding: utf-8 -*-
"""
SVG 渲染预检（防坑） —— 在批量渲染前 / 组装 PPTX 前跑一次。
用法：python lint_svg.py <svg目录>

检查五类高频坑（均来自实战复盘）：
1. tofu 高危字符：✕ ✓ ✗ ①-⑩ ↕ ☀ 等在等宽/无字形字体里会渲染成空心方块 □。
   → 对错请用 √(U+221A) / ×(U+00D7) 或画 path；序号用 圆圈+阿拉伯数字；勿把这些字符放进 MONO 文本。
2. 页脚总页数是否全册一致（避免出现 /50 与 /57 并存）。
3. 源码中文双引号 “” —— 会截断 Python 字符串导致 SyntaxError（请改用「」）。需配合传入 .py 目录用 --py。
4. rotate/负 scale 变换 —— svg_to_pptx 转换后元素漂移（designer-rules 约束7），任何元素禁用。
5. 文本精确超宽 —— 按 字符宽×字号 估算右界（CJK=1em，ASCII≈0.55em，含 letter-spacing 与 anchor），
   超出内容区红线 x>1242 才报（取代转换器"每行>20 CJK"的保守提示）。
"""
import sys, re, glob, os

RISK = ['✕', '✓', '✗', '↕', '☀', '✦', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩',
        '⑪', '⑫', '⑬', '⑭', '⑮', '㉕', '㉖', '㉗', '½', '¼', '∨']

def lint_svg_dir(d):
    svgs = sorted(glob.glob(os.path.join(d, '*.svg')))
    totals = {}
    risky = []
    for p in svgs:
        t = open(p, encoding='utf-8').read()
        hit = sorted(set(c for c in RISK if c in t))
        if hit:
            risky.append((os.path.basename(p), hit))
        for m in re.findall(r'>\s*\d+\s*/\s*(\d+)\s*<', t):  # 页脚 "x / N"
            totals.setdefault(m, []).append(os.path.basename(p))
    print(f"扫描 {len(svgs)} 个 SVG @ {d}")
    print("=== tofu 高危字符 ===")
    if risky:
        for n, h in risky:
            print(f"  [!] {n}: {' '.join(h)}")
    else:
        print("  无")
    print("=== rotate/负 scale 变换 ===")
    rot = []
    for p in svgs:
        t = open(p, encoding='utf-8').read()
        if re.search(r'transform="[^"]*(rotate\(|scale\(-)', t):
            rot.append(os.path.basename(p))
    print("  " + ("、".join(rot) + " ← 转换后会漂移，禁用" if rot else "无"))
    print("=== 文本精确超宽（右界>1242）===")
    ow = []
    for p in svgs:
        t = open(p, encoding='utf-8').read()
        for m in re.finditer(r'<text ([^>]*)>([^<]*)</text>', t):
            attrs, txt = m.group(1), m.group(2)
            gx = re.search(r'\bx="([\d.]+)"', attrs)
            gs = re.search(r'font-size="([\d.]+)"', attrs)
            if not gx or not gs or not txt.strip():
                continue
            xx, fs = float(gx.group(1)), float(gs.group(1))
            ls = float((re.search(r'letter-spacing="([\d.]+)"', attrs) or [None, "0"])[1])
            wd = sum(fs if ord(c) > 0x2E00 else fs * 0.55 for c in txt) + ls * max(0, len(txt) - 1)
            anc = (re.search(r'text-anchor="(\w+)"', attrs) or [None, "start"])[1]
            right = xx + (wd if anc == "start" else wd / 2 if anc == "middle" else 0)
            if right > 1242:
                ow.append(f"{os.path.basename(p)}: x={xx:.0f} fs={fs:.0f} 估右界{right:.0f} 「{txt[:14]}…」")
    print("\n".join("  [!] " + o for o in ow) if ow else "  无")

    print("=== 形状越界（rect/polygon 超内容区 x>1242 或 y>692）===")
    ob = []
    for p in svgs:
        t = open(p, encoding='utf-8').read()
        for m in re.finditer(r'<rect ([^>]*?)/?>', t):
            attrs = m.group(1)
            gx = re.search(r'\bx="([\d.-]+)"', attrs); gy = re.search(r'\by="([\d.-]+)"', attrs)
            gw = re.search(r'width="([\d.]+)"', attrs); gh = re.search(r'height="([\d.]+)"', attrs)
            if not (gw and gh):
                continue
            x = float(gx.group(1)) if gx else 0.0; y = float(gy.group(1)) if gy else 0.0
            w = float(gw.group(1)); h = float(gh.group(1))
            if w >= 1270 and h >= 710:
                continue  # 整页背景（含 C 档深底）豁免
            if x + w > 1242 or y + h > 692:
                ob.append(f"{os.path.basename(p)}: rect x={x:.0f} y={y:.0f} 右界{x+w:.0f} 底界{y+h:.0f}")
        for m in re.finditer(r'<polygon points="([^"]+)"', t):
            pts = re.findall(r'([\d.]+)[, ]([\d.]+)', m.group(1))
            if pts:
                mx = max(float(a) for a, _b in pts); my = max(float(_b) for a, _b in pts)
                if mx > 1242 or my > 692:
                    ob.append(f"{os.path.basename(p)}: polygon 右界{mx:.0f} 底界{my:.0f}")
    print("\n".join("  [!] " + o for o in ob) if ob else "  无")
    print("=== 页脚总页数 ===", end=" ")
    if not totals:
        print("一致：（未发现页脚）"); return
    # 众数为总页数；少数派若 N≤20 且仅出现在 ≤8 页，判为 themes.section 章节进度（如 01/07），豁免（v4.0：2→8，多章 deck 章节页数可达 8）
    main = max(totals, key=lambda k: len(totals[k]))
    odd = {k: v for k, v in totals.items() if k != main}
    exempt = {k: v for k, v in odd.items() if int(k) <= 20 and len(v) <= 8}
    real = {k: v for k, v in odd.items() if k not in exempt}
    msg = f"一致：{main}"
    if exempt:
        msg += "（豁免章节进度 " + "；".join(f"{k}: {','.join(v)}" for k, v in exempt.items()) + "）"
    print(msg if not real else f"⚠ 不一致 主={main} 异常={real}")

def lint_py_quotes(d):
    print("=== 源码中文双引号（会致 SyntaxError）===")
    bad = []
    for p in sorted(glob.glob(os.path.join(d, '*.py'))):
        t = open(p, encoding='utf-8').read()
        if '“' in t or '”' in t:
            bad.append(os.path.basename(p))
    print("  " + ("、".join(bad) + " ← 请改「」" if bad else "无"))

if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    lint_svg_dir(d)
    if '--py' in sys.argv:
        lint_py_quotes(d)
