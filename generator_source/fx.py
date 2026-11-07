from sv import *
INK='#1C1E26'; PAPER='#FBF8F2'
def speech(w=300,h=140,tail='left',txt='',c=PAPER):
    s=path(f'M{-w/2+40} {h/2-6} L{-w/2+20} {h/2+46} L{-w/2+90} {h/2-6}Z' if tail=='left' else f'M{w/2-90} {h/2-6} L{w/2-20} {h/2+46} L{w/2-40} {h/2-6}Z',fill=c,stroke=INK,stroke_width=4,stroke_linejoin='round')
    s+=rect(-w/2,-h/2,w,h,rx=h/2.4,fill=c,stroke=INK,stroke_width=4)
    s+=rect(-w/2+4,h/2-14,w-8,10,fill=c)  # hide tail seam
    s=path(f'M{-w/2+40} {h/2-6} L{-w/2+20} {h/2+46} L{-w/2+90} {h/2-6}' if tail=='left' else f'M{w/2-90} {h/2-6} L{w/2-20} {h/2+46} L{w/2-40} {h/2-6}',fill=c,stroke=INK,stroke_width=4,stroke_linejoin='round')+rect(-w/2,-h/2,w,h,rx=h/2.4,fill=c,stroke=INK,stroke_width=4)+path(f'M{-w/2+42} {h/2-2} L{-w/2+88} {h/2-2}' if tail=='left' else f'M{w/2-88} {h/2-2} L{w/2-42} {h/2-2}',stroke=c,stroke_width=6)
    if txt: s+=text(txt,0,10,size=30,fill=INK,weight=800,anchor='middle')
    return s
def thought(w=320,h=170,txt=''):
    rr=rnd(3); s=''
    pts=[]
    n=12
    for i in range(n):
        a=i/n*2*math.pi; pts.append([math.cos(a)*w/2,math.sin(a)*h/2])
    for p in pts: s+=circ(p[0],p[1],h*.26,fill=PAPER,stroke=INK,stroke_width=4)
    s+=ell(0,0,w/2,h/2,fill=PAPER)
    for p in pts: s+=circ(p[0],p[1],h*.26-4,fill=PAPER)
    s+=circ(-w*.28,h*.72,18,fill=PAPER,stroke=INK,stroke_width=4)+circ(-w*.36,h*.95,10,fill=PAPER,stroke=INK,stroke_width=4)
    if txt: s+=text(txt,0,10,size=30,fill=INK,weight=700,anchor='middle')
    return s
def shout(w=340,h=200,txt='WHAT?!',c='#FFE07A'):
    pts=[]; n=20
    for i in range(n):
        a=i/n*2*math.pi; k=1 if i%2==0 else .72
        pts.append([math.cos(a)*w/2*k,math.sin(a)*h/2*k])
    pts[5]=[w*.18,h*.9]
    s=path('M'+'L'.join(P(p) for p in pts)+'Z',fill=c,stroke=INK,stroke_width=4,stroke_linejoin='round')
    if txt: s+=text(txt,0,14,size=44,fill=INK,weight=900,anchor='middle',family="'Bebas Neue',Oswald,Impact,sans-serif")
    return s
def whisper(w=300,h=130,txt='...'):
    return rect(-w/2,-h/2,w,h,rx=h/2.4,fill=PAPER,stroke=INK,stroke_width=3.5,stroke_dasharray='14 10')+path(f'M{-w/2+50} {h/2} L{-w/2+30} {h/2+40} L{-w/2+90} {h/2}',fill=PAPER,stroke=INK,stroke_width=3.5,stroke_dasharray='10 8')+(text(txt,0,10,size=30,fill='#666',weight=600,anchor='middle',font_style='italic') if txt else '')
def inner_voice(w=360,h=150,txt='you are behind.'):
    return rect(-w/2,-h/2,w,h,rx=24,fill='#14070A',stroke='#B3262E',stroke_width=4)+path(f'M{-w/2+50} {h/2} L{-w/2+20} {h/2+50} L{-w/2+100} {h/2}Z',fill='#14070A',stroke='#B3262E',stroke_width=4)+path(f'M{-w/2+52} {h/2-2} L{-w/2+98} {h/2-2}',stroke='#14070A',stroke_width=6)+(text(txt,0,10,size=30,fill='#FF6A6A',weight=700,anchor='middle',font_style='italic') if txt else '')
def caption_box(w=520,h=90,txt='MEANWHILE...'):
    return rect(-w/2,-h/2,w,h,fill='#F2D45A',stroke=INK,stroke_width=4)+text(txt,0,14,size=40,fill=INK,weight=900,anchor='middle',family="'Bebas Neue',Oswald,Impact,sans-serif",letter_spacing='3')
def exclaim(c='#E5484D'): return path('M-14 -110 L14 -110 L8 -30 L-8 -30Z',fill=c,stroke=INK,stroke_width=4,stroke_linejoin='round')+circ(0,-6,12,fill=c,stroke=INK,stroke_width=4)
def question(c='#4F8CFF'): return path('M-34 -84 C-34 -130 40 -130 40 -86 C40 -56 6 -54 6 -26',fill='none',stroke=INK,stroke_width=24,stroke_linecap='round')+path('M-34 -84 C-34 -130 40 -130 40 -86 C40 -56 6 -54 6 -26',fill='none',stroke=c,stroke_width=16,stroke_linecap='round')+circ(6,6,12,fill=c,stroke=INK,stroke_width=4)
def interrobang(): return g(exclaim(),transform='translate(-30 0)')+g(question('#F2B53A'),transform='translate(30 0)')
def sweat_drop(): return path('M0 -80 C-10 -50 -34 -24 -34 2 C-34 22 -18 36 0 36 C18 36 34 22 34 2 C34 -24 10 -50 0 -80Z',fill='#CDEBFF',stroke='#5A9ED6',stroke_width=4)+path('M-14 -4 Q-16 14 -2 20',fill='none',stroke='#fff',stroke_width=5,stroke_linecap='round')
def anger_vein(): return path('M-34 -10 Q-10 -10 -10 -34 M10 -34 Q10 -10 34 -10 M34 10 Q10 10 10 34 M-10 34 Q-10 10 -34 10',fill='none',stroke='#D6453A',stroke_width=12,stroke_linecap='round')
def zzz(): return text('Z',0,0,size=70,fill='#BFD4FF',weight=900,family="'Bebas Neue',Oswald,Impact,sans-serif")+text('z',44,-50,size=50,fill='#BFD4FF',weight=900)+text('z',76,-90,size=34,fill='#BFD4FF',weight=900)
def hearts(): return ''.join(g(path('M0 0 C-30 -20 -24 -50 0 -36 C24 -50 30 -20 0 0Z',fill='#E8455A',stroke=INK,stroke_width=3),transform=f'translate({x} {y}) scale({k})') for x,y,k in ((0,0,1.4),(60,-60,.9),(-50,-70,.7)))
def sparkles(): return ''.join(g(path('M0 -40 Q4 -4 40 0 Q4 4 0 40 Q-4 4 -40 0 Q-4 -4 0 -40Z',fill='#FFE07A'),transform=f'translate({x} {y}) scale({k})') for x,y,k in ((0,0,1),(70,-50,.5),(-60,-40,.6),(50,50,.35)))
def scribble():
    d='M-60 0'
    rr=rnd(9)
    for i in range(22): d+=f' Q{f(rr.uniform(-70,70))} {f(rr.uniform(-50,50))} {f(rr.uniform(-60,60))} {f(rr.uniform(-40,40))}'
    return path(d,fill='none',stroke=INK,stroke_width=5,stroke_linecap='round',stroke_linejoin='round')
def dark_cloud_head(): return ''.join(circ(x,y,r_,fill='#3A3F4E') for x,y,r_ in ((-60,0,40),(0,-26,54),(60,0,42),(20,10,40),(-24,14,36)))+''.join(path(f'M{x} 50 l-8 30 l14 -12 l-6 34',fill='none',stroke='#FFE07A',stroke_width=5,stroke_linejoin='round') for x in (-10,))+''.join(line([x,54],[x-8,84],stroke='#8FC9F5',stroke_width=4,stroke_linecap='round') for x in (-60,40,70))
def motion_lines(): return ''.join(line([0,y],[-l,y],stroke=INK,stroke_width=6,stroke_linecap='round',opacity='.8') for y,l in ((-40,120),(0,180),(40,140),(80,90)))
def speed_lines():
    s=''
    for i in range(48):
        a=i/48*2*math.pi; r1=rnd(i).uniform(260,340)
        s+=path(f'M{f(math.cos(a)*r1)} {f(math.sin(a)*r1)} L{f(math.cos(a+.03)*600)} {f(math.sin(a+.03)*600)} L{f(math.cos(a-.03)*600)} {f(math.sin(a-.03)*600)}Z',fill=INK,opacity='.85')
    return s
def impact(c='#FFE07A'):
    pts=[]
    for i in range(16):
        a=i/16*2*math.pi; k=150 if i%2==0 else 80
        pts.append([math.cos(a)*k,math.sin(a)*k])
    return path('M'+'L'.join(P(p) for p in pts)+'Z',fill=c,stroke=INK,stroke_width=5,stroke_linejoin='round')+text('POW',0,18,size=56,fill='#D6453A',weight=900,anchor='middle',family="'Bebas Neue',Oswald,Impact,sans-serif")
def dust_puff(): return ''.join(circ(x,y,r_,fill='#D9D2C4',opacity='.85') for x,y,r_ in ((-40,0,26),(0,-10,34),(40,0,24),(-70,10,16),(72,8,14)))
def tear_stream(): return path('M0 0 Q-8 60 0 140 L14 140 Q8 60 16 0Z',fill='#9FD3FF',opacity='.9',stroke='#6FB2E6',stroke_width=2)
def stress_lines(): return ''.join(path(f'M{x} -60 L{x} 0',stroke='#6C7FA8',stroke_width=7,stroke_linecap='round') for x in (-40,-14,14,40))
def arrow(c='#F2D45A'): return path('M-120 -20 L40 -20 L40 -60 L120 0 L40 60 L40 20 L-120 20Z',fill=c,stroke=INK,stroke_width=4,stroke_linejoin='round')
def curved_arrow(c='#F2D45A'): return path('M-120 40 Q0 -100 100 -10',fill='none',stroke=INK,stroke_width=22,stroke_linecap='round')+path('M-120 40 Q0 -100 100 -10',fill='none',stroke=c,stroke_width=14,stroke_linecap='round')+path('M70 -50 L130 6 L56 20Z',fill=c,stroke=INK,stroke_width=4,stroke_linejoin='round')
def check(): return circ(0,0,70,fill='#3FA34D',stroke=INK,stroke_width=4)+path('M-32 0 L-8 26 L36 -26',fill='none',stroke='#fff',stroke_width=14,stroke_linecap='round',stroke_linejoin='round')
def cross(): return circ(0,0,70,fill='#D6453A',stroke=INK,stroke_width=4)+path('M-26 -26 L26 26 M26 -26 L-26 26',stroke='#fff',stroke_width=14,stroke_linecap='round')
def progress_bar(p=.14): return rect(-220,-26,440,52,rx=26,fill='#2A2D35',stroke=INK,stroke_width=4)+rect(-212,-18,424*p,36,rx=18,fill='#E5484D')+text(f'{int(p*100)}%',0,10,size=26,fill='#fff',weight=800,anchor='middle')
def loading_spinner(): return ''.join(circ(math.cos(i/8*2*math.pi)*50,math.sin(i/8*2*math.pi)*50,10,fill='#EEF1F7',opacity=f(.15+i/8*.85)) for i in range(8))
def like_heart(): return circ(0,0,60,fill='#FF3B5C')+path('M0 24 C-40 -4 -28 -40 0 -18 C28 -40 40 -4 0 24Z',fill='#fff')
def notif_badge(n='99+'): return circ(0,0,46,fill='#E5484D',stroke='#fff',stroke_width=6)+text(n,0,14,size=34 if len(n)>2 else 40,fill='#fff',weight=800,anchor='middle')
def thumbs_up_icon(): return circ(0,0,60,fill='#4F8CFF')+path('M-24 -2 L-12 -2 L-12 30 L-24 30Z M-8 30 L18 30 Q28 30 28 20 L30 -2 Q30 -10 22 -10 L6 -10 L8 -26 Q8 -36 0 -36 L-8 -4Z',fill='#fff')
def shadow_tendrils():
    rr=rnd(5); pts=[]
    for i in range(40):
        a=i/40*2*math.pi; r_=150+rr.uniform(-12,12)+(30 if i%5==0 else 0)
        pts.append([math.cos(a)*r_*.9,math.sin(a)*r_*1.1-40])
    s=ell(0,-40,240,260,fill='#5A0A10',opacity='.25')
    body=smooth(pts)
    tail='M-130 40 Q-150 200 -90 300 Q-60 220 -40 320 Q-10 230 10 330 Q40 230 60 310 Q80 220 100 300 Q150 200 130 40Z'
    s+=path(tail,fill='#060609')+path(body,fill='#060609',stroke='#2A0507',stroke_width=5)
    for sd in (-1,1):
        s+=path(f'M{sd*120} 0 Q{sd*260} -40 {sd*280} 120 Q{sd*300} 160 {sd*330} 150',fill='none',stroke='#060609',stroke_width=30,stroke_linecap='round')
        for k in (-1,0,1): s+=path(f'M{sd*330} 150 q{sd*30} {10+k*20} {sd*50} {30+k*28}',fill='none',stroke='#060609',stroke_width=10,stroke_linecap='round')
    s+=g(glowing_eyes(),transform='translate(0 -70)')+path('M-50 10 Q-25 30 0 14 Q25 30 50 10 Q25 50 0 36 Q-25 50 -50 10Z',fill='#B3262E',opacity='.85')
    return s
def glowing_eyes(): return ell(-40,0,26,14,fill='#FFE27A')+ell(40,0,26,14,fill='#FFE27A')+ell(-40,0,60,40,fill='#FFE27A',opacity='.15')+ell(40,0,60,40,fill='#FFE27A',opacity='.15')+ell(-40,0,8,10,fill='#3A0A0A')+ell(40,0,8,10,fill='#3A0A0A')
FXS={k:v for k,v in dict(
 bubble_speech_left=lambda: speech(tail='left'),bubble_speech_right=lambda: speech(tail='right'),bubble_speech_hi=lambda: speech(txt='Hey!'),bubble_thought=thought,bubble_thought_hmm=lambda: thought(txt='hmm...'),
 bubble_shout=shout,bubble_whisper=whisper,bubble_inner_voice=inner_voice,caption_meanwhile=caption_box,caption_years_later=lambda: caption_box(txt='5 YEARS LATER'),
 icon_exclaim=exclaim,icon_question=question,icon_interrobang=interrobang,icon_sweat_drop=sweat_drop,icon_anger_vein=anger_vein,icon_zzz=zzz,icon_hearts=hearts,icon_sparkles=sparkles,
 icon_scribble_stress=scribble,icon_storm_cloud=dark_cloud_head,icon_stress_lines=stress_lines,icon_tear_stream=tear_stream,
 fx_motion_lines=motion_lines,fx_speed_lines_focus=speed_lines,fx_impact_pow=impact,fx_dust_puff=dust_puff,
 ui_arrow=arrow,ui_curved_arrow=curved_arrow,ui_check=check,ui_cross=cross,ui_progress_14=progress_bar,ui_loading=loading_spinner,ui_like=like_heart,ui_badge_99=notif_badge,ui_thumbs_up=thumbs_up_icon,
 dark_shadow_creature=shadow_tendrils,dark_glowing_eyes=glowing_eyes).items()}
