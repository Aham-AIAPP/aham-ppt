// 把 HTML 幻灯片（1920×1080，绝对定位的 p、div、x-shape、x-connector、svg、img）转成可编辑的 PPTX
// 用法：node html2pptx.js <幻灯片目录> <输出.pptx> [--images 图片映射.json] [--font 字体] [--title 标题] [--author 作者]
//   幻灯片目录下有 deck.json（order 数组给出页序）和 slides/<id>.html；没有 deck.json 时按文件名排序。
//   本地图片按幻灯片目录解析；网络图片要在图片映射里给出本地文件。
// 做法：先在浏览器里按预览页同样的方式排版，再读出每个元素的实际位置和样式写进 PPT，网页和 PPT 用同一套数值。
// 换算：1px = 1/144 英寸 = 0.5 磅；文字、形状、线条可编辑，svg 和图片为图片。写法规则见 references/html-slides.md
const fs = require('fs'), path = require('path'), os = require('os');
const PptxGenJS = require('pptxgenjs');
const { chromium } = require('playwright');
const { loadDeck, buildPage } = require('./deck');

const argv = process.argv.slice(2);
const opt = k => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : undefined; };
const [DECK, OUT] = argv.filter((a, i) => !a.startsWith('--') && !(i > 0 && argv[i - 1].startsWith('--')));
if (!DECK || !OUT) { console.error('用法：node html2pptx.js <幻灯片目录> <输出.pptx> [--images map.json] [--font 字体] [--title 标题] [--author 作者]'); process.exit(2); }
const FONT = opt('font') || 'Microsoft YaHei';
const imgMap = opt('images') ? JSON.parse(fs.readFileSync(opt('images'), 'utf8')) : {};
const IN = v => v / 144, PT = v => v / 2;

// 连线的折点，与 runtime.js 一致；去掉长度为 0 的段
function points(c) {
  const { x1, y1, x2, y2, route } = c; let P;
  if (route === 'hv') P = [[x1, y1], [x2, y1], [x2, y2]];
  else if (route === 'vh') P = [[x1, y1], [x1, y2], [x2, y2]];
  else if (route === 'elbow') {
    if (Math.abs(x2 - x1) >= Math.abs(y2 - y1)) { const m = (x1 + x2) / 2; P = [[x1, y1], [m, y1], [m, y2], [x2, y2]]; }
    else { const m = (y1 + y2) / 2; P = [[x1, y1], [x1, m], [x2, m], [x2, y2]]; }
  } else if (!route) P = [[x1, y1], [x2, y2]];
  else throw new Error('route ' + route);
  return P.filter((p, i) => i === 0 || p[0] !== P[i - 1][0] || p[1] !== P[i - 1][1]);
}

async function render(slides) {
  const tmp = path.join(os.tmpdir(), `h2p-${process.pid}.html`);
  fs.writeFileSync(tmp, buildPage(slides, DECK, 'export'));
  const br = await chromium.launch();
  const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  await pg.goto('file://' + tmp + '?raw=1');
  await pg.evaluate(() => document.fonts.ready);
  await pg.addScriptTag({ path: path.join(__dirname, 'extract.js') });
  const data = await pg.evaluate(() => window.extractSlides());
  // svg 单独渲染成 4 倍图
  const icons = new Map(), ip = await br.newPage({ deviceScaleFactor: 4 });
  for (const s of data) for (const e of s.els) if (e.tag === 'svg' && !icons.has(e.svg)) {
    await ip.setContent(`<html><body style="margin:0;background:transparent">${e.svg.replace('<svg', '<svg id="ic"')}</body></html>`);
    icons.set(e.svg, await ip.locator('#ic').screenshot({ omitBackground: true }));
  }
  await br.close(); fs.unlinkSync(tmp);
  return { data, icons };
}

(async () => {
  const slides = loadDeck(DECK);
  const { data, icons } = await render(slides);
  const pres = new PptxGenJS(); pres.layout = 'LAYOUT_WIDE';
  if (opt('title')) pres.title = opt('title'); if (opt('author')) { pres.author = opt('author'); pres.company = opt('author'); }
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  const stat = { text: 0, shape: 0, line: 0, icon: 0, image: 0 }, warn = [];
  for (const s of data) {
    s.issues.filter(i => i[0] === 'ERROR').forEach(i => warn.push(`${s.id}：${i[1]}`));
    const sl = pres.addSlide(); sl.background = { color: s.bg };
    let n = 0; const name = k => `${s.id}-${k}-${++n}`;
    const lineOpt = b => ({ color: b.color, width: PT(b.w), dashType: b.dash ? 'dash' : 'solid' });
    const seg = (a, b, c, d, lo, begin, end) => {
      const o = { x: IN(Math.min(a, c)), y: IN(Math.min(b, d)), w: IN(Math.abs(c - a)), h: IN(Math.abs(d - b)), flipH: c < a, flipV: d < b, line: { ...lo }, objectName: name('line') };
      if (begin) o.line.beginArrowType = 'triangle'; if (end) o.line.endArrowType = 'triangle';
      sl.addShape(pres.ShapeType.line, o); stat.line++;
    };
    // 不统一的边框画成各边的线
    const sideLines = e => e.lines.forEach((b, i) => {
      if (!b) return; const h = b.w / 2;
      if (i === 0) seg(e.x, e.y + h, e.x + e.w, e.y + h, lineOpt(b));
      if (i === 1) seg(e.x + e.w - h, e.y, e.x + e.w - h, e.y + e.h, lineOpt(b));
      if (i === 2) seg(e.x, e.y + e.h - h, e.x + e.w, e.y + e.h - h, lineOpt(b));
      if (i === 3) seg(e.x + h, e.y, e.x + h, e.y + e.h, lineOpt(b));
    });
    const shapeType = e => (e.rad >= Math.min(e.w, e.h) / 2 - 0.5 && Math.abs(e.w - e.h) < 1) ? pres.ShapeType.ellipse : e.rad > 0 ? pres.ShapeType.roundRect : pres.ShapeType.rect;
    const geo = e => {
      const o = { x: IN(e.x), y: IN(e.y), w: IN(e.w), h: IN(e.h), fill: e.fill ? { color: e.fill } : { type: 'none' }, line: e.border ? lineOpt(e.border) : { type: 'none' } };
      if (e.rad > 0) o.rectRadius = IN(Math.min(e.rad, Math.min(e.w, e.h) / 2));
      return o;
    };
    for (const e of s.els) {
      if (e.tag === 'img') {
        const src = e.src || ''; let file = imgMap[src];
        if (!file && !/^[a-z]+:|^\//i.test(src) && fs.existsSync(path.resolve(DECK, src))) file = path.resolve(DECK, src);
        if (!file && !/^data:/.test(src)) throw new Error(`${s.id}：图片没有本地文件 ${src}`);
        sl.addImage({ ...(file ? { path: file } : { data: src.replace(/^data:/, '') }), x: IN(e.x), y: IN(e.y), w: IN(e.w), h: IN(e.h), sizing: { type: 'cover', w: IN(e.w), h: IN(e.h) }, altText: e.alt, objectName: name('img') });
        stat.image++; continue;
      }
      if (e.tag === 'svg') {
        sl.addImage({ data: 'image/png;base64,' + icons.get(e.svg).toString('base64'), x: IN(e.x), y: IN(e.y), w: IN(e.w), h: IN(e.h), altText: e.alt || '图标', objectName: name('icon') });
        stat.icon++; continue;
      }
      if (e.tag === 'x-connector') {
        const P = points(e), lo = { color: e.color, width: PT(e.w), dashType: e.dash ? 'dash' : 'solid' };
        const hs = e.head === 'start' || e.head === 'both', he = e.head === 'end' || e.head === 'both';
        for (let i = 1; i < P.length; i++) seg(P[i - 1][0], P[i - 1][1], P[i][0], P[i][1], lo, hs && i === 1, he && i === P.length - 1);
        continue;
      }
      if (e.tag === 'x-shape') {
        const t = { ellipse: pres.ShapeType.ellipse, diamond: pres.ShapeType.diamond, rect: pres.ShapeType.rect, rounded: pres.ShapeType.roundRect }[e.kind];
        if (!t) throw new Error(`${s.id}：x-shape kind=${e.kind}`);
        const o = geo(e); delete o.rectRadius; o.objectName = name(e.kind);
        sl.addShape(t, o); stat.shape++; sideLines(e); continue;
      }
      if (e.tag === 'div') {
        if (e.fill || e.border) { const o = geo(e); o.objectName = name('rect'); sl.addShape(shapeType(e), o); stat.shape++; }
        sideLines(e); continue;
      }
      // p：文字框；有底色或边框时是带文字的形状
      if (!e.runs.length) { if (e.fill || e.border) { const o = geo(e); o.objectName = name('rect'); sl.addShape(shapeType(e), o); stat.shape++; } continue; }
      const rs = [];
      e.runs.forEach(r => {
        if (r.br) { if (rs.length && !rs[rs.length - 1].options.breakLine) rs[rs.length - 1].options.breakLine = true; else rs.push({ text: '', options: { breakLine: true } }); return; }
        rs.push({ text: r.text, options: { color: r.color || '1F2633', bold: r.bold, italic: r.italic } });
      });
      const [pt, pr, pb, pl] = e.pad, [bt, brr, bb, bl] = e.bw;
      const inner = e.h - pt - pb - bt - bb, single = Math.abs(inner - e.lh) < 3;
      const o = {
        x: IN(e.x), y: IN(e.y), w: IN(e.w), h: IN(e.h),
        fontFace: e.mono ? 'Consolas' : FONT, fontSize: PT(e.fs), align: e.align,
        valign: single ? 'middle' : 'top', margin: [PT(pl + bl), PT(pr + brr), PT(pb + bb), PT(pt + bt)],
        wrap: !e.nowrap, fit: 'none', objectName: name('text'),
      };
      if (!single) o.lineSpacing = PT(e.lh);
      if (e.fill || e.border) {
        o.fill = e.fill ? { color: e.fill } : { type: 'none' }; o.line = e.border ? lineOpt(e.border) : { type: 'none' };
        o.shape = shapeType(e); if (e.rad > 0) o.rectRadius = IN(Math.min(e.rad, Math.min(e.w, e.h) / 2));
      }
      sl.addText(rs, o); stat.text++; sideLines(e);
    }
    if (s.notes) sl.addNotes(s.notes);
  }
  await pres.writeFile({ fileName: OUT });
  console.log(OUT, data.length, 'slides', JSON.stringify(stat), 'icons unique', icons.size);
  if (warn.length) { console.error('导出时丢失的效果（先运行 check_slides.js 改掉）：\n' + warn.join('\n')); }
})().catch(e => { console.error(e.message || e); process.exit(1); });
