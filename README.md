# Aham PPT — 克制的 AI PPT 制作技能

[![Release](https://img.shields.io/github/v/release/Aham-AIAPP/aham-ppt?color=336EE8)](https://github.com/Aham-AIAPP/aham-ppt/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-336EE8.svg)](LICENSE)
[![Design](https://img.shields.io/badge/Design-Aham%20UI%20v6.1-336EE8.svg)](https://github.com/Aham-AIAPP/aham-ui)
[![Type](https://img.shields.io/badge/type-Claude%20Skill-336EE8.svg)](#)
[![联系我](https://img.shields.io/badge/%E8%81%94%E7%B3%BB%E6%88%91-%E5%BE%AE%E4%BF%A1-336EE8.svg?logo=wechat&logoColor=white)](assets/wechat-qr.png)

![Aham PPT — 克制的 AI PPT 制作技能](assets/social-preview.png)

## 为什么做

市面上的 AI 做 PPT，大多是「一句话出一份能看的 PPT」——快，但只到「能看」。而要拿去给客户、给领导的**方案、汇报、报告**，需要的是逻辑站得住、论证有依据、版面专业克制、能直接交付的水准——这不是一键速成能给的。

这个技能为此而做：它不追求秒出，而是按资深顾问的成稿流程一步步推进，把零散素材做成**方案级 / 报告级**的专业 PPT。

## 定位

产出的不是「好看的模板 PPT」，而是一份经得起审视的专业交付物：

- **专业** — 像资深顾问写的白皮书：逻辑、数据、措辞都站得住，经得起客户和领导推敲。
- **简洁克制** — 一页一个核心结论，留白优先；不堆字、不花哨、不靠装饰撑场面。
- **内容优先** — 视觉只为内容服务，该上图表上图表、该留白留白，不喧宾夺主。
- **通篇一致** — 全册一套规范，没有东拼西凑的模板拼贴感。

> 简言之：做的是「方案 / 报告」，不是「标准模板速成片」。

## 能做什么

技能的核心是一条八步流水线，每一步都为「最后那份 PPT 够不够专业」负责：

- **1 · 规范加载** — 装入品牌色值 / 字体 / 禁用项，全册照同一套规范走。
- **2 · 材料解析** — 把文档 / 数据 / 纪要拆成事实 / 数据 / 问题 / 结论，标来源、不编数字。
- **3 · 论点提炼** — 金字塔原理逼出一句话核心结论（灵魂句），让全篇有立场。
- **4 · 叙事骨架** — 先把每页标题排成论证链（Ghost Deck），定逻辑再填内容。
- **5 · 大纲版式** — 每页定要点和版式：数据上图表、流程上结构图，不页页堆 bullet。
- **6 · 样稿确认** — 先做 3–5 页样稿对齐方向，再铺全册。
- **7 · 逐页设计** — 按规范出图，工具链转成原生可编辑 PPTX。
- **8 · 质检交付** — 按清单扫颜色 / 字体 / 来源 / 节奏，修完再交付。

## 预览

三档视觉风格**共用同一套内容与组件，只切视觉层**：A 克制档（白皮书）· B 现代专业档（默认）· C 高表现力档（深色重音 / 竞标）。

<table>
<tr>
<td width="33%"><img src="assets/shots/theme-a-cover.png" alt="A 克制档"><br><sub><b>A · 克制档</b> · 极简白皮书</sub></td>
<td width="33%"><img src="assets/shots/theme-b-cover.png" alt="B 现代专业档"><br><sub><b>B · 现代专业档（默认）</b> · Hero + 章节块</sub></td>
<td width="33%"><img src="assets/shots/theme-c-cover.png" alt="C 高表现力档"><br><sub><b>C · 高表现力档</b> · 深色重音</sub></td>
</tr>
<tr>
<td width="33%"><img src="assets/shots/consulting-tree.png" alt="驱动树"><br><sub><b>驱动树</b> · 肘线分解 + 圈注 + 自洽校验</sub></td>
<td width="33%"><img src="assets/shots/consulting-dots.png" alt="点阵去向"><br><sub><b>点阵去向</b> · 48 队去向 + 细分条 + 圈注</sub></td>
<td width="33%"><img src="assets/shots/consulting-chain.png" alt="链式递减"><br><sub><b>链式递减</b> · 节点链 + 终点拆解 + So-What</sub></td>
</tr>
</table>

同一份真源一键换肤（Aham 蓝 ⇄ 黑·白·金三国色，v2.5 世界杯样张）：

<img src="assets/shots/consulting-skin.png" alt="同一真源换肤对比" width="100%">

> 历史样张与可编辑 PPTX（11 页示例 + 世界杯十页双配色）存档于 [v2.5.2 tag](https://github.com/Aham-AIAPP/aham-ppt/tree/v2.5.2/examples)；v3.0 起版式收敛为参数化函数，不再随仓库携带示例产物。

## 版式库

**36 个内容版式（6 个叙事系）+ 3 个特殊页，共 39 个版式 ID**，全部参数化——坐标由函数冻结，不再手画；数据图表 15 类、标注/异形 API 14 个。来源两档如实标注：可考原型注明出处（BCG / Minto / Porter / Ishikawa / Tufte / Shostack…），查不到的明确标「通用惯例 / 本库自设计」，不虚构。

> 🆕 **v4.0（2026-07）· 库瘦身增肌**：16 个通用页型（大数字 / 宣言 / 两三栏并列等）**退库改走栅格直排**（[`grid-composition.md`](references/grid-composition.md)，版式退库、纪律不退）——依据是 AI 布局能力边界（纯栅格稳定、锚点咬合不可靠），不是来源有无；同时落地调研缺口七式：**Harvey 球表（S-16）· 竞争格局弧（S-17）· 价值链（E-05）· 鱼骨图（G-04）· Impact-Effort（A-04）· 决策树（A-05）· 小倍数网格（V-05）**，决策树期望值与报价合计一样由调用方传入、函数绝不代算。

<details>
<summary><b>点开查看全部 39 个版式</b>（ID · 用途 · 来源，长图）</summary>
<br>
<img src="assets/shots/layout-catalog.png" alt="Aham PPT 版式总览：39 个版式的 ID、用途与来源" width="100%">
</details>

> 权威清单与选版决策表见 [`references/layout-library.md`](references/layout-library.md)；图片由 [`tools/layout_catalog.py`](tools/layout_catalog.py) 生成，版式增减后重跑即可。

## 开始使用

最简单：**把本仓库地址 `https://github.com/Aham-AIAPP/aham-ppt` 发给 Claude，让它把技能装好**；或下载本仓库后，把技能文件上传给 Claude。

装好后对 Claude 说「帮我做 PPT / 做客户方案 PPT」即可——技能会自动按八步法推进，开场先问你选视觉档（默认 B）。

---

## 更新记录

[Releases](https://github.com/Aham-AIAPP/aham-ppt/releases) · [CHANGELOG](CHANGELOG.md)（Keep a Changelog · SemVer） · [CONTRIBUTING](CONTRIBUTING.md) · [MIT](LICENSE)

## 关于 Aham

> 把灵光一现，做成能用的 AI 工具。Aham 来自 *aha moment*，每个工具只把一件事做利落。

| 应用 | 一句话 |
|---|---|
| [Aham UI](https://github.com/Aham-AIAPP/aham-ui) | 供 AI 消费的设计系统——写一次规范，AI 产出处处一致 |
| [Aham Word](https://github.com/Aham-AIAPP/aham-word) | 供 AI 消费的 Word 规范——AI 据规范产出处处一致的 .docx |
| [Aham Survey](https://github.com/Aham-AIAPP/aham-survey) | 现场调研工具（macOS）——本地优先，把现场对话做成结构化调研成果 |
| [Aham Voice](https://github.com/Aham-AIAPP/aham-voice) | 录音转写与会议纪要（macOS）——本地离线转写，纪要走你自己的模型 |
| **Aham PPT** | 克制的 AI PPT 制作技能——把素材做成方案级 PPT |

来源与脱敏说明见 [`ORIGIN.md`](ORIGIN.md)。

### 关注 · 交流

公众号看更多 AI 工具实践与更新；也欢迎扫码加我，交流与反馈。

<p><img src="assets/wechat-qr.png" width="640" alt="关注 Aham 公众号 / 加作者微信"></p>
