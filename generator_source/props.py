from sv import *
LW='2.4'
def S(c,w=LW,k=.55): return dict(fill=c,stroke=dark(c,k),stroke_width=w,stroke_linejoin='round')
def R(x,y,w,h,c,rx=0,k=.55,**o):
    a=S(c,k=k) if c!='none' else dict(fill='none',stroke_width=LW); a.update(o); return rect(x,y,w,h,rx=rx,**a)
def hi(d,c,op='.35',w=3): return path(d,fill='none',stroke=c,stroke_width=w,stroke_linecap='round',opacity=op)
WOOD='#7A5A43'; WOOD_D='#5A4232'; WOOD_L='#9C7656'; SHEET='#5D6B84'; PIL='#D5DAE4'
# ======== BEDROOM ========
def bed(w=420,frame=WOOD,sheet=SHEET,blanket='#3F5A8C',messy=False,lump=False,pillow=PIL):
    # origin: bottom-left at floor (0,0). mattress top at y=-110
    s=''
    s+=R(-36,-300,46,300,frame,rx=12)+R(-26,-286,26,250,dark(frame,.15),rx=8,stroke='none')
    s+=R(-36,-300,46,22,light(frame,.15),rx=10)
    s+=R(0,-86,w,70,frame,rx=8)+R(8,-16,24,16,dark(frame,.35))+R(w-32,-16,24,16,dark(frame,.35))
    s+=hi(f'M14 -70 L{w-14} -70',light(frame,.3),'.35')
    s+=R(0,-128,w,50,sheet,rx=18)+rect(4,-92,w-8,10,fill='#000',opacity='.15')
    # pillow
    s+=path(f'M14 -128 C6 -176 150 -184 160 -132 C166 -114 18 -110 14 -128Z',**S(pillow,k=.45))+hi('M34 -150 Q86 -170 140 -152',light(pillow,.5),'.7')
    if messy:
        pts=[[150,-150],[210,-170],[270,-150],[330,-176],[392,-148],[w+12,-120]]
        d=smooth(pts,False)+f'L{w+14} -70 Q{w*.6} -60 140 -76 Q120 -110 150 -150Z'
        s+=path(d,**S(blanket,k=.5))
        for x in (220,300,370): s+=hi(f'M{x} -150 Q{x+20} -110 {x+6} -78',dark(blanket,.25),'.7',4)
        s+=hi(smooth(pts,False),light(blanket,.3),'.6',3)
    elif lump:
        d=f'M120 -132 C150 -230 330 -230 380 -150 C410 -140 {w+10} -136 {w+12} -118 L{w+14} -70 Q{w*.6} -60 110 -76 Q96 -104 120 -132Z'
        s+=path(d,**S(blanket,k=.5))+hi('M170 -190 Q250 -230 340 -180',light(blanket,.3),'.6',4)+hi('M260 -200 Q280 -130 268 -80',dark(blanket,.25),'.6',4)
    else:
        d=f'M170 -134 L{w+10} -134 L{w+14} -70 Q{w*.6} -62 166 -72Z'
        s+=path(d,**S(blanket,k=.5))+path(f'M170 -134 L{w+10} -134 L{w+10} -118 L168 -118Z',fill=light(blanket,.25))+hi(f'M240 -110 Q250 -90 244 -74 M330 -110 Q340 -90 334 -74',dark(blanket,.25),'.6',4)
    s+=R(w-8,-170,34,170,frame,rx=10)+R(w-8,-170,34,16,light(frame,.15),rx=8)
    return s
def double_bed(): return bed(w=560,blanket='#8A4F5E',sheet='#D9D2C4',pillow='#EEE9DF')
def nightstand(drawer_open=False):
    s=R(-60,-130,120,130,WOOD,rx=6)+R(-68,-140,136,16,WOOD_L,rx=5)
    s+=R(-50,-110,100,48,WOOD_D,rx=4)+R(-14,-90,28,7,'#D7B270',rx=3.5)
    s+=R(-50,-54,100,44,WOOD_D,rx=4)+R(-14,-36,28,7,'#D7B270',rx=3.5)
    s+=R(-56,0,14,6,dark(WOOD,.4))+R(42,0,14,6,dark(WOOD,.4))
    return s
def lamp(on=True):
    s=''
    if on: s+=ell(0,-150,170,150,fill='url(#lampGlow)')
    s+=ell(0,-6,34,8,**S('#3A3532'))+R(-5,-110,10,104,'#3A3532')
    sh='#FFE2A8' if on else '#7D7368'
    s+=path('M-46 -108 L46 -108 L30 -180 L-30 -180Z',**S(sh,k=.5 if on else .5))
    if on: s+=path('M-40 -108 L40 -108 L48 -100 L-48 -100Z',fill='#FFF3CF',opacity='.6')
    s+=hi('M-22 -170 L-34 -116',light(sh,.5),'.6',4)
    return s
def desk_lamp(on=True):
    s=''
    if on: s+=path('M40 -140 L-60 0 L160 0Z',fill='#FFE7B0',opacity='.18')
    s+=ell(0,-6,36,9,**S('#2F3A4A'))+path('M0 -10 L-30 -110 L40 -150',fill='none',stroke='#2F3A4A',stroke_width=8,stroke_linecap='round',stroke_linejoin='round')
    s+=circ(-30,-110,7,**S('#3E4B60'))
    s+=path('M20 -168 L72 -142 L56 -112 L4 -140Z',**S('#3E4B60'))+(path('M56 -112 L72 -142 L80 -136 L62 -106Z',fill='#FFF3CF') if on else '')
    return s
def wardrobe():
    s=R(-130,-420,260,410,WOOD,rx=6)+R(-140,-432,280,20,WOOD_L,rx=6)
    s+=R(-118,-400,114,380,WOOD_D,rx=4)+R(4,-400,114,380,WOOD_D,rx=4)
    s+=R(-20,-220,8,40,'#D7B270',rx=4)+R(12,-220,8,40,'#D7B270',rx=4)
    s+=hi('M-100 -380 L-100 -40 M24 -380 L24 -40',light(WOOD,.25),'.25',5)
    s+=R(-120,-10,20,10,dark(WOOD,.4))+R(100,-10,20,10,dark(WOOD,.4))
    return s
def desk(w=380):
    s=R(-w/2,-200,w,22,WOOD_L,rx=5)
    s+=R(-w/2+14,-178,18,178,WOOD)+R(w/2-32,-178,18,178,WOOD)
    s+=R(w/2-170,-178,150,92,WOOD,rx=4)+R(w/2-115,-136,40,8,'#D7B270',rx=4)
    s+=hi(f'M{-w/2+10} -192 L{w/2-10} -192',light(WOOD_L,.4),'.4',3)
    return s
def table(w=320,c=WOOD_L):
    return R(-w/2,-170,w,20,c,rx=6)+R(-w/2+20,-150,16,150,dark(c,.2))+R(w/2-36,-150,16,150,dark(c,.2))+rect(-w/2+30,-150,w-60,8,fill='#000',opacity='.18')
def chair_wood(c=WOOD):
    s=R(-12,-300,18,300,c,rx=6)+R(-12,-300,100,18,light(c,.1),rx=6)+R(-8,-250,90,10,c,rx=4)
    s+=R(-16,-130,110,20,light(c,.15),rx=6)+R(74,-112,16,112,c,rx=4)+R(-8,-112,16,112,dark(c,.15),rx=4)
    return s
def office_chair(c='#2E3340'):
    s=R(-70,-330,30,170,c,rx=14)+R(-62,-320,14,140,light(c,.12),rx=7,stroke='none')
    s+=R(-70,-160,150,26,light(c,.08),rx=12)+R(-8,-134,14,70,'#5B6170')
    s+=path('M-70 -18 L-2 -60 L66 -18',fill='none',stroke='#5B6170',stroke_width=9,stroke_linecap='round',stroke_linejoin='round')
    s+=circ(-70,-10,9,**S('#22252D'))+circ(66,-10,9,**S('#22252D'))+circ(-2,-12,9,**S('#22252D'))
    s+=R(30,-210,50,12,c,rx=6)+R(54,-200,10,44,c)
    return s
def sofa(c='#6E5A8A',w=480):
    s=R(-w/2,-250,w,150,c,rx=30)+R(-w/2-30,-190,70,170,light(c,.08),rx=26)+R(w/2-40,-190,70,170,light(c,.08),rx=26)
    s+=R(-w/2+30,-130,w-60,80,light(c,.12),rx=16)+path(f'M0 -128 L0 -54',stroke=dark(c,.3),stroke_width=3)
    s+=R(-w/2+20,-30,20,30,dark(c,.5))+R(w/2-40,-30,20,30,dark(c,.5))
    s+=hi(f'M{-w/2+40} -230 Q0 -244 {w/2-40} -230',light(c,.35),'.4',4)
    return s
def armchair(c='#B8694F'): return sofa(c,w=230)
def bookshelf():
    s=R(-120,-460,240,460,WOOD_D,rx=4)+R(-108,-448,216,436,dark(WOOD_D,.25),stroke='none')
    cols=['#B8463A','#3E6A8A','#6B8A3E','#C9963B','#6A4A8A','#D9D2C4','#3A7A6E','#8A3E5A']
    rr=rnd(3)
    for sh in range(4):
        y=-448+sh*110+108
        s+=R(-108,y-8,216,10,WOOD)
        x=-104
        while x<90:
            bw=rr.uniform(14,24); bh=rr.uniform(66,96); c=rr.choice(cols)
            if rr.random()<.12 and x<60:
                s+=g(R(0,-bh,bw,bh,c,rx=2),transform=f'translate({f(x+bh*.3)} {f(y-8)}) rotate(18)'); x+=bh*.45; continue
            s+=R(x,y-8-bh,bw,bh,c,rx=2)+rect(x+3,y-8-bh*.75,bw-6,3,fill='#fff',opacity='.35')
            x+=bw+1.5
    return s
def book_stack(n=4,dust=False):
    s=''; y=0; cols=['#8A3A3A','#3A5A7A','#5B7A3A','#9A7A3A','#5A3A7A','#A08A60']; rr=rnd(7)
    for i in range(n):
        h=rr.uniform(20,30); w=rr.uniform(150,200); ox=rr.uniform(-12,12); y-=h; c=cols[i%6]
        s+=R(ox-w/2,y,w,h,c,rx=3)+rect(ox-w/2+10,y+h*.38,w-20,3,fill='#EADDB8',opacity='.55')+R(ox+w/2-10,y+2,8,h-4,'#F1EBDD',stroke='none')
    if dust:
        s+=rect(-100,y-3,200,5,fill='#B8B0A0',opacity='.45',rx=2)
        for i in range(6): s+=circ(-80+i*30,y-8-rr.random()*10,1.5,fill='#C9C1B0',opacity='.5')
    return s
def book_open():
    return path('M0 0 L-90 -14 L-90 -110 L0 -96Z',**S('#F3EEE2',k=.4))+path('M0 0 L90 -14 L90 -110 L0 -96Z',**S('#FBF8F0',k=.4))+''.join(hi(f'M-78 {-90+i*14} L-12 {-80+i*14}','#A39A88','.8',2)+hi(f'M12 {-80+i*14} L78 {-90+i*14}','#A39A88','.8',2) for i in range(5))+path('M-96 -8 L0 6 L96 -8 L96 2 L0 14 L-96 2Z',**S('#8A3A3A'))
def laptop(open_=True,screen='#3B5B8A',content=''):
    s=''
    if open_:
        s+=path('M-110 -16 L110 -16 L128 0 L-128 0Z',**S('#A7ADB6',k=.5))
        s+=g(R(-105,-160,210,144,'#2B2F36',rx=8)+rect(-96,-151,192,126,fill=screen,rx=3)+content,transform='translate(0 0)')
        s+=rect(-20,-6,40,4,rx=2,fill='#7D838C')
        s+=circ(0,-155,1.8,fill='#555')
    else:
        s+=R(-118,-14,236,14,'#A7ADB6',rx=5)+hi('M-100 -8 L100 -8','#D9DDE2','.6',2)
    return s
def monitor(screen='#3B5B8A'):
    return R(-150,-250,300,180,'#23262D',rx=10)+rect(-138,-238,276,156,fill=screen,rx=3)+R(-14,-70,28,56,'#3A3E47')+R(-70,-18,140,18,'#3A3E47',rx=6)+R(-130,40,260,22,'#2F333B',rx=6)
def keyboard(): 
    s=R(-130,-22,260,22,'#3A3E47',rx=6)
    for r_ in range(2):
        for i in range(12): s+=rect(-120+i*20,-18+r_*9,16,6,rx=1.5,fill='#5A606C')
    return s
def mug(c='#E9E2D4',steam=True):
    s=path('M24 -48 q22 0 22 18 q0 18 -22 18',fill='none',stroke=dark(c,.45),stroke_width=9)+path('M24 -48 q22 0 22 18 q0 18 -22 18',fill='none',stroke=c,stroke_width=4)
    s+=path('M-26 -62 L26 -62 L22 -6 Q22 0 16 0 L-16 0 Q-22 0 -22 -6Z',**S(c,k=.45))+rect(-24,-44,48,10,fill='#C8573E')
    s+=ell(0,-62,26,5,fill='#4A2E22',stroke=dark(c,.45),stroke_width=2)
    if steam: s+=''.join(path(f'M{x} -74 q-8 -12 0 -24 q8 -12 0 -24',fill='none',stroke='#DCE3EE',stroke_width=4,stroke_linecap='round',opacity='.5') for x in (-10,10))
    return s
def plant(kind='monstera'):
    s=''
    pot='#C8734E'
    if kind=='monstera':
        rr=rnd(2)
        for i,(a,l) in enumerate([(-50,120),(-20,150),(15,140),(45,115),(-75,90),(70,95),(0,100)]):
            tip=add([0,-70],mul(dirv(180+a),l)); mid=add([0,-70],mul(dirv(180+a*1.1),l*.5))
            s+=path(f'M0 -70 Q{P(mid)} {P(tip)}',fill='none',stroke='#3E6B3A',stroke_width=4)
            c=['#4E8A48','#5FA055','#447A3F'][i%3]
            s+=g(path('M0 0 C-30 -10 -34 -50 0 -64 C34 -50 30 -10 0 0Z',**S(c,k=.45))+path('M0 -4 L0 -58',stroke=dark(c,.3),stroke_width=2),transform=f'translate({f(tip[0])} {f(tip[1])}) rotate({f(a)}) translate(0 28)')
    elif kind=='cactus':
        c='#5E9A5A'
        s+=R(-22,-180,44,150,c,rx=22)+path('M-22 -100 L-46 -100 Q-56 -100 -56 -110 L-56 -140',fill='none',stroke=dark(c,.45),stroke_width=24,stroke_linecap='round')+path('M-22 -100 L-46 -100 Q-56 -100 -56 -110 L-56 -140',fill='none',stroke=c,stroke_width=19,stroke_linecap='round')
        s+=path('M22 -120 L44 -120 Q52 -120 52 -130 L52 -150',fill='none',stroke=dark(c,.45),stroke_width=22,stroke_linecap='round')+path('M22 -120 L44 -120 Q52 -120 52 -130 L52 -150',fill='none',stroke=c,stroke_width=17,stroke_linecap='round')
        s+=hi('M-6 -170 L-6 -50',light(c,.3),'.5',3)+circ(0,-186,7,fill='#E8708A')
    elif kind=='dead':
        s+=path('M0 -70 Q-20 -110 -50 -100 M0 -70 Q8 -120 34 -128 M0 -70 Q20 -96 48 -80',fill='none',stroke='#7A6A4A',stroke_width=4,stroke_linecap='round')
        for (x,y,a) in((-50,-100,-120),(34,-128,30),(48,-80,100)): s+=g(path('M0 0 C-10 -4 -12 -18 0 -24 C12 -18 10 -4 0 0Z',**S('#9A8A5A')),transform=f'translate({x} {y}) rotate({a})')
        s+=g(path('M0 0 C-10 -4 -12 -18 0 -24 C12 -18 10 -4 0 0Z',**S('#9A8A5A')),transform='translate(70 -6) rotate(80)')
    s+=path('M-52 -76 L52 -76 L40 0 L-40 0Z',**S(pot))+R(-58,-86,116,18,light(pot,.1),rx=4)+hi('M-34 -60 L-28 -10',light(pot,.4),'.4',4)
    return s
def trash_bin(full=False):
    s=''
    if full:
        for (x,y,r) in ((-30,-150,20),(10,-160,24),(36,-146,18),(60,-110,18)): s+=circ(x,y,r,**S('#EDE8DC',k=.4))+hi(f'M{x-r*.5} {y} q{r*.3} -{r*.4} {r*.8} 0','#B5AE9F','.9',2)
    s+=path('M-56 -140 L56 -140 L46 0 L-46 0Z',**S('#5A6676'))+R(-62,-150,124,16,'#6E7A8A',rx=6)
    for x in (-24,0,24): s+=path(f'M{x} -126 L{x*0.85} -14',stroke=dark('#5A6676',.3),stroke_width=4,stroke_linecap='round')
    return s
def crumpled_paper():
    pts=[[-22,-6],[-14,-24],[2,-30],[18,-22],[24,-6],[16,6],[-2,10],[-18,4]]
    return path(smooth(pts),**S('#EDE8DC',k=.45))+path('M-12 -16 L0 -8 L10 -20 M-6 0 L4 -8 L14 -2',fill='none',stroke='#B5AE9F',stroke_width=2)
def rug(c='#8A4F5E'):
    return ell(0,0,240,46,**S(c,k=.35))+ell(0,0,200,34,fill='none',stroke=light(c,.3),stroke_width=5,stroke_dasharray='14 8')+ell(0,0,140,20,fill=dark(c,.12))
def tv(screen='#2A3A5A',on=True):
    s=R(-220,-300,440,260,'#17191F',rx=10)+rect(-206,-286,412,232,fill=screen if on else '#0C0D11')
    if on: s+=path('M-206 -286 L-60 -286 L-206 -120Z',fill='#fff',opacity='.06')
    s+=R(-60,-40,120,14,'#2A2D35',rx=4)+R(-160,-26,320,26,'#3A3E47',rx=4)
    return s
def fridge():
    c='#DDE3EA'
    s=R(-100,-460,200,460,c,rx=16)+path('M-100 -300 L100 -300',stroke=dark(c,.45),stroke_width=3)
    s+=R(66,-440,12,100,'#9AA3AF',rx=6)+R(66,-270,12,120,'#9AA3AF',rx=6)
    s+=R(-70,-430,50,40,'#F2C14E',rx=2,stroke='none')+R(-60,-380,40,46,'#8FC9F5',stroke='none',transform='rotate(-6 -40 -360)')
    s+=hi('M-80 -440 L-80 -320 M-80 -280 L-80 -30','#ffffff','.5',5)
    return s
def kitchen_counter(w=520):
    c='#C7B8A2'
    s=R(-w/2,-200,w,200,'#5E7A8A',rx=4)+R(-w/2-10,-220,w+20,24,c,rx=4)
    n=int(w//130)
    for i in range(n):
        x=-w/2+10+i*(w-20)/n
        s+=R(x+6,-186,(w-20)/n-12,170,light('#5E7A8A',.08),rx=4)+R(x+(w-20)/n/2-14,-170,28,6,'#C9CED6',rx=3)
    s+=R(w/2-170,-260,60,40,'#3A3E47',rx=6)+path(f'M{w/2-140} -260 L{w/2-140} -300 L{w/2-100} -300',fill='none',stroke='#9AA3AF',stroke_width=7,stroke_linecap='round')
    return s
def stove_pot(): return R(-60,-70,120,70,'#5A6676',rx=10)+R(-70,-80,140,14,'#6E7A8A',rx=6)+R(-12,-96,24,16,'#3A3E47',rx=5)+R(-92,-60,26,10,'#3A3E47',rx=5)+R(66,-60,26,10,'#3A3E47',rx=5)
def backpack(c='#C8573E'):
    s=path('M-50 -40 C-60 -150 60 -150 50 -40 L50 -10 Q50 0 40 0 L-40 0 Q-50 0 -50 -10Z',**S(c))
    s+=R(-36,-70,72,52,dark(c,.12),rx=12)+path('M-36 -52 L36 -52',stroke=dark(c,.45),stroke_width=2.4)+path('M-16 -150 Q0 -176 16 -150',fill='none',stroke=dark(c,.4),stroke_width=7)
    s+=R(-4,-60,8,10,'#D7B270',rx=2)
    return s
def sneakers(c='#E9A23B'):
    import rig
    return g(rig.shoe([0,0],90,c),transform='translate(-20 -9) scale(2)')+g(rig.shoe([0,0],90,dark(c,.08)),transform='translate(30 -9) scale(2)')
def dumbbell():
    s=R(-70,-12,140,24,'#8D939C',rx=6)
    for x in (-90,62): s+=R(x,-40,28,80,'#2E3240',rx=6)+R(x+(-14 if x<0 else 28),-30,14,60,'#3E4350',rx=4)
    return g(s,transform='translate(0 -40)')
def guitar():
    c='#C27A3A'
    s=path('M0 0 C-60 0 -70 -60 -40 -90 C-56 -120 -40 -160 0 -160 C40 -160 56 -120 40 -90 C70 -60 60 0 0 0Z',**S(c))
    s+=circ(0,-80,18,fill='#2A1D14')+R(-8,-330,16,180,'#5A3A22',rx=3)+R(-14,-366,28,40,'#3A2A1A',rx=5)+R(-26,-36,52,10,'#3A2A1A',rx=3)
    s+=''.join(path(f'M{x} -330 L{x} -36',stroke='#E8E2D4',stroke_width=1) for x in (-4,-1.3,1.3,4))
    return s
# ======== TIME ========
def wall_clock(hh=10,mm=10,c='#F3EEE2',rim='#3A3E47',broken=False):
    s=circ(0,0,92,**S(rim,k=.5))+circ(0,0,80,**S(c,k=.3))
    for i in range(60):
        a=i/60*2*math.pi; big=i%5==0
        r1=72 if not big else 64
        s+=line([math.sin(a)*r1,-math.cos(a)*r1],[math.sin(a)*76,-math.cos(a)*76],stroke='#3A3E47',stroke_width=4 if big else 1.6)
    for n in (12,3,6,9):
        a=n/12*2*math.pi; s+=text(str(n),math.sin(a)*52,-math.cos(a)*52+8,size=22,fill='#3A3E47',weight=700,anchor='middle')
    ha=(hh%12+mm/60)/12*360; ma=mm/60*360
    s+=g(R(-4,-46,8,52,'#22252D',rx=4),transform=f'rotate({f(ha)})')+g(R(-3,-66,6,74,'#22252D',rx=3),transform=f'rotate({f(ma)})')
    s+=g(line([0,10],[0,-70],stroke='#D6453A',stroke_width=2),transform=f'rotate({f(ma*3.3)})')+circ(0,0,6,fill='#D6453A')
    s+=path('M-60 -50 Q-30 -76 10 -78',fill='none',stroke='#fff',stroke_width=6,stroke_linecap='round',opacity='.35')
    if broken:
        s+=path('M-20 -80 L-6 -40 L-30 -10 L4 20 L-12 60 L6 80',fill='none',stroke='#22252D',stroke_width=3,stroke_linejoin='round')
        s+=path('M-30 -10 L-74 -6 M4 20 L50 34 M-6 -40 L30 -54',fill='none',stroke='#22252D',stroke_width=2.4)
    return g(s,transform='translate(0 -92)')
def alarm_clock(ring=False,c='#D6453A'):
    s=''
    if ring: s+=''.join(path(d,fill='none',stroke='#FFD86B',stroke_width=5,stroke_linecap='round') for d in ('M-96 -150 Q-110 -120 -98 -92','M96 -150 Q110 -120 98 -92','M-116 -168 Q-136 -120 -118 -76','M116 -168 Q136 -120 118 -76'))
    s+=path('M-50 -10 L-64 6 M50 -10 L64 6',stroke='#3A3E47',stroke_width=8,stroke_linecap='round')
    s+=circ(-52,-176,26,**S('#E2C26B'))+circ(52,-176,26,**S('#E2C26B'))+R(-6,-208,12,18,'#3A3E47',rx=4)
    s+=circ(0,-100,84,**S(c))+circ(0,-100,66,**S('#F6F1E6',k=.3))
    for i in range(12):
        a=i/12*2*math.pi; s+=line([math.sin(a)*52,-100-math.cos(a)*52],[math.sin(a)*60,-100-math.cos(a)*60],stroke='#3A3E47',stroke_width=4)
    s+=g(R(-4,-40,8,44,'#22252D',rx=4),transform='translate(0 -100) rotate(-60)')+g(R(-3,-54,6,58,'#22252D',rx=3),transform='translate(0 -100) rotate(0)')+circ(0,-100,6,fill=c)
    s+=path('M-52 -146 Q-30 -168 0 -170',fill='none',stroke='#fff',stroke_width=7,stroke_linecap='round',opacity='.3')
    return s
def digital_clock(t='07:00',c='#2A2D35',led='#FF5A4E'):
    s=path('M-120 0 L-110 -100 Q-108 -110 -96 -110 L96 -110 Q108 -110 110 -100 L120 0Z',**S(c))
    s+=R(-92,-94,184,70,'#0B0C10',rx=8)+text(t,0,-40,size=56,fill=led,weight=700,anchor='middle',family="'Courier New', monospace",letter_spacing='2')
    s+=rect(-92,-94,184,70,rx=8,fill=led,opacity='.08')
    return s
def hourglass(top=.3):
    s=R(-70,-250,140,18,WOOD,rx=6)+R(-70,-18,140,18,WOOD,rx=6)+R(-62,-232,10,214,WOOD_D)+R(52,-232,10,214,WOOD_D)
    s+=path('M-44 -232 C-44 -170 -6 -150 -6 -125 C-6 -100 -44 -80 -44 -18 L44 -18 C44 -80 6 -100 6 -125 C6 -150 44 -170 44 -232Z',fill='#DCEBFA',fill_opacity='.35',stroke='#9AB0C8',stroke_width=2.4)
    ty=-232+ (1-top)*100
    s+=path(f'M{-38*top-6} {f(-145-top*60)} Q0 {f(-150-top*70)} {38*top+6} {f(-145-top*60)} L6 -128 L-6 -128Z',fill='#E2B65A')
    s+=line([0,-125],[0,-30],stroke='#E2B65A',stroke_width=2.4)
    s+=path(f'M-40 -20 Q0 {f(-20-(1-top)*90)} 40 -20Z',fill='#E2B65A')
    return s
def calendar_page(day='13',month='DEADLINE',circled=True):
    s=R(-90,-200,180,200,'#F7F3EA',rx=8)+R(-90,-200,180,52,'#D6453A',rx=8)+rect(-90,-160,180,12,fill='#D6453A')
    s+=text(month,0,-164,size=24,fill='#fff',weight=800,anchor='middle',letter_spacing='2')
    s+=text(day,0,-46,size=96,fill='#2A2D35',weight=800,anchor='middle')
    for x in (-50,50): s+=R(x-6,-214,12,30,'#8D939C',rx=6)
    if circled: s+=path('M-60 -100 C-40 -150 70 -140 66 -80 C62 -20 -50 -20 -62 -70 C-66 -90 -50 -120 -20 -126',fill='none',stroke='#D6453A',stroke_width=5,stroke_linecap='round')
    return s
def calendar_month():
    s=R(-160,-300,320,300,'#F7F3EA',rx=10)+R(-160,-300,320,60,'#3E6A8A',rx=10)+rect(-160,-252,320,12,fill='#3E6A8A')
    s+=text('NOVEMBER',0,-258,size=28,fill='#fff',weight=800,anchor='middle',letter_spacing='3')
    rr=rnd(5)
    for i in range(35):
        x=-140+(i%7)*40; y=-226+(i//7)*44
        s+=R(x,y,34,38,'#ECE6D8',rx=4,stroke='none')+text(str(i+1) if i<30 else '',x+6,y+16,size=12,fill='#6B6256',weight=600)
        if i<12: s+=path(f'M{x+6} {y+24}L{x+28} {y+34}M{x+28} {y+24}L{x+6} {y+34}',stroke='#D6453A',stroke_width=3,stroke_linecap='round')
    return s
# ======== WALL / DECOR ========
def window(w=320,h=360,mode='night',curtain=None):
    # origin bottom-center of sill
    id_=uid('win'); x=-w/2; y=-h-30
    sky={'night':('#0B1530','#1C2C55'),'day':('#8EC5F0','#D9EEFA'),'sunset':('#3A2C5A','#F2A65A'),'dawn':('#5A6A9A','#F2C7A0')}[mode]
    defs=lg(id_+'g',[(0,sky[0]),(1,sky[1])])
    v=rect(x,y,w,h,fill=f'url(#{id_}g)')
    rr=rnd(11)
    if mode=='night':
        v+=circ(x+w*.72,y+h*.24,30,fill='#EEF2FC')+circ(x+w*.72,y+h*.24,62,fill='#CFE0FF',opacity='.12')+circ(x+w*.68,y+h*.21,6,fill='#D7DDEA')
        for i in range(30): v+=circ(x+rr.random()*w,y+rr.random()*h*.6,rr.uniform(.8,1.8),fill='#fff',opacity=f(rr.uniform(.3,.9)))
    elif mode=='day':
        v+=circ(x+w*.25,y+h*.22,26,fill='#FFF3C4',opacity='.95')+circ(x+w*.25,y+h*.22,50,fill='#FFF3C4',opacity='.25')
        for (cx,cy) in ((x+w*.65,y+h*.25),(x+w*.3,y+h*.45)): v+=''.join(circ(cx+dx,cy+dy,rr_,fill='#fff',opacity='.9') for dx,dy,rr_ in ((-20,0,16),(0,-8,20),(22,0,15),(0,6,14)))
    elif mode in('sunset','dawn'):
        v+=circ(x+w*.5,y+h*.75,40,fill='#FFD27A',opacity='.95')
    bc={'night':'#121A30','day':'#9DB7CF','sunset':'#4A3048','dawn':'#6A6A8A'}[mode]
    for i in range(9):
        bw=rr.uniform(26,46); bh=rr.uniform(70,200); bx=x+i*(w/8)-12
        v+=rect(bx,y+h-bh,bw,bh,fill=bc)
        if mode=='night':
            for k in range(8):
                if rr.random()>.6: v+=rect(bx+5+(k%2)*14,y+h-bh+12+(k//2)*22,6,9,fill='#FFD98A',opacity='.85')
    s=f'<defs>{defs}<clipPath id="{id_}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"/></clipPath></defs>'
    s+=g(v,clip_path=f'url(#{id_})')
    s+=path(f'M{x} {y} L{x+w*.45} {y} L{x} {y+h*.5}Z',fill='#fff',opacity='.06')
    fr='#E9E4DA' if mode=='day' else '#2B2F3A'
    s+=rect(x-12,y-12,w+24,h+24,fill='none',stroke=fr,stroke_width=24)+R(-6,y,12,h,fr,stroke='none')+R(x,y+h/2-6,w,12,fr,stroke='none')
    s+=rect(x-24,y-24,w+48,h+48,fill='none',stroke=dark(fr,.35),stroke_width=2)
    s+=R(x-34,-30,w+68,22,light(fr,.08) if mode=='day' else '#363B48',rx=4)
    if curtain: s+=curtains(w,h,curtain)
    return s
def curtains(w=320,h=360,openness=.8,col='#4A3A5E'):
    x=-w/2; y=-h-30; s=''
    s+=R(x-80,y-50,w+160,12,'#5B5048',rx=6)+circ(x-84,y-44,10,**S('#5B5048'))+circ(x+w+84,y-44,10,**S('#5B5048'))
    for ax,sg in ((x-70,1),(x+w+70,-1)):
        pw=lerp(w/2+70,80,openness); folds=6; bottom=y+h+60
        d=f'M{f(ax)} {f(y-40)}L{f(ax+sg*pw)} {f(y-40)}L{f(ax+sg*pw*(1+.0))} {f(bottom)}'
        for i in range(folds-1,-1,-1):
            px=ax+sg*pw*i/folds; d+=f'Q{f(px+sg*pw/folds/2)} {f(bottom+12)} {f(px)} {f(bottom)}'
        s+=path(d+'Z',**S(col,k=.5))
        for i in range(1,folds): px=ax+sg*pw*i/folds; s+=path(f'M{f(px)} {f(y-36)}L{f(px)} {f(bottom)}',stroke=dark(col,.3),stroke_width=f(lerp(10,5,openness)),opacity='.75')
        s+=hi(f'M{f(ax+sg*pw*.08)} {f(y-30)} L{f(ax+sg*pw*.08)} {f(bottom-10)}',light(col,.3),'.4',4)
    return s
def door(open_=0,c='#6B4F3C',light_='#FFE3A8',w=200,h=400):
    s=R(-w/2-16,-h-16,w+32,h+16,dark(c,.35))
    s+=rect(-w/2,-h,w,h,fill=light_ if open_ else '#141210')
    if open_:
        s+=path(f'M{-w/2} 0 L{w/2} 0 L{w/2+240*open_} 140 L{-w/2-80*open_} 140Z',fill=light_,opacity='.22')
        dw=w*math.cos(open_*1.3)
        s+=path(f'M{-w/2} {-h} L{-w/2+dw} {-h+22*open_} L{-w/2+dw} {-10*open_} L{-w/2} 0Z',**S(c))
        if dw>40: s+=R(-w/2+18,-h+30,dw-36,h*.36,dark(c,.12),rx=4)+circ(-w/2+dw-20,-h/2,8,**S('#D7B270'))
    else:
        s+=R(-w/2,-h,w,h,c)
        s+=R(-w/2+22,-h+26,w-44,h*.38,dark(c,.12),rx=4)+R(-w/2+22,-h*.5,w-44,h*.42,dark(c,.12),rx=4)
        s+=circ(w/2-24,-h/2,9,**S('#D7B270'))+hi(f'M{-w/2+10} {-h+10} L{-w/2+10} -10',light(c,.3),'.35',4)
    return s
def picture_frame(kind='landscape',c='#3A2E26',w=160,h=120):
    s=R(-w/2-12,-h-12,w+24,h+24,c,rx=3)+R(-w/2,-h,w,h,'#F3EEE2',stroke='none')
    if kind=='landscape':
        s+=rect(-w/2,-h,w,h,fill='#9FCBEB')+path(f'M{-w/2} {-h*.3} L{-w*.2} {-h*.7} L{w*.05} {-h*.4} L{w*.25} {-h*.6} L{w/2} {-h*.3} L{w/2} 0 L{-w/2} 0Z',fill='#5E8A5A')+circ(w*.25,-h*.75,10,fill='#FFE07A')
    elif kind=='family':
        for i,(x,hc) in enumerate(((-40,'#3A2A22'),(0,'#6A4A2A'),(38,'#2A1D14'))):
            s+=circ(x,-h*.55,15,fill='#ECE4D6',stroke='#8C8273',stroke_width=2)+path(f'M{x-15} {-h*.58} A15 15 0 0 1 {x+15} {-h*.58}Z',fill=hc)+R(x-14,-h*.38,28,h*.38,['#C8573E','#3E6A8A','#6B8A3E'][i],rx=10,stroke='none')
    elif kind=='diploma':
        s+=text('DIPLOMA',0,-h*.7,size=18,fill='#3A2E26',weight=800,anchor='middle',family='Georgia, serif')+''.join(rect(-w*.35,-h*.55+i*14,w*.7,3,fill='#B5AE9F') for i in range(3))+circ(w*.3,-h*.18,12,fill='#D6453A')
    elif kind=='heart':
        s+=path(f'M0 {-h*.2} C-50 {-h*.5} -30 {-h*.95} 0 {-h*.7} C30 {-h*.95} 50 {-h*.5} 0 {-h*.2}Z',fill='#D6453A')
    return s
def poster(textt='DREAM BIG',c='#2A2F4A'):
    w,h=170,240
    s=R(-w/2,-h,w,h,c,rx=2)+path(f'M{w/2-26} {-h} L{w/2} {-h} L{w/2} {-h+26}Z',fill=light(c,.2))
    words=textt.split()
    for i,wd in enumerate(words): s+=text(wd,0,-h+90+i*60,size=50,fill='#ECE4D6',weight=900,anchor='middle',family="'Bebas Neue', Oswald, Impact, sans-serif",opacity='.9')
    s+=rect(-50,-30,100,4,fill='#ECE4D6',opacity='.6')+circ(0,-h+10,4,fill='#C9C3B8')
    return s
def wall_shelf(items=True):
    s=R(-150,-16,300,16,WOOD_L,rx=3)+path('M-110 0 L-110 24 L-90 0 M110 0 L110 24 L90 0',fill='none',stroke='#3A3E47',stroke_width=4)
    if items: s+=g(book_stack(3),transform='translate(-50 -16) scale(.55)')+g(plant('cactus'),transform='translate(70 -16) scale(.38)')+g(R(-14,-60,28,60,'#D7B270',rx=3),transform='translate(10 -16)')
    return s
def mirror(): 
    s=ell(0,-170,90,150,**S('#C9A96E'))+ell(0,-170,74,134,fill='#B9CFE0',stroke='#8A7550',stroke_width=2)
    s+=path('M-40 -260 Q-60 -200 -50 -130',fill='none',stroke='#fff',stroke_width=10,stroke_linecap='round',opacity='.35')+path('M-20 -280 Q-34 -250 -32 -220',fill='none',stroke='#fff',stroke_width=6,stroke_linecap='round',opacity='.3')
    return s
def ceiling_lamp(on=True):
    s=line([0,-400],[0,-200],stroke='#3A3E47',stroke_width=3)
    if on: s+=path('M-60 -170 L-240 200 L240 200 L60 -170Z',fill='#FFE7B0',opacity='.12')
    s+=path('M-70 -170 Q-70 -230 0 -230 Q70 -230 70 -170Z',**S('#3E4B60'))+(ell(0,-170,40,10,fill='#FFF3CF') if on else '')
    return g(s,transform='translate(0 0)')
def light_switch(): return R(-22,-70,44,70,'#EDE8DC',rx=6)+R(-8,-52,16,30,'#D2CCBE',rx=3)
def wall_outlet(): return R(-22,-60,44,60,'#EDE8DC',rx=6)+R(-8,-46,4,10,'#5A5A5A')+R(4,-46,4,10,'#5A5A5A')+R(-8,-24,4,10,'#5A5A5A')+R(4,-24,4,10,'#5A5A5A')
# ======== OBJECTS ========
def money_stack(n=5):
    s=''
    for i in range(n):
        y=-i*12
        s+=R(-80,y-14,160,14,'#6BAA5A',rx=2)+rect(-80,y-11,160,8,fill='#85C474')+circ(0,y-7,4,fill='#4E8A40')
    s+=R(-82,-n*12-50,164,50,'#7BBE6A',rx=4)+ell(0,-n*12-25,22,18,fill='none',stroke='#4E8A40',stroke_width=3)+text('$',0,-n*12-15,size=26,fill='#4E8A40',weight=800,anchor='middle')+R(-10,-n*12-56,20,62,'#E9E2D4',stroke='none')
    return s
def banknote(): return R(-80,-40,160,80,'#7BBE6A',rx=4)+R(-70,-30,140,60,'none',rx=3,stroke='#4E8A40')+ell(0,0,20,22,fill='none',stroke='#4E8A40',stroke_width=3)+text('$',0,10,size=28,fill='#4E8A40',weight=800,anchor='middle')+text('100',-50,-12,size=14,fill='#4E8A40',weight=800,anchor='middle')
def coins():
    s=''
    for i in range(5): s+=ell(0,-i*10,40,12,**S('#E2B65A'))+rect(-40,-i*10,80,0.1)
    s+=circ(70,-36,36,**S('#E2B65A'))+circ(70,-36,26,fill='none',stroke=dark('#E2B65A',.3),stroke_width=2.4)+text('$',70,-26,size=30,fill=dark('#E2B65A',.35),weight=800,anchor='middle')
    return s
def wallet(empty=True):
    s=R(-90,-110,180,110,'#6B4A32',rx=12)+R(-90,-110,180,40,'#7E5A3E',rx=12)+R(50,-74,50,36,'#5A3E2A',rx=10)+circ(74,-56,6,fill='#D7B270')
    if empty: s+=g(path('M0 0 q-8 -20 6 -30 q14 -10 4 -26',fill='none',stroke='#C9C1B0',stroke_width=3,stroke_linecap='round'),transform='translate(-40 -116)')+path('M-30 -150 L-20 -140 M-10 -160 L-14 -146',stroke='#C9C1B0',stroke_width=2.4)
    else: s+=R(-70,-130,90,40,'#7BBE6A',rx=3,stroke='#4E8A40')
    return s
def credit_card(c='#3E4B8A'):
    return R(-100,-130,200,126,c,rx=12)+R(-80,-100,36,28,'#E2C26B',rx=5)+text('•••• •••• •••• 2847',-80,-40,size=15,fill='#fff',weight=600,family='monospace')+circ(60,-26,12,fill='#EB5A4E',opacity='.9')+circ(76,-26,12,fill='#F2B53A',opacity='.9')
def keys():
    s=circ(0,-60,22,fill='none',stroke='#B9BEC6',stroke_width=6)
    s+=g(R(-8,0,16,26,'#D7B270',rx=6)+R(-4,24,8,60,'#D7B270')+R(4,60,10,6,'#D7B270')+R(4,72,8,6,'#D7B270'),transform='translate(-10 -50) rotate(20)')
    s+=g(R(-8,0,16,26,'#B9BEC6',rx=6)+R(-4,24,8,54,'#B9BEC6')+R(4,58,10,6,'#B9BEC6'),transform='translate(10 -46) rotate(-25)')
    s+=R(14,-70,36,24,'#D6453A',rx=8)
    return s
def house_key_tag(): return keys()
def grad_cap():
    s=path('M-110 -60 L0 -100 L110 -60 L0 -20Z',**S('#1E2236'))+path('M-60 -48 L-60 -8 Q0 16 60 -8 L60 -48 L0 -26Z',**S('#1E2236'))
    s+=path('M0 -60 Q80 -50 84 0',fill='none',stroke='#E2C25A',stroke_width=4)+circ(84,4,6,fill='#E2C25A')+path('M78 6 L76 30 M84 8 L84 32 M90 6 L92 30',stroke='#E2C25A',stroke_width=3)
    return s
def diploma_roll(): return g(R(-90,-22,180,44,'#F3EEE2',rx=20)+ell(-90,0,10,22,**S('#E3DCCC'))+R(-10,-24,20,48,'#D6453A',stroke='none')+path('M0 24 L-10 50 M0 24 L10 50',stroke='#D6453A',stroke_width=6),transform='translate(0 -30) rotate(-12)')
def trophy():
    c='#E2B65A'
    s=R(-60,-30,120,30,WOOD_D,rx=4)+R(-14,-80,28,50,c)+path('M-60 -220 L60 -220 Q60 -110 0 -90 Q-60 -110 -60 -220Z',**S(c))
    s+=path('M-60 -200 Q-100 -200 -96 -160 Q-92 -130 -50 -130 M60 -200 Q100 -200 96 -160 Q92 -130 50 -130',fill='none',stroke=dark(c,.4),stroke_width=9)+path('M-60 -200 Q-100 -200 -96 -160 Q-92 -130 -50 -130 M60 -200 Q100 -200 96 -160 Q92 -130 50 -130',fill='none',stroke=c,stroke_width=5)
    s+=hi('M-34 -200 Q-36 -140 -10 -110',light(c,.5),'.6',6)+text('1',0,-150,size=46,fill=dark(c,.35),weight=900,anchor='middle')
    return s
def gift_box(c='#C8577A'):
    return R(-70,-110,140,110,c)+R(-80,-140,160,34,light(c,.1),rx=4)+R(-12,-140,24,140,'#F2C14E',stroke='none')+path('M0 -140 C-50 -190 -70 -140 0 -140 C70 -140 50 -190 0 -140Z',fill='none',stroke='#F2C14E',stroke_width=10)
def pizza_box(): return R(-110,-30,220,30,'#C9A16E',rx=3)+path('M-110 -30 L-90 -170 L130 -170 L110 -30Z',**S('#D7B47E'))+text('PIZZA',10,-90,size=34,fill='#B8463A',weight=900,anchor='middle')+circ(10,-130,16,fill='#B8463A',opacity='.8')
def water_bottle(): return R(-24,-180,48,170,'#8FC9F5',rx=14,fill_opacity='.6')+R(-16,-206,32,30,'#3E6A8A',rx=6)+rect(-24,-120,48,40,fill='#3E6A8A',opacity='.8')+hi('M-12 -160 L-12 -30','#fff','.6',4)
def soda_can(): return R(-26,-110,52,110,'#D6453A',rx=8)+ell(0,-108,24,6,fill='#C9CED6')+path('M-26 -40 Q0 -70 26 -40',fill='none',stroke='#fff',stroke_width=6)
def pills(): return R(-34,-110,68,110,'#F2A65A',rx=8,fill_opacity='.85')+R(-40,-140,80,34,'#F3EEE2',rx=6)+rect(-34,-80,68,40,fill='#F3EEE2')+text('Rx',0,-52,size=20,fill='#D6453A',weight=800,anchor='middle')
def lightbulb(on=True):
    c='#FFE07A' if on else '#D7DDE6'
    s=(circ(0,-140,110,fill='url(#bulbGlow)') if on else '')
    s+=path('M-60 -150 C-60 -230 60 -230 60 -150 C60 -110 30 -96 26 -60 L-26 -60 C-30 -96 -60 -110 -60 -150Z',**S(c,k=.45))
    s+=R(-28,-60,56,14,'#9AA3AF',rx=3)+R(-26,-46,52,14,'#8D939C',rx=3)+R(-16,-32,32,14,'#7D838C',rx=6)
    s+=path('M-14 -60 L-14 -110 L0 -124 L14 -110 L14 -60',fill='none',stroke=dark(c,.4),stroke_width=3)+hi('M-36 -170 Q-30 -200 -6 -206','#fff','.7',6)
    if on:
        for a in range(0,360,45):
            if a in (180,): continue
            v=dirv(a+180); s+=line(add([0,-150],mul(v,82)),add([0,-150],mul(v,106)),stroke='#FFD86B',stroke_width=6,stroke_linecap='round')
    return s
def heart_icon(c='#E8455A',broken=False):
    d='M0 0 C-90 -60 -70 -150 0 -110 C70 -150 90 -60 0 0Z'
    s=path(d,**S(c))+hi('M-50 -96 Q-46 -116 -26 -118','#fff','.6',6)
    if broken: s+=path('M0 -110 L-12 -80 L10 -60 L-8 -30 L0 0',fill='none',stroke='#1C2233',stroke_width=6,stroke_linejoin='round')
    return s
def battery(level=.1):
    c='#D6453A' if level<.25 else ('#F2B53A' if level<.55 else '#5FB55A')
    return R(-80,-60,160,60,'#2A2D35',rx=10)+R(80,-42,12,24,'#2A2D35',rx=3)+rect(-72,-52,144*level,44,rx=5,fill=c)
def sticky_note(t='TODO',c='#F2D45A'):
    return g(R(-60,-120,120,120,c,k=.3)+path('M30 0 L60 -30 L60 0Z',fill=dark(c,.15))+text(t,0,-70,size=24,fill='#3A3E47',weight=800,anchor='middle',family="'Caveat', 'Comic Sans MS', cursive")+''.join(rect(-40,-50+i*14,80-(i*14),3,fill='#3A3E47',opacity='.4') for i in range(3)),transform='rotate(-4)')
def clipboard():
    return R(-90,-240,180,240,'#8A6A4A',rx=10)+R(-74,-220,148,206,'#F7F3EA',stroke='none')+R(-40,-250,80,30,'#9AA3AF',rx=6)+''.join(R(-60,-190+i*40,18,18,'#fff',stroke='#8D939C')+(path(f'M-56 {-180+i*40} l5 6 l10 -12',fill='none',stroke='#3FA34D',stroke_width=3) if i<2 else '')+rect(-30,-184+i*40,90,5,fill='#B5AE9F') for i in range(4))
def car(c='#D6453A'):
    s=path('M-200 -50 L-190 -100 Q-180 -120 -150 -124 L-110 -126 L-60 -180 Q-50 -190 -30 -190 L80 -190 Q104 -190 118 -176 L160 -126 L190 -120 Q210 -114 212 -90 L214 -50Z',**S(c))
    s+=path('M-90 -128 L-48 -172 L20 -172 L20 -128Z',fill='#BFD8EC',stroke=dark(c,.5),stroke_width=2)+path('M34 -128 L34 -172 L82 -172 Q96 -172 104 -162 L132 -128Z',fill='#BFD8EC',stroke=dark(c,.5),stroke_width=2)
    for x in (-120,130): s+=circ(x,-40,40,**S('#22252D'))+circ(x,-40,18,fill='#9AA3AF')
    s+=R(180,-108,26,16,'#FFE7A8',rx=5)+R(-206,-100,16,16,'#F2A65A',rx=4)+hi('M-170 -112 L150 -112',light(c,.35),'.5',3)
    return s
def bicycle():
    s=''
    for x in (-90,90): s+=circ(x,-70,62,fill='none',stroke='#22252D',stroke_width=8)+circ(x,-70,6,fill='#5A606C')
    s+=path('M-90 -70 L-20 -70 L40 -150 L-40 -150 L-90 -70 M-20 -70 L-50 -170 M40 -150 L90 -70 M40 -150 L30 -186',fill='none',stroke='#3E6A8A',stroke_width=8,stroke_linejoin='round',stroke_linecap='round')
    s+=R(-74,-182,50,12,'#22252D',rx=6)+path('M14 -190 L48 -186',stroke='#22252D',stroke_width=8,stroke_linecap='round')
    return s
def tree(kind='round',c='#4E8A48'):
    s=R(-16,-200,32,200,'#6B4F3C',rx=6)
    if kind=='round':
        for (x,y,r_) in ((-60,-230,80),(60,-240,84),(0,-310,96),(-10,-210,80)): s+=circ(x,y,r_,**S(c,k=.4))
        s+=''.join(path(f'M{x} {y} q14 -10 28 0',fill='none',stroke=light(c,.25),stroke_width=4,opacity='.6',stroke_linecap='round') for x,y in ((-70,-280),(20,-340),(40,-250)))
    elif kind=='pine':
        for i in range(3): s+=path(f'M0 {-420+i*80} L{110+i*30} {-220+i*70} L{-110-i*30} {-220+i*70}Z',**S(dark(c,.08*i),k=.4))
    elif kind=='bare':
        s+=path('M0 -180 L-60 -280 M0 -200 L70 -300 M-40 -246 L-90 -260 M40 -260 L60 -340 M0 -200 L0 -330',fill='none',stroke='#6B4F3C',stroke_width=10,stroke_linecap='round')
    return s
def street_lamp(on=True):
    s=R(-10,-420,20,420,'#2F333B')+path('M0 -410 Q0 -450 60 -450 L90 -450',fill='none',stroke='#2F333B',stroke_width=12)+path('M66 -452 L114 -452 L104 -428 L76 -428Z',**S('#3A3E47'))
    if on: s+=path('M78 -428 L102 -428 L240 0 L-60 0Z',fill='#FFE3A0',opacity='.14')+ell(90,-428,22,8,fill='#FFF3CF')
    s+=R(-24,-20,48,20,'#2F333B',rx=4)
    return s
def bench(): return R(-160,-120,320,18,WOOD,rx=4)+R(-160,-180,320,16,WOOD,rx=4)+R(-160,-210,320,16,WOOD,rx=4)+''.join(R(x,-120,14,120,'#2F333B')+R(x,-210,10,90,'#2F333B') for x in (-140,126))
def cloud(c='#F3F6FA'):
    return ''.join(circ(x,y,r_,fill=c) for x,y,r_ in ((-70,-40,46),(0,-70,64),(70,-44,48),(30,-30,40),(-30,-26,40)))+rect(-116,-40,232,40,rx=20,fill=c)
def rain_cloud():
    s=cloud('#6E7A8E')
    s+=''.join(line([x,10],[x-10,40],stroke='#8FC9F5',stroke_width=4,stroke_linecap='round') for x in (-70,-30,10,50,90))
    return s
def sun(): return ''.join(line(add([0,0],mul(dirv(a),80)),add([0,0],mul(dirv(a),110)),stroke='#FFD86B',stroke_width=10,stroke_linecap='round') for a in range(0,360,30))+circ(0,0,64,fill='#FFD86B')+circ(0,0,50,fill='#FFE48F')
def moon(): return circ(0,0,70,fill='#EEF2FC')+circ(34,-20,60,fill='#1C2233')+circ(-26,10,8,fill='#D7DDEA')+circ(-34,-26,5,fill='#D7DDEA')
def stars():
    rr=rnd(4); s=''
    for i in range(14):
        x,y,k=rr.uniform(-200,200),rr.uniform(-120,120),rr.uniform(.3,1)
        s+=g(path('M0 -12 Q2 -2 12 0 Q2 2 0 12 Q-2 2 -12 0 Q-2 -2 0 -12Z',fill='#FFF3C4'),transform=f'translate({f(x)} {f(y)}) scale({f(k)})')
    return s
def mailbox(): return R(-8,-160,16,160,'#3A3E47')+path('M-60 -160 L-60 -220 Q-60 -260 0 -260 Q60 -260 60 -220 L60 -160Z',**S('#3E6A8A'))+R(56,-250,8,50,'#D6453A')+R(56,-250,30,18,'#D6453A')
def door_mat(): return R(-110,-16,220,16,'#8A6A4A',rx=4)+text('WELCOME',0,-3,size=12,fill='#5A3E2A',weight=800,anchor='middle',letter_spacing='3')
def box_cardboard(): return R(-90,-130,180,130,'#C9A16E')+path('M-90 -130 L-60 -160 L120 -160 L90 -130Z',**S('#D7B47E'))+path('M90 -130 L120 -160 L120 -30 L90 0Z',**S('#B08A58'))+R(-20,-130,40,40,'#E6CFA0',stroke='none')
def shopping_bag(): return path('M-70 -150 L70 -150 L80 0 L-80 0Z',**S('#E8C468'))+path('M-30 -150 Q-30 -200 0 -200 Q30 -200 30 -150',fill='none',stroke=dark('#E8C468',.45),stroke_width=6)
def umbrella(): return path('M-140 -260 Q0 -380 140 -260 Q110 -276 70 -260 Q35 -280 0 -260 Q-35 -280 -70 -260 Q-110 -276 -140 -260Z',**S('#3E6A8A'))+path('M0 -300 L0 -40 Q0 -10 -26 -14',fill='none',stroke='#3A3E47',stroke_width=7,stroke_linecap='round')
def coffee_cup_togo(): return path('M-40 -150 L40 -150 L30 0 L-30 0Z',**S('#F3EEE2'))+R(-46,-168,92,20,'#3A2E26',rx=6)+R(-38,-100,76,40,'#6B4F3C',stroke='none')
def headphones(): return path('M-80 -60 Q-80 -170 0 -170 Q80 -170 80 -60',fill='none',stroke='#2F333B',stroke_width=14)+R(-100,-90,40,70,'#3A3E47',rx=14)+R(60,-90,40,70,'#3A3E47',rx=14)
def game_controller(): return path('M-110 -30 C-130 -100 -90 -120 -60 -110 L60 -110 C90 -120 130 -100 110 -30 C100 0 70 0 54 -30 L-54 -30 C-70 0 -100 0 -110 -30Z',**S('#3A3E47'))+R(-74,-84,10,34,'#9AA3AF',rx=2)+R(-86,-72,34,10,'#9AA3AF',rx=2)+circ(60,-80,8,fill='#D6453A')+circ(80,-62,8,fill='#5FB55A')+circ(40,-62,8,fill='#3E6A8A')
def scale_weight(): return R(-110,-30,220,30,'#DDE3EA',rx=12)+R(-40,-26,80,20,'#2A2D35',rx=4)+text('88.4',0,-11,size=16,fill='#5FE07A',weight=700,anchor='middle',family='monospace')
