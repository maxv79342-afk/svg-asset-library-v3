"""v3 wearables: hats, masks, piercings, earbuds/headset, chest & wrist pieces.
Head pieces are head-local (head centre 0,0, face looks to +x in side views)."""
from sv import *
GOLD='#E3B24A'; INK='#2C2A30'
def S(c,k=.55,w=2.2): return dict(fill=c,stroke=dark(c,k),stroke_width=w,stroke_linejoin='round')
def hl(d,c='#fff',op='.45',w=2.4): return path(d,fill='none',stroke=c,stroke_width=w,stroke_linecap='round',opacity=op)
def _ear(r,turn,view):
    if view in('front','back'): return None
    if turn<0: return [-r*.06,r*.06]
    return [lerp(-r*.3,-r*.62,clamp(turn,0,1)),r*.08]
def _face_cx(turn,view):
    if view=='front': return 0
    if turn<0: return r_prof
    return lerp(13,0,clamp(turn,0,1))
r_prof=20
HEAD2=('fedora','bucket_hat','top_hat','crown','cap_back','bandana','face_mask','nose_ring','earbuds','headset','party_hat','chef_hat','police_cap','beret','headband_sport','bike_helmet','hard_hat','flower_crown','hair_bow','hoop_nose','eyebrow_ring','halo','devil_horns','cat_ears')
BODY2=('stethoscope','chain','bow_tie','badge','camera_neck','guitar_back','name_tag','pearls','dog_tag')
WRIST2=('bracelet','bracelet_far','bangles','wristband','rings','rings_far','fitness_band')
def head(acc,r,turn,view):
    s=''; side=view=='side'; back=view=='back'
    for a in acc:
        if a not in HEAD2: continue
        fn=globals().get('h_'+a)
        if fn: s+=fn(r,turn,view)
    return s
def h_fedora(r,turn,view,c='#4A3F38'):
    t='' if view!='side' else ' rotate(-5)'
    s=ell(0,-r*.62,r*1.42,r*.22,**S(c))+hl(f'M{f(-r*1.1)} {f(-r*.66)}Q0 {f(-r*.8)} {f(r*1.1)} {f(-r*.66)}',light(c,.4),'.5')
    s+=path(f'M{f(-r*.74)} {f(-r*.62)}Q{f(-r*.86)} {f(-r*1.5)} {f(-r*.12)} {f(-r*1.4)}Q0 {f(-r*1.28)} {f(r*.12)} {f(-r*1.4)}Q{f(r*.86)} {f(-r*1.5)} {f(r*.74)} {f(-r*.62)}Z',**S(c))
    s+=path(f'M{f(-r*.76)} {f(-r*.8)}Q0 {f(-r*.9)} {f(r*.76)} {f(-r*.8)}L{f(r*.75)} {f(-r*.66)}Q0 {f(-r*.74)} {f(-r*.75)} {f(-r*.66)}Z',fill='#B8463A',stroke=dark('#B8463A',.5),stroke_width='1.6')
    return g(s,transform='translate(0 0)'+t)
def h_bucket_hat(r,turn,view,c='#E8C468'):
    s=path(f'M{f(-r*1.24)} {f(-r*.3)}L{f(-r*.82)} {f(-r*.74)}L{f(r*.82)} {f(-r*.74)}L{f(r*1.24)} {f(-r*.3)}Q0 {f(-r*.12)} {f(-r*1.24)} {f(-r*.3)}Z',**S(dark(c,.08)))
    s+=path(f'M{f(-r*.8)} {f(-r*.7)}Q{f(-r*.9)} {f(-r*1.4)} 0 {f(-r*1.4)}Q{f(r*.9)} {f(-r*1.4)} {f(r*.8)} {f(-r*.7)}Z',**S(c))
    s+=path(f'M{f(-r*1.0)} {f(-r*.45)}Q0 {f(-r*.3)} {f(r*1.0)} {f(-r*.45)}',fill='none',stroke=dark(c,.4),stroke_width='1.4',stroke_dasharray='3 3',opacity='.7')
    s+=hl(f'M{f(-r*.5)} {f(-r*1.15)}Q0 {f(-r*1.32)} {f(r*.4)} {f(-r*1.2)}')
    return s
def h_top_hat(r,turn,view,c='#2A2A30'):
    s=ell(0,-r*.66,r*1.2,r*.17,**S(c))
    s+=path(f'M{f(-r*.62)} {f(-r*.68)}L{f(-r*.68)} {f(-r*1.95)}Q0 {f(-r*2.05)} {f(r*.68)} {f(-r*1.95)}L{f(r*.62)} {f(-r*.68)}Q0 {f(-r*.58)} {f(-r*.62)} {f(-r*.68)}Z',**S(c))
    s+=path(f'M{f(-r*.63)} {f(-r*.95)}Q0 {f(-r*.86)} {f(r*.63)} {f(-r*.95)}L{f(r*.62)} {f(-r*.72)}Q0 {f(-r*.62)} {f(-r*.62)} {f(-r*.72)}Z',fill='#B8463A')
    s+=hl(f'M{f(-r*.4)} {f(-r*1.1)}L{f(-r*.44)} {f(-r*1.8)}',light(c,.5),'.5',3)
    return s
def h_crown(r,turn,view,c=GOLD):
    s=path(f'M{f(-r*.72)} {f(-r*.72)}L{f(-r*.8)} {f(-r*1.4)}L{f(-r*.4)} {f(-r*1.05)}L0 {f(-r*1.55)}L{f(r*.4)} {f(-r*1.05)}L{f(r*.8)} {f(-r*1.4)}L{f(r*.72)} {f(-r*.72)}Q0 {f(-r*.6)} {f(-r*.72)} {f(-r*.72)}Z',**S(c,.45))
    for x,cc in ((-r*.42,'#D6453A'),(0,'#3E8AD6'),(r*.42,'#3FA34D')): s+=circ(x,-r*.86,3.6,fill=cc,stroke=dark(cc,.5),stroke_width='1.2')
    for x,y in ((-r*.8,-r*1.4),(0,-r*1.55),(r*.8,-r*1.4)): s+=circ(x,y,3,fill=light(c,.3),stroke=dark(c,.45),stroke_width='1.2')
    return s
def h_cap_back(r,turn,view,c='#D6453A'):
    if view=='side':
        s=path(f'M{f(-r*.55)} {f(-r*.42)}Q{f(-r*1.4)} {f(-r*.55)} {f(-r*1.6)} {f(-r*.3)}Q{f(-r*1.2)} {f(-r*.2)} {f(-r*.6)} {f(-r*.3)}Z',**S(dark(c,.2)))
        s+=path(f'M{f(r*1.0)} {f(-r*.1)}C{f(r*1.05)} {f(-r*1.35)} {f(-r*.95)} {f(-r*1.35)} {f(-r*.95)} {f(-r*.4)}Z',**S(c))
    else:
        s=path(f'M{f(-r*.5)} {f(-r*1.05)}Q0 {f(-r*1.45)} {f(r*.5)} {f(-r*1.05)}',fill='none',stroke=dark(c,.5),stroke_width='6',stroke_linecap='round')
        s+=path(f'M{f(-r*1.0)} {f(-r*.3)}C{f(-r*1.05)} {f(-r*1.4)} {f(r*1.05)} {f(-r*1.4)} {f(r*1.0)} {f(-r*.3)}Z',**S(c))
        if view=='front': s+=rect(-r*.25,-r*.72,r*.5,r*.18,rx=3,fill='#F3F1EC',opacity='.8')
    s+=circ(0 if view!='side' else -r*.05,-r*1.08,3.2,fill=dark(c,.25))
    return s
def h_bandana(r,turn,view,c='#B8463A'):
    if view=='side':
        d=f'M{f(r*.92)} {f(-r*.55)}C{f(r*.7)} {f(-r*1.35)} {f(-r*1.0)} {f(-r*1.3)} {f(-r*1.02)} {f(-r*.15)}L{f(-r*.8)} {f(-r*.05)}C{f(-r*.6)} {f(-r*.75)} {f(r*.3)} {f(-r*.8)} {f(r*.85)} {f(-r*.3)}Z'
        s=path(d,**S(c))+path(f'M{f(-r*.95)} {f(-r*.2)}L{f(-r*1.45)} {f(r*.25)}L{f(-r*1.15)} {f(r*.35)}Z M{f(-r*.95)} {f(-r*.2)}L{f(-r*1.35)} {f(-r*.5)}L{f(-r*1.15)} {f(-r*.7)}Z',**S(dark(c,.12)))
    else:
        d=f'M{f(-r*1.0)} {f(-r*.3)}C{f(-r*1.05)} {f(-r*1.35)} {f(r*1.05)} {f(-r*1.35)} {f(r*1.0)} {f(-r*.3)}Q0 {f(-r*.7)} {f(-r*1.0)} {f(-r*.3)}Z'
        s=path(d,**S(c))+path(f'M{f(r*.96)} {f(-r*.3)}L{f(r*1.35)} {f(r*.1)}L{f(r*1.1)} {f(r*.2)}Z',**S(dark(c,.12)))
    rr=rnd(4)
    for i in range(7): s+=circ(rr.uniform(-r*.6,r*.6),rr.uniform(-r*1.1,-r*.75),1.6,fill='#F3F1EC',opacity='.85')
    return s
def h_face_mask(r,turn,view,c='#BFD8EC'):
    if view=='back': return path(f'M{f(-r*.95)} {f(r*.05)}Q0 {f(-r*.05)} {f(r*.95)} {f(r*.05)}',fill='none',stroke=dark(c,.4),stroke_width='1.8')
    if view=='front':
        d=f'M{f(-r*.62)} {f(r*.1)}Q0 {f(-r*.02)} {f(r*.62)} {f(r*.1)}L{f(r*.58)} {f(r*.62)}Q0 {f(r*.92)} {f(-r*.58)} {f(r*.62)}Z'
        s=path(f'M{f(-r*.62)} {f(r*.16)}L{f(-r*.98)} {f(-r*.02)}M{f(-r*.6)} {f(r*.55)}L{f(-r*.96)} {f(r*.3)}M{f(r*.62)} {f(r*.16)}L{f(r*.98)} {f(-r*.02)}M{f(r*.6)} {f(r*.55)}L{f(r*.96)} {f(r*.3)}',stroke='#F3F1EC',stroke_width='1.8',stroke_linecap='round')
    else:
        cx=_face_cx(turn,view); e=_ear(r,turn,view)
        d=f'M{f(cx-r*.42)} {f(r*.08)}Q{f(cx+r*.2)} {f(-r*.04)} {f(r*1.04)} {f(r*.18)}Q{f(r*1.08)} {f(r*.55)} {f(r*.82)} {f(r*.78)}Q{f(cx)} {f(r*.92)} {f(cx-r*.42)} {f(r*.62)}Z'
        s=path(f'M{f(cx-r*.42)} {f(r*.14)}L{P(e)}M{f(cx-r*.42)} {f(r*.56)}L{P(add(e,[0,r*.2]))}',stroke='#F3F1EC',stroke_width='1.8',stroke_linecap='round')
    s+=path(d,**S(c,.45))
    s+=g(path(d,fill='none'),)
    s+=''.join(path(f'M{f(-r*.4 if view=="front" else _face_cx(turn,view)-r*.3)} {f(r*y)}L{f(r*.4 if view=="front" else r*.9)} {f(r*y)}',stroke=dark(c,.25),stroke_width='1.4',opacity='.6') for y in (.28,.42,.56))
    return s
def h_nose_ring(r,turn,view):
    x=(_face_cx(turn,view)+(3 if view=='side' else 0)) if view!='back' else None
    if x is None: return ''
    return circ(x+2,9,2.8,fill='none',stroke=dark(GOLD,.3),stroke_width='2.6')+circ(x+2,9,2.8,fill='none',stroke=GOLD,stroke_width='1.4')
h_hoop_nose=h_nose_ring
def h_eyebrow_ring(r,turn,view):
    if view=='back': return ''
    cx=_face_cx(turn,view); sp=11.5 if view=='front' else lerp(8.5,11.5,clamp(turn,0,1))
    x=cx+sp+4
    return circ(x,-13,2.4,fill='none',stroke='#C9CED6',stroke_width='1.6')+circ(x-1,-11,1.2,fill='#C9CED6')
def h_earbuds(r,turn,view):
    pts=[[-r*.98,r*.12],[r*.98,r*.12]] if view in('front','back') else [_ear(r,turn,view)]
    s=''
    for x,y in pts: s+=ell(x,y,4.2,5.2,fill='#F3F4F6',stroke='#7A808C',stroke_width='1.4')+path(f'M{f(x)} {f(y+4)}L{f(x+(1 if view=="side" else 0))} {f(y+13)}',stroke='#F3F4F6',stroke_width='3',stroke_linecap='round')
    return s
def h_headset(r,turn,view):
    import acc as AC
    s=AC.headphones(r,turn,view,col='#2F333B',pad='#3FA3D6')
    if view=='back': return s
    if view=='front': e=[r+2,0]; m=[r*.35,r*.62]
    else: e=_ear(r,turn,view); m=[_face_cx(turn,view)+r*.18,r*.62]
    s+=path(f'M{P(e)}Q{P([e[0]+r*.2,m[1]+2])} {P(m)}',fill='none',stroke='#2F333B',stroke_width='3',stroke_linecap='round')+circ(m[0],m[1],3.6,fill='#3A3E47')
    return s
def h_party_hat(r,turn,view,c='#7C5CD6'):
    s=path(f'M{f(-r*.55)} {f(-r*.7)}L{f(r*.08)} {f(-r*1.95)}L{f(r*.6)} {f(-r*.72)}Q0 {f(-r*.55)} {f(-r*.55)} {f(-r*.7)}Z',**S(c))
    s+=path(f'M{f(-r*.36)} {f(-r*1.08)}L{f(r*.43)} {f(-r*1.1)}M{f(-r*.18)} {f(-r*1.45)}L{f(r*.27)} {f(-r*1.48)}',stroke='#FFE07A',stroke_width='4',stroke_linecap='round')
    for i in range(6): s+=circ(r*.08+math.cos(i)*4,-r*1.98+math.sin(i)*4,3.2,fill='#FF8FAB')
    return s
def h_chef_hat(r,turn,view,c='#F7F6F2'):
    s=rect(-r*.8,-r*.92,r*1.6,r*.42,rx=4,**S(c,.3))
    for x,y,rr in ((-r*.55,-r*1.18,r*.42),(r*.55,-r*1.18,r*.42),(-r*.2,-r*1.45,r*.48),(r*.25,-r*1.42,r*.46)): s+=circ(x,y,rr,**S(c,.3))
    s+=rect(-r*.78,-r*.92,r*1.56,r*.16,fill=c)+path(f'M{f(-r*.4)} {f(-r*.9)}L{f(-r*.4)} {f(-r*.55)}M{f(r*.1)} {f(-r*.9)}L{f(r*.1)} {f(-r*.55)}M{f(r*.5)} {f(-r*.9)}L{f(r*.5)} {f(-r*.55)}',stroke=dark(c,.15),stroke_width='1.4')
    return s
def h_police_cap(r,turn,view,c='#22304F'):
    s=path(f'M{f(-r*1.1)} {f(-r*1.0)}Q0 {f(-r*1.5)} {f(r*1.1)} {f(-r*1.0)}L{f(r*.85)} {f(-r*.62)}L{f(-r*.85)} {f(-r*.62)}Z',**S(c))
    s+=rect(-r*.88,-r*.78,r*1.76,r*.2,fill='#111',opacity='.85')
    if view=='side': s+=path(f'M{f(r*.6)} {f(-r*.6)}Q{f(r*1.35)} {f(-r*.62)} {f(r*1.45)} {f(-r*.4)}Q{f(r*1.0)} {f(-r*.38)} {f(r*.6)} {f(-r*.5)}Z',**S('#15161A'))
    elif view=='front': s+=path(f'M{f(-r*.8)} {f(-r*.6)}Q0 {f(-r*.35)} {f(r*.8)} {f(-r*.6)}Z',**S('#15161A'))
    if view!='back': s+=path(f'M0 {f(-r*1.18)}l4 3l-1.5 4.5h-5l-1.5 -4.5Z',fill=GOLD,stroke=dark(GOLD,.4),stroke_width='1')
    return s
def h_beret(r,turn,view,c='#B8463A'):
    tr=' rotate(-10)' if view=='side' else ' rotate(-6)'
    s=ell(-r*.05,-r*.88,r*1.12,r*.42,**S(c))+circ(-r*.05,-r*1.32,3.2,fill=dark(c,.3))+hl(f'M{f(-r*.7)} {f(-r*1.0)}Q{f(-r*.2)} {f(-r*1.22)} {f(r*.4)} {f(-r*1.12)}',light(c,.4),'.5')
    return g(s,transform='translate(0 0)'+tr)
def h_headband_sport(r,turn,view,c='#F3F1EC'):
    if view=='side': d=f'M{f(-r*.99)} {f(-r*.18)}Q{f(-r*.1)} {f(-r*.66)} {f(r*.93)} {f(-r*.44)}'
    else: d=f'M{f(-r*.99)} {f(-r*.3)}Q0 {f(-r*.82)} {f(r*.99)} {f(-r*.3)}'
    return path(d,fill='none',stroke=dark(c,.4),stroke_width='13',stroke_linecap='round')+path(d,fill='none',stroke=c,stroke_width='9.5',stroke_linecap='round')+path(d,fill='none',stroke='#2F6FB8',stroke_width='2.4',stroke_linecap='round')
def h_bike_helmet(r,turn,view,c='#3FA34D'):
    s=path(f'M{f(-r*1.08)} {f(-r*.15)}C{f(-r*1.15)} {f(-r*1.45)} {f(r*1.15)} {f(-r*1.45)} {f(r*1.1)} {f(-r*.3)}Q0 {f(-r*.5)} {f(-r*1.08)} {f(-r*.15)}Z',**S(c))
    for x in (-.5,-.15,.2,.55): s+=path(f'M{f(r*x)} {f(-r*1.15)}L{f(r*(x+.08))} {f(-r*.7)}',stroke='#1E2230',stroke_width='4',stroke_linecap='round')
    if view=='front': s+=path(f'M{f(-r*.96)} {f(-r*.15)}Q{f(-r*.8)} {f(r*.85)} 0 {f(r*1.02)}Q{f(r*.8)} {f(r*.85)} {f(r*.96)} {f(-r*.15)}',fill='none',stroke='#1E2230',stroke_width='2',opacity='.8')
    elif view=='side':
        e=_ear(r,turn,view); s+=path(f'M{f(e[0])} {f(-r*.2)}L{P(e)}Q{f(e[0]+r*.05)} {f(r*.85)} {f(r*.35)} {f(r*1.0)}',fill='none',stroke='#1E2230',stroke_width='2',opacity='.8')
    return s
def h_hard_hat(r,turn,view,c='#F2C230'):
    s=ell(0,-r*.5,r*1.3,r*.16,**S(c))+path(f'M{f(-r*.95)} {f(-r*.52)}C{f(-r*1.0)} {f(-r*1.5)} {f(r*1.0)} {f(-r*1.5)} {f(r*.95)} {f(-r*.52)}Z',**S(c))
    s+=path(f'M0 {f(-r*1.27)}L0 {f(-r*.55)}',stroke=dark(c,.25),stroke_width='5',stroke_linecap='round')+hl(f'M{f(-r*.6)} {f(-r*.9)}Q{f(-r*.4)} {f(-r*1.2)} {f(-r*.1)} {f(-r*1.24)}')
    return s
def h_flower_crown(r,turn,view):
    s=''; cols=['#F2A6B8','#FFE07A','#F3F1EC','#E8455A','#B8A6F2']
    for i in range(7):
        a=(-165+i*25)*D; x=math.cos(a)*r*.98; y=math.sin(a)*r*.98-2
        c=cols[i%5]
        for k in range(5): s+=circ(x+math.cos(k*72*D)*3.6,y+math.sin(k*72*D)*3.6,3.4,fill=c,stroke=dark(c,.45),stroke_width='1')
        s+=circ(x,y,2.2,fill='#E9A23B')
        if i%2: s+=path(f'M{f(x+4)} {f(y+2)}q5 -2 7 3q-5 1 -7 -3Z',fill='#5FB55A')
    return s
def h_hair_bow(r,turn,view,c='#E8455A'):
    x,y=((r*.45,-r*.95) if view=='front' else (-r*.2,-r*1.02))
    s=path(f'M{f(x)} {f(y)}L{f(x-14)} {f(y-10)}Q{f(x-18)} {f(y)} {f(x-14)} {f(y+10)}Z M{f(x)} {f(y)}L{f(x+14)} {f(y-10)}Q{f(x+18)} {f(y)} {f(x+14)} {f(y+10)}Z',**S(c))
    return s+circ(x,y,4,**S(dark(c,.1)))
def h_halo(r,turn,view):
    return ell(0,-r*1.38,r*.7,r*.16,fill='none',stroke='#C9A23B',stroke_width='7')+ell(0,-r*1.38,r*.7,r*.16,fill='none',stroke='#FFE07A',stroke_width='4')
def h_devil_horns(r,turn,view,c='#D6453A'):
    s=''
    for sx in ((-1,1) if view!='side' else (-.4,.55)):
        x=sx*r*.55; s+=path(f'M{f(x-7)} {f(-r*.8)}Q{f(x-2)} {f(-r*1.35)} {f(x+sx*8)} {f(-r*1.45)}Q{f(x+3)} {f(-r*1.1)} {f(x+7)} {f(-r*.82)}Z',**S(c))
    return s
def h_cat_ears(r,turn,view,c='#2F333B'):
    s=''
    for sx in ((-1,1) if view!='side' else (-.45,.45)):
        x=sx*r*.62; s+=path(f'M{f(x-12)} {f(-r*.72)}L{f(x)} {f(-r*1.42)}L{f(x+12)} {f(-r*.78)}Z',**S(c))+path(f'M{f(x-6)} {f(-r*.82)}L{f(x)} {f(-r*1.22)}L{f(x+6)} {f(-r*.84)}Z',fill='#F2A6B8')
    if view!='side': s+=path(f'M{f(-r*.9)} {f(-r*.5)}Q0 {f(-r*1.3)} {f(r*.9)} {f(-r*.5)}',fill='none',stroke=c,stroke_width='4')
    return s
# ------------------------------------------------------------------ body pieces
def body_side(ACC,neck,back,sd,tw,q,p):
    s=''; fr=mul(back,-1)
    def chest(u,k=.5): return add(q(u),mul(fr,tw*k))
    if 'stethoscope' in ACC:
        a=add(neck,mul(back,tw*.2)); b=chest(.55,.42)
        s+=path(f'M{P(a)}Q{P(add(chest(.85,.6),mul(sd,4)))} {P(b)}',fill='none',stroke='#2F333B',stroke_width='3.4',stroke_linecap='round')
        s+=circ(b[0],b[1],5.6,fill='#C9CED6',stroke='#5A606C',stroke_width='1.8')
    if 'chain' in ACC:
        a=add(neck,mul(back,-tw*.05)); b=chest(.78,.48)
        s+=path(f'M{P(a)}Q{P(add(b,mul(sd,10)))} {P(b)}',fill='none',stroke=GOLD,stroke_width='3.4',stroke_dasharray='3 1.5',stroke_linecap='round')+circ(b[0],b[1]+3,4.4,fill=GOLD,stroke=dark(GOLD,.4),stroke_width='1.2')
    if 'pearls' in ACC:
        a=add(neck,mul(back,-tw*.05)); b=chest(.86,.48)
        for i in range(8):
            t=i/7; pt=[(1-t)**2*a[0]+2*(1-t)*t*(b[0])+t*t*b[0],(1-t)**2*a[1]+2*(1-t)*t*(b[1]+6)+t*t*b[1]]
            s+=circ(pt[0],pt[1],2.4,fill='#F7F3EA',stroke='#B8AE9C',stroke_width='.8')
    if 'dog_tag' in ACC:
        a=add(neck,mul(back,-tw*.05)); b=chest(.72,.5)
        s+=path(f'M{P(a)}L{P(b)}',stroke='#9AA3AF',stroke_width='1.6')+g(rect(-4,0,8,12,rx=3,fill='#C9CED6',stroke='#5A606C',stroke_width='1.2'),transform=f'translate({f(b[0])} {f(b[1])})')
    if 'bow_tie' in ACC:
        c=chest(.97,.42)
        s+=path(f'M{P(c)}l-7 -5l0 10Z M{P(c)}l7 -5l0 10Z',**S('#B8463A',.5,1.6))+circ(c[0],c[1],2.6,fill=dark('#B8463A',.2))
    if 'badge' in ACC:
        c=chest(.72,.38); s+=_star(c,7,GOLD)
    if 'name_tag' in ACC:
        c=chest(.7,.4); s+=g(rect(-8,-5,16,10,rx=2,fill='#F3F1EC',stroke='#5A6676',stroke_width='1.4')+path('M-5 0 L5 0',stroke='#3E6A8A',stroke_width='1.6'),transform=f'translate({f(c[0])} {f(c[1])}) rotate({f(-p["lean"])})')
    if 'camera_neck' in ACC:
        a=add(neck,mul(back,tw*.15)); b=chest(.45,.62)
        s+=path(f'M{P(a)}Q{P(chest(.8,.75))} {P(b)}',fill='none',stroke='#2F333B',stroke_width='3')
        s+=g(rect(-13,-9,26,18,rx=4,fill='#2F333B',stroke='#15161A',stroke_width='1.6')+circ(4,0,6.4,fill='#5A606C',stroke='#15161A',stroke_width='1.4')+circ(4,0,3,fill='#9FC4E8'),transform=f'translate({f(b[0])} {f(b[1])}) rotate({f(-p["lean"])})')
    if 'guitar_back' in ACC:
        c=add(q(.55),mul(back,tw*.62))
        s=g(ell(0,30,22,26,**S('#B8794A'))+ell(0,4,16,18,**S('#B8794A'))+circ(0,18,6,fill='#3A2E26')+rect(-3.4,-70,6.8,74,fill='#5A3E2A')+rect(-5,-84,10,16,rx=2,fill='#3A2E26'),transform=f'translate({f(c[0])} {f(c[1])}) rotate({f(-p["lean"]+15)})')+s
    return s
def _star(c,R,col):
    pts=[]
    for i in range(10):
        a=(-90+i*36)*D; rr=R if i%2==0 else R*.45; pts.append([c[0]+math.cos(a)*rr,c[1]+math.sin(a)*rr])
    return path('M'+'L'.join(P(p) for p in pts)+'Z',**S(col,.4,1.2))
def body_front(ACC,TL,tw,backv,p):
    if backv:
        s=''
        if 'guitar_back' in ACC: s+=g(ell(0,30,26,30,**S('#B8794A'))+ell(0,-6,19,21,**S('#B8794A'))+rect(-4,-90,8,70,fill='#5A3E2A'),transform=f'translate(-6 {f(-TL*.45)}) rotate(14)')
        return s
    s=''
    if 'stethoscope' in ACC:
        s+=path(f'M{f(-tw*.22)} {f(-TL+2)}Q{f(-tw*.3)} {f(-TL+40)} {f(-tw*.12)} {f(-TL+56)}M{f(tw*.22)} {f(-TL+2)}Q{f(tw*.3)} {f(-TL+40)} {f(tw*.12)} {f(-TL+56)}Q0 {f(-TL+66)} {f(-tw*.12)} {f(-TL+56)}',fill='none',stroke='#2F333B',stroke_width='3.2')
        s+=circ(0,-TL+64,5.4,fill='#C9CED6',stroke='#5A606C',stroke_width='1.6')
    if 'chain' in ACC: s+=path(f'M{f(-tw*.2)} {f(-TL+3)}Q0 {f(-TL+34)} {f(tw*.2)} {f(-TL+3)}',fill='none',stroke=GOLD,stroke_width='3.4',stroke_dasharray='3 1.5')+circ(0,-TL+22,4.6,fill=GOLD,stroke=dark(GOLD,.4),stroke_width='1.2')
    if 'pearls' in ACC:
        for i in range(11):
            t=i/10; x=lerp(-tw*.2,tw*.2,t); y=-TL+3+math.sin(t*math.pi)*16; s+=circ(x,y,2.4,fill='#F7F3EA',stroke='#B8AE9C',stroke_width='.8')
    if 'dog_tag' in ACC: s+=path(f'M{f(-tw*.18)} {f(-TL+3)}L0 {f(-TL+30)}L{f(tw*.18)} {f(-TL+3)}',fill='none',stroke='#9AA3AF',stroke_width='1.6')+rect(-4,-TL+30,8,12,rx=3,fill='#C9CED6',stroke='#5A606C',stroke_width='1.2')
    if 'bow_tie' in ACC: s+=path(f'M0 {f(-TL+8)}l-10 -6l0 12Z M0 {f(-TL+8)}l10 -6l0 12Z',**S('#B8463A',.5,1.6))+circ(0,-TL+8,3,fill=dark('#B8463A',.2))
    if 'badge' in ACC: s+=_star([-tw*.24,-TL+34],8,GOLD)
    if 'name_tag' in ACC: s+=rect(tw*.1,-TL+30,18,11,rx=2,fill='#F3F1EC',stroke='#5A6676',stroke_width='1.4')
    if 'camera_neck' in ACC:
        s+=path(f'M{f(-tw*.22)} {f(-TL+2)}L0 {f(-TL+52)}L{f(tw*.22)} {f(-TL+2)}',fill='none',stroke='#2F333B',stroke_width='3')
        s+=g(rect(-15,-10,30,20,rx=4,fill='#2F333B',stroke='#15161A',stroke_width='1.6')+circ(0,0,7,fill='#5A606C',stroke='#15161A',stroke_width='1.4')+circ(0,0,3.4,fill='#9FC4E8'),transform=f'translate(0 {f(-TL+58)})')
    if 'guitar_back' in ACC: s+=path(f'M{f(-tw*.3)} {f(-TL+4)}L{f(tw*.42)} -20',stroke='#5A3E2A',stroke_width='4.4',stroke_linecap='round')
    return s
def wrist(ACC,A,which):
    s=''; W=A['T']; a=A['la']
    def band(k,col,w=4.2,ln=None):
        c=add(W,mul(dirv(a),-k)); n=rot(dirv(a),90)
        p1=add(c,mul(n,10.5)); p2=add(c,mul(n,-10.5))
        return path(f'M{P(p1)}L{P(p2)}',stroke=ln or dark(col,.45),stroke_width=f(w+2),stroke_linecap='round')+path(f'M{P(p1)}L{P(p2)}',stroke=col,stroke_width=f(w),stroke_linecap='round')
    if ('bracelet' in ACC and which=='near') or ('bracelet_far' in ACC and which=='far'): s+=band(9,GOLD,3)
    if 'bangles' in ACC and which=='near': s+=band(7,GOLD,2.4)+band(11,'#D6453A',2.4)+band(15,'#3FA3D6',2.4)
    if 'wristband' in ACC and which=='far': s+=band(9,'#2F6FB8',7)
    if 'fitness_band' in ACC and which=='far': s+=band(8,'#2F333B',5)+circ(*add(W,mul(dirv(a),-8)),3,fill='#7FE0A8')
    if ('rings' in ACC and which=='near') or ('rings_far' in ACC and which=='far'): s+=band(-14,'#C9CED6',2.2,'#5A606C')
    return s
