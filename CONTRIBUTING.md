# 贡献指南

欢迎修改、重组、二次开发本技能（开放分发，MIT）。

## 改动约定
- **视觉/规范以 `references/brand-spec/` 为权威**：色值、字体、版式只从 `brand.md` / `tokens.css` 查表，不在其它文件写死色值。取值同步自设计源 [aham-ui](https://github.com/li599198347-svg/aham-ui)。
- **方法论与视觉分离**：八阶段流程、Action Title、探测场景等是方法论；颜色/字体/卡片是视觉。改一类不应顺手改另一类。
- 任何组件/骨架改动，按下方 §验证 与 §教训固化机制 执行。
- 提交走分支 + PR，提交信息沿用仓库既有风格（`feat:` / `fix:` / `docs:` / `chore:`）。

## 发版流程（SemVer + Keep a Changelog）
1. 定版本号：破坏性=MAJOR、向后兼容新功能=MINOR、修复=PATCH。
2. 把 `CHANGELOG.md` 的 `[Unreleased]` 内容移入 `## [X.Y.Z] - YYYY-MM-DD`，按 新增/变更/修复/移除 分组，补底部版本链接。
3. 提交推送后建 Release（自动打 tag）：
   ```sh
   gh release create vX.Y.Z --title "vX.Y.Z — 一句话主题" --notes-file <notes.md> --latest
   ```
4. 确认 README 的 Release 徽章动态显示新版本；**社交封面绝不印版本号**（版本由徽章动态显示）。
5. **对外物料统计核对**：重跑 `tools/layout_catalog.py` / `tools/build_pages.py` 前，先核对脚本内统计数字与组件实数一致（`charts.py` 图表函数数、`consulting.py` 公开 API 数、版式函数数）——这些数字曾漂移过（v3.1 修正）。

> **两个 tools 目录的分工**：`tools/` = 仓库发版物料脚本（README 长图 / GitHub Pages / 社交封面，需 playwright，与技能运行时无关）；`assets/tools/` = 技能运行时工具（lint_svg / pageno_fill / icons_preview）。

## 验证（改动的最低门槛）

- **组件级**：每个参数化函数必须有 (a) 渲染断言（关键元素计数/文本存在），(b) 负向测试（非法输入抛 ValueError）。
- **页级**：`python3 assets/tools/lint_svg.py <svg目录>` 五项预检全过（tofu / rotate / 精确超宽 / 页脚一致 / 中文引号）。
- **转换级**：`svg_to_pptx_wrapper` 转换成功，且 PPTX 形状数 ≥ SVG 元素数（空字符串文本被跳过属良性）。
- **回归级**：改动既有函数时，用受影响版式的成品页（如世界杯 deck 对应页）做像素 diff——默认路径必须字节级/像素级一致，除非改动本身就是要改渲染结果。

## 教训固化机制（禁止追加式教训堆）

## 触发评测集（v3.2 · 人工评测清单，改 description 前后各跑一遍）

> 技能无自动化评测 harness，本清单为**人工判定**：逐条设想用户只说这一句，判断技能应否触发。改动 SKILL.md description 后必须全量复跑并记录结果。

**应触发（12 条）**：①帮我做PPT ②做个演示文稿 ③根据这份资料做PPT ④做客户方案PPT ⑤制作幻灯片 ⑥把这份材料做成汇报 ⑦做一版给领导汇报的片子 ⑧做个路演deck ⑨竞标方案PPT ⑩项目复盘做成PPT ⑪这周的成果整理成演示 ⑫做一页报价PPT

**不应触发（8 条）**：①写个Word周报（→docx 技能）②做个Excel报表（→xlsx）③设计一张海报（→设计类技能）④做个官网/落地页（→前端）⑤要 SVG/HTML 版演示（→ppt-svg，description 已消歧）⑥帮我改一下这个现成 pptx 里的错别字（存量编辑→官方 pptx 技能文件操作）⑦做个PDF报告（→pdf）⑧「汇报一下进展」（口头汇报，无制作意图——**边界最模糊的一条**，误触发时优先收紧 description 的「做一个汇报」措辞）

任何实战教训**必须在当轮落到以下三选一**，不允许以"补遗 / LESSONS / 实测教训清单"等形式追加堆叠：

1. **代码级**：能由函数保证的，写进函数（常量锁定、布局规则、自动换挡），并配断言防回归；
2. **校验级**：能自动检查的，进 `tools/lint_svg.py` 或函数入参校验（抛 ValueError）；
3. **规范级**：只能约束生成行为的，**改写进对应规范文件的正文条目**（designer-rules / chart-impl / 各骨架章节），融入既有结构，不带"vX.X 补遗"字样。

判据：新读者只读现行文件就能正确执行，不需要知道任何历史。演进过程只记 `CHANGELOG.md`。
