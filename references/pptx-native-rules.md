# PPTX Native Rules · SVG转原生PPT规范

> **核心原则**：SVG 是唯一真源，原生 PPT 由机器从 SVG 转换得到，不手写。

---

## 何时走本规则(pptx-native 路径)

当 Phase 1 记录的 `output_format` 是以下任一值时:
- `pptx-native`(仅原生 PPT)
- `both`(SVG + 原生 PPT 双轨,推荐)

当 `output_format` 是 `svg` 时,不走本规则,直接走 designer-rules.md。

---

## 执行步骤(简洁版)

### 步骤 1 · 前置确认

本路径的前提:
- [ ] Phase 5 已完成,`svg_final/` 下有全部 SVG 文件
- [ ] Phase 6 视觉 QC(含第 5 层)已通过
- [ ] 用户对 SVG 视觉效果无异议

**不满足任一条件时，不要启动转换步骤。**

### 步骤 2 · 调用工具链

**转换调用代码段以 `phase-07.md` 步骤5 为唯一维护处，本文件不复写**。要点：
- `sys.path` 指向本机 `aham-ppt/assets` 绝对路径（必填，无可用默认值）；
- `from svg_to_pptx_wrapper import svg_to_native_pptx`；
- `canvas_format='auto'`（按 SVG viewBox 推导，16:9 设计基准）；返回值必须 assert。

### 步骤 3 · 验证产物

转换完成后必做:

1. **文件大小检查**:正常范围 50-300 KB(纯矢量)
   - 如果超过 1 MB,说明 SVG 里有栅格图嵌入,需要确认
2. **LibreOffice 转 PDF 抽检**:
   ```bash
   libreoffice --headless --convert-to pdf output.pptx
   ```
3. **视觉对比**:抽 3 张关键页(首页/复杂页/尾页),与对应 SVG 源的 PNG 对比
4. **可编辑性验证**(如果有 PowerPoint 环境):
   - 打开 PPTX
   - 双击任意文字 → 应该能直接进入编辑
   - 单击任意形状 → 应该能独立选中

### 步骤 4 · 交付

交付三件套(最少):
- `方案.pptx` · 原生可编辑 PPT
- `方案.pdf` · 打印分发版
- `svg_final/` · SVG 真源(放在 zip 里)

---

## 工具链能力范围

### 支持的 SVG 元素

| 元素 | 支持度 | 说明 |
|---|---|---|
| `<rect>` | ✅ 完整 | 支持圆角、填充、描边 |
| `<circle>` | ✅ 完整 | |
| `<ellipse>` | ✅ 完整 | |
| `<line>` | ✅ 完整 | 支持虚线、端点 |
| `<polygon>` | ✅ 完整 | 支持任意多边形（梯形/五边形等），**箭头首选方式** |
| `<polyline>` | ✅ 完整 | |
| `<path>` | ✅ 完整 | 贝塞尔曲线通过细分近似 |
| `<text>` | ✅ 完整 | CJK/英文自动双字体，可编辑 textbox |
| `<tspan>` | ✅ 完整 | 支持多 run 的复杂文字，**换行唯一可靠方式** |
| `<g>` + `translate` | ✅ 完整 | translate偏移正常传递 |
| `<g>` + `scale`（正数） | ✅ 完整 | 正数缩放正常传递 |
| `<g>` + `rotate` | ⚠️ 有风险 | 仅旋转容器，子元素绝对坐标不变，**实测会偏移，禁止使用** |
| `<g>` + `scale`（负数） | ❌ 不支持 | 负数缩放（镜像）被忽略，改用翻转画法 |
| `<image>` | ✅ 完整 | base64 或外部 URL |
| `<defs>` + `<use>` | ✅ 部分 | 基本图案引用 |
| `<marker>` on `<line>` | ⚠️ 部分 | 仅 `<line>` 元素上有限支持 |
| `<marker>` on `<path>` | ❌ 不支持 | `<path>/<polyline>` 上的 `marker-end` 静默丢失，**改用 `<polygon>`** |
| `<linearGradient>` | ✅ 部分 | 简单线性渐变 |
| 滤镜（模糊/阴影） | ⚠️ 部分 | 仅基础阴影 |
| `<mask>` | ⚠️ 部分 | 仅 clip-path |

### 不支持/需规避

> 完整的 SVG→PPTX 兼容雷区与正确写法以 `designer-rules.md` §PPTX兼容性硬性约束为**单一真源**；下表只列元素支持度速查。

- `<marker>` on `<path>/<polyline>`：转换后静默丢失，**用 `<polygon>` 画箭头替代**
- `<g transform="rotate(...)">` ：子元素坐标偏移，**改用元素级 rotate 或绝对坐标**
- `<g transform="scale(-1...)">` 负数缩放：被忽略
- 文字内容里的裸露 `&`：工具链会自动修复，但 `<>`、`"` 仍需手动转义
- 多行文字用 `\n`：被折叠为空格，**改用 `<tspan dy="1.4em">` 或独立 `<text y="...">` 标签**
- 复杂 CSS 选择器（建议用 inline style）
- SMIL 动画
- JS 交互
- 超大位图嵌入（> 5 MB，会让 PPT 膨胀）
- `<text>`/`<ellipse>` 上 translate+rotate 组合变换：实测转换后漂移，**不做竖排**（详见 designer-rules 约束7）
- 字符 `✓/✗`：tofu 高危，**用 consulting.py `check()` 线画对勾**

---

## 常见问题排查

### 问题 1 · 整页空白（最常见）

**原因A**：SVG 文字内容里有未转义的 `&`（如 "R&D"），导致 XML 解析崩溃。
**处置**：工具链已内置自动修复裸露 `&`，但 `<`、`>`、`"` 仍需手动转义。
检查 SVG 里所有文字内容是否有这些特殊字符。

**原因B**：SVG 文件编码非 UTF-8。
**处置**：工具链会自动尝试 latin-1 回退，但最好确保 SVG 文件保存为 UTF-8。

**原因C**：SVG viewBox 超出内容范围，所有元素坐标落在可视区外。
**处置**：检查 SVG 根元素的 `viewBox` 是否覆盖所有内容，默认应为 `0 0 1280 720`。

### 问题 2 · 箭头消失

**原因**：`<path>` 或 `<polyline>` 上的 `marker-end` 在转换时静默丢失。
**处置**：改用 `<polygon>` 多边形直接画箭头头部，`<line>` 画箭杆。

```svg
<!-- 替换方案：polygon画箭头 -->
<line x1="100" y1="200" x2="390" y2="200" stroke="#9B9B9B" stroke-width="2"/>
<polygon points="385,194 400,200 385,206" fill="#262626"/>
```

### 问题 3 · 元素位置偏移

**原因A**：使用了 `<g transform="rotate(...)">` group 级别旋转。
**处置**：把旋转属性移到具体元素上，或计算旋转后的绝对坐标直接填入。

**原因B**：嵌套 `<g>` 的 scale 传递在多层嵌套时累乘出错。
**处置**：尽量减少 `<g>` 嵌套层数，复杂变换用绝对坐标替代。

### 问题 4 · 多行文字变成一行

**原因**：文字内容里用了 `\n` 换行，工具链将其折叠为空格。
**处置**：改用 `<tspan x="..." dy="1.4em">` 手动换行。

### 问题 5 · 某页报警告 `Failed to convert <xxx>`

**原因**：SVG 含不支持的元素（如 `<use>` 引用的复杂图形）。
**处置**：看 verbose 输出定位元素，用支持的基础图形替代。

### 问题 6 · 字体显示异常（Windows 上）

**原因**：SVG 里用了 macOS 专有衬线字体，Windows 映射为备用字体后宽度不一致。
**处置**：标题统一用无衬线栈 `Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif`，
数字用 `'JetBrains Mono', Consolas, monospace`；不再使用衬线/宋体。
单一无衬线 + 等宽数字，跨平台宽度一致、层级靠字号字重而非字形。

### 问题 7 · 转换成功但 PPT 文字无法编辑

**原因**：没有使用 `use_native_shapes=True`（默认是图片嵌入模式）。
**处置**：通过 `svg_to_native_pptx()` 调用时默认已启用 `use_native_shapes=True`，确认调用的是 wrapper 而不是直接调底层。

---

## 编辑语义边界（v3.2 明示，交付前须让用户知情）

本工具链的文本是**标签级**而非段落级——转换器把多行文字（`<tspan dy>`）拆为 N 个独立单行文本框：

- 双击可改字、可改色、可换字体（原生可编辑成立）；但**改长一句不会自动回流换行**，需手动挪动下一行框；
- 项目符号圆点是画出来的图形，**不是 PPT 列表语义**（不能按 Tab 升降级、不能自动续点）；
- 同一 x 坐标、不同字号的文本框之间存在约「字号×0.1px」的系统性左移（视觉可忽略，知悉即可）。

**交付话术模板**：「每个元素都是原生形状/文本框，双击即可修改文字与颜色；若需整段重写或增删行，建议改 SVG 真源后重转（SVG 是单一可信源），比在 PPT 里手动挪框更快更齐。」

## 核心纪律

### ✅ 应该做的

- ✅ 设计阶段专注把 SVG 做好
- ✅ 输出 PPT 时用 `svg_to_native_pptx()` 一键转换
- ✅ 如果 PPT 效果有问题,**回去改 SVG 源**,重新转换
- ✅ 始终保持 SVG 为真源,PPT 为衍生物

### ❌ 不应该做的

- ❌ 手写 python-pptx 代码拼形状(老路,已废弃)
- ❌ 用 EMF 嵌入后声称"可编辑"(场景 21 血泪教训)
- ❌ PPT 生成后**直接改 PPT**(会和 SVG 真源漂移,场景 20)
- ❌ "这页我手打几个字快一点"(永远不!场景 20)

---

## 与其他 references 的协作

| 阶段 | 调用文件 |
|---|---|
| Phase 7 SVG 设计 | designer-rules.md |
| Phase 7/8 PPT 转换 | 本文件 |
| Phase 8 质检 | phase-08.md（五层质检） |
| 品牌规范 | brand.md |
| 质量审计 | quality-audit-protocol.md |

---