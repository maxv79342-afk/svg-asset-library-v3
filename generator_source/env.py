from sv import *
import props as PR
W,H=1920,1080; FL=860
def T(svg,x,y,s=1,r=0,flip=False): return g(svg,transform=f'translate({f(x)} {f(y)})'+(f' rotate({r})' if r else '')+(f' scale({f(-s)} {f(s)})' if flip else (f' scale({f(s)})' if s!=1 else '')))
# ---------- walls & floors ----------
def wall(kind='plain',c='#3A4258',y1=FL):
    s=rect(0,0,W,y1,fill=c)
    if kind=='stripes':
        for x in range(0,W,60): s+=rect(x,0,28,y1,fill=light(c,.05))
    elif kind=='dots':
        rr=rnd(1)
        for yy in range(30,y1,60):
            for xx in range(30+(yy//60%2)*30,W,60): s+=circ(xx,yy,3,fill=light(c,.08))
    elif kind=='brick':
        for i,yy in enumerate(range(0,y1,44)):
            for xx in range(-(i%2)*60,W,120): s+=rect(xx+3,yy+3,114,38,rx=3,fill=mixc(c,'#000',rnd(xx*7+yy).uniform(0,.12)))
    elif kind=='tiles':
        for yy in range(0,y1,70):
            for xx in range(0,W,70): s+=rect(xx+2,yy+2,66,66,rx=4,fill=light(c,.04))
    elif kind=='panels':
        s+=rect(0,y1-300,W,300,fill=dark(c,.12))+rect(0,y1-306,W,12,fill=light(c,.1))
        for xx in range(40,W,200): s+=rect(xx,y1-270,160,230,rx=4,fill='none',stroke=dark(c,.25),stroke_width=3)
    elif kind=='wallpaper':
        for yy in range(0,y1,90):
            for xx in range(0,W,90):
                ox=45 if (yy//90)%2 else 0
                s+=path(f'M{xx+ox} {yy+20} q12 25 0 50 q-12 -25 0 -50Z',fill=light(c,.07))
    s+=rect(0,0,W,y1,fill='url(#wallShade)')
    return s
def floor(kind='wood',c='#4A3A30',y0=FL):
    s=rect(0,y0,W,H-y0,fill=c)
    if kind=='wood':
        for i,yy in enumerate(range(y0,H,36)):
            s+=rect(0,yy,W,2,fill=dark(c,.25))
            for xx in range(((i*137)%240)-240,W,240): s+=rect(xx,yy,2,36,fill=dark(c,.2))
    elif kind=='tiles':
        for yy in range(y0,H,60):
            s+=rect(0,yy,W,2,fill=dark(c,.2))
        for xx in range(0,W,120): s+=line([xx,y0],[xx+(xx-W/2)*.35,H],stroke=dark(c,.2),stroke_width=2)
    elif kind=='carpet':
        rr=rnd(5)
        for i in range(600): s+=circ(rr.uniform(0,W),rr.uniform(y0,H),rr.uniform(1,2.2),fill=dark(c,.15),opacity='.5')
    elif kind=='checker':
        for j,yy in enumerate(range(y0,H,55)):
            for i,xx in enumerate(range(0,W,110)):
                if (i+j)%2: s+=rect(xx,yy,110,55,fill=light(c,.2))
    s+=rect(0,y0,W,10,fill='#000',opacity='.25')+rect(0,y0-14,W,14,fill=dark(c,.1))
    return s
def baseboard(c='#2A2F3E',y=FL): return rect(0,y-26,W,26,fill=c)+rect(0,y-26,W,4,fill=light(c,.15))
def night_overlay(a=.55,c='#05081A'): return rect(0,0,W,H,fill=c,opacity=f(a))
def vignette(): return rect(0,0,W,H,fill='url(#vignette)')
DEFS=lg('wallShade',[(0,'#000',.25),(.5,'#000',0),(1,'#000',.15)])+rg('vignette',[(0,'#000',0),(.7,'#000',0),(1,'#000',.38)],r=.75)+rg('lampGlow',[(0,'#FFE2A8',.45),(1,'#FFE2A8',0)])+rg('warmPool',[(0,'#FFD9A0',.35),(1,'#FFD9A0',0)])+rg('moonPool',[(0,'#AFC8FF',.22),(1,'#AFC8FF',0)])+lg('skyDay',[(0,'#7DB8EC'),(1,'#D9EEFA')])+lg('skyNight',[(0,'#070B1E'),(1,'#1E2C55')])+lg('skySunset',[(0,'#2E2350'),(.55,'#B5576A'),(1,'#F2A65A')])+rg('spot',[(0,'#3A4466',1),(1,'#121626',1)])+rg('screenGlow',[(0,'#A9CBFF',.6),(.5,'#6F9FE8',.2),(1,'#6F9FE8',0)])
# ---------- rooms ----------
def bedroom(mode='night',curtains_closed=False):
    wc='#6A7A9A' if mode=='day' else '#2A3148'
    bg=wall('stripes',wc)+baseboard()+floor('wood','#5A4536')
    win=T(PR.window(330,360,'day' if mode=='day' else 'night',curtain=(0 if curtains_closed else .75)),960,560)
    furn=T(PR.poster('DREAM BIG'),380,420)+T(PR.wall_shelf(),640,330)+win
    furn+=T(PR.bed(470,messy=True),150,FL)+T(PR.nightstand(),700,FL)+T(PR.lamp(on=mode!='day'),700,FL-140)+T(PR.alarm_clock(),760,FL-140,.32)
    furn+=T(PR.door(),1560,FL)+T(PR.desk(330),1260,FL)+T(PR.laptop(False),1230,FL-200,.8)+T(PR.book_stack(4,True),1340,FL-200,.5)+T(PR.office_chair(),1200,FL,.85,flip=True)
    furn+=T(PR.rug(),560,FL+120)+T(PR.trash_bin(),1440,FL+40,.6)+T(PR.crumpled_paper(),1500,FL+60)+T(PR.crumpled_paper(),1380,FL+90,.8)
    fx=''
    if mode=='night':
        fx+=night_overlay(.5)+ell(700,FL-220,320,260,fill='url(#lampGlow)')
        if not curtains_closed: fx+=path('M820 230 L1100 230 L1000 1080 L380 1080Z',fill='#AFC8FF',opacity='.07')
    elif mode=='dark':
        fx+=night_overlay(.78)
    fx+=vignette()
    return g(bg,id='background')+g(furn,id='furniture')+g(fx,id='lighting')
def living_room(mode='day'):
    bg=wall('wallpaper','#5C6E62' if mode=='day' else '#3A4640')+baseboard('#2E3A34')+floor('wood','#6B5240')
    furn=T(PR.window(300,340,'day' if mode=='day' else 'sunset',curtain=.8),360,600)+T(PR.picture_frame('family'),980,380)+T(PR.picture_frame('landscape'),1180,400,.8)+T(PR.ceiling_lamp(mode!='day'),980,90,1)
    furn+=T(PR.sofa('#6E5A8A',520),1060,FL)+T(PR.plant(),760,FL,.9)+T(PR.tv(),1640,FL-150,.7)+R_tvstand()+T(PR.rug('#A8634E'),1060,FL+110)+T(PR.table(240,'#7A5A43'),1080,FL+150,.6)+T(PR.mug(),1080,FL+50,.6)+T(PR.armchair(),340,FL)+T(PR.bookshelf(),1880,FL,.9)
    fx=(night_overlay(.35,'#1A0E22') + ell(980,300,500,300,fill='url(#warmPool)') if mode!='day' else '')+vignette()
    return g(bg,id='background')+g(furn,id='furniture')+g(fx,id='lighting')
def R_tvstand(): return T(PR.R(-200,-150,400,150,'#4A3A30',rx=6)+PR.R(-180,-120,170,90,'#3A2E26',rx=4)+PR.R(10,-120,170,90,'#3A2E26',rx=4),1640,FL)
def kitchen(mode='day'):
    bg=wall('tiles','#D6D2C4' if mode=='day' else '#6E6A60',y1=FL)+floor('checker','#3A3E47')
    upper=''.join(PR.R(x,140,170,220,'#5E7A8A',rx=6)+PR.R(x+70,320,30,8,'#C9CED6',rx=4) for x in (140,320,500,1140,1320))
    furn=upper+T(PR.window(380,300,'day' if mode=='day' else 'night'),900,560)+T(PR.kitchen_counter(760),520,FL)+T(PR.kitchen_counter(500),1300,FL)+T(PR.fridge(),1700,FL)+T(PR.stove_pot(),1300,FL-220,.9)+T(PR.mug(),300,FL-220,.6)+T(PR.wall_clock(9,15),900,120,.6)+T(PR.pizza_box(),620,FL-220,.6)+T(PR.plant('cactus'),1090,FL-260,.4)
    fx=(night_overlay(.45)+ell(900,300,600,300,fill='url(#warmPool)') if mode!='day' else '')+vignette()
    return g(bg,id='background')+g(furn,id='furniture')+g(fx,id='lighting')
def office(mode='day',chairs=True):
    bg=wall('panels','#C7CDD6' if mode=='day' else '#4A5262')+floor('carpet','#5A6476')
    sky='url(#skyDay)' if mode=='day' else 'url(#skyNight)'
    win=rect(160,90,1600,420,fill=sky)
    rr=rnd(9)
    for i in range(24):
        bw=rr.uniform(40,90); bh=rr.uniform(120,330); bx=160+i*70
        win+=rect(bx,510-bh,bw,bh,fill='#9DB7CF' if mode=='day' else '#121A30')
        if mode!='day':
            for k in range(10):
                if rr.random()>.55: win+=rect(bx+6+(k%3)*14,510-bh+12+(k//3)*24,6,10,fill='#FFD98A',opacity='.85')
    for x in range(160,1761,200): win+=rect(x-6,90,12,420,fill='#5A606C')
    win+=rect(150,80,1620,440,fill='none',stroke='#5A606C',stroke_width=14)
    furn=win
    for x in (380,960,1540):
        furn+=T(PR.desk(420),x,FL)+T(PR.monitor('#3B5B8A' if mode=='day' else '#5B7BB0'),x-40,FL-200-62,.55)+T(PR.mug(),x+140,FL-200,.45)+(T(PR.office_chair(),x+20,FL,.85) if chairs else '')
    furn+=T(PR.plant(),1830,FL,.9)+T(PR.plant(),80,FL,.8)
    fx=(night_overlay(.4,'#060A1E') if mode!='day' else '')+vignette()
    return g(bg,id='background')+g(furn,id='furniture')+g(fx,id='lighting')
def home_desk(mode='night'):
    bg=wall('plain','#2E3550')+floor('wood','#4A3A30')
    furn=T(PR.window(300,320,'night' if mode=='night' else 'day'),1520,520)+T(PR.wall_shelf(),640,300)+T(PR.sticky_note('TODO'),700,520,.6)+T(PR.sticky_note('PAY RENT','#F2A65A'),800,500,.55)+T(PR.sticky_note('call mom','#8FC9F5'),620,430,.5)
    furn+=T(PR.desk(780),860,FL)+T(PR.monitor('#5B7BB0'),860,FL-200-62)+T(PR.keyboard(),860,FL-200,.8)+T(PR.desk_lamp(mode=='night'),540,FL-200,.9)+T(PR.mug(steam=False),1120,FL-200,.6)+T(PR.book_stack(5),1180,FL-200,.6)+T(PR.office_chair(),860,FL,1.05)
    fx=(night_overlay(.45)+ell(860,500,500,320,fill='url(#screenGlow)') if mode=='night' else '')+vignette()
    return g(bg,id='background')+g(furn,id='furniture')+g(fx,id='lighting')
def classroom():
    bg=wall('plain','#C9B99A')+floor('wood','#7A5A43')
    board=rect(360,140,1200,440,rx=8,fill='#2E4A3E',stroke='#6B4F3C',stroke_width=18)+text('Final exam  –  Monday',460,250,size=46,fill='#E8E4D8',family="'Caveat','Comic Sans MS',cursive",opacity='.9')+text('E = mc²',460,340,size=46,fill='#E8E4D8',family="'Caveat','Comic Sans MS',cursive",opacity='.8')+path('M1100 400 Q1200 300 1300 420 T1480 380',fill='none',stroke='#E8E4D8',stroke_width=4,opacity='.7')+rect(400,580,1120,16,fill='#6B4F3C')
    furn=board+T(PR.wall_clock(8,55),1720,140,.6)+T(PR.window(260,300,'day'),180,560)
    for x in (300,760,1220,1680):
        furn+=T(PR.table(300,'#B08A58'),x,FL+100,.9)+T(PR.chair_wood('#8A6A4A'),x-60,FL+100,.75)
    return g(bg,id='background')+g(furn,id='furniture')+g(vignette(),id='lighting')
def bathroom():
    bg=wall('tiles','#9FB8C4')+floor('tiles','#D6D2C4')
    furn=T(PR.mirror(),960,560)+PR.R(760,600,400,40,'#EDE8DC',rx=10)+PR.R(800,640,320,220,'#C9C3B8',rx=10)+ell(960,615,120,14,fill='#B9C6CF')+path('M960 600 L960 570 L1000 570',fill='none',stroke='#9AA3AF',stroke_width=10,stroke_linecap='round')
    furn+=PR.R(1400,420,420,440,'#EDE8DC',rx=20)+rect(1420,440,380,420,rx=14,fill='#B9CFE0',opacity='.4')+T(PR.plant('monstera'),300,FL,.9)+PR.R(140,560,200,40,'#EDE8DC',rx=6)
    furn+=T(PR.scale_weight(),620,FL+60,.9)
    return g(bg,id='background')+g(furn,id='furniture')+g(vignette(),id='lighting')
def cafe():
    bg=wall('brick','#7A4A3A')+floor('wood','#5A4232')
    furn=rect(160,120,700,420,fill='url(#skyDay)')+''.join(rect(160+i*175,120,8,420,fill='#2A2D35') for i in range(5))+rect(150,110,720,440,fill='none',stroke='#2A2D35',stroke_width=16)
    furn+=rect(1100,150,640,260,rx=10,fill='#22262E')+text('MENU',1420,215,size=44,fill='#F2D45A',weight=800,anchor='middle',family="'Bebas Neue',Oswald,Impact,sans-serif")+''.join(text(t,1150,270+i*40,size=24,fill='#E8E4D8',family="'Caveat','Comic Sans MS',cursive")+text(p_,1690,270+i*40,size=24,fill='#E8E4D8',anchor='end',family="'Caveat','Comic Sans MS',cursive") for i,(t,p_) in enumerate([('Espresso','3.00'),('Latte','4.50'),('Croissant','3.20')]))
    for x in (400,1100):
        furn+=T(PR.table(220,'#3A2E26'),x,FL+60,.9)+T(PR.chair_wood('#3A2E26'),x-200,FL+60,.8)+T(PR.chair_wood('#3A2E26'),x+200,FL+60,.8,flip=True)+T(PR.coffee_cup_togo(),x,FL+60-153,.4)
    furn+=''.join(T(PR.ceiling_lamp(True),x,60,.8) for x in (400,1100,1600))
    fx=ell(960,300,900,400,fill='url(#warmPool)')+vignette()
    return g(bg,id='background')+g(furn,id='furniture')+g(fx,id='lighting')
# ---------- exterior ----------
def house(c='#C9B79A',roof='#8A3E3A',lit=False,w=520):
    s=PR.R(-w/2,-380,w,380,c,rx=2)+path(f'M{-w/2-40} -370 L0 -600 L{w/2+40} -370Z',**PR.S(roof))+PR.R(w/4-30,-620,60,140,dark(roof,.2))
    for (x,y) in ((-w/2+60,-320),(w/2-170,-320),(-w/2+60,-170)):
        s+=PR.R(x,y,110,100,'#FFE2A0' if lit else '#9FC3DA',rx=3)+rect(x+53,y,4,100,fill=dark(c,.4))+rect(x,y+48,110,4,fill=dark(c,.4))+rect(x-8,y+100,126,12,fill=light(c,.2))
    s+=PR.R(w/2-160,-200,100,200,'#6B4F3C',rx=3)+circ(w/2-74,-100,6,fill='#D7B270')+circ(0,-470,34,fill='#FFE2A0' if lit else '#9FC3DA',stroke=dark(c,.4),stroke_width=4)
    s+=PR.R(-w/2-20,-12,w+40,12,dark(c,.3))
    return s
def street(mode='day'):
    sky='url(#skyDay)' if mode=='day' else ('url(#skySunset)' if mode=='sunset' else 'url(#skyNight)')
    bg=rect(0,0,W,H,fill=sky)
    rr=rnd(21)
    if mode=='night':
        for i in range(80): bg+=circ(rr.uniform(0,W),rr.uniform(0,420),rr.uniform(.8,2),fill='#fff',opacity=f(rr.uniform(.3,.9)))
        bg+=T(PR.moon(),1600,160,.9)
    elif mode=='day': bg+=T(PR.sun(),1640,170,.8)+T(PR.cloud(),400,200,.9)+T(PR.cloud(),1100,140,.7)
    far=''
    for i in range(28):
        bw=rr.uniform(60,130); bh=rr.uniform(180,480); bx=i*72-30
        col={'day':'#A9BFD3','night':'#151D36','sunset':'#5A3A5A'}[mode]
        far+=rect(bx,680-bh,bw,bh,fill=col)
        if mode!='day':
            for k in range(14):
                if rr.random()>.6: far+=rect(bx+8+(k%3)*18,680-bh+16+(k//3)*30,8,12,fill='#FFD98A',opacity='.8')
    near=''
    for i,(x,c,hgt) in enumerate(((0,'#B8735A',420),(330,'#8A9AA8',520),(640,'#C9A16E',380),(940,'#7A8A6E',470),(1250,'#A8634E',430),(1560,'#6E7A9A',500))):
        cc=c if mode=='day' else dark(c,.55)
        near+=PR.R(x,780-hgt,320,hgt,cc,rx=2)+PR.R(x-6,780-hgt-14,332,20,dark(cc,.2))
        for yy in range(780-hgt+40,700,100):
            for xx in (x+40,x+140,x+240):
                lit=mode!='day' and rnd(xx+yy).random()>.4
                near+=PR.R(xx,yy,50,64,'#FFD98A' if lit else ('#9FC3DA' if mode=='day' else '#1A2238'),rx=2)
        near+=PR.R(x+120,700,80,80,dark(cc,.35),rx=2) if i%2 else PR.R(x+30,690,260,90,'#2A2D35' if mode!='day' else '#3A3E47',rx=3)+(text(['BOOKS','CAFE','GYM'][i//2%3],x+160,750,size=30,fill='#F2D45A' if mode!='day' else '#E8E4D8',weight=800,anchor='middle',family="'Bebas Neue',Oswald,Impact,sans-serif") if i%2==0 else '')
    ground=rect(0,780,W,80,fill='#8D8A84' if mode=='day' else '#3A3A40')+''.join(rect(x,780,2,80,fill='#6E6B66' if mode=='day' else '#2A2A30') for x in range(0,W,120))+rect(0,860,W,220,fill='#3A3D44' if mode=='day' else '#1C1E24')+''.join(rect(x,965,90,10,fill='#E8E4D8',opacity='.7') for x in range(40,W,200))+rect(0,856,W,8,fill='#B5B2AA' if mode=='day' else '#4A4A50')
    props_=T(PR.street_lamp(mode!='day'),250,780)+T(PR.street_lamp(mode!='day'),1200,780)+T(PR.tree(),700,790,.7)+T(PR.tree(),1700,790,.75)+T(PR.bench(),980,790,.7)+T(PR.car('#3E6A8A'),1500,1020,.8)
    fx=(night_overlay(.25,'#05081A') if mode=='night' else '')+vignette()
    return g(bg+far,id='sky_far')+g(near+ground,id='street')+g(props_,id='props')+g(fx,id='lighting')
def house_exterior(mode='day'):
    sky={'day':'url(#skyDay)','night':'url(#skyNight)','sunset':'url(#skySunset)'}[mode]
    s=rect(0,0,W,H,fill=sky)
    if mode=='night': s+=T(PR.moon(),300,180)+T(PR.stars(),1100,200,2)
    else: s+=T(PR.sun(),300,180,.8)+T(PR.cloud(),1300,180)
    s+=path(f'M0 760 Q480 680 960 740 T1920 720 L1920 1080 L0 1080Z',fill='#6E9A5A' if mode=='day' else '#1E2E28')
    s+=rect(0,860,W,220,fill='#5E8A4E' if mode=='day' else '#18261F')
    hs=T(house('#D8C7A8','#8A3E3A',mode!='day'),960,860)+T(house('#A8B8C8','#3E4A66',mode!='day',400),380,860,.8)+T(house('#C8A8A0','#5A3E3A',mode!='day',420),1560,860,.8)
    hs+=T(PR.tree(),180,880,.9)+T(PR.tree('pine'),1300,880,.8)+T(PR.mailbox(),720,890,.8)+path('M1050 860 L1000 1080 L1160 1080 L1110 860Z',fill='#B5B2AA' if mode=='day' else '#3A3A40')
    for x in range(40,W,60): hs+=PR.R(x,840,12,60,'#F3EEE2' if mode=='day' else '#6E6A62',rx=2)
    hs+=rect(0,860,W,10,fill='#F3EEE2' if mode=='day' else '#6E6A62')
    fx=(night_overlay(.25)+ell(960,700,400,300,fill='url(#warmPool)') if mode=='night' else '')+vignette()
    return g(s,id='sky_ground')+g(hs,id='houses')+g(fx,id='lighting')
def park():
    s=rect(0,0,W,H,fill='url(#skyDay)')+T(PR.sun(),1600,160,.8)+T(PR.cloud(),500,180)+T(PR.cloud(),1100,240,.7)
    s+=path('M0 640 Q400 560 900 640 T1920 600 L1920 1080 L0 1080Z',fill='#8BBF6A')+path('M0 760 Q600 700 1200 760 T1920 740 L1920 1080 L0 1080Z',fill='#6EA855')
    s+=path('M700 1080 Q900 860 1300 760 L1400 760 Q1060 880 960 1080Z',fill='#D9C9A0')
    t=T(PR.tree(),240,800)+T(PR.tree('round','#5A9A50'),560,700,.6)+T(PR.tree('pine','#3E7A44'),1500,720,.7)+T(PR.tree(),1760,820,1.05)+T(PR.bench(),1200,860,.8)+T(PR.street_lamp(False),1000,820,.7)
    rr=rnd(3)
    for i in range(30): x,y=rr.uniform(0,W),rr.uniform(800,1060); t+=circ(x,y,5,fill=rr.choice(['#F2D45A','#E8708A','#FFFFFF']))+circ(x,y,2,fill='#C9963B')
    return g(s,id='sky_ground')+g(t,id='props')+g(vignette(),id='lighting')
def rooftop_night():
    s=rect(0,0,W,H,fill='url(#skyNight)')+T(PR.moon(),1500,170)+T(PR.stars(),700,220,2.4)
    rr=rnd(31)
    for layer,(col,base,hmin,hmax,lit) in enumerate((('#141C34',760,200,480,.25),('#0E1428',860,120,360,.4))):
        for i in range(32):
            bw=rr.uniform(50,120); bh=rr.uniform(hmin,hmax); bx=i*64-30
            s+=rect(bx,base-bh,bw,bh,fill=col)
            for k in range(16):
                if rr.random()<lit: s+=rect(bx+6+(k%3)*16,base-bh+14+(k//3)*28,7,11,fill='#FFD98A',opacity='.85')
    s+=rect(0,880,W,200,fill='#262A36')+rect(0,860,W,24,fill='#3A3F4E')
    s+=PR.R(1500,700,180,180,'#3A3F4E')+''.join(rect(1510,710+i*30,160,8,fill='#2A2E3A') for i in range(5))
    return g(s,id='background')+g(vignette(),id='lighting')
# ---------- abstract / talk backgrounds ----------
def void_spot(c1='#3A4466',c2='#121626'):
    id_=uid('sp')
    return f'<defs>{rg(id_,[(0,c1),(1,c2)],cy=.45,r=.75)}</defs>'+rect(0,0,W,H,fill=f'url(#{id_})')+ell(960,900,520,60,fill='#000',opacity='.25')
def void_dark(): return rect(0,0,W,H,fill='#07080C')+ell(960,540,900,520,fill='url(#moonPool)')
def void_gradient(a='#2E2350',b='#B5576A'):
    id_=uid('vg'); return f'<defs>{lg(id_,[(0,a),(1,b)])}</defs>'+rect(0,0,W,H,fill=f'url(#{id_})')
def void_grid(c='#F3EEE2'):
    s=rect(0,0,W,H,fill=c)
    for x in range(0,W,60): s+=line([x,0],[x,H],stroke=dark(c,.08),stroke_width=1.5)
    for y in range(0,H,60): s+=line([0,y],[W,y],stroke=dark(c,.08),stroke_width=1.5)
    return s
def void_paper():
    rr=rnd(2); s=rect(0,0,W,H,fill='#EFE7D6')
    for i in range(500): s+=circ(rr.uniform(0,W),rr.uniform(0,H),rr.uniform(.6,2),fill='#C9BFA8',opacity=f(rr.uniform(.2,.6)))
    return s
def void_split(): return rect(0,0,W/2,H,fill='#2A3148')+rect(W/2,0,W/2,H,fill='#E8D9B8')+rect(W/2-3,0,6,H,fill='#111')
ENVS={
 'bedroom_night':lambda: bedroom('night'),'bedroom_day':lambda: bedroom('day'),'bedroom_dark_curtains_closed':lambda: bedroom('dark',True),
 'living_room_day':lambda: living_room('day'),'living_room_evening':lambda: living_room('evening'),
 'kitchen_day':lambda: kitchen('day'),'kitchen_night':lambda: kitchen('night'),
 'office_day':lambda: office('day'),'office_night':lambda: office('night'),'home_desk_night':lambda: home_desk('night'),'home_desk_day':lambda: home_desk('day'),
 'classroom':classroom,'bathroom_mirror':bathroom,'cafe':cafe,
 'street_day':lambda: street('day'),'street_sunset':lambda: street('sunset'),'street_night':lambda: street('night'),
 'house_exterior_day':lambda: house_exterior('day'),'house_exterior_sunset':lambda: house_exterior('sunset'),'house_exterior_night':lambda: house_exterior('night'),
 'park_day':park,'rooftop_city_night':rooftop_night,
 'void_spotlight':void_spot,'void_dark':void_dark,'void_sunset_gradient':void_gradient,'void_grid_paper':void_grid,'void_paper':void_paper,'void_split_screen':void_split,
}
WALLS={f'wall_{k}':(lambda k=k,c=c: wall(k,c)+baseboard()) for k,c in (('plain','#3A4258'),('stripes','#3E4A66'),('dots','#5C6E62'),('brick','#7A4A3A'),('tiles','#9FB8C4'),('panels','#C7CDD6'),('wallpaper','#5C6E62'))}
FLOORS={f'floor_{k}':(lambda k=k,c=c: floor(k,c,y0=0)) for k,c in (('wood','#5A4536'),('tiles','#D6D2C4'),('carpet','#5A6476'),('checker','#3A3E47'))}
