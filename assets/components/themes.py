# -*- coding: utf-8 -*-
"""三档主题模板：A 克制档 / B 现代专业档（默认）/ C 高表现力档。
A 克制白皮书，B 现代专业（默认），由 cover/toc/section/chrome 按 theme='A'|'B' 切换；
C 高表现力档为深色重音页（#1C1C1C + 超大 mono 数字），由 cover_dark/section_dark/quote_dark 提供。
三档共用同一份内容与组件，只切换封面/目录/章节模板与页眉皮肤（重音手法）。
全部参数化、无品牌/客户硬编码——调用时传入实际文字。
1280x720 画布。依赖同目录 components.py / icons.py。"""
from components import (T,P,L,MONO,ACC,INK1,INK2,INK3,INK4,LINE,PANEL)
from icons import icon_circle

def _svg(body,bg="#FFFFFF"):
    return (f'<svg width="1280" height="720" viewBox="0 0 1280 720" '
            f'xmlns="http://www.w3.org/2000/svg"><rect width="1280" height="720" fill="{bg}"/>{body}</svg>')

# ============================================================
#  封面
# ============================================================
def cover(theme,brand,title,subtitle,chapters,meta_left="",meta_right="",eyebrow="OVERVIEW"):
    """theme='A'|'B'. chapters=[(num,zh,sub,icon),...]。
    eyebrow：B 档大标题上方的小字眉标，中性占位，按实际主题传入（勿写死行业）。"""
    if theme=="A":
        b=[f'<rect x="40" y="60" width="12" height="12" rx="2" fill="{ACC}"/>',
           T(62,76,brand,19,INK1,700),
           T(40,312,title,46,INK1,700)]
        if subtitle: b.append(T(40,374,subtitle,19,INK2))
        b.append(f'<rect x="42" y="398" width="116" height="4" fill="{ACC}"/>')
        # 右侧竖排目录
        b.append(L(856,276,856,496))
        b.append(T(892,296,"目录　CONTENTS",13,INK3,ls=2))
        for i,(n,zh,sub,ic) in enumerate(chapters[:6]):
            y=344+i*42
            b.append(T(892,y,n,16,INK3,fam=MONO)); b.append(T(936,y,zh,17,INK1))
        b.append(L(40,648,1240,648))
        b.append(T(40,682,meta_left,13,INK3)); b.append(T(1240,682,meta_right,13,INK3,anchor="end"))
        return _svg("".join(b))
    # B · Hero
    b=[f'<rect x="40" y="60" width="12" height="12" rx="2" fill="{ACC}"/>',
       T(62,76,brand,19,INK1,700),
       T(80,168,eyebrow,13,INK3,ls=5),
       T(80,332,title,58,INK1,700)]
    if subtitle: b.append(T(80,404,subtitle,20,INK2))
    b.append(f'<rect x="84" y="430" width="150" height="5" rx="2" fill="{ACC}"/>')
    # 右侧浅色信息块 + 章节缩略（motif，不堆色）
    b.append(P(812,96,428,528,PANEL,r=22))
    b.append(T(852,150,"本册导览",15,INK1,700)); b.append(T(852,172,"IN THIS DECK",10,INK3,ls=2))
    for i,(n,zh,sub,ic) in enumerate(chapters[:5]):
        y=214+i*78
        b.append(icon_circle(ic,874,y,18,INK2,"#FFFFFF",isize=22))
        b.append(T(906,y-4,n+"  "+zh,16,INK1,600));
        if sub: b.append(T(906,y+18,sub,12,INK2))
    b.append(L(80,648,1240,648))
    b.append(T(80,682,meta_left,13,INK3)); b.append(T(1240,682,meta_right,13,INK3,anchor="end"))
    return _svg("".join(b))

# ============================================================
#  目录
# ============================================================
def toc(theme,chapters):
    """chapters=[(num,zh,sub,icon),...]"""
    if theme=="A":
        b=[T(40,200,"目录",40,INK1,700),T(40,250,"CONTENTS",15,INK3,ls=3)]
        for i,(n,zh,sub,ic) in enumerate(chapters):
            y=180+i*120
            b.append(T(620,y,n,30,INK3,fam=MONO,w=700))
            b.append(T(690,y,zh,24,INK1,600)); b.append(T(690,y+30,sub,14,INK2))
            if i<len(chapters)-1: b.append(L(620,y+58,1240,y+58))
        return _svg("".join(b))
    # B · 图标圆 + 描述 + 右侧缩略
    b=[T(40,140,"目录",40,INK1,700),T(40,190,"CONTENTS",15,INK3,ls=3),L(40,210,1240,210)]
    for i,(n,zh,sub,ic) in enumerate(chapters):
        y=270+i*96
        b.append(icon_circle(ic,80,y,24,ACC,PANEL,isize=28))
        b.append(T(124,y-8,n,14,INK3,fam=MONO,w=700)); b.append(T(124,y+16,zh,22,INK1,700))
        b.append(T(470,y+6,sub,15,INK2))
        if i<len(chapters)-1: b.append(L(40,y+48,1240,y+48))
    return _svg("".join(b))

# ============================================================
#  章节过渡页
# ============================================================
def section(theme,num,zh,summary,total="04",items=None):
    """items(B 用)=[(icon,text),...] 右侧「本章内容」。"""
    if theme=="A":
        b=[T(40,300,num,120,INK4,700,fam=MONO),
           f'<rect x="44" y="330" width="90" height="4" fill="{ACC}"/>',
           T(40,400,zh,40,INK1,700),
           T(40,452,summary,17,INK2),
           T(1240,700,f"{num} / {total}",11,INK3,fam=MONO,anchor="end")]
        return _svg("".join(b))
    # B · 大水印编号 + 右侧本章内容
    b=[f'<rect x="0" y="0" width="470" height="720" fill="{PANEL}"/>',
       T(60,300,num,200,"#FFFFFF",700,fam=MONO),
       f'<rect x="60" y="470" width="120" height="6" rx="3" fill="{ACC}"/>',
       T(60,540,zh,38,INK1,700),
       T(60,592,summary,15,INK2),
       T(60,640,f"PART {num} / {total}",13,INK3,ls=3,fam=MONO)]
    # 水印描边编号（叠在浅块上，避免纯填充太重）
    b.insert(1,T(60,300,num,200,PANEL,700,fam=MONO))
    rx=560
    b.append(T(rx,150,"本章内容",16,INK1,700)); b.append(T(rx,172,"IN THIS SECTION",10,INK3,ls=2))
    for i,(ic,t) in enumerate(items or []):
        y=230+i*84
        b.append(icon_circle(ic,rx+22,y,19,INK2,PANEL,isize=23))
        b.append(T(rx+52,y-4,t,16,INK1,600))
        if i<len(items)-1: b.append(L(rx,y+40,1240,y+40,LINE,1))
    return _svg("".join(b))

# ============================================================
#  内容页页眉（chrome）
# ============================================================
def chrome(theme,section_label,title,source,page,total,body,brand="",tsize=32,icon=None):
    head=[T(40,24,section_label,11,INK2,ls=1)]
    if brand:
        head.append(f'<rect x="1188" y="16" width="9" height="9" rx="2" fill="{ACC}"/>')
        head.append(T(1240,24,brand,12,INK1,600,anchor="end"))
    head.append(L(40,32,1240,32))
    tx=40
    if theme=="B" and icon:
        head.append(icon_circle(icon,58,70,16,ACC,PANEL,isize=20)); tx=86
    head.append(T(tx,78,title,tsize,INK1,700))
    head.append(L(40,94,1240,94))
    foot=[L(40,690,1240,690),
          T(40,709,"来源："+source,11,INK2),
          T(1240,709,f"{page} / {total}",11,INK2,fam=MONO,anchor="end")]
    return _svg("".join(head)+body+"".join(foot))


# ============================================================
#  C · 高表现力档 —— 深色模板（v3）
#  深底 #1C1C1C + 浅色字；不依赖 icons，只用 components 原子函数。
# ============================================================
BG_DARK = "#1C1C1C"
LT1 = "#F2F2F2"      # 深底上主字
LT2 = "#A8A8A8"      # 深底上次字
LT3 = "#787878"      # 深底装饰性弱字（对 #1C1C1C 仅 3.86:1，不得承载须读取的信息；信息性小字用 LT2）
DK_LINE = "#3A3A3A"  # 深底上的分隔线
DK_PANEL = "#262626" # 深底上稍亮的块
ACC_HOVER = "#5C8BED" # 深底信息性蓝字（对 #262626 4.59:1、对 #1C1C1C 5.17:1，过 AA；#336EE8 在深底仅作装饰）


def cover_dark(brand, title, subtitle, chapters, meta_left="", meta_right="", eyebrow="OVERVIEW"):
    """C 档深色封面。chapters=[(num,zh,sub,icon),...]（仅用 num/zh/sub）。
    eyebrow：大标题上方小字眉标，中性占位，按实际主题传入（勿写死行业）。"""
    b = [f'<rect x="40" y="60" width="12" height="12" rx="2" fill="{ACC}"/>',
         T(62, 76, brand, 19, LT1, 700),
         T(80, 168, eyebrow, 13, LT2, ls=5),
         T(80, 332, title, 56, LT1, 700)]
    if subtitle:
        b.append(T(80, 404, subtitle, 20, LT2))
    b.append(f'<rect x="84" y="430" width="150" height="5" rx="2" fill="{ACC}"/>')
    b.append(f'<rect x="812" y="96" width="428" height="528" rx="22" fill="{DK_PANEL}"/>')
    b.append(T(852, 150, "本册导览", 15, LT1, 700))
    b.append(T(852, 172, "IN THIS DECK", 10, LT2, ls=2))
    m = min(len(chapters), 5)
    for i, (n, zh, sub, ic) in enumerate(chapters[:5]):
        y = 220 + i * 78
        b.append(T(852, y, n, 14, ACC_HOVER, 700, fam=MONO))
        b.append(T(892, y, zh, 16, LT1, 600))
        if sub:
            b.append(T(892, y + 20, sub, 12, LT2))
        if i < m - 1:
            b.append(L(852, y + 46, 1200, y + 46, DK_LINE, 1))
    b.append(L(80, 648, 1240, 648, DK_LINE, 1))
    b.append(T(80, 682, meta_left, 13, LT2))
    b.append(T(1240, 682, meta_right, 13, LT2, anchor="end"))
    return _svg("".join(b), bg=BG_DARK)


def section_dark(num, zh, summary, total="04", items=None):
    """C 档深色章节页。items=[text,...]（字符串列表，右侧本章内容）。"""
    b = [T(60, 300, num, 200, "#2E2E2E", 700, fam=MONO),
         f'<rect x="60" y="470" width="120" height="6" rx="3" fill="{ACC}"/>',
         T(60, 540, zh, 40, LT1, 700),
         T(60, 592, summary, 16, LT2),
         T(60, 640, f"PART {num} / {total}", 13, LT2, ls=3, fam=MONO)]
    if items:
        rx = 620
        b.append(T(rx, 150, "本章内容", 16, LT1, 700))
        b.append(T(rx, 172, "IN THIS SECTION", 10, LT2, ls=2))
        for i, t in enumerate(items):
            y = 232 + i * 80
            b.append(f'<rect x="{rx}" y="{y-13}" width="6" height="26" rx="2" fill="{ACC}"/>')
            b.append(T(rx + 22, y + 5, t, 16, LT1, 600))
            if i < len(items) - 1:
                b.append(L(rx, y + 40, 1200, y + 40, DK_LINE, 1))
    b.append(T(1240, 700, f"{num} / {total}", 11, LT2, fam=MONO, anchor="end"))
    return _svg("".join(b), bg=BG_DARK)


def quote_dark(lines, attribution="", brand=""):
    """C 档金句页。lines=字符串或字符串列表（每行一句，自行折行）。"""
    if isinstance(lines, str):
        lines = [lines]
    b = []
    if brand:
        b.append(f'<rect x="40" y="60" width="12" height="12" rx="2" fill="{ACC}"/>')
        b.append(T(62, 76, brand, 17, LT2, 700))
    b.append(T(108, 300, "\u201C", 170, "#333333", 700))
    n = len(lines)
    lh = 66
    y0 = 360 - (n - 1) * lh / 2
    for i, ln in enumerate(lines):
        b.append(T(152, y0 + i * lh, ln, 40, LT1, 700))
    yend = y0 + (n - 1) * lh + 42
    b.append(f'<rect x="154" y="{yend:.0f}" width="120" height="4" rx="2" fill="{ACC}"/>')
    if attribution:
        b.append(T(154, yend + 44, attribution, 17, LT2))
    return _svg("".join(b), bg=BG_DARK)
