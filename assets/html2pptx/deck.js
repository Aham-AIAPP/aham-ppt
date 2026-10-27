// 读幻灯片目录、合成网页。preview.js、check_slides.js、html2pptx.js 共用，保证三者看到的是同一份排版。
const fs = require('fs'), path = require('path');

// 预览与导出用同一字体栈。导出时 PPT 里写第一项；网页按顺序找本机已装的字体。
const FONT_STACK = "'Microsoft YaHei','PingFang SC','Noto Sans SC',sans-serif";

function loadDeck(dir) {
  const slidesDir = fs.existsSync(path.join(dir, 'slides')) ? path.join(dir, 'slides') : dir;
  const deckJson = path.join(dir, 'deck.json');
  const order = fs.existsSync(deckJson) ? JSON.parse(fs.readFileSync(deckJson, 'utf8')).order
    : fs.readdirSync(slidesDir).filter(f => f.endsWith('.html')).sort().map(f => f.slice(0, -5));
  return order.map(id => {
    const file = path.join(slidesDir, id + '.html');
    if (!fs.existsSync(file)) throw new Error(`deck.json 里的 ${id} 没有对应文件 ${file}`);
    return { id, html: fs.readFileSync(file, 'utf8') };
  });
}

// 本地图片转成 data URI，网页才能单文件打开
function inlineImages(html, dir) {
  return html.replace(/<img\b([^>]*?)\bsrc="([^"]+)"/g, (m, pre, src) => {
    if (/^(data:|https?:|\/)/.test(src)) return m;
    const f = path.resolve(dir, src); if (!fs.existsSync(f)) return m;
    const ext = path.extname(f).slice(1).toLowerCase().replace('jpg', 'jpeg');
    return `<img${pre}src="data:image/${ext === 'svg' ? 'svg+xml' : ext};base64,${fs.readFileSync(f).toString('base64')}"`;
  });
}

// 每页包进 figure；section 加 class 和 data-id
function slideBlocks(slides, dir) {
  return slides.map((s, i) => {
    const h = inlineImages(s.html, dir).replace(/<!--[\s\S]*?-->/g, '').replace(/<section\b/, `<section class="slide" data-id="${s.id}"`);
    return `<figure class="pg"><div class="box"><div class="scale">${h}</div></div><figcaption>${String(i + 1).padStart(2, '0')}　${s.id}</figcaption></figure>`;
  }).join('\n');
}

function buildPage(slides, dir, title) {
  const runtime = fs.readFileSync(path.join(__dirname, 'runtime.js'), 'utf8');
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap">
<style>
:root{--bg:#EEF1F5;--fg:#1F2633;--muted:#7D8695}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#14181F;--fg:#E6E9EE;--muted:#9AA6B8}}
:root[data-theme="dark"]{--bg:#14181F;--fg:#E6E9EE;--muted:#9AA6B8}
body{margin:0;background:var(--bg);color:var(--fg);font-family:${FONT_STACK}}
section.slide{font-family:${FONT_STACK}}
main{max-width:1280px;margin:0 auto;padding:24px 16px 48px;display:grid;gap:24px}
h1{font-size:20px;margin:0}
.pg{margin:0}.box{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;background:#fff;border-radius:6px;box-shadow:0 0 0 1px rgba(0,0,0,.08)}
.scale{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0}
figcaption{font-size:13px;color:var(--muted);padding-top:6px;font-family:Consolas,monospace}
body.raw main{max-width:none;padding:0;gap:0;display:block}body.raw .box{width:1920px;height:1080px;aspect-ratio:auto;border-radius:0;box-shadow:none}
body.raw figcaption,body.raw h1{display:none}
</style><script>${runtime}</script></head>
<body><main><h1>${title}</h1>
${slideBlocks(slides, dir)}
</main>
<script>
if (new URLSearchParams(location.search).get('raw')) document.body.classList.add('raw');
function fit(){ if (document.body.classList.contains('raw')) return;
  document.querySelectorAll('.box').forEach(b => { b.querySelector('.scale').style.transform = 'scale(' + (b.clientWidth / 1920) + ')'; }); }
addEventListener('resize', fit); fit();
</script></body></html>`;
}

module.exports = { FONT_STACK, loadDeck, buildPage };
