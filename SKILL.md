---
name: aham-ppt
description: >
  把材料做成方案级、汇报级的 PPT。用户说「帮我做PPT」「做演示文稿」「做一个汇报」「根据这份资料做PPT」
  「做客户方案PPT」「制作幻灯片」时触发，只有一句话需求也触发。
  八个阶段：受众与规范 → 材料解析 → 论点提炼 → 叙事骨架 → 页面规划 → 样页确认 → 逐页设计 → 质检交付。
  页面写成 HTML 幻灯片，网页预览确认后导出可编辑 PPTX。
---

# Aham PPT

## 依赖

- Node.js：在 `assets/html2pptx/` 运行 `npm install`，安装 pptxgenjs 和 playwright。环境已有 playwright 时只装 pptxgenjs。
- Python：`pip install -r requirements.txt`，用于读材料提纲和检查 PPTX。
- LibreOffice 可选，用于导出 PDF 和抽查渲染。没有时交付物不含 PDF，并在交付说明里写明。

## 阶段与文件

每个阶段开始前读对应的阶段文件，按文件里的停等点、步骤和完成卡执行。八个阶段按顺序进行。
阶段共用的动作、完成卡格式和工作区文件见 `phase-common.md`，在第一阶段读一次。

| # | 阶段 | 阶段文件 | 同时读 |
| --- | --- | --- | --- |
| 1 | 受众与规范 | `phase-01.md` | `phase-common.md`、`style-tokens.md` |
| 2 | 材料解析 | `phase-02.md` | — |
| 3 | 论点提炼 | `phase-03.md` | — |
| 4 | 叙事骨架 | `phase-04.md` | `wording-rules.md` |
| 5 | 页面规划 | `phase-05.md` | `design-principles.md`、`style-elements.md` |
| 6 | 样页确认 | `phase-06.md` | `html-slides.md`、`assets/examples/README.md` |
| 7 | 逐页设计 | `phase-07.md` | 每章开工前重读 `design-principles.md` 第一节和范例库说明 |
| 8 | 质检交付 | `phase-08.md` | — |

除注明路径的文件外，文件都在 `references/` 下。已读的文件在后续阶段不重读，表里写明重读的除外。

按条件读的文件：

| 文件 | 条件 |
| --- | --- |
| `solution-deck.md` | 第一阶段把文稿类型定为方案 |
| `coach-engine.md` | 第一阶段末尾读第一、二节做档位检测；档位为引导或教练时，每个阶段读第三节对应的引导序列 |

## 风格的三层

| 层 | 文件 | 约束 |
| --- | --- | --- |
| 固定数值 | `style-tokens.md`，常量在 `assets/html2pptx/components.js` | 字号、颜色、线宽、圆角和页面框架全册不变 |
| 元素 | `style-elements.md`，画法在 `components.js` | 每种元素表达一种关系，按适用条件选用 |
| 构图 | `design-principles.md`、范例库 `assets/examples/` | 按本页内容设计，同类页不照抄构图 |

## 规则优先级

- 文字按 `wording-rules.md`。方案类的标题、子标题和页面短句按 `solution-deck.md`。
- 数值按 `style-tokens.md`，元素按 `style-elements.md`，构图按 `design-principles.md`。
- 用户在本次对话里的要求优先于以上文件，记进基线的修正记录。

## 常见错误

1. 序号写阿拉伯数字，不用 ①②③；对错写 √ ×。PPT 字体缺这些字符时显示方框。
2. 没有软件界面截图时画占位框并在页脚标「示意」，不画假界面。
3. 开工时建术语表，同一事物只用一个名称。客户评审过的架构图作为定稿，其他页与它一致。
4. 数字只取自信息清单，不编造。缺的数字记进基线的待确认清单，页面不写「待确认」。
