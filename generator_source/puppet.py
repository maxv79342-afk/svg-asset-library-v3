"""v3 cut-out puppet kits: every body segment as its own SVG with its pivot at (0,0),
plus rig.json (hierarchy + pivots) for After Effects / Spine / Moho / Rive / GSAP."""
from sv import *
import rig, tattoo as TT, json
def _clip(inner,box,cid):
    x,y,w,h=box
    return f'<defs><clipPath id="{cid}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"/></clipPath></defs>'+g(inner,clip_path=f'url(#{cid})')
def parts(ck):
    a=rig.cast_args(ck); p=rig.base_pose(**a)
    sk,lc=rig.SKINS.get(p['skin'],rig.SKINS['cream'])
    OF=rig.OUTFITS.get(p['outfit']) if isinstance(p['outfit'],(str,type(None))) else p['outfit']
    L1,L2,L3,L4=p['L1'],p['L2'],p['L3'],p['L4']; aw,lw=p['armW'],p['legW']
    out={}
    for side in ('near','far'):
        far=side=='far'
        scol=OF and OF.get('shirt'); scol=dark(scol,.12) if (scol and far) else scol
        # upper arm
        L=rig.Layer(lc); L.st(f'M0 0 L0 {f(L1)}',aw,sk)
        tat=''
        if p.get('tattoo'):
            tat=_clip(TT.arm(p,[0,0],dict(J=[0,L1],T=[0,L1+L2]),side,aw),(-aw,-aw,2*aw,L1+aw*.5),f'cu{ck}{side}')
        if tat: L.raw(tat)
        if OF and OF['sleeve']!='none':
            e=L1*.62 if OF['sleeve']=='short' else L1
            L.st(f'M0 0 L0 {f(e)}',aw+4,scol)
        out[f'upper_arm_{side}']=L.out()
        # forearm
        L=rig.Layer(lc); L.st(f'M0 0 L0 {f(L2)}',aw,sk)
        if p.get('tattoo'): L.raw(_clip(g(TT.arm(p,[0,-L1],dict(J=[0,0],T=[0,L2]),side,aw)),(-aw,-aw*.5,2*aw,L2+aw),f'cf{ck}{side}'))
        if OF and OF['sleeve']=='long': L.st(f'M0 0 L0 {f(L2*.86)}',aw+4,scol)
        out[f'forearm_{side}']=L.out()
        # legs
        pc=OF and OF.get('pants'); pc=dark(pc,.12) if (pc and far) else pc
        L=rig.Layer(lc); L.st(f'M0 0 L0 {f(L3)}',lw,sk)
        if OF and OF['legs']=='long' and pc: L.st(f'M0 0 L0 {f(L3)}',lw+3,pc)
        elif OF and OF['legs']=='shorts' and pc: L.st(f'M0 0 L0 {f(L3*.62)}',lw+4,pc,cap='butt')
        out[f'thigh_{side}']=L.out()
        L=rig.Layer(lc); L.st(f'M0 0 L0 {f(L4)}',lw,sk)
        if p.get('tattoo'): L.raw(TT.leg(p,[0,-L3],dict(J=[0,0],T=[0,L4]),side))
        if OF and OF['legs']=='long' and pc: L.st(f'M0 0 L0 {f(L4)}',lw+3,pc)
        out[f'shin_{side}']=L.out()
        if OF and OF.get('shoes'): out[f'foot_{side}']=rig.shoe([0,0],90,dark(OF['shoes'],.1) if far else OF['shoes'],OF.get('sole','#F4EFE6'),style=OF.get('shoeStyle','sneaker'),skin=sk)
        else:
            L=rig.Layer(lc); L.st('M-5 0 Q10 2.5 25 0',15.5,sk); out[f'foot_{side}']=L.out()
    for hk in rig.HAND_SPEC:
        L=rig.Layer(lc); rig.hand(L,[0,0],0,hk,sk); out[f'hand_{hk}']=L.out()
    # torso (hip origin) and head (head-centre origin)
    q=dict(a); q.update(turn=.15,hide={'arm_far','arm_near','leg_far','leg_near','head'})
    if ck=='shadow': q.update(eyes='glow',brow='none')
    t,J=rig.char(**q); out['torso']=t
    for ex in ('neutral','happy','sad','angry','shocked','laugh'):
        out[f'head_{ex}']=rig.head_only(turn=.15,view='side',expr=ex,**a) if ck!='shadow' else rig.head_only(turn=.15,view='side',expr=ex,**dict(a,eyes='glow',brow='none'))
    # pivots (rest pose, lean=0) -- mirrors rig._side
    TLn=p['torsoL']; neck=[0,-TLn]; a0=[0,-4]; c2=[0,-TLn*.55]
    u=.86; sh=[(1-u)**2*a0[i]+2*(1-u)*u*c2[i]+u*u*neck[i] for i in (0,1)]; sh=[sh[0]-1,sh[1]]
    sN=[sh[0]+1.5,sh[1]]; sF=[sh[0]-4,sh[1]]; head=[0,-TLn-6-p['headR']*.92]
    rigj=dict(character=ck,units='px (1 unit = 1 svg user unit)',root='torso',
      bones={
        'torso':dict(parent=None,pivot=[0,0],note='pivot = hips'),
        'head':dict(parent='torso',attach=neck,pivot_in_part=[0,p['headR']*.92+6],files=[f'head_{e}.svg' for e in ('neutral','happy','sad','angry','shocked','laugh')]),
        'upper_arm_near':dict(parent='torso',attach=sN,length=L1),'forearm_near':dict(parent='upper_arm_near',attach=[0,L1],length=L2),'hand_near':dict(parent='forearm_near',attach=[0,L2],files='hand_*.svg'),
        'upper_arm_far':dict(parent='torso',attach=sF,length=L1,z='behind torso'),'forearm_far':dict(parent='upper_arm_far',attach=[0,L1],length=L2),'hand_far':dict(parent='forearm_far',attach=[0,L2]),
        'thigh_near':dict(parent='torso',attach=[2.5,3],length=L3),'shin_near':dict(parent='thigh_near',attach=[0,L3],length=L4),'foot_near':dict(parent='shin_near',attach=[0,L4]),
        'thigh_far':dict(parent='torso',attach=[-2.5,3],length=L3,z='behind torso'),'shin_far':dict(parent='thigh_far',attach=[0,L3],length=L4),'foot_far':dict(parent='shin_far',attach=[0,L4]),
      },
      draw_order=['upper_arm_far','forearm_far','hand_far','thigh_far','shin_far','foot_far','thigh_near','shin_near','foot_near','torso','head','upper_arm_near','forearm_near','hand_near'],
      rotation='degrees, 0 = limb hanging straight down, positive = swing forward (toward +x)')
    return out,rigj
