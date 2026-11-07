from p3base import *
# origin = bottom centre on the floor/counter
# ---------- kitchen ----------
def microwave(on=False):
    s=R(-110,-130,220,130,'#E6E9EE',rx=10)+R(-96,-116,140,100,'#2A2D35' if not on else '#F2C27A',rx=6)
    if on: s+=E(-26,-66,50,34,'#FFE7A8',opacity='.6')+E(-26,-40,24,8,'#F7F3EA')
    s+=R(56,-116,40,100,'#D2D7DE',rx=4,k=.4)+''.join(C(76,y,5,'#9AA3AF') for y in (-96,-76))+R(64,-56,24,8,'#3FA34D' if on else '#22252D',rx=2)+hi('M-86 -106 L-60 -106','#fff','.5',3)
    return s
def toaster(up=False):
    s=R(-70,-90,140,90,'#C9CED6',rx=24)+hi('M-52 -74 Q0 -86 52 -74','#fff','.6',4)
    s+=R(-40,-96,28,10,'#3A3E47',rx=3)+R(12,-96,28,10,'#3A3E47',rx=3)+R(64,-60,18,12,'#22252D',rx=3)
    if up: s=R(-38,-130,24,44,'#D9A86A',rx=6)+R(14,-126,24,40,'#D9A86A',rx=6)+s
    return s
def kettle(c='#D6453A'):
    return path('M-60 0 L-70 -90 Q-60 -120 0 -122 Q60 -120 70 -90 L60 0Z',**S(c))+path('M66 -80 Q110 -100 104 -126',fill='none',stroke=dark(c,.5),stroke_width=10,stroke_linecap='round')+path('M-50 -126 Q0 -170 50 -126',fill='none',stroke='#22252D',stroke_width=10,stroke_linecap='round')+R(-70,-10,140,10,'#22252D',rx=4)+hi('M-44 -96 L-48 -30','#fff','.5',5)
def coffee_machine():
    s=R(-80,-220,160,220,'#2F333B',rx=12)+R(-60,-200,120,50,'#3A3E47',rx=6)+R(-40,-190,50,22,'#7FE0A8',rx=3)+C(30,-178,10,'#C9CED6')
    s+=R(-50,-140,100,20,'#22252D',rx=4)+R(-34,-120,68,6,'#5A606C')+R(-26,-60,52,54,'#F3F1EC',rx=6)+ln('M-12 -114 L-12 -66 M12 -114 L12 -66','#6B3E26',4)+R(-70,-10,140,10,'#5A606C',rx=3)
    return s
def blender(c='#3FA3A0'):
    return R(-50,-60,100,60,c,rx=10)+C(0,-30,10,'#F3F1EC')+path('M-46 -60 L-56 -210 L56 -210 L46 -60Z',fill=GLASS,fill_opacity='.7',stroke='#5A6676',stroke_width=2.4)+path('M-44 -120 L44 -120 L46 -64 L-46 -64Z',fill='#F2A65A',opacity='.85')+R(-60,-224,120,16,'#22252D',rx=5)
def oven_range():
    s=R(-160,-300,320,300,'#E6E9EE',rx=8)+R(-170,-310,340,20,'#3A3E47',rx=5)
    for x in (-90,90):
        s+=E(x,-310,50,6,'#22252D')
    s+=R(-140,-240,280,30,'#D2D7DE',rx=4)+''.join(C(x,-225,9,'#3A3E47') for x in (-100,-50,50,100))
    s+=R(-140,-200,280,170,'#2A2D35',rx=8)+R(-120,-180,240,110,'#3A3E47',rx=6)+R(-100,-196,200,8,'#C9CED6',rx=4)+hi('M-110 -170 L-60 -170','#fff','.4',3)
    return s
def washing_machine(on=False):
    s=R(-130,-300,260,300,'#F3F4F6',rx=12)+R(-120,-290,240,44,'#E1E5EA',rx=6,k=.3)+C(80,-268,12,'#C9CED6')+R(-100,-278,90,22,'#22252D',rx=3)
    s+=C(0,-130,96,'#C9CED6',.45)+C(0,-130,76,'#2A3A5A')
    if on: s+=path('M-60 -110 Q-30 -150 0 -110 Q30 -70 60 -110 L60 -70 Q0 -40 -60 -70Z',fill='#9FD3E8',opacity='.8')+''.join(C(x,y,8,'#F2A6B8' if i%2 else '#FFE07A') for i,(x,y) in enumerate(((-30,-160),(20,-170),(10,-120),(-20,-100))))
    return s+hi('M-50 -190 Q-20 -210 20 -200','#fff','.6',6)
def fridge_double():
    s=R(-130,-460,260,460,'#E6E9EE',rx=14)+ln('M0 -456 L0 -6','#9AA3AF',3)+R(-30,-330,10,90,'#9AA3AF',rx=4)+R(20,-330,10,90,'#9AA3AF',rx=4)
    s+=R(-110,-420,50,40,'#F2D45A',rx=2,k=.4)+R(-96,-370,36,30,'#9FD3E8',rx=2,k=.4)+R(-110,-160,90,50,'#F7F3EA',rx=3,k=.3)
    s+=R(-120,-380,40,40,'#22252D',rx=5)+R(-114,-374,28,14,'#5A8ACF',rx=2)
    return s+hi('M-110 -440 L-110 -300','#fff','.5',5)
def kitchen_sink():
    s=R(-200,-200,400,200,'#5A8A9A',rx=6)+R(-210,-216,420,22,'#E8DCC6',rx=4,k=.35)
    s+=R(-120,-214,180,10,'#9AA3AF',rx=4)+path('M-20 -214 L-20 -280 Q-20 -296 0 -296 L40 -296',fill='none',stroke='#9AA3AF',stroke_width=12,stroke_linecap='round')+R(-36,-236,32,20,'#9AA3AF',rx=4)
    s+=''.join(R(x,-180,180,160,dark('#5A8A9A',.1),rx=4) for x in (-190,10))+''.join(R(x,-110,30,8,'#C9CED6',rx=3) for x in (-114,86))
    return s
def frying_pan(): return E(0,-14,90,18,'#2F333B')+E(0,-18,74,12,'#3A3E47')+R(84,-24,110,14,'#22252D',rx=6)+E(-10,-20,26,9,'#FBF8F2',k=.3)+E(-6,-20,9,6,'#F2B530',k=.4)
def plate_stack(n=5):
    return ''.join(E(0,-10-i*10,90,10,'#F7F6F2',k=.35) for i in range(n))+E(0,-10-(n-1)*10,70,6,'#E1E5EA',k=.3)
def cutting_board():
    s=R(-120,-30,240,30,'#B8854E',rx=10)+C(96,-15,6,'#7A5A43')
    s+=path('M-90 -30 L40 -44 L44 -36 L-88 -30Z',fill='#C9CED6',stroke=METAL_D,stroke_width=2)+R(40,-48,60,14,'#22252D',rx=5)
    s+=E(-50,-40,22,10,'#E2493B')+E(-20,-38,12,8,'#5FB55A')
    return s
def fruit_bowl():
    s=C(-40,-70,28,'#E2493B')+C(10,-80,30,'#F2A65A')+path('M30 -60 Q70 -120 100 -100 Q70 -90 50 -50Z',**S('#F2D45A'))+C(-4,-110,20,'#7FB34E')+ln('M-4 -130 l4 -12','#5A3E2A',3)
    return s+path('M-110 -60 Q-100 0 0 0 Q100 0 110 -60Z',**S('#3E6A8A'))+hi('M-90 -46 Q-60 -20 -20 -16','#fff','.4',4)
def samovar():
    s=R(-60,-20,120,20,'#C9A23B',rx=5)+path('M-30 -20 L-50 -60 L50 -60 L30 -20Z',**S('#D9B44A'))
    s+=path('M-70 -60 Q-90 -160 -60 -230 L60 -230 Q90 -160 70 -60Z',**S('#E3B24A',.45))+hi('M-50 -80 Q-66 -150 -46 -210','#fff','.55',6)
    for y in (-110,-170): s+=ln(f'M-74 {y} Q0 {y+10} 74 {y}','#B8862E',3)
    s+=R(70,-120,40,10,'#B8862E',rx=4)+R(100,-128,14,26,'#B8862E',rx=4)+ln('M-70 -200 Q-110 -200 -100 -150 M70 -200 Q110 -200 100 -150','#B8862E',6)
    s+=R(-36,-250,72,22,'#C9A23B',rx=6)+path('M-40 -250 Q-46 -300 0 -300 Q46 -300 40 -250Z',**S('#3E6A9A'))+''.join(C(x,-276,5,'#F3F1EC') for x in (-18,0,18))+R(-8,-318,16,20,'#C9A23B',rx=4)
    return s
def tea_glass():
    s=E(0,-6,52,10,'#E3B24A')+path('M-28 -12 L-34 -90 Q-34 -100 -24 -104 L24 -104 Q34 -100 34 -90 L28 -12Z',fill='#F7D9C4',fill_opacity='.35',stroke='#B8AE9C',stroke_width=2.4)
    s+=path('M-30 -60 L30 -60 L28 -14 L-28 -14Z',fill='#B8463A',opacity='.85')+ln('M-30 -56 Q0 -50 30 -56','#E58A5A',2,'.8')+hi('M-20 -92 L-22 -24','#fff','.6',4)
    return s+path('M-8 -120 q6 -10 0 -20 M10 -124 q6 -10 0 -20',fill='none',stroke='#ECE4D6',stroke_width=3,stroke_linecap='round',opacity='.6')
def teapot(c='#F3F1EC'):
    return E(0,-70,80,66,c,.4)+path('M76 -86 Q120 -100 126 -140',fill='none',stroke=dark(c,.4),stroke_width=12,stroke_linecap='round')+path('M-76 -110 Q-130 -100 -110 -40',fill='none',stroke=dark(c,.4),stroke_width=10)+E(0,-132,40,10,c,.4)+C(0,-146,10,'#3E6A9A')+ln('M-60 -80 Q0 -60 60 -80','#3E6A9A',8)+R(-60,-8,120,8,dark(c,.2),rx=3)
def wine_glass(): return path('M-30 -200 Q-34 -130 0 -116 Q34 -130 30 -200Z',fill=GLASS,fill_opacity='.5',stroke='#9AA3AF',stroke_width=2.4)+path('M-30 -160 Q-30 -124 0 -118 Q30 -124 30 -160Z',fill='#9C2A3A',opacity='.85')+ln('M0 -116 L0 -10','#9AA3AF',4)+E(0,-6,34,7,'#C9CED6')
def glass_water(): return path('M-30 -120 L-24 0 L24 0 L30 -120Z',fill=GLASS,fill_opacity='.55',stroke='#9AA3AF',stroke_width=2.4)+path('M-28 -84 L-25 -4 L25 -4 L28 -84Z',fill='#9FD3E8',opacity='.7')+hi('M-18 -110 L-14 -12','#fff','.7',4)
# ---------- bathroom ----------
def toilet():
    s=R(-40,-300,100,120,'#F7F6F2',rx=10,k=.35)+R(-30,-312,90,16,'#E1E5EA',rx=5,k=.35)+R(40,-290,16,8,'#C9CED6',rx=3)
    s+=path('M-60 -180 L130 -180 Q140 -110 60 -90 L50 0 L-10 0 L-20 -110 Q-60 -120 -60 -180Z',**S('#F7F6F2',.35))+R(-66,-196,200,18,'#EEF0F2',rx=8,k=.35)
    return s+hi('M-40 -160 Q20 -130 100 -160','#fff','.7',4)
def bathtub(bubbles=False):
    s=path('M-300 -200 L300 -200 L290 -60 Q280 -20 240 -20 L-240 -20 Q-280 -20 -290 -60Z',**S('#F7F6F2',.35))+R(-310,-216,620,22,'#EEF0F2',rx=10,k=.35)
    for x in (-240,220): s+=path(f'M{x} -24 l-10 24 l30 0 l-6 -24Z',**S('#C9A23B'))
    s+=path('M250 -216 L250 -290 Q250 -310 230 -310 L200 -310',fill='none',stroke='#9AA3AF',stroke_width=10,stroke_linecap='round')
    if bubbles:
        rr=rnd(9)
        for i in range(26): s+=C(rr.uniform(-280,280),rr.uniform(-250,-200),rr.uniform(14,30),'#FFFFFF',.15,opacity='.92')
    return s
def shower():
    s=R(-160,-560,320,560,'#BFD8EC',rx=6,k=.5,opacity='.45')+R(-170,-14,340,14,'#E1E5EA',rx=4)+ln('M-150 -560 L-150 -10 M150 -560 L150 -10','#9AA3AF',5)
    s+=path('M100 -470 L100 -520 Q100 -540 80 -540 L20 -540',fill='none',stroke='#9AA3AF',stroke_width=8)+E(10,-534,34,10,'#C9CED6')
    for x in range(-14,40,10): s+=ln(f'M{x} -520 L{x-6} -380','#9FD3E8',2,'.7')
    return s+hi('M-120 -520 L-80 -100','#fff','.5',8)
def sink_vanity():
    s=R(-160,-200,320,200,'#7A8A9A',rx=8)+R(-170,-224,340,28,'#F3F1EC',rx=6,k=.35)+E(0,-226,90,10,'#E1E5EA',k=.35)
    s+=path('M-10 -228 L-10 -270 Q-10 -284 10 -284 L40 -284',fill='none',stroke='#9AA3AF',stroke_width=10,stroke_linecap='round')
    s+=ln('M0 -190 L0 -20','#5A6676',3)+''.join(R(x,-110,26,8,'#C9CED6',rx=3) for x in (-50,24))
    return s
def towel_rack(c='#9FD3C8'): return ln('M-90 -200 L90 -200','#9AA3AF',6)+''.join(C(x,-200,6,'#9AA3AF') for x in (-96,96))+path('M-70 -200 L70 -200 L70 -60 L-70 -60Z',**S(c))+ln('M-70 -90 L70 -90',light(c,.4),6)
def toilet_paper(): return ln('M-40 -80 L40 -80','#9AA3AF',5)+C(0,-80,30,'#F7F6F2',.35)+C(0,-80,10,'#C9A16E')+path('M24 -66 L24 20 L-10 20 L-6 -60Z',fill='#F7F6F2',stroke='#D2CCBE',stroke_width=2)
def rubber_duck(): return E(0,-40,54,38,'#F2C230')+C(30,-90,30,'#F2C230')+path('M56 -88 L84 -80 L56 -72Z',**S('#F2853A'))+C(38,-96,5,'#22252D')+hi('M-30 -60 Q0 -76 30 -60','#fff','.6',5)
def soap_dispenser(): return R(-26,-110,52,110,'#F2A6B8',rx=14)+R(-8,-140,16,32,'#F3F1EC',rx=4)+R(-8,-140,40,10,'#F3F1EC',rx=4)+hi('M-14 -96 L-14 -20','#fff','.6',4)
# ---------- office / school ----------
def printer():
    return R(-140,-140,280,140,'#E1E5EA',rx=10)+R(-120,-170,240,36,'#C9CED6',rx=6)+R(-90,-200,180,34,'#F7F6F2',k=.3)+R(-110,-60,220,14,'#2F333B',rx=4)+R(-80,-46,160,40,'#F7F6F2',k=.3)+C(110,-110,7,'#3FA34D')
def water_cooler():
    return R(-60,-300,120,300,'#E6E9EE',rx=10)+path('M-50 -300 Q-60 -360 -40 -420 L40 -420 Q60 -360 50 -300Z',fill='#9FD3E8',fill_opacity='.75',stroke='#5A8ACF',stroke_width=2.4)+R(-14,-440,28,22,'#5A8ACF',rx=4)+R(-34,-240,22,16,'#3E7AD6',rx=3)+R(12,-240,22,16,'#E2493B',rx=3)+R(-40,-180,80,60,'#C9CED6',rx=4)
def whiteboard(chart=True):
    s=R(-260,-560,520,320,'#F7F6F2',rx=6,k=.3)+R(-270,-570,540,340,'none',rx=8,fill='none',stroke='#9AA3AF',stroke_width=12)+R(-200,-236,400,12,'#9AA3AF',rx=4)
    s+=ln('M-200 -240 L-240 0 M200 -240 L240 0','#5A606C',8)
    if chart:
        s+=ln('M-220 -280 L-220 -520 M-220 -280 L220 -280','#22252D',3)+ln('M-200 -320 L-120 -380 L-40 -350 L40 -440 L120 -420 L200 -500','#E2493B',6)
        for i,h in enumerate((60,110,80,150)): s+=R(-200+i*50,-280-h,30,h,'#5A8ACF',k=.4,opacity='.8')
        s+=text('Q4 GOALS',90,-524,size=26,fill='#3E6A9A',weight=800,anchor='middle')
    return s
def filing_cabinet():
    s=R(-100,-420,200,420,'#7A8A9A',rx=6)
    for i in range(4): s+=R(-86,-406+i*102,172,90,light('#7A8A9A',.08),rx=4)+R(-30,-370+i*102,60,14,'#C9CED6',rx=4)+R(-20,-396+i*102,40,16,'#F7F6F2',k=.3)
    return s
def desk_phone(): return R(-80,-60,160,60,'#2F333B',rx=12)+path('M-90 -60 Q-90 -100 -60 -104 L60 -104 Q90 -100 90 -60 L60 -70 L-60 -70Z',**S('#3A3E47'))+''.join(R(-40+i%3*28,-48+i//3*14,20,10,'#9AA3AF',rx=2) for i in range(6))+R(40,-50,30,30,'#7FE0A8',rx=3)
def stapler(): return path('M-90 0 L90 0 L90 -16 L-90 -16Z',**S('#2F333B'))+path('M-90 -16 L80 -40 Q96 -40 94 -26 L-90 -20Z',**S('#D6453A'))
def pen_cup(): return ''.join(ln(f'M{x} -60 L{x+t} -140',c,6) for x,t,c in ((-14,-10,'#3E6A9A'),(0,4,'#E2493B'),(12,16,'#22252D'),(-4,-2,'#F2C230')))+path('M-30 -80 L-26 0 L26 0 L30 -80Z',**S('#5A8A7A'))
def globe(): return path('M-70 0 L70 0 L50 -20 L-50 -20Z',**S('#5A3E2A'))+ln('M0 -20 L0 -60','#5A3E2A',8)+C(0,-150,90,'#5A9ED6')+path('M-50 -200 Q-10 -220 20 -190 Q0 -160 -30 -170 Q-60 -150 -70 -170Z M10 -120 Q50 -140 70 -110 Q60 -80 30 -90 Q10 -90 10 -120Z',fill='#7FB34E',stroke='#4E8A40',stroke_width=2)+path('M-80 -80 A110 110 0 0 1 60 -250',fill='none',stroke='#C9A23B',stroke_width=6)
def cork_board():
    s=R(-200,-300,400,260,'#C9A16E',rx=6)+R(-210,-310,420,280,'none',fill='none',stroke='#7A5A43',stroke_width=14)
    for x,y,c,r_ in ((-150,-260,'#F2D45A',-6),(-40,-250,'#9FD3E8',4),(70,-260,'#F2A6B8',-3),(-110,-150,'#F7F6F2',3),(20,-160,'#7FE0A8',-5),(120,-150,'#F2D45A',6)):
        s+=g(R(-40,0,80,70,c,k=.35)+''.join(ln(f'M-28 {16+i*14} L28 {16+i*14}','#5A6676',2,'.5') for i in range(3))+C(0,4,6,'#E2493B'),transform=f'translate({x} {y}) rotate({r_})')
    return s
def paper_stack(n=8): return ''.join(R(-80+(i%2)*3,-8-i*8,160,8,'#F7F6F2',k=.3) for i in range(n))
def projector_screen(): return R(-300,-620,600,16,'#3A3E47',rx=6)+R(-280,-604,560,360,'#F7F6F2',k=.3)+R(-280,-604,560,16,'#2F333B')+ln('M0 -244 L0 -200','#5A606C',3)+C(0,-196,8,'#5A606C')
# ---------- gym ----------
def treadmill():
    s=path('M-260 -20 L200 -60 L210 -30 L-250 0Z',**S('#2F333B'))+ln('M150 -50 L190 -300','#3A3E47',12)+R(140,-340,110,50,'#22252D',rx=8)+R(156,-330,60,26,'#7FE0A8',rx=3)
    return s+ln('M120 -260 L200 -270','#3A3E47',10)+path('M-240 -12 L190 -50',stroke='#5A606C',stroke_width=4)
def bench_press():
    s=R(-200,-140,300,30,'#C8573E',rx=10)+ln('M-150 -110 L-170 0 M60 -110 L80 0','#3A3E47',10)
    s+=ln('M120 -140 L120 -320 M180 -140 L180 -320','#3A3E47',10)+ln('M60 -320 L240 -320','#9AA3AF',8)
    return s+E(60,-320,16,52,'#22252D')+E(240,-320,16,52,'#22252D')
def kettlebell(c='#3A3E47',w='16'): return path('M-30 -110 Q-30 -150 0 -150 Q30 -150 30 -110',fill='none',stroke=dark(c,.4),stroke_width=16)+path('M-30 -110 Q-30 -150 0 -150 Q30 -150 30 -110',fill='none',stroke=c,stroke_width=10)+path('M-60 -60 Q-60 -116 0 -116 Q60 -116 60 -60 Q60 0 0 0 Q-60 0 -60 -60Z',**S(c))+text(w,0,-46,size=26,fill='#F2C230',weight=900,anchor='middle')
def yoga_mat(rolled=False,c='#7C5CD6'):
    if rolled: return C(0,-40,40,c)+C(0,-40,28,light(c,.15),.4)+C(0,-40,14,c)+R(0,-80,240,80,c,k=.55,opacity='0')
    return path('M-260 0 L260 0 L250 -14 L-250 -14Z',**S(c))+hi('M-240 -10 L240 -10','#fff','.35',3)
def punching_bag(c='#B8463A'): return ln('M0 -600 L0 -520','#9AA3AF',4)+ln('M-50 -470 L0 -520 L50 -470','#9AA3AF',3)+R(-60,-480,120,300,c,rx=40)+R(-62,-440,124,20,dark(c,.2))+R(-62,-260,124,20,dark(c,.2))+hi('M-36 -440 L-36 -220','#fff','.4',6)
def barbell_rack():
    s=ln('M-200 0 L-200 -300 M200 0 L200 -300','#3A3E47',14)+ln('M-230 0 L-170 0 M170 0 L230 0','#3A3E47',10)
    for y in (-260,-170,-80):
        s+=ln(f'M-210 {y} L210 {y}','#9AA3AF',7)
        for x in (-160,160): s+=E(x,y,14,40,'#22252D')
    return s
def jump_rope(): return path('M-120 -20 Q0 -160 120 -20',fill='none',stroke='#E2493B',stroke_width=5)+R(-140,-60,20,50,'#22252D',rx=8)+R(120,-60,20,50,'#22252D',rx=8)
def exercise_bike():
    s=C(-150,-60,56,'#3A3E47')+C(-150,-60,20,'#9AA3AF')+ln('M-150 -60 L-60 -60 L20 -220 M-60 -60 L-40 -240 M20 -220 L60 -240','#5A606C',12)
    return s+R(-80,-260,90,20,'#22252D',rx=8)+R(40,-260,40,30,'#22252D',rx=6)+R(-220,-14,300,14,'#3A3E47',rx=6)
def medicine_ball(): return C(0,-60,60,'#3A3E47')+path('M-60 -60 Q0 -40 60 -60 M0 -120 Q20 -60 0 0',fill='none',stroke='#F2C230',stroke_width=5)
# ---------- music ----------
def piano_upright():
    s=R(-220,-380,440,380,'#2A2124',rx=8)+R(-200,-360,400,120,'#3A2E30',rx=4)+R(-210,-240,420,60,'#F7F6F2',k=.3)
    for x in range(-210,210,20): s+=ln(f'M{x} -240 L{x} -180','#B8AE9C',1.4)
    for x in range(-200,200,20):
        if (x//20)%7 not in (2,6): s+=rect(x+13,-240,10,36,fill='#15161A')
    s+=R(-230,-190,460,20,'#2A2124',rx=4)+R(-200,-40,30,40,'#2A2124')+R(170,-40,30,40,'#2A2124')+R(-60,-330,120,70,'#F7F6F2',k=.3,opacity='.9')
    return s
def drum_kit():
    s=E(0,-120,110,110,'#C8573E')+E(0,-120,80,80,'#F7F6F2',k=.3)+text('ROCK',0,-110,size=26,fill='#C8573E',weight=900,anchor='middle')
    s+=R(-200,-200,100,80,'#C8573E',rx=10)+E(-150,-200,50,10,'#F7F6F2',k=.3)+R(120,-160,90,70,'#C8573E',rx=10)+E(165,-160,45,9,'#F7F6F2',k=.3)
    s+=ln('M-220 -260 L-220 0 M240 -330 L240 0','#9AA3AF',5)+E(-220,-268,70,8,'#E3B24A')+E(240,-336,80,9,'#E3B24A')
    return s+ln('M60 -260 L120 -300 M80 -250 L130 -310','#E8C468',5)
def violin():
    s=path('M0 -40 C-50 -40 -60 -90 -34 -110 C-60 -130 -50 -180 0 -180 C50 -180 60 -130 34 -110 C60 -90 50 -40 0 -40Z',**S('#B8662E'))
    s+=R(-8,-300,16,140,'#2A2124',rx=4)+path('M-10 -300 Q-20 -330 0 -334 Q20 -330 10 -300Z',**S('#8A4A22'))+ln('M-12 -110 l-6 14 M12 -110 l6 14','#2A2124',3)+ln('M-3 -60 L-3 -290 M3 -60 L3 -290','#E8DCC6',1)
    return s+ln('M60 -40 L-120 -300','#5A3E2A',4)
def mic_stand(): return ln('M0 0 L0 -400 M0 -400 L40 -460','#3A3E47',8)+path('M-60 0 L60 0',stroke='#3A3E47',stroke_width=10,stroke_linecap='round')+g(R(-14,-30,28,40,'#3A3E47',rx=6)+C(0,-40,16,'#9AA3AF'),transform='translate(44 -460) rotate(30)')
def amp(): return R(-130,-220,260,220,'#2A2D35',rx=10)+R(-110,-200,220,40,'#3A3E47',rx=4)+''.join(C(x,-180,8,'#C9CED6') for x in (-80,-50,-20,10))+R(-110,-150,220,130,'#5A606C',rx=6,k=.5)+C(0,-86,50,'#2F333B')+text('LOUD',0,-30,size=14,fill='#C9A23B',weight=800,anchor='middle')
def setar():
    s=path('M0 -10 Q-48 -30 -40 -90 Q-30 -130 0 -132 Q30 -130 40 -90 Q48 -30 0 -10Z',**S('#9C6A3E'))
    s+=R(-7,-420,14,300,'#5A3E2A',rx=4)+R(-12,-450,24,36,'#3A2E26',rx=6)+''.join(ln(f'M-7 {y} L7 {y}','#E8DCC6',1.6) for y in range(-400,-140,22))
    return s+ln('M-2 -40 L-2 -440 M2 -40 L2 -440','#E8DCC6',.8)+''.join(C(sx*16,-430+i*12,4,'#E8DCC6') for sx in (-1,1) for i in range(2))
def electric_guitar(c='#D6453A'):
    s=path('M0 0 C-70 0 -80 -60 -50 -80 C-80 -110 -60 -150 -20 -130 L20 -130 C60 -170 80 -110 50 -80 C80 -60 70 0 0 0Z',**S(c))+R(-8,-400,16,280,'#C9A16E',rx=4)+R(-14,-440,28,48,'#2A2124',rx=6)
    return s+R(-30,-90,60,14,'#22252D',rx=3)+R(-30,-60,60,14,'#22252D',rx=3)+ln('M-2 -40 L-2 -400 M2 -40 L2 -400','#E8DCC6',.8)
def turntable(): return R(-160,-70,320,70,'#3A2E26',rx=8)+E(-30,-74,110,20,'#15161A')+E(-30,-76,36,8,'#E2493B')+ln('M110 -80 L60 -100 L10 -84','#C9CED6',5)+C(110,-80,10,'#9AA3AF')
def synth(): return R(-220,-60,440,60,'#2A2D35',rx=8)+''.join(R(x,-34,16,30,'#F7F6F2',rx=2,k=.3) for x in range(-200,200,18))+''.join(C(x,-48,6,'#F2853A') for x in range(-190,-80,24))
# ---------- tech ----------
def tablet(screen='#3B5B8A'): return R(-100,-150,200,150,'#22252D',rx=14)+R(-88,-138,176,126,screen,rx=6)+''.join(R(-70+i*40,-120,28,28,c,rx=6) for i,c in enumerate(('#F2C230','#E2493B','#3FA34D','#7C5CD6')))+hi('M-80 -130 L-30 -130','#fff','.3',3)
def drone(): return R(-60,-50,120,40,'#3A3E47',rx=14)+''.join(ln(f'M{sx*50} -40 L{sx*140} -60','#3A3E47',8)+E(sx*140,-70,60,8,'#C9CED6',opacity='.8') for sx in (-1,1))+C(0,-14,12,'#22252D')+C(0,-14,5,'#5A8ACF')+C(30,-40,4,'#3FE08A')
def vr_headset(): return R(-110,-80,220,90,'#F3F4F6',rx=30)+R(-96,-66,192,62,'#22252D',rx=24)+path('M-110 -40 Q-170 -40 -170 20 M110 -40 Q170 -40 170 20',fill='none',stroke='#3A3E47',stroke_width=10)+hi('M-80 -60 Q0 -74 80 -60','#7FB3E0','.6',4)
def smart_speaker(): return path('M-50 0 L-50 -150 Q-50 -170 0 -170 Q50 -170 50 -150 L50 0Z',**S('#3A3E47'))+E(0,-160,50,10,'#2F333B')+E(0,-160,40,6,'none',fill='none',stroke='#3FC0F0',stroke_width=4)+''.join(ln(f'M-40 {y} L40 {y}','#2F333B',2) for y in range(-130,-10,12))
def router(): return R(-110,-50,220,50,'#F3F4F6',rx=10)+''.join(ln(f'M{x} -50 L{x+8*(x/80)} -150','#3A3E47',8) for x in (-80,0,80))+''.join(C(x,-24,5,'#3FE08A') for x in (-60,-40,-20))
def ring_light(on=True):
    s=ln('M0 0 L0 -420','#3A3E47',8)+ln('M-80 0 L0 -60 L80 0','#3A3E47',6)
    if on: s+=C(0,-500,140,'#FFF3C4',.3,opacity='.25')
    s+=circ(0,-500,100,fill='none',stroke='#2F333B',stroke_width=30)+circ(0,-500,100,fill='none',stroke='#FFF8DC' if on else '#C9CED6',stroke_width=20)
    return s+R(-20,-520,40,72,'#22252D',rx=6)
def podcast_mic(): return ln('M0 -40 L0 -200','#3A3E47',8)+R(-70,-40,140,40,'#3A3E47',rx=10)+R(-34,-330,68,140,'#22252D',rx=34)+''.join(ln(f'M-26 {y} L26 {y}','#5A606C',2) for y in range(-310,-210,12))+path('M-50 -280 Q-50 -190 0 -190 Q50 -190 50 -280',fill='none',stroke='#9AA3AF',stroke_width=6)
def gaming_pc():
    s=R(-80,-300,160,300,'#22252D',rx=10)+R(-64,-280,90,260,'#2A2D35',rx=6)+R(-60,-276,82,252,'#7C5CD6',rx=4,k=.5,opacity='.5')
    for y in (-230,-150,-70): s+=circ(-18,y,26,fill='none',stroke='#3FC0F0',stroke_width=4)
    return s+C(54,-270,6,'#3FE08A')
def game_console(): return R(-150,-40,300,40,'#F3F4F6',rx=14)+R(-140,-36,120,30,'#22252D',rx=10)+C(110,-20,8,'#3FC0F0')+path('M-150 -20 Q-160 -30 -150 -40',fill='none',stroke='#3A3E47',stroke_width=2)
def webcam(): return R(-40,-20,80,20,'#3A3E47',rx=8)+ln('M0 -20 L0 -60','#3A3E47',8)+E(0,-90,60,40,'#22252D')+C(0,-90,22,'#3A4A6A')+C(0,-90,10,'#5A8ACF')+C(40,-110,4,'#E2493B')
def camera_tripod(): return ln('M0 -260 L-90 0 M0 -260 L90 0 M0 -260 L0 0','#3A3E47',8)+R(-60,-330,120,76,'#2F333B',rx=10)+C(0,-292,28,'#5A606C')+C(0,-292,14,'#5A8ACF')+R(30,-344,26,14,'#3A3E47',rx=3)
def projector(): return R(-120,-80,240,80,'#E1E5EA',rx=14)+C(70,-40,30,'#3A3E47')+C(70,-40,16,'#9FD3E8')+path('M100 -40 L500 -200 L500 120Z',fill='#FFF8DC',opacity='.18')
def smartwatch_big(): return R(-34,-140,68,40,'#2F333B',rx=12)+R(-34,20,68,40,'#2F333B',rx=12)+R(-60,-110,120,140,'#22252D',rx=30)+R(-48,-96,96,112,'#1A2433',rx=22)+text('10:42',0,-30,size=30,fill='#7FE0A8',weight=800,anchor='middle')+path('M-22 -6 C-30 -12 -28 -20 -22 -20 C-19 -20 -18 -17 -18 -16 C-18 -17 -17 -20 -14 -20 C-8 -20 -6 -12 -18 -4Z',fill='#E2493B')+text('72',8,4,size=18,fill='#E2493B',weight=700,anchor='middle')
GROUPS=dict(kitchen=dict(microwave=microwave(),microwave_on=microwave(True),toaster=toaster(),toaster_pop=toaster(True),kettle=kettle(),kettle_blue=kettle('#3E7AD6'),coffee_machine=coffee_machine(),blender=blender(),oven_range=oven_range(),washing_machine=washing_machine(),washing_machine_on=washing_machine(True),fridge_double=fridge_double(),kitchen_sink=kitchen_sink(),frying_pan_egg=frying_pan(),plate_stack=plate_stack(),cutting_board=cutting_board(),fruit_bowl=fruit_bowl(),samovar=samovar(),tea_glass=tea_glass(),teapot=teapot(),wine_glass=wine_glass(),glass_water=glass_water()),
 bathroom=dict(toilet=toilet(),bathtub=bathtub(),bathtub_bubbles=bathtub(True),shower=shower(),sink_vanity=sink_vanity(),towel_rack=towel_rack(),towel_rack_pink=towel_rack('#F2A6B8'),toilet_paper=toilet_paper(),rubber_duck=rubber_duck(),soap_dispenser=soap_dispenser()),
 office=dict(printer=printer(),water_cooler=water_cooler(),whiteboard_chart=whiteboard(),whiteboard_blank=whiteboard(False),filing_cabinet=filing_cabinet(),desk_phone=desk_phone(),stapler=stapler(),pen_cup=pen_cup(),globe=globe(),cork_board=cork_board(),paper_stack=paper_stack(),projector_screen=projector_screen()),
 gym=dict(treadmill=treadmill(),bench_press=bench_press(),kettlebell=kettlebell(),kettlebell_pink=kettlebell('#E88AA8','8'),yoga_mat=yoga_mat(),yoga_mat_rolled=yoga_mat(True),punching_bag=punching_bag(),barbell_rack=barbell_rack(),jump_rope=jump_rope(),exercise_bike=exercise_bike(),medicine_ball=medicine_ball()),
 music=dict(piano_upright=piano_upright(),drum_kit=drum_kit(),violin=violin(),mic_stand=mic_stand(),guitar_amp=amp(),setar=setar(),electric_guitar=electric_guitar(),electric_guitar_blue=electric_guitar('#3E7AD6'),turntable=turntable(),synth_keyboard=synth()),
 tech2=dict(tablet=tablet(),drone=drone(),vr_headset=vr_headset(),smart_speaker=smart_speaker(),wifi_router=router(),ring_light_on=ring_light(),ring_light_off=ring_light(False),podcast_mic=podcast_mic(),gaming_pc=gaming_pc(),game_console=game_console(),webcam=webcam(),camera_tripod=camera_tripod(),projector=projector(),smartwatch_closeup=smartwatch_big()))
def items():
    o={}
    for k,v in GROUPS.items(): o.update(v)
    return o
