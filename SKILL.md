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
| 1 | 规范与受众 | `phase-01.md` | `phase-common.md`、`brand-spec/brand.md`（配色、字体、PPT 三节） |
| 2 | 材料解析 | `phase-02.md` | — |
| 3 | 论点提炼 | `phase-03.md` | — |
| 4 | 叙事骨架 | `phase-04.md` | `wording-rules.md` |
| 5 | 大纲与版式 | `phase-05.md` | `design-principles.md` |
| 6 | 样页确认 | `phase-06.md` | `html-slides.md` |
| 7 | 逐页设计 | `phase-07.md` | — |
| 8 | 质检交付 | `phase-08.md` | — |

文件都在 `references/` 下。已读过的文件后续阶段不重读。

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

## 规则优先级

- 文字：`wording-rules.md`；方案类的标题和页面短句以 `solution-deck.md` 为准。
- 版式、颜色数量、字号层级：`design-principles.md`。`brand.md` 只提供色值和字体，
  其中「单一强调色」「图表只用一个高亮」和 PPT 字号表不再约束版式设计。

## 降级基线（读不到 brand.md 时）

- 白底；墨色 `#1F2633` `#4A5363` `#7D8695`；线 `#E3E6EB` `#C9CED6`；浅底 `#F6F7F9`。
- 强调色从 `#336EE8` 蓝、`#17998A` 青绿、`#D4892A` 橙取，一色一义并配图例。
- 字体：微软雅黑或 PingFang SC；数字可用 Consolas。禁衬线和纯黑 `#000`。
- 不用渐变、阴影、半透明、3D 和饼图。最小字号 9pt。

## 防坑

1. 序号不用 ①②③，对错号用 √ ×。PPT 字体缺字时会显示方框。
2. 软件界面没有截图时画占位框并标「示意」，不画假界面。
3. 开工建术语表，同一事物只用一个名称；客户评审过的架构图作为定稿，其他页与它一致。
4. 先建基线（`phase-common.md` 第四节），数字不编造，缺的写「待确认」。
