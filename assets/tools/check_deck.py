# -*- coding: utf-8 -*-
"""
方案 PPT 成品自查（读 .pptx，不改文件）—— Phase 8 交付前跑一次。
用法：
    python check_deck.py <方案.pptx> [--config 项目配置.json] [--out 报告.md]

规则出处：references/solution-deck.md §六。本脚本只做「机器能判的」那一半，
输出的「人工核对」各节要逐条对照页面看，脚本不替人下结论。

机器检查（ERROR / WARNING）
  1. 字号小于下限（默认 9pt，ERROR）；全册字号超过 8 级（WARNING）
  2. 页面用了 2 种以上强调色却找不到图例色块（WARNING，启发式）；配了色表时列出色表外的颜色（INFO）
  3. 页面文字一段里用逗号或分号连了两个分句
  4. 禁用词、口语词、观察词（页面与讲稿分开统计）
  5. 「第 N 页」引用超出总页数
  6. 内部编号（如 C01、A20）、代码标识符（如 search_knowledge）出现在页面上
  7. 同一组编号跳号（01、03、04）
  8. 术语表里的非标准写法
  9. 子标题不以句号结尾、超过 40 字；标题以句号结尾
 10. 页面上出现免费、赠送、折扣说法（ERROR）；出现金额（WARNING，业务数据可保留）。讲稿不查
 11. 数量用汉字数字写（如「三项」「五个」），应写阿拉伯数字（WARNING）
 12. 标题写成结论句（含「是」「能」「可以」「已」「将」等判断词，或长于 20 字）（WARNING）
 13. 配了语义色表时，页面用了色表外的强调色（WARNING）

人工核对清单（INFO，逐条看）
  - 标题与子标题一列（通读用）
  - 每处「第 N 页」引用及其指向页的标题
  - 全册带数量词的说法（N 项、N 个、N 类……），用于前后页数量对照
  - 每页用到的强调色，用于对照项目色表检查一色一义

配置文件（JSON，全部可选，缺省用下方 DEFAULTS）：
{
  "min_font": 9,                                  // 最小字号（pt）
  "max_levels": 8,                                // 全册字号层级上限，默认 8
  "palette": ["1F2633", "4A5363", ...],          // 可选：项目色表，色表外的颜色列为 INFO
  "banned": ["赋能", ...],                        // 追加到默认禁用词
  "watch": ["免费", "打样", "<其他客户名>"],       // 观察词：出现即列出，由人判断
  "terms": {"MOM（含 MES、WMS）": ["MOM系统", "制造运营系统"]},  // 标准名: [非标准写法]
  "internal_code": "\\b[A-Z]{1,2}\\d{2}\\b",     // 内部编号正则，可改
  "accents": {"336EE8": "AI", "17998A": "我方服务", "D4892A": "我方产品"}  // 语义色表：色值: 含义
}
"""
import sys, re, json, argparse, collections

try:
    from pptx import Presentation
    from pptx.util import Emu
except ImportError:  # pragma: no cover
    sys.exit("缺少 python-pptx：pip install python-pptx")

DEFAULTS = {
    "min_font": 9,
    "max_levels": 8,
    "palette": [],
    "banned": (
        "承接 赋能 沉淀 落地 抓手 闭环 粒度 颗粒度 归集 收敛 下沉 对位 波次 地基 命脉 灰度 旁路 水位 卡位 "
        "落库 对齐 原生 前置 全域 打通 颠覆 一站式 全链路 最佳实践 "
        "值得注意的是 需要指出的是 事实上 坦白说 总而言之 简而言之 一句话总结 "
        "撑不撑得住 对得起来 说不清 准不准 跟得上 划得来 值不值 一盘棋 一本账 全量检查"
    ).split(),
    # 口语词：方案页面不用，客户原话除外
    "colloquial": "干活 坐下来 兜底 露馅 放水 做砸 硬推 松口 长什么样 小工具 聊天窗口".split(),
    "watch": ["免费", "打样", "赠送", "价格", "待定", "待补充", "待现场确认"],
    "terms": {},
    "internal_code": r"(?<![A-Za-z0-9])[A-Z]{1,2}\d{2}(?![A-Za-z0-9])",
    "accents": {},
}

SNAKE = re.compile(r"\b[a-z]+(?:_[a-z0-9]+)+\b")          # search_knowledge
PAGE_REF = re.compile(r"第\s*(\d+)\s*(?:[—–-]\s*(\d+)\s*)?页")
QTY = re.compile(r"(\d+)\s*(项|个|类|条|步|层|组|台|人|款|种|批)")
SPLIT = re.compile(r"[，；;]|,(?!\d{3})")
SEQ = re.compile(r"^\s*0?(\d{1,2})\s*$")
PRICE = re.compile(r"(?:不|免)收费|免费|赠送|折扣|优惠价|报价\s*\d")
MONEY = re.compile(r"\d+(?:\.\d+)?\s*[万千百]?元|[¥￥]\s*\d|RMB")
CN_QTY = re.compile(r"(?<![第之一])([二三四五六七八九十两]|十[一二三四五六七八九])\s*(项|个|类|条|步|层|组|台|款|种|批|页|次|套)")
VERDICT = re.compile(r"是|(?<![功智性技])能(?!力)|可以|已经|已(?!有)|将|必须|应当|实现|提升|降低")


def load_cfg(path):
    cfg = {k: (list(v) if isinstance(v, list) else (dict(v) if isinstance(v, dict) else v))
           for k, v in DEFAULTS.items()}
    if path:
        user = json.load(open(path, encoding="utf-8"))
        for k, v in user.items():
            if k == "banned":
                cfg["banned"] += v
            elif k == "watch":
                cfg["watch"] += v
            else:
                cfg[k] = v
    cfg["palette"] = {c.upper().lstrip("#") for c in cfg["palette"]}
    return cfg


def is_accent(c):
    """饱和度和明度都够的颜色算强调色；灰、灰蓝、浅底不算。"""
    r, g, b = (int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    return mx > 0.35 and (mx - mn) / mx > 0.45 if mx else False


def iter_shapes(shapes):
    for sh in shapes:
        if sh.shape_type == 6:  # group
            yield from iter_shapes(sh.shapes)
        else:
            yield sh


def color_of(obj):
    try:
        if obj.type is not None and obj.rgb is not None:
            return str(obj.rgb).upper()
    except Exception:
        pass
    return None


def read_slide(slide, h):
    """返回 段落列表[(text, max_pt, top_ratio)]、字号计数、颜色计数、讲稿。"""
    paras, sizes, colors = [], collections.Counter(), collections.Counter()
    swatches = set()
    for sh in iter_shapes(slide.shapes):
        try:
            if sh.fill.type == 1:
                c = color_of(sh.fill.fore_color)
                if c:
                    colors[("填充", c)] += 1
                    # 图例色块：边长不超过 0.3 英寸的小方块或圆点
                    if c and (sh.width or 0) <= Emu(274320) and (sh.height or 0) <= Emu(274320):
                        swatches.add(c)
        except Exception:
            pass
        try:
            if sh.line.fill.type == 1:
                c = color_of(sh.line.color)
                if c:
                    colors[("线条", c)] += 1
        except Exception:
            pass
        if sh.shape_type == 13:  # 图片：图内颜色读不到，单独计数
            colors[("图片", "")] += 1
            continue
        top = (sh.top or 0) / h if h else 0
        frames = []
        if sh.has_text_frame:
            frames.append(sh.text_frame)
        if getattr(sh, "has_table", False) and sh.has_table:
            for row in sh.table.rows:
                for cell in row.cells:
                    frames.append(cell.text_frame)
        for tf in frames:
            for p in tf.paragraphs:
                text = "".join(r.text for r in p.runs).strip()
                if not text:
                    continue
                pmax = 0
                for r in p.runs:
                    if not r.text.strip():
                        continue
                    if r.font.size:
                        pt = round(r.font.size.pt, 2)
                        sizes[pt] += len(r.text)
                        pmax = max(pmax, pt)
                    c = color_of(r.font.color) if r.font.color else None
                    if c:
                        colors[("文字", c)] += len(r.text)
                paras.append((text, pmax, top))
    notes = ""
    if slide.has_notes_slide:
        notes = slide.notes_slide.notes_text_frame.text
    return paras, sizes, colors, notes, swatches


def guess_title(paras):
    """标题 = 页面上部 30% 内字号最大的段落；子标题 = 标题之后、上部 35% 内的第一段 12–20pt 文字。
    这是启发式判断，封面、章节页与特殊版式会猜错，报告里只作通读用。"""
    top = [(i, p) for i, p in enumerate(paras) if p[2] < 0.30 and p[1] >= 18]
    if not top:
        return None, None
    i, t = max(top, key=lambda x: x[1][1])
    sub = None
    for j in range(i + 1, len(paras)):
        tx, pt, tp = paras[j]
        if tp < 0.35 and 11 <= pt < 18 and len(tx) > 4:
            sub = tx
            break
    return t[0], sub


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--config")
    ap.add_argument("--out")
    a = ap.parse_args()
    cfg = load_cfg(a.config)
    prs = Presentation(a.pptx)
    H = prs.slide_height
    N = len(prs.slides)

    err, warn, info = [], [], []
    titles, refs, qtys = [], [], collections.defaultdict(list)
    size_hits, color_hits = collections.defaultdict(set), collections.defaultdict(set)
    accents = []
    slides = []
    for idx, s in enumerate(prs.slides, 1):
        paras, sizes, colors, notes, swatches = read_slide(s, H)
        slides.append((paras, notes))
        title, sub = guess_title(paras)
        titles.append((idx, title, sub))

        for pt in sizes:
            size_hits[pt].add(idx)
        npic = colors.pop(("图片", ""), 0)
        for (kind, c) in colors:
            if cfg["palette"] and c not in cfg["palette"]:
                color_hits[(kind, c)].add(idx)
        acc = sorted({c for (_, c) in colors if is_accent(c)})
        accents.append((idx, acc, npic))
        if len(acc) >= 2 and not any(is_accent(c) for c in swatches):
            warn.append((idx, f"用了 {len(acc)} 种强调色，未找到图例色块（启发式；子标题已写明含义时可忽略）"))

        page_text = "\n".join(p[0] for p in paras)
        for m in PRICE.finditer(page_text):
            err.append((idx, f"页面出现价格或免费说法「{m.group(0)}」，商务条款不写在页面上"))
        for m in MONEY.finditer(page_text):
            warn.append((idx, f"页面出现金额「{m.group(0)}」：业务数据可保留，我方价格不写在页面上"))
        for m in CN_QTY.finditer(page_text):
            warn.append((idx, f"数量用汉字数字「{m.group(0)}」，改为阿拉伯数字"))
        if cfg["accents"]:
            known = {c.upper().lstrip("#") for c in cfg["accents"]}
            extra = [c for c in acc if c not in known]
            if extra:
                warn.append((idx, f"用了语义色表外的强调色 {' '.join('#' + c for c in extra)}"))
        for where, txt in (("页面", page_text), ("讲稿", notes)):
            for w in cfg["banned"]:
                if w in txt:
                    err.append((idx, f"{where}含禁用词「{w}」"))
            for w in cfg["colloquial"]:
                if w in txt:
                    warn.append((idx, f"{where}含口语词「{w}」"))
            for w in cfg["watch"]:
                if w in txt:
                    info.append((idx, f"{where}出现观察词「{w}」，确认是否该出现"))
            for std, bad in cfg["terms"].items():
                for b in bad:
                    if b in txt:
                        warn.append((idx, f"{where}写了「{b}」，术语表标准名为「{std}」"))
            for m in PAGE_REF.finditer(txt):
                n1 = int(m.group(1)); n2 = int(m.group(2) or n1)
                refs.append((idx, where, m.group(0), n1, n2))
                if n1 < 1 or n2 > N:
                    err.append((idx, f"{where}引用「{m.group(0)}」超出总页数 {N}"))
            for m in QTY.finditer(txt):
                qtys[m.group(2)].append((idx, where, txt[max(0, m.start() - 8):m.end() + 4].replace("\n", " ")))

        for text, pt, top in paras:
            if SPLIT.search(text) and len(text) > 8 and pt < 18:
                warn.append((idx, f"一段两个分句：{text[:40]}"))
            for m in re.finditer(cfg["internal_code"], text):
                warn.append((idx, f"疑似内部编号「{m.group(0)}」：{text[:30]}"))
            for m in SNAKE.finditer(text):
                err.append((idx, f"代码标识符上了页面「{m.group(0)}」"))

        nums = sorted({int(SEQ.match(p[0]).group(1)) for p in paras if SEQ.match(p[0]) and len(p[0].strip()) == 2})
        if len(nums) >= 3:
            gaps = [n for n in range(nums[0], nums[-1] + 1) if n not in nums]
            if gaps and len(gaps) <= 2:
                warn.append((idx, f"两位编号疑似跳号：有 {nums}，缺 {gaps}"))

        if title and (VERDICT.search(title) or len(title) > 20):
            warn.append((idx, f"标题像结论句（应为名词短语，结论写进子标题）：{title}"))
        if title and title.endswith("。"):
            warn.append((idx, f"标题以句号结尾：{title}"))
        if sub:
            if not sub.endswith("。"):
                info.append((idx, f"子标题未以句号结尾：{sub[:40]}"))
            if len(sub) > 40:
                warn.append((idx, f"子标题超过 40 字（{len(sub)}）：{sub[:40]}…"))

    for pt, pages in sorted(size_hits.items()):
        if pt < cfg["min_font"]:
            err.append((min(pages), f"字号 {pt}pt 小于下限 {cfg['min_font']}pt，出现在第 {fmt(pages)} 页"))
    if len(size_hits) > cfg["max_levels"]:
        warn.append((1, f"全册用了 {len(size_hits)} 级字号（上限 {cfg['max_levels']}）：{', '.join(str(x) for x in sorted(size_hits))} pt"))
    for (kind, c), pages in sorted(color_hits.items()):
        info.append((min(pages), f"{kind}色 #{c} 不在色表内，出现在第 {fmt(pages)} 页"))

    out = []
    out.append(f"# 方案 PPT 自查报告\n\n文件：{a.pptx}　共 {N} 页\n")
    out.append(f"ERROR {len(err)} 条　WARNING {len(warn)} 条　INFO {len(info)} 条\n")
    for name, lst in (("ERROR", err), ("WARNING", warn), ("INFO", info)):
        out.append(f"\n## {name}\n")
        if not lst:
            out.append("无\n")
        for p, msg in sorted(lst, key=lambda x: x[0]):
            out.append(f"- 第 {p} 页　{msg}")
    out.append("\n\n## 人工核对一　标题与子标题通读\n")
    out.append("| 页 | 标题 | 子标题 |\n| --- | --- | --- |")
    for i, t, s in titles:
        out.append(f"| {i} | {t or '（未识别）'} | {s or ''} |")
    out.append("\n\n## 人工核对二　页码引用\n")
    out.append("| 所在页 | 位置 | 引用 | 指向页标题 |\n| --- | --- | --- | --- |")
    for i, where, raw, n1, n2 in refs:
        tgt = "；".join((titles[k - 1][1] or "（未识别）") for k in range(n1, n2 + 1) if 1 <= k <= N)
        out.append(f"| {i} | {where} | {raw} | {tgt} |")
    out.append("\n\n## 人工核对三　数量说法（前后页对照）\n")
    for unit, lst in sorted(qtys.items(), key=lambda x: -len(x[1])):
        out.append(f"\n**「{unit}」**")
        for i, where, ctx in lst:
            out.append(f"- 第 {i} 页 {where}：…{ctx}…")
    out.append("\n\n## 人工核对四　每页强调色（对照项目色表，一色一义）\n")
    out.append("图片和图标内的颜色读不到，有图片的页要打开对照。\n")
    out.append("| 页 | 强调色（文字、填充、线条） | 图片和图标数 |\n| --- | --- | --- |")
    for i, acc, npic in accents:
        out.append(f"| {i} | {' '.join('#' + c for c in acc) or '无'} | {npic or ''} |")
    report = "\n".join(out) + "\n"
    if a.out:
        open(a.out, "w", encoding="utf-8").write(report)
        print(f"已写出 {a.out}：ERROR {len(err)}　WARNING {len(warn)}　INFO {len(info)}")
    else:
        print(report)
    sys.exit(1 if err else 0)


def fmt(pages):
    p = sorted(pages)
    return "、".join(map(str, p[:12])) + ("…" if len(p) > 12 else "")


if __name__ == "__main__":
    main()
