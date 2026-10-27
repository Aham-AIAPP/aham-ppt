# Changelog 更新日志

本项目所有重要变更记录于此。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本遵循 [语义化版本 SemVer](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增
- `references/design-principles.md`：七条版式设计原则和检验方法，附内容结构与图形举例表。全部文稿类型适用，取代版式库查表、栅格坐标冻结和节奏阈值。
- `assets/html2pptx/`：网页幻灯片路线。`html2pptx.js` 把 1920×1080 绝对定位的 HTML 幻灯片导出为可编辑 PPTX（文字、形状、连线为原生对象，图标和内嵌 svg 为图片，`<aside>` 进备注）；`preview.js` 合成单文件预览页；`check_slides.js` 在浏览器里检查字号、溢出、越界和文字重叠，可出缩略图总览。写法见 `references/html-slides.md`。
- `references/phase-common.md`：八个阶段共用的固定动作、完成卡格式、跳过后果和工作区文件。
- `assets/tools/extract_outline.py`：把 PDF、Word、PPT、Excel、Markdown 转成提纲（章节、位置、字数、含数字的句子），Phase 2 先看提纲再读命中章节。
- `references/solution-deck.md`：方案类 PPT 规范。覆盖三种形态（通用方案、项目方案、整体规划方案）的章节骨架、固定页组（模块三页组、场景两页组、建设内容详解页）、全景与详解的对应、页面分区、字号阶梯、语义色表与图例、方案专用文字规则，按内容结构设计版式的对照表，以及 22 条交付前人工检查清单。规则提炼自三份真实方案及其逐版修改记录，文件内全部用占位符。
- `assets/tools/check_deck.py`：读 .pptx 自查字号、颜色、逗号分句、禁用词、「第 N 页」引用、内部编号、编号跳号、术语表和子标题格式；输出标题通读表、页码引用表和数量说法表。可用 JSON 配置项目色表、字号、术语表和观察词。

### 变更
- 生成路线改为「AI 写 HTML 幻灯片 → 网页预览 → 导出 PPTX」。SVG 转 PPTX 工具链、版式库、栅格、SVG 骨架、三档主题、designer-rules 移出主流程，文件保留并加「参考素材」表头。
- 八个阶段文件只留入场条件、停等点、步骤和完成卡字段；SKILL.md 从 18,209 字减到约 4,200 字，原「文案措辞」附录移入 `wording-rules.md` 第七节。
- Phase 2：信息清单写进基线文件，后续阶段只引编号；搜索最多 3 次；不单独停等，清单与 Phase 3 的灵魂句一次确认。同一客户再做时读已有清单。
- Phase 5 规划卡改填「内容结构、图形设计、参考（可空）」；Phase 6 样页加遮标题检验；Phase 7 坐标按内容自定。
- 颜色：保留一色一义并配图例，去掉「至多 3 个语义色」的上限。字号：去掉阶梯，改为最小 9pt、全册不超过 8 级。
- `check_deck.py`：去掉字号阶梯和色表比对，改查最小字号、字号级数、多强调色页的图例色块，并列出每页强调色。
- `solution-deck.md` v1.3：删去字号阶梯、四种页的参考构成和版式库对照表，版式改按 design-principles。
- Phase 1 受众卡增加「文稿类型」，选「方案」时加载 solution-deck.md，并要项目色表和术语表。
- 方案类 PPT 的标题改为名词短语加结论子标题，强调色放宽为至多 3 个语义色，正文字号改为 9–13 pt；只对方案类生效，wording-rules、phase-04、theme-tiers、brand.md 各加一处指针。
- Phase 8 增加步骤 1.2「方案类自查」。

## [4.0.0] - 2026-07-03 — 库瘦身增肌（通用页型退库直排 · 调研缺口七式落地）

依据：全量对标评估（40 版式移出/替换/保留决策）+ 深度调研报告（Gap Analysis and Source Upgrade）+ 用户三项拍板（移出 16 认可 / AI 能力边界判据认可 / 决策树与小倍数加入）。

### 破坏性变更（MAJOR）
- **16 个通用页型移出版式库**（S-01/S-04/S-05/S-06/E-01、I-01/I-05、T-01/T-02/T-03、S-03/S-08/S-12、A-01/A-02/G-02），`svg-skeleton-t.md` 删除，`layouts.py` 删除对应 13 个函数与 3 个整页 helper。移出判据=AI 布局能力边界（LaySPA 2509.16891 / GeoSVG-RL 2605.25447：纯栅格稳定、锚点/落位/咬合不可靠）而非来源有无——故 E-02/E-03/G-03 虽"无原版"仍保留。
- 新增 `references/grid-composition.md`：直排流程 + **16 个移出页型的结构要点与纪律收编**（版式退库、纪律不退：大数字禁悬空、语录须可考、宣言须断言句、图占比 40–75% 等）+ 季度复核回退条款。phase-05 改**两级选择逻辑**（命中触发条件查表 / 低自由度内容直排不查表）。

### 新增（调研落地七式，36 内容 ID + 3 SPC = 39）
- `structures.harvey_table`（S-16，Poppel @ Booz Allen 1970s；0–4 五档硬拦、图例默认必配）
- `structures.competitive_arc`（S-17，弧带型竞争格局，结构对标 Forrester Wave 2002 · **去品牌化+商标纪律**；3–12 家、size 1–3 硬拦）
- `structures.value_chain`（E-05，Porter 1985；主活动 3–6/支持 2–4 硬拦）
- `structures.fishbone`（G-04，Ishikawa 1960s/ASQ 6M；3–6 骨、子因 ≤4 硬拦，子因文字水平放置守约束7）
- `structures.impact_effort`（A-04，无单一可考原版·通用优先级工具族如实标注；2–12 项硬拦）
- `structures.decision_tree`（A-05，Magee HBR 1964；2–4 支、概率分支 ≤3 硬拦，**EV 调用方传入函数不代算**）
- `charts.small_multiples`（V-05，Tufte 1983；4–12 格、各格点数一致、**全局共享 Y 尺度函数强制**）
- 渲染断言 8 项 + 负向拦截 13 项全部通过。
- S-02 语义预设 2 个（不占 ID）：Power-Interest（Mendelow 1991）、四象限竞争定位（商标纪律同 S-17）。

### 变更
- `lint_svg.py` 页脚豁免条件 2 页→8 页（多章 deck 的章节进度页数可达 8，原条件误报 5 章样例）。
- **43 页版式陈列样例 deck 交付**（36 内容 ID 每页一次真实函数调用=调用关系端到端验证 + SPC 3；制造业售前演示数据，页脚统一声明"非真实客户"）：lint 五项、右缘红线 43/43、PPTX 形状数 43/43 全过；**图像目检通道本轮恢复**，抽检 Harvey/鱼骨/价值链/决策树/竞争弧 5 页人工目检通过。
- 样例实测回灌 2 项修复：`service_blueprint` 增加格子类型硬校验（元组/非字符串抛错——两版样例 deck 实测踩坑：传 (泳道名, 列表) 元组被静默渲染成列表字符串上屏）；`driver_op` 兼容 Unicode ×/÷/−（映射至 x / / / -）。均含负向+正向验证。
- 调用关系六项全检（清单↔章节双向、文档引用函数存在性、死 ID、死函数残留、速查表、grid-composition 引用）修复后清零。
- 来源栏升级 6 条：Minto 锚定 1996 版（弃 1978 说）、E-91 补 McKinsey Enduring Ideas 2009、S-02 补九宫格 McKinsey Quarterly 2008（Kevin Coyne）、RACI 改"无单一可考发明人 1970s 通行"、Zelazny 补全书名/出版社/1985 初版、瀑布加注 McKinsey 1990s 普及。
- 调研判定"不建议"照办：商业模式画布不做（专有内容框架非通用版式）、雷达维持不落地；Kearney 整合曲线入候选池待需求（M&A 场景与制造业售前不对口）。
- 对外物料同步：build_pages 39 版式口径、catalog 15 类图表；SKILL 组件清单追平实数。


## [3.2.0] - 2026-07-03 — 审计增强批（对标缺口补齐）

> 依据2026-07-03 四路专家审计的第三批。

### 新增
- **S-14 团队页 / S-15 报价页**参数化版式：`layouts.team_grid`（2–8 人硬拦，照片一律 placeholder 占位不硬编假头像）/ `layouts.price_table`（1–8 行硬拦，**合计由调用方传入、函数绝不求和**）；入 layout-library 决策表+速查表、svg-skeleton-s 五栏章节；版式库 46→48 ID、layouts 19→21 式（渲染断言+负向测试+转换实测通过）。
- **tokens.css §11 文字前景×背景允许组合表**：17 组组合全部脚本实算登记；新增任何组合必须先实测入表，QC 按表判定（对标 Carbon 的结构化对比度治理，堵住 P1 对比度失守的根因）。
- **讲者备注链路**（presenting/hybrid）：phase-05 规划卡增「讲者备注」字段，phase-07 转换后经 python-pptx 写入备注栏（Duarte「页面留冲击、内容进备注」的后半环）。
- **phase-08 步骤1.5 渲染目检**：soffice 出图逐页目检重叠感/拥挤感/节奏（对标官方 pptx 技能渲染 QA 闭环；LibreOffice 缺失则记录跳过）。
- **CONTRIBUTING 触发评测集**：12 条应触发 + 8 条不应触发的人工评测清单，改 description 前后必跑。
- **C 档内容层张力规则**（phase-04）：每章 ≥1 组「现状→愿景」对比结构（对标 Duarte sparkline；与深色重音页编排合并执行）。

### 变更
- pptx-native-rules 增「**编辑语义边界**」节：如实披露标签级文本框（改长不回流、bullet 非列表语义、~字号×0.1px 左移）+ 交付话术模板。
- theme-tiers 增**换肤纪律**：深底必须走 `--ppt-surface-dark`，禁手写近似值（登记 docs 演示图 #171717 漂移实例）。

## [3.1.0] - 2026-07-03 — 审计修正批（13 项 P1 + 22 项 P2）

> 依据2026-07-03 四路专家审计的第一、二批。

### 修复（P1，全部经断言/实测验证）
- **降级基线统一**：删除 phase-01「通用商务模式」第二套标准（#1A3C5E/#4A7CAB 双蓝体系与微软雅黑标题），降级唯一指向 SKILL §降级基线。
- **孤儿规范接线**：quality-audit-protocol / pptx-native-rules 由 phase-07/08 显式 view；转换代码段唯一维护处收敛到 phase-07；质检权威分工声明（视觉详单归 QAP、机判项归 phase-08 L2），消除双头。
- **删除跨环境硬编码** `view /mnt/skills/public/pptx/SKILL.md`（该路径仅存在于 claude.ai 容器，且官方 pptx 技能的配色/装饰指令与本体系直接冲突），改为条件化说明；phase-07 `sys.path` 默认值改为显式坏值强制替换。
- **依赖声明**：新增 `requirements.txt`；SKILL 增「依赖」节（python-pptx/cairosvg 必装、LibreOffice 可选及降级话术、字体回退现实说明）。
- **Action Title 上限 20→30 字**：修复「规则 ≤20 字 vs 自家三个好示例全部 22 字」的内伤；phase-04/06/07/08 四处同步。
- **纵向逻辑门禁全模式化**：Ghost Deck 四项测试扩为五项（测试5 · 证据配对，红色论点不得进 Ghost Deck，**专家模式不豁免**）；phase-08 L1 增「标题↔证据支撑，超卖页判 ERROR」；修正 phase-02 与 phase-04 的描述矛盾。
- **专家档合并闸门**（coach-engine）：强制停等从 ~18–20 次降至 ≤10 次；P3 灵魂句、P6 样稿任何档位不可合并；只减停等、不减任何测试/质检。
- **EQ 栅格真等分**：三列 380/380/408→**389/389/390**、四列 277×3+321→**288×4**、二列 590/594→**592×2**（grid-system、layouts.py、svg-skeleton-s、HERO-2/3/4 全同步；汉字字数表列宽更名；端到端实测 PPTX 落地 288×4）。
- **Chrome 规格统一 32px/y78/线94**：themes.chrome 由 26px/y74/线90 追平 common 骨架（=tokens `--ppt-title` 24pt；icon_circle 圆心 66→70 随基线对齐；实测落地 sz=2400）。
- **S-09 高阶网格越界修正**：388×224@x=40/452/864（右缘 1252 越线）→ **384×224@x=40/448/856**（缝 24、右缘恰 1240）；lint_svg 新增 **rect/polygon 越界检查**（整页背景豁免；负向测试通过）。
- **内容区口径唯一化**：红线 h=590（底 y=690，与页脚线对齐），分栏 h=580 为排版目标；svg-skeleton-v「540±」同口径。
- **页脚/来源/页码/轴标签升 ink-2** `#6E6E6E`（5.10:1）：themes 页眉页脚、charts 全部信息性文字（11 处）、common 页脚模板、designer-rules 来源模板与白名单表述、brand §2.2、track-rules 铁规改写（「任何承载信息的文字 ≥4.5:1；ink-3 仅限装饰」）。
- **C 档深底字色达标**：信息性小字 LT3 #787878（3.86:1）→ LT2 #A8A8A8（7.17:1）；封面导览蓝编号 #336EE8（3.27:1）→ **ACC_HOVER #5C8BED**（4.59:1，tokens 登记 `--ppt-dark-accent-info`）。
- **图表非文字对比（WCAG 1.4.11）**：面型数据元素+图例统一 **1px #6E6E6E 描边**（charts.py `EDGE` 常量，chart-impl/brand §7.5/QAP 同步）；slope 非高亮线与 sparkline 主线 INK3→INK2（执行中补充决定，线型元素无法用描边通道）。

### 变更（P2 · 口径对账）
- 图表口径单一源：phase-05/07 的「9 类」内联枚举改为 **14 类全量** + 指向 layout-library 速查表/chart-impl 权威清单。
- tokens §10 改为 **SVG px→PPTX pt 落地对账表**（`--ppt-body` 15pt→10.5pt 等，标注旧值为已废弃的手写 python-pptx 轨遗值；与 smoketest 实测 sz 一致）；大数字收敛双档（内容页 44–60pt / I-01 整页 127.5–135pt，grid/brand/tokens/skeleton-i 四处互引）。
- KPI 网格等分并文档追平代码：2×3=**373/373/374**（缝40，kpi_six 同步）、2×2=**592×2**（缝16）、1×3 缝 36→**32**（归 4 基阶）；右缘一律 1240。
- 字体栈顺序统一 **PingFang 优先**（tokens 与 brand/designer-rules/common/产线一致）；pt/px 单位统一（designer-rules ≥80pt→≥107px、≥60pt→≥80px）。
- 实现层 3 个白名单外色值收编 tokens §10（#2E2E2E 章节水印 / #333333 金句引号 / #F7F8FA 占位框底），QC 白名单同步；图标自绘例外正式登记（iconography：icons.py 为转换兼容自绘 Lucide 近似，QC 放行）。
- 「Inter→Calibri」回退承诺改为如实表述（PPTX 不嵌字体，替换由 PowerPoint 决定）；行距 1.3→**1.35** 归 `--lh-snug`。

### 变更（P2 · 方法论）
- phase-04 增**论证模式选择**（归纳分组默认 / 演绎链 ≤3 环）+ **Minto 四排序**（演绎/时间/结构/重要性）；**论点→页面折算规则**明文化（第二层论点=章节、证据 1–2 条/页、页数按受众顾虑加权）。
- phase-02 增**关键信息冲突登记**（关键数据冲突强制用户裁决后才进 P3）；《项目基线》机制提入正文引用。
- 一页一消息判据升级为语义判据（两个可独立证伪的断言；词表降为提示信号，单结论多依据不拆）。
- phase-03 锚点改为**增量确认**（引用 Phase 1 初检答案，消除逐字重复提问）。
- 受众卡增可选「**次要受众/否决点**」字段；phase-04 测试3 增次要受众顾虑核对。

### 变更（P2 · 工程卫生）
- `tools/build_pages.py` 移除硬编码个人路径（改 `AHAM_DOCS_ROOT` 环境变量，缺失即报错退出）。
- 对外物料统计追平实数（catalog：14 类图表/14 标注 API/45 内容版式；build_pages：48 版式/21 函数）并入 CONTRIBUTING 发版核对清单；两个 tools 目录分工写明。
- SKILL 增 **references 索引表**（全部文件→何时读）；Step 1 不再预载 designer-rules（473 行下沉至 Phase 6/7）。
- CHANGELOG 规范化：2.6–2.8 补 compare 链接与「随 v3.0.0 发布」注、删除尾部游离 v2.5 段、补 v1.0.0 说明。
- brand §5/§6 跳号说明；theme-tiers 补齐 **A/B/C 三列完整对照表**；基线坐标学注解（26/30/58 与 4 基间距阶的关系）。

## [3.0.0] - 2026-07-03

大版本主题：**全量参数化 · 历史产物清零 · 教训固化去补丁化**（用户三项整改决策 + 5 个确认点全落地）。43 内容版式实现路径收敛为：`layouts.py` 19 式（新模块）+ `structures.py`/`consulting.py`/`charts.py` 结构与图表 + 5 个栅格直排；**全库无照抄式冻结骨架**，7 个骨架文件全部重写为五栏格式（用途/适用场景/用法/来源/纪律），来源两档如实标注。明细见下方批次 0–5 条目。

### 3.0.0 · 批次 4

### 新增
- `layouts.py` A·G 组 5 函数：`three_steps`（固定 3 步硬拦，末步深色）、`option_ab`（A/B 两项，B 自动降调）、`action_table`（3–6 行硬拦）、`pillars`（2–4 柱硬拦，3 柱精确复现骨架）、`pyramid_light`（3–5 层硬拦，4 层精确复现含引线查表）。负向 4 项通过。
- 回归：5/5 字符级一致；deck 改调后 **md5 字节级一致 5/5**。过程更正 2 处如实记录：pyramid_light 初版比例取整（165.1 vs 165）与引线终点记忆错误（960/970 系已删骨架原值，deck 实际统一 1000/1010），均以 deck 为基准修正。
- `svg-skeleton-a.md` / `svg-skeleton-g.md` 全文五栏重写（A 系 5 ID + G 系 7 ID）；来源沿用调研出处（RACI=PMBOK/Wikipedia/Cornell、A-90=调研1+BCG 分桶、G-90=Matthies、G-91=Minto、G-92=Shostack/Zeithaml-Bitner/NN·g、G-93=Bain 合理杂交）。

### 3.0.0 · 批次 3

### 新增
- `layouts.py` E 组 3 函数：`concept_curve`（三段形态与语义色冻结，3 段硬拦）、`stage_flow`（3–6 段，4 段精确复现骨架坐标）、`tri_layer`（固定 3 层硬拦，>3 层分工给 arch_layers）。负向 3 项通过；回归 3/3 字符级一致（tri_layer 修正为层-箭头交错顺序后达成）；deck 改调后 **md5 字节级一致 3/3**。
- **设计修正（如实记录）**：V-02/V-04 不新建包装函数——其参数化实质即 charts.py 直调，额外壳属零价值函数（与审计①清理精神一致），偏离原方案映射表，已在骨架文档写清直调用法。
- `svg-skeleton-e.md` / `svg-skeleton-v.md` 全文五栏重写（E 系 6 ID + V 系 8 ID）；V-93 标注 BCG 达拉斯为本库最强单一可考原型，V-94/E-91 等沿用调研出处。

### 3.0.0 · 批次 2

### 新增
- `layouts.py` S 组 6 函数：`quad_cards`（固定 4 格硬拦）、`milestone_axis`（节点 3–5 硬拦）、`hero`（**支撑数硬拦 2/3/4**，依据 grid §3.6 三档栅格，用户拍板）、`versus`（行 3–5 且左右等长硬拦）、`kpi_six`（≤6 硬拦）、`full_panel`（bullets/body 二选一硬拦）。负向 5 项通过。
- 回归：新函数 vs deck 旧页 body 字符级比对 6/6 一致（S-03/S-09/S-12 为前缀比对，组合层在调用侧）；deck 改调 layouts 后重建 **md5 字节级一致 6/6**。
- `svg-skeleton-s.md` 全文重写为五栏格式（11 ID：4 直排 + 6 参数化 + S-13 组合配方）；来源两档如实标注（S-02 谱系=BCG/GE-McKinsey；S-07=Minto 金字塔原理版式化；S-09 高阶=Few 并注明品牌有意偏离；S-13 沿用调研1"无单一可核查原版"）。

### 3.0.0 · 批次 1

### 新增
- `assets/components/layouts.py` 新模块（整页型手画版式的参数化层，坐标冻结自骨架规范）：`bignumber`（I-01 双变体合一，基础变体 compare_anchor 必填硬拦、带证据变体固定 3 条硬拦）、`time_window`（I-05）、`quote_page`（T-01）、`declaration`（T-02）、`bridge`（T-03）。负向测试 2 项通过。
- **字符级回归**：用世界杯 deck 数据调新函数与旧手画页逐字符比对——04/05/08/22/30/39 六页完全一致；07_T-01 唯一差异为旧页被深底盖住的冗余白底 rect（新函数消除，视觉等价）。deck build 已改调 layouts（吃自身狗粮），重建后 md5 回归通过。
- 调研结论（如实）：大数字页为 MBB 通用惯例（多家对 McKinsey 公开 deck 的归纳佐证），**无单一可考原版**；T 系过渡页同为通用商务惯例。
- `svg-skeleton-i.md` / `svg-skeleton-t.md` 全文重写为**五栏统一格式**（用途/适用场景/用法/来源/纪律），删除冻结 SVG 块——确立后续批次的章节标准。
- 归一假设更正：T-01 与 `themes.quote_dark` 经读码确认为不同页型（过渡引言 vs C 档金句），**不合并**，文档已写清分工。

### 3.0.0 · 批次 0（清理与教训归位）

依据：用户整改决策（全量参数化 / 历史产物清理 / 教训固化去补丁化），详见后续批次条目。

### 移除
- `examples/` 整目录（11 页早期示例 SVG、demo pptx、preview、构建脚本、consulting/demo_d 与 FIFA26 十页真源、render_shots.py）；README 图墙段（引用的 assets/shots/ 目录早已不存在，属断链）。demo_d 的冒烟基线职能由「渲染断言 + 负向测试 + lint + 形状数比对 + 像素回归」验证体系取代（svg-skeleton-common §冒烟基线已改写，机制见 CONTRIBUTING）。恢复途径：aham-ppt-v2.8-backup.skill。
- `LESSONS.md` 删除。处置明细：FIFA26 七条中六条确认已固化于代码（BOUNDS/图例右上/引线反转/check()/tick_label/lint 名单），第六条的规范部分（图表底部≤2 层）归位 `chart-impl.md`；MES 六条确认固化于 lint/tools/quality-audit-protocol；工具链系数摘录以源码为准无需归档。
- **已知缺失（如实记录）**：LESSONS 索引的探测类场景 1–12 与专业判断类 13–14（数字诚实校验、矛盾一致性全扫描、延续 vs 重构边界、甲乙方责任边界等）——其完整正文原载 probing-scenarios.md / professional-judgment.md，该批文件在更早的历史重构中已撤销且正文未迁入 coach-engine/phase（本次逐项 grep 证伪了 LESSONS 头部"已分散到现行文件"的自述）。**正文已丢失，无法归位**；如需恢复须重新编写。

### 变更
- `designer-rules.md` 约束7 重构：撤销"实测补遗/v2.x"补丁式标题与叙事，按 变换/箭头/字符/文本间距/可用路径能力 五主题重组为正式规范条目（内容零删减）。


## [2.8.0] - 2026-07-03

> 随 v3.0.0 一次性提交发布，无独立 git tag；compare 链接指向 v2.5.2→v3.0.0 区间。

用户整改决策批次（7 项拍板全落地）。

### 新增
- `swimlane_roadmap` 三渲染模式（调研1 建议 `mode="gantt"|"chevron"|"phase_bucket"`）：gantt 默认行为与 v2.7 逐字节一致；chevron 块画雪佛龙形（相位推进）；phase_bucket 为 BCG 达拉斯式相位分桶（默认五桶 立即行动/速赢/战略优先/中期举措/长期机会，禁 today/milestones，日期不确定时比假装精确更诚实）。三模式渲染断言 + 2 项负向拦截实测通过；**未做视觉目检（本会话图像通道故障）**。
- `lint_svg.py` 页脚检查加章节进度豁免：总页数取众数，少数派 N≤20 且 ≤2 页判为 themes.section 章节进度并点名豁免（消除历史误报）。

### 变更/清理
- `components.py` 删除 6 个全仓零引用函数（big_btn/blueprint/device_screen/kpi/phone_screen/swimlane）；`placeholder` 确认在用（E-01 图占位）予以保留，并在 svg-skeleton-e.md E-01 直排指引补引用入口。
- `themes.py` section A 版删除无效空文本占位（渲染零变化，消 empty-text 警告）。
- `layout-library.md` 节奏约束新增「版式陈列册」场景豁免条款；A-90 行与速查表同步三模式（新增"日期不确定→phase_bucket"触发行）。

### 决策记录（不改）
- PDF/LibreOffice 字距放大 ~10% 的观察不写入规则：转 PDF 非主要目的，按该口径收缩会反过来影响 PPT 排版（用户拍板）。PowerPoint 实际字距未验证，以实际打开为准。


## [2.7.0] - 2026-07-03

> 随 v3.0.0 一次性提交发布，无独立 git tag；compare 链接指向 v2.5.2→v3.0.0 区间。

依据：2026-07《版式库全量对标评估》P0–P2 替换决策 + 第一批调研（5 类咨询版式）+ 第二批调研（6 类咨询图型）。
上轮（v2.6）遗留的替换升级与新增版式本轮全部落地。

### 新增（代码）
- **`assets/components/structures.py`（新模块，咨询结构版式层，15 API）**：
  - 共享引擎：`grid_cells` 网格对齐（RACI/服务蓝图复用）；`issue_tree` 内置树对齐（根/支/叶三列、父居中于子组）。
  - 记号：`milestone` 里程碑菱形 / `gate` stage-gate 三角 / `flag_line` 标志虚线（路线图与 fte_ramp 共用）。
  - 推算件：`mini_table` 三线表 / `bridge_arrow` 显式乘数桥 / `footnote_band` 方法论脚注三件套（BCG 式）。
  - 结构版式：`portfolio_matrix`（气泡面积∝规模 r=10+24√(s/max)、迁移虚线箭头、grid=3 九宫格、自动画"气泡面积∝X"诚实标注）、`raci_matrix`（**强制校验每行恰好一个 A**，违反抛 ValueError；字母+灰阶双通道）、`issue_tree`（MECE 组间虚线分隔、末端假设=虚线框+「假设」角标）、`arch_layers`（层高∝weight、层内模块网格 1–2 行、纵向能力条=**单字逐个 text 堆叠非 rotate**、层间双三角接口标记）、`swimlane_roadmap`（3–6 泳道、committed/planned/proposed 三态、里程碑在轴头、Today 线、依赖肘线）、`service_blueprint`（**固定 5 泳道 + 3 分界线按 NN/g 位置**：客户|前台=互动线、前台|后台=可见性线、后台|支持=内部互动线；行数≠5 抛错）、`layered_pyramid`（梯形层内切格 + 右侧逐层 takeaway 引线）、`argument_ladder`（横向 buildup 默认 / 纵向变体）、`concentric_arcs`（**降级工具：不接受数值**，≤5 层，强制绘制「弧径不代表数值」）。
- **`charts.py` 追加 5 函数（追加式，既有 9 图表零改动）**：`sparkline`、`kpi_card`（Few 式：值+基准+sparkline+状态）、`marimekko`（gap=0、列宽∝列总量、wlabel 必填强制画出、≤7 列/≤4 段抛错、pct/abs 双模式）、`fte_ramp`（**<10 期自动堆叠柱 / ≥10 期堆叠面积**（Datawrapper 规则）、stage-gate、图例右上）、`horizon_curves`（3–4 条 S 曲线 path 折线、强制「概念示意·无刻度」）。
- **`consulting.py` 追加 `driver_op`**（G-90 可选算子 ×÷+−，纯线画；实证仅 ~4% 显式建模——默认不加）。

### 死代码/冗余审计修复（2026-07-03 审计①，全部零行为变化）
- `components.py`：删除 L94 不可达 `placeholder`（"真实照片占位框"，自 v2.2 起被 L132 同名"软件界面占位框"覆盖从未生效；如需照片占位从 git 历史恢复并改名）。**更正上文"components.py 零改动"声明——本次审计清理属例外。**
- `consulting.py`：删 unused import `SANS`；删 `flow_bands` 内被覆盖的 `thh` 死赋值（v2.6 发现、本轮清）；删 `driver_node` 内 no-op replace 块。
- `structures.py`：删 unused import `esc`/`check`。
- pyflakes 全组件模块清洁；**遗留待决**：`components.py` 的 big_btn/blueprint/device_screen/kpi/phone_screen/swimlane/placeholder 共 7 个函数在本技能代码与文档中零引用（疑似 ppt-svg 姊妹技能共享残留），未删除、待用户决策。

### 变更（版式库，46 个 ID）
- **同 ID 高阶变体（轻量版并存）**：S-02（+portfolio_matrix）、S-09（+Few 卡）、A-03（+标准 RACI）、E-04（+arch_layers）。
- **同 ID 替换**：G-01 手画树骨架撤销→参数化 issue_tree（树对齐是 AI 弱项，评估 P0 重度）；V-03 图左+洞察右撤销→图上直接标注（Knaflic "Label data directly" pp.176–181）。
- **纪律追加**：V-04 图上标注差异原则；G-90 可选算子配方（含 4% caveat）。
- **9 个新版式**：S-13 勾选盘点（组合配方，调研注明无确切一手原版）、E-91 三地平线、V-93 推算双栏（BCG 达拉斯第 11 页蓝本）、V-94 Marimekko、A-90 泳道路线图、A-91 FTE 爬坡、G-91 论证阶梯（Minto）、G-92 服务蓝图（Shostack 1984/NN-g）、G-93 剖面金字塔（Bain/Keller 形态；层内切格+右侧箭头复合结构调研注明为合理杂交）。
- **不落地**：雷达图（layout-library 新增 §不提供的图型：Zelazny 体系外 + Few 2005 + 轴序/面积失真三缺陷；替代 hbar 分组/bullet/slope）；同心弧仅降级定性（Aon 2025 Investor Day Slide 69 系品牌叙事非数据图）。
- 划界指针更新：E-02→E-91、G-03→G-93；速查表新增 13 行触发条件；`svg-skeleton-common.md` D 段纳入 structures.py 与通用记号/footnote_band。
- 修复存量 bug：`designer-rules.md` L292 嵌套围栏导致全文件代码块开闭错位（v2.5.1 起即有，本轮围栏配对校验发现）。
- `designer-rules.md` 约束7 新增第 6 条实测补遗：path 折线/path A 圆弧/polygon+opacity/circle 经 E2E 确认存活。

### 有意偏离（记录在案）
- **Few「状态色」→ 符号+文字双通道**（+/− 号 + 达标/未达）：brand 图表铁律禁红绿，kpi_card 按此适配并在骨架章节标注。
- **归系与调研建议不同**：horizon_curves 入 E 系（调研建议 T/S；因 E-02 划界指针已指向它）、layered_pyramid 入 G 系（调研建议 S；与 G-03 划界共处）。
- 版式计数口径：保留 5 个栅格直排 ID（v2.6 决策），故总数 46 而非评估文档估算的 ~42。

### 验证（全部真实执行）
- 16 页示例视觉渲染（cairosvg PNG）逐页目检；过程中修正 9 处：服务蓝图分界线错位一层（对 NN/g 规范）、泳道依赖肘线断裂、里程碑标签与刻度碰撞、fte_ramp 底部三层拥挤（图例移右上）、同心弧引线交叉（外环对顶行）、纵向阶梯箭头瞄准、峰值标签出界、GRAY_B/math 引用错误。
- 端到端：16 页 SVG→svg_to_pptx→PPTX→LibreOffice PDF→PNG 抽检 8 页，path A 弧/path 折线/polygon opacity/circle 全部存活。
- 15 项负向/属性测试全过：RACI 双 A/零 A/列数/非法记号、Mekko 8 列/5 段/abs 缺宽、蓝图 4 行、同心弧 6 层、地平线 2 条、算子非法、fte 期数不齐各抛错；fte n=9→柱 n=12→面积自动换挡、Mekko 列宽 1:3 比例、气泡 r=10+24√(s/max) 属性断言。

## [2.6.0] - 2026-07-02 — 版式库对标改造 · 结构层（D 层归系 + 移出/合并/划界）

> 随 v3.0.0 一次性提交发布，无独立 git tag；compare 链接指向 v2.5.2→v3.0.0 区间。

依据《aham-ppt 版式库全量对标评估（40 版式）》与 D 层调用链路分析执行。**纯文档重组 + 纪律固化，consulting.py / charts.py 代码零改动，无新增绘图。**

### 变更（D 层归系 · Wave 0，修复"有执行入口、无选择入口"断点）
- **90 段版式骨架归入各系文件末尾章节**：E-90→svg-skeleton-e、V-90/V-91/V-92→svg-skeleton-v、G-90→svg-skeleton-g、I-90→svg-skeleton-i（各含组件签名+组合配方+分工/纪律）。
- **layout-library**：90 段进各系表格；**速查表新增 6 行触发条件**（阶段带量→E-90、多源汇总→V-90、逐指标对比→V-91、配额规则→V-92、指标数学分解→G-90、收敛到1→I-90），"唯一权威决策表"口径自此闭合；D 层附录删除。
- **svg-skeleton-common**：并入 D 层横切部分——降方卡味三原则、标注层 5 API、密度纪律+标注配额+chrome红线+蓝的记账、冒烟基线。
- **designer-rules 新增约束7**（原 skeleton-d §4 五条 PPTX 实测补遗）；pptx-native-rules 速查表补 2 条。
- phase-05/phase-07 例外句改写：90 段走"版式ID=章节名"常规路径，不再特例指向独立文件。

### 移除
- **`references/svg-skeleton-d.md`**（内容全部拆并，无信息丢失；LESSONS/SKILL 指针已更新）。
- **5 个纯栅格版式的冻结 SVG 骨架**：S-01/S-04/S-05/S-06/E-01 改**栅格直排**——各系文件保留同名章节，写明 grid-system §三 坐标 + skeleton-common 构件 + 直排纪律（评估判定：纯栅格无隐性对齐约束，AI 在栅格+字号规范下可稳定生成；反复画错可整段回退）。

### 合并（不增计数）
- **S-10/S-11 → S-07 参数化 HERO（N=2/3/4）**：三变体代码块原样保留于同一章节，坐标即 grid-system §3.6 三行。
- **I-04 → I-01 参数化大数字页（0–N 支撑）**：基础/带证据双变体；**新增内容纪律**：`[compare_anchor]` 必填（同比/目标/基准三选一，原 [support_1] 位，坐标未动）+ 来源脚注必填（评估 P2）。

### 划界（写进适用场景列，不引用未落地版式）
- S-03 限定轻量单轴（多泳道/阶段底色带不属本版式）；E-02 限定单条概念曲线（三地平线类多曲线叠加不属本版式）；G-03 限定纯层级金字塔；V-04 与 V-91 分工（逐指标对比优先 V-91）。

### 核查（V-90 数据诚实性，评估要求项）
- `flow_bands` 读码+脚本实测：源侧条高与汇侧带宽对测试值 50/30/15/5 均严格 10:6:3:1，汇侧带宽合计=汇总块内高——**带宽∝数值成立，无"为美观调宽"问题**；带体锥形是汇入汇总块的既定形态。
- **缺口**：target 数字由调用方传入，代码不校验 =Σsources；守恒纪律已写入 V-90 骨架章节（损耗须列显式 source 行）。另：flow_bands 内有一行被立即覆盖的死代码（`thh` 首次赋值），无功能影响，未动。

## [2.5.2] - 2026-07-02 — D 层修订（chrome 红线 + 密度纪律）

### 移除
- `consulting.py` 的 `sidebar()`（左缘竖排侧标）。用户裁定：页眉/页脚/页面框架归 skeleton-common 与 themes.py，D 层禁止改动 chrome、只作用于内容区。
### 变更
- `svg-skeleton-d.md`：§2 六版式改为「主视觉＋必配辅助层」组合配方；§3 新增密度纪律（禁单元素占满内容区）；§4 竖排处置改为「D 层不做竖排」。
- LESSONS 新增第 4 条（单组件整页=过简）。

## [2.5.1] - 2026-07-02 — 咨询密集层 D（异形 + 标注，降 AI 方形大卡片味）

### 新增
- **`assets/components/consulting.py`**：12 个异形/标注 API（雪佛龙链、流向带、哑铃、点阵、驱动树节点+肘线、链式递减；椭圆圈注、引线、水印、逐字侧标、So-What、线画对勾）。
- **`references/svg-skeleton-d.md`**：D 层骨架与纪律（降 AI 味三原则含出处、X-90 段版式 6 个、标注层配额、PPTX 兼容补遗）。
- **layout-library**：新增 90 段版式 E-90/V-90/V-91/V-92/G-90/I-90；phase-05/07 例外句挂接 consulting.py。
- **examples/consulting/**：冒烟页 demo_d（12 API 一页，原生转换 sp=339/pic=0）+ FIFA26 世界杯 10 页 SVG 真源作参考。
### 实测结论（写入 LESSONS 与 skeleton-d §4）
- `<text>/<ellipse>` 上 translate+rotate 组合变换转换后漂移 → 竖排一律逐字侧标。
- 细段标注需自带空格并错层（"1/44" 粘连事故）；`✓` 属 tofu 高危 → 线画对勾。

## [2.5.0] - 2026-07-01 — 工程预检工具 + 防坑附录

### 新增
- **工程预检工具** `assets/tools/`：`lint_svg.py`（tofu 高危字符 / 页脚总页数一致性 / 源码中文双引号预检）、`icons_preview.py`（图标缩略校验）、`pageno_fill.py`（页码集中回填，根治 /50 与 /57 并存）。
- **`assets/components/mes_icons.py`**：25 个具象制造业图标（worker / conveyor / andon / scanner / gearmold / injection…）。
- **`components.placeholder()`**：软件界面占位框（UI 未到位时占位，不硬编假界面）。

### 变更
- SKILL.md 新增「工程预检与防坑」附录（字符安全 / 图标 / 页码 / 占位 / 术语 / 基线 + 双轨审计 / 客户图为锚 / 每页不套模板）；质检协议增自动预检 + 双轨审计；LESSONS 补大体量册复盘。

## [2.4.0] - 2026-06-26 — 更稳的流程（防跳步）+ 更准的版式（去重 · 单一决策表 · 硬门禁）

> 治两大体验问题：Claude **跳步骤** 与 **版式选不对**。不改对外触发与产出视觉，核心八阶段方法论不变。

### 新增
- **选版式单一权威表**：`layout-library §版式选择速查` 设为唯一决策表 + 标注「首选核心集」（治选项过载）；`phase-05` 删内联映射、改为引用。
- **数据强制图表化 = 硬门禁（规划/设计/质检三环）**：Phase 5 布局规划卡每页必勾「版式自检」（≥3 条数据→必用 charts / 非数据页先判结构图 / 主角↔版式匹配）；Phase 7 设计前门禁加同款拦截；Phase 8 新增 `L4.5 版式合规`（数据被文字化 = ERROR）。
- Phase 7 出片前必声明"已加载 svg-skeleton + grid-system、坐标照抄不自算"。

### 变更
- **README 重排**：改为"为什么做 / 定位 / 八步法 / 样式与示例 / 使用方法 / 更新记录 / 关于"线性结构；删技术目录树与冗余预览（图墙收为 6 张），篇幅减半。
- **入口铁律（治"跳步骤"）**：`SKILL.md` Step 2 从"列阶段名"改为 **"逐阶段加载 + 卡点等待 + 不可跳步 + 进度可见"** 的强制循环；8 个 phase 顶部"可插拔模块"→"必经一步（不可跳过/合并）"。经对抗验证补漏：进度行 `【N/8】` 下沉到每个 phase 文件顶部；明确 **Phase 1 ≠ Step 1**（受众卡/完成卡不被"已加载文件"吞掉）；phase-05 补顶部 `强制等待锚点`。

### 修复
- 出片/质检阶段不再用红绿染 KPI / 大数字（S-09、I-05 改墨色，状态靠点+文字双通道）。
- 修孤儿 **T-02**：补"白底大字宣言/金句"选择路径（原先零路径指向）。
- **HERO 家族统一命名**（S-07 阶梯递进→HERO-3，选择速查三行收一）。
- `designer-rules` 路径A 的封面/目录/章节改走 `themes.py`，删除与之打架的旧 cover→I-01 映射；SPC 系不再谎称"骨架在 common.md 末尾"。

### 移除
- 删重复版式：**I-02**（→T-01）、**I-03**（→S-08）、**V-01**（→S-09）；删 **Ch 伪系**（数据图表归 V 系 + `charts.py`）。
- 版式库：声明 37→**34 ID**，骨架实存 **31 个**（i3 s12 e4 v3 t3 a3 g3）。

## [2.3.0] - 2026-06-26 — 仓库清理：去悬空引用 / 退役影子层 / 删死代码 / 规范单一源

> 工程与规范层清理，**不改变技能的对外行为与产出视觉**；核心八阶段引擎保持不变。

### 修复
- 修正 **9 处**指向不存在文件 `aham-ui-office.md` 的悬空引用 → 改指 `brand.md §7` + `tokens.css §10`（取值唯一事实源）。
- 出片/质检阶段不再教用衬线"宋体-简"与"顶部蓝条 / Action Title 蓝竖线"（违 brand 北极星，照做会被 Phase 8 判 ERROR）：`phase-06/07/08` 统一无衬线 + 无蓝竖线。
- Action Title 字号统一 **32px**（双行 22px）；删除 `designer-rules` 与 `grid-system §八` 冲突的字数表（字数表唯一源 = `grid-system §八`）。
- 图表配色去红绿：瀑布正负改灰阶 + 符号、甘特去蓝灰多色混用；KPI 数值不再染红绿（V-01 骨架数值改墨色，状态靠点 + 文字）。
- 修正 `designer-rules` 自相矛盾（"禁写死色值"却内置色表）、伪造的 brand §2.3 引文、过时的 brand 结构索引；T-01 深色页去游离钢蓝 `#4A6680`。
- 全仓脱敏真实项目名；修补 `layout-impl.md` / `svg-skeleton.md` 单数断链与 SPC/G 系→文件映射例外。

### 变更
- **规范单一事实源化**：PPTX 兼容雷区唯一源 = `designer-rules`；字数表 = `grid-system §八`；节奏阈值 = `layout-library §节奏约束`；版式坐标 = `grid-system`；其余文件改为引用而非各写一份。
- **视觉档接线**：`phase-05/07` 显式按 `theme` 调用 `themes.py`（A/B→cover/toc/section/chrome；C→cover_dark/section_dark/quote_dark），兑现选档对产物的影响。
- **C 高表现力档正式登记**：`brand.md §2.1` 登记 `#1C1C1C` 为唯一非纯白底例外（限封面/章节/金句），`tokens.css §10` + `quality-audit` 收录 C 档深色 ramp。
- `iconography` 回写 v2.1"内容区线性图标"为 B/C 档例外；Phase 1 完成卡记录 deck_mode/output_format/theme；Phase 3→4 反对意见链路补专家模式回退（取受众卡"主要顾虑"）。

### 移除
- 退役整套影子版式层 `references/layout-impl-*.md`（7 个，与 `svg-skeleton-*` 重复且坐标漂移；坐标真源是 `grid-system`）。
- 删除 `references/enhancements.md`（v2.1 增量已并入 `designer-rules` / `phase-02` / 组件代码）。
- 工具链死代码：`pptx_cli.py` / `pptx_discovery.py`（无人调用的第二入口）、切换动画死分支（缺失模块 `pptx_animations`）、失效的 `config` / `project_utils` import、死函数 `get_element_opacity` / `num_badge` / `num_ring`。
- 一次性发版脚本移出 `examples/` → `tools/`（`article_figures.py` / `social_banners.py`），去掉硬编码 `~/Desktop` 输出路径。
- 旧 demo `examples/Aham-PPT-Demo.pptx`、散落的 `.DS_Store`。

## [2.2.0] - 2026-06-26 — C 高表现力档 + 数据图表组件 + 去对标

### 新增
- **C · 高表现力档**：A/B 基础上新增深色重音页（`#1C1C1C`）+ 超大 mono 数字 + 图表占版面，面向路演/竞标/重点客户；深色模板 `cover_dark / section_dark / quote_dark`（`themes.py`）。视觉档由 A/B 两档扩为 **A/B/C 三档**。
- **数据图表组件库** `assets/components/charts.py`：9 类（柱/横柱/折线/瀑布/漏斗/甘特/子弹/堆叠/坡度），一行调用、brand §7.5 合规、转换实测可编辑。
- **防平淡规则链**：数据强制图表化 + 图形化占比下限 + 防平淡审计（`phase-04/05`、`chart-impl`、`quality-audit-protocol`、`designer-rules`）。

### 变更
- 文案去除“对标麦肯锡/德勤”“咨询级”等对标式描述，统一为“克制”定位；八阶段“麦肯锡金字塔”→“金字塔原理”。
- 重做 banner（`social-preview` · “三档风格 · 八阶段流程 · 原生 PPTX”）；README 加「🆕 三档视觉风格」节 + C 档封面 + A/B/C 对比；Pages 同步。

## [2.1.0] - 2026-06-22 — 双档主题 + 工具链修复

### 新增
- **双档主题系统**：A 克制档 / B 现代专业档（默认 B）。共用内容与组件，仅切换封面/目录/章节模板与页眉皮肤；两档均坚持单一主色 + 中性灰，不引入多色体系。见 `references/theme-tiers.md`。
- **启动选档步骤**（SKILL.md Step 1.5）：规范加载后、解析材料前询问一次，回车默认 B。
- **图标与组件库**（`assets/components/`）：`icons.py`（~40 线性图标 + icon_circle/num_badge/num_ring）、`components.py`（泳道/蓝图/箭头/KPI/状态/设备屏/手机/占位框）、`themes.py`（A/B 封面/目录/章节/页眉模板）。
- 设计规则：**强调色语义** QC 项（禁无语义单点强调色）、真实照片**占位框**（禁 AI 图/网图）、**样张先行**。
- 内容方法论：一手材料优先、措辞分寸、show-don't-tell、脱敏固定步骤、流程先确认形态。

### 修复
- **转换器文本宽度估算偏窄导致折行**（`assets/svg_to_pptx/drawingml_utils.py` 的 `estimate_text_width`）：窄字符 0.3→0.5、基准 0.55→0.62、mMwWOQ→0.82、CJK→1.02、整体 ×1.08。修复编号"01"、长英文串被 LibreOffice 拆行的问题。

### 变更
- 规范微调：放开"内容区线性单色图标"为 B 档允许项（原仅限导航/发送栏）。
- 建议产物写"版本目录"、页码用 ORDER 列表统一重排。

## [2.0.1] - 2026-06-21

### 新增
- 示例新增 3 种版式：**流程闭环**（E-03）、**VS 对照**（S-08）、**深色过渡**（T-01），示例增至 11 页。
- README 加「示例预览」图墙——11 页真实渲染截图（2× 高清），存 `assets/shots/`。
- `examples/render_shots.py`：用 Playwright/Chromium 把示例 SVG 渲染成 PNG（Inter/JetBrains 网络字体 + 系统 CJK）。

### 变更
- Action Title 字号统一为 24pt（32px）；品牌蓝点位置微调（与品牌字留清晰间距）。

## [2.0.0] - 2026-06-21

设计语言换血：从旧规范（`#1677FF` 重蓝 · 衬线标题 · 描边大卡）
全量迁移到 **Aham UI v6.1**（Claude desktop 气质 · 冷色的纸 · 蓝是点缀）。
生成的 PPT 视觉彻底改变；八阶段方法论、触发词、调用方式保持不变。

### 变更
- 主色 `#1677FF` → `#336EE8`，且蓝降为**点缀**——无顶部蓝条、绝不铺底（「蓝若第一眼注意到就超标」）。
- 中性体系改为三层灰 `#FFFFFF` / `#F3F3F3` / `#E7E7E7` + 墨四级 `#262626` / `#6E6E6E` / `#9B9B9B` / `#C4C4C4`（禁纯黑 `#000`）。
- 字体改为**单一无衬线** Inter / 微软雅黑（禁衬线），数字一律等宽 mono JetBrains Mono / Consolas。
- 卡片**无边框无阴影**；分块靠留白 + 细横线；选中 / 强调 = 扁平灰，非蓝。
- 状态 = **6px 点 + 文字**；表格只横线、数字右对齐 mono；图表灰阶 + **一个**蓝高亮。
- Action Title 改为无衬线 bold（24pt / 32px），去掉左侧蓝竖线与衬线。
- `track-rules` 重构为四介质轨（网页 / 应用 / Office / 邮件），明确**本技能 = Office 轨 · PPT 子模型**。

### 新增
- `examples/`：8 页密集示例（封面 / KPI 看板 / 方案选型 / 趋势 / 路线图 / 大数字 / 三层架构 / 2×2 矩阵）。
- `examples/build_examples.py`：示例生成器，一键产出 8 页 SVG + 浏览器预览 `preview/deck.html`。
- 示例转 PPTX 工具链回归：8/8 通过、0 跳过、原生可编辑。

### 移除
- 旧视觉件：深蓝强调卡、浅蓝 Callout、描边白卡、顶部 3pt 蓝条、衬线标题、状态色块 / 红黄绿灯、图表多色。
- 全仓库旧视觉 token（`#1677FF` / `#1A1A1A` / `#E2E2E2` / 思源宋体 / Roboto Mono / `var(--brand-primary)`）清零。

> 注：v1.0.0 初版未单独立条，公开条目自 [1.1.0] 始（tag 列表亦无 v1.0.0）。

## [1.1.0] - 2026-04-30

### 修复
- 修复版式命名冲突、品牌色硬编码等 8 项问题。

[Unreleased]: https://github.com/Aham-AIAPP/aham-ppt/compare/v3.2.0...HEAD
[3.2.0]: https://github.com/Aham-AIAPP/aham-ppt/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/Aham-AIAPP/aham-ppt/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/Aham-AIAPP/aham-ppt/compare/v2.5.2...v3.0.0
[2.8.0]: https://github.com/Aham-AIAPP/aham-ppt/compare/v2.5.2...v3.0.0
[2.7.0]: https://github.com/Aham-AIAPP/aham-ppt/compare/v2.5.2...v3.0.0
[2.6.0]: https://github.com/Aham-AIAPP/aham-ppt/compare/v2.5.2...v3.0.0
[2.5.2]: https://github.com/Aham-AIAPP/aham-ppt/compare/v2.5.1...v2.5.2
[2.5.1]: https://github.com/Aham-AIAPP/aham-ppt/compare/v2.5.0...v2.5.1
[2.5.0]: https://github.com/Aham-AIAPP/aham-ppt/compare/v2.4.0...v2.5.0
[2.4.0]: https://github.com/Aham-AIAPP/aham-ppt/releases/tag/v2.4.0
[2.3.0]: https://github.com/Aham-AIAPP/aham-ppt/releases/tag/v2.3.0
[2.2.0]: https://github.com/Aham-AIAPP/aham-ppt/releases/tag/v2.2.0
[2.1.0]: https://github.com/Aham-AIAPP/aham-ppt/releases/tag/v2.1.0
[2.0.1]: https://github.com/Aham-AIAPP/aham-ppt/releases/tag/v2.0.1
[2.0.0]: https://github.com/Aham-AIAPP/aham-ppt/releases/tag/v2.0.0
[1.1.0]: https://github.com/Aham-AIAPP/aham-ppt/releases/tag/v1.1.0

