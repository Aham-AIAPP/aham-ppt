// 幻灯片组件：固定数值、元素画法、图表和图标。每个函数返回一段 HTML，坐标单位 px，画布 1920×1080。
// 数值与 references/style-tokens.md 一致，元素的含义和用法见 references/style-elements.md。
// 组件只定元素画法，构图由本页内容决定。
// 用法：const K = require('<仓库>/assets/html2pptx/components'); 在 build.js 里拼页，最后 K.writeDeck(目录, 页列表)。
const fs = require('fs'), path = require('path');

// —— 固定数值 ——
const C = {
  ink1: '#1F2633', ink2: '#4A5363', ink3: '#7D8695', slate: '#5B6B82', mute: '#AEB5C0',
  line1: '#E3E6EB', line2: '#C9CED6', bg1: '#F6F7F9', bg2: '#EEF1F5', white: '#FFFFFF',
  ai: '#336EE8', aiBg: '#EAF0FD', svc: '#17998A', svcBg: '#E1F3F0', prod: '#D4892A', prodBg: '#FBF0DF',
};
const FS = { body: 18, name: 20, section: 22, sub: 26, big: 40, title: 52, cover: 72 };
const LW = { struct: 1.5, stroke: 1.8, flow: 2.4, heavy: 3.6 };
const RAD = { box: 6, card: 8 };
const MARGIN = 96, RIGHT = 1824, MAIN = { y0: 195, y1: 895 };
const MONO = 'Consolas,monospace';

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const n = v => +(+v).toFixed(1);
const isNum = v => /^[\d.,%¥+\-–~ ]+$/.test(String(v));

// 文字宽度估算：汉字按 1 个字号，拉丁字母和数字按 0.58，空格按 0.3
function tw(s, size = FS.body, bold = false) {
  let w = 0;
  for (const ch of String(s)) w += /[⺀-￿]/.test(ch) ? size : ch === ' ' ? size * 0.3 : size * 0.58;
  return w * (bold ? 1.04 : 1);
}

// —— 基础元素 ——

// 单行文字。y 是文字框顶边；align 取 left / center / right，x 是对应的锚点
function text(x, y, s, o = {}) {
  if (s === '' || s == null) return '';
  const size = o.size || FS.body, bold = (o.weight || 400) >= 600;
  const w = o.width || Math.ceil(tw(s, size, bold) * 1.12 + 8);
  const left = o.align === 'center' ? x - w / 2 : o.align === 'right' ? x - w : x;
  let st = `left:${n(left)}px;top:${n(y)}px;width:${n(w)}px;font-size:${size}px;line-height:1.25;color:${o.color || C.ink2};white-space:nowrap`;
  if (o.align && o.align !== 'left') st += `;text-align:${o.align}`;
  if (o.weight) st += `;font-weight:${o.weight}`;
  if (o.mono) st += `;font-family:${MONO}`;
  return `<p style="${st}">${o.html ? s : esc(s)}</p>`;
}

// 多行段落：按宽度自动换行；lines 为数组时每项一行
function para(x, y, w, lines, o = {}) {
  const size = o.size || FS.body, lh = o.lh || Math.round(size * 1.45);
  const body = Array.isArray(lines) ? lines.map(esc).join('<br>') : esc(lines);
  let st = `left:${n(x)}px;top:${n(y)}px;width:${n(w)}px;font-size:${size}px;line-height:${lh}px;color:${o.color || C.ink2}`;
  if (o.weight) st += `;font-weight:${o.weight}`;
  return `<p style="${st}">${body}</p>`;
}

// 方框。o: fill, stroke, sw, dash, r（默认 6）
function box(x, y, w, h, o = {}) {
  let st = `left:${n(x)}px;top:${n(y)}px;width:${n(w)}px;height:${n(h)}px`;
  if (o.fill) st += `;background:${o.fill}`;
  if (o.stroke) st += `;border:${o.sw || LW.stroke}px ${o.dash ? 'dashed' : 'solid'} ${o.stroke}`;
  const r = o.r === undefined ? RAD.box : o.r;
  if (r) st += `;border-radius:${r}px`;
  return `<div style="${st}"></div>`;
}

// 连线。o: color, sw, dash, head（none / end / start / both）, route（'' / hv / vh / elbow）
function line(x1, y1, x2, y2, o = {}) {
  const st = `color:${o.color || C.line2};border-width:${o.sw || LW.struct}px${o.dash ? ';border-style:dashed' : ''}`;
  return `<x-connector x1="${n(x1)}" y1="${n(y1)}" x2="${n(x2)}" y2="${n(y2)}" head="${o.head || 'none'}"${o.route ? ` route="${o.route}"` : ''} style="${st}"></x-connector>`;
}
const arrow = (x1, y1, x2, y2, o = {}) => line(x1, y1, x2, y2, { color: C.slate, sw: LW.flow, head: 'end', ...o });

function circle(cx, cy, r, o = {}) {
  let st = `left:${n(cx - r)}px;top:${n(cy - r)}px;width:${n(2 * r)}px;height:${n(2 * r)}px`;
  if (o.fill) st += `;background:${o.fill}`;
  if (o.stroke) st += `;border:${o.sw || LW.stroke}px solid ${o.stroke}`;
  return `<x-shape kind="ellipse" style="${st}"></x-shape>`;
}
function diamond(cx, cy, w, h, o = {}) {
  let st = `left:${n(cx - w / 2)}px;top:${n(cy - h / 2)}px;width:${n(w)}px;height:${n(h)}px`;
  if (o.fill) st += `;background:${o.fill}`;
  if (o.stroke) st += `;border:${o.sw || LW.stroke}px solid ${o.stroke}`;
  return `<x-shape kind="diamond" style="${st}"></x-shape>`;
}

// 胶囊：返回 { html, w }。y 是胶囊顶边，高 34
function chip(x, y, label, o = {}) {
  const color = o.color || C.ink2, size = o.size || FS.body, h = size + 16;
  const w = Math.ceil(tw(label, size, true) * 1.08 + 28), left = o.align === 'right' ? x - w : x;
  const st = `left:${n(left)}px;top:${n(y)}px;width:${w}px;height:${h}px;padding:0;font-size:${size}px;line-height:${h - 2 * LW.stroke}px;` +
    `text-align:center;font-weight:600;color:${color};background:${o.fill || C.white};border:${LW.stroke}px solid ${o.stroke || color};border-radius:${h / 2}px;white-space:nowrap`;
  return { html: `<p style="${st}">${esc(label)}</p>`, w };
}

// 标签与值：标签在上，值在下；值是数字时用等宽字体
function labelValue(x, y, label, value, o = {}) {
  return text(x, y, label, { color: C.ink3 }) +
    text(x, y + 28, value, { size: o.size || FS.name, color: o.color || C.ink1, weight: 700, mono: isNum(value) });
}

// 属性带：主图下方一行属性，items = [[标签, 值], ...]
function attrBand(items, o = {}) {
  const x = o.x || MARGIN, y = o.y || 906, w = o.w || RIGHT - MARGIN, h = o.h || 84, cw = w / items.length;
  let s = box(x, y, w, h, { fill: C.bg1 });
  items.forEach(([l, v], i) => {
    s += labelValue(x + 24 + i * cw, y + 12, l, v);
    if (i) s += line(x + i * cw, y + 16, x + i * cw, y + h - 16, { color: C.line2 });
  });
  return s;
}

// 图例：items = [[文字, 类型, 颜色]]；类型取 fill / stroke / dash / line / diamond / dot
function legend(items, x, y, o = {}) {
  const ws = items.map(([l]) => 14 + 8 + tw(l) + 24), total = ws.reduce((a, b) => a + b, 0);
  let cx = o.align === 'right' ? x - total : x, s = '';
  items.forEach(([l, kind, col], i) => {
    if (kind === 'fill') s += box(cx, y + 5, 14, 12, { fill: col, r: 3 });
    else if (kind === 'stroke') s += box(cx, y + 5, 14, 12, { fill: C.white, stroke: col, sw: 1.5, r: 3 });
    else if (kind === 'dash') s += box(cx, y + 5, 14, 12, { fill: C.white, stroke: col, sw: 1.5, r: 3, dash: true });
    else if (kind === 'line') s += line(cx, y + 11, cx + 16, y + 11, { color: col, sw: LW.flow });
    else if (kind === 'diamond') s += diamond(cx + 7, y + 11, 12, 12, { fill: col });
    else s += circle(cx + 7, y + 11, 6, { fill: col });
    s += text(cx + 22, y, l, { color: C.ink2 });
    cx += ws[i];
  });
  return s;
}

// —— 编号与标记 ——

// 件号气泡：清单项的编号，可跨页引用
function balloon(cx, cy, no, color = C.slate) {
  return circle(cx, cy, 15, { fill: C.white, stroke: color }) +
    text(cx, cy - 12, no, { color, weight: 700, mono: true, align: 'center', width: 30 });
}
// 流程序号：数据或步骤的先后
function stepNo(cx, cy, no, color = C.ai) {
  return circle(cx, cy, 13, { fill: color }) + text(cx, cy - 12, no, { color: C.white, weight: 700, mono: true, align: 'center', width: 26 });
}
// 界面注释号：截图或原型上的区域
function noteNo(cx, cy, no) {
  return circle(cx, cy, 13, { fill: C.ink1 }) + text(cx, cy - 12, no, { color: C.white, weight: 700, mono: true, align: 'center', width: 26 });
}
// 进度节点：主线上的工序或阶段
function node(cx, cy, no, o = {}) {
  return circle(cx, cy, 18, { fill: C.white, stroke: o.color || C.ink1, sw: LW.stroke }) +
    text(cx, cy - 12, no, { color: o.color || C.ink1, weight: 700, mono: true, align: 'center', width: 36 });
}
// 拦截叉：数据或权限停住的位置
function crossMark(cx, cy, size = 18, color = C.ink1) {
  const h = size / 2;
  return line(cx - h, cy - h, cx + h, cy + h, { color, sw: LW.flow }) + line(cx - h, cy + h, cx + h, cy - h, { color, sw: LW.flow });
}
// 尺寸线：时长或跨度。两端短竖线，双箭头，标签居中压白底
function dimLine(x1, x2, y, label, o = {}) {
  const color = o.color || C.ink2, w = Math.ceil(tw(label, FS.body, true) + 20);
  return line(x1, y - 12, x1, y + 12, { color }) + line(x2, y - 12, x2, y + 12, { color }) +
    line(x1, y, x2, y, { color, head: 'both' }) +
    `<p style="left:${n((x1 + x2) / 2 - w / 2)}px;top:${n(y - 14)}px;width:${w}px;font-size:${FS.body}px;line-height:28px;text-align:center;font-weight:700;color:${color};background:${o.bg || C.white};white-space:nowrap">${esc(label)}</p>`;
}
// 评审点：时间线上的关口。o.toY 给出时画竖向参考虚线
function reviewPoint(cx, y, label, o = {}) {
  let s = diamond(cx, y, 20, 20, { fill: C.ink1 });
  if (o.toY) s += line(cx, y - 10, cx, o.toY, { color: C.ink3, dash: true });
  if (label) s += text(cx, y + 16, label, { align: 'center', color: C.ink1, weight: 600 });
  return s;
}
// 引线：图上部件指到表格分组，起点画实心点；pts = [[x, y], ...]
function leader(pts, color = C.slate) {
  let s = circle(pts[0][0], pts[0][1], 4, { fill: color });
  for (let i = 1; i < pts.length; i++) s += line(pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1], { color });
  return s;
}
// 差值大数卡：前后对比的差值
function bigNumber(x, y, w, value, unit, label, o = {}) {
  const col = o.color || C.ai;
  return box(x, y, w, 132, { fill: o.fill || C.aiBg, r: RAD.card }) +
    text(x + 24, y + 16, label, { color: C.ink2 }) +
    text(x + 24, y + 46, value, { size: FS.big, color: col, weight: 700, mono: true }) +
    text(x + 24 + tw(value, FS.big) * 1.05 + 10, y + 64, unit, { color: col, weight: 600 });
}
// 等轴测叠板：x, y 是顶面左角，w 宽，d 进深，o.t 厚度。导出为图片
function plate(x, y, w, d, o = {}) {
  const top = o.top || C.bg2, side = o.side || C.slate, t = o.t || 14, dx = d * 0.87, dy = d * 0.5;
  const W = w + dx + 4, P = (a, b) => `${n(a + 2)},${n(b + 2)}`;
  const dash = o.dash ? ' stroke-dasharray="6 4"' : '', stroke = o.stroke || side, fillSide = o.dash ? 'none' : side;
  const topPoly = [[0, dy], [dx, 0], [dx + w, 0], [w, dy]].map(q => P(q[0], q[1])).join(' ');
  const front = [P(0, dy), P(w, dy), P(w, dy + t), P(0, dy + t)].join(' ');
  const right = [P(w, dy), P(dx + w, 0), P(dx + w, t), P(w, dy + t)].join(' ');
  return `<svg style="left:${n(x - 2)}px;top:${n(y - 2)}px;width:${n(W)}px;height:${n(dy + t + 4)}px" viewBox="0 0 ${n(W)} ${n(dy + t + 4)}" aria-label="${esc(o.label || '叠板')}">` +
    `<polygon points="${front}" fill="${fillSide}" stroke="${stroke}" stroke-width="1.5"${dash}/>` +
    `<polygon points="${right}" fill="${fillSide}" stroke="${stroke}" stroke-width="1.5"${dash}/>` +
    `<polygon points="${topPoly}" fill="${o.dash && !o.top ? C.white : top}" stroke="${stroke}" stroke-width="1.5"${dash}/></svg>`;
}
// 图框：外框加等分刻度，只用于封面
function frame(o = {}) {
  const x = 48, y = 48, w = 1824, h = 984, col = o.color || C.slate, nx = o.nx || 12, ny = o.ny || 7;
  let s = box(x, y, w, h, { stroke: col, sw: LW.struct, r: 0 });
  for (let i = 1; i < nx; i++) { const xx = x + w * i / nx; s += line(xx, y, xx, y + 12, { color: col }) + line(xx, y + h - 12, xx, y + h, { color: col }); }
  for (let i = 1; i < ny; i++) { const yy = y + h * i / ny; s += line(x, yy, x + 12, yy, { color: col }) + line(x + w - 12, yy, x + w, yy, { color: col }); }
  return s;
}

// —— 图标：线性单色，24 网格，导出为图片 ——
const ICONS = {
  user: '<circle cx="12" cy="8" r="4"/><path d="M5 21a7 7 0 0 1 14 0"/>',
  users: '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0"/><path d="M16 5.2a3.2 3.2 0 0 1 0 6M17 20a5.5 5.5 0 0 0-3-5"/>',
  server: '<rect x="4" y="4" width="16" height="6" rx="1.5"/><rect x="4" y="14" width="16" height="6" rx="1.5"/><path d="M8 7h.01M8 17h.01"/>',
  database: '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.6 3.1 3 7 3s7-1.4 7-3V6M5 12c0 1.6 3.1 3 7 3s7-1.4 7-3"/>',
  file: '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
  clipboard: '<rect x="6" y="4" width="12" height="18" rx="2"/><rect x="9" y="2.5" width="6" height="3.4" rx="1"/><path d="M9 11h6M9 15h6"/>',
  search: '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
  shield: '<path d="M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
  lock: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
  key: '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/>',
  check: '<circle cx="12" cy="12" r="9"/><path d="M8 12.2l2.6 2.6L16 9"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
  calendar: '<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 9h16M8 3v4M16 3v4"/>',
  flag: '<path d="M6 21V4M6 4h11l-2.5 4L17 12H6"/>',
  message: '<path d="M4 5h16v11H9l-4 4z"/><path d="M8 9h8M8 12h5"/>',
  bell: '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
  monitor: '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M9 20h6M12 16v4"/>',
  phone: '<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M11 18h2"/>',
  scan: '<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3"/><path d="M4 12h16"/>',
  factory: '<path d="M3 21V10l6 4V10l6 4V6l3 1v14z"/><path d="M3 21h18"/>',
  truck: '<rect x="2" y="7" width="12" height="9" rx="1.5"/><path d="M14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17.5" cy="18" r="2"/>',
  box: '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
  layers: '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5M3 16.5l9 5 9-5"/>',
  link: '<path d="M9 12a4 4 0 0 1 4-4h2a4 4 0 0 1 0 8h-1"/><path d="M15 12a4 4 0 0 1-4 4H9a4 4 0 0 1 0-8h1"/>',
  gear: '<circle cx="12" cy="12" r="3.2"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.5 5.5l2 2M16.5 16.5l2 2M18.5 5.5l-2 2M7.5 16.5l-2 2"/>',
  chart: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 15v-3M12 15V9M17 15v-5"/>',
  trend: '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
  cpu: '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
  building: '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M10 21v-3h4v3"/>',
  wallet: '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 14h2"/>',
};
const ICON_NAMES = Object.keys(ICONS);

// 图标。x, y 是左上角；名称不在表里时报错，避免静默换成别的图标
function icon(name, x, y, size = 28, color = C.ink2, sw = 1.8) {
  if (!ICONS[name]) throw new Error(`图标 ${name} 不存在，可用：${ICON_NAMES.join(' ')}`);
  return `<svg style="left:${n(x)}px;top:${n(y)}px;width:${size}px;height:${size}px" viewBox="0 0 24 24" aria-label="${name}" fill="none" stroke="${color}" stroke-width="${n(sw * 24 / size)}" stroke-linecap="round" stroke-linejoin="round">${ICONS[name]}</svg>`;
}
// 圆底图标：方框名前的类别标识
function iconCircle(name, cx, cy, r = 20, o = {}) {
  const s = Math.round(r * 1.2);
  return circle(cx, cy, r, { fill: o.bg || C.bg2 }) + icon(name, cx - s / 2, cy - s / 2, s, o.color || C.ink2);
}

// —— 图表：全部画成可编辑的形状、线条和文字 ——
// 数值格式：同一张图的数统一位数。digits 未给时，数据里有小数就保留 1 位，全是整数就不带小数
const fmt = (v, digits) => typeof v !== 'number' ? String(v) : v.toFixed(digits);
const autoDigits = (vals, digits) => digits ?? (vals.every(Number.isInteger) ? 0 : 1);

// 条形图。o: x, y, w, h, items:[{label, value, hi}], unit, digits, max, labelW（横向时标签列宽）, vertical
// 高亮项用墨一，其余用线二；高亮的含义写在子标题或图例里
function bars(o) {
  const items = o.items, max = o.max || Math.max(...items.map(i => i.value)), unit = o.unit || '';
  const d = autoDigits(items.map(i => i.value), o.digits);
  let s = '';
  if (!o.vertical) {
    const lw = o.labelW || 220, x0 = o.x + lw, bw = o.w - lw - 120, step = o.h / items.length, t = Math.min(48, step * 0.56);
    items.forEach((it, i) => {
      const y = o.y + i * step + (step - t) / 2, len = bw * it.value / max;
      s += text(x0 - 20, y + t / 2 - 13, it.label, { size: FS.name, color: it.hi ? C.ink1 : C.ink2, weight: it.hi ? 700 : 400, align: 'right' });
      s += box(x0, y, Math.max(len, 2), t, { fill: it.hi ? C.ink1 : C.line2, r: 0 });
      s += text(x0 + len + 12, y + t / 2 - 13, fmt(it.value, d) + unit, { size: FS.name, color: C.ink1, weight: 700, mono: true });
    });
    s += line(x0, o.y, x0, o.y + o.h, { color: C.ink3 });
  } else {
    const base = o.y + o.h - 40, bh = o.h - 90, step = o.w / items.length, t = Math.min(96, step * 0.56);
    items.forEach((it, i) => {
      const cx = o.x + i * step + step / 2, len = bh * it.value / max;
      s += box(cx - t / 2, base - len, t, Math.max(len, 2), { fill: it.hi ? C.ink1 : C.line2, r: 0 });
      s += text(cx, base - len - 34, fmt(it.value, d) + unit, { size: FS.name, color: C.ink1, weight: 700, mono: true, align: 'center' });
      s += text(cx, base + 10, it.label, { color: it.hi ? C.ink1 : C.ink2, weight: it.hi ? 700 : 400, align: 'center' });
    });
    s += line(o.x, base, o.x + o.w, base, { color: C.ink3 });
  }
  return s;
}

// 折线图。o: x, y, w, h, labels:[横轴文字], series:[{name, values, color}], unit, digits, min, max, ticks（纵轴格数）
// 每条线在末端写名称和末值，不另放图例。浅灰线的文字改用墨三，保证对比度
function lineChart(o) {
  const all = o.series.flatMap(s => s.values), lo = o.min ?? 0, unit = o.unit || '';
  // 刻度取 1、2、2.5、5 乘 10 的整数次幂，纵轴读数是整齐的数
  // o.ticks 未给时在 4 到 6 格里选顶端最贴近最大值的一种
  const top = o.max ?? Math.max(...all), d = autoDigits(all, o.digits);
  const axis = k => { const raw = (top - lo) / k, mag = 10 ** Math.floor(Math.log10(raw || 1));
    const step = [1, 2, 2.5, 5, 10].map(m => m * mag).find(v => v >= raw); return { k, step, hi: lo + step * k }; };
  const { k: nT, step, hi } = o.ticks ? axis(o.ticks) : [4, 5, 6].map(axis).sort((a, b) => a.hi - b.hi)[0];
  const tickDigits = Number.isInteger(step) ? 0 : 1;
  const x0 = o.x + 70, x1 = o.x + o.w - 220, y0 = o.y, y1 = o.y + o.h - 44;
  const X = i => x0 + (x1 - x0) * i / (o.labels.length - 1), Y = v => y1 - (y1 - y0) * (v - lo) / (hi - lo);
  let s = '';
  for (let k = 0; k <= nT; k++) {
    const v = lo + (hi - lo) * k / nT, y = Y(v);
    s += line(x0, y, x1, y, { color: k ? C.line1 : C.ink3 });
    s += text(x0 - 14, y - 12, fmt(v, tickDigits), { color: C.ink3, mono: true, align: 'right' });
  }
  o.labels.forEach((l, i) => { s += text(X(i), y1 + 12, l, { color: C.ink3, align: 'center' }); });
  o.series.forEach(se => {
    const col = se.color || C.ink1;
    for (let i = 1; i < se.values.length; i++) s += line(X(i - 1), Y(se.values[i - 1]), X(i), Y(se.values[i]), { color: col, sw: LW.flow });
    se.values.forEach((v, i) => { s += circle(X(i), Y(v), 5, { fill: col }); });
    const last = se.values[se.values.length - 1];
    s += text(X(se.values.length - 1) + 16, Y(last) - 13, `${se.name}　${fmt(last, d)}${unit}`, { color: col === C.mute ? C.ink3 : col, weight: 700 });
  });
  return s;
}

// 坡度图：两个时点的前后对比。o: x, y, w, h, items:[{label, a, b, hi}], left, right, unit, digits, min, max
function slope(o) {
  const vals = o.items.flatMap(i => [i.a, i.b]), lo = o.min ?? Math.min(...vals), hi = o.max || Math.max(...vals);
  const xa = o.x + 260, xb = o.x + o.w - 260, y0 = o.y + 50, y1 = o.y + o.h, unit = o.unit || '';
  const Y = v => y1 - (y1 - y0) * (v - lo) / ((hi - lo) || 1), d = autoDigits(vals, o.digits);
  let s = text(xa, o.y, o.left || '前', { color: C.ink3, weight: 600, align: 'center' }) + text(xb, o.y, o.right || '后', { color: C.ink3, weight: 600, align: 'center' });
  s += line(xa, y0 - 10, xa, y1 + 10, { color: C.line2 }) + line(xb, y0 - 10, xb, y1 + 10, { color: C.line2 });
  o.items.forEach(it => {
    const col = it.hi ? C.ink1 : C.mute;
    s += line(xa, Y(it.a), xb, Y(it.b), { color: col, sw: it.hi ? LW.flow : LW.struct });
    s += circle(xa, Y(it.a), 5, { fill: col }) + circle(xb, Y(it.b), 5, { fill: col });
    s += text(xa - 16, Y(it.a) - 13, `${it.label}　${fmt(it.a, d)}${unit}`, { color: it.hi ? C.ink1 : C.ink3, weight: it.hi ? 700 : 400, align: 'right' });
    s += text(xb + 16, Y(it.b) - 13, `${fmt(it.b, d)}${unit}`, { color: it.hi ? C.ink1 : C.ink3, weight: it.hi ? 700 : 400, mono: true });
  });
  return s;
}

// 甘特条：阶段有起止并可重叠。o: x, y, w, labelW, rowH, periods:[表头文字], rows:[{name, start, end, fill, stroke, label, note}]
// start、end 以期数计，可为小数；label 写在条内，note 写在条下方
function gantt(o) {
  const lw = o.labelW || 240, x0 = o.x + lw, pw = (o.w - lw) / o.periods.length, rh = o.rowH || 80;
  let s = '';
  o.periods.forEach((p, i) => {
    s += text(x0 + i * pw + pw / 2, o.y, p, { color: C.ink3, align: 'center' });
    s += line(x0 + i * pw, o.y + 36, x0 + i * pw, o.y + 44 + o.rows.length * rh, { color: C.line1 });
  });
  s += line(x0 + o.periods.length * pw, o.y + 36, x0 + o.periods.length * pw, o.y + 44 + o.rows.length * rh, { color: C.line1 });
  o.rows.forEach((r, i) => {
    const y = o.y + 52 + i * rh, bh = Math.min(52, rh - 24);
    s += text(o.x, y + bh / 2 - 13, r.name, { size: FS.name, color: C.ink1, weight: 600 });
    s += box(x0 + r.start * pw + 4, y, (r.end - r.start) * pw - 8, bh, { fill: r.fill || C.bg2, stroke: r.stroke || C.slate });
    if (r.label) s += text(x0 + r.start * pw + 18, y + bh / 2 - 13, r.label, { color: r.stroke || C.ink2, weight: 600 });
    if (r.note) s += text(x0 + r.start * pw + 4, y + bh + 8, r.note, { color: C.ink3 });
  });
  return s;
}

// —— 页面 ——

// 正文页框架：页眉章名、页眉右侧引用、标题、子标题、提供方胶囊、属性带、页脚线、页脚标注、页码
function page(o) {
  let s = text(MARGIN, 39, o.chapter || '', { color: C.ink3 }) +
    text(MARGIN, 70, o.title, { size: FS.title, color: C.ink1, weight: 700 }) +
    text(MARGIN, 141, o.sub || '', { size: FS.sub, color: C.ink2 });
  if (o.right) s += text(RIGHT, 39, o.right, { color: C.ink3, align: 'right' });
  if (o.provider) s += chip(RIGHT, 142, o.provider[0], { color: o.provider[1], align: 'right' }).html;
  s += o.body || '';
  if (o.attrs) s += attrBand(o.attrs);
  s += line(MARGIN, 1017, RIGHT, 1017, { color: C.line1 });
  if (o.foot) s += text(MARGIN, 1030, o.foot, { color: C.ink3 });
  if (o.no) s += text(RIGHT, 1030, String(o.no), { color: C.ink3, mono: true, align: 'right' });
  return slide(s, o.bg, o.notes);
}
// 无框架页：封面、目录、章节页
function slide(body, bg = C.white, notes) {
  return `<section style="background:${bg}">\n${body}\n${notes ? `<aside>${esc(notes)}</aside>\n` : ''}</section>\n`;
}
// 写出 deck.json 和 slides/<id>.html。pages = [{ id, html }]
function writeDeck(dir, pages) {
  fs.mkdirSync(path.join(dir, 'slides'), { recursive: true });
  pages.forEach(p => fs.writeFileSync(path.join(dir, 'slides', p.id + '.html'), p.html));
  fs.writeFileSync(path.join(dir, 'deck.json'), JSON.stringify({ order: pages.map(p => p.id) }, null, 2));
}

module.exports = {
  C, FS, LW, RAD, MARGIN, RIGHT, MAIN, esc, tw,
  text, para, box, line, arrow, circle, diamond, chip, labelValue, attrBand, legend,
  balloon, stepNo, noteNo, node, crossMark, dimLine, reviewPoint, leader, bigNumber, plate, frame,
  icon, iconCircle, ICON_NAMES, bars, lineChart, slope, gantt,
  page, slide, writeDeck,
};
