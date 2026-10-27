// 在浏览器里读出每页元素的实际位置和样式，供 html2pptx.js 导出、check_slides.js 检查导出兼容性。
// 读的是浏览器排版后的结果，所以网页上看到的位置、尺寸、颜色就是导出到 PPT 的值。
(function () {
  const INLINE_OK = new Set(['b', 'strong', 'span', 'br', 'i', 'em']);
  const TAGS = new Set(['p', 'div', 'x-shape', 'x-connector', 'svg', 'img']);

  function rgba(s) {
    const m = /rgba?\(([^)]+)\)/.exec(s || ''); if (!m) return null;
    const p = m[1].split(/[\s,/]+/).filter(Boolean).map(parseFloat);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  // 半透明色按底色混成实色；全透明返回 null
  function hex(s, under) {
    const c = rgba(s); if (!c || c.a === 0) return null;
    const u = under || { r: 255, g: 255, b: 255 };
    return ['r', 'g', 'b'].map(k => Math.round(c[k] * c.a + u[k] * (1 - c.a)).toString(16).padStart(2, '0')).join('').toUpperCase();
  }
  // 把行内写的颜色（可能是命名色）换成 rgb()
  function resolve(v) {
    if (!v) return ''; const d = document.createElement('i'); d.style.color = v; document.body.appendChild(d);
    const c = getComputedStyle(d).color; d.remove(); return c;
  }
  const alpha = s => { const c = rgba(s); return c ? c.a : 1; };
  const px = v => parseFloat(v) || 0;

  function sides(cs, under) {
    return ['Top', 'Right', 'Bottom', 'Left'].map(k => {
      const w = px(cs['border' + k + 'Width']), st = cs['border' + k + 'Style'];
      return w > 0 && st !== 'none' && st !== 'hidden' ? { w, dash: st !== 'solid', color: hex(cs['border' + k + 'Color'], under) } : null;
    });
  }

  // 段内文字：<br> 分行；颜色、加粗、斜体按每段文字所在元素的计算样式取
  function runs(p, under) {
    const pre = /pre/.test(getComputedStyle(p).whiteSpace), out = [];
    (function walk(n) {
      for (const c of n.childNodes) {
        if (c.nodeType === 3) {
          let t = c.textContent; if (!pre) t = t.replace(/\s+/g, ' '); if (!t) continue;
          const st = getComputedStyle(c.parentElement);
          out.push({ text: t, color: hex(st.color, under), bold: +st.fontWeight >= 600, italic: st.fontStyle === 'italic' });
        } else if (c.nodeType === 1) { if (c.localName === 'br') out.push({ br: true }); else walk(c); }
      }
    })(p);
    // 行首行尾的空格去掉，与浏览器显示一致
    for (let i = 0; i < out.length; i++) {
      if (out[i].br) continue;
      const atStart = i === 0 || out[i - 1].br, atEnd = i === out.length - 1 || out[i + 1].br;
      if (atStart) out[i].text = out[i].text.replace(/^ +/, '');
      if (atEnd) out[i].text = out[i].text.replace(/ +$/, '');
    }
    return out.filter(r => r.br || r.text);
  }

  function lint(el, cs, issues, tag) {
    const t = (el.textContent || '').trim().slice(0, 16) || tag;
    if (cs.position !== 'absolute') issues.push(['ERROR', `${tag} 没有绝对定位：${t}`]);
    if (cs.transform !== 'none') issues.push(['ERROR', `transform 导出时丢失：${t}`]);
    if (cs.boxShadow !== 'none') issues.push(['ERROR', `阴影导出时丢失：${t}`]);
    if (cs.textShadow !== 'none') issues.push(['ERROR', `文字阴影导出时丢失：${t}`]);
    if (cs.backgroundImage !== 'none') issues.push(['ERROR', `渐变或背景图导出时丢失：${t}`]);
    if (+cs.opacity < 1) issues.push(['ERROR', `opacity 导出时丢失：${t}`]);
    if (cs.filter !== 'none') issues.push(['ERROR', `filter 导出时丢失：${t}`]);
    for (const k of ['backgroundColor', 'color', 'borderTopColor']) {
      const a = alpha(cs[k]);
      if (a > 0 && a < 1 && !(k === 'borderTopColor' && px(cs.borderTopWidth) === 0) && !(k === 'color' && tag !== 'p'))
        issues.push(['WARNING', `半透明色按底色混成实色导出：${t}`]);
    }
  }

  window.extractSlides = function () {
    return [...document.querySelectorAll('section.slide')].map(sec => {
      const sr = sec.getBoundingClientRect(), k = sr.width / 1920;
      const scs = getComputedStyle(sec), bgc = rgba(scs.backgroundColor);
      const under = bgc && bgc.a > 0 ? bgc : { r: 255, g: 255, b: 255 };
      const issues = [], els = [];
      const notes = [...sec.querySelectorAll('aside')].map(a => a.textContent.trim()).filter(Boolean).join('\n');
      for (const el of sec.children) {
        const tag = el.localName;
        if (tag === 'aside' || tag === 'script' || tag === 'style') continue;
        if (!TAGS.has(tag)) { issues.push(['ERROR', `不支持的元素 <${tag}>，导出时忽略`]); continue; }
        const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
        const box = { x: (r.left - sr.left) / k, y: (r.top - sr.top) / k, w: r.width / k, h: r.height / k };
        if (tag !== 'x-connector') lint(el, cs, issues, tag);
        if (tag === 'x-connector') {
          const a = n => +el.getAttribute(n);
          els.push({ tag, x1: a('x1'), y1: a('y1'), x2: a('x2'), y2: a('y2'), head: el.getAttribute('head') || 'none', route: el.getAttribute('route') || '',
            color: hex(cs.color, under) || '000000', w: px(el.style.borderWidth) || 2, dash: /dash|dot/.test(el.style.borderStyle) });
          continue;
        }
        if (tag === 'svg' || tag === 'img') {
          if (!box.w || !box.h) issues.push(['ERROR', `${tag} 宽或高为 0`]);
          const o = { tag, ...box, alt: el.getAttribute('aria-label') || el.getAttribute('alt') || '' };
          if (tag === 'img') o.src = el.getAttribute('src');
          else { const c = el.cloneNode(true); c.setAttribute('width', box.w); c.setAttribute('height', box.h); c.removeAttribute('style'); o.svg = c.outerHTML; }
          els.push(o); continue;
        }
        const fill = hex(cs.backgroundColor, under), sd = sides(cs, under);
        const uniform = sd.every(s => s && sd[0] && s.w === sd[0].w && s.color === sd[0].color && s.dash === sd[0].dash);
        const rad = /%$/.test(cs.borderTopLeftRadius) ? Math.min(box.w, box.h) * px(cs.borderTopLeftRadius) / 100 : px(cs.borderTopLeftRadius);
        const base = { tag, ...box, fill, border: uniform ? sd[0] : null, lines: uniform ? [] : sd, rad };
        if (tag === 'x-shape') {
          const kind = el.getAttribute('kind');
          // 菱形在网页上由 runtime 画成 svg，原样式在行内 style 里
          if (kind === 'diamond') {
            const st = el.style, w = px(st.borderTopWidth);
            base.fill = hex(resolve(st.backgroundColor), under);
            base.border = w > 0 && st.borderTopStyle !== 'none' ? { w, dash: st.borderTopStyle !== 'solid', color: hex(resolve(st.borderTopColor), under) } : null;
            base.lines = [];
          }
          els.push({ ...base, kind }); continue;
        }
        if (tag === 'div') {
          if (el.textContent.trim()) issues.push(['ERROR', `div 里有文字，导出时丢失：${el.textContent.trim().slice(0, 16)}`]);
          els.push(base); continue;
        }
        // p
        for (const c of el.querySelectorAll('*')) if (!INLINE_OK.has(c.localName)) {
          issues.push([c.localName === 'svg' || c.localName === 'img' ? 'ERROR' : 'WARNING', `p 里的 <${c.localName}> 导出为普通文字：${el.textContent.trim().slice(0, 16)}`]); break;
        }
        const fs = px(cs.fontSize), lh = cs.lineHeight === 'normal' ? fs * 1.2 : px(cs.lineHeight);
        els.push({ ...base, runs: runs(el, under), fs, lh, mono: /mono|consolas|courier/i.test(cs.fontFamily),
          align: { center: 'center', right: 'right', end: 'right' }[cs.textAlign] || 'left',
          nowrap: cs.whiteSpace === 'nowrap' || !el.style.width,
          pad: ['Top', 'Right', 'Bottom', 'Left'].map(s => px(cs['padding' + s])),
          bw: ['Top', 'Right', 'Bottom', 'Left'].map(s => px(cs['border' + s + 'Width'])) });
      }
      return { id: sec.dataset.id, bg: hex(scs.backgroundColor) || 'FFFFFF', els, notes, issues };
    });
  };
})();
