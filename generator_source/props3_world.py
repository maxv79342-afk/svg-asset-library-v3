from p3base import *
# ---------- food ----------
def apple(c='#E2493B'): return path('M0 -20 C-70 -10 -70 -120 -20 -118 Q0 -110 0 -110 Q0 -110 20 -118 C70 -120 70 -10 0 -20Z',**S(c))+ln('M0 -110 Q4 -130 10 -140','#5A3E2A',5)+path('M8 -128 Q30 -146 40 -126 Q22 -118 8 -128Z',**S('#5FB55A'))+hi('M-34 -96 Q-44 -70 -36 -50','#fff','.5',5)
def banana(): return path('M-90 -60 Q-40 10 60 -10 Q100 -24 106 -60 Q96 -40 60 -36 Q-20 -24 -80 -76Z',**S('#F2D45A'))+ln('M-84 -70 L-96 -80','#5A3E2A',6)+ln('M-60 -44 Q0 -14 70 -30',dark('#F2D45A',.25),2,'.6')
def orange(): return C(0,-56,56,'#F2853A')+''.join(circ(x,y,1.6,fill=dark('#F2853A',.25)) for x,y in ((-20,-70),(10,-40),(24,-76),(-10,-30),(30,-50)))+path('M0 -112 Q14 -130 30 -120 Q16 -108 0 -112Z',**S('#5FB55A'))+hi('M-34 -80 Q-40 -60 -32 -40','#fff','.5',5)
def watermelon(): return path('M-100 -20 A100 100 0 0 0 100 -20Z',**S('#3F9A4A'))+path('M-88 -20 A88 88 0 0 0 88 -20Z',fill='#F7F3EA')+path('M-80 -20 A80 80 0 0 0 80 -20Z',fill='#E8455A')+''.join(E(x,y,4,7,'#22252D',k=.2) for x,y in ((-40,-6),(0,10),(40,-6),(-20,30),(20,30)))
def strawberry(): return path('M0 0 C-50 -30 -40 -90 0 -86 C40 -90 50 -30 0 0Z',**S('#E2493B'))+path('M-24 -86 L-8 -96 L0 -110 L8 -96 L24 -86 L0 -80Z',**S('#5FB55A'))+''.join(circ(x,y,2,fill='#FFE07A') for x,y in ((-14,-60),(8,-56),(-4,-36),(14,-34),(-18,-30)))
def cake(): 
    s=R(-120,-140,240,140,'#F2C4D6',rx=10)+path('M-120 -140 Q-100 -110 -80 -140 Q-60 -110 -40 -140 Q-20 -110 0 -140 Q20 -110 40 -140 Q60 -110 80 -140 Q100 -110 120 -140 L120 -150 L-120 -150Z',**S('#F7F6F2',.3))
    s+=rect(-120,-70,240,14,fill='#B8463A',opacity='.6')+E(0,-2,140,12,'#E1E5EA',k=.3)
    for x in (-60,0,60): s+=R(x-6,-200,12,50,['#3E7AD6','#F2C230','#3FA34D'][x//60+1],rx=3)+path(f'M{x} -200 q-8 -14 0 -26 q8 12 0 26Z',fill='#FFB13B')
    return s
def cupcake(): return path('M-50 -70 L-40 0 L40 0 L50 -70Z',**S('#E8C468'))+''.join(ln(f'M{x} -66 L{x*.8} -4',dark('#E8C468',.25),2) for x in (-30,-10,10,30))+path('M-60 -70 Q-70 -110 -30 -116 Q-20 -150 10 -140 Q50 -150 50 -110 Q74 -100 60 -70Z',**S('#F2A6B8'))+C(0,-150,12,'#E2493B')
def ice_cream(): return path('M-40 -100 L0 0 L40 -100Z',**S('#D9A86A'))+ln('M-26 -70 L10 -96 M-14 -40 L24 -70 M20 -96 L-20 -50',dark('#D9A86A',.3),2)+C(0,-120,40,'#F2C4D6')+C(-6,-170,34,'#9C6A3E')+C(0,-210,8,'#E2493B')
def fries(): return ''.join(R(x,-160+abs(x)//2,16,100,'#F2C230',rx=3) for x in (-50,-30,-10,10,30))+path('M-60 -100 L60 -100 L44 0 L-44 0Z',**S('#E2493B'))+path('M-30 -60 Q0 -40 30 -60',fill='none',stroke='#F7F6F2',stroke_width=6)
def hotdog(): return E(0,-40,110,30,'#D9A86A')+E(0,-48,120,16,'#B8463A')+path('M-90 -52 Q-70 -64 -50 -52 Q-30 -64 -10 -52 Q10 -64 30 -52 Q50 -64 70 -52 Q90 -64 100 -52',fill='none',stroke='#F2C230',stroke_width=5)+path('M-110 -40 Q0 -10 110 -40',fill='none',stroke=dark('#D9A86A',.3),stroke_width=3)
def sandwich(): return path('M-100 -20 L100 -20 L0 -150Z',**S('#E8C890'))+path('M-90 -40 L90 -40 L80 -56 L-80 -56Z',fill='#5FB55A')+path('M-84 -56 L84 -56 L72 -70 L-72 -70Z',fill='#E2493B')+path('M-76 -70 L76 -70 L60 -84 L-60 -84Z',fill='#F2D45A')+path('M-100 -20 L100 -20 L94 -6 L-94 -6Z',**S('#D9A86A'))
def sushi(): 
    s=''
    for x in (-70,0,70): s+=E(x,-30,30,26,'#2A3A2A')+E(x,-34,24,20,'#F7F6F2',k=.3)+E(x,-36,12,10,'#F2853A' if x else '#E2493B')
    return s+R(-110,-6,220,8,'#7A5A43',rx=3)
def salad(): return path('M-100 -50 Q-90 0 0 0 Q90 0 100 -50Z',**S('#F3F1EC',.35))+''.join(C(x,y,r_,c) for x,y,r_,c in ((-60,-60,24,'#5FB55A'),(-20,-72,28,'#7FB34E'),(30,-66,26,'#5FB55A'),(66,-56,20,'#7FB34E'),(-10,-58,12,'#E2493B'),(40,-58,10,'#E2493B'),(10,-84,10,'#F2D45A')))
def bread(): return path('M-110 -20 Q-120 -100 -60 -110 Q0 -130 60 -110 Q120 -100 110 -20Z',**S('#C9884A'))+''.join(ln(f'M{x} -100 Q{x+20} -70 {x+10} -50',dark('#C9884A',.35),4) for x in (-60,-10,40))
def noodles(): return path('M-60 -140 L60 -140 L44 0 L-44 0Z',**S('#F7F6F2',.35))+path('M-60 -140 L-40 -180 L40 -180 L60 -140Z',**S('#E8E2D4',.35))+text('麺',0,-50,size=40,fill='#E2493B',weight=900,anchor='middle',family='sans-serif')*0+C(0,-70,22,'#E2493B')+ln('M30 -180 L70 -260 M42 -180 L86 -256','#C9A16E',5)
def kebab_plate():
    s=E(0,-16,150,26,'#F7F6F2',k=.3)+E(-40,-34,80,26,'#F7F3EA',k=.25)+''.join(C(-90+i*16,-46+(i%3)*4,6,'#F2D45A',opacity='.8') for i in range(10))
    s+=g(R(-90,-14,180,28,'#8A4A2A',rx=12)+''.join(ln(f'M{x} -12 L{x} 12',dark('#8A4A2A',.3),2) for x in range(-70,90,30)),transform='translate(50 -46) rotate(-6)')
    return s+C(110,-50,18,'#E2493B')+C(118,-36,12,'#E25A3B')+ln('M-130 -40 L140 -62','#C9CED6',3)
def fried_egg(): return path('M-80 -20 Q-90 -60 -40 -64 Q0 -90 40 -60 Q90 -60 80 -20 Q40 0 0 -6 Q-40 0 -80 -20Z',**S('#FBF8F2',.3))+C(4,-40,22,'#F2B530')+hi('M-6 -50 Q0 -56 8 -54','#fff','.7',4)
def latte(): return path('M-60 -110 L-50 0 L50 0 L60 -110Z',**S('#F7F6F2',.35))+E(0,-110,60,12,'#C9884A')+path('M-20 -110 Q0 -124 20 -110 Q0 -100 -20 -110Z',fill='#F7F3EA')+path('M60 -90 Q100 -80 60 -40',fill='none',stroke='#D2CCBE',stroke_width=10)+E(0,4,80,10,'#E1E5EA',k=.3)
def juice_box(): return R(-40,-140,80,140,'#F2853A',rx=6)+path('M-40 -140 L-20 -160 L60 -160 L40 -140Z',**S('#F2A65A'))+C(0,-80,22,'#F2C230')+ln('M20 -160 L30 -210','#F2A6B8',6)
def popcorn(): return path('M-60 -110 L-40 0 L40 0 L60 -110Z',**S('#F7F6F2',.35))+''.join(R(x,-110,14,110,'#E2493B',k=.4) for x in (-48,-14,20))+''.join(C(x,y,16,'#FFF3C4',.3) for x,y in ((-40,-120),(-10,-136),(24,-124),(44,-112),(0,-112),(-24,-146),(16,-150)))
def cookie(): return C(0,-60,60,'#C9884A')+''.join(E(x,y,8,6,'#3A2216') for x,y in ((-24,-80),(16,-90),(20,-50),(-14,-40),(-30,-60),(30,-70)))
def chocolate(): return R(-70,-130,140,130,'#5A3420',rx=6)+''.join(R(-60+i%3*42,-120+i//3*42,36,36,'#6E4630',rx=3,k=.4) for i in range(9))+path('M-70 -60 L70 -60 L70 0 L-70 0Z',**S('#C8573E'))+text('CHOCO',0,-24,size=22,fill='#F7F3EA',weight=900,anchor='middle')
def milk(): return path('M-50 0 L-50 -150 L0 -190 L50 -150 L50 0Z',**S('#F7F6F2',.35))+path('M-50 -150 L0 -190 L50 -150Z',fill='#3E7AD6')+R(-36,-110,72,50,'#3E7AD6',rx=6)+text('MILK',0,-78,size=20,fill='#fff',weight=900,anchor='middle')
def cereal(): return R(-70,-220,140,220,'#F2C230',rx=6)+text('CRUNCH',0,-180,size=22,fill='#B8463A',weight=900,anchor='middle')+E(0,-90,50,36,'#F7F6F2',k=.3)+''.join(C(x,y,8,c) for x,y,c in ((-20,-96,'#E2493B'),(10,-100,'#3FA34D'),(20,-84,'#F2853A'),(-6,-80,'#7C5CD6')))
# ---------- nature ----------
def bush(c='#4E8A48'): return ''.join(C(x,y,r_,c,.4) for x,y,r_ in ((-70,-50,50),(0,-80,64),(70,-50,50),(-30,-40,44),(36,-40,46)))+''.join(hi(f'M{x} {y} q12 -8 24 0',light(c,.3),'.6',4) for x,y in ((-80,-80),(-10,-120),(60,-80)))
def flowers_bed():
    s=R(-160,-40,320,40,'#6B4F3C',rx=10)
    for i,x in enumerate(range(-140,160,40)):
        c=['#E8455A','#F2C230','#F2A6B8','#B8A6F2'][i%4]; h=70+(i*17)%40
        s+=ln(f'M{x} -36 L{x} {-36-h}','#4E8A48',4)+''.join(C(x+math.cos(k*72*D)*9,-36-h+math.sin(k*72*D)*9,8,c,.45) for k in range(5))+C(x,-36-h,6,'#E9A23B')
    return s
def rock(): return path('M-90 0 Q-100 -50 -50 -70 Q0 -100 50 -70 Q100 -50 90 0Z',**S('#8A8F99'))+hi('M-50 -56 Q-20 -76 20 -70','#fff','.35',5)
def palm_tree():
    s=path('M-10 0 Q-30 -200 20 -400 L40 -396 Q4 -200 20 0Z',**S('#9C7656'))+''.join(ln(f'M-20 {y} L26 {y-8}',dark('#9C7656',.3),3) for y in range(-60,-380,-40))
    for a in (-160,-120,-60,-20,20,170):
        s+=g(path('M0 0 Q80 -40 170 10 Q80 -10 0 0Z',**S('#4E9A48',.4)),transform=f'translate(30 -400) rotate({a})')
    return s+C(20,-388,12,'#6B4F3C')+C(40,-384,12,'#6B4F3C')
def mushroom(): return R(-20,-70,40,70,'#F3F1EC',rx=10)+path('M-80 -60 Q-80 -150 0 -150 Q80 -150 80 -60Z',**S('#E2493B'))+''.join(C(x,y,r_,'#F7F6F2',.3) for x,y,r_ in ((-40,-100,12),(10,-126,10),(44,-90,9)))
def grass_tuft(): return ''.join(path(f'M{x} 0 Q{x+d} -40 {x+d*2} -{h} Q{x+d*.6} -40 {x+10} 0Z',**S('#5FB55A',.4)) for x,d,h in ((-40,-10,80),(-20,6,100),(0,-6,90),(20,10,70),(-60,8,60)))
def sunflower(): return ln('M0 0 L0 -300','#4E8A48',10)+path('M0 -140 Q60 -170 80 -130 Q40 -120 0 -140Z',**S('#5FB55A'))+''.join(g(E(0,-48,14,30,'#F2C230',.4),transform=f'translate(0 -330) rotate({a})') for a in range(0,360,30))+C(0,-330,34,'#6B4F3C')
def log(): return R(-140,-60,280,60,'#8A5A3C',rx=30)+E(140,-30,22,30,'#C9A16E')+circ(140,-30,12,fill='none',stroke='#8A5A3C',stroke_width=3)
def campfire(lit=True):
    s=ln('M-80 -10 L80 -40 M-80 -40 L80 -10','#6B4F3C',22)+''.join(C(x,-6,16,'#8A8F99') for x in (-110,-70,70,110))
    if lit: s=E(0,-80,180,140,'#FFB13B',opacity='.18')+s+path('M-50 -30 Q-60 -110 -10 -170 Q-10 -110 20 -100 Q20 -150 50 -180 Q80 -100 50 -30Z',**S('#F2853A',.3))+path('M-24 -30 Q-30 -90 0 -120 Q10 -80 30 -70 Q40 -50 24 -30Z',fill='#FFE07A')
    return s
def tent(c='#E2725B'): return path('M-200 0 L0 -260 L200 0Z',**S(c))+path('M0 -260 L-50 0 L50 0Z',fill=dark(c,.3))+ln('M0 -260 L0 -300','#5A3E2A',6)+path('M0 -300 L30 -290 L0 -280Z',fill='#F2C230')
def flower_vase(): return path('M-40 0 Q-70 -70 -30 -120 L30 -120 Q70 -70 40 0Z',**S('#3E7AD6'))+''.join(ln(f'M{x*.3} -120 L{x} -230','#4E8A48',4)+C(x,-236,16,c,.45) for x,c in ((-50,'#E8455A'),(0,'#F2C230'),(50,'#F2A6B8')))
def mountain(): return path('M-300 0 L-80 -360 L20 -220 L100 -300 L300 0Z',**S('#6E7A9A'))+path('M-80 -360 L-130 -280 L-100 -290 L-70 -270 L-40 -300Z',fill='#F7F6F2')+path('M100 -300 L70 -250 L95 -258 L120 -240 L140 -260Z',fill='#F7F6F2')
# ---------- city ----------
def traffic_light(state='red'):
    s=R(-10,-300,20,300,'#3A3E47')+R(-40,-460,80,180,'#22252D',rx=12)
    for i,c in enumerate(('#E2493B','#F2C230','#3FA34D')):
        on=['red','yellow','green'][i]==state
        if on: s+=C(0,-430+i*58,38,c,.2,opacity='.3')
        s+=C(0,-430+i*58,22,c if on else dark(c,.6),.3)
    return s
def stop_sign(): 
    pts=[[math.cos((22.5+i*45)*D)*70,-260+math.sin((22.5+i*45)*D)*70] for i in range(8)]
    return R(-8,-200,16,200,'#9AA3AF')+path('M'+'L'.join(P(p) for p in pts)+'Z',**S('#D6453A'))+text('STOP',0,-250,size=34,fill='#fff',weight=900,anchor='middle')
def fire_hydrant(): return R(-46,-20,92,20,'#B8362E',rx=4)+path('M-36 -20 L-36 -120 Q-36 -150 0 -150 Q36 -150 36 -120 L36 -20Z',**S('#D6453A'))+R(-56,-110,112,26,'#D6453A',rx=10)+C(0,-98,10,'#9AA3AF')+R(-10,-170,20,24,'#D6453A',rx=4)
def bus_stop():
    s=R(-220,-340,440,20,'#3A3E47',rx=6)+R(-210,-320,10,320,'#5A606C')+R(200,-320,10,320,'#5A606C')+R(-190,-300,250,240,GLASS,rx=4,k=.5,opacity='.5')
    s+=R(90,-300,100,170,'#F7F6F2',rx=4,k=.3)+text('BUS',140,-260,size=24,fill='#3E6A9A',weight=900,anchor='middle')+''.join(ln(f'M106 {y} L176 {y}','#9AA3AF',3) for y in (-230,-210,-190))
    return s+R(-170,-110,220,20,WOOD_L,rx=5)+R(-160,-90,10,90,'#3A3E47')+R(30,-90,10,90,'#3A3E47')
def parking_meter(): return R(-6,-180,12,180,'#5A606C')+R(-36,-280,72,110,'#9AA3AF',rx=20)+R(-22,-260,44,36,'#2A3A2A',rx=4)+text('P',0,-196,size=24,fill='#3E7AD6',weight=900,anchor='middle')
def street_bin(): return path('M-50 0 L-60 -160 L60 -160 L50 0Z',**S('#3E6A4A'))+R(-66,-176,132,22,'#2F5A3A',rx=6)+''.join(ln(f'M{x} -150 L{x*.85} -10',dark('#3E6A4A',.3),3) for x in (-30,0,30))
def phone_booth(): return R(-90,-460,180,460,'#D6453A',rx=8)+R(-70,-400,140,340,GLASS,rx=4,k=.5)+''.join(ln(f'M-70 {y} L70 {y}','#D6453A',6) for y in (-330,-260,-190,-120))+ln('M0 -400 L0 -60','#D6453A',6)+R(-60,-446,120,30,'#22252D',rx=4)+text('PHONE',0,-424,size=20,fill='#fff',weight=900,anchor='middle')
def traffic_cone(): return R(-50,-14,100,14,'#E2593B',rx=3)+path('M-36 -14 L-10 -150 L10 -150 L36 -14Z',**S('#F2853A'))+path('M-28 -54 L28 -54 L22 -84 L-22 -84Z',fill='#F7F6F2')
def barrier(): return R(-160,-120,320,40,'#F7F6F2',rx=4)+''.join(path(f'M{x} -120 L{x+40} -120 L{x+20} -80 L{x-20} -80Z',fill='#E2493B') for x in range(-140,160,60))+R(-140,-80,16,80,'#5A606C')+R(124,-80,16,80,'#5A606C')
def billboard(txt='BIG SALE'): return R(-10,-300,20,300,'#5A606C')+R(-260,-560,520,260,'#F2C230',rx=6)+text(txt,0,-410,size=72,fill='#22252D',weight=900,anchor='middle')+text('50% OFF',0,-344,size=40,fill='#D6453A',weight=900,anchor='middle')
def atm(): return R(-90,-320,180,320,'#3A4258',rx=10)+R(-70,-290,140,90,'#5A8ACF',rx=4)+text('ATM',0,-236,size=30,fill='#fff',weight=900,anchor='middle')+''.join(R(-50+i%3*36,-180+i//3*28,26,20,'#C9CED6',rx=3) for i in range(9))+R(-60,-80,120,10,'#22252D',rx=3)
def vending_machine(): 
    s=R(-120,-460,240,460,'#D6453A',rx=12)+R(-100,-430,150,330,'#1A2433',rx=6)
    for r_ in range(4):
        for c in range(3): s+=R(-90+c*48,-420+r_*80,36,56,['#3E7AD6','#F2C230','#3FA34D','#F2853A'][(r_+c)%4],rx=6,k=.5)
    return s+R(64,-420,40,120,'#22252D',rx=4)+R(-90,-80,140,40,'#22252D',rx=4)
def manhole(): return E(0,-6,110,20,'#3A3E47')+''.join(ln(f'M{x} -16 L{x+20} 4','#22252D',3) for x in range(-80,80,20))
def crosswalk(): return ''.join(R(-200+i*80,-30,50,30,'#F7F6F2',k=.2) for i in range(6))
def bench_park(): return R(-160,-120,320,18,WOOD,rx=4)+R(-160,-200,320,16,WOOD,rx=4)+R(-160,-160,320,16,WOOD,rx=4)+''.join(R(x,-120,14,120,'#2F333B')+R(x,-200,10,90,'#2F333B') for x in (-140,126))
def fountain(): return E(0,-20,200,30,'#9AA3AF')+R(-200,-60,400,40,'#C9CED6',rx=10)+E(0,-60,180,14,'#9FD3E8')+R(-20,-200,40,140,'#C9CED6',rx=8)+E(0,-200,70,14,'#C9CED6')+path('M0 -210 Q-60 -300 -110 -70 M0 -210 Q60 -300 110 -70 M0 -210 L0 -320',fill='none',stroke='#9FD3E8',stroke_width=6,stroke_linecap='round',opacity='.8')
# ---------- animals ----------
def cat_sit(c='#F2A65A',eyes='#3FA34D'):
    s=path('M-50 0 Q-70 -90 -30 -120 L30 -120 Q70 -90 50 0Z',**S(c))+path('M40 -10 Q110 0 100 -70',fill='none',stroke=dark(c,.5),stroke_width=16,stroke_linecap='round')+path('M40 -10 Q110 0 100 -70',fill='none',stroke=c,stroke_width=11,stroke_linecap='round')
    s+=C(0,-150,46,c)+path('M-40 -170 L-34 -214 L-8 -188Z M40 -170 L34 -214 L8 -188Z',**S(c))+path('M-32 -180 L-30 -204 L-16 -188Z M32 -180 L30 -204 L16 -188Z',fill='#F2A6B8')
    s+=E(-16,-154,7,9,eyes,k=.6)+E(16,-154,7,9,eyes,k=.6)+E(-16,-154,2.4,7,'#15161A',k=.1)+E(16,-154,2.4,7,'#15161A',k=.1)+path('M-5 -138 L5 -138 L0 -132Z',fill='#E88AA8')+ln('M0 -132 Q-6 -124 -12 -128 M0 -132 Q6 -124 12 -128','#5A3E2A',1.8)
    s+=ln('M-20 -134 L-50 -140 M-20 -130 L-48 -126 M20 -134 L50 -140 M20 -130 L48 -126','#5A3E2A',1.4,'.7')+''.join(ln(f'M{x} -110 Q{x+6} -90 {x} -70',dark(c,.3),4,'.5') for x in (-20,0,20))
    return s+E(-22,-4,16,8,light(c,.2))+E(22,-4,16,8,light(c,.2))
def cat_sleep(c='#5A606C'):
    s=E(0,-40,100,40,c)+C(70,-52,34,c)+path('M50 -78 L56 -108 L76 -84Z M80 -80 L94 -104 L100 -74Z',**S(c))
    s+=ln('M58 -54 Q66 -48 74 -54 M82 -54 Q88 -48 94 -54','#15161A',2.4)+path('M-90 -30 Q-140 -10 -100 20 Q-60 30 20 10',fill='none',stroke=dark(c,.5),stroke_width=16,stroke_linecap='round')+path('M-90 -30 Q-140 -10 -100 20 Q-60 30 20 10',fill='none',stroke=c,stroke_width=11,stroke_linecap='round')
    return s+text('z',110,-110,size=30,fill='#BFD4FF',weight=900)+text('z',130,-140,size=22,fill='#BFD4FF',weight=900)
def dog_sit(c='#C9884A'):
    s=path('M-50 0 Q-70 -100 -20 -130 L30 -130 Q70 -90 50 0Z',**S(c))+path('M-40 -10 Q-100 -20 -90 -60',fill='none',stroke=dark(c,.5),stroke_width=14,stroke_linecap='round')+path('M-40 -10 Q-100 -20 -90 -60',fill='none',stroke=c,stroke_width=9,stroke_linecap='round')
    s+=C(10,-170,48,c)+E(40,-150,30,22,light(c,.35))+E(60,-160,10,8,'#22252D')
    s+=path('M-30 -200 Q-60 -200 -56 -140 Q-40 -150 -26 -170Z',**S(dark(c,.3)))
    s+=C(10,-184,6,'#22252D')+C(12,-186,2,'#fff')+path('M40 -136 Q50 -122 64 -136',fill='#E88AA8',stroke='#9C4A5A',stroke_width=1.6)
    return s+R(-30,-136,70,12,'#D6453A',rx=5)+C(10,-122,7,'#F2C230')+E(-24,-4,18,9,light(c,.2))+E(28,-4,18,9,light(c,.2))
def dog_stand(c='#F3F1EC',spot='#3A3E47'):
    s=R(-110,-150,200,70,c,rx=34)+''.join(R(x,-100,22,100,c,rx=10) for x in (-100,-60,40,70))
    s+=E(-30,-130,30,20,spot,k=.3)+path('M-110 -130 Q-160 -170 -150 -200',fill='none',stroke=dark(c,.4),stroke_width=14,stroke_linecap='round')+path('M-110 -130 Q-160 -170 -150 -200',fill='none',stroke=c,stroke_width=9,stroke_linecap='round')
    s+=C(110,-190,46,c)+E(146,-170,28,20,light(c,.2),k=.35)+E(168,-178,9,7,'#22252D')+path('M80 -224 Q60 -230 60 -170 Q76 -180 90 -200Z',**S(spot))+C(110,-202,6,'#22252D')
    return s
def bird(c='#3E7AD6'): return E(0,-40,46,32,c)+C(36,-70,24,c)+path('M56 -72 L80 -66 L56 -60Z',**S('#F2C230'))+C(42,-76,4,'#15161A')+path('M-10 -50 Q-40 -90 -70 -60 Q-40 -40 -10 -40Z',**S(dark(c,.15)))+path('M-40 -30 L-80 -20 L-44 -18Z',**S(c))+ln('M-6 -8 L-6 4 M10 -8 L10 4','#F2853A',3)
def pigeon(): return bird('#8A93A3')+E(24,-58,12,8,'#7FB3A6',opacity='.7')
def parrot(): return path('M-20 -10 Q-40 -100 10 -130 Q50 -110 30 -10Z',**S('#3FA34D'))+C(16,-140,30,'#E2493B')+path('M40 -146 Q66 -140 50 -116 Q40 -126 40 -146Z',**S('#F7F3EA'))+C(22,-148,5,'#15161A')+path('M-10 -20 L-30 60 L0 0Z',**S('#3E7AD6'))+path('M0 -20 L-6 70 L14 0Z',**S('#F2C230'))
def fish_bowl(): return C(0,-110,100,GLASS,.5,opacity='.55')+path('M-96 -90 Q0 -70 96 -90 L80 -40 Q0 0 -80 -40Z',fill='#5A9ED6',opacity='.7')+E(-10,-60,26,16,'#F2853A')+path('M-36 -60 L-54 -74 L-54 -46Z',**S('#F2853A'))+C(0,-64,3,'#15161A')+R(-60,-10,120,12,'#5A606C',rx=4)+''.join(C(x,y,5,'#fff',.2,opacity='.7') for x,y in ((20,-110),(30,-140),(14,-170)))
def rabbit(c='#F3F1EC'): return E(0,-50,60,46,c,.35)+C(40,-110,34,c,.35)+E(26,-176,10,40,c,.35)+E(52,-174,10,40,c,.35)+E(26,-176,5,30,'#F2A6B8')+E(52,-174,5,30,'#F2A6B8')+C(52,-114,5,'#15161A')+C(72,-104,4,'#E88AA8')+C(-58,-60,14,'#FFFFFF',.2)
def hamster(): return E(0,-50,70,50,'#E8B07A')+C(44,-70,8,'#15161A')+C(68,-60,5,'#E88AA8')+E(-10,-40,40,26,'#F7F3EA',k=.25)+C(20,-96,14,'#E8B07A')+C(-20,-94,14,'#E8B07A')
def turtle(): return path('M-80 -20 Q-80 -110 0 -110 Q80 -110 80 -20Z',**S('#5A8A4A'))+''.join(path(f'M{x} -100 L{x+30} -100 L{x+40} -60 L{x+15} -40 L{x-10} -60Z',fill='none',stroke=dark('#5A8A4A',.4),stroke_width=3) for x in (-50,0))+C(100,-40,24,'#9FC47A')+C(110,-46,4,'#15161A')+''.join(E(x,-10,16,12,'#9FC47A') for x in (-60,60))
def butterfly_big(): return path('M0 -60 Q-80 -160 -110 -80 Q-110 -30 0 -40Z M0 -60 Q80 -160 110 -80 Q110 -30 0 -40Z',**S('#7C5CD6'))+path('M0 -40 Q-70 -10 -70 30 Q-30 40 0 -30Z M0 -40 Q70 -10 70 30 Q30 40 0 -30Z',**S('#F2A6B8'))+R(-6,-80,12,80,'#22252D',rx=6)+ln('M0 -80 L-16 -110 M0 -80 L16 -110','#22252D',3)
GROUPS=dict(
 food2=dict(apple=apple(),apple_green=apple('#7FB34E'),banana=banana(),orange=orange(),watermelon_slice=watermelon(),strawberry=strawberry(),birthday_cake=cake(),cupcake=cupcake(),ice_cream_cone=ice_cream(),fries=fries(),hotdog=hotdog(),sandwich=sandwich(),sushi_plate=sushi(),salad_bowl=salad(),bread_loaf=bread(),noodle_box=noodles(),kebab_plate=kebab_plate(),fried_egg=fried_egg(),latte=latte(),juice_box=juice_box(),popcorn=popcorn(),cookie=cookie(),chocolate_bar=chocolate(),milk_carton=milk(),cereal_box=cereal()),
 nature=dict(bush=bush(),bush_dark=bush('#3E6A3A'),flower_bed=flowers_bed(),rock=rock(),palm_tree=palm_tree(),mushroom=mushroom(),grass_tuft=grass_tuft(),sunflower=sunflower(),log=log(),campfire_lit=campfire(),campfire_out=campfire(False),tent=tent(),tent_blue=tent('#3E7AD6'),flower_vase=flower_vase(),mountain=mountain()),
 city=dict(traffic_light_red=traffic_light('red'),traffic_light_yellow=traffic_light('yellow'),traffic_light_green=traffic_light('green'),stop_sign=stop_sign(),fire_hydrant=fire_hydrant(),bus_stop=bus_stop(),parking_meter=parking_meter(),street_bin=street_bin(),phone_booth=phone_booth(),traffic_cone=traffic_cone(),road_barrier=barrier(),billboard=billboard(),atm=atm(),vending_machine=vending_machine(),manhole=manhole(),crosswalk=crosswalk(),park_bench=bench_park(),fountain=fountain()),
 animals=dict(cat_sit=cat_sit(),cat_sit_black=cat_sit('#2F333B','#F2C230'),cat_sit_white=cat_sit('#F3F1EC','#3E7AD6'),cat_sleep=cat_sleep(),cat_sleep_orange=cat_sleep('#F2A65A'),dog_sit=dog_sit(),dog_sit_black=dog_sit('#3A3E47'),dog_stand=dog_stand(),dog_stand_brown=dog_stand('#C9884A','#7A4A2A'),bird_blue=bird(),bird_red=bird('#E2493B'),pigeon=pigeon(),parrot=parrot(),fish_bowl=fish_bowl(),rabbit=rabbit(),hamster=hamster(),turtle=turtle(),butterfly=butterfly_big()))
def items():
    o={}
    for k,v in GROUPS.items(): o.update(v)
    return o
