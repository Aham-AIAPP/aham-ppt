// 幻灯片组件：固定数值和元素画法。每个函数返回一段 HTML，坐标单位 px，画布 1920×1080。
// 数值与 references/style-tokens.md 一致，元素用法见 references/style-elements.md。
// 组件只管零件长什么样，页面怎么构图由内容决定。
// 用法：const K = require('<仓库>/assets/html2pptx/components'); 写 build.js 拼页，K.writeDeck() 输出。
const fs = require('fs'), path = require('path');

const C = {
  ink1: '#1F2633', ink2: '#4A5363', ink3: '#7D8695', slate: '#5B6B82', mute: '#AEB5C0',
  line1: '#E3E6EB', line2: '#C9CED6', bg1: '#F6F7F9', bg2: '#EEF1F5', white: '#FFFFFF',
  ai: '#336EE8', aiBg: '#EAF0FD', svc: '#17998A', svcBg: '#E1F3F0', prod: '#D4892A', prodBg: '#FBF0DF',
};
const FS = { body: 18, name: 20, section: 22, sub: 26, big: 40, title: 52, cover: 72 };
const LW = { struct: 1.5, stroke: 1.8, flow: 2.4, heavy: 3.6 };
const RAD = { box: 6, card: 8 };
const MARGIN = 96, RIGHT = 1824;
const MONO = 'Consolas,monospace';

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const n = v => +(+v).toFixed(1);

// 文字宽度估算：汉字按 1 个字号，拉丁字母和数字按 0.58，空格 0.3
function tw(s, size = FS.body, bold = false) {
  let w = 0;
  for (const ch of String(s)) w += /[⺀-￿]/.test(ch) ? size : ch === ' ' ? size * 0.3 : size * 0.58;
  return w * (bold ? 1.04 : 1);
}

// 单行文字。y 是文字框顶边。align 取 left / center / right，x 是对应的锚点。
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

// 多行段落：给定宽度自动换行；lines 为字符串数组时按 <br> 分行
function para(x, y, w, lines, o = {}) {
  const size = o.size || FS.body, lh = o.lh || Math.round(size * 1.45);
  const body = Array.isArray(lines) ? lines.map(esc).join('<br>') : esc(lines);
  let st = `left:${n(x)}px;top:${n(y)}px;width:${n(w)}px;font-size:${size}px;line-height:${lh}px;color:${o.color || C.ink2}`;
  if (o.weight) st += `;font-weight:${o.weight}`;
  return `<p style="${st}">${body}</p>`;
}

function box(x, y, w, h, o = {}) {
  let st = `left:${n(x)}px;top:${n(y)}px;width:${n(w)}px;height:${n(h)}px`;
  if (o.fill) st += `;background:${o.fill}`;
  if (o.stroke) st += `;border:${o.sw || LW.stroke}px ${o.dash ? 'dashed' : 'solid'} ${o.stroke}`;
  const r = o.r === undefined ? RAD.box : o.r;
  if (r) st += `;border-radius:${r}px`;
  return `<div style="${st}"></div>`;
}

// 连线。head: none / end / start / both；route: '' / hv / vh / elbow
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

// 胶囊标签：返回 { html, w }。y 是胶囊顶边，高 34
function chip(x, y, label, o = {}) {
  const color = o.color || C.ink2, size = o.size || FS.body, h = size + 16;
  const w = Math.ceil(tw(label, size, true) * 1.08 + 28), left = o.align === 'right' ? x - w : x;
  const st = `left:${n(left)}px;top:${n(y)}px;width:${w}px;height:${h}px;padding:0;font-size:${size}px;line-height:${h - 2 * LW.stroke}px;` +
    `text-align:center;font-weight:600;color:${color};background:${o.fill || C.white};border:${LW.stroke}px solid ${o.stroke || color};border-radius:${h / 2}px;white-space:nowrap`;
  return { html: `<p style="${st}">${esc(label)}</p>`, w };
}

// 标签在上、数值在下。数值是数字时用等宽字体
function labelValue(x, y, label, value, o = {}) {
  return text(x, y, label, { size: FS.body, color: C.ink3 }) +
    text(x, y + 28, value, { size: o.size || FS.name, color: o.color || C.ink1, weight: 700, mono: /^[\d.,%¥+\-–~ ]+$/.test(String(value)) });
}

// 属性带：主图下方的一行属性，items = [[标签, 值], ...]
function attrBand(items, o = {}) {
  const x = o.x || MARGIN, y = o.y || 906, w = o.w || RIGHT - MARGIN, h = o.h || 84, cw = w / items.length;
  let s = box(x, y, w, h, { fill: C.bg1 });
  items.forEach(([l, v], i) => {
    s += labelValue(x + 24 + i * cw, y + 12, l, v);
    if (i) s += line(x + i * cw, y + 16, x + i * cw, y + h - 16, { color: C.line2 });
  });
  return s;
}

// 图例：items = [[文字, 类型, 颜色]]；类型 fill / stroke / dash / line / diamond / dot
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

// —— 元素词汇（画法见 style-elements.md）——

// 件号气泡：清单项的编号，跨页引用时用
function balloon(cx, cy, no, color = C.slate) {
  return circle(cx, cy, 15, { fill: C.white, stroke: color }) +
    text(cx, cy - 12, no, { size: FS.body, color, weight: 700, mono: true, align: 'center', width: 30 });
}
// 流程序号：数据或步骤的先后，实心蓝圆
function stepNo(cx, cy, no, color = C.ai) {
  return circle(cx, cy, 13, { fill: color }) + text(cx, cy - 12, no, { color: C.white, weight: 700, mono: true, align: 'center', width: 26 });
}
// 界面注释号：截图或原型上的区域编号，实心墨色圆
function noteNo(cx, cy, no) {
  return circle(cx, cy, 13, { fill: C.ink1 }) + text(cx, cy - 12, no, { color: C.white, weight: 700, mono: true, align: 'center', width: 26 });
}
// 拦截叉：数据或权限停住的位置
function crossMark(cx, cy, size = 18, color = C.ink1) {
  const h = size / 2;
  return line(cx - h, cy - h, cx + h, cy + h, { color, sw: LW.flow }) + line(cx - h, cy + h, cx + h, cy - h, { color, sw: LW.flow });
}
// 尺寸线：时长或跨度。两端短竖线，中间双箭头，标签在线上居中、白底
function dimLine(x1, x2, y, label, o = {}) {
  const color = o.color || C.ink2, w = Math.ceil(tw(label, FS.body, true) + 20);
  return line(x1, y - 12, x1, y + 12, { color }) + line(x2, y - 12, x2, y + 12, { color }) +
    line(x1, y, x2, y, { color, head: 'both' }) +
    `<p style="left:${n((x1 + x2) / 2 - w / 2)}px;top:${n(y - 14)}px;width:${w}px;font-size:${FS.body}px;line-height:28px;text-align:center;font-weight:700;color:${color};background:${o.bg || C.white};white-space:nowrap">${esc(label)}</p>`;
}
// 评审点：时间线上的关口，菱形加竖向虚线
function reviewPoint(cx, y, label, o = {}) {
  let s = diamond(cx, y, 20, 20, { fill: C.ink1 });
  if (o.toY) s += line(cx, y + 10, cx, o.toY, { color: C.ink3, dash: true });
  if (label) s += text(cx, y + 16, label, { align: 'center', color: C.ink1, weight: 600 });
  return s;
}
// 引线：从图上部件指到表格分组，起点画实心点；pts = [[x,y], ...]
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
// 等轴测叠板：分层叠加。x,y 是顶面左角，w 是宽，d 是进深，t 是厚度。导出为图片
function plate(x, y, w, d, o = {}) {
  const top = o.top || C.bg2, side = o.side || C.slate, t = o.t || 14, dx = d * 0.87, dy = d * 0.5;
  const W = w + dx + 4, ox = 2, oy = 2;
  const P = (a, b) => `${n(a + ox)},${n(b + oy)}`;
  const pts = [[0, dy], [dx, 0], [dx + w, 0], [w, dy]];
  const dash = o.dash ? ' stroke-dasharray="6 4"' : '';
  const stroke = o.stroke || side;
  const topPoly = pts.map(q => P(q[0], q[1])).join(' ');
  const front = [P(0, dy), P(w, dy), P(w, dy + t), P(0, dy + t)].join(' ');
  const right = [P(w, dy), P(dx + w, 0), P(dx + w, t), P(w, dy + t)].join(' ');
  const fillSide = o.dash ? 'none' : side;
  return `<svg style="left:${n(x - ox)}px;top:${n(y - oy)}px;width:${n(W)}px;height:${n(dy + t + 4)}px" viewBox="0 0 ${n(W)} ${n(dy + t + 4)}" aria-label="${esc(o.label || '叠板')}">` +
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

// 正文页框架：页眉章名、标题、子标题、提供方胶囊、页脚线、页脚标注、页码
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
  C, FS, LW, RAD, MARGIN, RIGHT, esc, tw, text, para, box, line, arrow, circle, diamond, chip, labelValue, attrBand, legend,
  balloon, stepNo, noteNo, crossMark, dimLine, reviewPoint, leader, bigNumber, plate, frame, page, slide, writeDeck,
};
