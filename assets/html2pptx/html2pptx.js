// 把 HTML 幻灯片（1920×1080，绝对定位的 p、div、x-shape、x-connector、svg、img）转成可编辑的 PPTX
// 用法：node html2pptx.js <幻灯片目录> <输出.pptx> [--images 图片映射.json] [--font 字体] [--title 标题] [--author 作者]
//   幻灯片目录下有 deck.json（order 数组给出页序）和 slides/<id>.html；没有 deck.json 时按文件名排序。
//   img 的 src 是本地相对路径时按幻灯片目录解析；其他地址要在图片映射里给出本地文件。
// 换算：1920px 对应 13.333 英寸，1px = 1/144 英寸 = 0.5 磅；文字、形状、线条均可编辑，图标、内嵌 svg 和图片为图片
// 写法规则见 references/html-slides.md
const fs = require('fs'), path = require('path');
const PptxGenJS = require('pptxgenjs');
const { chromium } = require('playwright');

const argv = process.argv.slice(2);
const opt = k => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : undefined; };
const [DECK, OUT] = argv.filter((a, i) => !a.startsWith('--') && !(i > 0 && argv[i - 1].startsWith('--')));
if (!DECK || !OUT) { console.error('用法：node html2pptx.js <幻灯片目录> <输出.pptx> [--images map.json] [--font 字体] [--title 标题] [--author 作者]'); process.exit(2); }
const FONT = opt('font') || 'Microsoft YaHei';
const SLIDES = fs.existsSync(path.join(DECK, 'slides')) ? path.join(DECK, 'slides') : DECK;
const deckJson = path.join(DECK, 'deck.json');
const order = fs.existsSync(deckJson) ? JSON.parse(fs.readFileSync(deckJson, 'utf8')).order
  : fs.readdirSync(SLIDES).filter(f => f.endsWith('.html')).sort().map(f => f.slice(0, -5));
const imgMap = opt('images') ? JSON.parse(fs.readFileSync(opt('images'), 'utf8')) : {};
const IN = px => px / 144, PT = px => px / 2;

function style(s) {
  const o = {};
  (s || '').split(';').forEach(d => { const i = d.indexOf(':'); if (i > 0) o[d.slice(0, i).trim().toLowerCase()] = d.slice(i + 1).trim(); });
  return o;
}
const num = v => (v === undefined ? undefined : parseFloat(v));
function color(v) {
  if (!v) return null; v = v.trim().toLowerCase();
  if (v === 'transparent' || v === 'none') return null;
  let m = /^#([0-9a-f]{6})$/.exec(v); if (m) return m[1].toUpperCase();
  m = /^#([0-9a-f]{3})$/.exec(v); if (m) return m[1].split('').map(c => c + c).join('').toUpperCase();
  m = /^rgba?\(([^)]*)\)$/.exec(v); if (m) { const p = m[1].split(',').map(x => parseFloat(x)); return p.slice(0, 3).map(x => Math.round(x).toString(16).padStart(2, '0')).join('').toUpperCase(); }
  throw new Error('color ' + v);
}
function border(v) {
  if (!v) return null; const m = /([\d.]+)px\s+(solid|dashed|dotted)\s+(\S+)/.exec(v); if (!m) return null;
  return { w: parseFloat(m[1]), dash: m[2] !== 'solid', color: color(m[3]) };
}
function lineOpt(b) { return { color: b.color, width: PT(b.w), dashType: b.dash ? 'dash' : 'solid' }; }
const ent = s => s.replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
  .replace(/&#(\d+);/g, (m, d) => String.fromCodePoint(+d)).replace(/&#x([0-9a-f]+);/gi, (m, h) => String.fromCodePoint(parseInt(h, 16))).replace(/&amp;/g, '&');

// 段内文字：<br> 分行，<span style="color"> 和 <b> 为局部格式
function runs(inner, base) {
  const out = []; const stack = [{ color: base.color, bold: base.bold }];
  const re = /<br\s*\/?>|<span\b([^>]*)>|<\/span>|<b>|<\/b>|<strong>|<\/strong>|([^<]+)/g; let m;
  while ((m = re.exec(inner))) {
    const tok = m[0], cur = stack[stack.length - 1];
    if (/^<br/.test(tok)) { if (out.length) out[out.length - 1].options.breakLine = true; else out.push({ text: '', options: { breakLine: true } }); }
    else if (/^<span/.test(tok)) { const st = style((/style="([^"]*)"/.exec(m[1] || '') || [])[1]); stack.push({ ...cur, color: color(st.color) || cur.color, bold: st['font-weight'] ? +st['font-weight'] >= 600 : cur.bold }); }
    else if (tok === '<b>' || tok === '<strong>') stack.push({ ...cur, bold: true });
    else if (tok === '</span>' || tok === '</b>' || tok === '</strong>') { if (stack.length > 1) stack.pop(); }
    else { const t = ent(m[2]); if (t) out.push({ text: t, options: { color: cur.color, bold: !!cur.bold } }); }
  }
  // 末尾的换行标记去掉，避免多出空行
  if (out.length && out[out.length - 1].options.breakLine && out[out.length - 1].text !== '') delete out[out.length - 1].options.breakLine;
  return out;
}

function parseSlide(html) {
  const notesM = /<aside>([\s\S]*?)<\/aside>/.exec(html);
  const notes = notesM ? ent(notesM[1].replace(/<[^>]+>/g, '')).trim() : '';
  const body = html.replace(/<aside>[\s\S]*?<\/aside>/, '');
  const sec = /<section\b[^>]*style="([^"]*)"/.exec(body);
  const els = [];
  const re = /<(p|div|x-shape|x-connector|svg|img)\b([^>]*)>/g; let m;
  while ((m = re.exec(body))) {
    const tag = m[1], attrs = m[2]; let inner = '';
    if (tag !== 'img') {
      const close = '</' + tag + '>'; const j = body.indexOf(close, re.lastIndex);
      if (j < 0) throw new Error('unclosed ' + tag);
      inner = body.slice(re.lastIndex, j); re.lastIndex = j + close.length;
    }
    els.push({ tag, attrs, inner, st: style((/style="([^"]*)"/.exec(attrs) || [])[1]) });
  }
  return { bg: color(style(sec && sec[1]).background) || 'FFFFFF', els, notes };
}
const attr = (a, k) => { const m = new RegExp('\\b' + k + '="([^"]*)"').exec(a); return m ? m[1] : undefined; };

async function iconPngs(slides) {
  const uniq = new Map();
  slides.forEach(s => s.els.forEach(e => { if (e.tag === 'svg') { const key = '<svg' + e.attrs.replace(/\sstyle="[^"]*"/, '') + '>' + e.inner + '</svg>'; e.key = key; uniq.set(key, null); } }));
  const br = await chromium.launch(); const pg = await br.newPage({ deviceScaleFactor: 4 });
  for (const key of uniq.keys()) {
    await pg.setContent(`<html><body style="margin:0;background:transparent">${key.replace('<svg', '<svg id="ic"')}</body></html>`);
    uniq.set(key, await pg.locator('#ic').screenshot({ omitBackground: true }));
  }
  await br.close(); return uniq;
}

(async () => {
  const slides = order.map(id => ({ id, ...parseSlide(fs.readFileSync(path.join(SLIDES, id + '.html'), 'utf8')) }));
  const icons = await iconPngs(slides);
  const pres = new PptxGenJS(); pres.layout = 'LAYOUT_WIDE';
  if (opt('title')) pres.title = opt('title'); if (opt('author')) { pres.author = opt('author'); pres.company = opt('author'); }
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  const stat = { text: 0, shape: 0, line: 0, icon: 0, image: 0 };
  for (const s of slides) {
    const sl = pres.addSlide(); sl.background = { color: s.bg };
    let n = 0; const name = k => `${s.id}-${k}-${++n}`;
    for (const e of s.els) {
      const st = e.st, x = num(st.left) || 0, y = num(st.top) || 0;
      if (e.tag === 'img') {
        const src = attr(e.attrs, 'src'); const local = path.resolve(DECK, src || '');
        const file = imgMap[src] || (src && !/^[a-z]+:|^\//i.test(src) && fs.existsSync(local) ? local : null);
        if (!file && !/^data:/.test(src || '')) throw new Error('图片没有本地文件：' + src);
        const w = num(st.width), h = num(st.height);
        sl.addImage({ ...(file ? { path: file } : { data: src.replace(/^data:/, '') }), x: IN(x), y: IN(y), w: IN(w), h: IN(h), sizing: { type: 'cover', w: IN(w), h: IN(h) }, altText: attr(e.attrs, 'alt') || '', objectName: name('img') });
        stat.image++; continue;
      }
      if (e.tag === 'svg') {
        const w = num(st.width) || num(attr(e.attrs, 'width')), h = num(st.height) || num(attr(e.attrs, 'height'));
        sl.addImage({ data: 'image/png;base64,' + icons.get(e.key).toString('base64'), x: IN(x), y: IN(y), w: IN(w), h: IN(h), altText: attr(e.attrs, 'aria-label') || '图标', objectName: name('icon') });
        stat.icon++; continue;
      }
      if (e.tag === 'x-connector') {
        const x1 = +attr(e.attrs, 'x1'), y1 = +attr(e.attrs, 'y1'), x2 = +attr(e.attrs, 'x2'), y2 = +attr(e.attrs, 'y2');
        const head = attr(e.attrs, 'head') || 'none', route = attr(e.attrs, 'route');
        const lo = { color: color(st.color) || '000000', width: PT(num(st['border-width']) || 2), dashType: st['border-style'] === 'dashed' ? 'dash' : 'solid' };
        const seg = (a, b, c, d, arrow) => {
          const o = { x: IN(Math.min(a, c)), y: IN(Math.min(b, d)), w: IN(Math.abs(c - a)), h: IN(Math.abs(d - b)), flipH: c < a, flipV: d < b, line: { ...lo }, objectName: name('line') };
          if (arrow === 'end' || arrow === 'both') o.line.endArrowType = 'triangle';
          if (arrow === 'start' || arrow === 'both') o.line.beginArrowType = 'triangle';
          sl.addShape(pres.ShapeType.line, o); stat.line++;
        };
        if (route === 'hv') { seg(x1, y1, x2, y1, head === 'start' || head === 'both' ? 'start' : 'none'); seg(x2, y1, x2, y2, head === 'end' || head === 'both' ? 'end' : 'none'); }
        else if (route === 'vh') { seg(x1, y1, x1, y2, head === 'start' || head === 'both' ? 'start' : 'none'); seg(x1, y2, x2, y2, head === 'end' || head === 'both' ? 'end' : 'none'); }
        else if (route === 'elbow') {
          const hs = head === 'start' || head === 'both' ? 'start' : 'none', he = head === 'end' || head === 'both' ? 'end' : 'none';
          if (Math.abs(x2 - x1) >= Math.abs(y2 - y1)) { const mx = (x1 + x2) / 2; seg(x1, y1, mx, y1, hs); seg(mx, y1, mx, y2, 'none'); seg(mx, y2, x2, y2, he); }
          else { const my = (y1 + y2) / 2; seg(x1, y1, x1, my, hs); seg(x1, my, x2, my, 'none'); seg(x2, my, x2, y2, he); }
        }
        else if (route) throw new Error('route ' + route);
        else seg(x1, y1, x2, y2, head);
        continue;
      }
      const w = num(st.width) || 0, h = num(st.height) || 0;
      const fill = color(st.background || st['background-color']);
      const bd = border(st.border);
      const rad = num(st['border-radius']) || 0;
      const shapeOpts = () => {
        const o = { x: IN(x), y: IN(y), w: IN(w), h: IN(h) };
        o.fill = fill ? { color: fill } : { type: 'none' };
        o.line = bd ? lineOpt(bd) : { type: 'none' };
        if (rad > 0) o.rectRadius = IN(Math.min(rad, Math.min(w, h) / 2));
        return o;
      };
      if (e.tag === 'x-shape') {
        const kind = attr(e.attrs, 'kind');
        const t = { ellipse: pres.ShapeType.ellipse, diamond: pres.ShapeType.diamond, rect: pres.ShapeType.rect, rounded: pres.ShapeType.roundRect }[kind];
        if (!t) throw new Error('kind ' + kind);
        const o = shapeOpts(); delete o.rectRadius; o.objectName = name(kind);
        sl.addShape(t, o); stat.shape++; continue;
      }
      if (e.tag === 'div') {
        if (e.inner.replace(/\s/g, '')) throw new Error('div with content in ' + s.id);
        const bl = border(st['border-left']), bt = border(st['border-top']);
        if (fill || bd) { const o = shapeOpts(); o.objectName = name('rect'); sl.addShape(rad > 0 ? pres.ShapeType.roundRect : pres.ShapeType.rect, o); stat.shape++; }
        // 只有左边框或上边框的 div 是虚线：画成线条
        if (bt) { const yy = y + bt.w / 2; sl.addShape(pres.ShapeType.line, { x: IN(x), y: IN(yy), w: IN(w), h: 0, line: lineOpt(bt), objectName: name('line') }); stat.line++; }
        if (bl) { const xx = x + bl.w / 2; sl.addShape(pres.ShapeType.line, { x: IN(xx), y: IN(y), w: 0, h: IN(h), line: lineOpt(bl), objectName: name('line') }); stat.line++; }
        continue;
      }
      // p：文字框；有底色或边框时是带文字的形状
      const fs_ = num(st['font-size']) || 18;
      const lhv = st['line-height'] || '1.2'; const lh = /px$/.test(lhv) ? parseFloat(lhv) : parseFloat(lhv) * fs_;
      const bold = st['font-weight'] ? +st['font-weight'] >= 600 || st['font-weight'] === 'bold' : false;
      const base = { color: color(st.color) || '1F2633', bold };
      const rs = runs(e.inner.replace(/\s*\n\s*/g, ''), base); if (!rs.length) continue;
      const lines = (e.inner.match(/<br\s*\/?>/g) || []).length + 1;
      const pad = (st.padding || '0').split(/\s+/).map(v => parseFloat(v) || 0);
      const [pt_, pr_, pb_, pl_] = pad.length === 1 ? [pad[0], pad[0], pad[0], pad[0]] : pad.length === 2 ? [pad[0], pad[1], pad[0], pad[1]] : pad.length === 3 ? [pad[0], pad[1], pad[2], pad[1]] : pad;
      const bw = bd ? bd.w : 0;
      const hh = h || lines * lh + pt_ + pb_ + 2 * bw;
      const single = lines === 1 && h && Math.abs(lh - (h - 2 * bw - pt_ - pb_)) < 3;
      const o = {
        x: IN(x), y: IN(y), w: IN(w), h: IN(hh),
        fontFace: /monospace/.test(st['font-family'] || '') ? 'Consolas' : FONT, fontSize: PT(fs_),
        align: { center: 'center', right: 'right' }[st['text-align']] || 'left',
        valign: single ? 'middle' : 'top', lineSpacing: PT(lh),
        margin: [PT(pl_ + bw), PT(pr_ + bw), PT(pb_ + bw), PT(pt_ + bw)],
        wrap: st['white-space'] !== 'nowrap', fit: 'none', objectName: name('text'),
      };
      if (single) delete o.lineSpacing;
      if (fill || bd) {
        o.fill = fill ? { color: fill } : { type: 'none' }; o.line = bd ? lineOpt(bd) : { type: 'none' };
        o.shape = rad > 0 ? pres.ShapeType.roundRect : pres.ShapeType.rect;
        if (rad > 0) o.rectRadius = IN(Math.min(rad, Math.min(w, hh) / 2));
      }
      sl.addText(rs, o); stat.text++;
    }
    if (s.notes) sl.addNotes(s.notes);
  }
  await pres.writeFile({ fileName: OUT });
  console.log(OUT, slides.length, 'slides', JSON.stringify(stat), 'icons unique', icons.size);
})().catch(e => { console.error(e); process.exit(1); });
