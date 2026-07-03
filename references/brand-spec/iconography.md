# Iconography — Aham UI v6.1

## One library, one style

Across all Aham surfaces (网页 / 应用 macOS / Office / 邮件) there is exactly **one icon system**:

> **Lucide** — outline (line) icons, single-color, **1.5–2 px stroke**, rounded caps, on a 24×24 grid.

Why one library: mixing libraries is the #1 way that AI-generated work starts looking inconsistent. Pick Lucide. Stay there.

## Iron rule — where icons are allowed

> **Icons are for navigation and the send/compose bar only.** Everywhere in the **content area**, use **`•` + 文字**, never an icon.

- ✅ Allowed: left/side nav items, top bar, tab bar, the send/submit button in a compose bar.
- ❌ Not allowed: bullet lists, KPI labels, table cells, status rows, section headers, card bodies, callouts — these use `•` (or a 6px dot) + text.
- **File types** are shown as a **text badge** — `DOCX` / `PDF` / `XLSX` — never a colored brand-blue file icon.

Rationale: the content layer reads as a quiet white-paper. Icons there add visual noise and a second "color language"; a leading `•` + label carries the same meaning with less ink.

> **v2.1 例外（B / C 档）**：自 v2.1 起，**B 现代专业档 / C 高表现力档**允许在内容区使用 **Lucide 线性、单色**图标（如 `assets/components/icons.py` 的 `icon_circle` / 流程节点 / 关系图标识），用于结构化表达（流程、关系图、KPI 标识）；仍**禁多色 / 填充 / emoji**，单色随墨色或单蓝。**A 克制档**维持本铁规——内容区只用 `•` + 文字。落地判定见 `designer-rules.md`。

## CDN (recommended for prototypes)

```html
<!-- Lucide: vanilla -->
<script src="https://unpkg.com/lucide@latest"></script>
<i data-lucide="send"></i>
<script>lucide.createIcons();</script>

<!-- Or as inline SVGs from https://lucide.dev/icons/ -->
```

## Sizes

| Context | px |
|---|---|
| Nav item / send bar inline | 16 |
| Top bar | 20 |
| Tab bar | 24 |

(Sizes track `--icon-sm 16 / --icon-md 20 / --icon-lg 24` in `tokens.css`. Stroke 1.5–2 px.)
Content-area meaning is carried by `•` + text, not by sized icons.

## Color rules

- **Default** — inherit ink color (`#262626` on light / white on dark bars). Never a brand-blue or colored fill by default.
- **Active / interactive** — `#336EE8` (the single accent; e.g. selected nav item, active send button).
- **Status icons** — match the semantic color: success `#5A7A60` / warning `#8A7333` / danger `#9E3D31`. Status is still **dot + text first** (see below); the Lucide icon is optional.
- **Stroke** — 1.5–2 px (Lucide default ≈ 2 px; tighter UIs may go 1.5 px).
- **Fill vs outline** — **outline only**. Filled variants are reserved for the *selected/active tab indicator* and nothing else.

## Status mapping (replaces emoji)

The system explicitly bans emoji. **Primary channel is a 6px dot + text label**; a Lucide icon is optional and only in nav/send contexts.

| Meaning | dot + text (mandatory) | Lucide name (optional, nav/send only) |
|---|---|---|
| Confirm / pass | `● 合格` (`#5A7A60`) | `check` |
| Warning | `▲ 预警` (`#8A7333`) | `alert-triangle` |
| Fail / risk | `✕ 异常` / `✕ 风险` (`#9E3D31`) | `x` |
| In progress | `→ 进行中` (`#6E6E6E`) | — |
| Pending | `○ 待检` (`#9B9B9B`) | — |
| Send / submit | — | `send` |
| Search | — | `search` |
| Settings | — | `settings` |
| Back | — | `chevron-left` |
| Drop down | — | `chevron-down` |
| More | — | `more-horizontal` |

## Status double channel — dot + text is mandatory

For any status, use the **double channel**: a **6px dot (or textual symbol ●▲✕→○) plus a label**, semantic-color-coded. Color alone is never enough; the Lucide icon is optional and the dot + text is mandatory.

Example (content area — no icons):

```
●  合格      ▲  预警      ✕  异常      →  进行中      ○  待检
```

Colors: `●` success `#5A7A60` · `▲` warning `#8A7333` · `✕` danger `#9E3D31` · `→` / `○` neutral `#6E6E6E / #9B9B9B`.

## Hard bans

❌ **Emoji** in any production output (📊 🚀 ✨ 🔋 …)
❌ **Icons in the content area**（A 克制档）— bullets, KPIs, table cells, status rows, headers use `•`/dot + text, not icons。**B / C 档见上文 v2.1 例外**：内容区允许 Lucide 线性单色图标用于结构化表达
❌ **Colored-background pills stacking icons** (`bg-blue-light` rounded squares are retired)
❌ **Filled icons** — outline only; the *only* exception is the selected/active tab indicator
❌ **Multi-color** icons
❌ **Brand-color file-type icons** — use a `DOCX` / `PDF` text badge instead
❌ **3D / skeuomorphic / Fluent-3D / Icons8-3D** style
❌ **Filled + outline mixed** in one screen
❌ Decorative icons with no meaning — every icon must convey information
❌ Font Awesome legacy / iconfont multi-color packs
❌ Self-drawn SVGs that diverge from Lucide's geometry

> **PPTX-track registered exception**: `assets/components/icons.py` uses **self-drawn Lucide-style approximations**（为 SVG→PPTX 转换兼容；几何简化已审定，默认 stroke 1.7px 在 1.5–2 规范区间内）。QC 对 icons.py 产出按此放行，不判违例；新增图标仍须先过 `icons_preview.py` 缩略目检。

## Logo as icon (favicon, app icon)

Use `assets/logo.png` (full lockup). The brand mark renders as a small `#336EE8` square + `Aham` wordmark; the blue square is the *only* blue point on a cover/header. For 24 × 24 favicons, supply a graphic-mark-only SVG (see README caveats).

## Substitutions flagged to user

We use **Lucide** as the single library per Aham UI v6.1 — no substitution required. If a particular glyph is missing from Lucide, cross-check Tabler / Feather before introducing anything; never mix two libraries in one piece of work.
