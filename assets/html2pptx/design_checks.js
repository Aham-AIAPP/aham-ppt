// 设计检查：用 extract.js 读出的元素位置查版式问题。由 check_slides.js 调用。
// 只查机器能判的部分，结果是 WARNING 或 INFO，由人判断改不改。
// 1 文字越出所在方框  2 文字压在线上  3 文字与底色对比不足  4 箭头没有标签
// 5 方框只写一个名称  6 主图区大块空白或占用率低
const MAIN = { x: 96, y: 195, w: 1728, h: 700 };

const isBox = e => (e.tag === 'div' || e.tag === 'x-shape' || (e.tag === 'p' && !(e.runs || []).length)) && (e.fill || e.border) && e.w >= 40 && e.h >= 30;
const isFilled = e => (e.tag === 'div' || e.tag === 'x-shape' || (e.tag === 'p' && !(e.runs || []).some(r => r.text && r.text.trim()))) && e.fill;
const isText = e => e.tag === 'p' && (e.runs || []).some(r => r.text && r.text.trim());
const textOf = e => (e.runs || []).map(r => r.br ? ' ' : r.text).join('').trim();
const inter = (a, b) => Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x)) * Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));
const inside = (a, b, t = 2) => a.x >= b.x - t && a.y >= b.y - t && a.x + a.w <= b.x + b.w + t && a.y + a.h <= b.y + b.h + t;

// 连线的线段；只设单边边框的细 div 也算线
function segments(e) {
  if (e.tag === 'x-connector') {
    const { x1, y1, x2, y2, route } = e; let P;
    if (route === 'hv') P = [[x1, y1], [x2, y1], [x2, y2]];
    else if (route === 'vh') P = [[x1, y1], [x1, y2], [x2, y2]];
    else if (route === 'elbow') {
      if (Math.abs(x2 - x1) >= Math.abs(y2 - y1)) { const m = (x1 + x2) / 2; P = [[x1, y1], [m, y1], [m, y2], [x2, y2]]; }
      else { const m = (y1 + y2) / 2; P = [[x1, y1], [x1, m], [x2, m], [x2, y2]]; }
    } else P = [[x1, y1], [x2, y2]];
    const s = []; for (let i = 1; i < P.length; i++) s.push([...P[i - 1], ...P[i]]); return s;
  }
  if (e.tag === 'div' && !e.fill && (e.lines || []).some(Boolean) && (e.w <= 6 || e.h <= 6)) {
    return e.w <= 6 ? [[e.x + e.w / 2, e.y, e.x + e.w / 2, e.y + e.h]] : [[e.x, e.y + e.h / 2, e.x + e.w, e.y + e.h / 2]];
  }
  return [];
}
// 线段与矩形相交（矩形四边各缩进 3px，擦边不算）
function segHitsRect(s, r) {
  const R = { x: r.x + 3, y: r.y + 3, w: r.w - 6, h: r.h - 6 }; if (R.w <= 0 || R.h <= 0) return false;
  const [x1, y1, x2, y2] = s;
  if (x1 === x2) return x1 > R.x && x1 < R.x + R.w && Math.max(y1, y2) > R.y && Math.min(y1, y2) < R.y + R.h;
  if (y1 === y2) return y1 > R.y && y1 < R.y + R.h && Math.max(x1, x2) > R.x && Math.min(x1, x2) < R.x + R.w;
  for (let k = 0; k <= 20; k++) { const x = x1 + (x2 - x1) * k / 20, y = y1 + (y2 - y1) * k / 20; if (x > R.x && x < R.x + R.w && y > R.y && y < R.y + R.h) return true; }
  return false;
}
function distSegRect(s, r) {
  let d = Infinity; const [x1, y1, x2, y2] = s;
  for (let k = 0; k <= 20; k++) {
    const x = x1 + (x2 - x1) * k / 20, y = y1 + (y2 - y1) * k / 20;
    const dx = Math.max(r.x - x, 0, x - r.x - r.w), dy = Math.max(r.y - y, 0, y - r.y - r.h);
    d = Math.min(d, Math.hypot(dx, dy));
  }
  return d;
}
function lum(hex) {
  const c = [0, 2, 4].map(i => parseInt(hex.slice(i, i + 2), 16) / 255).map(v => v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
const contrast = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };

// 主图区最大空白矩形（24px 网格，直方图法）
function largestEmpty(rects) {
  const G = 24, cols = Math.floor(MAIN.w / G), rows = Math.floor(MAIN.h / G);
  const occ = Array.from({ length: rows }, () => new Array(cols).fill(false));
  for (const r of rects) {
    const c0 = Math.max(0, Math.floor((r.x - MAIN.x) / G)), c1 = Math.min(cols - 1, Math.floor((r.x + r.w - MAIN.x) / G));
    const r0 = Math.max(0, Math.floor((r.y - MAIN.y) / G)), r1 = Math.min(rows - 1, Math.floor((r.y + r.h - MAIN.y) / G));
    for (let i = r0; i <= r1; i++) for (let j = c0; j <= c1; j++) occ[i][j] = true;
  }
  const hgt = new Array(cols).fill(0); let best = { a: 0 };
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) hgt[j] = occ[i][j] ? 0 : hgt[j] + 1;
    const st = [];
    for (let j = 0; j <= cols; j++) {
      const h = j < cols ? hgt[j] : 0; let s = j;
      while (st.length && st[st.length - 1][1] >= h) {
        const [k, hh] = st.pop(), a = hh * (j - k);
        if (a > best.a) best = { a, x: MAIN.x + k * G, y: MAIN.y + (i - hh + 1) * G, w: (j - k) * G, h: hh * G };
        s = k;
      }
      st.push([s, h]);
    }
  }
  best.ratio = best.a / (rows * cols);
  best.fill = occ.flat().filter(Boolean).length / (rows * cols); return best;
}

module.exports = function designChecks(slide, isBody) {
  const out = [], els = slide.els;
  const texts = els.filter(isText), boxes = els.filter(isBox), segs = els.flatMap(e => segments(e).map(s => ({ s, e })));
  const short = e => textOf(e).slice(0, 16);

  for (const t0 of texts) {
    const t = t0.text || t0, ti = els.indexOf(t0);
    // 1 文字一部分在方框里、一部分在外。压在方框边上的徽标（文字下有自己的实底小圆或小框）不算
    const badge = els.some((b, k) => k < ti && isFilled(b) && b.w < 60 && b.h < 60 && inside(t, b, 4));
    for (const b of badge ? [] : boxes) {
      if (b === t0 || inside(t, b)) continue;
      const a = inter(t, b);
      if (a > t.w * t.h * 0.15 && a < t.w * t.h * 0.98) { out.push(['WARNING', `文字越出方框：${short(t0)}`]); break; }
    }
    // 2 无底色的文字压在线上。浅色网格线不算；线和文字之间有实底方框盖住时不算
    if (!t0.fill && segs.some(({ s, e }) => {
      if (!segHitsRect(s, t)) return false;
      const col = e.color || ((e.lines || []).find(Boolean) || {}).color;
      if (col && contrast(col, slide.bg) < 1.3) return false;
      const li = els.indexOf(e);
      return !els.some((b, k) => k > li && k < ti && isFilled(b) && inside(t, b));
    })) out.push(['WARNING', `文字压在线上：${short(t0)}`]);
    // 3 对比度：底色取文字自身底色，否则取盖住文字中心的最上层方框，否则取页面底色
    let bg = t0.fill;
    if (!bg) {
      const cx = t.x + t.w / 2, cy = t.y + t.h / 2;
      for (let k = ti - 1; k >= 0; k--) { const b = els[k]; if (isFilled(b) && cx > b.x && cx < b.x + b.w && cy > b.y && cy < b.y + b.h) { bg = b.fill; break; } }
    }
    bg = bg || slide.bg;
    const low = (t0.runs || []).filter(r => r.color && r.text && r.text.trim()).map(r => contrast(r.color, bg)).filter(c => c < 2.5);
    if (low.length) out.push(['WARNING', `文字与底色对比不足（${Math.min(...low).toFixed(1)}:1，低于 2.5:1）：${short(t0)}`]);
  }

  // 4 带箭头的连线附近 40px 内没有文字
  for (const c of els.filter(e => e.tag === 'x-connector' && e.head !== 'none')) {
    const ss = segments(c);
    if (!texts.some(t => ss.some(s => distSegRect(s, t.text || t) < 40))) out.push(['INFO', `箭头没有标签（${c.x1},${c.y1} → ${c.x2},${c.y2}）：只表示先后时可以不写`]);
  }

  // 5 方框里只有一个短名称。同尺寸方框排成 3 行 3 列以上的是矩阵格子，不算
  const same = (a, b) => Math.abs(a.w - b.w) < 3 && Math.abs(a.h - b.h) < 3;
  for (const b of boxes) {
    if (b.w < 140 || b.h < 56) continue;
    const peers = boxes.filter(o => same(o, b));
    const rowsN = new Set(peers.map(o => Math.round(o.y))).size, colsN = new Set(peers.map(o => Math.round(o.x))).size;
    if (rowsN >= 3 && colsN >= 3) continue;
    const inT = texts.filter(t => t !== b && inside(t.text || t, b));
    const inOther = els.filter(e => e !== b && !isText(e) && e.tag !== 'x-connector' && inside(e, b, 0) && e.w * e.h < b.w * b.h * 0.9);
    if (inT.length === 1 && !inOther.length && !(inT[0].runs || []).some(r => r.br) && textOf(inT[0]).length <= 10)
      out.push(['INFO', `方框只写一个名称「${textOf(inT[0])}」：补第二项信息或改成列表`]);
  }

  // 6 正文页主图区的大块空白；大底色框当作容器，不算占用
  if (isBody) {
    const occ = els.filter(e => !(isBox(e) && e.w * e.h > MAIN.w * MAIN.h * 0.25) && e.y < MAIN.y + MAIN.h && e.y + e.h > MAIN.y)
      .map(e => e.tag === 'x-connector' ? { x: Math.min(e.x1, e.x2), y: Math.min(e.y1, e.y2), w: Math.abs(e.x2 - e.x1) + 1, h: Math.abs(e.y2 - e.y1) + 1 } : e);
    const g = largestEmpty(occ);
    if (g.ratio > 0.25) out.push(['WARNING', `主图区有大块空白：x ${g.x}–${g.x + g.w}，y ${g.y}–${g.y + g.h}，占主图区 ${Math.round(g.ratio * 100)}%`]);
    else if (g.fill < 0.25) out.push(['INFO', `主图区只用了 ${Math.round(g.fill * 100)}%，与范例库同类页对比密度`]);
  }
  return out;
};
