from sv import *
import math
def phone_in_hand(scale=1,screen='#8FB6F0',glow=True,back=False):
    def fn(W,h):
        # phone center offset from wrist along the hand
        c=add(W,mul(dirv(h),15*scale))
        s=''
        if glow and not back: s+=circ(c[0],c[1],60*scale,fill='url(#phoneGlow)')
        bw,bh=22*scale,40*scale
        s+=g(rect(-bw/2,-bh/2,bw,bh,rx=4*scale,fill='#1A1D24',stroke='#0B0C10',stroke_width='1.6')+
             (rect(-bw/2+2.2*scale,-bh/2+2.6*scale,bw-4.4*scale,bh-5.2*scale,rx=2.4*scale,fill=screen) if not back else circ(-bw/4,-bh/3,3*scale,fill='#333842')),
             transform=f'translate({f(c[0])} {f(c[1])}) rotate({f(-h+180-25)})')
        return s
    return fn
def mug_in_hand():
    def fn(W,h):
        c=add(W,mul(dirv(h),14))
        return g(rect(-11,-13,22,26,rx=4,fill='#E9E2D4',stroke='#6B6256',stroke_width='2')+path('M11 -6 q9 0 9 7 q0 7 -9 7',fill='none',stroke='#6B6256',stroke_width='3')+rect(-11,-6,22,5,fill='#C8573E'),transform=f'translate({f(c[0])} {f(c[1])})')
    return fn
def book_in_hands():
    def fn(W,h):
        c=add(W,mul(dirv(h),12))
        return g(path('M0 0 L-34 -6 L-34 30 L0 36Z',fill='#F3EEE2',stroke='#6B6256',stroke_width='2')+path('M0 0 L30 -10 L30 26 L0 36Z',fill='#FBF8F0',stroke='#6B6256',stroke_width='2')+path('M-30 6 L-6 9 M-30 14 L-6 17 M-30 22 L-6 25 M5 6 L25 0 M5 14 L25 8',stroke='#B8AE9C',stroke_width='1.6')+path('M-36 -8 L0 -1 L32 -12 L32 28 L0 38 L-36 32Z',fill='none',stroke='#7A3B3B',stroke_width='3'),transform=f'translate({f(c[0])} {f(c[1])}) rotate(-8)')
    return fn

STAND=dict()
# name -> (description, params)
POSES={
 'stand':        ('Standing idle',dict()),
 'stand_sad':    ('Slumped, sad',dict(curl=.9,lean=8,head=14,aN=[2,4],aF=[-2,6],expr='sad')),
 'stand_proud':  ('Chest out, proud',dict(lean=-5,head=-8,curl=-.4,aN=[-6,10],aF=[-14,12],expr='proud')),
 'phone_look':   ('Looking at phone',dict(head=20,lean=4,ikN=[42,-58],hN='grip',wN=-35,aF=[-6,14],look=(.5,.8),expr='focused')),
 'phone_shock':  ('Shocked at phone',dict(head=4,lean=-6,ikN=[50,-72],hN='grip',wN=-30,ikF=[-34,-150,1],hF='open',expr='shocked')),
 'phone_scroll_sad': ('Doom-scrolling',dict(head=24,lean=10,curl=.8,ikN=[40,-50],hN='grip',wN=-38,aF=[0,6],look=(.4,.9),expr='depressed')),
 'thinking':     ('Hand on chin',dict(head=-6,ikN=[24,-104],hN='fist',wN=-150,ikF=[18,-46,1],hF='relax',wF=0,look=(.6,-.8),expr='thinking')),
 'facepalm':     ('Facepalm',dict(head=16,lean=6,ikN=[30,-122],hN='open',wN=-165,aF=[-4,8],expr='annoyed')),
 'point':        ('Pointing forward',dict(lean=2,aN=[85,8],hN='point',aF=[-8,14],expr='determined')),
 'wave':         ('Waving',dict(aN=[150,-40],hN='spread',wN=0,aF=[-6,14],expr='happy')),
 'cheer':        ('Cheering, arms up',dict(lean=-4,head=-12,aN=[118,42],aF=[150,10],hN='fist',hF='fist',lN=[8,6],lF=[-8,6],expr='joy')),
 'talk':         ('Explaining, open palm',dict(aN=[48,62],hN='spread',wN=-60,aF=[-6,14],expr='happy',mouth='v_AI')),
 'scared':       ('Recoiling in fear',dict(lean=-14,head=-10,ikN=[78,-118],ikF=[66,-108],hN='spread',hF='spread',wN=-80,wF=-80,lN=[16,24],lF=[-14,6],expr='terrified')),
 'shrug_side':   ('Shrug',dict(aN=[40,110],hN='spread',wN=-40,aF=[-20,110],hF='spread',head=-6,expr='confused')),
 'stretch':      ('Morning stretch / yawn',dict(lean=-8,head=-16,aN=[172,4],aF=[168,8],hN='fist',hF='fist',expr='sleepy')),
 'coffee':       ('Drinking coffee',dict(head=-4,ikN=[40,-92],hN='grip',wN=-70,holdN=mug_in_hand(),aF=[-6,14],expr='content')),
 'reading':      ('Reading a book',dict(head=18,ikN=[50,-70],hN='grip',wN=-20,ikF=[44,-66],hF='grip',holdN=book_in_hands(),look=(.5,.8),expr='focused')),
 'jump':         ('Jump for joy',dict(y=-60,lean=-4,head=-10,aN=[155,-10],aF=[140,20],hN='fist',hF='fist',lN=[40,80],lF=[-30,70],fN=-20,fF=-30,expr='joy')),
 'fall':         ('Falling / tripping',dict(rot=40,lean=10,head=-20,aN=[130,30],aF=[100,40],hN='spread',hF='spread',lN=[-30,40],lF=[-60,20],expr='shocked')),
 'kneel':        ('On knees, despair',dict(y=72,lean=16,curl=.8,head=24,lN=[4,92],lF=[-2,92],fN=90,fF=90,aN=[10,10],aF=[4,8],hN='open',hF='open',expr='crying')),
 'run_late':     ('Running late',dict(lean=16,head=-6,aN=[-50,90],aF=[60,80],hN='fist',hF='fist',lN=[50,30],lF=[-34,100],fF=10,expr='nervous')),
 'sneak':        ('Sneaking / hiding',dict(lean=26,curl=.6,head=-14,y=20,aN=[60,96],aF=[30,100],hN='relax',hF='relax',legIkN=[44,126],legIkF=[-30,127],fF=30,expr='nervous',look=(-1,0))),
 'sit_chair':    ('Sitting on a chair',dict(y=70,lean=2,legIkN=[66,70],legIkF=[58,72],aN=[36,40],aF=[30,46],expr='neutral')),
 'sit_typing':   ('Typing at laptop',dict(y=70,lean=10,head=10,legIkN=[66,70],legIkF=[58,72],ikN=[86,-30],ikF=[78,-24],hN='flat',hF='flat',wN=-60,wF=-60,look=(.8,.4),expr='focused')),
 'sit_head_in_hands': ('Head in hands',dict(y=70,lean=22,curl=.9,head=34,legIkN=[66,70],legIkF=[58,72],ikN=[62,-118],ikF=[54,-112],hN='open',hF='open',wN=-160,wF=-160,expr='crying')),
 'sit_desk_slump':('Head down on desk',dict(y=70,lean=60,curl=.5,head=30,legIkN=[66,70],legIkF=[58,72],ikN=[120,-98],ikF=[96,-90],hN='flat',hF='flat',wN=-70,wF=-70,expr='sleeping')),
 'sit_phone':    ('Sitting, on phone',dict(y=70,lean=14,curl=.6,head=22,legIkN=[66,70],legIkF=[58,72],ikN=[54,-40],hN='grip',wN=-40,ikF=[50,-30],hF='relax',look=(.5,.9),expr='depressed')),
 'sit_floor_hug':('Hugging knees on floor',dict(y=136,lean=18,curl=.9,head=22,lN=[140,110],lF=[134,108],ikN=[72,-44],ikF=[66,-40],hN='relax',hF='relax',expr='lonely',fN=-10,fF=-10)),
 'lie_back':     ('Lying on back',dict(y=120,rot=-90,lN=[2,2],lF=[-1,3],fN=30,fF=34,aN=[6,10],aF=[-4,10],expr='sleeping',turn=.15)),
 'lie_phone':    ('Lying in bed with phone',dict(y=120,rot=-90,lN=[4,8],lF=[-2,6],fN=30,fF=34,head=-4,ikN=[60,-150],hN='grip',wN=40,aF=[-4,12],look=(1,0),expr='dead_inside')),
 'lie_curl':     ('Curled up (fetal)',dict(rot=-90,y=110,lean=26,curl=.6,head=20,lN=[118,118],lF=[110,116],ikN=[70,-40],ikF=[62,-36],hN='relax',hF='relax',fN=-30,fF=-30,expr='very_sad')),
}
# --- cycles ---
def walk(phase,amp=1,sad=False):
    s=math.sin(phase); c=math.cos(phase); sF=math.sin(phase+math.pi); cF=math.cos(phase+math.pi)
    knee=lambda cc: 6+44*max(0,cc)**1.4*amp
    d=dict(lN=[26*s*amp,knee(c)],lF=[26*sF*amp,knee(cF)],
           fN=-8*s*amp+(10*max(0,-c)*amp if s<0 else 0), fF=-8*sF*amp+(10*max(0,-cF)*amp if sF<0 else 0),
           aN=[-24*s*amp,18+10*max(0,-s)*amp],aF=[24*s*amp,18+10*max(0,s)*amp],
           y=-3.5*amp*abs(math.cos(phase)),lean=4*amp,head=-2)
    if sad: d.update(curl=.8,lean=8,head=16,expr='sad')
    return d
def run(phase,amp=1):
    s=math.sin(phase); c=math.cos(phase); sF=-s; cF=-c
    knee=lambda cc: 18+88*max(0,cc)**1.1*amp
    return dict(lN=[44*s*amp+6,knee(c)],lF=[44*sF*amp+6,knee(cF)],
        fN=-10*s+18*max(0,-c),fF=-10*sF+18*max(0,-cF),
        aN=[-48*s*amp+6,82],aF=[48*s*amp+6,82],hN='fist',hF='fist',
        y=-9*amp*abs(math.sin(phase+.2)),lean=12*amp,head=-6,expr='determined')
FRONT={
 'front_stand':   ('Front – standing',dict()),
 'front_wave':    ('Front – waving',dict(aN=[150,-30],hN='spread',expr='happy')),
 'front_cheer':   ('Front – arms up',dict(aN=[150,10],aF=[150,10],hN='fist',hF='fist',expr='joy')),
 'front_shrug':   ('Front – shrug',dict(aN=[28,95],aF=[28,95],hN='spread',hF='spread',wN=0,wF=0,head=-6,expr='confused')),
 'front_hips':    ('Front – hands on hips',dict(aN=[50,-80],aF=[50,-80],hN='fist',hF='fist',expr='determined')),
 'front_cross':   ('Front – arms crossed',dict(ikN=[-26,-60,-1],ikF=[26,-56,-1],hN='fist',hF='fist',expr='annoyed')),
 'front_facepalm':('Front – facepalm',dict(ikN=[2,-140,-1],hN='open',wN=0,head=8,expr='annoyed')),
 'front_think':   ('Front – thinking',dict(ikN=[6,-112,-1],hN='fist',ikF=[10,-58,-1],hF='relax',head=-6,look=(.6,-.8),expr='thinking')),
 'front_sad':     ('Front – sad',dict(aN=[3,0],aF=[3,0],head=10,expr='very_sad')),
 'front_panic':   ('Front – panic',dict(ikN=[30,-150,1],ikF=[-30,-150,1],hN='spread',hF='spread',expr='terrified')),
 'front_point':   ('Front – pointing aside',dict(aN=[88,2],hN='point',wN=0,head=6,look=(1,0),expr='determined')),
 'front_call':    ('Front – phone call',dict(ikN=[-4,-70,-1],hN='grip',head=12,look=(0,1),expr='focused')),
 'front_meditate':('Front – meditating',dict(y=110,lN=[80,150],lF=[80,150],aN=[30,-30],aF=[30,-30],hN='relax',hF='relax',expr='content')),
 'front_hug_self':('Front – hugging self',dict(ikN=[-30,-70,-1],ikF=[30,-74,-1],hN='open',hF='open',head=8,expr='anxious')),
}
BACK={'back_stand':('Back view – standing',dict(view='back')),'back_window':('Back view – arms crossed',dict(view='back',ikN=[-26,-60,-1],ikF=[26,-56,-1],hN='fist',hF='fist'))}

# =====================================================================
# v2: held items (drawn in the hand). fn(W,h): W = wrist point, h = hand angle
# =====================================================================
def _grip(W,h,k=15): return add(W,mul(dirv(h),k))
def _S(c,k=.55,w=2.2): return dict(fill=c,stroke=dark(c,k),stroke_width=w,stroke_linejoin='round')
def coffee_togo_in_hand(cup='#F3EEE2',sleeve='#8A5A3C',lid='#3A2E26'):
    def fn(W,h):
        c=_grip(W,h,13)
        s=path('M-11 -16 L11 -16 L8.5 17 L-8.5 17Z',**_S(cup))+path('M-10.4 -6 L10.4 -6 L9.4 7 L-9.4 7Z',**_S(sleeve))
        s+=rect(-13,-22,26,7,rx=3,**_S(lid))+rect(-6,-25,12,4,rx=2,fill=dark(lid,.2))
        s+=path('M-4 -30 q3 -5 0 -10 M3 -32 q3 -5 0 -10',fill='none',stroke='#ECE4D6',stroke_width='2',stroke_linecap='round',opacity='.55')
        return g(s,transform=f'translate({f(c[0])} {f(c[1])})')
    return fn
def umbrella_in_hand(col='#3E6A8A',tilt=-8,closed=False,L=150):
    def fn(W,h):
        c=_grip(W,h,12)
        t=f'translate({f(c[0])} {f(c[1])}) rotate({f(tilt)})'
        s=path(f'M0 4 L0 {-L}',stroke='#3A3E47',stroke_width='5',stroke_linecap='round')
        s+=path('M0 4 Q0 22 -12 20',fill='none',stroke='#5A3E2A',stroke_width='6',stroke_linecap='round')
        if closed:
            s+=path('M0 -40 L-9 -120 L0 -150 L9 -120Z',**_S(col))
        else:
            ln=dark(col,.55); s0=s; s=''
            s+=path('M-110 -150 Q-100 -230 0 -236 Q100 -230 110 -150 Q92 -162 73 -150 Q55 -164 37 -150 Q18 -164 0 -150 Q-18 -164 -37 -150 Q-55 -164 -73 -150 Q-92 -162 -110 -150Z',fill=col,stroke=ln,stroke_width='2.6',stroke_linejoin='round')
            s+=path('M0 -236 Q-40 -200 -37 -150 M0 -236 Q40 -200 37 -150 M0 -236 Q-90 -210 -73 -150 M0 -236 Q90 -210 73 -150',fill='none',stroke=ln,stroke_width='1.8',opacity='.55')
            s+=path('M-70 -205 Q-40 -226 -10 -228',fill='none',stroke=light(col,.4),stroke_width='4',stroke_linecap='round',opacity='.6')
            s+=path('M0 -236 L0 -248',stroke='#3A3E47',stroke_width='4',stroke_linecap='round')
            s=s0+g(s,transform=f'translate(0 {150-L})')
        return g(s,transform=t)
    return fn
def briefcase_in_hand(col='#5A3E2A'):
    def fn(W,h):
        c=_grip(W,h,14); ln=dark(col,.55)
        s=path('M-10 6 L-10 -2 Q-10 -6 -6 -6 L6 -6 Q10 -6 10 -2 L10 6',fill='none',stroke=ln,stroke_width='4.4')
        s+=rect(-34,4,68,46,rx=6,**_S(col))+path('M-34 20 L34 20',stroke=ln,stroke_width='2')+rect(-6,15,12,10,rx=2,fill='#E3B24A',stroke=ln,stroke_width='1.4')
        s+=path('M-28 10 L-10 10',stroke=light(col,.3),stroke_width='2.4',stroke_linecap='round',opacity='.6')
        return g(s,transform=f'translate({f(c[0])} {f(c[1])})')
    return fn
def shopping_bag_in_hand(col='#E8C468',logo='#C8573E'):
    def fn(W,h):
        c=_grip(W,h,12); ln=dark(col,.5)
        s=path('M-12 26 Q-12 -4 0 -4 Q12 -4 12 26',fill='none',stroke=ln,stroke_width='3.4')
        s+=path('M-28 22 L28 22 L32 82 L-32 82Z',**_S(col))+path('M-28 22 L-22 30 L22 30 L28 22',fill=dark(col,.12),stroke=ln,stroke_width='1.6')
        s+=circ(0,54,10,fill='none',stroke=logo,stroke_width='3')+path('M-4 54 L4 54',stroke=logo,stroke_width='3',stroke_linecap='round')
        return g(s,transform=f'translate({f(c[0])} {f(c[1])})')
    return fn
def dumbbell_in_hand(col='#3A3E47'):
    def fn(W,h):
        c=_grip(W,h,13)
        s=circ(0,0,17,**_S(col))+circ(0,0,11,fill=light(col,.15))+circ(0,0,4,fill='#9AA3AF')
        return g(s,transform=f'translate({f(c[0])} {f(c[1])})')
    return fn
def bottle_in_hand(col='#8FC9F5',tilt=0):
    def fn(W,h):
        c=_grip(W,h,13)
        s=rect(-9,-30,18,58,rx=7,fill=col,fill_opacity='.75',stroke=dark(col,.5),stroke_width='2.2')+rect(-6,-40,12,11,rx=3,**_S('#3E6A8A'))+rect(-9,-6,18,14,fill='#3E6A8A',opacity='.75')
        s+=path('M-4 -24 L-4 18',stroke='#fff',stroke_width='2.4',stroke_linecap='round',opacity='.6')
        return g(s,transform=f'translate({f(c[0])} {f(c[1])}) rotate({f(tilt)})')
    return fn
def letter_in_hand(tilt=-6):
    def fn(W,h):
        c=_grip(W,h,10)
        s=rect(-22,-30,44,56,rx=2,fill='#FBF8F0',stroke='#6B6256',stroke_width='2')
        s+=path('M-15 -20 L15 -20 M-15 -12 L12 -12 M-15 -4 L15 -4 M-15 4 L8 4 M-15 12 L14 12',stroke='#B8AE9C',stroke_width='1.8',stroke_linecap='round')
        s+=circ(12,-22,0.1,fill='none')
        return g(s,transform=f'translate({f(c[0])} {f(c[1])}) rotate({f(tilt)})')
    return fn
def flower_in_hand(col='#E8455A'):
    def fn(W,h):
        c=_grip(W,h,13)
        s=path('M0 8 Q4 -30 2 -62',fill='none',stroke='#4E8A48',stroke_width='4',stroke_linecap='round')
        s+=path('M2 -34 Q18 -42 22 -30 Q12 -26 2 -34Z',**_S('#5FB55A'))+path('M2 -22 Q-14 -30 -18 -18 Q-8 -14 2 -22Z',**_S('#5FB55A'))
        s+=path('M-12 -66 Q-14 -84 2 -82 Q16 -86 15 -68 Q14 -56 2 -56 Q-10 -56 -12 -66Z',**_S(col))
        s+=path('M-4 -74 Q2 -64 8 -74 M-8 -68 Q2 -60 11 -68',fill='none',stroke=dark(col,.4),stroke_width='1.8',stroke_linecap='round')
        return g(s,transform=f'translate({f(c[0])} {f(c[1])}) rotate(10)')
    return fn
def controller_in_hands(col='#3A3E47'):
    def fn(W,h):
        c=_grip(W,h,6)
        s=path('M-30 -4 C-36 -24 -24 -30 -16 -27 L16 -27 C24 -30 36 -24 30 -4 C27 4 19 4 15 -4 L-15 -4 C-19 4 -27 4 -30 -4Z',**_S(col))
        s+=rect(-21,-21,3,10,fill='#9AA3AF')+rect(-24.5,-17.5,10,3,fill='#9AA3AF')+circ(17,-20,2.6,fill='#D6453A')+circ(22,-15,2.6,fill='#5FB55A')+circ(12,-15,2.6,fill='#3E6A8A')
        return g(s,transform=f'translate({f(c[0])} {f(c[1])}) rotate(-6)')
    return fn
def box_in_hands(col='#C9A16E'):
    def fn(W,h):
        c=_grip(W,h,2); ln=dark(col,.55)
        s=path('M-46 -50 L30 -50 L30 22 L-46 22Z',**_S(col))+path('M-46 -50 L-34 -62 L42 -62 L30 -50Z',**_S(light(col,.12)))+path('M30 -50 L42 -62 L42 10 L30 22Z',**_S(dark(col,.12)))
        s+=rect(-16,-50,16,20,fill=light(col,.3),opacity='.8')+path('M-40 4 L-20 4',stroke=ln,stroke_width='2',opacity='.6')
        return g(s,transform=f'translate({f(c[0]-6)} {f(c[1])})')
    return fn
def selfie_phone():
    def fn(W,h):
        c=_grip(W,h,14)
        s=rect(-7,-20,14,40,rx=4,fill='#1A1D24',stroke='#0B0C10',stroke_width='1.6')+circ(0,-13,2.6,fill='#333842')
        return g(s,transform=f'translate({f(c[0])} {f(c[1])}) rotate(-12)')
    return fn
def mic_in_hand(col='#3A3E47'):
    def fn(W,h):
        c=_grip(W,h,10)
        s=path('M0 22 L0 -6',stroke=col,stroke_width='8',stroke_linecap='round')+circ(0,-14,11,**_S('#9AA3AF'))+path('M-8 -18 L8 -18 M-9 -12 L9 -12',stroke=dark('#9AA3AF',.3),stroke_width='1.4')
        return g(s,transform=f'translate({f(c[0])} {f(c[1])}) rotate(18)')
    return fn
def laptop_on_lap(screen='#3B5B8A',glow=True):
    def fn(G):
        kn=G['kneeN']; hp=G['hip']
        y=min(kn[1],hp[1])-14
        x0=hp[0]+18; x1=kn[0]+16
        s=''
        if glow: s+=circ(x1-6,y-30,70,fill='url(#screenGlow)',opacity='.6')
        s+=rect(x0,y,x1-x0,7,rx=2.5,fill='#B8BEC8',stroke='#5A6070',stroke_width='2')
        s+=g(rect(-4,-58,8,60,rx=3,fill='#9AA3AF',stroke='#5A6070',stroke_width='2')+circ(0,-30,2.6,fill='#E9EDF2'),transform=f'translate({f(x1-3)} {f(y+2)}) rotate(-14)')
        return s
    return fn

# ---------------------------------------------------------------------
# v2 poses (side view). All re-checked against the fixed spine (positive lean = forward)
# ---------------------------------------------------------------------
_SEAT=dict(y=70,legIkN=[66,70],legIkF=[58,72])
def _sit(**o): d=dict(_SEAT); d.update(o); return d
POSES2={
 'coffee_togo':   ('Holding a to-go coffee',dict(head=-2,ikN=[38,-58],hN='grip',wN=-90,holdN=coffee_togo_in_hand(),aF=[-6,14],expr='content')),
 'umbrella':      ('Under an umbrella',dict(head=6,lean=2,ikN=[30,-74],hN='fist',wN=-100,holdN=umbrella_in_hand(),aF=[-4,10],expr='sad',look=(.3,.3))),
 'briefcase':     ('Commuter with briefcase',dict(lean=3,aN=[6,6],hN='grip',wN=0,holdN=briefcase_in_hand(),aF=[-14,18],expr='determined')),
 'shopping':      ('Carrying shopping bags',dict(aN=[10,6],hN='grip',holdN=shopping_bag_in_hand(),aF=[-10,8],hF='grip',holdF=shopping_bag_in_hand('#B8D4E8','#3E6A8A'),expr='happy')),
 'dumbbell_curl': ('Bicep curl',dict(lean=-2,ikN=[34,-62],hN='fist',wN=-110,holdN=dumbbell_in_hand(),aF=[-8,10],hF='fist',expr='determined',fx=['sweat'])),
 'drink_water':   ('Drinking water',dict(head=-18,lean=-3,ikN=[30,-136],hN='grip',wN=-160,holdN=bottle_in_hand(tilt=-120),aF=[-6,12],expr='content')),
 'read_letter':   ('Reading a letter (shock)',dict(head=10,ikN=[48,-82],hN='grip',wN=-60,holdN=letter_in_hand(),ikF=[42,-76],hF='grip',wF=-60,look=(.6,.5),expr='shocked')),
 'give_flower':   ('Offering a flower (shy)',dict(lean=4,head=10,aN=[66,26],hN='fist',wN=-90,holdN=flower_in_hand(),aF=[-20,30],expr='shy')),
 'carry_box':     ('Carrying a box',dict(lean=-4,head=-4,ikN=[50,-56],hN='flat',wN=-90,ikF=[44,-52],hF='flat',holdN=box_in_hands(),expr='nervous',fx=['sweat'])),
 'selfie':        ('Taking a selfie',dict(head=-6,aN=[150,-20],hN='grip',wN=0,holdN=selfie_phone(),aF=[-6,14],look=(.8,-.6),expr='wink')),
 'sing_mic':      ('Singing into a mic',dict(lean=-6,head=-10,ikN=[34,-118],hN='fist',wN=-170,holdN=mic_in_hand(),aF=[40,60],hF='spread',expr='laugh',mouth='O')),
 'listen_music':  ('Vibing with headphones',dict(head=-6,ikN=[-6,-150],hN='open',wN=-200,aF=[-8,30],hF='relax',expr='content',acc=['headphones'])),
 'cry_hands':     ('Crying into hands',dict(lean=6,curl=.5,head=18,ikN=[34,-132],hN='open',wN=-170,ikF=[28,-128],hF='open',wF=-170,expr='sobbing')),
 'angry_fists':   ('Angry, fists clenched',dict(lean=6,head=-4,aN=[-18,46],hN='fist',aF=[-30,52],hF='fist',lN=[8,4],lF=[-8,4],expr='furious',fx=['vein'])),
 'yawn':          ('Yawning',dict(lean=-4,head=-14,ikN=[30,-128],hN='fist',wN=-170,aF=[-4,10],expr='sleepy',mouth='yawn')),
 'bow':           ('Polite bow',dict(lean=48,curl=.1,head=6,aN=[-44,6],aF=[-50,6],hN='flat',hF='flat',expr='content')),
 'hands_hips':    ('Hands on hips (side)',dict(lean=-3,ikN=[10,-28,-1],hN='fist',wN=-40,ikF=[-14,-28,1],hF='fist',expr='proud')),
 'sit_laptop':    ('Laptop on lap',_sit(lean=10,head=14,ikN=[70,-30],hN='flat',wN=-80,ikF=[62,-26],hF='flat',wF=-80,look=(.7,.5),expr='focused',mid=laptop_on_lap())),
 'sit_gaming':    ('Gaming with controller',_sit(lean=14,head=6,ikN=[52,-28],hN='grip',wN=-90,holdN=controller_in_hands(),ikF=[46,-24],hF='grip',wF=-90,expr='excited')),
 'sit_sleep':     ('Dozed off sitting',_sit(lean=2,curl=.3,head=34,aN=[20,30],aF=[16,34],hN='relax',hF='relax',expr='sleeping')),
 'sit_coffee':    ('Sitting with coffee',_sit(lean=4,head=-2,ikN=[40,-52],hN='grip',wN=-90,holdN=mug_in_hand(),aF=[30,40],expr='content')),
 'sit_think':     ('Sitting, chin on hand',_sit(lean=18,head=4,ikN=[42,-100],hN='fist',wN=-170,ikF=[50,-30],hF='relax',look=(.7,-.4),expr='thinking')),
}
FRONT2={
 'front_thumbs_up':('Front – thumbs up',dict(aN=[30,120],hN='thumb',wN=-10,expr='happy')),
 'front_clap':     ('Front – clapping',dict(ikN=[7,-52,-1],ikF=[-7,-52,-1],hN='flat',hF='flat',expr='joy')),
 'front_heart':    ('Front – heart hands',dict(aN=[155,75],aF=[155,75],hN='claw',hF='claw',expr='in_love')),
 'front_umbrella': ('Front – umbrella',dict(aN=[26,-24],hN='fist',holdN=umbrella_in_hand(tilt=-9,L=205),expr='neutral')),
 'front_briefcase':('Front – with briefcase',dict(aN=[8,0],hN='grip',holdN=briefcase_in_hand(),expr='determined')),
 'front_coffee':   ('Front – coffee in hand',dict(aN=[12,-36],hN='grip',holdN=coffee_togo_in_hand(),expr='content')),
}
POSES.update(POSES2); FRONT.update(FRONT2)
