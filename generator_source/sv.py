import math, itertools
_uid = itertools.count(1)
def uid(p='u'): return f"{p}{next(_uid)}"
def f(v): 
    s = f"{v:.1f}"
    return s[:-2] if s.endswith('.0') else s
def P(p): return f"{f(p[0])} {f(p[1])}"
def attrs(o):
    out=''
    for k,v in o.items():
        if v is None: continue
        k=k.replace('_','-')
        if k=='cls': k='class'
        out+=f' {k}="{v}"'
    return out
def path(d, **o): return f'<path d="{d}"{attrs(o)}/>'
def circ(x,y,r,**o): return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"{attrs(o)}/>'
def ell(x,y,rx,ry,**o): return f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry)}"{attrs(o)}/>'
def rect(x,y,w,h,**o): return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"{attrs(o)}/>'
def line(a,b,**o): return f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}"{attrs(o)}/>'
def g(inner, **o): return f'<g{attrs(o)}>{inner}</g>'
def text(s,x,y,size=20,fill='#fff',weight=400,anchor='start',family="Inter, 'Segoe UI', Arial, sans-serif",**o):
    s=s.replace('&','&amp;').replace('<','&lt;')
    return f'<text x="{f(x)}" y="{f(y)}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{attrs(o)}>{s}</text>'
def doc(inner, vb, defs='', title=None, w=None, h=None):
    x,y,W,H = vb
    t = f'<title>{title}</title>' if title else ''
    d = f'<defs>{defs}</defs>' if defs else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f(x)} {f(y)} {f(W)} {f(H)}" width="{f(w or W)}" height="{f(h or H)}">{t}{d}{inner}</svg>'
def lg(id, stops, x1=0,y1=0,x2=0,y2=1):
    s=''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a is not None else '') + '/>' for o,c,a in [(st+(None,))[:3] for st in stops])
    return f'<linearGradient id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'
def rg(id, stops, cx=.5, cy=.5, r=.5, fx=None, fy=None):
    s=''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a is not None else '') + '/>' for o,c,a in [(st+(None,))[:3] for st in stops])
    fxy = f' fx="{fx}" fy="{fy}"' if fx is not None else ''
    return f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}"{fxy}>{s}</radialGradient>'
# vector math (angle convention: 0 = down, +90 = forward(+x), 180 = up)
D=math.pi/180
def dirv(a): return [math.sin(a*D), math.cos(a*D)]
def add(a,b): return [a[0]+b[0],a[1]+b[1]]
def sub(a,b): return [a[0]-b[0],a[1]-b[1]]
def mul(a,k): return [a[0]*k,a[1]*k]
def vlen(a): return math.hypot(a[0],a[1])
def ang(v): return math.atan2(v[0],v[1])/D
def rot(v,a):
    c,s=math.cos(a*D),math.sin(a*D); return [v[0]*c-v[1]*s, v[0]*s+v[1]*c]
def lerp(a,b,t): return a+(b-a)*t
def clamp(v,a=0,b=1): return max(a,min(b,v))
def hexrgb(h):
    h=h.lstrip('#'); h=''.join(c*2 for c in h) if len(h)==3 else h; return [int(h[i:i+2],16) for i in (0,2,4)]
def mixc(a,b,t):
    A,B=hexrgb(a),hexrgb(b); return '#'+''.join(f'{round(lerp(A[i],B[i],t)):02x}' for i in range(3))
def dark(c,t=.35): return mixc(c,'#000000',t)
def light(c,t=.35): return mixc(c,'#ffffff',t)
def smooth(pts, closed=True, k=1.0):
    n=len(pts)
    if n<3: return 'M'+'L'.join(P(p) for p in pts)
    d='M'+P(pts[0])
    rng = range(n) if closed else range(n-1)
    for i in rng:
        p0=pts[(i-1)%n] if closed or i>0 else pts[i]
        p1=pts[i]; p2=pts[(i+1)%n]
        p3=pts[(i+2)%n] if closed or i+2<n else p2
        c1=add(p1, mul(sub(p2,p0), k/6)); c2=sub(p2, mul(sub(p3,p1), k/6))
        d+=f'C{P(c1)} {P(c2)} {P(p2)}'
    return d+('Z' if closed else '')
import random
def rnd(seed): return random.Random(seed)
