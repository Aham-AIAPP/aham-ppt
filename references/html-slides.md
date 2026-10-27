# 网页幻灯片写法与导出

> Phase 6 写样页、Phase 7 写全册时加载。本文件只管写法和导出约束，版式由 `design-principles.md` 决定。
> 路线：AI 直接写 HTML 幻灯片 → 网页预览 → 排版检查 → 导出可编辑 PPTX。
> 旧的 SVG 转 PPTX 工具链移出主流程，文件暂留在 `assets/svg_to_pptx/`。

---

## 一、目录结构

```
<工作目录>/deck/
  deck.json          {"order": ["p01", "p02", ...]}   页序
  slides/p01.html    每页一个文件
  img/               截图、照片（相对路径引用）
```

## 二、页面写法

每页一个 `<section>`，画布 1920 × 1080 像素。页内元素全部绝对定位，坐标写在 `style` 里，单位 px。

```html
<section style="background:#FFFFFF">
  <p style="left:96px;top:64px;width:1200px;font-size:52px;font-weight:700;color:#1F2633">页标题</p>
  <div style="left:96px;top:200px;width:560px;height:320px;background:#F6F7F9;border:2px solid #C9CED6"></div>
  <x-shape kind="ellipse" style="left:700px;top:220px;width:48px;height:48px;background:#336EE8"></x-shape>
  <x-connector x1="656" y1="360" x2="900" y2="360" head="end" style="color:#5B6B82;border-width:2px"></x-connector>
  <aside>讲稿：原因、例外、举例和出处写在这里。</aside>
</section>
```

### 2.1 元素

| 元素 | 用途 | 导出结果 |
| --- | --- | --- |
| `<p>` | 一段文字；可带底色和边框，成为带字的方框 | 文本框，可编辑 |
| `<div>` | 无文字的矩形、圆角矩形；只设 `border-top` 或 `border-left` 时是横线或竖线 | 形状或线条，可编辑 |
| `<x-shape kind>` | `ellipse` `diamond` `rect` `rounded` | 形状，可编辑 |
| `<x-connector>` | 连线；`x1 y1 x2 y2` 端点，`head` 取 `none` `end` `start` `both`，`route` 取 `hv` `vh` `elbow` 时走直角折线 | 线条，可编辑 |
| `<svg>` | 图标和 PPT 形状画不出的曲线 | 图片，不可编辑 |
| `<img>` | 截图、照片 | 图片 |
| `<aside>` | 讲稿 | PPT 备注 |

`<p>` 内可用 `<br>` 分行，用 `<b>` 或 `<span style="color:…;font-weight:…">` 改局部格式。

### 2.2 可用样式

- 位置与尺寸：`left` `top` `width` `height`，只写 px。
- 文字：`font-size` `font-weight` `color` `line-height` `text-align` `white-space:nowrap` `padding`；
  `font-family` 含 `monospace` 时导出为 Consolas。
- 填充与边框：`background` `border:Npx solid|dashed 颜色` `border-radius` `border-top` `border-left`。
- 颜色只写 `#RRGGBB` 或 `rgb()`。
- 连线：`color` `border-width` `border-style:dashed`。

### 2.3 导出不支持的写法

- 渐变、阴影、半透明、旋转、`transform`：导出时丢失。
- flex、grid、相对定位、外部 CSS 类：导出只读行内 `style`。
- `<div>` 里放文字：导出报错。文字一律写在 `<p>` 里。
- 不在 2.1 表中的标签：导出时忽略。

### 2.4 字号与尺寸换算

1px 等于 0.5pt。PPT 上 9pt 的正文写 18px，26pt 的页标题写 52px。
全册最小字号 18px（9pt），排版检查低于此值报错。

### 2.5 可编辑性取舍

文字、方框、连线都写成 2.1 表中的可编辑元素。只有图标和曲线用 `<svg>`。
一页里 `<svg>` 占主图面积一半以上时，在讲稿注明「本页主图为图片」。

## 三、命令

脚本在 `assets/html2pptx/`。首次使用在该目录运行 `npm install`；环境已有 playwright 时只装 pptxgenjs。

```bash
node assets/html2pptx/preview.js deck/ deck/preview.html --title "方案预览"   # 单文件预览页
node assets/html2pptx/check_slides.js deck/preview.html --png deck/png --sheet deck/总览.png  # 排版检查、截图、缩略图总览
node assets/html2pptx/html2pptx.js deck/ 交付.pptx --title "方案" --author "〈我方〉"  # 导出
```

- 预览页自包含，可直接发布为 Artifact 给用户看。
- 排版检查在浏览器里实际排版后检查字号过小、文字溢出、超出画布和文字重叠。ERROR 必须改完。
- 导出后用 LibreOffice 转 PDF 抽查几页，确认 PPT 里的换行与网页一致。

## 四、写页顺序

1. 按 Phase 5 规划卡的内容结构先画主图，再放标题、子标题和属性带。
2. 写完一页运行一次预览和排版检查，看截图再改。
3. 文字溢出时先删次要信息或拆页，最后才缩小方框内边距。不缩字号。
4. 相同元素的尺寸和间距在本册内统一。可在工作目录写生成脚本复用组件，脚本不进交付物。
