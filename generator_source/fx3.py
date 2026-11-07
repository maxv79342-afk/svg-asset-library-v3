"""v3 FX: frame-by-frame effect sequences (12 frames) + full-frame weather overlays."""
from sv import *
INK='#221E1B'
def _e(t): return 1-(1-t)**3
def dust_puff(t):
    s=''; k=_e(t); op=f(max(0,1-t*1.05))
    for i,(a,r0) in enumerate(((200,26),(160,34),(250,22),(130,20),(290,18),(180,28))):
        c=add([0,-10],mul(dirv(a),20+90*k)); s+=circ(c[0],c[1],r0*(.6+k*.9),fill='#D9D2C4',opacity=op,stroke='#B8AE9C',stroke_width=2)
    return s
def sparkle_burst(t):
    s=''; k=_e(t)
    for i in range(8):
        a=i*45; c=mul(dirv(a),20+110*k); sc=(1-t)*1.1*(1 if i%2 else .7)
        s+=g(path('M0 -30 Q3 -3 30 0 Q3 3 0 30 Q-3 3 -30 0 Q-3 -3 0 -30Z',fill='#FFE07A'),transform=f'translate({f(c[0])} {f(c[1])}) scale({f(max(sc,.01))}) rotate({f(t*90)})')
    s+=circ(0,0,40*(1-t),fill='#FFF3C4',opacity=f(max(0,.8-t)))
    return s
def smoke_rise(t):
    s=''
    for i in range(5):
        u=(t+i/5)%1; y=-u*260; x=math.sin(u*6+i)*24; r=18+u*44
        s+=circ(x,y,r,fill='#8A8F99',opacity=f(.55*(1-u)))
    return s
def impact_star(t):
    sc=.4+1.2*_e(min(1,t*2)); op=f(1 if t<.6 else max(0,1-(t-.6)*2.5))
    pts=[]
    for i in range(16):
        a=(-90+i*22.5)*D; rr=110 if i%2==0 else 50; pts.append([math.cos(a)*rr,math.sin(a)*rr])
    return g(path('M'+'L'.join(P(p) for p in pts)+'Z',fill='#FFE07A',stroke=INK,stroke_width=5,stroke_linejoin='round')+text('POW!',0,14,size=40,fill='#E2493B',weight=900,anchor='middle',family="'Bebas Neue',Impact,sans-serif"),transform=f'scale({f(sc)}) rotate({f(-8+t*16)})',opacity=op)
def heart_pop(t):
    s=''
    for i,(x0,dl,sc0) in enumerate(((0,0,1.2),(-50,.15,.8),(46,.3,.7),(-20,.45,.6))):
        u=clamp((t-dl)/.55); 
        if u<=0: continue
        y=-u*200; sc=sc0*(_e(min(1,u*3)))
        s+=g(path('M0 0 C-30 -20 -24 -50 0 -36 C24 -50 30 -20 0 0Z',fill='#E8455A',stroke=INK,stroke_width=3),transform=f'translate({f(x0+math.sin(u*8)*10)} {f(y)}) scale({f(sc)})',opacity=f(1-u**2))
    return s
def zzz_float(t):
    s=''
    for i in range(3):
        u=(t+i/3)%1; s+=text('Z',u*80,-u*160,size=30+u*40,fill='#BFD4FF',weight=900,opacity=f(1-u),family="'Bebas Neue',Impact,sans-serif")
    return s
def sweat_drop_fall(t):
    y=-40+_e(t)*90 if t<.8 else 50
    return g(path('M0 -40 C-6 -24 -18 -12 -18 2 C-18 13 -9 20 0 20 C9 20 18 13 18 2 C18 -12 6 -24 0 -40Z',fill='#CDEBFF',stroke='#5A9ED6',stroke_width=3),transform=f'translate(0 {f(y)})',opacity=f(1 if t<.75 else max(0,1-(t-.75)*4)))
def confetti(t):
    rr=rnd(3); s=''
    for i in range(40):
        a=rr.uniform(-160,-20); v=rr.uniform(200,420); c=rr.choice(['#E2493B','#F2C230','#3FA34D','#3E7AD6','#F2A6B8','#7C5CD6'])
        x=math.cos(a*D)*v*t; y=math.sin(a*D)*v*t+380*t*t
        s+=g(rect(-6,-3,12,6,fill=c),transform=f'translate({f(x)} {f(y)}) rotate({f(rr.uniform(0,360)+t*720)})',opacity=f(max(0,1-t**3)))
    return s
def explosion(t):
    k=_e(t); s=''
    s+=circ(0,0,40+200*k,fill='#FFB13B',opacity=f(max(0,.5-.5*t)))
    for i in range(12):
        a=i*30+15; c=mul(dirv(a),60+160*k); s+=circ(c[0],c[1],(36+20*(i%3))*(1-t*.7),fill=['#F2853A','#E2493B','#FFE07A'][i%3],opacity=f(max(0,1-t)))
    s+=circ(0,0,70*(1-t)+10,fill='#FFF3C4',opacity=f(max(0,1-t*1.4)))
    return s
def splash(t):
    s=''; k=_e(t)
    for i in range(9):
        a=-160+i*17.5; L=60+60*(i%2); c=mul([math.cos(a*D),math.sin(a*D)],L*k); c[1]+=240*t*t
        s+=circ(c[0],c[1],10*(1-t*.6),fill='#9FD3E8',stroke='#5A9ED6',stroke_width=2)
    s+=ell(0,6,40+80*k,10+8*k,fill='none',stroke='#9FD3E8',stroke_width=4,opacity=f(1-t))
    return s
def fire_flicker(t):
    ph=t*2*math.pi; a=math.sin(ph); b=math.sin(ph*2+1)
    s=path(f'M-60 0 Q{-80+a*6} {-80} {-20+b*8} {-170-a*14} Q{-10} {-110} {20} {-100} Q{24+a*8} {-150-b*10} {54} {-190+a*8} Q{90} {-90} 60 0Z',fill='#F2853A',stroke='#C8573E',stroke_width=3)
    s+=path(f'M-30 0 Q{-40+b*5} -60 {-4+a*5} {-110+b*8} Q6 -70 24 -64 Q{40+a*4} -90 34 0Z',fill='#FFE07A')
    return ell(0,-60,140,120,fill='#FFB13B',opacity=f(.16+.05*a))+s
def lightning(t):
    op=f(1 if int(t*12)%4 in (0,2) else .0)
    return g(rect(-960,-540,1920,1080,fill='#E8F0FF',opacity='.35')+path('M0 -540 L-60 -200 L20 -200 L-80 200 L120 -260 L30 -260 L100 -540Z',fill='#FFF8C4',stroke='#F2C230',stroke_width=6),opacity=op)
def pulse_ring(t): return circ(0,0,30+150*t,fill='none',stroke='#3FC0F0',stroke_width=f(14*(1-t)+1),opacity=f(1-t))
def spinner(t): return ''.join(circ(math.cos((i/8+t)*2*math.pi)*50,math.sin((i/8+t)*2*math.pi)*50,10,fill='#EEF1F7',opacity=f(.15+((i/8)%1)*.85)) for i in range(8))
def typing_dots(t): return rect(-80,-40,160,80,rx=40,fill='#E6E9EE')+''.join(circ(-40+i*40,-6*max(0,math.sin((t-i*.15)*2*math.pi)),10,fill='#7A808C') for i in range(3))
SEQ=dict(dust_puff=dust_puff,sparkle_burst=sparkle_burst,smoke_rise=smoke_rise,impact_pow=impact_star,heart_pop=heart_pop,zzz_float=zzz_float,sweat_drop=sweat_drop_fall,confetti_burst=confetti,explosion=explosion,splash=splash,fire_loop=fire_flicker,lightning=lightning,pulse_ring=pulse_ring,loading_spinner=spinner,typing_dots=typing_dots)
LOOPING={'smoke_rise','zzz_float','fire_loop','loading_spinner','typing_dots','pulse_ring'}
NF=12
# --------------- full-frame overlays
W,H=1920,1080
def rain(seed=1,n=500,c='#9FC4E8'):
    rr=rnd(seed); return ''.join(line([x,y],[x-12,y+46],stroke=c,stroke_width=2,opacity=f(rr.uniform(.25,.7))) for x,y in ((rr.uniform(0,W+100),rr.uniform(-50,H)) for _ in range(n)))
def snow(seed=2,n=260):
    rr=rnd(seed); return ''.join(circ(rr.uniform(0,W),rr.uniform(0,H),rr.uniform(2,6),fill='#fff',opacity=f(rr.uniform(.5,.95))) for _ in range(n))
def fog(): return ''.join(ell(x,y,420,90,fill='#E6ECF4',opacity='.18') for x,y in ((300,800),(900,860),(1500,780),(600,960),(1300,980)))
def light_leak(): return f'<defs>{rg("leak",[(0,"#FFB13B",.5),(1,"#FFB13B",0)],cx=.1,cy=.1,r=.8)}</defs>'+rect(0,0,W,H,fill='url(#leak)')
def film_grain(seed=4):
    rr=rnd(seed); return ''.join(circ(rr.uniform(0,W),rr.uniform(0,H),rr.uniform(.6,1.6),fill='#fff' if rr.random()>.5 else '#000',opacity=f(rr.uniform(.05,.2))) for _ in range(1600))
def letterbox(): return rect(0,0,W,120,fill='#000')+rect(0,H-120,W,120,fill='#000')
def vignette_strong(): return f'<defs>{rg("vs",[(0,"#000",0),(.6,"#000",0),(1,"#000",.8)],r=.75)}</defs>'+rect(0,0,W,H,fill='url(#vs)')
def falling_leaves(seed=5):
    rr=rnd(seed); s=''
    for _ in range(40):
        c=rr.choice(['#E2853A','#D6453A','#F2C230','#C8904E'])
        s+=g(path('M0 -14 Q12 -4 0 14 Q-12 -4 0 -14Z',fill=c,stroke=dark(c,.4),stroke_width=1.4),transform=f'translate({f(rr.uniform(0,W))} {f(rr.uniform(0,H))}) rotate({f(rr.uniform(0,360))}) scale({f(rr.uniform(.8,1.6))})')
    return s
OVERLAYS=dict(rain=rain,snow=snow,fog=fog,light_leak=light_leak,film_grain=film_grain,letterbox=letterbox,vignette_strong=vignette_strong,falling_leaves=falling_leaves)
