# 三档主题系统

提供三个视觉档，**共用同一套内容与组件，只切换"主题层"**（封面/目录/章节模板 + 页眉皮肤）。
不引入多色体系——实测多色"AI 感 / 营销感"偏重，且与"单一主色 + 中性灰"品牌冲突；
三档都坚持单一品牌主色 + 四级墨灰。

| 维度 | A · 克制档 | B · 现代专业档（默认） | C · 高表现力档 |
|---|---|---|---|
| 气质 | 纯白白皮书、安静权威 | 现代专业、有设计感、信息层次强 | 演说感、深浅三明治节奏 |
| 适用 | 高层正式汇报、严谨决策 | 多数客户方案、汇报 + 会后阅读 | 路演 / 竞标 / 重点客户（严肃决策仍用 A） |
| 封面 | 极简：标题 + 目录竖排 + 落款 | Hero：左大标题 + 英文衬词 + 右侧浅色信息块（章节缩略 motif） | 深底 `cover_dark`：深墨底大字 + 右侧深面板导览 |
| 目录 | 编号 + 标题 + 一句话 | 每章 图标圆 + 编号 + 描述 + 右侧要点 | 同 B（深底仅限三类重音页） |
| 章节页 | 大编号 + 标题 | 大水印编号 + 标题 + 右侧"本章内容"图标清单 | 深底 `section_dark`：超大编号水印 + 浅字 |
| 内容页 | 留白 + 细横线 + 主色点缀 | A 的一切 + 线性图标 / 图标圆 / 编号圆徽 / 关系图组件 | B 的一切 + 数据图表占版面主导 + 更大深色结论块 + 金句页 `quote_dark` |
| 颜色 | 单主色点缀 | 单主色点缀（同 A，不加多色） | 同 A/B 单主色；深底 `#1C1C1C` 仅封面/章节/金句三类页 |

> 把"设计化的封面 / 目录 / 章节"归入 **B 档**；A 档保留极简版。
> 状态双通道、禁渐变/3D/阴影/衬线/emoji 等铁规三档一致。**纯白底是 A/B 铁规**；C 档仅**封面/章节/金句**三类重音页例外用深底 `#1C1C1C`（brand.md §2.1 已登记），内容页仍纯白。

## C · 高表现力档（激进；路演 / 竞标 / 重点客户方案）

在 B 档基础上**把设计感下沉到内容页**，允许更强视觉手段（仍守单一主色 + 中性灰，不引入多色相）：
- **深色重音页**：封面 / 章节页 / 金句页用深墨底 `#1C1C1C`（非纯黑，brand.md §2.1 已登记的唯一非纯白底例外）+ 浅色大字，制造“白—白—深”三明治节奏。
- **半幅大数字冲击页**：关键结论用 I 系 ≥120pt mono 大数字 + 右侧拆解。
- **数据图表占版面主导**：数据页直接用 charts 组件铺满主区，不塞进小卡。
- **内容页更大深色块**：允许更大面积 `#262626` 结论块（如 S-07 深色结论区放大）。

**代价（务必向用户说明）**：C 档偏离“安静的权威 / 白皮书”，更接近“有设计感的演说稿”，适合路演 / 竞标；严肃决策汇报仍用 A 档。
**绝不松动的底线**：单一主色 + 中性灰、禁渐变 / 3D / 投影 / 饼图、禁衬线、数字 mono、状态双通道、禁 emoji。
**换肤纪律（v3.2）**：任何换肤/主题演示（如活动皮肤）中，深底也必须取 `--ppt-surface-dark #1C1C1C`，禁手写近似值（docs 演示图曾出现 #171717 漂移实例）；彩色顶条等仅限演示物料，**不得进入客户交付**。
> Step 1.5 选档增加 C 选项。C 档深色模板**已实现**于 `themes.py`：`cover_dark(brand,title,subtitle,chapters,meta_left,meta_right)` / `section_dark(num,zh,summary,total,items)` / `quote_dark(lines,attribution,brand)`（均深底 #1C1C1C + 浅字，已渲染 + 转换实测）。

## 调用（assets/components/themes.py）

```python
from themes import cover, toc, section, chrome
theme = "B"   # 由 Step 1.5 用户选择，默认 B
ch = [("01","章名","一句话描述","layers"), ...]   # (num, zh, sub, icon)

cover(theme, brand="{品牌}", title="{项目} 建设规划",
      subtitle="副标题", chapters=ch,
      meta_left="受众：{受众} · 日期：YYYY-MM-DD", meta_right="机密 · 仅限内部")
toc(theme, ch)
section(theme, "02", "章节标题", "一句话引导",
        items=[("grid","要点一"),("refresh","要点二")])   # items 仅 B 用
chrome(theme, "页眉小标", "页面 Action Title", "来源", page="5", total="20",
       body=<svg 片段>, brand="{品牌}", icon="trend")        # icon 仅 B 用
```

**C 档调用（深色模板是独立函数，不走 theme 参数）：**

```python
from themes import cover_dark, section_dark, quote_dark, chrome
from charts import bar, line, waterfall   # 数据页按形态选

cover_dark(brand="{品牌}", title="{项目} 建设规划", subtitle="副标题",
           chapters=ch, meta_left="受众：… · YYYY-MM-DD", meta_right="机密")
section_dark("02", "章节标题", "一句话引导", total="04",
             items=["要点一", "要点二", "要点三"])   # 注意：items 是字符串列表（与 B 的 (icon,text) 不同）
quote_dark(["金句第一行", "第二行", "第三行"], attribution="—— 出处", brand="{品牌}")
chrome("B", "页眉小标", "Action Title", "来源", page="5", total="20", body=<svg>)  # C 档内容页仍用 B 皮肤
```
- C 档 = B 的内容页皮肤 + 深色封面/章节/金句重音页 + 数据页 charts 占主导；深色页穿插制造“白—白—深”节奏。

- `theme="A"` 时，section 的 `items` / chrome 的 `icon` 自动忽略，回退极简。
- 所有文字参数化，**不在模板内写死任何品牌/客户/项目名**——出片前用真实文字替换占位。
- 颜色默认取 Aham 角色色；换品牌时改 `components.py` 顶部的 `ACC` 等角色色常量即可，**不要在页面里散落硬编码色值**。
