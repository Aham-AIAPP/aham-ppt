# Designer Rules · SVG设计规范

Phase 7 每页SVG设计的执行规范。
**品牌规范以 brand.md 为权威来源，本文件只管「怎么画」。**

> **设计补充（本节即权威版，方法论同见 phase-02/03）**
> - **强调色 = 信号，不是装饰**：同类并列项要么全中性、要么完全一致；主色只用于 当前/推荐/阶段/主操作/单个高亮数据/品牌点。QC 必查：页面内是否存在无语义的单点强调色？
> - **内容区线性单色图标**为 B/C 档允许项（A 档可不用）；图标单色、取角色墨色或主色，不上多色/面性填充（见 `brand-spec/iconography.md` 例外）。
> - **真实照片用占位框**（`assets/components/components.py` 的 `placeholder`），禁 AI 生成图/网图。
> - **样张先行**：大改视觉语言后先出 3–4 张样张确认再铺全册。
**颜色唯一来源：brand.md §2 / tokens.css。禁止使用规范外色值；本文件下方「色值与字体」表是 brand 白名单的执行级速查（非新增色值）。**
**语义色必须颜色+符号双通道（brand.md §2.3）。**

## 色值与字体（直接写字面 hex，权威来源 tokens.css / brand.md）

> SVG 里**直接写字面 hex**（转换器对 hex 最可靠），不要用 CSS 变量。下表是全部允许色值——白名单之外不得出现。

| 角色 | 色值 | 用途 |
|---|---|---|
| 表面 1 / 底 | `#FFFFFF` | 页底（永远纯白）、卡内 |
| 表面 2 / 面板 | `#F3F3F3` | 成块面板（少用） |
| 表面 3 / 线 | `#E7E7E7` | 分隔线、表格横线、选中 |
| 墨 主 | `#262626` | 标题、正文、数字 |
| 墨 次 | `#6E6E6E` | 次要、表头副文 |
| 墨 三 | `#9B9B9B` | 占位、装饰性弱字（对白 2.78:1，**不承载须读取的信息**；页脚/来源/轴标签用墨次 `#6E6E6E`） |
| 墨 四 | `#C4C4C4` | 最弱线、禁用（不承载正文） |
| 强调蓝 | `#336EE8` | **仅点缀**：品牌点/主操作/选中下划线/推荐标/单个高亮数据点/封面短线 |
| 蓝 hover/press | `#5C8BED` / `#164EC3` | 同上 |
| 语义 成功/警示/风险 | `#5A7A60` / `#8A7333` / `#9E3D31` | 仅真风险，配符号+文字双通道 |

**字体**：文字一律无衬线 `Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif`；数字一律 mono `'JetBrains Mono', Consolas, monospace`。**禁衬线、禁纯黑 `#000`**。

---

---

## 执行前确认

Phase 7 每页设计开始时确认以下输入已就绪：
- Phase 5 布局规划卡（含版式ID和区域坐标）
- Phase 6 视觉基调确认单
- BRAND_RULES（来自 brand.md §2）

输出格式默认为 SVG（由工具链转PPTX）。

---

## 执行流程

```
Step 1  读 Phase 5 布局规划卡 → 确认版式ID和区域坐标
Step 2  读 svg-skeleton-[系].md → 复制对应版式骨架（坐标真源 grid-system.md）
Step 3  若有图表 → 优先调用 charts.py 组件（未覆盖时兜底见 chart-impl.md）
Step 4  替换骨架中所有 [占位符] 为实际内容，不改坐标
Step 5  执行输出前自检（含PPTX兼容性5条负面约束）
```

---

## 路径A：结构性页面

封面 / 目录 / 章节页**按 Phase 1 视觉档调用 `themes.py` 模板**，不在内容版式系内选：
- cover → `cover`（A/B）/ `cover_dark`（C）
- toc → `toc`（A/B）/（C 沿用 toc 或封面同款深色）
- section → `section`（A/B）/ `section_dark`（C）
- exec_summary → S-09 KPI看板（内容版式）
- end → 三步行动直排页（grid-composition §三步卡）

内容页 Chrome 读 `svg-skeleton-common.md` 的 Chrome 骨架（坐标真源 `grid-system.md`）。
替换所有 `[占位符]` 为实际内容。

**交叉检查：替换完成后，SVG 中不能有任何 `[` 或 `]` 字符（占位符未替换完）。**

---

## 路径B：内容页

### B-0：确认页面基调

在绘制任何卡片之前，读取 Phase 5 布局规划卡确认：
1. `叙事目的`（决定整体视觉基调，对应 narrative_purpose）
2. `信息密度`（对应 deck_mode 的 bullets 上限）
3. `内容要点`（这就是要画的内容）

**根据 narrative_purpose 的视觉基调指引**：

| narrative_purpose | 视觉基调 | 关键指令 |
|---|---|---|
| **impact** | 震撼 | 单数字/单句字号 ≥107px（≈80pt），留白 ≥ 50%，极简 Chrome |
| **structure** | 结构 | 标准 Chrome，多区块布局，信息密度中高 |
| **explain** | 说明 | 图示优先，图示占画面 ≥ 40% |
| **evidence** | 证据 | 图表优先，数据来源标注必备 |
| **transition** | 过渡 | 极简，留白 ≥ 60%，可深色底 |
| **action** | 动作 | 清晰结构化，行动条目带编号 |

### B-1：Chrome 结构

**根据 narrative_purpose 选择 Chrome 类型**：

| narrative_purpose | Chrome 类型 |
|---|---|
| impact（大数字/时间窗直排页） | 极简 Chrome |
| transition | 极简 Chrome 或深色底 |
| 其他 | 标准 Chrome |

从 `svg-skeleton-common.md` 读取对应 Chrome 骨架（坐标真源见 `grid-system.md`），填入：
- `[section_path]`、`[title]`、`[source]`、`[date]`、`[page_index]`、`[total_pages]`
- Draft标签：`is_draft=true` 时渲染

**字体关键规则**（无衬线 + 数字 mono · 见 brand.md）：
- Action Title：无衬线 Bold 32px，fill=`#262626`
- 内容小标题：无衬线 600，**fill=`#262626`（墨色，非蓝）**
- 正文说明：无衬线 Regular，fill=`#262626`（次要 `#6E6E6E`）
- 数字/KPI：mono `'JetBrains Mono', Consolas, monospace` Bold，fill=`#262626`（唯一关键数可 `#336EE8`；状态靠点+文字，不靠数字染色）

### B-2：按 layout_code 读取坐标

根据 `layout_code` 在 `svg-skeleton-[系].md` 查找对应骨架；版式坐标的唯一真源是 `grid-system.md`。

### B-3：卡片样式

**默认：不画卡，靠留白 + `#E7E7E7` 细横线分块。** 需要明显成块时才用面板：

**面板卡（无边框无阴影）**：
```svg
<rect rx="12" fill="#F3F3F3"/>
```

**强调 / Callout（面板 + 左侧蓝细条点缀，不铺蓝底）**：
```svg
<rect rx="12" fill="#F3F3F3"/>
<rect width="3" rx="1.5" fill="#336EE8"/><!-- 左侧细条，h=卡片高 -->
<!-- 内部文字一律 #262626，不改白字 -->
```

> 旧的「深蓝底卡 + 白字」「浅蓝底 Callout」「描边白卡」**已废止**——蓝不铺底，选中/强调=扁平灰面板，卡片无边框无阴影。

### B-4：卡片内容元素

**卡片内边距**：16px

**卡片标题**：y=卡片y+30，无衬线 600 15px，**#262626（墨色，非蓝）**

**Bullets**（• 点 + 文字，起始y=卡片y+58，间距26px）：
> 注：卡片内 y+30 / y+58 / 行距 26 属**基线坐标学**（文字基线定位值），不属 4 基间距阶；间距阶只约束块间距。页边距 40 为画布常数（Carbon 间距体系亦含 40 档，不视为出圈）。
```svg
<circle cx="[cx+19]" cy="[itemY-4]" r="3" fill="#9B9B9B"/>
<text x="[cx+32]" y="[itemY]" font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif"
      font-size="14" fill="#262626">[bullet文字]</text>
```

**impact 类大数字**（数字 mono · 墨色；唯一关键数可 #336EE8）：
```svg
<text x="[卡片中心x]" y="[卡片中心y]" text-anchor="middle"
      font-family="'JetBrains Mono', Consolas, monospace" font-size="[80-160]"
      font-weight="bold" fill="#262626">[big_number]</text>
```

**数据来源标注**（有 data_points 时必须）：
```svg
<text x="[cx+cw-16]" y="[cy+ch-10]" text-anchor="end"
      font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif" font-size="9" fill="#6E6E6E">
  来源：[source]，[date]</text>
```

### B-5：文字换行（字数表唯一源见 `grid-system.md §八`）

### B-6：信息密度约束

按 Phase 5 布局规划卡中的信息密度字段执行：
- presenting 模式：≤3条 bullet
- hybrid 模式（默认）：≤5条 bullet
- reading 模式：≤7条 bullet
- impact 类页面：必须有 ≥80px（=60pt）大数字
- explain 类页面：必须有图示（占画面 ≥40%）

---

## 品牌规范执行纪律

## 场景 15 · 颜色使用必须从品牌规范读取,不得自定义 ★★

**Trigger Point**:设计任何涉及颜色选择的页面时。

**核心原则(最高优先级)**:
> **颜色规范的单一源头是 `references/brand-spec/brand.md`。**
> **顾问/AI 不得在任何文档中自定义颜色值**,包括但不限于 PPT 设计说明、Skill 文档、方案附录。

### AI 最常见的三种失守方式

1. **多色相分类滥用**:为了区分模块擅自引入绿/红/蓝等多种色相
2. **擅自定义色值**:在 Skill 里写"深蓝 #336EE8"这种具体色值,形成第二套"事实标准",与 brand.md 分裂
3. **擅自收紧/放宽规范**:比如"不用绿色""最多 3 种色相"——这些限制如果 brand.md 没有,就是 AI 的臆造

### 正确做法

- 所有颜色使用决策 → **读取 brand.md §2 配色体系**,按规范执行
- 需要说明某个颜色含义时 → **引用规范条款**(如"按 brand.md §2.3 语义色表,✕ 异常用语义警示色")
- 规范里没有的场景 → **停下来问用户**,不自己补充

### 必问问题(每次要引入颜色时)

1. brand.md **第几节第几条**明确允许这个颜色的使用?
2. 我是在**执行规范**,还是在**补充规范**?(补充就是越权)
3. 如果我觉得规范没覆盖到,是**规范有漏洞**,还是**我没读仔细**?
4. 如果规范真有漏洞,正确做法是**告知用户并请求规范更新**,而不是自己临时定义

### Aham 规范结构概览(查表索引)

顾问执行时直接查 brand.md 对应章节,不在本文件复述具体色值:

- **§2.1** 主色 / 表面(三层表面 + 唯一强调蓝;C 档深底例外)
- **§2.2** 中性墨(四级:#262626/#6E6E6E/#9B9B9B/#C4C4C4)
- **§2.3** 语义色(成功/警示/风险三色,必须符号+颜色双通道)★ 关键硬要求
- **§2.4** 图表色顺序(灰阶 + 一个蓝高亮)

### §2.3 的硬要求

brand.md §2.3 要求:状态 = **6px 点 + 文字**双通道,颜色之外文字本身可区分,去色后仍可辨;禁红黄绿灯、禁 pill/徽章/色块。

这意味着:如果要在某个工序上标"缺口",不能只用红色高亮,**必须同时用 ✕ 或 ▲ 符号 + 文字**。
这条规则容易被忽略,所有语义色场景都要双通道。

### 多色相滥用的本质

不是"AI 爱花哨",而是 **AI 没有把"品牌规范"作为权威参照**,每次设计都在重新发明配色。一旦建立了"从 brand.md 读取"的纪律,多色相滥用问题会**自动消失**,因为规范本身就限定了色彩谱系。

### Usage(三步走)

1. 设计前读 brand.md §2 配色体系
2. 列出本页所有需要颜色的元素,逐一映射到规范中的色值
3. 如果某个元素在规范里找不到对应位置,**停下来问用户**,不自行决策

### Cost of Skipping

- 规范与设计分裂,每次都在"重新发明"
- 规范升级(如 V1.4)后,所有旧 PPT 和旧 Skill 描述都失效
- AI 成为"规范的第二作者",权威性被稀释
- 客户看到不同 PPT 色值不一致,品牌一致性崩塌

### 某真实项目的两次翻车(作为教训)

**翻车 1 · P9 第一版多色相滥用**
- 错误:上游绿 / 中游红 / 下游蓝三色相分类
- 用户纠正:不应用色相分类,应该用明度变化

**翻车 2 · AI 在 Skill 里擅自定义色值**
- 错误:在 SKILL_UPGRADE_NOTES 里写具体色值,形成第二套规范
- 用户纠正:"你不应该在这里定义,都应该从 brand.md 读取"

---

## 架构级修正:brand.md 作为唯一真源

### 背景

某真实项目在 Phase 4.5 样稿阶段连续暴露了两层问题:
1. **单页级**:P9 用多色相分类(绿/红/蓝分段)
2. **技能级**:AI 在 SKILL 文档里擅自定义色值,试图"补充规范"

用户明确指出:
> "**整个设计规范是比技能更严谨的存在**。可能因为技能的要求,就在更改设计规范。设计规范是下一个环节的事情。"

这个表述把问题的**责任层次**说清楚了——**技能是规范的执行者,不是共同作者。**

### 四项强制纪律

#### 纪律 1 · 前置读取

在 SKILL 执行时(Phase 0.5 品牌规范读取阶段),必须强制读取:
- `references/brand-spec/brand.md §2 配色体系`
- `references/brand-spec/brand.md §3 字体体系`
- `references/brand-spec/brand.md §7 PPT 规范`

读取后把**完整色值白名单**加载到上下文,后续所有设计决策**只能从白名单查表**。

#### 纪律 2 · designer 阶段的硬性规则

在 `designer-rules.md` 里有顶级原则:
> **任何涉及颜色的决策,必须先在 brand.md §2 中找到对应条款。**
> **规范里没有的色值,不得使用。**
> **如遇规范未覆盖的场景,停下来问用户,禁止自行补充色值。**

#### 纪律 3 · QC 阶段的强制审计

在输出前必须有**色值合规审计**:

```python
## 审计结果示例(供参考)

某真实项目 Phase 4.5 的一次合规审计:

违规触发点: 7 张样稿中有 3 张违规,共 10 处色值违规
修正方案: A · 严格合规替换(映射到 brand.md §2 标准色)
修正后: 7 张全部通过审计,单一源头原则建立
```

违规色值映射记录供未来参考:

| 违规色值 | 映射到 | 规范位置 |
|---|---|---|
| 擅创的深蓝底 | 近黑 | §2.1 |
| 擅创的中灰 | 注释灰 | §2.2 |
| 擅创的冷灰 | H2 底线色 | §2.2 |

(具体色值按 brand.md 查表,不在本文件写死)

---

## 自查清单

每次设计时,Claude 要问自己:

- [ ] 我用的每个颜色,都能在 brand.md 里找到对应条款吗?
- [ ] 有没有因为"好看"就临时定义色值?
- [ ] 语义色场景有没有用**颜色+符号**双通道?
- [ ] 字体选择,是按 §3 查表,还是凭记忆?
- [ ] 如果用户问"为什么用这个色",我能指出规范条款吗?

---

---

## PPTX 兼容性硬性约束（SVG转PPTX实测雷区）

以下规则来自实测问题总结。违反任意一条，转换后的PPTX会出现内容丢失、空白页或排版错位。

### 约束1：特殊字符必须转义（最高优先级）

SVG文字内容中，以下字符必须使用XML转义：

| 原字符 | 转义写法 | 常见场景 |
|--------|---------|---------|
| `&` | `&amp;` | R&D、AT&T、P&L |
| `<` | `&lt;` | 比较符、尖括号 |
| `>` | `&gt;` | 比较符 |
| `"` | `&quot;` | 属性值内的引号 |

工具链会自动修复裸露的 `&`，但其他字符仍需手动处理。
写SVG时养成习惯：**文字内容有特殊符号，先转义再填入**。

### 约束2：箭头必须用 `<polygon>` 画，禁止用 `<marker>`

`<marker>` 定义的箭头在 `<path>` 和 `<polyline>` 上的 `marker-end` 属性转换后会丢失。

```svg
<!-- ❌ 禁止：marker箭头，转换后消失 -->
<defs>
  <marker id="arrow" ...><path d="M0,0 L10,5 L0,10"/></marker>
</defs>
<path d="M100,100 L300,100" marker-end="url(#arrow)"/>

<!-- ✅ 正确：polygon多边形直接画箭头 -->
<line x1="100" y1="100" x2="290" y2="100" stroke="#9B9B9B" stroke-width="2"/>
<polygon points="285,94 300,100 285,106" fill="#262626"/>
```

注：`<line>` 元素上的 `marker-end` 有部分支持，但仍推荐用 `<polygon>` 确保100%可靠。

### 约束3：禁止 `<g>` 上的 `rotate` 和负数 `scale`

`<g transform="rotate(...)">` 只旋转容器边框，不旋转子元素坐标，转换后子元素位置偏移。
`<g transform="scale(-1, 1)">` 等负数缩放在DrawingML中无对应实现，会被忽略。

```svg
<!-- ❌ 禁止：group级别rotate，子元素坐标会偏移 -->
<g transform="rotate(45, 640, 360)">
  <rect x="500" y="300" width="200" height="100"/>
</g>

<!-- ✅ 正确：计算旋转后的绝对坐标，直接写入元素 -->
<rect x="..." y="..." width="200" height="100" transform="rotate(45, 600, 350)"/>
```

`translate` 是安全的，可以在 `<g>` 上使用。

### 约束4：多行文字换行方式（两种方式均可靠）

SVG `<text>` 不支持自动换行。有两种可靠的换行方式，工具链均支持：

**方式一：`<tspan dy="1.4em">` 换行（推荐，语义清晰）**
工具链会自动将每个 `<tspan dy>` 拆成独立的 TextBox，坐标正确。
```svg
<text x="100" y="100" font-size="16">
  <tspan x="100" dy="0">第一行文字内容</tspan>
  <tspan x="100" dy="1.4em">第二行文字内容</tspan>
  <tspan x="100" dy="1.4em">第三行文字内容</tspan>
</text>
```

**方式二：独立 `<text>` 标签，各自指定 y 坐标（可靠，适合复杂布局）**
```svg
<text x="100" y="100" font-size="16">第一行文字内容</text>
<text x="100" y="124" font-size="16">第二行文字内容</text>
<text x="100" y="148" font-size="16">第三行文字内容</text>
```

**禁止：** 在文字内容里用 `\n` 换行（被折叠为空格，换行消失）。

### 约束5：单行文字长度不得超过容器宽度

工具链生成的TextBox宽度是按文字内容估算的，不会自动裁剪。文字超出容器在PPTX里仍然超出。

**单行最大字数：以 `grid-system.md §八` 为唯一字数表**（按容器宽度 × 字号查，如 1200px 容器 14px 约 43 字、16px 约 37 字）。Action Title 单行 32px、换行后 22px（坐标见 `grid-system.md §五`）。

超出时必须拆成多个 `<tspan>`，不得依赖容器自动截断。

### 约束6：字体只用无衬线 + 数字 mono（禁衬线）

全部文字用同一无衬线栈，数字用等宽，跨平台落字最稳：
```svg
font-family="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif"   <!-- 标题/正文 -->
font-family="'JetBrains Mono', Consolas, monospace"                  <!-- 数字/编号/时间 -->
```
Windows 无 Inter 时由 PowerPoint 决定替换（常见 Calibri）、中文微软雅黑、数字 Consolas；macOS 无 Inter 时常落 PingFang，数字 JetBrains Mono。PPTX 不嵌字体，回退不受文件控制——需精确度量请安装 Inter（SKILL.md §依赖）。**不得使用宋体 / Songti / SimSun 等衬线字体。**

---

### 约束7：PPTX 原生转换兼容（svg_to_pptx 工具链硬约束）

**变换**：任何元素禁 `rotate` / 负 `scale`——`<text>`/`<ellipse>` 上 translate+rotate 组合转换后整体漂移（白字落白底，灰度差质检不可见）。竖排文字用**单字逐个 `<text>` 纵向堆叠**（arch_layers 纵向能力条即此实现）；斜椭圆观感靠 rx/ry 比例。chrome（页眉/页脚/左缘）归 skeleton-common 与 themes.py，组件层禁触。

**箭头**：一律 `line` + `polygon`（`<marker>` 在 path/polyline 上静默丢失）。

**字符**：`✓/✗` 等在 `tools/lint_svg.py` tofu 高危名单，对勾用 `consulting.check()` 线画；mono 文本内全角 `＋ ＝` 可正常转换（Pango 逐字回退）。

**文本间距**：细段标注文字**自带空格**并 `tick_label(level)` 错层，防止相邻文本粘连（如 "1/4" 与 "4" 粘成 "1/44"）。

**已验证可用的路径能力**（E2E：SVG→svg_to_pptx→PPTX→PDF）：`<path>` M+L 折线（多段单 shape）、`<path>` A 圆弧（转换器内部转三次贝塞尔）、`<polygon>` 带 `opacity` 填充、`<circle>`——horizon_curves 的 S 曲线、concentric_arcs 的半圆弧、fte_ramp 的堆叠面积、气泡/芯片/端点均据此实现。

## 输出前自检

**结构性页面**：
- [ ] 所有 `[xxx]` 占位符已替换

**内容页**：
- [ ] viewBox = `0 0 1280 720`
- [ ] Chrome 类型与 narrative_purpose 匹配
- [ ] Action Title 字体是 `Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif`
- [ ] Action Title 坐标按 `grid-system.md §五`：单行 y=78 / 32px，双行 y=60·86 / 22px（无蓝竖线）
- [ ] 坐标严格按布局规划卡，无自行调整
- [ ] 所有卡片间距 ≥16px
- [ ] impact类页面有大数字（mono，≥60pt）
- [ ] explain类页面有图示
- [ ] 蓝只点缀：无顶部蓝条，全页蓝面积极小（仅品牌点/主操作/选中/推荐/单个高亮/封面短线）
- [ ] 卡片无边框无阴影；分块靠留白+`#E7E7E7` 细横线；强调=灰面板+左侧蓝细条，文字 `#262626`
- [ ] 表格只横线无竖线；数字右对齐 mono；状态=6px 点+文字（无 pill/红黄绿灯）
- [ ] 文字按保守字数换行（见上方字数参考表）
- [ ] 无禁用元素（衬线/饼图/3D/纯黑#000000/渐变/阴影/蓝铺底/第二装饰彩色/表格竖线/emoji）
- [ ] 有 data_points 的卡片已在右下角标注来源
- [ ] Callout 已渲染（callout_needed=true时）
- [ ] **[PPTX兼容] 文字内容中 & < > " 已转义**
- [ ] **[PPTX兼容] 无 `<marker>` 箭头，箭头已改用 `<polygon>`**
- [ ] **[PPTX兼容] 无 `<g transform="rotate(...)">` 或负数scale**
- [ ] **[PPTX兼容] 多行文字已用 `<tspan dy="...">` 或独立 `<text y="...">` 换行，无 `\n`**

---

## 防平淡自检（v3）

单页设计完成、写入前补一个正向检查（与上面的“防过度 / 兼容”自检互补）：
- [ ] 本页有视觉主体（数据图表 / 结构图 / 大数字 / UI原型 / 关系图 之一）
- [ ] 若是纯文字排列版式，已确认此页确实无可图形化内容（否则回 Phase 5 改为图表 / 结构图）
- [ ] 本页 ≥3 条 D 类数据 / 可对比排序 / 时间序列已用 charts 组件（否则回 Phase 5 改版式，不得文字化）

---

## 输出

写入：`./workspace/slides/slide_[page_index补零两位].svg`

汇报：**"第[N]页：[page_type]·[narrative_purpose] — [title前15字] → slide_[NN].svg"**

---
