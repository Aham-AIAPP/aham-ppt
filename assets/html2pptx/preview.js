// 把幻灯片目录合成一个自包含的预览页（可本地打开，也可发布为 Artifact）
// 用法：node preview.js <幻灯片目录> <输出.html> [--title 标题]
// 每页按窗口宽度缩放；?raw=1 时不缩放（排版检查和导出用）
const fs = require('fs');
const { loadDeck, buildPage } = require('./deck');
const argv = process.argv.slice(2);
const opt = k => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : undefined; };
const [DECK, OUT] = argv.filter((a, i) => !a.startsWith('--') && !(i > 0 && argv[i - 1].startsWith('--')));
if (!DECK || !OUT) { console.error('用法：node preview.js <幻灯片目录> <输出.html> [--title 标题]'); process.exit(2); }
const slides = loadDeck(DECK);
fs.writeFileSync(OUT, buildPage(slides, DECK, opt('title') || '幻灯片预览'));
console.log(OUT, slides.length, 'slides');
