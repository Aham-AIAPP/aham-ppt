---
name: aham-ppt
description: >
  全流程 AI 制作 PPT 演示文稿技能（Aham UI v6.1 · Office 轨 · PPT）。
  用户说「帮我做PPT」「做演示文稿」「做一个汇报」「根据这份资料做PPT」「做客户方案PPT」「制作幻灯片」时触发，只有一句话需求也触发。
  八阶段流程：规范与受众 → 材料解析 → 论点提炼 → 叙事骨架 → 大纲与版式 → 样页确认 → 逐页设计 → 质检交付。
  版式按内容结构设计；AI 直接写 HTML 幻灯片，网页预览确认后导出可编辑 PPTX。
---

# Aham PPT 技能

## 依赖

- Node.js、`pptxgenjs`、`playwright`：在 `assets/html2pptx/` 运行 `npm install`。环境已有 playwright 时只装 pptxgenjs。
- Python：`python-pptx`（自查脚本），读材料提纲另需 `pypdf`、`python-docx`、`openpyxl`。
- 可选 LibreOffice：导出 PDF 和渲染抽查。没有时交付物不含 PDF，在交付说明里写明。

## 执行规则

1. 逐阶段加载：进入第 N 阶段前读 `references/phase-0N.md`，不凭阶段名直接产出。
2. 卡点等待：每阶段输出完成卡，用户确认后再进下一阶段。合并规则见 `coach-engine.md`「停等卡点合并」。
3. 不跳步：八个阶段按序执行。Phase 3 灵魂句和 Phase 6 样页任何档位都单独停等。
4. 进度可见：每阶段第一句输出 `【阶段 N/8 · 名称 · 已加载 phase-0N.md】`。

| # | 阶段 | 文件 | 同时加载 |
| --- | --- | --- | --- |
| 1 | 规范与受众 | `phase-01.md` | `phase-common.md`、`style-tokens.md` |
| 2 | 材料解析 | `phase-02.md` | — |
| 3 | 论点提炼 | `phase-03.md` | — |
| 4 | 叙事骨架 | `phase-04.md` | `wording-rules.md` |
| 5 | 大纲与版式 | `phase-05.md` | `design-principles.md`、`style-elements.md` |
| 6 | 样页确认 | `phase-06.md` | `html-slides.md`、`assets/examples/README.md`（范例库） |
| 7 | 逐页设计 | `phase-07.md` | 每章开工前重读 `design-principles.md` 第一节和范例库说明 |
| 8 | 质检交付 | `phase-08.md` | — |

除注明路径的以外，文件都在 `references/` 下。表中写明重读的文件按要求重读，其他已读文件后续阶段不重读。

## 按条件加载

| 文件 | 条件 |
| --- | --- |
| `solution-deck.md` | Phase 1 定为方案类 |
| `coach-engine.md` | Phase 1 档位检测时读第二节；档位为引导或教练时各阶段读第三节对应序列 |
| `brand-spec/iconography.md` | 页面要画图标 |

## 参考素材（主流程不加载）

下列文件来自旧的 SVG 路线，留作参考：要画某种结构或图表时可以查，查到的画法按本页内容改，不照搬坐标。

| 文件 | 内容 |
| --- | --- |
| `layout-library.md`、`svg-skeleton-*.md`、`grid-composition.md` | 39 个版式的画法 |
| `grid-system.md`、`theme-tiers.md` | 栅格坐标、A/B/C 三档主题 |
| `designer-rules.md`、`chart-impl.md` | 设计细则、图表手画模板 |
| `pptx-native-rules.md`、`quality-audit-protocol.md`、`assets/svg_to_pptx/` | SVG 转 PPTX 工具链 |
| `assets/components/` | Python 图表、图标、结构图函数（输出 SVG） |
| `brand-spec/track-rules.md` | 轨道分流规则 |

## 风格的三层定义

| 层 | 文件 | 约束程度 |
| --- | --- | --- |
| 固定数值 | `style-tokens.md`，代码常量在 `assets/html2pptx/components.js` | 字号、颜色、线宽、圆角、页面框架全册不变 |
| 元素词汇 | `style-elements.md`，画法在 `components.js` | 每种元素表达一种关系，按适用条件选用 |
| 构图 | `design-principles.md`、范例库 | 由本页内容决定，同类页不抄同一构图 |

## 规则优先级

- 文字：`wording-rules.md`；方案类的标题和页面短句以 `solution-deck.md` 为准。
- 数值：`style-tokens.md`。版式：`design-principles.md`。
- `brand-spec/brand.md` 是品牌总规范，主流程不加载；与 `style-tokens.md` 不一致处以后者为准。

## 防坑

1. 序号不用 ①②③，对错号用 √ ×。PPT 字体缺字时会显示方框。
2. 软件界面没有截图时画占位框并标「示意」，不画假界面。
3. 开工建术语表，同一事物只用一个名称；客户评审过的架构图作为定稿，其他页与它一致。
4. 先建基线（`phase-common.md` 第四节），数字不编造。缺的数字记进基线的待确认清单，页面不写「待确认」；方案类集中列在待确认事项页。
