from sv import *
import face as FX
import acc as AC
import tattoo as TT
import acc2 as AC2
OW=2.6
SKINS={'cream':('#ECE4D6','#8C8273'),'warm':('#F2D3B8','#9C7A62'),'tan':('#D9A877','#8A6340'),'brown':('#A8714A','#5E3B22'),'deep':('#6E4630','#3A2216'),'shadow':('#2A2733','#121118')}
HANDS={'open':0,'relax':.35,'grip':.72,'fist':1,'point':'point','flat':-.05,'claw':.55,'thumb':'thumb','peace':'peace','spread':'spread'}

def base_pose(**o):
    p=dict(x=0,y=0,s=1,face=1,rot=0,view='side',lean=0,curl=0,head=0,
           aN=[8,14],aF=[-8,16],wN=0,wF=0,hN='relax',hF='relax',
           lN=[3,3],lF=[-3,3],fN=0,fF=0,ikN=None,ikF=None,legIkN=None,legIkF=None,
           expr='neutral',look=None,turn=.15,eyes=None,brow=None,mouth=None,fx=None,
           armW=19,legW=23,torsoW=54,torsoL=104,headR=39,L1=60,L2=54,L3=72,L4=68,muscle=0,belly=0,
           skin='cream',hair=None,hairCol='#3a2a22',outfit=None,holdN=None,holdF=None,extra='',back=False,
           shadow=True, beard=None, glasses=None, acc=None, mid=None)
    p.update(o); return p

def solve2(S,T,L1,L2,bend):
    v=sub(T,S); d=vlen(v)
    mx=L1+L2-.01; mn=abs(L1-L2)+2
    if d>mx: v=mul(v,mx/d); d=mx
    if d<mn: v=[0,mn] if d<1e-3 else mul(v,mn/d); d=mn
    base=ang(v)
    A=math.acos(clamp((L1*L1+d*d-L2*L2)/(2*L1*d),-1,1))/D
    ua=base-bend*A
    J=add(S,mul(dirv(ua),L1)); Tt=add(S,v)
    return dict(J=J,T=Tt,ua=ua,la=ang(sub(Tt,J)))
def fk(S,a,b,L1,L2,sign):
    J=add(S,mul(dirv(a),L1)); la=a+sign*b
    return dict(J=J,T=add(J,mul(dirv(la),L2)),ua=a,la=la)

class Layer:
    """unified-outline primitive group"""
    def __init__(s, lc): s.o=''; s.f=''; s.lc=lc
    def st(s,d,w,col,od=None,ocap=None,cap='round',noOut=False):
        if not noOut: s.o+=path(od or d,fill='none',stroke=s.lc,stroke_width=f(w+2*OW),stroke_linecap=ocap or cap,stroke_linejoin='round')
        s.f+=path(d,fill='none',stroke=col,stroke_width=f(w),stroke_linecap=cap,stroke_linejoin='round')
    def fill(s,d,col,noOut=False):
        if not noOut: s.o+=path(d,fill=s.lc,stroke=s.lc,stroke_width=f(2*OW),stroke_linejoin='round')
        s.f+=path(d,fill=col)
    def c(s,x,y,r,col):
        s.o+=circ(x,y,r+OW,fill=s.lc); s.f+=circ(x,y,r,fill=col)
    def e(s,x,y,rx,ry,a,col):
        t=f'rotate({f(a)} {f(x)} {f(y)})'
        s.o+=ell(x,y,rx+OW,ry+OW,fill=s.lc,transform=t); s.f+=ell(x,y,rx,ry,fill=col,transform=t)
    def raw(s,svg): s.f+=svg
    def out(s): return s.o+s.f

# ---------- v3 hand system: every hand is a numeric spec, so shapes can be blended frame by frame ----------
def lerp_pt(a,b,t): return [lerp(a[0],b[0],t),lerp(a[1],b[1],t)]
FX_=[-6.6,-2.2,2.2,6.4]; FL_=[11,13.5,13,11]   # finger order: 0 pinky, 1 ring, 2 index, 3 middle (thumb side = +x)
def _legacy_spec(typ):
    c=_LEG.get(typ,.35)
    if c=='point': curls=[1,1,0,1]
    elif c=='thumb': curls=[1,1,1,1]
    elif c=='peace': curls=[1,1,-.1,-.1]
    elif c=='spread': curls=[-.25,-.12,-.05,0]
    else: curls=[c]*4
    spread=[(i-1.5)*(10 if c=='spread' else 6 if c=='peace' and curls[i]<0 else (5 if curls[i]<.3 else 1.5)) for i in range(4)]
    if c=='thumb': tb=[4,8]; tm=[4,-2]; tt=[3.5,-11]
    else:
        tb=[5.5,6]; cc=0 if c in('point','peace','spread') else c
        if c=='spread': tm=[13,2]; tt=[19,-1]
        else: tm=add(tb,rot([0,7],-55-cc*20)); tt=add(tm,rot([0,6.5],-25-cc*50))
    return dict(curls=curls,spread=spread,tb=tb,tm=tm,tt=tt)
_LEG={'open':0,'relax':.35,'grip':.72,'fist':1,'point':'point','flat':-.05,'claw':.55,'thumb':'thumb','peace':'peace','spread':'spread'}
def _tip(spec,i):
    cc=spec['curls'][i]; sp=spec['spread'][i]; b=[FX_[i]*.95,17]
    Ln=FL_[i]*(1-.25*max(0,cc)); mid=add(b,rot([0,Ln*.55],-cc*55+sp)); return b,mid,add(mid,rot([0,Ln*.5],-cc*125+sp))
def mk_hand(curls,thumb=.35,spread=None):
    sp=spread or [(i-1.5)*(5 if curls[i]<.3 else 1.5) for i in range(4)]
    s=dict(curls=list(curls),spread=list(sp),tb=[5.5,6])
    tb=s['tb']
    if thumb=='up': s.update(tb=[4,8],tm=[4,-2],tt=[3.5,-11])
    elif thumb=='out': s.update(tm=[13,2],tt=[19,-1])
    elif thumb=='side': s.update(tm=[11,8],tt=[16,12])
    elif thumb=='tuck': s.update(tm=[3,13],tt=[-3,15])
    elif thumb=='touch':
        _,_,t=_tip(s,2); s['tt']=add(t,[1.5,-.5]); s['tm']=add(lerp_pt(tb,s['tt'],.5),[5,-1])
    elif thumb=='touch_mid':
        _,_,t=_tip(s,3); s['tt']=add(t,[1.5,-.5]); s['tm']=add(lerp_pt(tb,s['tt'],.5),[5,-1])
    else:
        cc=float(thumb); s['tm']=add(tb,rot([0,7],-55-cc*20)); s['tt']=add(s['tm'],rot([0,6.5],-25-cc*50))
    return s
HAND_SPEC={k:_legacy_spec(k) for k in _LEG}
HAND_SPEC.update({
 'ok':        mk_hand([-.05,-.08,.82,.05],'touch',[-9,-4,2,4]),
 'pinch':     mk_hand([.95,.9,.55,.85],'touch'),
 'rock':      mk_hand([-.08,1,-.08,1],1,[-8,0,4,0]),
 'call_me':   mk_hand([-.1,1,1,1],'out',[-10,0,0,0]),
 'love_you':  mk_hand([-.08,1,-.08,1],'out',[-8,0,4,0]),
 'finger_gun':dict(mk_hand([1,1,0,.05],.3,[0,0,2,3]),tm=[11,6],tt=[15,1]),
 'count_1':   mk_hand([1,1,-.05,1],'tuck',[0,0,0,0]),
 'count_2':   mk_hand([1,1,-.05,-.05],'tuck',[0,0,-3,5]),
 'count_3':   mk_hand([1,-.05,-.05,-.05],'tuck',[0,-6,0,6]),
 'count_4':   mk_hand([-.05,-.05,-.05,-.05],'tuck',[-9,-4,2,8]),
 'count_5':   mk_hand([-.15,-.1,-.05,0],'out',[-14,-6,3,10]),
 'beckon':    mk_hand([1,1,.62,1],.9),
 'pen_grip':  mk_hand([.9,.85,.42,.6],'touch'),
 'cup':       mk_hand([.42,.42,.42,.42],.45,[-2,-.7,.7,2]),
 'karate':    mk_hand([-.02,-.02,-.02,-.02],'side',[-1,-.4,.4,1]),
 'grab':      mk_hand([.85,.8,.75,.8],.75,[-4,-1.5,1.5,4]),
 'wave_a':    mk_hand([-.25,-.15,-.05,0],'out',[-14,-6,4,12]),
 'wave_b':    mk_hand([-.05,.05,.08,.12],'out',[-6,-2,1,4]),
 'knock':     mk_hand([1,1,1,1],1.1),
 'relax_hang':mk_hand([.45,.4,.3,.38],.4,[-3,-1,1,3]),
 'tap':       mk_hand([.9,.85,.12,.8],.7),
 'shh':       mk_hand([1,1,-.04,1],.95,[0,0,0,0]),
})
HANDS={k:k for k in HAND_SPEC}  # kept for build loops / backwards compat
def hand_lerp(a,b,t):
    A=HAND_SPEC[a] if isinstance(a,str) else a; B=HAND_SPEC[b] if isinstance(b,str) else b
    L_=lambda x,y: [lerp(x[i],y[i],t) for i in range(len(x))]
    return dict(curls=L_(A['curls'],B['curls']),spread=L_(A['spread'],B['spread']),tb=L_(A['tb'],B['tb']),tm=L_(A['tm'],B['tm']),tt=L_(A['tt'],B['tt']))
def hand(L,W,h,typ,skin,sc=1,mirror=1,noThumb=False):
    spec=typ if isinstance(typ,dict) else HAND_SPEC.get(typ,HAND_SPEC['relax'])
    R=lambda p: add(W,rot([p[0]*sc*mirror,p[1]*sc],-h))
    pc=R([1,10]); L.e(pc[0],pc[1],10.2*sc,11.6*sc,-h,skin)
    tips=[]; ds=[]
    for i in range(4):
        b,mid,tip=_tip(spec,i); tips.append(R(tip))
        d='M'+P(R(b))+'Q'+P(R(mid))+' '+P(R(tip)); ds.append(d)
        L.st(d,5.7*sc,skin)
    # v3: per-finger contour so fingers read separately (drawn in fill pass, over the palm)
    order=[0,1,3,2] if mirror>0 else [3,2,0,1]
    for i in order:
        L.f+=path(ds[i],fill='none',stroke=L.lc,stroke_width=f(5.7*sc+1.5*sc),stroke_linecap='round',opacity='.75')+path(ds[i],fill='none',stroke=skin,stroke_width=f(5.7*sc-.4*sc),stroke_linecap='round')
    if not noThumb:
        td='M'+P(R(spec['tb']))+'Q'+P(R(spec['tm']))+' '+P(R(spec['tt']))
        L.st(td,6.4*sc,skin)
        L.f+=path(td,fill='none',stroke=L.lc,stroke_width=f(6.4*sc+1.5*sc),stroke_linecap='round',opacity='.75')+path(td,fill='none',stroke=skin,stroke_width=f(6.4*sc-.4*sc),stroke_linecap='round')
        L.f+=ell(pc[0],pc[1],7.4*sc,8.6*sc,fill=skin,transform=f'rotate({f(-h)} {f(pc[0])} {f(pc[1])})') if False else ''
    return dict(tips=tips,palm=pc)

def bentD(S,J,T,soft=.24):
    """limb path with a softened (rubber-hose) elbow/knee instead of a hard corner"""
    a=sub(S,J); b=sub(T,J); la=vlen(a); lb=vlen(b)
    if la<1e-3 or lb<1e-3: return 'M'+P(S)+'L'+P(J)+'L'+P(T)
    cosang=(a[0]*b[0]+a[1]*b[1])/(la*lb)
    bend=clamp((cosang+1)/1.0,0,1)          # 0 straight .. 1 = 90deg+
    k=min(la,lb)*soft*min(1,bend*1.6)
    if k<.6: return 'M'+P(S)+'L'+P(J)+'L'+P(T)
    J1=add(J,mul(a,k/la)); J2=add(J,mul(b,k/lb))
    return 'M'+P(S)+'L'+P(J1)+'Q'+P(J)+' '+P(J2)+'L'+P(T)

def shoe(A,fd,col,sole='#F4EFE6',sc=1,mirror=1,style='sneaker',skin=None):
    th=90-fd
    if style!='sneaker': return shoe_v3(A,fd,col,sole,sc,mirror,style,skin)
    body='M-11 -5 C-12 -14 -2 -16 4 -14 L14 -12 C22 -10 30 -7 36 -1 C39 2 38 7 35 8 L-9 8 C-13 8 -13 2 -11 -5Z'
    ln=dark(col,.6)
    return g(path(body,fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')+
             path('M-11 4 L36 4 C38 5 37 8 35 9 L-9 9 C-12 9 -12 6 -11 4Z',fill=sole,stroke=ln,stroke_width='1.6')+
             path('M6 -11 L10 -4 M11 -11 L15 -5 M16 -10 L19 -5',stroke=sole,stroke_width='2',stroke_linecap='round'),
             transform=f'translate({f(A[0])} {f(A[1])}) rotate({f(th)}) scale({f(sc*mirror)} {f(sc)})')
def shoe_v3(A,fd,col,sole,sc,mirror,style,skin):
    th=90-fd; ln=dark(col,.6); s=''
    if style=='boot':
        s+=path('M-12 -30 L10 -30 L12 -13 L18 -11 C28 -8 35 -4 37 1 C38 5 36 8 34 8 L-10 8 C-14 8 -14 2 -12 -6Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')
        s+=path('M-11 3 L36 3 C37 5 36 9 34 9.5 L-10 9.5 C-13 9.5 -13 6 -11 3Z',fill=sole,stroke=ln,stroke_width='1.6')
        s+=path('M-11 -24 L10 -24',stroke=light(col,.25),stroke_width='2.2',stroke_linecap='round',opacity='.7')+path('M2 -27 L6 -17 M-2 -27 L2 -17',stroke=dark(col,.3),stroke_width='1.6',opacity='.8')
    elif style=='heel':
        s+=path('M-10 -6 C-10 -13 0 -14 6 -11 L16 -6 C24 -2 31 1 34 4 C35 6 34 8 32 8 L8 8 L-2 2 L-6 8 L-9 8 Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')
        s+=path('M-9 2 L-10 14 L-6.5 14 L-5 3Z',fill=dark(col,.25),stroke=ln,stroke_width='1.4',stroke_linejoin='round')
        s+=path('M8 -8 Q16 -6 24 -1',fill='none',stroke=light(col,.35),stroke_width='1.8',stroke_linecap='round',opacity='.7')
    elif style=='dress':
        s+=path('M-11 -6 C-12 -13 -2 -14 4 -12 L14 -10 C24 -8 32 -4 36 0 C38 3 37 7 34 7 L-9 7 C-13 7 -13 1 -11 -6Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')
        s+=path('M-11 4.5 L36 4.5 C37 6 36 8.6 34 8.8 L-9 8.8 C-12 8.8 -12 6 -11 4.5Z',fill=sole,stroke=ln,stroke_width='1.4')
        s+=path('M14 -7 Q24 -5 31 -1',fill='none',stroke='#fff',stroke_width='2',stroke_linecap='round',opacity='.35')
    elif style=='sandal':
        sk=skin or '#ECE4D6'; sl=dark(sk,.45)
        s+=path('M-10 -4 C-11 -12 0 -12 6 -10 L18 -7 C27 -5 33 -2 35 2 C36 5 34 6 32 6 L-8 6 C-12 6 -12 2 -10 -4Z',fill=sk,stroke=sl,stroke_width='2',stroke_linejoin='round')
        s+=path('M-11 5 L36 5 C37 7 36 9 34 9 L-9 9 C-12 9 -12 7 -11 5Z',fill=col,stroke=ln,stroke_width='1.4')
        s+=path('M10 -9 L14 5 M-4 -10 L-2 5',stroke=col,stroke_width='3.4',stroke_linecap='round')
        for x in (24,28.5,32): s+=circ(x,1.5,1.6,fill=light(sk,.15),stroke=sl,stroke_width='.8')
    elif style=='slipper':
        s+=path('M-11 -3 C-12 -11 0 -13 8 -11 L20 -8 C29 -6 35 -2 36 2 C37 6 35 8 33 8 L-9 8 C-13 8 -13 3 -11 -3Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')
        s+=path('M8 -11 C18 -12 30 -6 36 2',fill='none',stroke=light(col,.4),stroke_width='5',stroke_linecap='round',opacity='.8')
        s+=path('M-11 5 L36 5 L35 9 L-9 9Z',fill=sole,stroke=ln,stroke_width='1.2')
    elif style=='flat':
        s+=path('M-10 -4 C-11 -11 0 -12 6 -10 L18 -7 C27 -5 33 -2 35 2 C36 5 34 7 32 7 L-8 7 C-12 7 -12 2 -10 -4Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')
        s+=path('M-11 5.5 L35 5.5 L34 8.6 L-9 8.6Z',fill=sole,stroke=ln,stroke_width='1.2')+circ(16,-5,2.2,fill=light(col,.4))
    else:  # high-top
        s+=path('M-12 -24 L8 -24 L10 -13 L16 -12 C24 -10 31 -6 36 -1 C39 2 38 7 35 8 L-9 8 C-13 8 -14 2 -12 -6Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')
        s+=path('M-11 4 L36 4 C38 5 37 8 35 9 L-9 9 C-12 9 -12 6 -11 4Z',fill=sole,stroke=ln,stroke_width='1.6')+circ(-4,-14,4,fill='#F4EFE6',stroke=ln,stroke_width='1.2')
        s+=path('M2 -21 L6 -14 M4 -17 L9 -10',stroke=sole,stroke_width='2',stroke_linecap='round')
    return g(s,transform=f'translate({f(A[0])} {f(A[1])}) rotate({f(th)}) scale({f(sc*mirror)} {f(sc)})')
def shoe_front(A,col,sole='#F4EFE6',mirror=1,style='sneaker',skin=None):
    ln=dark(col,.6)
    if style=='boot':
        return g(path('M-12 -26 L12 -26 L13 6 L-13 6Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')+path('M-12 -20 L12 -20',stroke=light(col,.25),stroke_width='2')+rect(-14,4,28,7,rx=3,fill=sole,stroke=ln,stroke_width='1.6'),transform=f'translate({f(A[0])} {f(A[1])})')
    if style=='heel':
        return g(path('M-9 -6 C-9 -12 9 -12 9 -6 L10 6 L-10 6Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')+rect(-3,5,6,9,rx=1.5,fill=dark(col,.25),stroke=ln,stroke_width='1.2'),transform=f'translate({f(A[0])} {f(A[1])})')
    if style=='sandal':
        sk=skin or '#ECE4D6'
        return g(path('M-11 -6 C-11 -13 11 -13 11 -6 L12 5 L-12 5Z',fill=sk,stroke=dark(sk,.45),stroke_width='2',stroke_linejoin='round')+path('M-11 -3 L11 -3',stroke=col,stroke_width='4')+rect(-13,4,26,5,rx=2.5,fill=col,stroke=ln,stroke_width='1.4'),transform=f'translate({f(A[0])} {f(A[1])})')
    if style=='slipper':
        return g(ell(0,-2,13,9,fill=col,stroke=ln,stroke_width='2')+ell(0,-6,9,4,fill=light(col,.4),opacity='.8')+rect(-14,4,28,5,rx=2.5,fill=sole,stroke=ln,stroke_width='1.2'),transform=f'translate({f(A[0])} {f(A[1])})')
    if style=='hightop':
        return g(path('M-12 -22 L12 -22 L13 6 L-13 6Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')+rect(-14,4,28,6,rx=3,fill=sole,stroke=ln,stroke_width='1.6')+path('M-5 -18 L5 -14 M-5 -12 L5 -8',stroke=sole,stroke_width='2'),transform=f'translate({f(A[0])} {f(A[1])})')
    return g(path('M-12 -6 C-12 -14 12 -14 12 -6 L13 6 L-13 6Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')+rect(-14,4,28,6,rx=3,fill=sole,stroke=ln,stroke_width='1.6'),transform=f'translate({f(A[0])} {f(A[1])})')
def _old_shoe_front(A,col,sole='#F4EFE6',mirror=1):
    ln=dark(col,.6)
    return g(path('M-12 -6 C-12 -14 12 -14 12 -6 L13 6 L-13 6Z',fill=col,stroke=ln,stroke_width='2',stroke_linejoin='round')+rect(-14,4,28,6,rx=3,fill=sole,stroke=ln,stroke_width='1.6'),transform=f'translate({f(A[0])} {f(A[1])})')

# ---------------- hair ----------------
def hair_paths(style,r,view,col):
    """returns (back_svg, front_svg) in head-local coords (facing +x)"""
    ln=dark(col,.55)
    st=dict(fill=col,stroke=ln,stroke_width='2.2',stroke_linejoin='round')
    hl=lambda d: path(d,fill='none',stroke=light(col,.25),stroke_width='2.5',stroke_linecap='round',opacity='.55')
    def arc(a0,a1,rr,n=24,cx=0,cy=0,bump=0):
        pts=[]
        for i in range(n+1):
            a=lerp(a0,a1,i/n)*D; k=rr+(bump*(1 if i%2==0 else -0.2) if bump else 0)
            pts.append([cx+math.cos(a)*k, cy+math.sin(a)*k])
        return pts
    B=F=''
    if style is None or style=='bald': return '',''
    if style in HAIR_V3: return _hair_v3(style,r,view,col)
    side = view=='side'; front=view=='front'; backv=view=='back'
    if style in('short','bun','ponytail','long','curly','spiky','buzz','bob','afro','pigtails'):
        rr=r+3.5 if style!='buzz' else r+1.2
        if backv:
            pts=arc(150,390,rr,28,bump=4 if style in('curly','afro') else 0)
            low = r*.35 if style!='buzz' else r*.2
            d=smooth(pts,False)+f'L{P([math.cos(390*D)*r*.98,low])}Q0 {f(low+6)} {P([math.cos(150*D)*r*.98,low])}Z'
            F+=path(d,**st)+hl(f'M{f(-r*.4)} {f(-r*.75)}Q0 {f(-r*.9)} {f(r*.35)} {f(-r*.8)}')
        elif front:
            pts=arc(165,375,rr,26,bump=4 if style in('curly','afro') else 0)
            if style=='spiky':
                pts=[]
                for i in range(15):
                    a=lerp(165,375,i/14)*D; k=rr+(9 if i%2 else 0)
                    pts.append([math.cos(a)*k, math.sin(a)*k])
            hlY=-r*.48
            d=('M'+'L'.join(P(p) for p in pts) if style=='spiky' else smooth(pts,False))
            d+=f'L{P([r*.92,-r*.3])}Q{f(r*.55)} {f(hlY-2)} {f(r*.1)} {f(hlY-6)}Q{f(-r*.3)} {f(hlY+4)} {f(-r*.8)} {f(-r*.12)}Q{f(-r*.95)} {f(-r*.2)} {P(pts[0])}Z'
            F+=path(d,**st)+hl(f'M{f(-r*.45)} {f(-r*.78)}Q{f(-r*.1)} {f(-r*.95)} {f(r*.3)} {f(-r*.85)}')
        else:
            a0,a1=(150,338)
            pts=arc(a0,a1,rr,26,bump=4 if style in('curly','afro') else 0)
            if style=='spiky':
                pts=[]
                for i in range(15):
                    a=lerp(a0,a1,i/14)*D; k=rr+(9 if i%2 else 0)
                    pts.append([math.cos(a)*k-(3 if i%2 else 0), math.sin(a)*k])
            d=('M'+'L'.join(P(p) for p in pts) if style=='spiky' else smooth(pts,False))
            # fringe to front then hairline back and down to nape
            fy=-r*.52
            d+=f'Q{f(r*.62)} {f(fy+6)} {f(r*.42)} {f(fy+2)}Q{f(r*.15)} {f(fy-2)} {f(-r*.05)} {f(fy+2)}Q{f(-r*.45)} {f(-r*.1)} {f(-r*.5)} {f(r*.3)}Q{f(-r*.75)} {f(r*.45)} {P(pts[0])}Z'
            F+=path(d,**st)+hl(f'M{f(-r*.55)} {f(-r*.6)}Q{f(-r*.25)} {f(-r*.92)} {f(r*.2)} {f(-r*.88)}')
            if style!='buzz': F+=path(f'M{f(-r*.48)} {f(r*.05)}q4 -6 10 -4',fill='none',stroke=ln,stroke_width='1.8',stroke_linecap='round',opacity='.6')
        if style=='bun':
            bx,by=(-r*.45,-r*.95) if side else ((0,-r*1.12) if front else (0,-r*1.0))
            B+=circ(bx,by,r*.42,**st)+path(f'M{f(bx-r*.25)} {f(by-r*.1)}Q{f(bx)} {f(by-r*.32)} {f(bx+r*.22)} {f(by-r*.12)}',fill='none',stroke=ln,stroke_width='1.8',opacity='.6')
        if style=='ponytail':
            if side:
                d=f'M{f(-r*.85)} {f(-r*.55)}C{f(-r*1.7)} {f(-r*.5)} {f(-r*1.75)} {f(r*.9)} {f(-r*1.2)} {f(r*1.5)}C{f(-r*1.35)} {f(r*.8)} {f(-r*1.15)} {f(-r*.1)} {f(-r*.7)} {f(-r*.15)}Z'
            else:
                d=f'M{f(-r*.25)} {f(-r*.7)}C{f(-r*.6)} {f(r*.2)} {f(-r*.3)} {f(r*1.1)} 0 {f(r*1.5)}C{f(r*.3)} {f(r*1.1)} {f(r*.6)} {f(r*.2)} {f(r*.25)} {f(-r*.7)}Z'
            B+=path(d,**st)
        if style=='pigtails':
            for sx in (-1,1):
                if side and sx>0: continue
                cx=sx*r*1.05 if not side else -r*1.0
                d=f'M{f(cx)} {f(-r*.2)}C{f(cx+sx*r*.7)} {f(-r*.1)} {f(cx+sx*r*.6)} {f(r*.9)} {f(cx+sx*r*.25)} {f(r*1.2)}C{f(cx+sx*r*.1)} {f(r*.6)} {f(cx-sx*r*.1)} {f(r*.2)} {f(cx)} {f(-r*.2)}Z'
                B+=path(d,**st)
        if style in('long','bob'):
            ln2=r*(1.75 if style=='long' else 1.0)
            if side:
                d=f'M{f(-r*.2)} {f(-r*1.08)}C{f(-r*1.35)} {f(-r*1.0)} {f(-r*1.35)} {f(r*.2)} {f(-r*1.15)} {f(ln2*.7)}Q{f(-r*1.1)} {f(ln2)} {f(-r*.6)} {f(ln2)}L{f(-r*.25)} {f(ln2*.9)}Q{f(-r*.5)} {f(r*.3)} {f(r*.1)} {f(-r*.3)}Z'
            else:
                w=r*1.22
                d=f'M0 {f(-r*1.1)}C{f(-w*1.1)} {f(-r*1.05)} {f(-w)} {f(r*.4)} {f(-w)} {f(ln2)}L{f(-r*.55)} {f(ln2)}L{f(-r*.6)} 0 L{f(r*.6)} 0 L{f(r*.55)} {f(ln2)} L{f(w)} {f(ln2)}C{f(w)} {f(r*.4)} {f(w*1.1)} {f(-r*1.05)} 0 {f(-r*1.1)}Z'
                if backv: d=f'M0 {f(-r*1.1)}C{f(-w*1.1)} {f(-r*1.05)} {f(-w)} {f(r*.4)} {f(-w)} {f(ln2)}Q0 {f(ln2+10)} {f(w)} {f(ln2)}C{f(w)} {f(r*.4)} {f(w*1.1)} {f(-r*1.05)} 0 {f(-r*1.1)}Z'
            B+=path(d,**st)
            if backv: F+=path(d,**st)
        if style=='afro':
            B+=path(smooth(arc(0,360,r*1.42,30,cy=-r*.25,bump=5)[:-1],True),**st)
    if style=='cap':
        if side:
            F+=path(f'M{f(-r*1.02)} {f(-r*.05)}C{f(-r*1.05)} {f(-r*1.3)} {f(r*.95)} {f(-r*1.35)} {f(r*.95)} {f(-r*.38)}Z',fill=col,stroke=ln,stroke_width='2.2')
            F+=path(f'M{f(r*.7)} {f(-r*.42)}Q{f(r*1.5)} {f(-r*.52)} {f(r*1.65)} {f(-r*.28)}Q{f(r*1.2)} {f(-r*.2)} {f(r*.7)} {f(-r*.3)}Z',fill=dark(col,.2),stroke=ln,stroke_width='2.2')
        else:
            F+=path(f'M{f(-r*1.0)} {f(-r*.3)}C{f(-r*1.05)} {f(-r*1.4)} {f(r*1.05)} {f(-r*1.4)} {f(r*1.0)} {f(-r*.3)}Z',fill=col,stroke=ln,stroke_width='2.2')
            if front: F+=path(f'M{f(-r*.9)} {f(-r*.32)}Q0 {f(-r*.55)} {f(r*.9)} {f(-r*.32)}Q0 {f(-r*.05)} {f(-r*.9)} {f(-r*.32)}Z',fill=dark(col,.2),stroke=ln,stroke_width='2.2')
        F+=circ(0 if not side else -r*.05,-r*1.08,3.2,fill=dark(col,.25))
    if style=='beanie':
        F+=path(f'M{f(-r*1.03)} {f(-r*.2)}C{f(-r*1.1)} {f(-r*1.45)} {f(r*1.1)} {f(-r*1.45)} {f(r*1.03)} {f(-r*.2)}Z',fill=col,stroke=ln,stroke_width='2.2')
        F+=rect(-r*1.08,-r*.42,r*2.16,r*.3,rx=r*.12,fill=dark(col,.15),stroke=ln,stroke_width='2.2')
        F+=circ(0,-r*1.32,r*.2,fill=light(col,.2),stroke=ln,stroke_width='2')
    return B,F

# ---------------- outfits ----------------
OUTFITS={
 None:None,
 'tee':     dict(shirt='#E2725B',sleeve='short',pants='#3E4A61',legs='long',shoes='#F2F0EA',sole='#C9C3B8'),
 'hoodie':  dict(shirt='#5B6C8F',sleeve='long',pants='#2E3240',legs='long',shoes='#E9A23B',hood=True,pocket=True),
 'office':  dict(shirt='#F3F1EC',sleeve='long',pants='#2F3545',legs='long',shoes='#3A2A20',sole='#22170f',tie='#B8463A',collar=True),
 'suit':    dict(shirt='#2F3545',sleeve='long',pants='#2F3545',legs='long',shoes='#1E1712',sole='#120c08',tie='#B8463A',collar=True,lapel=True),
 'dress':   dict(shirt='#C8577A',sleeve='short',pants=None,legs='skirt',skirt='#C8577A',shoes='#3A2A40',sole='#2a1d30'),
 'casualF': dict(shirt='#7FB3A6',sleeve='short',pants='#3D4C6E',legs='long',shoes='#F2F0EA',sole='#C9C3B8'),
 'gym':     dict(shirt='#2E2E35',sleeve='none',pants='#2E2E35',legs='shorts',shoes='#E2493B',sole='#F4EFE6'),
 'pajama':  dict(shirt='#8EA6C9',sleeve='long',pants='#8EA6C9',legs='long',shoes=None,stripes=True),
 'student': dict(shirt='#E8C468',sleeve='long',pants='#4B5A78',legs='long',shoes='#F2F0EA',sole='#C9C3B8',hood=True),
 'grandpa': dict(shirt='#8B7B5E',sleeve='long',pants='#4F4A44',legs='long',shoes='#3A2A20',sole='#22170f',collar=True,vest='#6E5F45'),
}

def char(**o):
    if o.get('view','side')!='side':
        o=dict(o); o.setdefault('aN',[12,6]); o.setdefault('aF',[12,6]); o.setdefault('lN',[2,0]); o.setdefault('lF',[2,0])
    p=base_pose(**o)
    sk,lc=SKINS.get(p['skin'],SKINS['cream'])
    if p['skin']=='shadow': pass
    OF=OUTFITS.get(p['outfit']) if isinstance(p['outfit'],(str,type(None))) else p['outfit']
    if p['view']=='side': inner,J=_side(p,sk,lc,OF)
    else: inner,J=_front(p,sk,lc,OF)
    T=f'translate({f(p["x"])} {f(p["y"])})'+(f' rotate({f(p["rot"])})' if p['rot'] else '')+f' scale({f(p["s"]*p["face"])} {f(p["s"])})'
    return g(inner,transform=T),J

def _shirtcols(OF):
    c=OF['shirt']; return c, dark(c,.5)

def _side(p,sk,lc,OF):
    tw=p['torsoW']*(1+p['muscle']*.32)+p['belly']*10
    hip=[0,0]; sd=dirv(180-p['lean'])
    neck=add(hip,mul(sd,p['torsoL']))
    back=dirv(-p['lean']-90)
    c2=add(add(hip,mul(sd,p['torsoL']*.55)),mul(back,p['curl']*11))
    if p['belly']: c2=add(c2,mul(back,-p['belly']*14))
    a0=add(hip,mul(sd,4))
    torsoD='M'+P(a0)+'Q'+P(c2)+' '+P(neck)
    def q(u): return [(1-u)**2*a0[i]+2*(1-u)*u*c2[i]+u*u*neck[i] for i in (0,1)]
    shoulder=add(q(.86),mul(back,1))
    sN=add(shoulder,[1.5,0]); sF=add(shoulder,mul(back,4))
    hlean=p['lean']*.6+p['head']
    hdir=dirv(180-hlean)
    neckTop=add(neck,mul(sd,6))
    hc=add(neckTop,mul(hdir,p['headR']*.92))
    def arm(S,a,ik):
        if ik: return solve2(S,[ik[0],ik[1]],p['L1'],p['L2'],ik[2] if len(ik)>2 else 1)
        return fk(S,a[0]+p['lean'],a[1],p['L1'],p['L2'],1)
    aN=arm(sN,p['aN'],p['ikN']); aF=arm(sF,p['aF'],p['ikF'])
    hipN=[2.5,3]; hipF=[-2.5,3]
    def leg(H,a,ik):
        if ik: return solve2(H,[ik[0],ik[1]],p['L3'],p['L4'],ik[2] if len(ik)>2 else -1)
        return fk(H,a[0],a[1],p['L3'],p['L4'],-1)
    lN=leg(hipN,p['lN'],p['legIkN']); lF=leg(hipF,p['lF'],p['legIkF'])
    armD=lambda a,S: bentD(S,a['J'],a['T'])
    legD=lambda H,l: bentD(H,l['J'],l['T'])
    hN=aN['la']+p['wN']; hF=aF['la']+p['wF']
    out=''
    r=p['headR']
    HB,HF=hair_paths(p['hair'],r,'back' if p['back'] else 'side',p['hairCol'])
    hrot=clamp(hlean*.4,-12,12)
    htr=f'translate({f(hc[0])} {f(hc[1])}) rotate({f(hrot)})'
    nod=clamp(hlean,-30,45)/45.0
    p['_faceoff']=(r*.07*nod, r*.17*nod if nod>0 else r*.12*nod)
    if HB and 'head' not in p.get('hide',()): out+=g(HB,id='hair_back',transform=htr)
    ACC=AC.norm(p)
    if 'backpack' in ACC: out+=g(AC.backpack_side(q(.86),q(.3),back,p['lean']),id='backpack')
    shirt=OF and OF.get('shirt'); scol=shirt; sln=dark(shirt,.5) if shirt else None
    # ----- far arm
    L=Layer(lc)
    L.st(armD(aF,sF),p['armW'],sk)
    if p['muscle']: L.e(lerp(sF[0],aF['J'][0],.5),lerp(sF[1],aF['J'][1],.5),p['armW']*(.5+p['muscle']*.14),p['L1']*.34,-aF['ua'],sk)
    if p.get('tattoo'): L.raw(g(TT.arm(p,sF,aF,'far',p['armW']),opacity='.8'))
    if OF and OF['sleeve']!='none': _sleeve(L,sF,aF,OF,p,dark(scol,.12))
    hhF=hand(L,aF['T'],hF,p['hF'],sk)
    if p.get('tattoo'): L.raw(g(TT.hand_t(p,hhF['palm'],hF,'far'),opacity='.8'))
    _wrist_acc(L,p,aF,'far')
    s=L.out()
    if 'tote' in AC.norm(p) and not p['holdF']: s=AC.tote_bag(aF['T'])+s
    if p['holdF']: s+=p['holdF'](aF['T'],hF)
    if 'arm_far' not in p.get('hide',()): out+=g(s,id='arm_far')
    # ----- far leg
    def legLayer(H,l,fl,far):
        L=Layer(lc)
        fd=l['la']+90-fl
        dd=dirv(fd); up=dirv(fd-90)
        heel=add(l['T'],mul(dd,-5)); toe=add(l['T'],mul(dd,25)); mid=add(add(l['T'],mul(dd,10)),mul(up,2.5))
        pc = OF and OF.get('pants')
        if pc and OF['legs'] in ('long','shorts'): pc=dark(pc,.12) if far else pc
        L.st(legD(H,l),p['legW'],sk)
        if p.get('tattoo'): L.raw(TT.leg(p,H,l,'far' if far else 'near'))
        if not (OF and OF.get('shoes')): L.st('M'+P(heel)+'Q'+P(mid)+' '+P(toe),15.5,sk)
        if OF and OF['legs']=='long' and pc:
            L.st(legD(H,l),p['legW']+3,pc)
        elif OF and OF['legs']=='shorts' and pc:
            J2=add(H,mul(sub(l['J'],H),.62)); L.st('M'+P(H)+'L'+P(J2),p['legW']+4,pc,cap='butt' if True else 'round')
        s=L.out()
        if OF and OF.get('stripes') and OF['legs']=='long':
            s+=path(legD(H,l),fill='none',stroke=light(OF['pants'],.35),stroke_width='3',stroke_dasharray='2 9',opacity='.8')
        if OF and OF.get('shoes'): s+=shoe(l['T'],fd,dark(OF['shoes'],.1) if far else OF['shoes'],OF.get('sole','#F4EFE6'),style=OF.get('shoeStyle','sneaker'),skin=sk)
        return s
    if 'leg_far' not in p.get('hide',()): out+=g(legLayer(hipF,lF,p['fF'],True),id='leg_far')
    # ----- body (near leg + pelvis + torso + neck)
    L=Layer(lc)
    nearleg=legLayer(hipN,lN,p['fN'],False)
    body=Layer(lc)
    body.st('M'+P(neck)+'L'+P(hc),17,sk)
    if OF:
        pc=OF.get('pants')
        if OF['legs']=='skirt':
            sc_=OF['skirt']; top=q(.12)
            kn=add(lerp_pt(hipN,lN['J'],.85),[6,0]); kf=add(lerp_pt(hipF,lF['J'],.85),[-6,0])
            body.fill(f'M{P(add(top,[-tw*.5,0]))}L{P(add(top,[tw*.5,0]))}Q{P(add(kn,[14,-10]))} {P(add(kn,[18,4]))}Q{P(lerp_pt(kn,kf,.5))} {P(add(kf,[-16,8]))}Q{P(add(kf,[-8,-10]))} {P(add(top,[-tw*.5,0]))}Z',sc_)
        elif pc: body.e(0,-8,tw*.47,16,p['lean'],pc)
        body.st(torsoD,tw,scol)
    else:
        body.st(torsoD,tw,sk)
    if p['muscle']>0:
        pt=q(.7); body.e(pt[0]+6,pt[1],tw*.5,p['torsoL']*.22,p['lean'],scol or sk)
    body.c(hc[0],hc[1],0.01,sk)  # placeholder
    bs=''
    # assemble: near leg drawn first with its own outline, then body outline+fill on top (covers leg top)
    bs+=g(nearleg,id='leg_near') if 'leg_near' not in p.get('hide',()) else ''
    bs+=body.out()
    if p.get('tattoo'): bs+=TT.neck(p,neck,hc)
    if OF and OF.get('coat'): bs+=_coat_side(p,OF,q,hipN,hipF,lN,lF,tw,lc,back)
    if OF and OF.get('apron'): bs+=_apron_side(p,OF,q,lN,tw,lc,back)
    if OF:
        # hem line + details
        hem=q(.13); bd=dirv(90-p['lean'])
        if OF['legs']!='skirt' and OF.get('pants'):
            bs+=path(f'M{P(add(hem,mul(dirv(-p["lean"]-90),tw*.48)))}L{P(add(hem,mul(dirv(-p["lean"]+90),tw*.48)))}',stroke=sln,stroke_width='2.2',stroke_linecap='round',opacity='.6')
        if OF.get('pocket'):
            pp=q(.3); bs+=path(f'M{P(add(pp,[-4,-8]))}L{P(add(pp,[tw*.42,-10]))}L{P(add(pp,[tw*.42,10]))}L{P(add(pp,[-4,10]))}',fill='none',stroke=sln,stroke_width='2',opacity='.55')
        if OF.get('stripes'):
            bs+=path(torsoD,fill='none',stroke=light(scol,.35),stroke_width='3',stroke_dasharray='2 10',opacity='.8')
        if OF.get('vest'):
            vb=Layer(lc); vb.st('M'+P(q(.12))+'Q'+P(c2)+' '+P(q(.92)),tw*.9,OF['vest'],noOut=True); bs+=vb.out()
            for u in (.35,.55,.75): pt=q(u); bs+=circ(pt[0]+tw*.36,pt[1],2.4,fill=dark(OF['vest'],.5))
        if OF.get('lapel'):
            nt=q(.98); bs+=path(f'M{P(add(nt,[tw*.5,4]))}L{P(add(q(.55),[tw*.42,0]))}L{P(add(nt,[tw*.18,6]))}Z',fill=dark(scol,.25))
    # neck shadow + collar
    if OF:
        nt=q(.99)
        if OF.get('hood'):
            bs+=path(f'M{P(add(nt,[-tw*.55,6]))}Q{P(add(nt,[-tw*.6,-22]))} {P(add(nt,[-tw*.05,-12]))}Q{P(add(nt,[tw*.2,-4]))} {P(add(nt,[tw*.15,8]))}',fill=dark(scol,.08),stroke=lc,stroke_width='2.4',stroke_linejoin='round')
        if OF.get('collar'):
            bs+=path(f'M{P(add(nt,[tw*.05,-6]))}L{P(add(nt,[tw*.45,6]))}L{P(add(nt,[tw*.2,10]))}Z',fill=light(OF['shirt'],.1) if not OF.get('lapel') else '#F3F1EC',stroke=lc,stroke_width='1.6',stroke_linejoin='round')
        if OF.get('tie'):
            tt=add(nt,[tw*.38,6]); bs+=path(f'M{P(tt)}l5 4l-2 44l-5 8l-4 -8l2 -44Z',fill=OF['tie'],stroke=dark(OF['tie'],.5),stroke_width='1.6')
    bodyacc=''
    if 'backpack' in ACC: bodyacc+=AC.strap_side(add(q(.97),mul(back,tw*.05)),add(q(.42),mul(back,tw*.42)))
    if 'crossbody' in ACC:
        bodyacc+=AC.crossbody_strap(add(q(.95),mul(back,tw*.3)),add(q(.16),mul(back,-tw*.46)))
        bodyacc+=AC.crossbody_bag(add(q(.08),mul(back,-tw*.56)),p['lean'])
    if 'lanyard' in ACC: bodyacc+=AC.lanyard_side(neck,back,sd,tw)
    if 'necklace' in ACC: bodyacc+=AC.necklace_side(neck,back,sd,tw)
    if 'scarf' in ACC: bodyacc+=AC.scarf_side(neck,back,sd,tw)
    if 'headphones_neck' in ACC: bodyacc+=AC.neck_headphones(neck,back,sd)
    bodyacc+=AC2.body_side(ACC,neck,back,sd,tw,q,p)
    if bodyacc: bs+=g(bodyacc,id='accessories_body')
    if 'body' not in p.get('hide',()): out+=g(bs,id='body')
    # ----- head
    H=Layer(lc); H.c(0,0,r,sk)
    hs=H.out()
    fo=p.get('_faceoff',(0,0))
    if p['back']:
        hs+=HF
    else:
        hs+=g(_face(p,r,sk)+(TT.face(p,lerp(13,0,clamp(p['turn'],0,1)),lerp(8.5,11.5,clamp(p['turn'],0,1)),'side') if p.get('tattoo') else ''),id='face',transform=f'translate({f(fo[0])} {f(fo[1])})')
        if p['beard']: hs+=g(_beard(p['beard'],r,'side',p['hairCol']),transform=f'translate({f(fo[0])} {f(fo[1])})')
        hs+=HF
    ha=AC.head_layer([a for a in ACC if not(p['back'] and a in AC.GLASS_STYLES)],r,p['turn'],'side')
    if ha: hs+=g(ha,id='accessories_head',transform=f'translate({f(fo[0])} {f(fo[1])})' if not p['back'] else None)
    if 'head' not in p.get('hide',()): out+=g(hs,id='head',transform=htr)
    if p['mid']: out+=g(p['mid'](dict(hip=hip,kneeN=lN['J'],kneeF=lF['J'],footN=lN['T'],footF=lF['T'],handN=aN['T'],handF=aF['T'],head=hc,neck=neck,lean=p['lean'])),id='held_prop')
    # ----- near arm
    L=Layer(lc)
    odS=add(sN,mul(dirv(aN['ua']),p['armW']*.9))
    L.st(armD(aN,sN),p['armW'],sk,od=bentD(odS,aN['J'],aN['T']),ocap='butt')
    if p['muscle']: L.e(lerp(sN[0],aN['J'][0],.5),lerp(sN[1],aN['J'][1],.5),p['armW']*(.5+p['muscle']*.14),p['L1']*.34,-aN['ua'],sk)
    if p.get('tattoo'): L.raw(TT.arm(p,sN,aN,'near',p['armW']))
    if OF and OF['sleeve']!='none': _sleeve(L,sN,aN,OF,p,scol,near=True)
    hh=hand(L,aN['T'],hN,p['hN'],sk)
    if p.get('tattoo'): L.raw(TT.hand_t(p,hh['palm'],hN,'near'))
    _wrist_acc(L,p,aN,'near')
    s=L.out()
    if 'watch' in ACC: s+=AC.watch(aN['T'],aN['la'])
    if p['holdN']: s+=p['holdN'](aN['T'],hN)
    if 'arm_near' not in p.get('hide',()): out+=g(s,id='arm_near')
    out+=p['extra']
    J=dict(head=hc,handN=aN['T'],handF=aF['T'],footN=lN['T'],footF=lF['T'],hip=hip,neck=neck)
    return out,J

def lerp_pt(a,b,t): return [lerp(a[0],b[0],t),lerp(a[1],b[1],t)]
def _sleeve(L,S,a,OF,p,col,near=False):
    w=p['armW']+4
    if OF['sleeve']=='short':
        E=lerp_pt(S,a['J'],.62); d='M'+P(S)+'L'+P(E)
        od=None
        if near: od='M'+P(add(S,mul(dirv(a['ua']),p['armW']*.9)))+'L'+P(E)
        L.st(d,w,col,od=od,ocap='butt' if near else None)
    else:
        E=lerp_pt(a['J'],a['T'],.86); d=bentD(S,a['J'],E)
        od=bentD(add(S,mul(dirv(a['ua']),p['armW']*.9)),a['J'],E) if near else None
        L.st(d,w,col,od=od,ocap='butt' if near else None)

def _face(p,r,sk):
    e=FX.EXPR.get(p['expr'],FX.EXPR['neutral'])
    eL,eR,br,mo,ex,lk=e
    if p['eyes']: eL,eR=(p['eyes'] if isinstance(p['eyes'],tuple) else (p['eyes'],p['eyes']))
    if p['brow']: br=p['brow']
    if p['mouth']: mo=p['mouth']
    if p['fx'] is not None: ex=p['fx']
    if p['look'] is not None: lk=p['look']
    lx,ly=lk[0]*3,lk[1]*3
    if p['turn']<0:  # true profile: one eye near the front edge
        exx=r*.52; s=FX.eye(eR,exx,-3,1,lx*.5,ly,1,sk,None)+FX.brow(br,exx,-3,1,1)
        s+=g(FX.mouth(mo,0,0,1,sk),id='mouth',transform=f'translate({f(r*.7)} 15) scale(.55 1)')
        s+=FX.extras([e for e in ex if e in('blush','sweat','gloom','vein','pale','sick','sparkle')],r*.4-11,1,1,r,sk)
        return s
    t=clamp(p['turn'],0,1)
    cx=lerp(13,0,t); sp=lerp(8.5,11.5,t)
    s=''
    for i,exx in enumerate((cx-sp,cx+sp)):
        sc=lerp(.88,1,t) if i==0 else 1
        side=-1 if i==0 else 1
        kind=eL if i==0 else eR
        s+=FX.eye(kind,exx,-3,sc,lx,ly,side,sk,None)
        s+=FX.brow(br,exx,-3,sc,side)
    s+=g(FX.mouth(mo,cx+1,15,1,sk),id='mouth')
    s+=FX.extras(ex,cx,sp,1,r,sk)
    return s

def _beard(kind,r,view,col):
    ln=dark(col,.55)
    if kind in BEARD_V3: return _beard_v3(kind,r,view,col)
    if kind=='stubble': return path(f'M{f(-r*.2)} {f(r*.35)}Q{f(r*.3)} {f(r*1.05)} {f(r*.92)} {f(r*.25)}Q{f(r*.4)} {f(r*.7)} {f(-r*.2)} {f(r*.35)}Z',fill=col,opacity='.35')
    if kind=='full': return path(f'M{f(-r*.55)} {f(r*.1)}Q{f(-r*.2)} {f(r*1.25)} {f(r*.55)} {f(r*1.05)}Q{f(r*1.0)} {f(r*.8)} {f(r*.98)} {f(r*.15)}Q{f(r*.6)} {f(r*.32)} {f(r*.45)} {f(r*.28)}Q{f(r*.25)} {f(r*.6)} {f(r*-0.0)} {f(r*.35)}Q{f(-r*.2)} {f(r*.25)} {f(-r*.55)} {f(r*.1)}Z',fill=col,stroke=ln,stroke_width='2')
    if kind=='mustache': return path(f'M{f(r*.02)} {f(r*.3)}Q{f(r*.35)} {f(r*.18)} {f(r*.68)} {f(r*.3)}Q{f(r*.38)} {f(r*.42)} {f(r*.02)} {f(r*.3)}Z',fill=col,stroke=ln,stroke_width='1.6')
    return ''
def _glasses(r,turn,view):
    t=clamp(turn,0,1); cx=lerp(13,0,t); sp=lerp(8.5,11.5,t)
    s=''
    for i,ex in enumerate((cx-sp,cx+sp)):
        rr=9.5*(lerp(.88,1,t) if i==0 else 1)
        s+=circ(ex,-3,rr,fill='#DDEBFA',fill_opacity='.25',stroke='#2C2A30',stroke_width='2.6')
    s+=path(f'M{f(cx-sp+9)} -4 Q{f(cx)} -8 {f(cx+sp-9)} -4',fill='none',stroke='#2C2A30',stroke_width='2.4')
    if view=='side' and t<.6: s+=path(f'M{f(cx-sp-9)} -4L{f(-r*.7)} -8',stroke='#2C2A30',stroke_width='2.4')
    return s

# ---------------- front / back view ----------------
def _front(p,sk,lc,OF):
    backv=p['view']=='back'
    tw=p['torsoW']*1.12*(1+p['muscle']*.3)+p['belly']*12
    hip=[0,0]; neck=[0,-p['torsoL']]; r=p['headR']
    hc=add([0,-p['torsoL']-6],[math.sin(p['head']*D)*r*.92,-math.cos(p['head']*D)*r*.92])
    shY=-p['torsoL']+12; shx=tw/2-p['armW']*.55
    out=''
    HB,HF=hair_paths(p['hair'],r,'back' if backv else 'front',p['hairCol'])
    htr=f'translate({f(hc[0])} {f(hc[1])}) rotate({f(clamp(p["head"]*.7,-9,9))})'
    if HB and not backv: out+=g(HB,id='hair_back',transform=htr)
    shirt=OF and OF.get('shirt'); scol=shirt; sln=dark(shirt,.5) if shirt else None
    def armR(sign,a,ik,hk,wr):
        S=[sign*shx,shY]
        if ik:
            A=solve2(S,[ik[0],ik[1]],p['L1'],p['L2'],(ik[2] if len(ik)>2 else 1)*sign)
        else:
            ua=sign*a[0]; la=sign*(a[0]+a[1])
            Jt=add(S,mul(dirv(ua),p['L1'])); A=dict(J=Jt,T=add(Jt,mul(dirv(la),p['L2'])),ua=ua,la=la)
        return S,A
    # legs
    def legR(sign,a,fl):
        H=[sign*13,4]
        ua=sign*a[0]; la=sign*(a[0]-a[1])
        Jt=add(H,mul(dirv(ua),p['L3'])); T=add(Jt,mul(dirv(la),p['L4']))
        return H,dict(J=Jt,T=T,ua=ua,la=la)
    legs=[legR(-1,p['lF'],0),legR(1,p['lN'],0)]
    arms=[armR(-1,p['aF'],p['ikF'],p['hF'],p['wF']),armR(1,p['aN'],p['ikN'],p['hN'],p['wN'])]
    def legLayer(H,l,sign):
        L=Layer(lc); pc=OF and OF.get('pants')
        d=bentD(H,l['J'],l['T'])
        L.st(d,p['legW'],sk)
        if p.get('tattoo'): L.raw(TT.leg(p,H,l,'near' if sign>0 else 'far'))
        if not(OF and OF.get('shoes')): L.e(l['T'][0]+sign*3,l['T'][1]+4,10,7,0,sk)
        if OF and OF['legs']=='long' and pc: L.st(d,p['legW']+3,pc)
        elif OF and OF['legs']=='shorts' and pc: L.st('M'+P(H)+'L'+P(lerp_pt(H,l['J'],.62)),p['legW']+4,pc,cap='butt')
        s=L.out()
        if OF and OF.get('shoes'): s+=shoe_front(add(l['T'],[sign*2,0]),OF['shoes'],OF.get('sole','#F4EFE6'),style=OF.get('shoeStyle','sneaker'),skin=sk)
        return s
    for i,(H,l) in enumerate(legs): out+=g(legLayer(H,l,-1 if i==0 else 1),id='leg_far' if i==0 else 'leg_near')
    # body
    B=Layer(lc)
    B.st(f'M0 {f(-p["torsoL"])}L{P(hc)}',17,sk)
    if OF and OF['legs']=='skirt':
        B.fill(f'M{f(-tw*.46)} -14L{f(tw*.46)} -14L{f(tw*.72)} 62Q0 72 {f(-tw*.72)} 62Z',OF['skirt'])
    elif OF and OF.get('pants'): B.e(0,-4,tw*.5,18,0,OF['pants'])
    tcol=scol or sk
    B.st(f'M0 -10L0 {f(-p["torsoL"]+tw*.32)}',tw,tcol)
    bs=B.out()
    if OF:
        if OF['legs']!='skirt' and OF.get('pants'): bs+=path(f'M{f(-tw*.48)} -14L{f(tw*.48)} -14',stroke=sln,stroke_width='2.2',opacity='.6')
        if OF.get('pocket') and not backv: bs+=path(f'M{f(-tw*.3)} -22L{f(-tw*.22)} -46L{f(tw*.22)} -46L{f(tw*.3)} -22Z',fill='none',stroke=sln,stroke_width='2',opacity='.55')
        if OF.get('stripes'): 
            for xx in (-tw*.25,0,tw*.25): bs+=path(f'M{f(xx)} -14L{f(xx)} {f(-p["torsoL"]+10)}',stroke=light(scol,.35),stroke_width='3',stroke_dasharray='2 9',opacity='.8')
        if OF.get('vest') and not backv:
            bs+=path(f'M{f(-tw*.42)} -16L{f(-tw*.42)} {f(-p["torsoL"]+10)}L{f(-6)} {f(-p["torsoL"]+48)}L0 -12L{f(6)} {f(-p["torsoL"]+48)}L{f(tw*.42)} {f(-p["torsoL"]+10)}L{f(tw*.42)} -16Z',fill=OF['vest'],stroke=dark(OF['vest'],.5),stroke_width='1.6')
        if OF.get('lapel') and not backv:
            bs+=path(f'M-16 {f(-p["torsoL"]+6)}L0 {f(-p["torsoL"]+46)}L16 {f(-p["torsoL"]+6)}Z',fill='#F3F1EC')
            bs+=path(f'M-16 {f(-p["torsoL"]+6)}L-4 {f(-p["torsoL"]+54)}L-24 {f(-p["torsoL"]+28)}Z M16 {f(-p["torsoL"]+6)}L4 {f(-p["torsoL"]+54)}L24 {f(-p["torsoL"]+28)}Z',fill=dark(scol,.25))
        if OF.get('collar') and not backv:
            bs+=path(f'M-12 {f(-p["torsoL"]+2)}L0 {f(-p["torsoL"]+12)}L-10 {f(-p["torsoL"]+18)}Z M12 {f(-p["torsoL"]+2)}L0 {f(-p["torsoL"]+12)}L10 {f(-p["torsoL"]+18)}Z',fill='#F3F1EC' if OF.get('lapel') else light(OF['shirt'],.1),stroke=lc,stroke_width='1.6',stroke_linejoin='round')
        if OF.get('tie') and not backv:
            bs+=path(f'M0 {f(-p["torsoL"]+10)}l5 5l-2 40l-3 7l-3 -7l-2 -40Z',fill=OF['tie'],stroke=dark(OF['tie'],.5),stroke_width='1.6')
        if OF.get('hood'):
            if backv: bs+=path(f'M{f(-tw*.36)} {f(-p["torsoL"]+4)}Q0 {f(-p["torsoL"]+50)} {f(tw*.36)} {f(-p["torsoL"]+4)}Q0 {f(-p["torsoL"]-8)} {f(-tw*.36)} {f(-p["torsoL"]+4)}Z',fill=dark(scol,.08),stroke=lc,stroke_width='2.4')
            else: bs+=path(f'M{f(-tw*.34)} {f(-p["torsoL"]+2)}Q0 {f(-p["torsoL"]+22)} {f(tw*.34)} {f(-p["torsoL"]+2)}',fill='none',stroke=dark(scol,.3),stroke_width='5',stroke_linecap='round')+path(f'M-7 {f(-p["torsoL"]+16)}l-2 22M7 {f(-p["torsoL"]+16)}l2 22',stroke='#F3F1EC',stroke_width='2.4',stroke_linecap='round')
    ACC=AC.norm(p); TL=p['torsoL']; ba=''
    if 'backpack' in ACC:
        if backv:
            ba+=rect(-tw*.4,-TL+14,tw*.8,TL*.78,rx=18,fill=AC.PACK,stroke=dark(AC.PACK,.55),stroke_width='2.6')
            ba+=rect(-tw*.3,-TL*.42,tw*.6,TL*.3,rx=10,fill=dark(AC.PACK,.12),stroke=dark(AC.PACK,.55),stroke_width='2.2')
            ba+=path(f'M{f(-tw*.2)} {f(-TL+16)}Q0 {f(-TL-2)} {f(tw*.2)} {f(-TL+16)}',fill='none',stroke=dark(AC.PACK,.55),stroke_width='4',stroke_linecap='round')
        else:
            for sx in (-1,1): ba+=AC.strap_side([sx*tw*.3,-TL+4],[sx*tw*.36,-TL*.42],AC.PACK)
    if 'crossbody' in ACC:
        sx=-1 if backv else 1
        ba+=AC.crossbody_strap([-sx*tw*.36,-TL+6],[sx*tw*.44,-22])+AC.crossbody_bag([sx*tw*.5,-14])
    if 'lanyard' in ACC and not backv:
        ba+=path(f'M{f(-tw*.22)} {f(-TL+2)}L0 {f(-TL+44)}L{f(tw*.22)} {f(-TL+2)}',fill='none',stroke='#3E6A8A',stroke_width='3.4',stroke_linejoin='round')
        ba+=g(rect(-9,0,18,24,rx=3,fill='#F3F1EC',stroke='#5A6676',stroke_width='1.8')+rect(-6,4,12,8,rx=1.5,fill='#8EA6C9'),transform=f'translate(0 {f(-TL+44)})')
    if 'necklace' in ACC and not backv:
        ba+=path(f'M{f(-tw*.2)} {f(-TL+3)}Q0 {f(-TL+26)} {f(tw*.2)} {f(-TL+3)}',fill='none',stroke=AC.GOLD,stroke_width='2')+circ(0,-TL+17,3.6,fill='#7FC6E8',stroke=dark(AC.GOLD,.3),stroke_width='1.2')
    if 'scarf' in ACC:
        c=AC.SCARF; ln=dark(c,.5)
        ba+=path(f'M{f(-tw*.36)} {f(-TL+1)}Q0 {f(-TL+16)} {f(tw*.36)} {f(-TL+1)}',fill='none',stroke=ln,stroke_width='19',stroke_linecap='round')
        ba+=path(f'M{f(-tw*.36)} {f(-TL+1)}Q0 {f(-TL+16)} {f(tw*.36)} {f(-TL+1)}',fill='none',stroke=c,stroke_width='14',stroke_linecap='round')
        if not backv:
            ba+=path(f'M{f(tw*.16)} {f(-TL+10)}L{f(tw*.2)} {f(-TL+56)}',stroke=ln,stroke_width='15',stroke_linecap='round')+path(f'M{f(tw*.16)} {f(-TL+10)}L{f(tw*.2)} {f(-TL+56)}',stroke=c,stroke_width='10.5',stroke_linecap='round')
    if 'headphones_neck' in ACC and not backv:
        ba+=AC.neck_headphones([0,-TL],[1,0],[0,-1])
    ba+=AC2.body_front(ACC,TL,tw,backv,p)
    if ba: bs+=g(ba,id='accessories_body')
    if OF and OF.get('coat'): bs+=_coat_front(p,OF,tw,lc,backv)
    if OF and OF.get('apron') and not backv: bs+=_apron_front(p,OF,tw,lc)
    if p.get('tattoo') and not backv: bs+=TT.neck(p,[0,-p['torsoL']],hc)
    out+=g(bs,id='body')
    # head
    Hh=Layer(lc); Hh.c(0,0,r,sk); hs=Hh.out()
    if backv: hs+=HB+HF
    else:
        q=dict(p); q['turn']=1
        hs+=g(_face(q,r,sk),id='face')
        if p['beard']: hs+=_beard(p['beard'],r,'front',p['hairCol'])
        hs+=HF
    ha=AC.head_layer(ACC,r,1,'back' if backv else 'front')
    if ha: hs+=g(ha,id='accessories_head')
    out+=g(hs,id='head',transform=htr)
    # arms on top
    for i,(S,A) in enumerate(arms):
        sign=-1 if i==0 else 1
        L=Layer(lc)
        od=bentD(add(S,mul(dirv(A['ua']),p['armW']*.7)),A['J'],A['T'])
        L.st(bentD(S,A['J'],A['T']),p['armW'],sk,od=od,ocap='butt')
        wh=('far' if i==0 else 'near') if not backv else ('near' if i==0 else 'far')
        if p.get('tattoo'): L.raw(TT.arm(p,S,A,wh,p['armW']))
        if OF and OF['sleeve']!='none': _sleeve(L,S,A,OF,p,scol,near=True)
        hk=p['hF'] if i==0 else p['hN']; wr=p['wF'] if i==0 else p['wN']
        hh_=hand(L,A['T'],A['la']+sign*wr,hk,sk,mirror=-sign if not backv else sign)
        if p.get('tattoo'): L.raw(TT.hand_t(p,hh_['palm'],A['la']+sign*wr,wh))
        _wrist_acc(L,p,A,wh)
        s=L.out()
        if 'watch' in ACC and i==0: s+=AC.watch(A['T'],A['la'])
        if 'tote' in ACC and i==1 and not p['holdN']: s=AC.tote_bag(A['T'])+s
        hold=p['holdF'] if i==0 else p['holdN']
        if hold: s+=hold(A['T'],A['la'])
        out+=g(s,id='arm_left' if i==0 else 'arm_right')
    out+=p['extra']
    return out,dict(head=hc)

# ------------- body type presets -------------
BODY={
 'man':   dict(),
 'woman': dict(torsoW=48,armW=17,legW=21,torsoL=98,headR=38,L1=56,L2=50,L3=68,L4=64),
 'buff':  dict(muscle=.9,torsoW=58,armW=22,legW=26),
 'chubby':dict(torsoW=60,belly=2.2,armW=21,legW=26),
 'kid':   dict(torsoW=44,armW=15,legW=17,torsoL=66,headR=40,L1=38,L2=34,L3=44,L4=42),
 'old':   dict(curl=.8,lean=10,torsoW=52,armW=18,legW=21),
}
CAST={
 'alex':  dict(name='Alex (protagonist)',body='man',skin='cream',hair=None,outfit=None),
 'alex_hoodie': dict(name='Alex – hoodie',body='man',skin='cream',hair='short',hairCol='#3A2C24',outfit='hoodie',acc=['headphones_neck']),
 'alex_commute': dict(name='Alex – commuter',body='man',skin='cream',hair='short',hairCol='#3A2C24',outfit='hoodie',acc=['backpack','watch','headphones']),
 'maya':  dict(name='Maya',body='woman',skin='cream',hair='bun',hairCol='#3a2a22',outfit=None),
 'maya_dressed': dict(name='Maya – casual',body='woman',skin='warm',hair='long',hairCol='#4A2E22',outfit='casualF',acc=['earrings','crossbody']),
 'sam':   dict(name='Sam – gym friend',body='buff',skin='tan',hair='buzz',hairCol='#1E1712',outfit='gym'),
 'leo':   dict(name='Leo – office',body='man',skin='brown',hair='short',hairCol='#17110D',outfit='office',beard='stubble',acc=['watch','lanyard']),
 'priya': dict(name='Priya – student',body='woman',skin='tan',hair='ponytail',hairCol='#1B1310',outfit='student',glasses='glasses_square',acc=['earrings_studs','backpack']),
 'boss':  dict(name='Boss',body='chubby',skin='warm',hair='short',hairCol='#7A6A5C',outfit='suit',beard='mustache',acc=['watch']),
 'kid':   dict(name='Kid',body='kid',skin='warm',hair='curly',hairCol='#5A3B26',outfit='tee',acc=['backpack']),
 'grandpa':dict(name='Grandpa',body='old',skin='warm',hair='short',hairCol='#D9D4CC',outfit='grandpa',glasses='glasses_round',beard='mustache',acc=['scarf']),
 'nora':  dict(name='Nora – creative',body='woman',skin='deep',hair='afro',hairCol='#1B1310',outfit='dress',acc=['earrings','necklace','glasses_cat','tote']),
 'shadow':dict(name='Shadow self',body='man',skin='shadow',hair=None,outfit=None),
}
def cast_args(key):
    c=dict(CAST[key]); b=BODY[c.pop('body')]; c.pop('name')
    out=dict(b); out.update(c); return out

def head_only(turn=.15,view='side',expr='neutral',s=1,x=0,y=0,rotd=0,**o):
    p=base_pose(**o); p['turn']=turn; p['expr']=expr
    for k,v in o.items(): p[k]=v
    p['turn']=turn
    sk,lc=SKINS.get(p['skin'],SKINS['cream']); r=p['headR']
    v='front' if view=='front' else ('back' if view=='back' else 'side')
    HB,HF=hair_paths(p['hair'],r,v,p['hairCol'])
    out=''
    if HB and v!='back': out+=g(HB,id='hair_back')
    out+=Layer(lc).__class__(lc).__dict__ and ''
    H=Layer(lc); H.c(0,0,r,sk); out+=H.out()
    if v=='back': out+=HB+HF
    else:
        q=dict(p); q['turn']=1 if v=='front' else turn
        out+=g(_face(q,r,sk),id='face')
        if p['beard']: out+=_beard(p['beard'],r,v,p['hairCol'])
        out+=HF
    ha=AC.head_layer(AC.norm(p),r,1 if v=='front' else turn,v)
    if ha: out+=ha
    return g(out,transform=f'translate({f(x)} {f(y)}) rotate({f(rotd)}) scale({f(s)})')

def hip_h(a,s=1): return (a.get('L3',72)+a.get('L4',68)+7)*s


# =====================================================================
# v3 additions: hair styles, beards, coats/aprons, wrist pieces, outfits, bodies, cast
# =====================================================================
HAIR_V3=('hijab','side_part','undercut','mohawk','braid','wavy','top_knot','curtain','dreads')
def _hair_v3(style,r,view,col):
    ln=dark(col,.55); st=dict(fill=col,stroke=ln,stroke_width='2.2',stroke_linejoin='round')
    side=view=='side'; front=view=='front'; backv=view=='back'
    hl=lambda d,op='.5': path(d,fill='none',stroke=light(col,.28),stroke_width='2.6',stroke_linecap='round',opacity=op)
    B=F=''
    if style=='hijab':
        fold=dark(col,.18)
        if side:
            outer=[]
            for i in range(19):
                a=lerp(-62,-238,i/18)*D; k=r+4.5; outer.append([math.cos(a)*k,math.sin(a)*k])
            pts=outer+[[-r*1.02,r*.55],[-r*.82,r*1.05],[-r*.2,r*1.32],[r*.55,r*1.18],[r*.98,r*.72],
                       [r*.78,r*.74],[r*.42,r*.98],[-r*.02,r*.72],[-r*.16,r*.2],[-r*.1,-r*.36],[r*.18,-r*.64],[r*.52,-r*.8]]
            F+=path(smooth(pts,True,.9),**st)
            F+=path(f'M{f(-r*.1)} {f(-r*.36)}Q{f(-r*.24)} {f(r*.2)} {f(-r*.02)} {f(r*.72)}',fill='none',stroke=fold,stroke_width='3',stroke_linecap='round',opacity='.8')
            F+=path(f'M{f(-r*.7)} {f(r*.4)}Q{f(-r*.5)} {f(r*.95)} {f(r*.1)} {f(r*1.12)}M{f(-r*.85)} {f(-r*.2)}Q{f(-r*.95)} {f(r*.4)} {f(-r*.62)} {f(r*.85)}',fill='none',stroke=fold,stroke_width='2.4',stroke_linecap='round',opacity='.7')
            F+=hl(f'M{f(-r*.55)} {f(-r*.75)}Q{f(-r*.1)} {f(-r*1.05)} {f(r*.35)} {f(-r*.9)}')
            B+=path(f'M{f(-r*.9)} {f(r*.2)}C{f(-r*1.35)} {f(r*.9)} {f(-r*1.3)} {f(r*1.9)} {f(-r*.85)} {f(r*2.25)}L{f(r*.45)} {f(r*2.05)}C{f(r*.7)} {f(r*1.6)} {f(r*.6)} {f(r*1.2)} {f(r*.3)} {f(r*1.0)}Z',**st)
        else:
            d=(f'M0 {f(-r-4.5)}C{f(-r*1.45)} {f(-r-4)} {f(-r*1.3)} {f(r*.6)} {f(-r*1.12)} {f(r*1.05)}C{f(-r*.7)} {f(r*1.45)} {f(r*.7)} {f(r*1.45)} {f(r*1.12)} {f(r*1.05)}C{f(r*1.3)} {f(r*.6)} {f(r*1.45)} {f(-r-4)} 0 {f(-r-4.5)}Z')
            if front:
                d+=(f'M0 {f(-r*.72)}C{f(-r*.62)} {f(-r*.74)} {f(-r*.82)} {f(-r*.1)} {f(-r*.72)} {f(r*.38)}C{f(-r*.6)} {f(r*.92)} {f(r*.6)} {f(r*.92)} {f(r*.72)} {f(r*.38)}C{f(r*.82)} {f(-r*.1)} {f(r*.62)} {f(-r*.74)} 0 {f(-r*.72)}Z')
            F+=path(d,fill_rule='evenodd',**st)
            if front: F+=path(f'M{f(-r*.6)} {f(-r*.62)}Q0 {f(-r*.86)} {f(r*.6)} {f(-r*.62)}',fill='none',stroke=fold,stroke_width='3',opacity='.8')+path(f'M{f(-r*.8)} {f(r*.82)}Q0 {f(r*1.25)} {f(r*.8)} {f(r*.82)}',fill='none',stroke=fold,stroke_width='2.4',opacity='.7')
            F+=hl(f'M{f(-r*.75)} {f(-r*.8)}Q{f(-r*.2)} {f(-r*1.1)} {f(r*.35)} {f(-r*1.02)}')
            B+=path(f'M{f(-r*1.15)} {f(r*.6)}C{f(-r*1.35)} {f(r*1.5)} {f(-r*1.2)} {f(r*2.0)} {f(-r*1.0)} {f(r*2.25)}L{f(r*1.0)} {f(r*2.25)}C{f(r*1.2)} {f(r*2.0)} {f(r*1.35)} {f(r*1.5)} {f(r*1.15)} {f(r*.6)}Z',**st)
        return B,F
    if style in('side_part','curtain'):
        B,F=hair_paths('short',r,view,col)
        if front: F+=path(f'M{f(-r*.55)} {f(-r*.95)}Q{f(r*.2)} {f(-r*1.25)} {f(r*.98)} {f(-r*.45)}Q{f(r*.4)} {f(-r*.7)} {f(-r*.2)} {f(-r*.55)}Q{f(-r*.5)} {f(-r*.75)} {f(-r*.55)} {f(-r*.95)}Z',**st)+path(f'M{f(-r*.3)} {f(-r*1.0)}L{f(-r*.22)} {f(-r*.62)}',stroke=ln,stroke_width='1.8',opacity='.6')
        elif side: F+=path(f'M{f(-r*.5)} {f(-r*1.0)}Q{f(r*.4)} {f(-r*1.35)} {f(r*.95)} {f(-r*.5)}Q{f(r*.5)} {f(-r*.72)} {f(r*.05)} {f(-r*.62)}Q{f(-r*.35)} {f(-r*.75)} {f(-r*.5)} {f(-r*1.0)}Z',**st)
        if style=='curtain' and front: F+=path(f'M0 {f(-r*1.05)}Q{f(-r*.7)} {f(-r*.8)} {f(-r*.85)} {f(-r*.25)}M0 {f(-r*1.05)}Q{f(r*.7)} {f(-r*.8)} {f(r*.85)} {f(-r*.25)}',fill='none',stroke=ln,stroke_width='2',opacity='.6')
        return B,F+hl(f'M{f(-r*.3)} {f(-r*1.02)}Q{f(r*.1)} {f(-r*1.15)} {f(r*.45)} {f(-r*.95)}')
    if style=='undercut':
        B,F=hair_paths('buzz',r,view,col)
        F=g(F,opacity='.55')
        if side: F+=path(f'M{f(-r*.7)} {f(-r*.6)}C{f(-r*.85)} {f(-r*1.5)} {f(r*.6)} {f(-r*1.55)} {f(r*1.0)} {f(-r*.62)}Q{f(r*.55)} {f(-r*.8)} {f(r*.1)} {f(-r*.72)}Q{f(-r*.4)} {f(-r*.62)} {f(-r*.7)} {f(-r*.6)}Z',**st)
        else: F+=path(f'M{f(-r*.72)} {f(-r*.6)}C{f(-r*.8)} {f(-r*1.55)} {f(r*.8)} {f(-r*1.55)} {f(r*.72)} {f(-r*.6)}Q0 {f(-r*.82)} {f(-r*.72)} {f(-r*.6)}Z',**st)
        return B,F+hl(f'M{f(-r*.4)} {f(-r*1.15)}Q{f(r*.05)} {f(-r*1.35)} {f(r*.45)} {f(-r*1.1)}')
    if style=='mohawk':
        B,F=hair_paths('buzz',r,view,col); F=g(F,opacity='.35')
        if side:
            pts=[]
            for i in range(9):
                a=lerp(-200,-20,i/8)*D; k=r+(18 if i%2 else 4); pts.append([math.cos(a)*k,math.sin(a)*k])
            F+=path('M'+'L'.join(P(p) for p in pts)+f'L{f(r*.85)} {f(-r*.42)}Q0 {f(-r*.95)} {f(-r*.9)} {f(-r*.2)}Z',**st)
        else:
            F+=path(f'M{f(-r*.2)} {f(-r*.85)}L{f(-r*.3)} {f(-r*1.55)}L{f(-r*.1)} {f(-r*1.35)}L0 {f(-r*1.7)}L{f(r*.1)} {f(-r*1.35)}L{f(r*.3)} {f(-r*1.55)}L{f(r*.2)} {f(-r*.85)}Z',**st)
        return B,F
    if style=='braid':
        B,F=hair_paths('short',r,view,col)
        seg=''
        if side:
            for i in range(7): seg+=ell(-r*1.0-i*.6,r*.1+i*r*.28,r*.17,r*.16,**st)
            seg+=path(f'M{f(-r*1.1)} {f(r*1.95)}l-4 10l8 0Z',fill='#E8455A',stroke=dark('#E8455A',.5),stroke_width='1.4')
        else:
            for i in range(7): seg+=ell(r*.95+i*.5,r*.2+i*r*.27,r*.16,r*.15,**st)
        B=seg+B
        return B,F
    if style in('wavy','dreads'):
        B,F=hair_paths('long',r,view,col)
        if style=='wavy':
            ex=''.join(path(f'M{f(x)} {f(r*.2)}q6 {f(r*.3)} 0 {f(r*.6)}q-6 {f(r*.3)} 0 {f(r*.6)}',fill='none',stroke=ln,stroke_width='1.8',opacity='.55') for x in ((-r*1.05,-r*.8) if side else (-r*1.05,-r*.85,r*.85,r*1.05)))
            B+=ex
        else:
            locks=''
            xs=(-r*1.2,-r*1.0,-r*.8) if side else (-r*1.15,-r*.95,r*.95,r*1.15)
            for x in xs: locks+=path(f'M{f(x)} {f(-r*.3)}L{f(x+2)} {f(r*1.6)}',stroke=ln,stroke_width='9',stroke_linecap='round')+path(f'M{f(x)} {f(-r*.3)}L{f(x+2)} {f(r*1.6)}',stroke=col,stroke_width='6',stroke_linecap='round',stroke_dasharray='4 2')
            B=locks
        return B,F
    if style=='top_knot':
        B,F=hair_paths('buzz',r,view,col)
        bx,by=(-r*.1,-r*1.18) if not front else (0,-r*1.2)
        F+=circ(bx,by,r*.32,**st)+rect(bx-r*.22,by+r*.18,r*.44,r*.1,rx=2,fill=dark(col,.3))
        return B,F
    return B,F
BEARD_V3=('goatee','full_long','chin_strap','beard_short')
def _beard_v3(kind,r,view,col):
    ln=dark(col,.55); st=dict(fill=col,stroke=ln,stroke_width='1.8',stroke_linejoin='round')
    fr=view=='front'; cx=0 if fr else 13
    if kind=='goatee':
        return path(f'M{f(cx-7)} {f(r*.62)}Q{f(cx)} {f(r*1.12)} {f(cx+8)} {f(r*.62)}Q{f(cx)} {f(r*.75)} {f(cx-7)} {f(r*.62)}Z',**st)+path(f'M{f(cx-9)} {f(r*.32)}Q{f(cx)} {f(r*.2)} {f(cx+10)} {f(r*.32)}Q{f(cx)} {f(r*.42)} {f(cx-9)} {f(r*.32)}Z',**st)
    if kind=='chin_strap':
        if fr: return path(f'M{f(-r*.96)} {f(-r*.05)}Q{f(-r*.8)} {f(r*1.05)} 0 {f(r*1.04)}Q{f(r*.8)} {f(r*1.05)} {f(r*.96)} {f(-r*.05)}L{f(r*.84)} {f(-r*.05)}Q{f(r*.7)} {f(r*.88)} 0 {f(r*.9)}Q{f(-r*.7)} {f(r*.88)} {f(-r*.84)} {f(-r*.05)}Z',**st)
        return path(f'M{f(-r*.5)} {f(-r*.05)}Q{f(-r*.3)} {f(r*1.02)} {f(r*.6)} {f(r*.92)}Q{f(r*.95)} {f(r*.75)} {f(r*.98)} {f(r*.4)}L{f(r*.86)} {f(r*.45)}Q{f(r*.7)} {f(r*.78)} {f(r*.4)} {f(r*.82)}Q{f(-r*.2)} {f(r*.85)} {f(-r*.38)} {f(-r*.05)}Z',**st)
    if kind=='beard_short':
        if fr: return path(f'M{f(-r*.92)} {f(0)}Q{f(-r*.85)} {f(r*1.12)} 0 {f(r*1.12)}Q{f(r*.85)} {f(r*1.12)} {f(r*.92)} 0Q{f(r*.6)} {f(r*.5)} {f(r*.32)} {f(r*.48)}Q0 {f(r*.3)} {f(-r*.32)} {f(r*.48)}Q{f(-r*.6)} {f(r*.5)} {f(-r*.92)} 0Z',**st)
        return path(f'M{f(-r*.55)} {f(0)}Q{f(-r*.3)} {f(r*1.15)} {f(r*.55)} {f(r*1.02)}Q{f(r*1.0)} {f(r*.8)} {f(r*.98)} {f(r*.2)}Q{f(r*.65)} {f(r*.42)} {f(r*.5)} {f(r*.32)}Q{f(r*.3)} {f(r*.25)} {f(r*.08)} {f(r*.34)}Q{f(-r*.2)} {f(r*.3)} {f(-r*.55)} 0Z',**st)
    if kind=='full_long':
        if fr: d=f'M{f(-r*.95)} {f(-r*.05)}Q{f(-r*.95)} {f(r*1.6)} 0 {f(r*1.85)}Q{f(r*.95)} {f(r*1.6)} {f(r*.95)} {f(-r*.05)}Q{f(r*.6)} {f(r*.5)} {f(r*.3)} {f(r*.45)}Q0 {f(r*.28)} {f(-r*.3)} {f(r*.45)}Q{f(-r*.6)} {f(r*.5)} {f(-r*.95)} {f(-r*.05)}Z'
        else: d=f'M{f(-r*.55)} {f(-r*.05)}Q{f(-r*.4)} {f(r*1.6)} {f(r*.45)} {f(r*1.8)}Q{f(r*1.1)} {f(r*1.2)} {f(r*.98)} {f(r*.15)}Q{f(r*.65)} {f(r*.4)} {f(r*.5)} {f(r*.3)}Q{f(r*.3)} {f(r*.22)} {f(r*.06)} {f(r*.32)}Q{f(-r*.2)} {f(r*.25)} {f(-r*.55)} {f(-r*.05)}Z'
        s=path(d,**st)
        for i in range(4): s+=path(f'M{f(cx-8+i*6)} {f(r*.8)}q2 {f(r*.35)} 0 {f(r*.6)}',fill='none',stroke=ln,stroke_width='1.6',opacity='.55')
        return s
    return ''
def _wrist_acc(L,p,A,which):
    s=AC2.wrist(AC.norm(p),A,which)
    if s: L.raw(s)
def _hull(pts):
    pts=sorted(map(tuple,pts))
    if len(pts)<3: return [list(x) for x in pts]
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for q_ in pts:
        while len(lo)>=2 and cr(lo[-2],lo[-1],q_)<=0: lo.pop()
        lo.append(q_)
    for q_ in reversed(pts):
        while len(up)>=2 and cr(up[-2],up[-1],q_)<=0: up.pop()
        up.append(q_)
    return [list(x) for x in lo[:-1]+up[:-1]]
def _coat_side(p,OF,q,hipN,hipF,lN,lF,tw,lc,back):
    col=OF['coat']; ln=dark(col,.5); fr=mul(back,-1)
    Lc=Layer(lc)
    pts=[add(q(.14),mul(back,tw*.52)),add(q(.14),mul(fr,tw*.52))]
    ln_=OF.get('coatLen',.62)
    for H,l in ((hipN,lN),(hipF,lF)):
        pt=lerp_pt(H,l['J'],ln_); dv=sub(l['J'],H); n=rot([dv[0]/max(vlen(dv),1e-3),dv[1]/max(vlen(dv),1e-3)],90)
        pts+= [add(pt,mul(n,p['legW']*.95)),add(pt,mul(n,-p['legW']*.95))]
    hull=_hull(pts)
    Lc.fill(smooth(hull,True,.5),col)
    tpath='M'+'L'.join(P(q(u)) for u in [i/10*.92+.06 for i in range(11)])
    Lc.st(tpath,tw+3,col)
    s=Lc.out()
    # open front showing the shirt + lapel
    a=add(q(.96),mul(fr,tw*.36)); b=add(q(.5),mul(fr,tw*.46))
    s+=path(f'M{P(a)}L{P(b)}',stroke=OF.get('shirt','#F3F1EC'),stroke_width='7',stroke_linecap='round')
    s+=path(f'M{P(add(q(.97),mul(fr,tw*.2)))}L{P(add(q(.62),mul(fr,tw*.44)))}',stroke=ln,stroke_width='1.8',stroke_linecap='round',opacity='.7')
    pk=add(q(.2),mul(fr,tw*.12)); s+=path(f'M{P(pk)}l{f(tw*.3)} 0',stroke=ln,stroke_width='2',opacity='.6',stroke_linecap='round')
    for u in (.4,.6,.8): pt=add(q(u),mul(fr,tw*.48)); s+=circ(pt[0],pt[1],2,fill=dark(col,.35))
    return s
def _apron_side(p,OF,q,lN,tw,lc,back):
    col=OF['apron']; fr=mul(back,-1)
    us=[.74,.6,.45,.3,.16]
    frontE=[add(q(u),mul(fr,tw*.5+3)) for u in us]
    backE=[add(q(u),mul(fr,tw*.12)) for u in reversed(us)]
    kn=lerp_pt([2.5,3],lN['J'],.72); dv=sub(lN['J'],[2.5,3]); n=rot([dv[0]/max(vlen(dv),1e-3),dv[1]/max(vlen(dv),1e-3)],90)
    if n[0]<0: n=mul(n,-1)
    k1=add(kn,mul(n,p['legW']*.75)); k2=add(kn,mul(n,-p['legW']*.35))
    pts=frontE+[k1,k2]+backE
    Lc=Layer(lc); Lc.fill(smooth(pts,True,.35),col)
    s=Lc.out()+path(f'M{P(add(q(.74),mul(fr,tw*.3)))}L{P(add(q(.98),mul(fr,tw*.1)))}',stroke=dark(col,.3),stroke_width='3',stroke_linecap='round')
    s+=path(f'M{P(add(q(.3),mul(fr,tw*.14)))}L{P(add(q(.3),mul(fr,tw*.52)))}',stroke=dark(col,.25),stroke_width='2.4',stroke_linecap='round',opacity='.7')
    return s
def _coat_front(p,OF,tw,lc,backv):
    col=OF['coat']; ln=dark(col,.5); TL=p['torsoL']; Ln=OF.get('coatLen',.62)*p['L3']+6
    if backv:
        return path(f'M{f(-tw*.54)} {f(-TL+6)}L{f(-tw*.62)} {f(Ln)}L{f(tw*.62)} {f(Ln)}L{f(tw*.54)} {f(-TL+6)}Q0 {f(-TL-6)} {f(-tw*.54)} {f(-TL+6)}Z',fill=col,stroke=lc,stroke_width='2.6',stroke_linejoin='round')+path(f'M0 {f(Ln*.4)}L0 {f(Ln)}',stroke=ln,stroke_width='2')
    s=''
    for sx in (-1,1):
        s+=path(f'M{f(sx*tw*.54)} {f(-TL+6)}L{f(sx*tw*.64)} {f(Ln)}L{f(sx*tw*.1)} {f(Ln+2)}L{f(sx*tw*.14)} {f(-TL+44)}L{f(sx*tw*.22)} {f(-TL+2)}Z',fill=col,stroke=lc,stroke_width='2.6',stroke_linejoin='round')
        s+=path(f'M{f(sx*tw*.22)} {f(-TL+2)}L{f(sx*tw*.3)} {f(-TL+30)}L{f(sx*tw*.14)} {f(-TL+44)}',fill=dark(col,.08),stroke=ln,stroke_width='1.6',stroke_linejoin='round')
        s+=path(f'M{f(sx*tw*.26)} {f(-12)}l{f(sx*tw*.22)} 0',stroke=ln,stroke_width='2',opacity='.6')
    return s
def _apron_front(p,OF,tw,lc):
    col=OF['apron']; TL=p['torsoL']; Ln=.7*p['L3']
    s=path(f'M{f(-tw*.3)} {f(-TL+34)}L{f(tw*.3)} {f(-TL+34)}L{f(tw*.4)} -10L{f(tw*.48)} {f(Ln)}L{f(-tw*.48)} {f(Ln)}L{f(-tw*.4)} -10Z',fill=col,stroke=lc,stroke_width='2.4',stroke_linejoin='round')
    s+=path(f'M{f(-tw*.3)} {f(-TL+34)}L{f(-tw*.2)} {f(-TL+2)}M{f(tw*.3)} {f(-TL+34)}L{f(tw*.2)} {f(-TL+2)}',stroke=dark(col,.3),stroke_width='3')
    s+=rect(-tw*.2,4,tw*.4,18,rx=3,fill='none',stroke=dark(col,.25),stroke_width='2',opacity='.7')
    return s
OUTFITS.update({
 'jacket':   dict(shirt='#5E6B45',sleeve='long',pants='#34465E',legs='long',shoes='#6B4A32',sole='#3A2A20',shoeStyle='boot',collar=True,pocket=True),
 'manteau':  dict(shirt='#E8DCC6',sleeve='long',pants='#2F3545',legs='long',shoes='#3A2A40',sole='#2a1d30',shoeStyle='flat',coat='#B89A72',coatLen=.78),
 'tank':     dict(shirt='#2E2E35',sleeve='none',pants='#22252D',legs='long',shoes='#1E1E22',sole='#3A3A40',shoeStyle='boot'),
 'crop_tee': dict(shirt='#22252D',sleeve='short',pants=None,legs='skirt',skirt='#3A3550',shoes='#1E1E22',sole='#F4EFE6',shoeStyle='hightop'),
 'doctor':   dict(shirt='#BFD3E6',sleeve='long',pants='#3E5A7A',legs='long',shoes='#F2F0EA',sole='#C9C3B8',coat='#F6F6F3',coatLen=.66),
 'chef':     dict(shirt='#F4F2EC',sleeve='long',pants='#3A3E47',legs='long',shoes='#22252D',sole='#111',shoeStyle='dress',apron='#ECE8DE',collar=True),
 'cardigan': dict(shirt='#B86A6A',sleeve='long',pants=None,legs='skirt',skirt='#5A5466',shoes='#7A5A6E',sole='#4a3a44',shoeStyle='flat',pocket=True),
 'sweater':  dict(shirt='#E8C468',sleeve='long',pants='#3E5A8A',legs='long',shoes='#F2F0EA',sole='#C9C3B8',shoeStyle='hightop',stripes=False),
 'tracksuit':dict(shirt='#2F6FB8',sleeve='long',pants='#2F6FB8',legs='long',shoes='#F2F0EA',sole='#E2493B',hood=False,collar=True),
 'police':   dict(shirt='#2C3E66',sleeve='long',pants='#22304F',legs='long',shoes='#15161A',sole='#0b0b0d',shoeStyle='boot',collar=True,tie='#15161A',pocket=True),
 'biker':    dict(shirt='#2B2B30',sleeve='none',pants='#34465E',legs='long',shoes='#2A2420',sole='#111',shoeStyle='boot',vest='#1A1A1E'),
 'suit_skirt':dict(shirt='#3A3550',sleeve='long',pants=None,legs='skirt',skirt='#3A3550',shoes='#1E1712',sole='#120c08',shoeStyle='heel',collar=True,lapel=True),
 'summer':   dict(shirt='#F2A65A',sleeve='short',pants='#C9B48A',legs='shorts',shoes='#8A5A3C',sole='#3A2A20',shoeStyle='sandal'),
 'pajama_cozy':dict(shirt='#C8A6D9',sleeve='long',pants='#C8A6D9',legs='long',shoes='#F2C4D6',sole='#E8A6BE',shoeStyle='slipper',stripes=True),
})
BODY.update({
 'teen':      dict(torsoW=46,armW=16,legW=19,torsoL=84,headR=39,L1=48,L2=44,L3=58,L4=56),
 'old_woman': dict(torsoW=50,armW=17,legW=21,torsoL=94,headR=38,L1=54,L2=48,L3=64,L4=60,curl=.7,lean=8),
 'tall':      dict(torsoL=112,L3=78,L4=74,L1=64,L2=58),
})
CAST.update({
 'reza':    dict(name='Reza – bearded',body='man',skin='tan',hair='side_part',hairCol='#1E1611',outfit='jacket',beard='beard_short',acc=['watch','bracelet']),
 'sara':    dict(name='Sara – hijab',body='woman',skin='warm',hair='hijab',hairCol='#7A3B4E',outfit='manteau',acc=['crossbody','rings']),
 'kai':     dict(name='Kai – tattoo artist',body='man',skin='warm',hair='undercut',hairCol='#2A2320',outfit='tank',beard='goatee',acc=['earrings','chain','bangles','rings_far'],tattoo=['sleeve@arm_near','sleeve@arm_far','star@neck','star@hand_near']),
 'luna':    dict(name='Luna – inked',body='woman',skin='tan',hair='bob',hairCol='#C8577A',outfit='crop_tee',acc=['nose_ring','earrings','eyebrow_ring','bracelet'],tattoo=['rose@forearm_near','swallow@forearm_far','wave@calf_near','moon@calf_far','heart@upperarm_near','butterfly@neck']),
 'dr_hana': dict(name='Dr. Hana – doctor',body='woman',skin='cream',hair='bob',hairCol='#2A1E18',outfit='doctor',glasses='glasses_round',acc=['stethoscope','name_tag']),
 'chef_marco':dict(name='Marco – chef',body='chubby',skin='tan',hair='short',hairCol='#2A2320',outfit='chef',beard='mustache',acc=['chef_hat'],tattoo=['anchor@forearm_near']),
 'grandma': dict(name='Grandma',body='old_woman',skin='warm',hair='bun',hairCol='#D9D4CC',outfit='cardigan',glasses='glasses_round',acc=['pearls']),
 'zoe':     dict(name='Zoe – teen',body='teen',skin='brown',hair='braid',hairCol='#24170F',outfit='sweater',acc=['earbuds','backpack','hair_bow']),
 'jay':     dict(name='Jay – athlete',body='tall',skin='deep',hair='buzz',hairCol='#120D0A',outfit='tracksuit',acc=['headband_sport','fitness_band','wristband']),
 'officer_dan':dict(name='Dan – police officer',body='man',skin='cream',hair='short',hairCol='#5A4030',outfit='police',acc=['police_cap','badge','watch']),
 'rocky':   dict(name='Rocky – biker',body='buff',skin='warm',hair=None,hairCol='#5A4030',outfit='biker',beard='full_long',acc=['sunglasses','chain','bandana','bracelet'],tattoo=['sleeve@arm_near','tribal@upperarm_far','skull@forearm_far','barcode@neck']),
 'elena':   dict(name='Elena – executive',body='woman',skin='warm',hair='wavy',hairCol='#6B3A24',outfit='suit_skirt',acc=['earrings_studs','watch','bracelet_far']),
})

_sh=CAST.pop('shadow'); CAST['shadow']=_sh
