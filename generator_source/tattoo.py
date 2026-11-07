"""v3 tattoos. Designs are drawn in a small local frame (~16px tall, 'up' = -y) and
mapped onto limb segments of the rig. Same designs render big for the flash sheet."""
from sv import *
INK='#26304A'; RED='#C0413A'; GRN='#3F7A4A'; YEL='#D9A23B'; BLU='#3E6A9A'; PNK='#D9668A'
def _i(w=1.1,op='.9'): return dict(fill='none',stroke=INK,stroke_width=f(w),stroke_linecap='round',stroke_linejoin='round',opacity=op)
def _c(c,op='.78'): return dict(fill=c,opacity=op)
def rose(k=1):
    s=path('M0 7 Q-1 2 0 -2',**_i(1.1))+path('M0 4 Q-5 1 -6 4 Q-3 6 0 4Z',**_c(GRN))+path('M0 2 Q5 -1 6 2 Q3 4 0 2Z',**_c(GRN))
    s+=path('M-4.6 -5 Q-5 -9.5 0 -9.5 Q5 -9.5 4.6 -5 Q4 -1.6 0 -1.6 Q-4 -1.6 -4.6 -5Z',**_c(RED,'.85'))+path('M-4.6 -5 Q-5 -9.5 0 -9.5 Q5 -9.5 4.6 -5 Q4 -1.6 0 -1.6 Q-4 -1.6 -4.6 -5Z',**_i(.9))
    s+=path('M-2 -6 Q0 -3.6 2 -6 M-3 -4.4 Q0 -2.4 3 -4.4 M-1 -7.6 Q.5 -6 1.6 -7.4',**_i(.7,'.8'))
    return s
def heart(k=1):
    d='M0 6 C-8 0 -7 -7 -3 -7 C-1 -7 0 -5 0 -4 C0 -5 1 -7 3 -7 C7 -7 8 0 0 6Z'
    return path(d,**_c(RED,'.85'))+path(d,**_i(1))+path('M-7 -1 L7 -3 L6 1 L-6 3Z',fill='#EFE3C8',opacity='.85')+path('M-7 -1 L7 -3 L6 1 L-6 3Z',**_i(.7))
def anchor(k=1):
    return path('M0 -7 L0 7 M-4 -3.5 L4 -3.5 M-6 3 Q-5 8 0 8 Q5 8 6 3 M-7 4.2 L-6 3 L-4.6 4.4 M7 4.2 L6 3 L4.6 4.4',**_i(1.2))+circ(0,-8.6,1.6,**_i(1))
def star(k=1):
    pts=[]
    for i in range(10):
        a=(-90+i*36)*D; rr=7 if i%2==0 else 2.9; pts.append([math.cos(a)*rr,math.sin(a)*rr])
    d='M'+'L'.join(P(p) for p in pts)+'Z'
    return path(d,fill=INK,opacity='.82')
def star_outline(k=1):
    pts=[]
    for i in range(10):
        a=(-90+i*36)*D; rr=7 if i%2==0 else 2.9; pts.append([math.cos(a)*rr,math.sin(a)*rr])
    return path('M'+'L'.join(P(p) for p in pts)+'Z',**_i(1))
def swallow(k=1):
    d='M-8 -3 Q-3 -4 0 -1 Q3 -6 9 -7 Q5 -3 3 0 Q6 3 8 7 Q3 4 1 3 Q-1 6 -3 7 L-2 2 Q-6 1 -8 -3Z'
    return path(d,**_c(BLU,'.8'))+path(d,**_i(.9))+path('M-1 -1 Q1 1 1 3',**_i(.7))+circ(-5,-2.6,.6,fill=INK)
def wave(k=1):
    return path('M-6 6 Q-6 -2 1 -6 Q6 -8 6 -3 Q6 0 2 -1 Q-1 -2 0 2 Q1 5 6 6',**_i(1.2))+path('M-7 6 L7 6',**_i(1))+path('M-3 3 Q-3 -1 0 -3',**_i(.7,'.7'))
def moon(k=1): return path('M2 -7 A7 7 0 1 0 2 7 A5.5 5.5 0 1 1 2 -7Z',**_c(YEL,'.8'))+path('M2 -7 A7 7 0 1 0 2 7 A5.5 5.5 0 1 1 2 -7Z',**_i(.9))
def sun(k=1):
    s=circ(0,0,3.6,**_i(1))
    for a in range(0,360,45): s+=line(mul(dirv(a),5.4),mul(dirv(a),8),**_i(1))
    return s
def dagger(k=1):
    return path('M0 -9 L1.6 -2 L1.2 4 L0 5 L-1.2 4 L-1.6 -2Z',fill='#C9CED6',opacity='.8')+path('M0 -9 L1.6 -2 L1.2 4 L0 5 L-1.2 4 L-1.6 -2Z',**_i(.8))+path('M-4 4.5 L4 4.5 M0 4.5 L0 8.5',**_i(1.3))+circ(0,9.6,1,fill=INK)
def compass(k=1):
    s=circ(0,0,6.6,**_i(1))+path('M0 -8.5 L1.6 0 L0 8.5 L-1.6 0Z',fill=INK,opacity='.8')+path('M-8.5 0 L0 1.4 L8.5 0 L0 -1.4Z',**_i(.8))
    return s
def butterfly(k=1):
    s=path('M0 -2 Q-6 -10 -8 -4 Q-8 0 0 0Z M0 -2 Q6 -10 8 -4 Q8 0 0 0Z M0 0 Q-6 2 -6 6 Q-3 7 0 1Z M0 0 Q6 2 6 6 Q3 7 0 1Z',**_c(PNK,'.75'))
    s+=path('M0 -2 Q-6 -10 -8 -4 Q-8 0 0 0Z M0 -2 Q6 -10 8 -4 Q8 0 0 0Z M0 0 Q-6 2 -6 6 Q-3 7 0 1Z M0 0 Q6 2 6 6 Q3 7 0 1Z',**_i(.8))
    return s+path('M0 -4 L0 3 M0 -4 L-2 -7 M0 -4 L2 -7',**_i(.8))
def snake(k=1): return path('M-4 9 Q4 6 0 2 Q-5 -2 1 -5 Q5 -7 2 -9.5',**_i(2.4,'.85'))+path('M-4 9 Q4 6 0 2 Q-5 -2 1 -5 Q5 -7 2 -9.5',fill='none',stroke=GRN,stroke_width='1.1',stroke_linecap='round',opacity='.9')+circ(2.3,-9.6,1.4,fill=INK)
def feather(k=1): return path('M0 9 L0 -9 M0 -6 L-4 -3 M0 -3 L-5 0 M0 0 L-5 3 M0 3 L-4 5.5 M0 -6 L4 -3 M0 -3 L5 0 M0 0 L5 3 M0 3 L4 5.5',**_i(.9))+path('M0 -9 Q-6 -2 -4 6 L0 9 L4 6 Q6 -2 0 -9Z',**_i(.8,'.7'))
def infinity(k=1): return path('M0 0 C-3 -4 -8 -4 -8 0 C-8 4 -3 4 0 0 C3 -4 8 -4 8 0 C8 4 3 4 0 0Z',**_i(1.2))
def script(k=1): return path('M-7 -6 q2 -3 3 0 q1 4 -1 5 M-2 -2 q1 -2 2 0 q1 2 2 0 M3 -2 q1 -3 2 0 l1 2 M-6 4 q3 -3 5 0 q2 3 4 0 q2 -3 4 0',**_i(.9))
def mountain(k=1): return path('M-8 5 L-3 -4 L0 0 L3 -6 L8 5Z',**_i(1))+path('M3 -6 L1.6 -3.4 L3 -2.6 L4.4 -3.4Z',fill=INK,opacity='.8')+circ(-5,-6,1.6,**_i(.8))
def lotus(k=1):
    return path('M0 4 Q-3 -2 0 -7 Q3 -2 0 4Z M0 4 Q-7 1 -7 -4 Q-3 -2 0 4Z M0 4 Q7 1 7 -4 Q3 -2 0 4Z',**_c(PNK,'.7'))+path('M0 4 Q-3 -2 0 -7 Q3 -2 0 4Z M0 4 Q-7 1 -7 -4 Q-3 -2 0 4Z M0 4 Q7 1 7 -4 Q3 -2 0 4Z M-8 5 L8 5',**_i(.8))
def skull(k=1):
    s=path('M-6 0 Q-7 -8 0 -8 Q7 -8 6 0 Q6 3 3 3.5 L3 6 L-3 6 L-3 3.5 Q-6 3 -6 0Z',fill='#EFE3C8',opacity='.85')+path('M-6 0 Q-7 -8 0 -8 Q7 -8 6 0 Q6 3 3 3.5 L3 6 L-3 6 L-3 3.5 Q-6 3 -6 0Z',**_i(.9))
    return s+circ(-2.6,-2,1.7,fill=INK,opacity='.85')+circ(2.6,-2,1.7,fill=INK,opacity='.85')+path('M-1 4 L-1 6 M1 4 L1 6',**_i(.6))
def koi(k=1):
    d='M-2 -8 Q4 -6 3 0 Q2 4 -1 6 L-4 9 L-1 9 L1 6.5 L3 9 L4 8 L1.5 5.5 Q5 1 4 -4 Q2 -9 -2 -8Z'
    return path(d,**_c('#E87A3E','.8'))+path(d,**_i(.8))+circ(0.6,-5.4,.6,fill=INK)
def music(k=1): return path('M-3 6 L-3 -6 L5 -8 L5 4',**_i(1.2))+ell(-5,6,2.4,1.8,fill=INK,opacity='.85')+ell(3,4,2.4,1.8,fill=INK,opacity='.85')
def mandala(k=1):
    s=circ(0,0,2,**_i(.8))+circ(0,0,7,**_i(.8))
    for a in range(0,360,30): s+=path(f'M{P(mul(dirv(a),2.6))}Q{P(mul(dirv(a+15),5))} {P(mul(dirv(a),6.6))}Q{P(mul(dirv(a-15),5))} {P(mul(dirv(a),2.6))}',**_i(.6))
    return s
def tribal(k=1): return path('M-6 -9 Q2 -6 0 -1 Q-2 4 6 9 Q-1 7 -3 1 Q-4 -5 -6 -9Z M3 -9 Q7 -6 5 -3 Q4 -6 3 -9Z',fill=INK,opacity='.85')
def band(k=1,w=11): return path(f'M{-w} -2 L{w} -2 M{-w} 2 L{w} 2',**_i(1.2))+''.join(path(f'M{x} -2 L{x+2} 2',**_i(.8)) for x in range(-w,w,4))
def barcode(k=1): return ''.join(path(f'M{x} -4 L{x} 4',**_i(.5+abs((x*7)%3)*.35)) for x in range(-6,7,2))
DESIGNS=dict(rose=rose,heart=heart,anchor=anchor,star=star,star_outline=star_outline,swallow=swallow,wave=wave,moon=moon,sun=sun,dagger=dagger,compass=compass,butterfly=butterfly,snake=snake,feather=feather,infinity=infinity,script=script,mountain=mountain,lotus=lotus,skull=skull,koi=koi,music=music,mandala=mandala,tribal=tribal,band=band,barcode=barcode)

# --------------------------------------------------------- mapping onto the rig
def parse(lst):
    out=[]
    for t in (lst or []):
        d,_,slot=t.partition('@'); out.append((d,slot or 'forearm_near'))
    return out
def _on_seg(design,A,B,u=.5,sc=1.0,flip=False):
    c=lerp_pt(A,B,u); a=ang(sub(B,A))
    return g(DESIGNS[design](),transform=f'translate({f(c[0])} {f(c[1])}) rotate({f(-a+(180 if flip else 0))}) scale({f(sc)})')
def lerp_pt(a,b,t): return [lerp(a[0],b[0],t),lerp(a[1],b[1],t)]
SLEEVE_SET=['rose','swallow','star','wave','compass','dagger','koi','skull','lotus','snake']
def sleeve(A,J,T,seed=0,w=18):
    """full sleeve: packed motifs + filler shading down the whole arm"""
    s=''
    r_=rnd(seed)
    a1=ang(sub(J,A)); a2=ang(sub(T,J))
    for (P0,P1,us) in ((A,J,(.32,.74)),(J,T,(.28,.66))):
        for u in us:
            d=SLEEVE_SET[r_.randrange(len(SLEEVE_SET))]
            s+=_on_seg(d,P0,P1,u,.82,flip=True)
        # filler: little dots + swirls
        for i in range(5):
            u=r_.uniform(.1,.9); off=r_.uniform(-w*.32,w*.32)
            c=lerp_pt(P0,P1,u); nrm=rot(dirv(ang(sub(P1,P0))),90)
            c=add(c,mul(nrm,off)); s+=circ(c[0],c[1],r_.uniform(.6,1.1),fill=INK,opacity='.6')
    s+=_on_seg('band',J,T,.93,.75)
    return s
def arm(p,S,A,which,armW=19):
    """which: 'near'|'far'.  S shoulder, A = solver dict (J,T)."""
    s=''
    for d,slot in parse(p.get('tattoo')):
        part,_,side=slot.rpartition('_')
        if side!=which: continue
        if d=='sleeve' and part in('arm',''):
            s+=sleeve(S,A['J'],A['T'],seed=3 if which=='near' else 11,w=armW)
        elif part=='upperarm': s+=_on_seg(d,S,A['J'],.66,1.0,flip=True)
        elif part=='forearm': s+=_on_seg(d,A['J'],A['T'],.5,1.0,flip=True)
        elif part=='wrist': s+=_on_seg('band' if d=='band' else d,A['J'],A['T'],.88,.8,flip=True)
    return s
def hand_t(p,palm,h,which):
    s=''
    for d,slot in parse(p.get('tattoo')):
        if slot==f'hand_{which}': s+=g(DESIGNS[d](),transform=f'translate({f(palm[0])} {f(palm[1])}) rotate({f(-h+180)}) scale(.55)')
    return s
def leg(p,H,l,which):
    s=''
    for d,slot in parse(p.get('tattoo')):
        if slot==f'calf_{which}': s+=_on_seg(d,l['J'],l['T'],.42,1.05,flip=True)
        elif slot==f'thigh_{which}': s+=_on_seg(d,H,l['J'],.7,1.05,flip=True)
        elif slot==f'ankle_{which}': s+=_on_seg(d,l['J'],l['T'],.86,.7,flip=True)
    return s
def neck(p,neckpt,head_c):
    s=''
    for d,slot in parse(p.get('tattoo')):
        if slot=='neck': s+=_on_seg(d,neckpt,head_c,.18,.62,flip=True)
    return s
def face(p,cx,sp,view):
    s=''
    for d,slot in parse(p.get('tattoo')):
        if slot=='face':
            x=(cx+sp+3) if view!='front' else 15
            s+=g(DESIGNS[d](),transform=f'translate({f(x)} 9) scale(.32)')
    return s
def flash(d,big=6):
    """standalone flash-sheet version of a design (skin swatch + bold render)"""
    return g(DESIGNS[d](),transform=f'scale({big})')
