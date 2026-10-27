// 把幻灯片目录合成一个自包含的预览页（可本地打开，也可发布为 Artifact）
// 用法：node preview.js <幻灯片目录> <输出.html> [--title 标题]
// 每页按窗口宽度缩放；?raw=1 时不缩放（排版检查用）
const fs = require('fs'), path = require('path');
const argv = process.argv.slice(2);
const opt = k => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : undefined; };
const [DECK, OUT] = argv.filter((a, i) => !a.startsWith('--') && !(i > 0 && argv[i - 1].startsWith('--')));
if (!DECK || !OUT) { console.error('用法：node preview.js <幻灯片目录> <输出.html> [--title 标题]'); process.exit(2); }
const SLIDES = fs.existsSync(path.join(DECK, 'slides')) ? path.join(DECK, 'slides') : DECK;
const deckJson = path.join(DECK, 'deck.json');
const order = fs.existsSync(deckJson) ? JSON.parse(fs.readFileSync(deckJson, 'utf8')).order
  : fs.readdirSync(SLIDES).filter(f => f.endsWith('.html')).sort().map(f => f.slice(0, -5));
const runtime = fs.readFileSync(path.join(__dirname, 'runtime.js'), 'utf8');
const title = opt('title') || '幻灯片预览';

// 本地图片转成 data URI，预览页才能单文件打开
const inlineImg = html => html.replace(/<img\b([^>]*?)\bsrc="([^"]+)"/g, (m, pre, src) => {
  if (/^(data:|https?:|\/)/.test(src)) return m;
  const f = path.resolve(DECK, src); if (!fs.existsSync(f)) return m;
  const ext = path.extname(f).slice(1).toLowerCase().replace('jpg', 'jpeg');
  return `<img${pre}src="data:image/${ext === 'svg' ? 'svg+xml' : ext};base64,${fs.readFileSync(f).toString('base64')}"`;
});

const pages = order.map((id, i) => {
  let h = fs.readFileSync(path.join(SLIDES, id + '.html'), 'utf8');
  h = inlineImg(h).replace(/<section\b/, `<section class="slide" data-id="${id}"`);
  return `<figure class="pg"><div class="box"><div class="scale">${h}</div></div><figcaption>${String(i + 1).padStart(2, '0')}　${id}</figcaption></figure>`;
}).join('\n');

const html = `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap">
<style>
:root{--bg:#EEF1F5;--fg:#1F2633;--muted:#7D8695}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#14181F;--fg:#E6E9EE;--muted:#9AA6B8}}
:root[data-theme="dark"]{--bg:#14181F;--fg:#E6E9EE;--muted:#9AA6B8}
body{margin:0;background:var(--bg);color:var(--fg);font-family:'Noto Sans SC','Microsoft YaHei','PingFang SC',sans-serif}
main{max-width:1280px;margin:0 auto;padding:24px 16px 48px;display:grid;gap:24px}
h1{font-size:20px;margin:0}
.pg{margin:0}.box{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;background:#fff;border-radius:6px;box-shadow:0 0 0 1px rgba(0,0,0,.08)}
.scale{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0}
figcaption{font-size:13px;color:var(--muted);padding-top:6px;font-family:Consolas,monospace}
body.raw main{max-width:none;padding:0;gap:0;display:block}body.raw .box{width:1920px;height:1080px;aspect-ratio:auto;border-radius:0;box-shadow:none}
body.raw figcaption,body.raw h1{display:none}
</style><script>${runtime}</script></head>
<body><main><h1>${title}</h1>
${pages}
</main>
<script>
if (new URLSearchParams(location.search).get('raw')) document.body.classList.add('raw');
function fit(){ if (document.body.classList.contains('raw')) return;
  document.querySelectorAll('.box').forEach(b => { b.querySelector('.scale').style.transform = 'scale(' + (b.clientWidth / 1920) + ')'; }); }
addEventListener('resize', fit); fit();
</script></body></html>`;
fs.writeFileSync(OUT, html);
console.log(OUT, order.length, 'slides');
