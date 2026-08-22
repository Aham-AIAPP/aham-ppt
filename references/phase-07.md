# Phase 7 · 逐页SVG设计

> 本阶段是八步流水线的**必经一步**（不可跳过 / 不可与其它阶段合并产出）；文件本身可独立维护。
> ▶ **进入本阶段第一句先输出**：`【阶段 7/8 · 逐页SVG设计 · 已加载 phase-07.md】`
> 本Phase按布局规划卡逐页输出SVG，所有设计决策基于已确认的视觉基调。
> SVG是唯一真源（Single Source of Truth）。PPTX由SVG机器转换，不手写。
> **图内文案与卡片标题规则见 `wording-rules.md` §4：方框标签用完整规范术语；
> 禁自造概念，自造词换成对象名而非动作名；卡片标题为动宾结构，动词须是日常动词；
> 并列项必须真正同级同类；同一组并列项中不要只有一项带数字。**

---

## 入场条件

- Phase 6视觉基调已确认 ✓
- 逐页布局规划卡已确认 ✓
- BRAND_RULES已加载 ✓
- svg_final/ 目录已创建（工作区）

---

## 阶段提示卡

```
┌─────────────────────────────────────────┐
│ Phase 7 · 逐页SVG设计                    │
├─────────────────────────────────────────┤
│ 这一步要做什么                           │
│   按布局规划卡逐页生成SVG               │
│                                         │
│ 用什么方法                               │
│   严格按样稿基调，严格按版式规划         │
│   颜色全部查规范，不自定义              │
│   SVG为唯一真源，PPTX从SVG转换           │
│                                         │
│ 你需要做的                               │
│   每3页确认一次，有问题及时告诉我        │
│   全部完成后整体预览                     │
└─────────────────────────────────────────┘
```

---

## 教练机制检查

读取 `coach-engine.md`，执行Phase 7入口检查：
- 如果用户对某页设计不满意但说不清楚哪里不对，激活教练模式
- 执行 coach-engine.md 中「Phase 7 · 逐页设计」引导序列

---

## 强制等待锚点

**在开始逐页设计前，确认设计依据已齐全：**

```
进入 Phase 7 · 逐页SVG设计。

在开始之前确认：
1. Phase 5 的版式规划（含每页坐标）已确认 ✓
2. Phase 6 的样稿视觉基调已确认 ✓
3. 品牌规范已加载 ✓

我将按页码顺序设计，每完成3页暂停让你确认。
设计过程中有任何问题随时说。

准备好了吗？（回复"开始"或提出任何要求）
```

等待用户确认后，才进入执行步骤。

---

## 执行步骤

### 步骤1：设计前准备

读取以下文件，加载设计规则：
- `svg-skeleton-common.md`：通用 Chrome/构件规范与咨询密集层纪律
- `svg-skeleton-[当前版式系].md`：当前页版式的五栏章节（仅读对应 1 个）——**一律按「用法」栏调用参数化函数**（`layouts.py` 整页/内容区型、`consulting.py` 形体、`structures.py` / `charts.py` 结构与图表），坐标由函数冻结、不手画不自算；标注层纪律随 `svg-skeleton-common.md §咨询密集层 D` 一并加载。**系→文件例外**：封面/目录/章节用 `themes.py` 生成（不读 svg-skeleton）；直排页（Phase 5 规划卡标注「直排」的页面）读 `grid-composition.md` + `grid-system.md §三`，不读版式章节
- `designer-rules.md`：设计原则+品牌纪律+PPTX约束
- `chart-impl.md`：图表（有图表的页面才读）。**优先 `from charts import bar, hbar, line, waterfall, funnel, gantt, bullet, stacked, slope, sparkline, kpi_card, marimekko, fte_ramp, horizon_curves`（14 类全量）一行生成，不逐坐标手画**；charts 未覆盖的类型才用 chart-impl 手画模板

**按视觉档（theme，Phase 1 记录）调用 `themes.py` 结构性页模板：**
- A / B 档：`cover / toc / section / chrome`（B 档 chrome 可带图标/关系图）
- C 高表现力档：`cover_dark / section_dark / quote_dark` 用于封面/章节/金句重音页，内容页仍用 `chrome`(B 皮肤)，数据页 `charts` 占主导

确认以下内容已就绪：
- 布局规划卡（来自Phase 5）
- 视觉基调确认单（来自Phase 6）
- BRAND_RULES（颜色/字体）+ theme 视觉档

---

### 步骤2：逐页串行设计

**设计顺序：** 按页码顺序逐页设计，每3页询问用户确认。

**每页开始前，必须先输出以下自检声明，再写SVG代码：**

```
[第X页 · 第X/总页数 · 设计前自检]
版式：[版式ID]  骨架：svg-skeleton-[系].md → [章节名]（SPC→svg-skeleton-common.md）
坐标：来自Phase 5规划卡，不自行计算

设计前门禁（全部✓才开始写代码）：
□ 已加载 svg-skeleton-[系].md + grid-system.md，按章节「用法」栏调用参数化函数、坐标不自算（layouts/charts/consulting/structures 按归属；结构性页用 themes.py；直排版式按 grid §三）
□ 本页若聚集 ≥3 条 D 类数据/可对比排序/时间序列 → 已选 V 系并调 charts 组件（否则停，回 Phase 5 改版式，不得文字化）
□ 无未转义的 & < > "
□ 无 <marker>（箭头用 <polygon>）
□ 无 <g transform="rotate/scale(-1)">
□ 无 \n 换行
□ 无 rgb()/hsl() 颜色
→ 全部通过，开始写SVG
```

**每页设计时强制执行：**

坐标规则（新增）：
- 坐标严格按 Phase 5 布局规划卡中的区域坐标，不自行调整
- 每页主体由对应章节「用法」栏的函数调用生成（坐标函数内冻结）；直排版式坐标严格取 grid §三，不自算不微调
- 替换完成后检查：SVG中不应有任何剩余的 `[` 或 `]` 字符

颜色规则：
- 所有色值决策查BRAND_RULES，禁止自定义色值
- 语义色场景必须颜色+符号双通道（不能只靠颜色区分）

标题规则：
- Action Title≤30字，**无衬线 Bold `#262626`，无蓝竖线**（禁宋体/衬线）
- 坐标按 `grid-system.md §五`：单行 y=78 / 32px，双行 y=60·86 / 22px

图表规则（有图表时读 chart-impl.md）：
- 禁用饼图（任何情况下）
- 禁用3D效果和渐变
- 柱状图Y轴必须从0开始
- 数据来源必须标注

**绝对禁止：**
- 渐变 / 3D效果 / 投影（drop shadow） / 纯黑色 #000000 / 饼图

**PPTX转换兼容性禁止：**
- 文字内容里出现未转义的 `&`、`<`、`>`、`"`
- 用 `<marker>` + `marker-end` 画箭头（改用 `<polygon>`）
- `<g transform="rotate(...)">` group级别旋转
- `<g transform="scale(-1...)">` 负数缩放
- 多行文字用 `\n` 换行（改用 `<tspan dy>` 或独立 `<text>`）
- 单行文字超出容器宽度（查 grid-system.md 字数参考表）

---

### 步骤3：每3页确认

每完成3页，输出中间确认（**专家档**按 coach-engine「专家档合并闸门」改为**每章一次**）：

```
已完成第[X]-[X+2]页，请查看以上设计。

如有修改意见请告知，确认后继续设计第[X+3]页。
```

用户确认后继续，有修改意见则先修改再继续。

---

### 步骤4：全量完成后整体预览

所有页面设计完成后：
1. 生成 `preview.html`（所有SVG的HTML预览文件）
2. 输出整体预览提示：
```
全部[X]页设计完成，请整体浏览预览文件。

重点检查：
- 整体风格是否统一？
- 有没有某页感觉突兀或不协调？
- 内容是否有明显遗漏或错误？

确认后进入质检与交付。
```

---

### 步骤5：输出格式处理

读取Phase 1记录的output_format，确定交付格式：

**SVG模式（output_format=svg）：**
输出 svg_final/ 目录下所有SVG文件，不需要PPTX转换。

**PPTX模式（output_format=pptx-native 或 both，默认both）：**

> **转换前必读** `view references/pptx-native-rules.md`（支持元素矩阵/雷区/验证步骤）；
> **转换后必执行** `view references/quality-audit-protocol.md`（三级关卡说明 + lint 渲染前后双轨 + 人工审计入口）。

```python
import sys
from pathlib import Path

# ⚠️ 必填：将下一行替换为本机 aham-ppt/assets 的绝对路径（故意不给可用默认值，不替换会 ImportError）
# 定位提示：本地克隆 → /<你的路径>/aham-ppt/assets；Claude 云容器 → /mnt/skills/user/aham-ppt/assets
sys.path.insert(0, '<替换为_aham-ppt/assets_绝对路径>')

from svg_to_pptx_wrapper import svg_to_native_pptx

svg_files = sorted(Path('./workspace/svg_final').glob('*.svg'))
output = Path('./workspace/deliverables/方案.pptx')

# presenting/hybrid 模式：从 Phase 5 规划卡收集「讲者备注」，转换完成后写入 PPTX 备注栏
notes_list = []  # 与 svg_files 逐页对应；无备注的页留空字符串

success = svg_to_native_pptx(
    svg_files=svg_files,
    output_path=output,
    canvas_format='ppt169',
)
assert success, "转换失败，检查SVG是否规范"

# 写入讲者备注（Duarte 式「页面留冲击、内容进备注」的后半环；python-pptx 已在依赖中）
if any(notes_list):
    from pptx import Presentation
    prs = Presentation(output)
    for slide, note in zip(prs.slides, notes_list):
        if note:
            slide.notes_slide.notes_text_frame.text = note
    prs.save(output)
```

**PPTX转换的严禁行为：**
- 不手写python-pptx代码拼形状
- 不用EMF嵌入后声称"可编辑"
- PPTX生成后不直接改PPTX（会与SVG真源漂移）
- 出现故障时，回去改SVG源，重新运行工具链

---

## 跳过风险

```
风险等级：无法跳过
风险说明：
  本Phase是核心产出阶段，无法跳过。
```

---

## 完成卡

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Phase 7 · 逐页SVG设计 完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
入场条件    Phase 6视觉基调已确认 ✓
本阶段输出  SVG文件：svg_final/（共[X]页）
           预览文件：preview.html
           [PPTX：方案.pptx（如output_format包含pptx）]
关键结论    设计完成率：[X]/[X]页
           中间确认：每3页已确认
           整体预览：[已确认]
待确认      整体浏览后，有没有需要修改的页面？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
以上内容确认无误后进入 Phase 8 · 质检与交付。
如需修改请直接说明。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
