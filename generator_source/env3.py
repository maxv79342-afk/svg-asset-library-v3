"""v3 backgrounds (1920x1080, floor line FL=860)."""
from sv import *
import env as EN, props as PR
import props3_beds as PB, props3_vehicles as PV, props3_home as PH, props3_world as PW, tattoo as TT
from p3base import R as PR3, S as S3, hi as hi3, GLASS
W,H=1920,1080; FL=EN.FL; T=EN.T
def sky(mode): return {'day':'url(#skyDay)','night':'url(#skyNight)','sunset':'url(#skySunset)'}[mode]
def stars(n=90,seed=5,ymax=500):
    rr=rnd(seed); return ''.join(circ(rr.uniform(0,W),rr.uniform(0,ymax),rr.uniform(.8,2.2),fill='#fff',opacity=f(rr.uniform(.3,.95))) for _ in range(n))
def ceiling_lights(n=4,c='#FFF3C4',y=0):
    return ''.join(rect(x-80,y,160,14,fill='#E6E9EE')+path(f'M{x-80} {y+14} L{x+80} {y+14} L{x+220} {FL} L{x-220} {FL}Z',fill=c,opacity='.07') for x in [W*(i+.5)/n for i in range(n)])
def poster(txt,c,x,y,w=160,h=220,tc='#F7F3EA'):
    return PR3(x,y,w,h,c,rx=4)+text(txt,x+w/2,y+h/2+10,size=30,fill=tc,weight=900,anchor='middle',family="'Bebas Neue',Oswald,Impact,sans-serif")
def neon(txt,x,y,c='#FF4FA0',size=90):
    return text(txt,x,y,size=size,fill='none',weight=900,anchor='middle',stroke=c,stroke_width=10,opacity='.25',family="'Bebas Neue',Oswald,Impact,sans-serif")+text(txt,x,y,size=size,fill='none',weight=900,anchor='middle',stroke=light(c,.5),stroke_width=3.4,family="'Bebas Neue',Oswald,Impact,sans-serif")
def window_city(x,y,w,h,mode='night'):
    s=rect(x,y,w,h,fill=sky(mode))
    rr=rnd(int(x+y))
    for i in range(int(w/50)+1):
        bw=rr.uniform(30,70); bh=rr.uniform(h*.25,h*.8); bx=x+i*50
        s+=rect(bx,y+h-bh,min(bw,x+w-bx),bh,fill='#151D36' if mode=='night' else '#A9BFD3')
        if mode=='night':
            for k in range(8):
                if rr.random()>.55: s+=rect(bx+6+(k%2)*16,y+h-bh+12+(k//2)*22,6,10,fill='#FFD98A',opacity='.85')
    s+=rect(x-10,y-10,w+20,h+20,fill='none',stroke='#E6E9EE',stroke_width=16)+''.join(rect(x+w*k/3-4,y,8,h,fill='#E6E9EE') for k in (1,2))
    return s
# ---------------------------------------------------------------- interiors
def gym():
    s=EN.wall('brick','#5A5F6A')+rect(0,FL,W,H-FL,fill='#2A2D35')+''.join(rect(x,FL,2,H-FL,fill='#22252D') for x in range(0,W,160))
    s+=rect(0,300,W,280,fill='#9FB8C4',opacity='.25')+rect(0,296,W,8,fill='#C9CED6')+rect(0,580,W,8,fill='#C9CED6')
    s+=poster('NO PAIN NO GAIN','#C8573E',1560,90,300,150)+ceiling_lights(4)
    p=T(PH.treadmill(),260,FL)+T(PH.treadmill(),620,FL)+T(PH.bench_press(),1060,FL)+T(PH.barbell_rack(),1500,FL,.9)+T(PH.punching_bag(),1800,FL-20,.9)
    p+=T(PH.kettlebell(),860,FL,.6)+T(PH.kettlebell('#E88AA8','8'),920,FL,.5)+T(PH.yoga_mat(),1300,FL+120)+T(PH.medicine_ball(),1200,FL+60,.7)+T(PH.water_cooler(),80,FL,.9)
    return g(s,id='room')+g(p,id='equipment')+g(EN.vignette(),id='lighting')
def hospital_room():
    s=EN.wall('plain','#B8D4C8')+EN.floor('tiles','#D6D2C4')+EN.baseboard('#8AA89A')+T(PR.window(320,320,'day'),420,560)
    s+=rect(1560,120,20,600,fill='#C9CED6')+path('M1560 140 L1900 140 L1900 760 Q1730 780 1560 760Z',fill='#9FC4E8',opacity='.85')+''.join(ln_ for ln_ in [path(f'M{x} 150 Q{x+10} 450 {x} 750',fill='none',stroke='#7FA8D0',stroke_width=4) for x in range(1600,1900,60)])
    mon=PR3(-80,-140,160,120,'#2F333B',rx=10)+rect(-68,-128,136,96,fill='#10241A')+path('M-60 -80 L-30 -80 L-20 -110 L-8 -50 L4 -90 L14 -80 L60 -80',fill='none',stroke='#3FE08A',stroke_width=4)+text('72',40,-104,size=18,fill='#3FE08A',weight=800)
    p=T(PB.bed_hospital('made'),760,FL)+T(mon,1340,500)+rect(1336,500,8,FL-500,fill='#9AA3AF')+T(PR.chair_wood(),1460,FL,.9)+T(PR.plant(),300,FL,.8)+T(PR.wall_clock(),1000,200,.6)
    return g(s,id='room')+g(p,id='furniture')+g(EN.vignette(),id='lighting')
def supermarket():
    s=rect(0,0,W,H,fill='#E8ECEF')+rect(0,0,W,90,fill='#3FA34D')+text('FRESH MARKET',W/2,64,size=48,fill='#fff',weight=900,anchor='middle')+EN.floor('tiles','#E1DED4')+ceiling_lights(5,'#FFFFFF',90)
    rr=rnd(77); cols=['#E2493B','#F2C230','#3E7AD6','#3FA34D','#F2853A','#7C5CD6','#F2A6B8','#9FD3E8']
    for sx in (60,1000):
        s+=PR3(sx,200,860,FL-200,'#C9CED6',rx=4)
        for row in range(5):
            y=230+row*126
            s+=rect(sx,y+96,860,14,fill='#9AA3AF')
            x=sx+16
            while x<sx+840:
                w=rr.uniform(34,70); h=rr.uniform(50,92); c=rr.choice(cols)
                s+=PR3(x,y+96-h,w,h,c,rx=4)+rect(x+4,y+96-h*0.6,w-8,h*.25,fill='#fff',opacity='.6'); x+=w+6
        s+=rect(sx+600,180,180,46,fill='#E2493B')+text('SALE -30%',sx+690,212,size=26,fill='#fff',weight=900,anchor='middle')
    return g(s,id='store')+g(EN.vignette(),id='lighting')
def metro():
    s=EN.wall('tiles','#D9E3E8',y1=FL-120)+rect(0,FL-120,W,40,fill='#3A3E47')+rect(0,FL-80,W,H-FL+80,fill='#8A8F99')+rect(0,FL-84,W,14,fill='#F2C230')
    s+=rect(0,120,W,90,fill='#22304F')+text('METRO  -  LINE 1  >  TAJRISH',W/2,180,size=46,fill='#F7F3EA',weight=800,anchor='middle')
    train=PR3(-40,300,1300,420,'#C9CED6',rx=40)+rect(-40,560,1300,30,fill='#E2493B')+''.join(PR3(40+i*240,360,180,150,GLASS,rx=12,k=.5) for i in range(5))+''.join(PR3(220+i*480,340,90,360,'#9AA3AF',rx=6,k=.4) for i in range(2))
    p=g(train,id='train')+T(PR.wall_clock(),1600,320,.6)+T(PW.bench_park(),1500,FL+40,.8)+T(PW.street_bin(),1800,FL+40,.6)
    return g(s,id='station')+p+g(EN.vignette(),id='lighting')
def beach(mode='day'):
    s=rect(0,0,W,H,fill=sky(mode))
    if mode=='day': s+=T(PR.sun(),1560,180,.9)+T(PR.cloud(),400,200)+T(PR.cloud(),1000,130,.6)
    else: s+=circ(960,560,140,fill='#FFC46A')+circ(960,560,220,fill='#FFC46A',opacity='.25')
    sea='#3E8ACF' if mode=='day' else '#5A4A7A'
    s+=rect(0,560,W,240,fill=sea)+''.join(path(f'M{x} {y} q30 -10 60 0',fill='none',stroke='#fff',stroke_width=3,opacity='.5') for x,y in ((200,620),(600,660),(1200,640),(1500,700),(900,720)))
    if mode=='sunset': s+=''.join(rect(860+((i*37)%120)-60,580+i*20,240-i*20,6,fill='#FFC46A',opacity='.6') for i in range(8))
    s+=path('M0 760 Q600 720 1200 770 T1920 760 L1920 1080 L0 1080Z',fill='#E8CF9A' if mode=='day' else '#B8936A')+path('M0 790 Q500 770 1000 800 T1920 790',fill='none',stroke='#fff',stroke_width=10,opacity='.5')
    um=path('M-150 -300 Q0 -420 150 -300Z',**S3('#E2493B'))+path('M-50 -330 Q0 -410 50 -330Z',fill='#F7F3EA')+rect(-5,-300,10,300,fill='#5A3E2A')
    p=T(PW.palm_tree(),220,880,1.2)+T(PW.palm_tree(),1760,860,1,flip=True)+T(um,1300,920)+T(PH.yoga_mat(c='#3E7AD6'),1200,960,.8)+T(PW.rock(),500,930,.7)
    return g(s,id='sky_sea_sand')+g(p,id='props')+g(EN.vignette(),id='lighting')
def forest(mode='day'):
    s=rect(0,0,W,H,fill=sky(mode))+(stars(60,9,400)+T(PR.moon(),1500,160,.8) if mode=='night' else T(PR.cloud(),600,160))
    for layer,(c,y,sc,n) in enumerate((('#5A8A6A',720,.7,14),('#3E7A54',800,.9,11),('#2E5E40',880,1.2,8))):
        col=c if mode=='day' else dark(c,.6)
        s+=rect(0,y,W,H-y,fill=dark(col,.2))
        for i in range(n): s+=T(PR.tree('pine' if (i+layer)%3 else 'round',col),i*W/(n-1)+((layer*70)%140)-70,y+10,sc)
    s+=path('M800 1080 Q900 960 1000 880 L1060 880 Q1000 960 1080 1080Z',fill='#B8936A' if mode=='day' else '#4A3A2E')
    p=T(PW.mushroom(),400,1000,.5)+T(PW.log(),1400,1010,.8)+T(PW.bush(),200,1040)+T(PW.grass_tuft(),1700,1040)
    if mode=='night': p+=T(PW.tent(),560,1020,1.1)+T(PW.campfire(),1100,1030,1)
    fx=EN.night_overlay(.3) if mode=='night' else ''
    if mode=='night': fx+=ell(1100,960,360,220,fill='url(#warmPool)')
    return g(s,id='forest')+g(p,id='props')+g(fx+EN.vignette(),id='lighting')
def mountains(snow=False):
    s=rect(0,0,W,H,fill='url(#skyDay)')+T(PR.sun(),1600,160,.7)+T(PR.cloud(),500,180)
    s+=T(PW.mountain(),500,760,2.4)+T(PW.mountain(),1400,760,2.8)+T(PW.mountain(),980,780,2)
    s+=rect(0,760,W,320,fill='#F3F6FA' if snow else '#8BBF6A')+path('M0 800 Q600 760 1300 820 T1920 800 L1920 1080 L0 1080Z',fill='#E6ECF4' if snow else '#6EA855')
    p=''.join(T(PR.tree('pine','#3E7A54' if not snow else '#4A6A5A'),x,880,.7) for x in (140,320,1500,1760))
    if snow:
        rr=rnd(12); p+=''.join(circ(rr.uniform(0,W),rr.uniform(0,H),rr.uniform(2,5),fill='#fff',opacity='.85') for _ in range(160))
        p+=''.join(path(f'M{x-110} {-330+880+40} Q{x} {-420+880+40} {x+110} {-330+880+40}',fill='none') for x in ())
    return g(s,id='landscape')+g(p,id='props')+g(EN.vignette(),id='lighting')
def desert():
    s=rect(0,0,W,H,fill='url(#skySunset)')+circ(1400,420,110,fill='#FFC46A')
    s+=path('M0 700 Q400 600 900 700 T1920 660 L1920 1080 L0 1080Z',fill='#D9A86A')+path('M0 820 Q500 740 1100 820 T1920 800 L1920 1080 L0 1080Z',fill='#C8904E')
    cac=lambda: path('M-20 0 L-20 -260 Q-20 -290 0 -290 Q20 -290 20 -260 L20 0Z',**S3('#4E8A48'))+path('M-20 -140 L-60 -140 L-60 -200 Q-60 -214 -48 -214 Q-36 -214 -36 -200 L-36 -160 L-20 -160Z M20 -110 L56 -110 L56 -180 Q56 -194 68 -194 Q80 -194 80 -180 L80 -90 L20 -90Z',**S3('#4E8A48'))
    p=T(cac(),300,900,1.1)+T(cac(),1600,880,.8)+T(PW.rock(),900,940,.8)+T(PW.rock(),1200,960,.5)
    return g(s,id='landscape')+g(p,id='props')+g(EN.vignette(),id='lighting')
def airport():
    s=rect(0,0,W,H,fill='#D9DEE6')+rect(0,80,W,560,fill='url(#skyDay)')
    plane=path('M-500 -40 Q-520 -90 -460 -100 L380 -100 Q470 -100 520 -60 Q540 -40 500 -20 L-460 -20 Q-500 -20 -500 -40Z',**S3('#F7F6F2',.35))+path('M-80 -60 L-220 120 L-140 120 L60 -40Z',**S3('#C9CED6'))+path('M-440 -100 L-500 -220 L-420 -220 L-340 -100Z',**S3('#3E7AD6'))+''.join(C_ for C_ in [circ(x,-70,8,fill='#3A4A6A') for x in range(-360,360,40)])+rect(-500,-40,1020,10,fill='#3E7AD6')
    s+=T(plane,1000,480,.9)+rect(0,560,W,80,fill='#8A8F99')
    for x in range(0,W+1,320): s+=rect(x-10,80,20,560,fill='#5A606C')
    s+=rect(0,640,W,H-640,fill='#B8BEC8')+''.join(rect(0,y,W,2,fill='#9AA3AF') for y in range(700,H,60))
    board=PR3(-200,-120,400,120,'#22252D',rx=8)+''.join(text(t,-180,-84+i*34,size=22,fill='#F2C230',weight=700,family='monospace') for i,t in enumerate(('IKA  08:40  BOARDING','DXB  09:15  ON TIME','IST  10:05  DELAYED')))
    seats=''.join(T(PR3(-40,-90,80,50,'#3E6A9A',rx=10)+PR3(-40,-150,80,70,'#3E6A9A',rx=12)+rect(-4,-40,8,40,fill='#5A606C'),x,980) for x in range(200,1800,110))
    return g(s,id='terminal')+g(T(board,1640,260),id='board')+g(seats,id='seats')+g(EN.vignette(),id='lighting')
def library():
    s=EN.wall('panels','#7A5A43')+EN.floor('wood','#5A4536')
    for x in (60,520,1380): s+=T(PR.bookshelf(),x+180,FL,1.5)
    s+=T(PR.window(260,340,'day'),1060,520)+ceiling_lights(3,'#FFE7A8')
    p=T(PR.table(420),780,FL)+T(PR.chair_wood(),720,FL,.9,flip=True)+T(PR.chair_wood(),1240,FL,.9)+T(PR.desk_lamp(True),880,FL-170,.8)+T(PR.book_stack(5),1060,FL-170,.6)+T(PH.globe(),1700,FL,.8)
    return g(s,id='room')+g(p,id='furniture')+g(EN.vignette(),id='lighting')
def restaurant():
    s=EN.wall('wallpaper','#6A2E36')+EN.floor('checker','#3A2E26')+EN.baseboard('#3A1E22')
    for x in (300,960,1620): s+=ell(x,0,140,40,fill='#FFE2A8',opacity='.25')+rect(x-4,0,8,120,fill='#22252D')+path(f'M{x-50} 160 L{x+50} 160 L{x+30} 120 L{x-30} 120Z',fill='#C9A23B')+ell(x,170,220,80,fill='url(#lampGlow)')
    s+=T(PR.picture_frame(),640,360,1)+T(PR.picture_frame('heart'),1280,360,1)
    tbl=PR3(-170,-170,340,24,'#F7F3EA',rx=4,k=.3)+path('M-170 -146 L-180 -60 L180 -60 L170 -146Z',fill='#F7F3EA',stroke='#D2CCBE',stroke_width=2)+rect(-10,-60,20,60,fill='#3A2E26')+T(PH.wine_glass(),-60,-170,.5)+T(PR.candle() if hasattr(PR,'candle') else '',0,-170,.4)+C_candle()
    p=T(tbl,520,FL+80)+T(tbl,1400,FL+80)+T(PR.chair_wood(),300,FL+80,.9)+T(PR.chair_wood(),740,FL+80,.9,flip=True)+T(PR.chair_wood(),1180,FL+80,.9)+T(PR.chair_wood(),1620,FL+80,.9,flip=True)
    return g(s,id='room')+g(p,id='tables')+g(EN.night_overlay(.18,'#200810')+EN.vignette(),id='lighting')
def C_candle(): return rect(-6,-220,12,50,fill='#F7F3EA')+path('M0 -222 q-6 -10 0 -20 q6 10 0 20Z',fill='#FFB13B')+ell(0,-230,40,40,fill='url(#lampGlow)')
def school_hallway():
    s=EN.wall('plain','#E6D8B8')+EN.floor('tiles','#C9C3B8')+EN.baseboard('#7A6A5A')
    for i in range(14): s+=PR3(40+i*96,FL-420,88,420,['#3E6A9A','#3E6A9A','#C8573E'][i%3==2],rx=4)+''.join(rect(56+i*96,FL-400+k*12,56,4,fill='#000',opacity='.2') for k in range(4))+rect(110+i*96,FL-240,8,40,fill='#C9CED6')
    s+=poster('SCIENCE FAIR','#3FA34D',300,80,260,160)+poster('BE KIND','#7C5CD6',1200,90,220,150)+T(PR.wall_clock(),960,170,.6)+ceiling_lights(4)
    return g(s,id='hallway')+g(EN.vignette(),id='lighting')
def tattoo_studio():
    s=EN.wall('brick','#2A2224')+EN.floor('checker','#1E1E22')
    s+=neon('INK & SOUL',960,200,'#FF4FA0',120)
    flash=''
    for i,d in enumerate(['rose','swallow','anchor','skull','koi','dagger','heart','butterfly','compass','snake','moon','lotus']):
        x=180+(i%6)*130+(0 if i<6 else 0)+(i//6)*0; y=300+(i//6)*150
        if i>=6: x=1180+((i-6)%6)*110; y=300
        flash+=PR3(x-50,y-60,100,120,'#F3EAD7',rx=3,k=.45)+g(TT.DESIGNS[d](),transform=f'translate({x} {y}) scale(4.4)')
    chair=PR3(-200,-170,360,40,'#22252D',rx=18)+path('M-200 -170 L-260 -330 L-220 -340 L-160 -170Z',**S3('#22252D'))+rect(-20,-130,40,110,fill='#5A606C')+PR3(-110,-20,220,20,'#5A606C',rx=8)
    lamp=path('M0 0 L0 -500 L180 -560',fill='none',stroke='#5A606C',stroke_width=10)+path('M150 -580 L230 -540 L200 -500 L130 -540Z',**S3('#3A3E47'))+ell(190,-470,120,90,fill='url(#lampGlow)')
    p=T(chair,900,FL+60)+T(lamp,560,FL+40)+T(PR3(-80,-140,160,140,'#3A3E47',rx=8)+''.join(C(x,-150,10) for x in ()),1500,FL+40)+T(PR.plant('monstera'),1760,FL+20,.9)
    return g(s,id='room')+g(flash,id='flash_wall')+g(p,id='furniture')+g(EN.night_overlay(.12,'#1A0010')+EN.vignette(),id='lighting')
def C(*a,**k): return ''
def garage():
    s=EN.wall('panels','#8A8F99')+rect(0,FL,W,H-FL,fill='#7A7E86')+''.join(ell(x,y,120,20,fill='#5A5E66',opacity='.3') for x,y in ((500,980),(1300,1020)))
    s+=PR3(80,180,560,360,'#5A606C',rx=4)+''.join(ln for ln in [path(f'M{x} 220 L{x} {300+((x*7)%60)}',stroke='#2F333B',stroke_width=10,stroke_linecap='round') for x in range(130,620,50)])
    s+=PR3(1500,240,340,FL-240,'#3A3E47',rx=4)+''.join(rect(1500,300+k*140,340,10,fill='#22252D') for k in range(4))+''.join(PR3(1520+i*80,240+k*140,60,60,['#E2493B','#F2C230','#3E7AD6','#3FA34D'][(i+k)%4],rx=4) for i in range(4) for k in range(4))
    p=T(PV.sedan('#3E6A8A'),1000,1000,1.3)+T(PW.traffic_cone(),300,1000,.8)
    return g(s,id='garage')+g(p,id='car')+g(EN.vignette(),id='lighting')
def highway(mode='day'):
    s=rect(0,0,W,H,fill=sky(mode))+(stars(80,3,400)+T(PR.moon(),300,150,.8) if mode=='night' else T(PR.sun(),300,160,.8)+T(PR.cloud(),900,150))
    rr=rnd(40)
    for i in range(30):
        bw=rr.uniform(50,110); bh=rr.uniform(120,360); bx=i*66
        s+=rect(bx,600-bh,bw,bh,fill='#A9BFD3' if mode=='day' else '#151D36')
        if mode=='night': s+=''.join(rect(bx+8+(k%3)*14,600-bh+12+(k//3)*24,6,10,fill='#FFD98A',opacity='.8') for k in range(12) if rr.random()>.6)
    s+=rect(0,600,W,120,fill='#6EA855' if mode=='day' else '#1E2E28')+rect(0,720,W,360,fill='#3A3D44' if mode=='day' else '#1C1E24')
    s+=''.join(rect(x,880,120,12,fill='#F2C230',opacity='.85') for x in range(0,W,220))+rect(0,730,W,8,fill='#F7F6F2')+rect(0,1060,W,8,fill='#F7F6F2')
    s+=rect(0,700,W,10,fill='#C9CED6')+''.join(rect(x,690,8,30,fill='#9AA3AF') for x in range(0,W,80))
    nt=mode=='night'
    p=T(PV.sedan('#D6453A',nt),500,860,.8)+T(PV.suv('#F3F4F6',nt),1300,860,.8)+T(PV.delivery_truck(nt) if False else PV.box_truck(night=nt),1100,1040,.7)+T(PV.sports('#F2C230',nt),300,1040,.8)
    return g(s,id='sky_city')+g(p,id='traffic')+g((EN.night_overlay(.2) if nt else '')+EN.vignette(),id='lighting')
def snow_park():
    s=rect(0,0,W,H,fill='#B8C8DA')+path('M0 700 Q480 640 960 700 T1920 680 L1920 1080 L0 1080Z',fill='#F3F6FA')+path('M0 820 Q600 780 1200 830 T1920 820 L1920 1080 L0 1080Z',fill='#E6ECF4')
    p=''.join(T(PR.tree('bare'),x,800,s_) for x,s_ in ((200,1.1),(700,.8),(1500,1.2),(1800,.9)))+T(PW.bench_park(),1100,900,.8)+T(PR.street_lamp(True),900,860,.9)
    rr=rnd(17); snow=''.join(circ(rr.uniform(0,W),rr.uniform(0,H),rr.uniform(2,6),fill='#fff',opacity=f(rr.uniform(.5,.95))) for _ in range(220))
    snowman=C2(0,-60,60,'#F7F6F2')+C2(0,-150,44,'#F7F6F2')+C2(0,-222,32,'#F7F6F2')+path('M0 -222 L36 -214 L0 -208Z',fill='#F2853A')+circ(-10,-232,4,fill='#22252D')+circ(10,-232,4,fill='#22252D')+rect(-30,-270,60,16,fill='#22252D')+rect(-20,-310,40,44,fill='#22252D')
    return g(s,id='landscape')+g(p+T(snowman,500,960),id='props')+g(snow,id='snowfall')+g(EN.vignette(),id='lighting')
def C2(x,y,r,c): return circ(x,y,r,fill=c,stroke='#C9D4E0',stroke_width=3)
def rainy_street():
    s=EN.street('night')
    rr=rnd(19); rain=''.join(line([x,y],[x-10,y+40],stroke='#9FC4E8',stroke_width=2,opacity=f(rr.uniform(.3,.7))) for x,y in ((rr.uniform(0,W+200),rr.uniform(-40,H)) for _ in range(420)))
    pud=''.join(ell(x,y,w,10,fill='#9FC4E8',opacity='.25') for x,y,w in ((300,1000,140),(900,1040,200),(1500,990,160)))
    return g(s,id='street')+g(pud,id='puddles')+g(rain,id='rain')
def tehran(mode='night'):
    s=rect(0,0,W,H,fill=sky(mode))+(stars(100,8,360)+T(PR.moon(),1650,140,.7) if mode=='night' else T(PR.sun(),1650,150,.7)+T(PR.cloud(),300,160))
    mcol='#3A4466' if mode=='night' else '#8A9AB8'
    s+=path(f'M0 600 L180 420 L320 520 L520 330 L700 470 L900 360 L1100 480 L1300 340 L1500 460 L1700 380 L1920 520 L1920 700 L0 700Z',fill=mcol)
    s+=path(f'M520 330 L470 380 L500 376 L530 396 L560 372 L580 380Z M1300 340 L1250 392 L1290 384 L1320 404 L1350 380Z',fill='#F3F6FA',opacity='.9')
    rr=rnd(55); bcol='#151D36' if mode=='night' else '#A9BFD3'
    for i in range(40):
        bw=rr.uniform(40,100); bh=rr.uniform(80,300); bx=i*50-20
        s+=rect(bx,800-bh,bw,bh,fill=bcol)
        if mode=='night': s+=''.join(rect(bx+6+(k%3)*13,800-bh+10+(k//3)*22,6,9,fill='#FFD98A',opacity='.8') for k in range(12) if rr.random()>.55)
    tc='#20294A' if mode=='night' else '#7A8AA8'
    milad=path('M-14 0 L-10 -380 L10 -380 L14 0Z',fill=tc)+path('M-60 -380 Q-70 -420 -40 -440 L40 -440 Q70 -420 60 -380Z',fill=tc)+rect(-48,-470,96,30,rx=10,fill=tc)+path('M-4 -470 L-2 -600 L2 -600 L4 -470Z',fill=tc)
    if mode=='night': milad+=rect(-56,-420,112,8,fill='#7FC6E8',opacity='.9')+circ(0,-600,6,fill='#E2493B')
    azadi=path('M-150 0 Q-140 -160 -60 -220 L-40 -300 L40 -300 L60 -220 Q140 -160 150 0 L90 0 Q80 -110 0 -150 Q-80 -110 -90 0Z',fill='#C9B48A' if mode=='day' else '#5A5070',stroke=dark('#C9B48A',.4),stroke_width=3)
    s+=T(milad,620,800)+T(azadi,1340,820,.9)
    s+=rect(0,800,W,280,fill='#2A2D35' if mode=='night' else '#5A606C')+''.join(rect(x,930,100,10,fill='#E8E4D8',opacity='.6') for x in range(40,W,200))
    p=T(PV.taxi(mode=='night'),500,1060,.8)+T(PV.city_bus(mode=='night') if hasattr(PV,'city_bus') else PV.bus(night=mode=='night'),1350,1060,.7)
    return g(s,id='skyline')+g(p,id='street')+g((EN.night_overlay(.15) if mode=='night' else '')+EN.vignette(),id='lighting')
def podcast_studio():
    s=EN.wall('plain','#2A2F44')+EN.floor('carpet','#3A3550')
    for i in range(6):
        for k in range(3): s+=PR3(160+i*120,160+k*120,100,100,['#3A3F5A','#4A3F6A'][(i+k)%2],rx=10,k=.3)
    s+=neon('ON AIR',1450,260,'#FF4A3D',110)
    p=T(PR.desk(500),700,FL)+T(PH.podcast_mic(),860,FL-200,.6)+T(PH.podcast_mic(),1080,FL-200,.6)+T(PR.laptop(),980,FL-200,.6)+T(PH.ring_light(),1500,FL,.9)+T(PH.camera_tripod(),1700,FL,1.1)+T(PR.office_chair(),640,FL,.9)+T(PR.plant(),150,FL,.9)
    return g(s,id='room')+g(p,id='gear')+g(EN.vignette(),id='lighting')
def kids_bedroom(mode='day'):
    s=EN.wall('dots','#9FC4E8' if mode=='day' else '#2A3A5A')+EN.floor('wood','#B8854E')+EN.baseboard('#F7F3EA')
    s+=T(PR.window(300,320,mode),1260,560)+''.join(path(f'M{x} {y} l6 12 l13 2 l-10 9 l3 13 l-12 -7 l-12 7 l3 -13 l-10 -9 l13 -2Z',fill='#FFE07A',opacity='.8') for x,y in ((200,140),(500,90),(820,170),(1600,120),(1780,260)))
    p=T(PB.bed_kids_car('made'),160,FL)+T(PH.globe(),900,FL,.7)+T(PR.rug('#F2A6B8'),960,FL+80,.8)+T(PW.cat_sleep('#F2A65A'),1000,FL+60,.6)
    try:
        import props2 as P2; p+=T(P2.teddy_bear(),1600,FL,.9)
    except Exception: pass
    return g(s,id='room')+g(p,id='furniture')+g((EN.night_overlay(.4) if mode=='night' else '')+EN.vignette(),id='lighting')
def bedroom_modern(mode='night'):
    s=EN.wall('plain','#3A3F4E' if mode=='night' else '#D9D4CC')+EN.floor('wood','#6E5A48')+window_city(1080,140,640,500,'night' if mode=='night' else 'day')
    p=T(PB.bed_platform('messy',blanket='#5A8A7A',head='#C9B79A'),160,FL)+T(PR.nightstand(),760,FL)+T(PR.lamp(mode=='night'),760,FL-140)+T(PR.plant(),1800,FL,1.1)+T(PR.rug('#8A93A3'),1200,FL+90,.9)
    return g(s,id='room')+g(p,id='furniture')+g((EN.night_overlay(.3) if mode=='night' else '')+EN.vignette(),id='lighting')
def balcony_night():
    s=rect(0,0,W,H,fill='url(#skyNight)')+stars(80,23,420)+T(PR.moon(),1600,150,.7)
    rr=rnd(29)
    for i in range(36):
        bw=rr.uniform(50,110); bh=rr.uniform(140,420); bx=i*56-20
        s+=rect(bx,760-bh,bw,bh,fill='#151D36')+''.join(rect(bx+6+(k%3)*14,760-bh+12+(k//3)*24,6,10,fill='#FFD98A',opacity='.85') for k in range(14) if rr.random()>.55)
    s+=rect(0,760,W,320,fill='#2A2D35')+rect(0,740,W,20,fill='#5A606C')+''.join(rect(x,620,8,140,fill='#5A606C') for x in range(0,W,60))+rect(0,610,W,16,fill='#7A808C')
    p=T(PR.chair_wood('#5A606C'),700,1000,.9)+T(PR.table(220),900,1000,.8)+T(PH.tea_glass(),920,1000-140,.6)+T(PR.plant(),200,1000,1)+T(PR.plant('cactus'),1700,1000,.9)
    return g(s,id='view')+g(p,id='balcony')+g(EN.vignette(),id='lighting')
def concert_stage():
    s=rect(0,0,W,H,fill='#0B0D16')
    for x,c in ((300,'#FF4FA0'),(800,'#3FC0F0'),(1300,'#F2C230'),(1700,'#7C5CD6')): s+=path(f'M{x-20} 0 L{x+20} 0 L{x+260} 760 L{x-260} 760Z',fill=c,opacity='.14')+ell(x,10,40,20,fill=c)
    s+=rect(0,760,W,120,fill='#22252D')+rect(0,756,W,8,fill='#3A3E47')
    p=T(PH.drum_kit(),960,760,1.2)+T(PH.amp(),300,760,1)+T(PH.amp(),1620,760,1)+T(PH.mic_stand(),620,760,1)+T(PH.mic_stand(),1300,760,1)
    crowd=''.join(circ(x,1020-((x*13)%30),46,fill='#05060A')+rect(x-50,1020-((x*13)%30),100,120,fill='#05060A') for x in range(40,W,90))+''.join(path(f'M{x} 980 l-10 -110 l14 0Z',fill='#05060A') for x in range(80,W,260))
    return g(s,id='stage')+g(p,id='band_gear')+g(crowd,id='crowd')
def meeting_room():
    s=EN.wall('plain','#C9D4DE')+EN.floor('carpet','#5A6476')+window_city(1300,140,520,420,'day')
    p=T(PH.projector_screen(),620,FL-60,1)+T(PR.table(900),180,FL+60)+''.join(T(PR.office_chair(),x,FL+60,.8,flip=x>600) for x in (260,460,860,1060))+T(PR.laptop(),400,FL+60-170,.7)+T(PH.water_cooler(),1800,FL,.8)+T(PR.plant(),1240,FL,.9)
    return g(s,id='room')+g(p,id='furniture')+g(EN.vignette(),id='lighting')
def persian_living_room(mode='day'):
    s=EN.wall('wallpaper','#C9A27A' if mode=='day' else '#5A4030')+EN.floor('wood','#6E4A32')
    s+=T(PR.window(300,340,'day' if mode=='day' else 'night',curtain=.7),980,560)
    rug=E3()+''
    s+=g(rug,transform=f'translate(960 {FL+110})')
    cushions=''.join(T(PR3(-110,-180,220,180,c,rx=40)+path('M-80 -150 Q0 -90 80 -150 M-80 -40 Q0 -100 80 -40',fill='none',stroke='#F2C230',stroke_width=4),x,FL) for x,c in ((220,'#8A1F2A'),(470,'#2F4A7A'),(1460,'#2F4A7A'),(1710,'#8A1F2A')))
    p=cushions+T(PH.samovar(),960,FL+30,.9)+T(PH.tea_glass(),820,FL+60,.5)+T(PH.tea_glass(),1100,FL+60,.5)+T(PH.fruit_bowl(),720,FL+70,.6)+T(PR.picture_frame(),600,360,1)+T(PR.plant(),1850,FL,.8)
    return g(s,id='room')+g(p,id='furniture')+g((EN.night_overlay(.3)+ell(960,700,500,300,fill='url(#warmPool)') if mode=='night' else '')+EN.vignette(),id='lighting')
def E3():
    s=ell(0,0,700,120,fill='#8A1F2A',stroke='#5A1018',stroke_width=4)+ell(0,0,620,100,fill='none',stroke='#F2C230',stroke_width=6)+ell(0,0,520,80,fill='#2F4A7A')+ell(0,0,300,50,fill='#8A1F2A')+ell(0,0,140,24,fill='#F2C230',opacity='.8')
    for i in range(16): a=i/16*2*math.pi; s+=circ(math.cos(a)*580,math.sin(a)*90,8,fill='#F7F3EA')
    return s
def kitchen_modern(mode='day'):
    s=EN.wall('tiles','#E6E9EE' if mode=='day' else '#3A3F4E',y1=FL)+EN.floor('wood','#8A6A4E')+T(PR.window(300,260,'day' if mode=='day' else 'night'),960,480)
    p=T(PH.fridge_double(),200,FL)+T(PH.oven_range(),560,FL)+T(PH.kitchen_sink(),1100,FL)+T(PH.microwave(),1100,FL-260,.8)+T(PH.coffee_machine(),1460,FL-216,.6)
    p+=PR3(1340,FL-216,560,216,'#5A8A9A',rx=4)+PR3(1330,FL-232,580,22,'#E8DCC6',rx=4,k=.35)+T(PH.coffee_machine(),1480,FL-232,.6)+T(PH.kettle(),1640,FL-232,.6)+T(PH.fruit_bowl(),1800,FL-232,.6)
    return g(s,id='room')+g(p,id='appliances')+g((EN.night_overlay(.35) if mode=='night' else '')+EN.vignette(),id='lighting')
def bathroom_tub():
    s=EN.wall('tiles','#BFE0E8')+EN.floor('checker','#3A3E47')
    p=T(PH.bathtub(True),600,FL)+T(PH.toilet(),1260,FL)+T(PH.sink_vanity(),1620,FL)+T(PR.mirror(),1620,FL-460,.8)+T(PH.towel_rack(),1000,FL-300)+T(PH.rubber_duck(),460,FL-240,.4)+T(PH.toilet_paper(),1400,FL-180,.7)
    return g(s,id='room')+g(p,id='fixtures')+g(EN.vignette(),id='lighting')
def bus_stop_scene(mode='day'):
    s=EN.street(mode)
    return s+g(T(PW.bus_stop(),700,860,1)+T(PV.bus(night=mode=='night'),1400,1050,.8),id='bus_stop')
def parking_lot(mode='day'):
    s=rect(0,0,W,H,fill=sky(mode))+(stars(60,6,400) if mode=='night' else T(PR.cloud(),400,150))
    s+=rect(0,560,W,520,fill='#4A4D55' if mode=='day' else '#22252D')+''.join(path(f'M{x} 600 L{x+(x-960)*.4} 1080',stroke='#F7F6F2',stroke_width=6,opacity='.8') for x in range(0,W+1,240))
    s+=rect(0,540,W,30,fill='#7A808C')
    p=T(PV.suv('#F3F4F6',mode=='night'),360,820,.7)+T(PV.hatchback('#F2A65A',mode=='night'),850,820,.7)+T(PV.sedan('#2A2D35',mode=='night'),1600,1020,.85)+T(PR.street_lamp(mode=='night'),1300,600,.9)+T(PW.parking_meter(),200,1000,.8)
    return g(s,id='lot')+g(p,id='cars')+g((EN.night_overlay(.2) if mode=='night' else '')+EN.vignette(),id='lighting')
def cafe_street_tehran(): return tehran('day')
ENVS3={
 'gym':gym,'hospital_room':hospital_room,'supermarket':supermarket,'metro_station':metro,'beach_day':lambda: beach('day'),'beach_sunset':lambda: beach('sunset'),
 'forest_day':lambda: forest('day'),'forest_camp_night':lambda: forest('night'),'mountains':mountains,'mountains_snow':lambda: mountains(True),'desert':desert,'airport_gate':airport,
 'library':library,'restaurant':restaurant,'school_hallway':school_hallway,'tattoo_studio':tattoo_studio,'garage':garage,'highway_day':lambda: highway('day'),'highway_night':lambda: highway('night'),
 'snow_park':snow_park,'rainy_street_night':rainy_street,'tehran_skyline_day':lambda: tehran('day'),'tehran_skyline_night':lambda: tehran('night'),'podcast_studio':podcast_studio,
 'kids_bedroom_day':lambda: kids_bedroom('day'),'kids_bedroom_night':lambda: kids_bedroom('night'),'bedroom_modern_night':lambda: bedroom_modern('night'),'bedroom_modern_day':lambda: bedroom_modern('day'),
 'balcony_night':balcony_night,'concert_stage':concert_stage,'meeting_room':meeting_room,'persian_living_room_day':lambda: persian_living_room('day'),'persian_living_room_night':lambda: persian_living_room('night'),
 'kitchen_modern_day':lambda: kitchen_modern('day'),'kitchen_modern_night':lambda: kitchen_modern('night'),'bathroom_tub':bathroom_tub,'bus_stop_day':lambda: bus_stop_scene('day'),'bus_stop_night':lambda: bus_stop_scene('night'),
 'parking_lot_day':lambda: parking_lot('day'),'parking_lot_night':lambda: parking_lot('night'),
}
