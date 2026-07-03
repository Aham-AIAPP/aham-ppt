# Aham PPT · 代码资产目录

本目录包含两类代码资产：

- **`svg_to_pptx/` + `svg_to_pptx_wrapper.py`** —— SVG → 原生 PPTX 工具链（**只有一个入口**，其他都是底层实现）。
- **`components/`** —— 生成 SVG 页面用的组件库（原子组件 / 图表 / 图标 / 三档模板）。

---

## 入口：`svg_to_pptx_wrapper.py` ★

唯一对外使用的模块。调用方式：

```python
from svg_to_pptx_wrapper import svg_to_native_pptx
from pathlib import Path

svg_files = sorted(Path('svg_final').glob('*.svg'))
svg_to_native_pptx(svg_files, Path('output.pptx'))
```

**重要**：只使用这个 wrapper，**不要**直接调用 `svg_to_pptx/` 内部模块。

---

## 工具链主体：`svg_to_pptx/`

**用途**：把 SVG 文件批量转成原生可编辑的 PPTX 文件。

**特性**：
- 每个 SVG 元素 → 独立的 PPT 原生形状（不是图片嵌入）
- 所有文字都是可编辑 textbox，在 PowerPoint 里双击就能改
- 矩形、圆、线条都是 PPT 原生 shape
- 多边形（如梯形）通过 custGeom 实现，仍可编辑

**来源**：基于 `github.com/hugohe3/ppt-master`（MIT License）。
详见 `svg_to_pptx/LICENSE_NOTE.md`。

---

## 组件库：`components/`

生成 SVG 页面用的参数化组件库——一行调用 = 一个合规元素，不再逐坐标手画。
四个模块**自包含、无品牌/客户硬编码**，颜色一律按 `brand.md` / `tokens.css` 的角色色传入。

| 文件 | 能力 |
|---|---|
| `components.py` | 原子组件：文本 `T`、面板 `P`、连线 `L`、直/曲箭头、`chip` / `hexagon` / `status`、界面占位框 `placeholder`。（v3.0 删除全仓零引用的 6 个旧原型组件） |
| `charts.py` | 参数化图表：`waterfall` / `bar` / `hbar` / `line` / `funnel` / `gantt` / `bullet` / `stacked` / `slope`。严格遵守 `brand.md §7.5 / §2.4`——灰阶 + 至多一个 `#336EE8` 高亮、无饼图/环形/3D/渐变、正负靠符号+文字双通道、数字 mono。 |
| `icons.py` | Lucide 风格线性图标库（~40 个）：`ICON` 取图标、`icon_circle` 图标圆；取色传入，不写死品牌色。 |
| `themes.py` | A / B / C 三档模板：`cover` / `toc` / `section` / `chrome`（A·B 通用）+ `cover_dark` / `section_dark` / `quote_dark`（C·高表现力深色档）。1280×720 画布，依赖 `components.py` / `icons.py`。 |

---

## 文件清单

```
assets/
├── README.md                    # 本文件
├── svg_to_pptx_wrapper.py       # ★ SVG → PPTX 对外入口
├── components/                  # SVG 组件库
│   ├── components.py            # 关系图 / UI 原型原子组件
│   ├── charts.py                # 参数化图表
│   ├── icons.py                 # Lucide 风格线性图标
│   └── themes.py                # A / B / C 三档模板
└── svg_to_pptx/                 # SVG → PPTX 工具链主体
    ├── __init__.py
    ├── drawingml_context.py
    ├── drawingml_converter.py
    ├── drawingml_elements.py
    ├── drawingml_paths.py
    ├── drawingml_styles.py
    ├── drawingml_utils.py
    ├── pptx_builder.py
    ├── pptx_dimensions.py
    ├── pptx_media.py
    ├── pptx_notes.py
    ├── pptx_slide_xml.py
    └── LICENSE_NOTE.md
```

---

## 设计原则

- **不手写 python-pptx 代码拼形状**：baseline 偏移、letter-spacing、textbox 宽度估算有无数坑
- **不用 EMF 嵌入后声称"可编辑"**：那只是图片
- **PPTX 生成后不直接改 PPTX**：会与 SVG 真源漂移
- **出现故障时，回去改 SVG 源，重新运行工具链**
