from sv import *
LW=2.4
def S(c,k=.55,w=LW): return dict(fill=c,stroke=(dark(c,k) if c.startswith('#') else '#22252D'),stroke_width=w,stroke_linejoin='round')
def R(x,y,w,h,c,rx=0,k=.55,**o):
    a=S(c,k); a.update(o); return rect(x,y,w,h,rx=rx,**a)
def hi(d,c='#ffffff',op='.4',w=3): return path(d,fill='none',stroke=c,stroke_width=w,stroke_linecap='round',opacity=op)
def shade(d,op='.16'): return path(d,fill='#000',opacity=op)
def ln(d,c,w=2,op=None,**o): return path(d,fill='none',stroke=c,stroke_width=w,stroke_linecap='round',stroke_linejoin='round',**({'opacity':op} if op else {}),**o)
def E(x,y,rx,ry,c,k=.55,**o):
    a=S(c,k); a.update(o); return ell(x,y,rx,ry,**a)
def C(x,y,r,c,k=.55,**o):
    a=S(c,k); a.update(o); return circ(x,y,r,**a)
def T(svg,x=0,y=0,s=1,r=0,flip=False):
    t=f'translate({f(x)} {f(y)})'+(f' rotate({f(r)})' if r else '')
    if flip: t+=f' scale({f(-s)} {f(s)})'
    elif s!=1: t+=f' scale({f(s)})'
    return g(svg,transform=t)
WOOD='#7A5A43'; WOOD_L='#9C7656'; WOOD_D='#5A4232'; METAL='#9AA3AF'; METAL_D='#5A606C'; GLASS='#BFD8EC'; INK='#22252D'
