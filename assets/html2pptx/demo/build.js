// 组件用法示例：三页虚构内容。运行：node build.js <输出目录>
// 每页先判断内容结构，再用组件拼图形。坐标按本页内容定，不是固定版式。
const K = require('../components');
const { C, FS, LW } = K;
const out = process.argv[2] || 'demo-deck';

// 第 1 页 封面：深色底、图框刻度、叠板线稿
const cover = K.slide(
  K.frame({ color: C.slate }) +
  K.text(160, 300, '〈客户〉', { color: C.mute, size: FS.sub }) +
  K.text(160, 350, 'AI 应用一期项目方案', { size: FS.cover, color: C.white, weight: 700 }) +
  K.text(160, 460, '平台、系统接入、试点场景与实施计划', { size: FS.sub, color: C.line2 }) +
  K.plate(1180, 330, 360, 180, { top: C.svcBg, side: C.svc }) +
  K.plate(1180, 460, 360, 180, { top: C.prodBg, side: C.prod }) +
  K.plate(1180, 590, 360, 180, { top: C.ink1, side: C.mute, dash: true, stroke: C.mute }) +
  K.text(1130, 420, '实施服务', { color: C.line2, align: 'right' }) +
  K.text(1130, 550, '平台组件', { color: C.line2, align: 'right' }) +
  K.text(1130, 680, '企业现有系统', { color: C.mute, align: 'right' }),
  C.ink1, '封面图形是第 3 页建设内容的线稿。');

// 第 2 页 边界与穿越：数据在企业网络边界内外停在哪里
let b = '';
b += K.box(96, 220, 1100, 640, { stroke: C.slate, sw: LW.heavy, dash: true, r: 0 });
b += K.text(116, 232, '企业网络内', { color: C.slate, weight: 600 });
b += K.text(1240, 232, '企业网络外', { color: C.ink3, weight: 600 });
const sys = [['ERP（含 CRM）', '订单、客户、报价'], ['MES', '工单、报工'], ['知识库', '制度、工艺文件']];
sys.forEach(([name, data], i) => {
  const y = 300 + i * 170;
  b += K.box(140, y, 300, 120, { fill: C.white, stroke: C.line2 });
  b += K.text(164, y + 20, name, { size: FS.name, color: C.ink1, weight: 600 });
  b += K.text(164, y + 58, data, { color: C.ink3 });
  b += K.arrow(440, y + 60, 640, y + 60, { color: C.ai });
  b += K.text(470, y + 22, '读取', { color: C.ai });
});
b += K.box(640, 300, 380, 460, { fill: C.aiBg, stroke: C.ai });
b += K.text(664, 320, 'AI 工作台', { size: FS.name, color: C.ink1, weight: 700 });
b += K.para(664, 364, 330, ['MCP 网关统一鉴权', '按岗位限定可读数据', '调用记录逐条留存']);
b += K.stepNo(664 + 300, 330, 1);
b += K.arrow(1020, 520, 1420, 520, { color: C.ai });
b += K.text(1216, 480, '只发送脱敏问题', { color: C.ai });
b += K.crossMark(1180, 620);
b += K.line(1020, 620, 1170, 620, { color: C.ink1, sw: LW.flow });
b += K.text(1060, 640, '原始单据不出网', { color: C.ink1, weight: 600 });
b += K.box(1420, 440, 380, 160, { fill: C.white, stroke: C.line2 });
b += K.text(1444, 460, '公共大模型', { size: FS.name, color: C.ink1, weight: 600 });
b += K.text(1444, 500, '按调用量计费', { color: C.ink3 });
b += K.legend([['AI 组件', 'stroke', C.ai], ['网络边界', 'dash', C.slate]], 1824, 830, { align: 'right' });
const p2 = K.page({ no: 2, chapter: '01　平台架构', title: 'AI 平台架构', sub: '原始单据停在企业网络内。', right: '件号 8–11',
  provider: ['我方产品', C.prod], body: b, foot: '示意',
  attrs: [['部署', '企业服务器'], ['接入系统', '3 套'], ['出网内容', '脱敏问题'], ['留存', '调用记录']],
  notes: '边界内外的划分依据是客户信息安全制度。' });

// 第 3 页 时间压缩：同一时间轴上的前后两组泳道
let t = '';
const x0 = 360, unit = 220; // 1 天 = 220px
t += K.text(96, 230, '现状', { size: FS.section, color: C.ink1, weight: 700 });
[['收集需求', 0, 1], ['核对历史报价', 1, 2.5], ['审批', 2.5, 4.5]].forEach(([s, a, z], i) => {
  t += K.box(x0 + a * unit, 280 + i * 56, (z - a) * unit - 8, 40, { fill: C.bg2 });
  t += K.text(x0 + a * unit + 12, 288 + i * 56, s, { color: C.ink2 });
});
t += K.dimLine(x0, x0 + 4.5 * unit, 470, '4.5 天');
t += K.text(96, 560, '上线后', { size: FS.section, color: C.ink1, weight: 700 });
[['AI 预填报价单', 0, 0.5, true], ['业务员核对缺项', 0.5, 1, false], ['审批', 1, 2, false]].forEach(([s, a, z, ai], i) => {
  t += K.box(x0 + a * unit, 610 + i * 56, (z - a) * unit - 8, 40, ai ? { fill: C.aiBg, stroke: C.ai } : { fill: C.bg2 });
  t += K.text(x0 + z * unit + 8, 618 + i * 56, s, { color: ai ? C.ai : C.ink2 });
});
t += K.dimLine(x0, x0 + 2 * unit, 800, '2 天');
t += K.bigNumber(1440, 600, 384, '−2.5', '天', '单张报价周期');
t += K.legend([['AI 步骤', 'stroke', C.ai], ['人工步骤', 'fill', C.bg2]], 1824, 830, { align: 'right' });
const p3 = K.page({ no: 3, chapter: '02　试点场景', title: '销售报价应用前后的流程', sub: '业务员只核对 AI 标出的缺项。',
  provider: ['我方服务', C.svc], body: t, foot: '举例　时长为试点前的估算',
  attrs: [['输入', '客户询价单'], ['输出', '报价单草稿'], ['执行岗位', '业务员'], ['边界', '价格由人工确认']] });

K.writeDeck(out, [{ id: 'p01', html: cover }, { id: 'p02', html: p2 }, { id: 'p03', html: p3 }]);
console.log('已写出', out);
