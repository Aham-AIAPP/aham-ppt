// 读 tokens.json，给出各脚本要用的常量。数值只写在 tokens.json，本文件只做换算，不另写数值。
// tokens.json 与 references/style-tokens.md 一致，由 tests/test_tokens.py 检查。
const T = require('./tokens.json');

const CANVAS = T.canvas;                         // 画布，单位 px
const PX_PER_PT = T.canvas.pxPerPt;              // 2px = 1 磅
const PX_PER_IN = PX_PER_PT * 72;                // 144px = 1 英寸
const F = T.frame;

// 字体栈的第一项是导出到 PPT 时写的字体
const firstFamily = stack => stack.split(',')[0].replace(/['"]/g, '').trim();

module.exports = {
  C: T.C, FS: T.FS, LW: T.LW, RAD: T.RAD, CANVAS, PX_PER_PT, PX_PER_IN,
  FONT_STACK: T.font.stack, MONO: T.font.mono,
  FONT_FACE: firstFamily(T.font.stack), MONO_FACE: firstFamily(T.font.mono),
  FRAME: F, MARGIN: F.margin, RIGHT: F.right,
  MAIN: { y0: F.main.y0, y1: F.main.y1 },
  // 主图区矩形：左右边距之间，主图区上下界之间
  MAIN_RECT: { x: F.margin, y: F.main.y0, w: F.right - F.margin, h: F.main.y1 - F.main.y0 },
};
