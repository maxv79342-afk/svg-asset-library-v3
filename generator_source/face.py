from sv import *
INK='#221E1B'; BROW='#5A5047'; MOUTH='#4A3530'; TONGUE='#D9736B'; TEETH='#FBF8F2'
# ---------- eyes ----------
def eye(kind, ex, ey, sc, lx, ly, side, skin, line):
    """side: +1 = eye nearer the face-direction (right), -1 = other. returns svg"""
    s=''
    rx,ry=4.6*sc,6.4*sc
    cx,cy=ex+lx,ey+ly
    hl=lambda: circ(cx+1.4*sc, cy-2.2*sc, 1.5*sc, fill='#fff', opacity='.9')
    lidline=lambda d: path(d, fill='none', stroke=INK, stroke_width=f(2.4*sc), stroke_linecap='round')
    if kind in ('normal','look'):
        s+=ell(cx,cy,rx,ry,fill=INK)+hl()
    elif kind=='wide':
        s+=ell(cx,cy,rx*1.18,ry*1.2,fill=INK)+hl()+circ(cx-1.6*sc,cy+2.5*sc,.9*sc,fill='#fff',opacity='.7')
    elif kind=='shock':
        s+=ell(ex,ey,7.4*sc,8.6*sc,fill='#fff',stroke=INK,stroke_width=f(2.2*sc))+circ(ex+lx*.6,ey+ly*.6,2.4*sc,fill=INK)
    elif kind=='tiny':
        s+=circ(cx,cy,2.3*sc,fill=INK)
    elif kind=='happy':   # ^ arcs
        s+=lidline(f'M{f(ex-5.5*sc)} {f(ey+2*sc)}Q{f(ex)} {f(ey-7.5*sc)} {f(ex+5.5*sc)} {f(ey+2*sc)}')
    elif kind=='closed':  # relaxed closed (sleep)
        s+=lidline(f'M{f(ex-5.5*sc)} {f(ey)}Q{f(ex)} {f(ey+5*sc)} {f(ex+5.5*sc)} {f(ey)}')
        s+=path(f'M{f(ex-5*sc)} {f(ey+1.5*sc)}l{f(-2*sc)} {f(2*sc)}M{f(ex-2*sc)} {f(ey+3.3*sc)}l{f(-1*sc)} {f(2.4*sc)}',stroke=INK,stroke_width=f(1.4*sc),stroke_linecap='round',opacity='.7') if side<0 else ''
    elif kind=='tight':   # > <
        k=1 if side>0 else -1
        s+=lidline(f'M{f(ex+5*sc*k)} {f(ey-5*sc)}L{f(ex-4*sc*k)} {f(ey)}L{f(ex+5*sc*k)} {f(ey+5*sc)}')
    elif kind=='squint':
        s+=lidline(f'M{f(ex-5.5*sc)} {f(ey)}L{f(ex+5.5*sc)} {f(ey)}')
    elif kind in ('sad','angry','tired','sly','worried'):
        s+=ell(cx,cy,rx,ry,fill=INK)+hl()
        # lid polygon covering top part, tilt
        inner = -side  # direction toward the other eye (x sign)
        if kind=='sad' or kind=='worried':  # outer corner droops: lid low at outer, high at inner
            yo,yi = ey-1.0*sc, ey-6*sc
        elif kind=='angry':
            yo,yi = ey-6*sc, ey-0.5*sc
        elif kind=='tired':
            yo,yi = ey-0.8*sc, ey-0.8*sc
        else: # sly half low flat
            yo,yi = ey+0.6*sc, ey+0.6*sc
        xo,xi = ex - inner*8*sc, ex + inner*8*sc
        d=f'M{f(xo)} {f(yo)}L{f(xi)} {f(yi)}L{f(xi)} {f(ey-14*sc)}L{f(xo)} {f(ey-14*sc)}Z'
        s+=path(d, fill=skin)
        # lid line clipped to eye width
        t0,t1=.3,.7
        a=[lerp(xo,xi,t0),lerp(yo,yi,t0)]; b=[lerp(xo,xi,t1),lerp(yo,yi,t1)]
        s+=lidline(f'M{P(a)}L{P(b)}')
        if kind=='tired':
            s+=path(f'M{f(ex-5*sc)} {f(ey+8.5*sc)}Q{f(ex)} {f(ey+11*sc)} {f(ex+5*sc)} {f(ey+8.5*sc)}', fill='none', stroke='#8E7F92', stroke_width=f(2*sc), stroke_linecap='round', opacity='.75')
    elif kind=='teary':
        s+=ell(cx,cy,rx*1.15,ry*1.12,fill=INK)+circ(cx+1.6*sc,cy-2.6*sc,2.1*sc,fill='#fff')+circ(cx-1.6*sc,cy+2.4*sc,1.1*sc,fill='#fff',opacity='.85')
        s+=path(f'M{f(cx-6*sc)} {f(cy+5*sc)}Q{f(cx)} {f(cy+9.5*sc)} {f(cx+6*sc)} {f(cy+5*sc)}', fill='none', stroke='#8FC9F5', stroke_width=f(2.6*sc), stroke_linecap='round')
    elif kind=='dizzy':
        d='M'+P([ex,ey])
        for i in range(1,26):
            a=i*0.55; r=a*0.95*sc
            d+='L'+P([ex+math.cos(a)*r, ey+math.sin(a)*r])
        s+=path(d, fill='none', stroke=INK, stroke_width=f(1.8*sc), stroke_linecap='round')
    elif kind=='dead':
        s+=path(f'M{f(ex-5*sc)} {f(ey-5*sc)}L{f(ex+5*sc)} {f(ey+5*sc)}M{f(ex+5*sc)} {f(ey-5*sc)}L{f(ex-5*sc)} {f(ey+5*sc)}', stroke=INK, stroke_width=f(2.6*sc), stroke_linecap='round')
    elif kind=='heart':
        k=sc*1.05
        s+=path(f'M{f(ex)} {f(ey+6*k)}C{f(ex-9*k)} {f(ey-1*k)} {f(ex-6*k)} {f(ey-8*k)} {f(ex)} {f(ey-3.5*k)}C{f(ex+6*k)} {f(ey-8*k)} {f(ex+9*k)} {f(ey-1*k)} {f(ex)} {f(ey+6*k)}Z', fill='#E8455A', stroke='#9E2236', stroke_width=f(1.2*sc))
    elif kind=='star':
        pts=[]
        for i in range(10):
            r=(8 if i%2==0 else 3.4)*sc; a=-math.pi/2+i*math.pi/5
            pts.append([ex+math.cos(a)*r, ey+math.sin(a)*r])
        s+=path('M'+'L'.join(P(p) for p in pts)+'Z', fill='#F6C443', stroke='#B8821A', stroke_width=f(1.2*sc), stroke_linejoin='round')
    elif kind=='money':
        s+=text('$',ex,ey+6*sc,size=f(17*sc),fill='#3FA34D',weight=800,anchor='middle')
    elif kind=='glow':
        s+=ell(ex,ey,rx*1.2,ry*1.1,fill='#FFF6C9')+ell(ex,ey,rx*2.2,ry*2,fill='#FFE27A',opacity='.25')
    elif kind=='none':
        pass
    return s
# ---------- brows ----------
BROWS = { # (outer dy, inner dy, arch)
 'neutral':(0,0,2), 'raised':(-4,-5,3), 'high':(-6,-8,3.5), 'angry':(-3,6,0), 'furious':(-4,8,-1),
 'sad':(3,-5,1), 'worried':(2,-6,2.5), 'flat':(1,1,0), 'low':(3,3,1), 'focused':(0,3,0.5), 'none':None,
}
def brow(kind, ex, ey, sc, side, lift=0):
    if kind=='none' or kind is None: return ''
    o,i,arch = BROWS[kind]
    inner=-side
    by=ey-13*sc-lift
    a=[ex-inner*6.2*sc, by+o*sc]; b=[ex+inner*6.2*sc, by+i*sc]
    m=[(a[0]+b[0])/2, (a[1]+b[1])/2-arch*sc]
    return path(f'M{P(a)}Q{P(m)} {P(b)}', fill='none', stroke=BROW, stroke_width=f(3.4*sc), stroke_linecap='round')
# ---------- mouths ----------
def mouth(kind, mx, my, sc, skin):
    k=sc
    st=lambda d,w=3: path(d, fill='none', stroke=MOUTH, stroke_width=f(w*k), stroke_linecap='round', stroke_linejoin='round')
    fl=lambda d: path(d, fill=MOUTH, stroke=MOUTH, stroke_width=f(2*k), stroke_linejoin='round')
    X=lambda v: f(mx+v*k); Y=lambda v: f(my+v*k)
    s=''
    if kind=='neutral': s+=st(f'M{X(-7)} {Y(0)}Q{X(0)} {Y(2.5)} {X(7)} {Y(0)}')
    elif kind=='smile': s+=st(f'M{X(-9)} {Y(-2)}Q{X(0)} {Y(8)} {X(9)} {Y(-2)}')
    elif kind=='softsmile': s+=st(f'M{X(-6)} {Y(0)}Q{X(0)} {Y(4.5)} {X(6)} {Y(0)}')
    elif kind=='grin':
        s+=fl(f'M{X(-11)} {Y(-3)}Q{X(0)} {Y(-1)} {X(11)} {Y(-3)}Q{X(10)} {Y(12)} {X(0)} {Y(12)}Q{X(-10)} {Y(12)} {X(-11)} {Y(-3)}Z')
        s+=path(f'M{X(-9.5)} {Y(-2)}Q{X(0)} {Y(0)} {X(9.5)} {Y(-2)}L{X(9)} {Y(2.4)}Q{X(0)} {Y(3.6)} {X(-9)} {Y(2.4)}Z', fill=TEETH)
        s+=path(f'M{X(-6)} {Y(10.5)}Q{X(0)} {Y(5)} {X(6)} {Y(10.5)}Q{X(0)} {Y(12)} {X(-6)} {Y(10.5)}Z', fill=TONGUE)
    elif kind=='laugh':
        s+=fl(f'M{X(-12)} {Y(-4)}Q{X(0)} {Y(-2)} {X(12)} {Y(-4)}Q{X(11)} {Y(16)} {X(0)} {Y(16)}Q{X(-11)} {Y(16)} {X(-12)} {Y(-4)}Z')
        s+=path(f'M{X(-7)} {Y(14)}Q{X(0)} {Y(6)} {X(7)} {Y(14)}Q{X(0)} {Y(16)} {X(-7)} {Y(14)}Z', fill=TONGUE)
    elif kind=='teeth':  # wide toothy smile
        s+=fl(f'M{X(-11)} {Y(-2)}Q{X(0)} {Y(0)} {X(11)} {Y(-2)}Q{X(8)} {Y(8)} {X(0)} {Y(8)}Q{X(-8)} {Y(8)} {X(-11)} {Y(-2)}Z')
        s+=path(f'M{X(-10)} {Y(-1.6)}Q{X(0)} {Y(.4)} {X(10)} {Y(-1.6)}Q{X(8)} {Y(7)} {X(0)} {Y(7)}Q{X(-8)} {Y(7)} {X(-10)} {Y(-1.6)}Z', fill=TEETH)
        s+=st(f'M{X(-9)} {Y(2.6)}Q{X(0)} {Y(4.2)} {X(9)} {Y(2.6)}',1.2)
    elif kind=='frown': s+=st(f'M{X(-8)} {Y(3)}Q{X(0)} {Y(-5)} {X(8)} {Y(3)}')
    elif kind=='bigfrown': s+=st(f'M{X(-10)} {Y(5)}Q{X(0)} {Y(-7)} {X(10)} {Y(5)}')
    elif kind=='flat': s+=st(f'M{X(-7)} {Y(0)}L{X(7)} {Y(0)}')
    elif kind=='tiny': s+=st(f'M{X(-3)} {Y(0)}L{X(3)} {Y(0)}')
    elif kind=='o': s+=fl(f'M{X(0)} {Y(-4)}C{X(5)} {Y(-4)} {X(5)} {Y(5)} {X(0)} {Y(5)}C{X(-5)} {Y(5)} {X(-5)} {Y(-4)} {X(0)} {Y(-4)}Z')
    elif kind=='O':
        s+=fl(f'M{X(0)} {Y(-6)}C{X(9)} {Y(-6)} {X(9)} {Y(13)} {X(0)} {Y(13)}C{X(-9)} {Y(13)} {X(-9)} {Y(-6)} {X(0)} {Y(-6)}Z')
        s+=path(f'M{X(-5)} {Y(10)}Q{X(0)} {Y(5)} {X(5)} {Y(10)}Q{X(0)} {Y(13)} {X(-5)} {Y(10)}Z', fill=TONGUE)
    elif kind=='shout':
        s+=fl(f'M{X(-12)} {Y(-4)}L{X(12)} {Y(-4)}Q{X(9)} {Y(15)} {X(0)} {Y(15)}Q{X(-9)} {Y(15)} {X(-12)} {Y(-4)}Z')
        s+=path(f'M{X(-11)} {Y(-3.5)}L{X(11)} {Y(-3.5)}L{X(10.4)} {Y(0)}L{X(-10.4)} {Y(0)}Z', fill=TEETH)
        s+=path(f'M{X(-6)} {Y(13)}Q{X(0)} {Y(7)} {X(6)} {Y(13)}Q{X(0)} {Y(15)} {X(-6)} {Y(13)}Z', fill=TONGUE)
    elif kind=='scream':
        s+=fl(f'M{X(0)} {Y(-5)}C{X(9)} {Y(-5)} {X(10)} {Y(20)} {X(0)} {Y(20)}C{X(-10)} {Y(20)} {X(-9)} {Y(-5)} {X(0)} {Y(-5)}Z')
        s+=path(f'M{X(-5)} {Y(17)}Q{X(0)} {Y(11)} {X(5)} {Y(17)}Q{X(0)} {Y(20)} {X(-5)} {Y(17)}Z', fill=TONGUE)
    elif kind=='sadopen':
        s+=fl(f'M{X(-10)} {Y(8)}Q{X(0)} {Y(-6)} {X(10)} {Y(8)}Q{X(0)} {Y(5)} {X(-10)} {Y(8)}Z')
    elif kind=='cry':
        s+=fl(f'M{X(-11)} {Y(10)}Q{X(-8)} {Y(-5)} {X(0)} {Y(-5)}Q{X(8)} {Y(-5)} {X(11)} {Y(10)}Q{X(0)} {Y(7)} {X(-11)} {Y(10)}Z')
        s+=path(f'M{X(-8)} {Y(-2)}Q{X(0)} {Y(-6)} {X(8)} {Y(-2)}L{X(7)} {Y(0)}Q{X(0)} {Y(-3)} {X(-7)} {Y(0)}Z', fill=TEETH)
    elif kind=='wavy': s+=st(f'M{X(-10)} {Y(1)}Q{X(-6.6)} {Y(-3)} {X(-3.3)} {Y(1)}Q{X(0)} {Y(5)} {X(3.3)} {Y(1)}Q{X(6.6)} {Y(-3)} {X(10)} {Y(1)}',2.6)
    elif kind=='grit':
        s+=path(f'M{X(-11)} {Y(-4)}L{X(11)} {Y(-4)}Q{X(12)} {Y(4)} {X(11)} {Y(5)}L{X(-11)} {Y(5)}Q{X(-12)} {Y(4)} {X(-11)} {Y(-4)}Z', fill=TEETH, stroke=MOUTH, stroke_width=f(2.2*k), stroke_linejoin='round')
        s+=st(f'M{X(-11)} {Y(.5)}L{X(11)} {Y(.5)}M{X(-5.5)} {Y(-4)}L{X(-5.5)} {Y(5)}M{X(0)} {Y(-4)}L{X(0)} {Y(5)}M{X(5.5)} {Y(-4)}L{X(5.5)} {Y(5)}',1.4)
    elif kind=='smirk': s+=st(f'M{X(-7)} {Y(1)}Q{X(2)} {Y(3)} {X(9)} {Y(-4)}')
    elif kind=='tongue':
        s+=st(f'M{X(-9)} {Y(-1)}Q{X(0)} {Y(5)} {X(9)} {Y(-1)}')
        s+=path(f'M{X(-1)} {Y(1.8)}Q{X(-1)} {Y(10)} {X(4)} {Y(10)}Q{X(8.5)} {Y(10)} {X(7.5)} {Y(.6)}', fill=TONGUE, stroke=MOUTH, stroke_width=f(2*k), stroke_linejoin='round')
    elif kind=='pout': s+=st(f'M{X(-4)} {Y(1)}Q{X(0)} {Y(-3)} {X(4)} {Y(1)}',3.2)+st(f'M{X(-3)} {Y(3)}Q{X(0)} {Y(5)} {X(3)} {Y(3)}',2)
    elif kind=='yawn':
        s+=fl(f'M{X(0)} {Y(-6)}C{X(8)} {Y(-6)} {X(8)} {Y(18)} {X(0)} {Y(18)}C{X(-8)} {Y(18)} {X(-8)} {Y(-6)} {X(0)} {Y(-6)}Z')
        s+=path(f'M{X(-4.5)} {Y(15)}Q{X(0)} {Y(10)} {X(4.5)} {Y(15)}Q{X(0)} {Y(18)} {X(-4.5)} {Y(15)}Z', fill=TONGUE)
    elif kind=='drool':
        s+=fl(f'M{X(-6)} {Y(0)}Q{X(0)} {Y(-2)} {X(6)} {Y(0)}Q{X(0)} {Y(6)} {X(-6)} {Y(0)}Z')
        s+=path(f'M{X(4)} {Y(2)}q{f(-1*k)} {f(6*k)} {f(1*k)} {f(9*k)}q{f(3*k)} {f(-1*k)} {f(1*k)} {f(-9*k)}Z', fill='#BFE6FF', stroke='#8FC9F5', stroke_width=f(1*k))
    # ---- visemes (Preston Blair) ----
    elif kind=='v_rest': s+=st(f'M{X(-7)} {Y(0)}Q{X(0)} {Y(1.5)} {X(7)} {Y(0)}')
    elif kind=='v_MBP': s+=st(f'M{X(-8)} {Y(0)}L{X(8)} {Y(0)}',3.6)+st(f'M{X(-4)} {Y(3.4)}Q{X(0)} {Y(4.6)} {X(4)} {Y(3.4)}',1.6)
    elif kind=='v_AI':
        s+=fl(f'M{X(-10)} {Y(-3)}Q{X(0)} {Y(-5)} {X(10)} {Y(-3)}Q{X(8)} {Y(14)} {X(0)} {Y(14)}Q{X(-8)} {Y(14)} {X(-10)} {Y(-3)}Z')
        s+=path(f'M{X(-9)} {Y(-2.6)}Q{X(0)} {Y(-4.4)} {X(9)} {Y(-2.6)}L{X(8.6)} {Y(.4)}Q{X(0)} {Y(-1)} {X(-8.6)} {Y(.4)}Z', fill=TEETH)
        s+=path(f'M{X(-5)} {Y(12)}Q{X(0)} {Y(7)} {X(5)} {Y(12)}Q{X(0)} {Y(14)} {X(-5)} {Y(12)}Z', fill=TONGUE)
    elif kind=='v_E':
        s+=fl(f'M{X(-11)} {Y(-2)}Q{X(0)} {Y(-3)} {X(11)} {Y(-2)}Q{X(8)} {Y(7)} {X(0)} {Y(7)}Q{X(-8)} {Y(7)} {X(-11)} {Y(-2)}Z')
        s+=path(f'M{X(-10)} {Y(-1.6)}Q{X(0)} {Y(-2.6)} {X(10)} {Y(-1.6)}L{X(9.4)} {Y(1.4)}Q{X(0)} {Y(.6)} {X(-9.4)} {Y(1.4)}Z', fill=TEETH)
    elif kind=='v_O':
        s+=fl(f'M{X(0)} {Y(-5)}C{X(8)} {Y(-5)} {X(8)} {Y(10)} {X(0)} {Y(10)}C{X(-8)} {Y(10)} {X(-8)} {Y(-5)} {X(0)} {Y(-5)}Z')
        s+=path(f'M{X(-4)} {Y(7.6)}Q{X(0)} {Y(4)} {X(4)} {Y(7.6)}Q{X(0)} {Y(10)} {X(-4)} {Y(7.6)}Z', fill=TONGUE)
    elif kind=='v_U': s+=fl(f'M{X(0)} {Y(-2.6)}C{X(4)} {Y(-2.6)} {X(4)} {Y(4)} {X(0)} {Y(4)}C{X(-4)} {Y(4)} {X(-4)} {Y(-2.6)} {X(0)} {Y(-2.6)}Z')+st(f'M{X(-5.5)} {Y(-3)}Q{X(-7)} {Y(.6)} {X(-5.5)} {Y(4.4)}M{X(5.5)} {Y(-3)}Q{X(7)} {Y(.6)} {X(5.5)} {Y(4.4)}',1.4)
    elif kind=='v_CDG':
        s+=fl(f'M{X(-10)} {Y(-2)}Q{X(0)} {Y(-3)} {X(10)} {Y(-2)}Q{X(7)} {Y(5)} {X(0)} {Y(5)}Q{X(-7)} {Y(5)} {X(-10)} {Y(-2)}Z')
        s+=path(f'M{X(-9.4)} {Y(-1.6)}L{X(9.4)} {Y(-1.6)}L{X(8.6)} {Y(.8)}L{X(-8.6)} {Y(.8)}Z', fill=TEETH)+path(f'M{X(-8.6)} {Y(2.4)}L{X(8.6)} {Y(2.4)}L{X(6)} {Y(4.4)}L{X(-6)} {Y(4.4)}Z', fill=TEETH)
    elif kind=='v_FV':
        s+=fl(f'M{X(-9)} {Y(-2)}Q{X(0)} {Y(-3)} {X(9)} {Y(-2)}Q{X(7)} {Y(4)} {X(0)} {Y(4)}Q{X(-7)} {Y(4)} {X(-9)} {Y(-2)}Z')
        s+=path(f'M{X(-7)} {Y(-1.8)}L{X(7)} {Y(-1.8)}L{X(6.4)} {Y(2.6)}L{X(-6.4)} {Y(2.6)}Z', fill=TEETH)+st(f'M{X(-8)} {Y(3.4)}Q{X(0)} {Y(5.6)} {X(8)} {Y(3.4)}',2.6)
    elif kind=='v_L':
        s+=fl(f'M{X(-9)} {Y(-3)}Q{X(0)} {Y(-4)} {X(9)} {Y(-3)}Q{X(7)} {Y(11)} {X(0)} {Y(11)}Q{X(-7)} {Y(11)} {X(-9)} {Y(-3)}Z')
        s+=path(f'M{X(-8.4)} {Y(-2.6)}L{X(8.4)} {Y(-2.6)}L{X(8)} {Y(-.2)}L{X(-8)} {Y(-.2)}Z', fill=TEETH)+path(f'M{X(-5)} {Y(10)}Q{X(-3)} {Y(1)} {X(0)} {Y(1)}Q{X(3)} {Y(1)} {X(5)} {Y(10)}Z', fill=TONGUE)
    elif kind=='v_WQ':
        s+=fl(f'M{X(0)} {Y(-3.4)}C{X(5.4)} {Y(-3.4)} {X(5.4)} {Y(6)} {X(0)} {Y(6)}C{X(-5.4)} {Y(6)} {X(-5.4)} {Y(-3.4)} {X(0)} {Y(-3.4)}Z')+st(f'M{X(-7)} {Y(-3)}Q{X(-9)} {Y(1.4)} {X(-7)} {Y(6)}M{X(7)} {Y(-3)}Q{X(9)} {Y(1.4)} {X(7)} {Y(6)}',1.6)
    elif kind=='v_TH':
        s+=fl(f'M{X(-9)} {Y(-2)}Q{X(0)} {Y(-3)} {X(9)} {Y(-2)}Q{X(7)} {Y(6)} {X(0)} {Y(6)}Q{X(-7)} {Y(6)} {X(-9)} {Y(-2)}Z')
        s+=path(f'M{X(-7.6)} {Y(-1.6)}L{X(7.6)} {Y(-1.6)}L{X(7)} {Y(.6)}L{X(-7)} {Y(.6)}Z', fill=TEETH)+path(f'M{X(-4.6)} {Y(4.2)}Q{X(0)} {Y(.4)} {X(4.6)} {Y(4.2)}Q{X(0)} {Y(6.4)} {X(-4.6)} {Y(4.2)}Z', fill=TONGUE)
    return s
# ---------- extras ----------
def extras(lst, cx, sp, sc, r, skin):
    s=''
    for e in lst:
        if e=='blush':
            s+=ell(cx-sp-4,8,6.5,3.6,fill='#E58F7A',opacity='.5')+ell(cx+sp+4,8,6.5,3.6,fill='#E58F7A',opacity='.5')
        elif e=='tears':
            for xx in (cx-sp, cx+sp):
                s+=path(f'M{f(xx-2)} 3 Q{f(xx-5)} 18 {f(xx-2)} 34 L{f(xx+2)} 34 Q{f(xx+1)} 18 {f(xx+3)} 3Z', fill='#9FD3FF', opacity='.85')
        elif e=='tear':
            xx=cx-sp
            s+=path(f'M{f(xx-1)} 6 q-4 7 0 10 q4 -3 0 -10Z', fill='#9FD3FF', stroke='#6FB2E6', stroke_width='1')
        elif e=='sweat':
            s+=path(f'M{f(cx+sp+13)} -22 q-6 10 0 14 q6 -4 0 -14Z', fill='#CDEBFF', stroke='#7FBDE8', stroke_width='1.4')
        elif e=='sweats':
            for (xx,yy,k) in ((cx+sp+14,-24,1),(cx-sp-15,-16,.75)):
                s+=g(path('M0 0 q-6 10 0 14 q6 -4 0 -14Z', fill='#CDEBFF', stroke='#7FBDE8', stroke_width='1.4'), transform=f'translate({f(xx)} {f(yy)}) scale({k})')
        elif e=='gloom':
            for i in range(5):
                xx=cx-14+i*7
                s+=path(f'M{f(xx)} {f(-r*.82)}L{f(xx)} {f(-r*.82+12+(i%2)*6)}', stroke='#6C7FA8', stroke_width='2.2', stroke_linecap='round', opacity='.8')
        elif e=='vein':
            x0,y0=cx+sp+10,-r*.62
            s+=g(path('M-7 -2 Q-2 -2 -2 -7 M2 -7 Q2 -2 7 -2 M7 2 Q2 2 2 7 M-2 7 Q-2 2 -7 2', fill='none', stroke='#D6453A', stroke_width='2.6', stroke_linecap='round'), transform=f'translate({f(x0)} {f(y0)})')
        elif e=='bags':
            for xx in (cx-sp, cx+sp):
                s+=path(f'M{f(xx-5)} 5.5 Q{f(xx)} 9 {f(xx+5)} 5.5', fill='none', stroke='#8E7F92', stroke_width='2', stroke_linecap='round', opacity='.7')
        elif e=='pale':
            s+=path(f'M{f(-r)} {f(-r*.2)} A{f(r)} {f(r)} 0 0 1 {f(r)} {f(-r*.2)} L{f(r)} {f(-r*.05)} Q0 {f(-r*.3)} {f(-r)} {f(-r*.05)}Z', fill='#7E9BC2', opacity='.35')
            for i in range(4):
                xx=cx-12+i*8
                s+=path(f'M{f(xx)} {f(-r*.78)}L{f(xx)} {f(-r*.5)}', stroke='#4E6A96', stroke_width='2', stroke_linecap='round', opacity='.7')
        elif e=='sick':
            s+=path(f'M{f(-r)} 0 A{f(r)} {f(r)} 0 0 1 {f(r)} 0 Q0 -10 {f(-r)} 0Z', fill='#8DBF6A', opacity='.4')
        elif e=='sparkle':
            for (xx,yy,k) in ((cx+sp+16,-26,1),(cx-sp-14,-30,.6)):
                s+=g(path('M0 -8 Q1 -1 8 0 Q1 1 0 8 Q-1 1 -8 0 Q-1 -1 0 -8Z', fill='#FFE07A'), transform=f'translate({f(xx)} {f(yy)}) scale({k})')
        elif e=='snot':
            s+=path(f'M{f(cx+2)} 6 q-2 6 1 9 q3 -2 1 -9Z', fill='#CDEFD0', opacity='.9')
    return s

# --------- expression presets ---------
# (eyeL, eyeR, brow, mouth, extras, look)
EXPR = {
 'neutral':      ('normal','normal','neutral','neutral',[],(0,0)),
 'happy':        ('normal','normal','raised','smile',[],(0,0)),
 'joy':          ('happy','happy','raised','grin',['blush'],(0,0)),
 'laugh':        ('tight','tight','high','laugh',['blush'],(0,-.3)),
 'excited':      ('star','star','high','grin',['blush'],(0,0)),
 'in_love':      ('heart','heart','raised','smile',['blush'],(0,0)),
 'content':      ('closed','closed','neutral','softsmile',['blush'],(0,0)),
 'proud':        ('sly','sly','raised','smirk',[],(0,0)),
 'smug':         ('sly','sly','flat','smirk',[],(.6,0)),
 'wink':         ('normal','happy','raised','tongue',[],(0,0)),
 'sad':          ('sad','sad','sad','frown',[],(0,.4)),
 'very_sad':     ('teary','teary','worried','sadopen',['tear'],(0,.3)),
 'crying':       ('tight','tight','worried','cry',['tears'],(0,0)),
 'sobbing':      ('closed','closed','worried','sadopen',['tears','blush'],(0,0)),
 'depressed':    ('tired','tired','sad','flat',['bags','gloom'],(0,.6)),
 'lonely':       ('sad','sad','worried','tiny',[],(-.6,.5)),
 'angry':        ('angry','angry','angry','frown',[],(0,0)),
 'furious':      ('angry','angry','furious','grit',['vein'],(0,0)),
 'yelling':      ('angry','angry','furious','shout',['vein'],(0,0)),
 'annoyed':      ('sly','sly','flat','flat',[],(.7,0)),
 'disgusted':    ('angry','sly','angry','wavy',['sick'],(0,0)),
 'surprised':    ('wide','wide','high','o',[],(0,0)),
 'shocked':      ('shock','shock','high','O',[],(0,0)),
 'terrified':    ('shock','shock','worried','scream',['pale','sweats'],(0,0)),
 'scared':       ('wide','wide','worried','wavy',['sweat'],(-.4,0)),
 'anxious':      ('normal','normal','worried','wavy',['sweats'],(.6,-.2)),
 'nervous':      ('wide','wide','worried','teeth',['sweat'],(.7,0)),
 'embarrassed':  ('tight','tight','worried','wavy',['blush','sweat'],(0,0)),
 'shy':          ('normal','normal','worried','softsmile',['blush'],(-.6,.6)),
 'confused':     ('normal','tiny','raised','wavy',[],(.3,-.4)),
 'thinking':     ('normal','normal','focused','flat',[],(.6,-.7)),
 'skeptical':    ('sly','normal','raised','flat',[],(0,0)),
 'determined':   ('angry','angry','focused','smile',[],(0,0)),
 'focused':      ('normal','normal','focused','tiny',[],(.5,.2)),
 'bored':        ('tired','tired','flat','flat',[],(.4,0)),
 'tired':        ('tired','tired','sad','tiny',['bags'],(0,.4)),
 'sleepy':       ('closed','closed','sad','yawn',['bags'],(0,0)),
 'sleeping':     ('closed','closed','neutral','drool',[],(0,0)),
 'dizzy':        ('dizzy','dizzy','worried','wavy',[],(0,0)),
 'dead_inside':  ('tiny','tiny','flat','flat',['gloom'],(0,0)),
 'knocked_out':  ('dead','dead','none','O',[],(0,0)),
 'greedy':       ('money','money','raised','teeth',[],(0,0)),
 'sick':         ('tired','tired','worried','wavy',['sick','sweat'],(0,0)),
 'hopeful':      ('teary','teary','worried','softsmile',[],(.2,-.6)),
 'relieved':     ('closed','closed','sad','smile',['sweat'],(0,0)),
 'jealous':      ('sly','sly','angry','pout',[],(.8,0)),
 'evil':         ('angry','angry','furious','teeth',[],(0,0)),
 'awkward':      ('normal','normal','flat','teeth',['sweat'],(-.7,0)),
}
VISEMES=['v_rest','v_MBP','v_AI','v_E','v_O','v_U','v_CDG','v_FV','v_L','v_WQ','v_TH']
VISEME_LABEL={'v_rest':'Rest','v_MBP':'M B P','v_AI':'A I','v_E':'E','v_O':'O','v_U':'U','v_CDG':'C D G K N S T','v_FV':'F V','v_L':'L','v_WQ':'W Q','v_TH':'TH'}
