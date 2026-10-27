// 浏览器里显示 x-shape 和 x-connector。预览页和排版检查都内嵌本文件。
// 形状与连线的语义与 html2pptx.js 一致：导出时它们是 PPT 原生形状和线条。
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const css = `
section.slide{position:relative;width:1920px;height:1080px;overflow:hidden;box-sizing:border-box}
section.slide > p{margin:0;position:absolute;box-sizing:border-box}
section.slide > div,section.slide > x-shape,section.slide > svg,section.slide > img{position:absolute;box-sizing:border-box;display:block}
section.slide x-shape[kind=ellipse]{border-radius:50%}
section.slide x-shape[kind=diamond]{background:none!important;border:none!important}
section.slide x-connector{position:absolute;left:0;top:0;width:0;height:0;display:block;overflow:visible}
section.slide aside{display:none}`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function el(tag, attrs) { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; }
  function pts(c) {
    const x1 = +c.getAttribute('x1'), y1 = +c.getAttribute('y1'), x2 = +c.getAttribute('x2'), y2 = +c.getAttribute('y2');
    const r = c.getAttribute('route');
    if (r === 'hv') return [[x1, y1], [x2, y1], [x2, y2]];
    if (r === 'vh') return [[x1, y1], [x1, y2], [x2, y2]];
    if (r === 'elbow') {
      if (Math.abs(x2 - x1) >= Math.abs(y2 - y1)) { const mx = (x1 + x2) / 2; return [[x1, y1], [mx, y1], [mx, y2], [x2, y2]]; }
      const my = (y1 + y2) / 2; return [[x1, y1], [x1, my], [x2, my], [x2, y2]];
    }
    return [[x1, y1], [x2, y2]];
  }
  function head(svg, a, b, color, w) {
    const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), L = 6 + w * 3, W = 3 + w * 1.6;
    const p = [b, [b[0] - L * Math.cos(ang) + W * Math.sin(ang), b[1] - L * Math.sin(ang) - W * Math.cos(ang)],
      [b[0] - L * Math.cos(ang) - W * Math.sin(ang), b[1] - L * Math.sin(ang) + W * Math.cos(ang)]];
    svg.appendChild(el('polygon', { points: p.map(q => q.join(',')).join(' '), fill: color }));
  }
  function render(root) {
    root.querySelectorAll('x-connector').forEach(c => {
      if (c.dataset.done) return; c.dataset.done = 1;
      const cs = c.getAttribute('style') || '';
      const color = (/(?:^|;)\s*color\s*:\s*([^;]+)/.exec(cs) || [])[1] || '#000';
      const w = parseFloat((/border-width\s*:\s*([\d.]+)/.exec(cs) || [])[1] || 2);
      const dash = /border-style\s*:\s*dashed/.test(cs);
      const P = pts(c), h = c.getAttribute('head') || 'none';
      const svg = el('svg', { width: 1920, height: 1080, style: 'position:absolute;left:0;top:0;overflow:visible;pointer-events:none' });
      svg.appendChild(el('polyline', { points: P.map(q => q.join(',')).join(' '), fill: 'none', stroke: color, 'stroke-width': w, 'stroke-dasharray': dash ? `${w * 3} ${w * 2}` : 'none' }));
      if (h === 'end' || h === 'both') head(svg, P[P.length - 2], P[P.length - 1], color, w);
      if (h === 'start' || h === 'both') head(svg, P[1], P[0], color, w);
      c.appendChild(svg);
    });
    // 圆角矩形按 PPT 默认圆角（短边的 1/6）显示，与导出一致
    root.querySelectorAll('x-shape[kind=rounded]').forEach(d => {
      d.style.borderRadius = Math.min(parseFloat(d.style.width) || 0, parseFloat(d.style.height) || 0) / 6 + 'px';
    });
    root.querySelectorAll('x-shape[kind=diamond]').forEach(d => {
      if (d.dataset.done) return; d.dataset.done = 1;
      const cs = d.getAttribute('style') || '';
      const bg = (/background(?:-color)?\s*:\s*([^;]+)/.exec(cs) || [])[1] || 'none';
      const bd = /border\s*:\s*([\d.]+)px\s+\w+\s+([^;]+)/.exec(cs);
      const w = parseFloat(d.style.width), hh = parseFloat(d.style.height), sw = bd ? +bd[1] : 0;
      const svg = el('svg', { width: w, height: hh, style: 'position:absolute;left:0;top:0;overflow:visible' });
      svg.appendChild(el('polygon', { points: `${w / 2},0 ${w},${hh / 2} ${w / 2},${hh} 0,${hh / 2}`, fill: bg, stroke: bd ? bd[2] : 'none', 'stroke-width': sw }));
      d.appendChild(svg);
    });
  }
  window.renderSlides = render;
  document.addEventListener('DOMContentLoaded', () => render(document));
})();
