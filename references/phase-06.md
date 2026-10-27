# Phase 6 · 样页确认

入场条件：Phase 5 规划卡已确认。开始前加载 `html-slides.md`，读范例库 `assets/examples/README.md` 并看合格页和不合格页的截图。

**停等点**：先问用户有没有视觉上要避开的东西（如配色要低调、字要大一点）。没有就开始。

## 步骤

**1. 选 4 至 5 页**：按内容结构选，每页一种结构，覆盖本册用得最多的几种结构。
信息层级最多的一页和图形最复杂的一页必须在内。封面不算在内，用户要求时另加。

**2. 写样页**：用 `components.js` 写生成脚本，按 `design-principles.md` 设计，数值取自 `style-tokens.md` 和项目色表。

**3. 自动检查**：

```bash
node assets/html2pptx/check_slides.js deck/ --png deck/png
node assets/html2pptx/html2pptx.js deck/ 样页.pptx
python assets/tools/check_deck.py 样页.pptx --config 项目配置.json
```

ERROR 改完。WARNING 逐条改，或在自查表里写明保留的理由。样页阶段就导出 PPTX，导出问题在这里发现。

**4. 人工检查**：逐页填 `phase-07.md` 的七项自查表。方案类再按 `solution-deck.md` 6.2 的第 1、11、13、15、16、21、22 项检查。
把样页截图和范例库的合格页并排看，质感差距写进自查表。

**5. 给用户看**：把预览页发布为可分享的网页（如 Artifact），附：

- 每页的七项自查表。
- 自动检查的 ERROR、WARNING、INFO 条数和保留项。

请用户从三方面反馈：配色调性、信息密度、给客户看是否有信心。

**6. 修改**：用户指出具体问题时，先按 `phase-07.md`「修正记录」记进基线，再改页面。用户整体否定时先问清期望的风格，再重做。

## 完成卡字段

样页预览链接、每页的内容结构和自查表、自动检查结果、用户反馈和修正记录、确定的视觉基调（色表、元素选择、密度）。
待确认：视觉基调是否满意。确认后进入全量设计。
