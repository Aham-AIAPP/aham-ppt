# -*- coding: utf-8 -*-
"""关系图 / UI 原型组件库（自包含，通用）。供 B·现代专业档使用。
颜色一律传入；缺省取 Aham 角色色，使用时改成你的 tokens 角色色即可。
不写死任何品牌名/客户名——示例文字用占位符 BRAND。"""
import math as _m
SANS="Inter, 'PingFang SC', 'Microsoft YaHei', sans-serif"
MONO="'JetBrains Mono', Consolas, monospace"
ACC="#336EE8"; INK1="#262626"; INK2="#6E6E6E"; INK3="#9B9B9B"; INK4="#C4C4C4"; LINE="#E7E7E7"; PANEL="#F3F3F3"
BRAND="BRAND"  # 出片前替换为实际品牌占位

def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def T(x,y,s,size=14,fill=INK1,w=None,fam=SANS,anchor="start",ls=None):
    a=f' font-weight="{w}"' if w else ''; l=f' letter-spacing="{ls}"' if ls else ''
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-size="{size}" fill="{fill}"{a}{l}>{esc(s)}</text>'
def P(x,y,w,h,fill=PANEL,blue=False,r=12,stroke=None,sw=1):
    st=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st}/>'
    if blue: s+=f'<rect x="{x}" y="{y}" width="3" height="{h}" rx="1.5" fill="{ACC}"/>'
    return s
def L(x1,y1,x2,y2,c=LINE,sw=1,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"{d}/>'

# ---- 箭头：直线 / 曲线 ----
def arrow(x1,y1,x2,y2,c=INK3,sw=1.5,dash=None):
    ang=_m.atan2(y2-y1,x2-x1); hl=8
    ax,ay=x2-hl*_m.cos(ang),y2-hl*_m.sin(ang)
    p1=(x2-hl*_m.cos(ang-0.42),y2-hl*_m.sin(ang-0.42))
    p2=(x2-hl*_m.cos(ang+0.42),y2-hl*_m.sin(ang+0.42))
    return L(x1,y1,ax,ay,c,sw,dash)+f'<polygon points="{x2},{y2} {p1[0]},{p1[1]} {p2[0]},{p2[1]}" fill="{c}"/>'
def carrow(x1,y1,x2,y2,c=INK3,sw=1.6,bend=0.18,dash=None):
    mx,my=(x1+x2)/2,(y1+y2)/2; dx,dy=x2-x1,y2-y1
    cx,cy=mx-dy*bend,my+dx*bend
    ang=_m.atan2(y2-cy,x2-cx); hl=9
    p1=(x2-hl*_m.cos(ang-0.4),y2-hl*_m.sin(ang-0.4))
    p2=(x2-hl*_m.cos(ang+0.4),y2-hl*_m.sin(ang+0.4))
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<path d="M{x1} {y1} Q {cx} {cy} {x2} {y2}" fill="none" stroke="{c}" stroke-width="{sw}"{d}/>'
            f'<polygon points="{x2},{y2} {p1[0]},{p1[1]} {p2[0]},{p2[1]}" fill="{c}"/>')

# ---- chip / hexagon / KPI ----
def chip(x,y,w,h,label,sub=None,blue=False,dashed=False):
    st=f' stroke="{ACC if blue else INK4}" stroke-width="1.2"'
    da=' stroke-dasharray="4 3"' if dashed else ''
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#FFFFFF"{st}{da}/>'
    if blue and not dashed: s+=f'<rect x="{x}" y="{y}" width="3" height="{h}" rx="1.5" fill="{ACC}"/>'
    s+=T(x+w/2,y+(h/2+5 if not sub else h/2-2),label,13.5,INK1,600,anchor="middle")
    if sub: s+=T(x+w/2,y+h/2+16,sub,10.5,INK3,anchor="middle")
    return s
def hexagon(cx,cy,r,fill="#FFFFFF",stroke=INK3,sw=1.4):
    pts=" ".join(f"{cx+r*_m.cos(_m.radians(a))},{cy+r*_m.sin(_m.radians(a))}" for a in range(0,360,60))
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

# ---- 状态点（双通道：色点 + 文字，色盲友好）----
def status(x,y,label,kind="ok"):
    c={"ok":"#5A7A60","warn":"#8A7333","bad":"#9E3D31","idle":INK3}.get(kind,INK3)
    return f'<circle cx="{x}" cy="{y-4}" r="4" fill="{c}"/>'+T(x+12,y,label,12.5,INK1)




def placeholder(x, y, w, h, label="产品界面"):
    """软件界面占位框（待替换真实截图）——demo/UI 未到位时占位，不硬编假界面。"""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#F7F8FA" stroke="{INK4}" stroke-width="1.5" stroke-dasharray="7 5"/>'
    cx, cy = x + w/2, y + h/2
    s += f'<rect x="{cx-30:.0f}" y="{cy-34:.0f}" width="60" height="44" rx="5" fill="none" stroke="{INK3}" stroke-width="1.8"/>'
    s += f'<circle cx="{cx-12:.0f}" cy="{cy-20:.0f}" r="5" fill="{INK3}"/>'
    s += f'<path d="M{cx-26:.0f} {cy+8:.0f} l18 -18 l11 11 l9 -7 l16 14" fill="none" stroke="{INK3}" stroke-width="1.8" stroke-linejoin="round"/>'
    s += T(cx, cy+38, "产品界面占位", 12, INK2, 700, anchor="middle")
    s += T(cx, cy+59, label, 10, INK3, anchor="middle")
    return s
