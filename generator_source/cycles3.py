"""v3 motion: 24-frame loops built from phase functions + eased keyframes.
Every numeric pose parameter (angles, IK targets, finger specs) is interpolated, so
transitions between hand shapes, expressions and body poses are smooth."""
from sv import *
import rig
N=24
DEF=dict(lean=0,curl=0,head=0,aN=[8,14],aF=[-8,16],wN=0,wF=0,lN=[3,3],lF=[-3,3],fN=0,fF=0,y=0,turn=.15,air=0)
def ease(u): return u*u*(3-2*u)
def ease_io(u): return .5-.5*math.cos(u*math.pi)
def _mix(a,b,t,k):
    if a is None: return b
    if b is None: return a
    if k in('hN','hF'):
        if a==b: return a
        return rig.hand_lerp(a,b,t)
    if isinstance(a,(int,float)) and isinstance(b,(int,float)): return lerp(a,b,t)
    if isinstance(a,(list,tuple)) and isinstance(b,(list,tuple)) and len(a)==len(b) and all(isinstance(x,(int,float)) for x in list(a)+list(b)):
        r=[lerp(a[i],b[i],t) for i in range(len(a))]; return tuple(r) if isinstance(a,tuple) else r
    return a if t<.5 else b
def keyframes(keys,n=N,loop=True,e=ease):
    """keys: [(t0,dict),...] t in 0..1 ; returns n frame dicts"""
    allk=set()
    for _,d in keys: allk|=set(d)
    out=[]
    for i in range(n):
        t=i/n if loop else i/(n-1)
        ks=keys+([(1.0,keys[0][1])] if loop and keys[-1][0]<1 else [])
        for j in range(len(ks)-1):
            if ks[j][0]<=t<=ks[j+1][0]: a,b=ks[j],ks[j+1]; break
        else: a=b=ks[-1]
        u=0 if b[0]==a[0] else (t-a[0])/(b[0]-a[0]); u=e(u)
        fr={}
        for k in allk:
            fr[k]=_mix(a[1].get(k,DEF.get(k)),b[1].get(k,DEF.get(k)),u,k)
        out.append(fr)
    return out
TAU=2*math.pi
LFULL=[126]
# ---------------- locomotion ----------------
def walk3(i,style='normal',n=N):
    ph=i/n*TAU; s=math.sin(ph); c=math.cos(ph); sF=-s; cF=-c
    amp=dict(normal=1,sad=.78,happy=1.12,sneak=.85,phone=.85,old=.55,strut=1.05)[style]
    kb=dict(normal=6,sad=6,happy=8,sneak=34,phone=6,old=12,strut=4)[style]
    knee=lambda cc: kb+44*max(0,cc)**1.4*amp
    lag=.55  # arms follow through
    sl=math.sin(ph-lag)
    d=dict(lN=[26*s*amp+(10 if style=='sneak' else 0),knee(c)],lF=[26*sF*amp+(10 if style=='sneak' else 0),knee(cF)],
           fN=-8*s*amp+(10*max(0,-c)*amp if s<0 else 0), fF=-8*sF*amp+(10*max(0,-cF)*amp if sF<0 else 0),
           aN=[-24*sl*amp,18+10*max(0,-sl)*amp],aF=[24*sl*amp,18+10*max(0,sl)*amp],
           lean=4*amp+1.2*math.sin(2*ph),head=-2+1.6*math.sin(2*ph+.9),ground=True)
    if style=='sad': d.update(curl=.8,lean=8+1*math.sin(2*ph),head=16+1.5*math.sin(2*ph+.9),expr='sad')
    if style=='happy':
        d.update(lean=-1+1.5*math.sin(2*ph),head=-8+2.5*math.sin(2*ph+.9),expr='happy',aN=[-34*sl,30+16*max(0,-sl)],aF=[34*sl,30+16*max(0,sl)],hN='open',hF='open',bounce=-6*abs(math.sin(ph))+3)
    if style=='sneak':
        d.update(lean=24+1.5*math.sin(2*ph),curl=.5,head=-12,aN=[40+10*sl,80],aF=[30-10*sl,86],hN='relax',hF='relax',expr='nervous',look=(-.6+.4*math.sin(ph),0))
    if style=='phone':
        d.update(head=20+1*math.sin(2*ph+.9),lean=6,ikN=[42,-58],hN='grip',wN=-35,look=(.5,.8),expr='focused',phone=True)
    if style=='old':
        d.update(curl=.9,lean=12+1*math.sin(2*ph),head=8,aN=[-12*sl,20],aF=[12*sl,24],expr='content')
    if style=='strut':
        d.update(lean=-4+1*math.sin(2*ph),head=-10+1.5*math.sin(2*ph+.9),aN=[-30*sl,12],aF=[30*sl,12],expr='smug')
    return d
def run3(i,amp=1,n=N):
    ph=i/n*TAU; s=math.sin(ph); c=math.cos(ph); sF=-s; cF=-c
    knee=lambda cc: 18+88*max(0,cc)**1.1*amp
    sl=math.sin(ph-.35)
    return dict(lN=[44*s*amp+6,knee(c)],lF=[44*sF*amp+6,knee(cF)],fN=-10*s+18*max(0,-c),fF=-10*sF+18*max(0,-cF),
        aN=[-48*sl*amp+6,82],aF=[48*sl*amp+6,82],hN='fist',hF='fist',
        y=-9*amp*abs(math.sin(ph+.2)),lean=12*amp+1.5*math.sin(2*ph),head=-6+2*math.sin(2*ph+1),expr='determined' if amp>.8 else 'content')
# ---------------- idles & gestures ----------------
def _blink(i,at=(15,16)): return dict(eyes='closed') if i in at else {}
def idle(i,n=N):
    ph=i/n*TAU; s=math.sin(ph)
    d=dict(lean=1.2*s,head=-1+1.4*math.sin(ph+.6),aN=[8+2.4*math.sin(ph+.4),14+3*s],aF=[-8+2*math.sin(ph+.8),16+3*s],hN='relax_hang',hF='relax_hang',ground=True,expr='neutral')
    d.update(_blink(i)); return d
VIS=['v_AI','v_E','v_O','v_MBP','v_AI','v_L','v_E','v_rest','v_O','v_U','v_CDG','v_AI','v_FV','v_E','v_MBP','v_rest','v_AI','v_O','v_TH','v_E','v_WQ','v_AI','v_MBP','v_rest']
def talk(i,n=N):
    ks=keyframes([(0,dict(aN=[48,62],hN='spread',wN=-60,head=-2,lean=0)),(.25,dict(aN=[60,50],hN='open',wN=-40,head=2,lean=2)),
                  (.5,dict(aN=[40,80],hN='count_1',wN=-80,head=-1,lean=1)),(.75,dict(aN=[56,58],hN='karate',wN=-50,head=3,lean=2))],n)[i]
    ks.update(aF=[-6,14],expr='happy',mouth=VIS[i%len(VIS)],ground=True); ks.update(_blink(i,(9,10))); return ks
def wave(i,n=N):
    ph=i/n*TAU*2; s=math.sin(ph)
    return dict(aN=[148,-38+26*s],wN=14*math.sin(ph-.6),hN=rig.hand_lerp('wave_a','wave_b',(math.sin(ph-1.2)+1)/2),aF=[-6,14],lean=-1+1*s,head=-4+1.5*math.sin(ph+.5),expr='happy',ground=True)
def jump(i,n=N):
    ks=keyframes([(0,dict(lN=[3,3],lF=[-3,3],aN=[8,14],aF=[-8,16],lean=0,air=0,head=0,expr='neutral')),
                  (.18,dict(lN=[52,100],lF=[44,96],aN=[-40,30],aF=[-46,34],lean=22,air=0,head=6,fN=-8,fF=-8,expr='determined')),
                  (.32,dict(lN=[-6,4],lF=[-12,6],aN=[150,-10],aF=[140,10],lean=-4,air=-60,head=-10,fN=40,fF=40,hN='spread',hF='spread',expr='joy')),
                  (.5,dict(lN=[60,90],lF=[50,96],aN=[160,-20],aF=[150,0],lean=-2,air=-118,head=-12,fN=10,fF=10,hN='spread',hF='spread',expr='joy')),
                  (.68,dict(lN=[10,14],lF=[4,14],aN=[110,20],aF=[100,30],lean=4,air=-30,head=-4,hN='open',hF='open',expr='joy')),
                  (.8,dict(lN=[48,92],lF=[40,90],aN=[40,40],aF=[30,44],lean=18,air=0,head=6,expr='happy')),
                  (.92,dict(lN=[8,10],lF=[0,10],aN=[10,16],aF=[-6,18],lean=2,air=0,head=0,expr='happy'))],n)[i]
    ks['ground']=True; return ks
def cheer(i,n=N):
    ph=i/n*TAU*2; s=math.sin(ph); up=(s+1)/2
    return dict(aN=[130+30*up,30-24*up],aF=[120+34*(1-up),36-26*(1-up)],hN='fist',hF='fist',lean=-4,head=-12+3*s,lN=[8,6+10*(1-up)],lF=[-8,6+10*up],air=-14*abs(math.sin(ph/2*2)),expr='joy',ground=True)
def laugh(i,n=N):
    ph=i/n*TAU*3; s=math.sin(ph)
    return dict(lean=4+6*s,head=-8+8*math.sin(ph+.5),ikN=[30,-36],ikF=[24,-30],hN='open',hF='open',wN=-90,wF=-90,expr='laugh',mouth='laugh' if s>0 else 'v_AI',ground=True)
def nod(i,n=N):
    ph=i/n*TAU*2; return dict(head=6+11*math.sin(ph),lean=1.5*math.sin(ph-.4),expr='happy',ground=True,**_blink(i,(18,)))
def shake(i,n=N):
    ph=i/n*TAU*2; return dict(turn=.32+.3*math.sin(ph),head=2+2*math.sin(ph*2),look=(-.8*math.sin(ph),0),expr='annoyed',ground=True)
def dance(i,n=N):
    ph=i/n*TAU*2; s=math.sin(ph); c=math.cos(ph)
    return dict(lean=-2+7*s,head=-6+5*math.sin(ph+.8),aN=[140*max(0,s)+20,20+40*max(0,-s)],aF=[140*max(0,-s)+20,20+40*max(0,s)],hN='point' if s>0 else 'fist',hF='point' if s<0 else 'fist',
                lN=[10*s+6,10+24*max(0,c)],lF=[-10*s-6,10+24*max(0,-c)],air=-6*abs(c),expr='joy',ground=True)
def cry(i,n=N):
    ph=i/n*TAU*3; s=math.sin(ph)
    return dict(lean=6+3*s,curl=.5,head=18+3*math.sin(ph+.6),ikN=[34,-132+3*s],ikF=[28,-128+3*s],hN='open',hF='open',wN=-170,wF=-170,expr='sobbing',ground=True)
def typing(i,n=N):
    ph=i/n*TAU*4
    d=dict(y=70,lean=10,head=10+1.2*math.sin(ph/4),legIkN=[66,70],legIkF=[58,72],ikN=[86,-30+3*max(0,math.sin(ph))],ikF=[78,-24+3*max(0,-math.sin(ph))],hN='tap' if math.sin(ph)<0 else 'flat',hF='tap' if math.sin(ph)>0 else 'flat',wN=-60,wF=-60,look=(.8,.4),expr='focused')
    d.update(_blink(i,(12,))); return d
def stand_to_sit(i,n=N):
    L_=LFULL[0]
    ks=keyframes([(0,dict(y=0,legIkN=[3,L_],legIkF=[-3,L_],lean=0,head=0,aN=[8,14],aF=[-8,16])),
                  (.45,dict(y=34,legIkN=[38,L_*.78],legIkF=[30,L_*.78],lean=26,head=-4,aN=[50,20],aF=[40,24])),
                  (1,dict(y=70,legIkN=[66,70],legIkF=[58,72],lean=2,head=0,aN=[36,40],aF=[30,46]))],n,loop=False,e=ease_io)[i]
    ks['expr']='neutral'; return ks
def clap(i,n=N):
    ph=i/n*TAU*3; o=(1+math.cos(ph))/2
    return dict(view='front',ikN=[7+16*o,-56,-1],ikF=[-7-16*o,-56,-1],hN='flat',hF='flat',expr='joy',ground=True)
def front_idle(i,n=N):
    ph=i/n*TAU; s=math.sin(ph)
    d=dict(view='front',aN=[12+2*s,6+3*s],aF=[12+2*math.sin(ph+.5),6+3*s],head=1.6*math.sin(ph+.6),hN='relax_hang',hF='relax_hang',expr='neutral')
    d.update(_blink(i,(14,15))); return d
CYCLES={
 'walk':lambda i: walk3(i,'normal'),'walk_sad':lambda i: walk3(i,'sad'),'walk_happy':lambda i: walk3(i,'happy'),
 'walk_strut':lambda i: walk3(i,'strut'),'walk_phone':lambda i: walk3(i,'phone'),'sneak':lambda i: walk3(i,'sneak'),
 'run':lambda i: run3(i,1),'jog':lambda i: run3(i,.62),
 'idle_breathe':idle,'idle_front':front_idle,'talk':talk,'wave':wave,'jump':jump,'cheer':cheer,'laugh':laugh,
 'nod_yes':nod,'shake_no':shake,'dance':dance,'cry':cry,'typing':typing,'stand_to_sit':stand_to_sit,'clap_front':clap,
}
GROUND_FREE={'run','jog','typing','stand_to_sit'}
def frame_params(a,ck,cyc,i,phone_fn=None):
    """turn a cycle frame dict into rig.char kwargs for cast args `a`"""
    hy=rig.hip_h(a)
    Lfull=a.get('L3',72)+a.get('L4',68)-2
    LFULL[0]=Lfull
    d=dict(CYCLES[cyc](i))
    for k in('legIkN','legIkF'):
        if k in d and isinstance(d[k],list):
            v=list(d[k])
            if v[1]=='L': v[1]=Lfull
            elif v[1]=='L2': v[1]=Lfull*.78
            d[k]=v
    ground=d.pop('ground',False); air=d.pop('air',0); bounce=d.pop('bounce',0); phone=d.pop('phone',False)
    q=dict(a); q.update(d)
    if a.get('acc'): q['acc']=list(a['acc'])
    if ck=='shadow': q.update(eyes='glow',brow='none',fx=[])
    if phone and phone_fn: q['holdN']=phone_fn()
    q['y']=-hy+q.pop('y',0)
    if ground and q.get('view','side')=='side':
        q2=dict(q); _,J=rig.char(**q2)
        low=max(J['footN'][1],J['footF'][1])
        q['y']=-(low+7)+air
    elif ground: q['y']+=air
    return q
