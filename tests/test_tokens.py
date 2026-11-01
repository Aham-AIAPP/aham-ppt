"""固定数值的一致性检查。

数值的机器可读来源是 assets/html2pptx/tokens.json，代码都从它读取。
本测试确认：
- references/style-tokens.md 表格里的字号、颜色、线宽、圆角和页面框架与 tokens.json 一致；
- references/html-slides.md 写的画布、字体栈与 tokens.json 一致；
- 不能读 tokens.json 的地方（浏览器里运行的 runtime.js、给用户复制的 check_deck.example.json）与它一致；
- 引擎脚本里没有再写死调色板色值和画布尺寸；
- 有 Node.js 时，components.js、tokens.js 引出的常量与 tokens.json 一致。
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "assets" / "html2pptx"
TOKENS = json.loads((ENGINE / "tokens.json").read_text("utf-8"))
DOC = (ROOT / "references" / "style-tokens.md").read_text("utf-8")


def section(text: str, title: str) -> str:
    """取「## 标题」到下一个「## 」之间的正文。"""
    m = re.search(rf"^## {re.escape(title)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        raise AssertionError(f"style-tokens.md 里找不到「## {title}」")
    return m.group(1)


def numbers(cell: str) -> list[float]:
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", cell)]


class StyleTokensDocTest(unittest.TestCase):
    def test_canvas(self):
        m = re.search(r"画布 (\d+) × (\d+) 像素，1px 等于 ([\d.]+)pt", DOC)
        self.assertIsNotNone(m, "style-tokens.md 开头应写画布尺寸和 px 与 pt 的换算")
        c = TOKENS["canvas"]
        self.assertEqual((int(m.group(1)), int(m.group(2))), (c["w"], c["h"]))
        self.assertEqual(float(m.group(3)), 1 / c["pxPerPt"])

    def test_font_size(self):
        doc = {k: float(v) for v, k in re.findall(r"^\| ([\d.]+)px \| `FS\.(\w+)` \|", section(DOC, "一、字号"), re.M)}
        self.assertEqual(doc, {k: float(v) for k, v in TOKENS["FS"].items()})

    def test_mono_font(self):
        m = re.search(r"等宽字体 `([^`]+)`", section(DOC, "一、字号"))
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1).replace(", ", ","), TOKENS["font"]["mono"])

    def test_colors(self):
        body = section(DOC, "二、颜色")
        doc = {}
        for name, value, light in re.findall(r"`C\.(\w+)` \| `(#[0-9A-Fa-f]{6})` \|(?: `(#[0-9A-Fa-f]{6})` \|)?", body):
            doc[name] = value.upper()
            if light:
                doc[name + "Bg"] = light.upper()
        self.assertEqual(doc, {k: v.upper() for k, v in TOKENS["C"].items()})

    def test_line_width(self):
        doc = {k: float(v) for v, k in re.findall(r"^\| ([\d.]+)px \| `LW\.(\w+)` \|", section(DOC, "三、线宽"), re.M)}
        self.assertEqual(doc, {k: float(v) for k, v in TOKENS["LW"].items()})

    def test_radius(self):
        m = re.search(r"方框 (\d+)px，卡片 (\d+)px", section(DOC, "四、圆角与形状"))
        self.assertIsNotNone(m)
        self.assertEqual({"box": int(m.group(1)), "card": int(m.group(2))}, TOKENS["RAD"])

    def test_frame(self):
        f, fs = TOKENS["frame"], TOKENS["FS"]
        # 每行「数值」一栏里的数字，按出现顺序
        expected = {
            "左右边距": [f["margin"], f["right"]],
            "页眉左": [fs["body"], f["headerTop"]],
            "页眉右": [fs["body"], f["right"]],
            "标题": [fs["title"], 700, f["titleTop"]],
            "子标题": [fs["sub"], f["subTop"]],
            "主图区": [f["main"]["y0"], f["main"]["y1"]],
            "属性带": [f["attr"]["y0"], f["attr"]["y1"], TOKENS["RAD"]["box"]],
            "页脚线": [f["footLine"], TOKENS["LW"]["struct"]],
            "页脚左": [fs["body"]],
            "页脚右": [fs["body"]],
        }
        rows = {}
        for line in section(DOC, "五、页面框架").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 3 and cells[0] in expected:
                rows[cells[0]] = numbers(cells[2])
        self.assertEqual(set(rows), set(expected), "页面框架表的行与检查项不符")
        for name, want in expected.items():
            with self.subTest(row=name):
                self.assertEqual(rows[name], [float(x) for x in want])


class OtherSourcesTest(unittest.TestCase):
    def test_html_slides_doc(self):
        text = (ROOT / "references" / "html-slides.md").read_text("utf-8")
        c = TOKENS["canvas"]
        self.assertIn(f"画布 {c['w']} × {c['h']} 像素", text)
        m = re.search(r"预览和导出用同一组字体：`([^`]+)`", text)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), TOKENS["font"]["stack"])
        m = re.search(r"数字和编号用 `([^`]+)`", text)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1).replace(", ", ","), TOKENS["font"]["mono"])

    def test_runtime_canvas(self):
        # runtime.js 在浏览器里运行，并原样内嵌进预览页，读不到 tokens.json，只能在这里核对
        text = (ENGINE / "runtime.js").read_text("utf-8")
        c = TOKENS["canvas"]
        self.assertIn(f"width:{c['w']}px;height:{c['h']}px", text)
        self.assertIn(f"width: {c['w']}, height: {c['h']}", text)

    def test_check_deck_example(self):
        # 示例配置给用户复制成项目配置，保留完整色表；色表和语义色要与 tokens.json 一致
        cfg = json.loads((ROOT / "assets" / "tools" / "check_deck.example.json").read_text("utf-8"))
        colors = {k: v.upper().lstrip("#") for k, v in TOKENS["C"].items()}
        self.assertEqual(sorted(cfg["palette"]), sorted(colors.values()))
        self.assertEqual(set(cfg["accents"]), {colors["ai"], colors["svc"], colors["prod"]})
        self.assertEqual(cfg["min_font"], TOKENS["FS"]["body"] / TOKENS["canvas"]["pxPerPt"])

    def test_no_hardcoded_values_in_engine(self):
        # runtime.js 见上；demo 是用法示例，只用组件和常量
        palette = [v.upper() for v in TOKENS["C"].values()]
        c = TOKENS["canvas"]
        for path in sorted(ENGINE.glob("*.js")):
            if path.name == "runtime.js":
                continue
            code = "\n".join(re.sub(r"//.*$", "", line) for line in path.read_text("utf-8").splitlines())
            with self.subTest(file=path.name):
                found = sorted({h for h in re.findall(r"#[0-9A-Fa-f]{6}\b", code) if h.upper() in palette})
                self.assertEqual(found, [], "色值应从 tokens.json 读取")
                self.assertNotRegex(code, rf"\b({c['w']}|{c['h']})\b", "画布尺寸应从 tokens.json 读取")
                self.assertNotIn("Microsoft YaHei", code, "字体应从 tokens.json 读取")
                self.assertNotIn("'Consolas", code, "等宽字体应从 tokens.json 读取")


@unittest.skipUnless(shutil.which("node"), "没有 Node.js")
class NodeExportsTest(unittest.TestCase):
    def test_constants(self):
        script = (
            "const K = require('./components'), T = require('./tokens');"
            "console.log(JSON.stringify({ C: K.C, FS: K.FS, LW: K.LW, RAD: K.RAD, MARGIN: K.MARGIN, RIGHT: K.RIGHT,"
            " MAIN: K.MAIN, MAIN_RECT: T.MAIN_RECT, FONT_FACE: T.FONT_FACE, MONO_FACE: T.MONO_FACE, PX_PER_IN: T.PX_PER_IN }))"
        )
        out = json.loads(subprocess.run(["node", "-e", script], cwd=ENGINE, check=True, capture_output=True, text=True).stdout)
        f = TOKENS["frame"]
        self.assertEqual(out["C"], TOKENS["C"])
        self.assertEqual(out["FS"], TOKENS["FS"])
        self.assertEqual(out["LW"], TOKENS["LW"])
        self.assertEqual(out["RAD"], TOKENS["RAD"])
        self.assertEqual((out["MARGIN"], out["RIGHT"]), (f["margin"], f["right"]))
        self.assertEqual(out["MAIN"], f["main"])
        self.assertEqual(out["MAIN_RECT"], {"x": 96, "y": 195, "w": 1728, "h": 700})
        self.assertEqual((out["FONT_FACE"], out["MONO_FACE"]), ("Microsoft YaHei", "Consolas"))
        self.assertEqual(out["PX_PER_IN"], 144)


if __name__ == "__main__":
    unittest.main()
