// 排版检查：在浏览器里实际排版后，查文字溢出、文字互相重叠、超出画布和字号过小；
// 再按 design_checks.js 查文字越框、压线、对比度、箭头标签、单名称方框和大块空白
// 用法：node check_slides.js <幻灯片目录或预览.html> [--png 截图目录] [--sheet 缩略图总览.png] [--min-font 18]
// --sheet 把全册缩略图排成一张图，用来看相邻页的主图结构有没有重复
// 输出 Markdown 报告；有 ERROR 时退出码为 1
const path = require('path'), fs = require('fs');
const { chromium } = require('playwright');
const argv = process.argv.slice(2);
const opt = k => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : undefined; };
const FILE = argv.find((a, i) => !a.startsWith('--') && !(i > 0 && argv[i - 1].startsWith('--')));
const MIN = +(opt('min-font') || 18), PNG = opt('png'), SHEET = opt('sheet');

(async () => {
  const br = await chromium.launch();
  const pg = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  let file = path.resolve(FILE), tmp;
  if (fs.statSync(file).isDirectory()) {
    const { loadDeck, buildPage } = require('./deck');
    tmp = path.join(require('os').tmpdir(), `chk-${process.pid}.html`);
    fs.writeFileSync(tmp, buildPage(loadDeck(file), file, 'check')); file = tmp;
  }
  await pg.goto('file://' + file + '?raw=1');
  if (tmp) fs.unlinkSync(tmp);
  await pg.evaluate(() => document.fonts.ready);
  await pg.addScriptTag({ path: path.join(__dirname, 'extract.js') });
  const data = await pg.evaluate(() => window.extractSlides());
  const designChecks = require('./design_checks');
  const compat = data.map(s => [...s.issues, ...designChecks(s, s.els.some(e => e.tag === 'p' && e.fs === 52))]);
  const res = await pg.evaluate(MIN => {
    const out = [];
    document.querySelectorAll('section.slide').forEach((s, i) => {
      const id = s.dataset.id, no = i + 1, sr = s.getBoundingClientRect(), issues = [];
      const ps = [...s.querySelectorAll(':scope > p')];
      const boxes = ps.map(p => {
        const r = p.getBoundingClientRect(), cs = getComputedStyle(p), fs = parseFloat(cs.fontSize);
        const t = p.textContent.trim().slice(0, 16);
        if (fs < MIN) issues.push(['ERROR', `字号 ${fs}px 小于 ${MIN}px：${t}`]);
        if (p.scrollWidth > p.clientWidth + 2) issues.push(['ERROR', `文字横向溢出 ${p.scrollWidth - p.clientWidth}px：${t}`]);
        if (p.style.height && p.scrollHeight > p.clientHeight + 2) issues.push(['ERROR', `文字纵向溢出 ${p.scrollHeight - p.clientHeight}px：${t}`]);
        if (r.right > sr.right + 1 || r.bottom > sr.bottom + 1 || r.left < sr.left - 1 || r.top < sr.top - 1) issues.push(['ERROR', `超出画布：${t}`]);
        // 会自动换行的段落，文字已占满宽度时，PPT 里字体略宽就会多出一行
        if (cs.whiteSpace !== 'nowrap' && p.style.width) {
          const rg0 = document.createRange(); rg0.selectNodeContents(p);
          const lines = [...rg0.getClientRects()].reduce((a, q) => { if (!a.some(y => Math.abs(y - q.top) < fs / 2)) a.push(q.top); return a; }, []);
          const inner = p.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
          const widest = Math.max(0, ...[...rg0.getClientRects()].map(q => q.width));
          if (lines.length === 1 && widest > inner * 0.95) issues.push(['WARNING', `单行文字占满宽度，PPT 里可能折行（加宽方框或写 white-space:nowrap）：${t}`]);
        }
        // 实际文字范围：用 Range 量，避免把空白宽度算进重叠
        const rg = document.createRange(); rg.selectNodeContents(p); const tr = rg.getBoundingClientRect();
        return { t, r: tr.width ? tr : r };
      });
      for (let a = 0; a < boxes.length; a++) for (let b = a + 1; b < boxes.length; b++) {
        const A = boxes[a].r, B = boxes[b].r;
        const w = Math.min(A.right, B.right) - Math.max(A.left, B.left), h = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top);
        if (w > 2 && h > 2) issues.push(['WARNING', `文字重叠：「${boxes[a].t}」与「${boxes[b].t}」`]);
      }
      for (const sv of s.querySelectorAll(':scope > svg, :scope > img')) {
        const q = sv.getBoundingClientRect();
        if (q.right > sr.right + 1 || q.bottom > sr.bottom + 1 || q.left < sr.left - 1 || q.top < sr.top - 1) issues.push(['ERROR', `${sv.localName} 超出画布`]);
      }
      out.push({ no, id, issues });
    });
    return out;
  }, MIN);
  if (PNG || SHEET) {
    if (PNG) fs.mkdirSync(PNG, { recursive: true });
    const secs = await pg.$$('section.slide'), shots = [];
    for (let i = 0; i < secs.length; i++) {
      const buf = await secs[i].screenshot(PNG ? { path: path.join(PNG, `${String(i + 1).padStart(2, '0')}.png`) } : {});
      shots.push(buf.toString('base64'));
    }
    if (SHEET) {
      // 每行 5 张，每张 384×216，下方写页码
      const cols = 5, w = 384, h = 216, rows = Math.ceil(shots.length / cols);
      const sp = await br.newPage({ viewport: { width: cols * (w + 16) + 16, height: rows * (h + 40) + 16 } });
      await sp.setContent(`<body style="margin:0;padding:8px;background:#EEF1F5;font:14px monospace">${shots.map((b, i) =>
        `<div style="display:inline-block;margin:8px;vertical-align:top"><img src="data:image/png;base64,${b}" style="width:${w}px;height:${h}px;display:block;box-shadow:0 0 0 1px #C9CED6"><div style="color:#4A5363;padding-top:4px">${String(i + 1).padStart(2, '0')}</div></div>`).join('')}</body>`);
      await sp.screenshot({ path: SHEET, fullPage: true });
    }
  }
  await br.close();
  const cnt = { ERROR: 0, WARNING: 0, INFO: 0 }, lines = ['# 排版检查', ''];
  res.forEach((s, i) => s.issues.push(...compat[i]));
  for (const lv of ['ERROR', 'WARNING', 'INFO'])
    res.forEach(s => s.issues.filter(x => x[0] === lv).forEach(([, m]) => { cnt[lv]++; lines.push(`- 第 ${s.no} 页（${s.id}）${lv}　${m}`); }));
  lines.splice(1, 0, `ERROR ${cnt.ERROR} 条　WARNING ${cnt.WARNING} 条　INFO ${cnt.INFO} 条　共 ${res.length} 页`);
  const e = cnt.ERROR;
  console.log(lines.join('\n'));
  process.exit(e ? 1 : 0);
})().catch(err => { console.error(err); process.exit(2); });
