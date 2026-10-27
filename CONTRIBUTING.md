# 贡献指南

本技能以 MIT 许可开放，欢迎修改和二次开发。

## 改动约定

- 数值只在两处定义：`references/style-tokens.md` 和 `assets/html2pptx/components.js` 的常量。改一处时同步改另一处。
- 流程和文字规则与视觉规则分开。改一类时不顺手改另一类。
- 仓库公开，例子只用占位符，例如〈客户〉〈我方〉〈主系统〉。不写真实客户名、产品名、项目场景和数据。
- 提交走分支和 PR，提交信息写明改了什么。

## 验证

改组件、检查脚本或导出程序后，运行以下命令，结果写进 PR 描述：

```bash
cd assets/html2pptx && npm install
node demo/build.js /tmp/demo                       # 生成五页示例
node check_slides.js /tmp/demo --png /tmp/demo/png  # 应为 0 ERROR、0 WARNING
node html2pptx.js /tmp/demo /tmp/demo.pptx          # 导出
python ../tools/check_deck.py /tmp/demo.pptx --config ../tools/check_deck.example.json
```

- 新增或修改组件函数时，在 `demo/build.js` 里用到它，并看截图确认画法。
- 新增检查项时，先构造一页会触发它的页面，确认报出；再用示例确认没有误报。
- 改导出程序时，比较网页截图和 PPTX 渲染结果，位置和换行一致。

## 经验写进规则正文

实际使用中得到的经验，在当次改动里写进以下三处之一，不另建「补遗」或「教训清单」：

1. 代码：能由函数保证的写进组件函数，例如常量、默认值、参数检查。
2. 检查：能自动判断的写进 `check_slides.js`、`design_checks.js` 或 `check_deck.py`。
3. 规则：只能约束写作行为的，改写进对应规则文件的正文条目，并附用户否定过的原句作反例。

判断标准：新读者只读现行文件就能正确执行，不需要知道历史。演进过程只记在 `CHANGELOG.md`。

## 触发测试

改 `SKILL.md` 的 description 前后各做一遍：逐条假设用户只说这一句，判断技能是否应该触发。

应触发（12 条）：帮我做PPT；做个演示文稿；根据这份资料做PPT；做客户方案PPT；制作幻灯片；把这份材料做成汇报；
做一版给领导汇报的片子；做个路演deck；竞标方案PPT；项目复盘做成PPT；这周的成果整理成演示；做一页报价PPT。

不应触发（7 条）：写个Word周报；做个Excel报表；设计一张海报；做个官网或落地页；改一下现成 pptx 里的错别字；
做个PDF报告；「汇报一下进展」（口头汇报，没有制作意图）。

## 发版

1. 定版本号：不兼容的改动升主版本，向后兼容的新功能升次版本，修复升修订号。
2. 把 `CHANGELOG.md` 的 `[Unreleased]` 移入 `## [X.Y.Z] - YYYY-MM-DD`，按新增、变更、修复、移除分组，补底部的版本链接。
3. 推送后建 Release：`gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <notes.md> --latest`。
4. 社交封面不印版本号，版本由 README 的徽章显示。
