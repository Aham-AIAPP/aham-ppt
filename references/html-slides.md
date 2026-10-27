# 网页幻灯片写法与导出

> Phase 6 写样页、Phase 7 写全册时加载。本文件只管写法和导出约束，版式由 `design-principles.md` 决定。
> 路线：用 `components.js` 写生成脚本拼出 HTML 幻灯片 → 网页预览 → 排版检查 → 导出可编辑 PPTX。
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

导出程序在浏览器里排版后读取每个元素的实际位置和计算样式，所以 CSS 怎么写都能读到数值。
下列效果 PPT 形状表达不了，`check_slides.js` 报 ERROR：

- 渐变、阴影、文字阴影、`opacity`、`filter`、`transform`、背景图。
- 非绝对定位的元素（flex、grid、相对定位）。
- `<div>` 里放文字；`<p>` 里放 `<svg>` 或 `<img>`。
- 不在 2.1 表中的标签。

半透明颜色按页面底色混成实色导出，报 WARNING。`<p>` 里 `b strong span br i em` 以外的行内标签按普通文字导出，报 WARNING。

### 2.4 字体

预览和导出用同一组字体：`'Microsoft YaHei','PingFang SC','Noto Sans SC',sans-serif`，导出到 PPT 写微软雅黑。
数字和编号用 `Consolas, monospace`。不同机器上字宽略有差别，所以单行文字不要贴满文字框：
单行文字占满宽度 95% 以上时排版检查报 WARNING。

### 2.5 字号与尺寸换算

1px 等于 0.5pt。PPT 上 9pt 的正文写 18px，26pt 的页标题写 52px。
全册最小字号 18px（9pt），排版检查低于此值报错。

### 2.6 可编辑性取舍

文字、方框、连线都写成 2.1 表中的可编辑元素。只有图标和曲线用 `<svg>`。
一页里 `<svg>` 占主图面积一半以上时，在讲稿注明「本页主图为图片」。

## 三、组件与生成脚本

页面用 `assets/html2pptx/components.js` 拼，不手写坐标和色值。组件里的常量与 `style-tokens.md` 一致：

| 类别 | 内容 |
| --- | --- |
| 常量 | `C` 颜色、`FS` 字号、`LW` 线宽、`RAD` 圆角、`MARGIN` 左边距、`RIGHT` 右边线 |
| 基础 | `text` 单行字、`para` 段落、`box` 方框、`line` 连线、`arrow` 箭头、`circle`、`diamond`、`chip` 胶囊、`labelValue` 标签与值、`attrBand` 属性带、`legend` 图例 |
| 元素词汇 | `balloon` `stepNo` `noteNo` `crossMark` `dimLine` `reviewPoint` `leader` `bigNumber` `plate` `frame`，用法见 `style-elements.md` |
| 页面 | `page` 正文页框架、`slide` 无框架页（封面、目录、章节页）、`writeDeck` 写出 deck 目录 |

在工作目录写 `build.js`，每页先按规划卡画主图，再交给 `page()` 加页眉页脚。示例见 `assets/html2pptx/demo/build.js`。
组件没有的元素可以在脚本里自己画，数值仍取 `C`、`FS`、`LW`，并在基线里记下这个新元素表达什么。
生成脚本留在工作目录，不进交付物。

## 四、命令

脚本在 `assets/html2pptx/`。首次使用在该目录运行 `npm install`；环境已有 playwright 时只装 pptxgenjs。

```bash
node build.js deck/                                                            # 生成 deck/
node assets/html2pptx/preview.js deck/ deck/preview.html --title "方案预览"     # 单文件预览页
node assets/html2pptx/check_slides.js deck/ --png deck/png --sheet deck/总览.png  # 排版和导出兼容检查、截图、缩略图总览
node assets/html2pptx/html2pptx.js deck/ 交付.pptx --title "方案" --author "〈我方〉"  # 导出
```

- 预览页自包含，可直接发布为 Artifact 给用户看。
- `check_slides.js` 接受 deck 目录或预览页。它查字号过小、文字溢出、超出画布、文字重叠、单行贴边和 2.3 节的导出兼容问题。ERROR 必须改完。
- 导出程序与预览页用同一套页面和字体排版，网页上看到的位置就是 PPT 里的位置。导出时仍有 ERROR 会在最后列出。
- LibreOffice 可用时把 PPTX 转 PDF 抽查几页换行。

## 五、写页顺序

1. 按 Phase 5 规划卡的内容结构先画主图，再放标题、子标题和属性带。
2. 写完一页运行一次生成、预览和排版检查，看截图再改。
3. 文字溢出时先删次要信息或拆页，最后才缩小方框内边距。不缩字号。
4. 相同元素用同一个组件函数画，尺寸和间距在本册内统一。
