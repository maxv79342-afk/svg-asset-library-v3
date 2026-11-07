from p3base import *
# side views facing right (+x), origin = ground under the middle of the vehicle
def wheel(x,r=40,rim='#C9CED6',spokes=5):
    s=C(x,-r,r,'#22252D',.4)+C(x,-r,r*.62,'#3A3E47',.4)+C(x,-r,r*.48,rim,.5)
    for i in range(spokes):
        a=i*360/spokes; s+=ln(f'M{P([x,-r])}L{P(add([x,-r],mul(dirv(a),r*.44)))}',dark(rim,.35),3)
    return s+C(x,-r,r*.14,dark(rim,.3),.5)
def beams(x,y,dirx=1,L=520):
    return path(f'M{x} {y-8} L{x+dirx*L} {y-70} L{x+dirx*L} {y+90} L{x} {y+8}Z',fill='#FFF3C4',opacity='.22')+ell(x,y,18,12,fill='#FFF8DC',opacity='.9')
def tail_glow(x,y): return ell(x,y,34,24,fill='#FF4A3D',opacity='.28')+ell(x,y,10,8,fill='#FF6A5E')
def car_body(L=420,H=150,roof=(.28,.72),cab=95,col='#D6453A',hood=40,trunk=30,cl=28,wr=40,glass=GLASS,kind='sedan',night=False,stripe=None):
    x0=-L/2; x1=L/2; y0=-cl; yb=-cl-H+cab   # belt line
    r0=x0+L*roof[0]; r1=x0+L*roof[1]; yt=yb-cab
    if kind=='hatch': pts=[[x0+6,y0],[x0,yb+30],[x0+8,yb],[r0-30,yb-4],[r0+10,yt],[r1-10,yt],[x1-L*.12,yb-6],[x1-6,yb+10],[x1,y0]]
    elif kind=='suv': pts=[[x0+4,y0],[x0,yt+20],[x0+14,yt],[r1-6,yt],[x1-L*.16,yb-4],[x1-4,yb+12],[x1,y0]]
    elif kind=='sports': pts=[[x0+8,y0],[x0,yb+20],[x0+20,yb],[r0,yb-6],[r0+40,yt],[r1-40,yt],[x1-L*.26,yb-2],[x1-8,yb+18],[x1,y0]]
    elif kind=='beetle': pts=[[x0+10,y0],[x0,yb+10],[x0+40,yb-30],[r0+10,yt+10],[(r0+r1)/2,yt-6],[r1+10,yt+16],[x1-30,yb-10],[x1-4,yb+20],[x1,y0]]
    elif kind=='convertible': pts=[[x0+6,y0],[x0,yb+18],[x0+12,yb],[x1-L*.22,yb-4],[x1-8,yb+14],[x1,y0]]
    else: pts=[[x0+6,y0],[x0,yb+22],[x0+10,yb],[r0-24,yb-6],[r0+16,yt],[r1-12,yt],[r1+30,yb-6],[x1-14,yb+2],[x1-2,yb+18],[x1,y0]]
    d=smooth(pts,True,.35) if kind in('beetle',) else 'M'+'L'.join(P(p) for p in pts)+'Z'
    s=path(d,**S(col),stroke_linejoin_='round')
    s=path(d,**S(col))
    s+=shade(f'M{x0+4} {y0} L{x1} {y0} L{x1} {y0-18} L{x0+2} {y0-18}Z','.18')
    if kind not in('convertible',):
        # windows
        if kind=='suv': wp=[[x0+28,yb-4],[x0+30,yt+10],[r1-10,yt+10],[x1-L*.18,yb-6]]
        elif kind=='hatch': wp=[[r0-12,yb-6],[r0+16,yt+10],[r1-14,yt+10],[x1-L*.14,yb-6]]
        elif kind=='beetle': wp=[[r0+6,yb-6],[r0+20,yt+20],[r1,yt+24],[r1+20,yb-6]]
        elif kind=='sports': wp=[[r0+6,yb-8],[r0+44,yt+10],[r1-40,yt+10],[x1-L*.3,yb-6]]
        else: wp=[[r0-14,yb-6],[r0+20,yt+10],[r1-14,yt+10],[r1+20,yb-6]]
        s+=path('M'+'L'.join(P(p) for p in wp)+'Z',fill=glass,stroke=dark(col,.5),stroke_width=2.4,stroke_linejoin='round')
        midx=(wp[1][0]+wp[2][0])/2+(10 if kind!='suv' else 0)
        s+=ln(f'M{midx} {wp[1][1]} L{midx+(6 if kind!="suv" else 0)} {yb-6}',col,8)
        if kind=='suv': s+=ln(f'M{midx+90} {yt+10} L{midx+90} {yb-6}',col,8)
        s+=hi(f'M{wp[1][0]+16} {wp[1][1]+8} L{wp[1][0]+4} {yb-12}','#fff','.6',4)
        if night: s+=path('M'+'L'.join(P(p) for p in wp)+'Z',fill='#0B1430',opacity='.55')
    else:
        s+=path(f'M{r0} {yb} L{r0+30} {yb-50} L{r0+36} {yb-50} L{r0+12} {yb}Z',fill=glass,stroke=dark(col,.5),stroke_width=2)
        s+=R(r0+60,yb-34,46,34,'#3A2E26',rx=8)+R(r0+130,yb-30,40,30,'#3A2E26',rx=8)
    # door seams, handles, mirror
    dx=(r0+r1)/2 if kind!='suv' else x0+L*.45
    s+=ln(f'M{dx} {yb-4} L{dx} {y0-8}',dark(col,.4),2,'.7')
    if kind not in('sports','beetle','hatch'): s+=ln(f'M{r0-20} {yb-4} Q{r0-30} {y0-30} {r0-10} {y0-8}',dark(col,.4),2,'.6')
    s+=R(dx+12,yb+14,22,6,dark(col,.25),rx=3,k=.4)+R(r0-50,yb+14,22,6,dark(col,.25),rx=3,k=.4)
    s+=path(f'M{r0-10} {yb-4} l-14 -14 l-12 2 l2 12Z',**S(col))
    if stripe: s+=path(f'M{x0+6} {yb+34} L{x1-6} {yb+34} L{x1-4} {yb+50} L{x0+4} {yb+50}Z',fill=stripe,opacity='.95')
    s+=hi(f'M{x0+30} {yb+8} L{x1-40} {yb+8}','#fff','.35',3)
    # lights + bumpers
    s+=R(x1-18,yb+12,20,16,'#FFE7A8',rx=5,k=.45)+R(x0-2,yb+12,16,18,'#E2493B',rx=4,k=.45)
    s+=R(x1-30,y0-14,36,14,'#3A3E47',rx=6)+R(x0-6,y0-14,36,14,'#3A3E47',rx=6)
    wx=(x0+wr+38, x1-wr-44)
    for x in wx: s+=path(f'M{x-wr-10} {y0} A{wr+10} {wr+10} 0 0 1 {x+wr+10} {y0}Z',fill='#14161B')
    for x in wx: s+=wheel(x,wr)
    if night: s=beams(x1+2,yb+20)+s+tail_glow(x0+6,yb+21)
    return s
def sedan(c='#D6453A',night=False): return car_body(col=c,night=night)
def hatchback(c='#3FA3A0',night=False): return car_body(L=360,col=c,kind='hatch',roof=(.3,.82),night=night)
def suv(c='#3A4258',night=False): return car_body(L=460,H=190,cab=110,col=c,kind='suv',cl=34,wr=46,night=night)
def sports(c='#F2C230',night=False): return car_body(L=460,H=118,cab=62,col=c,kind='sports',cl=22,wr=38,roof=(.32,.66),night=night)
def convertible(c='#C8577A',night=False): return car_body(L=430,H=110,cab=40,col=c,kind='convertible',roof=(.3,.7),night=night)
def beetle(c='#7FB3A6',night=False): return car_body(L=360,H=160,cab=96,col=c,kind='beetle',roof=(.3,.66),night=night)
def taxi(night=False):
    s=car_body(col='#F2C230',stripe='#22252D',night=night)
    s+=R(-36,-208,72,26,'#F7F6F2',rx=6)+text('TAXI',0,-189,size=18,fill='#22252D',weight=900,anchor='middle')
    for x in range(-150,170,24): s+=rect(x,-74,12,8,fill='#F7F6F2',opacity='.9')
    return s
def police(night=False):
    s=car_body(col='#F3F4F6',stripe='#2C3E66',night=night)
    s+=R(-46,-200,44,16,'#E2493B',rx=4)+R(2,-200,44,16,'#3E7AD6',rx=4)+text('POLICE',30,-70,size=22,fill='#F7F6F2',weight=900,anchor='middle')
    if night: s=ell(-24,-192,90,40,fill='#E2493B',opacity='.3')+ell(24,-192,90,40,fill='#3E7AD6',opacity='.3')+s
    return s
def pickup(c='#4E7A5A',night=False):
    s=path('M-260 -40 L-260 -150 L-20 -150 L-10 -270 Q-6 -282 10 -282 L120 -282 Q140 -282 152 -262 L196 -170 L250 -160 Q266 -154 266 -130 L268 -40Z',**S(c))
    s+=path('M8 -268 L118 -268 Q132 -268 140 -252 L176 -176 L8 -176Z',fill=GLASS,stroke=dark(c,.5),stroke_width=2.4)+ln('M70 -268 L74 -176',c,8)
    s+=hi('M24 -254 L14 -190','#fff','.6',4)+path('M-250 -150 L-30 -150 L-30 -136 L-250 -136Z',fill=dark(c,.3))
    s+=shade('M-256 -40 L268 -40 L268 -58 L-258 -58Z','.18')+ln('M-20 -150 L-20 -50',dark(c,.4),2,'.7')+R(30,-160,22,6,dark(c,.25),rx=3)
    s+=R(250,-150,18,18,'#FFE7A8',rx=5)+R(-266,-140,14,24,'#E2493B',rx=4)+R(-270,-54,40,14,'#3A3E47',rx=6)+R(236,-54,40,14,'#3A3E47',rx=6)
    for x in (-160,170): s+=path(f'M{x-58} -40 A58 58 0 0 1 {x+58} -40Z',fill='#14161B')+wheel(x,46)
    if night: s=beams(268,-140)+s+tail_glow(-262,-128)
    return s
def van(c='#F3F4F6',night=False,stripe=None,txt=None,tc='#D6453A'):
    L=520; x0=-L/2; x1=L/2
    s=path(f'M{x0} -34 L{x0} -250 Q{x0} -270 {x0+20} -270 L{x1-120} -270 Q{x1-90} -270 {x1-60} -200 L{x1-6} -150 Q{x1+4} -140 {x1} -120 L{x1} -34Z',**S(c))
    s+=path(f'M{x1-110} -256 L{x1-80} -256 L{x1-40} -190 L{x1-110} -190Z',fill=GLASS,stroke=dark(c,.5),stroke_width=2.4)
    s+=R(x0+40,-250,120,70,GLASS,rx=6,k=.5)+ln(f'M{x1-130} -260 L{x1-130} -50 M{x0+200} -260 L{x0+200} -50',dark(c,.35),2,'.7')
    if stripe: s+=rect(x0,-150,L,22,fill=stripe)
    if txt: s+=text(txt,x0+250,-90,size=30,fill=tc,weight=900,anchor='middle')
    s+=R(x1-18,-150,20,18,'#FFE7A8',rx=5)+R(x0-4,-150,14,26,'#E2493B',rx=4)+R(x1-30,-48,36,14,'#3A3E47',rx=6)+R(x0-6,-48,36,14,'#3A3E47',rx=6)
    for x in (x0+90,x1-100): s+=path(f'M{x-54} -34 A54 54 0 0 1 {x+54} -34Z',fill='#14161B')+wheel(x,44)
    if night: s=beams(x1+2,-140)+s+tail_glow(x0+2,-138)
    return s
def ambulance(night=False):
    s=van('#F7F6F2',night,stripe='#E2493B')
    s+=path('M-150 -230 h20 v20 h20 v20 h-20 v20 h-20 v-20 h-20 v-20 h20Z',fill='#E2493B')+R(-60,-282,50,14,'#E2493B',rx=4)+R(-6,-282,50,14,'#3E7AD6',rx=4)
    s+=text('AMBULANCE',40,-160,size=24,fill='#E2493B',weight=900,anchor='middle')
    return s
def ice_cream_truck(night=False):
    s=van('#F2A6B8',night,stripe='#9FD3E8',txt='ICE CREAM',tc='#7A2F4A')
    s+=R(-200,-230,170,60,'#3A2E26',rx=8)+path('M-120 -296 L-100 -270 L-140 -270Z',**S('#F2C27A'))+C(-120,-306,16,'#F7F3EA')+C(-110,-318,10,'#E88AA8')
    return s
def bus(c='#2F6FB8',night=False,school=False):
    if school: c='#F2B530'
    L=820; x0=-L/2; x1=L/2
    s=R(x0,-330,L,296,c,rx=26)+rect(x0,-120,L,10,fill=dark(c,.25))
    for i in range(7): s+=R(x0+40+i*100,-300,80,90,GLASS,rx=8,k=.5)+(rect(x0+40+i*100,-300,80,90,fill='#0B1430',opacity='.5',rx=8) if night else '')
    s+=R(x1-90,-300,70,240,GLASS,rx=8,k=.5)+ln(f'M{x1-55} -300 L{x1-55} -60',dark(c,.5),2.4)
    s+=R(x1-6,-110,16,22,'#FFE7A8',rx=4)+R(x0-8,-110,14,26,'#E2493B',rx=4)+R(x0+20,-330,L-40,16,light(c,.2),rx=6,k=.3)
    if school: s+=text('SCHOOL BUS',x0+330,-160,size=34,fill='#22252D',weight=900,anchor='middle')
    else: s+=R(x1-220,-360,150,30,'#22252D',rx=5)+text('42  CITY',x1-145,-338,size=20,fill='#FFB13B',weight=800,anchor='middle')
    for x in (x0+140,x1-170): s+=path(f'M{x-56} -34 A56 56 0 0 1 {x+56} -34Z',fill='#14161B')+wheel(x,46)
    if night: s=beams(x1+8,-100,L=600)+s+tail_glow(x0+0,-98)
    return s
def box_truck(c='#F3F4F6',night=False,txt='DELIVERY',cab='#3E6A8A'):
    s=R(-360,-340,480,300,c,rx=10)+text(txt,-120,-180,size=40,fill=cab,weight=900,anchor='middle')+ln('M-330 -90 L90 -90',dark(c,.2),3)
    s+=path('M120 -40 L120 -250 L220 -250 Q250 -250 270 -200 L300 -150 L300 -40Z',**S(cab))+path('M140 -236 L215 -236 Q236 -236 250 -200 L262 -170 L140 -170Z',fill=GLASS,stroke=dark(cab,.5),stroke_width=2.4)
    s+=R(286,-140,18,18,'#FFE7A8',rx=4)+R(-366,-120,12,26,'#E2493B',rx=3)
    for x in (-280,-150,220): s+=path(f'M{x-54} -38 A54 54 0 0 1 {x+54} -38Z',fill='#14161B')+wheel(x,44)
    if night: s=beams(304,-130)+s
    return s
def fire_truck(night=False):
    s=box_truck('#D6453A',night,txt='',cab='#C23A30')
    s+=R(-360,-380,460,22,METAL,rx=6)+''.join(ln(f'M{x} -380 L{x} -358',METAL_D,4) for x in range(-340,100,40))
    s+=text('FIRE 12',-120,-200,size=46,fill='#F7F6F2',weight=900,anchor='middle')+R(-330,-140,420,16,'#F2C230',rx=3)
    for i in range(6): s+=R(-340+i*72,-300,56,60,dark('#D6453A',.15),rx=6,k=.5)
    s+=R(150,-270,30,14,'#E2493B',rx=4)+R(184,-270,30,14,'#3E7AD6',rx=4)
    return s
def jeep(c='#7A8A4E',night=False):
    s=path('M-200 -40 L-200 -150 L-150 -150 L-140 -260 L60 -260 L80 -150 L200 -140 L210 -40Z',**S(c))
    s+=path('M-130 -246 L-40 -246 L-40 -160 L-136 -160Z M-24 -246 L52 -246 L66 -160 L-24 -160Z',fill=GLASS,stroke=dark(c,.5),stroke_width=2.4)
    s+=R(-232,-180,40,90,'#22252D',rx=12)+C(-212,-135,30,'#22252D')+R(196,-130,16,20,'#FFE7A8',rx=5)+R(-210,-56,430,14,'#3A3E47',rx=5)
    for x in (-120,130): s+=path(f'M{x-56} -36 A56 56 0 0 1 {x+56} -36Z',fill='#14161B')+wheel(x,48,'#5A606C')
    if night: s=beams(212,-120)+s
    return s
def motorcycle(c='#D6453A',night=False):
    s=wheel(-130,46,'#5A606C',8)+wheel(130,46,'#5A606C',8)
    s+=ln('M-130 -46 L-40 -110 L60 -110 L130 -46 M60 -110 L100 -170 M-40 -110 L-20 -60 L40 -60',INK,8)
    s+=path('M-30 -150 Q30 -170 70 -140 L60 -110 L-40 -110Z',**S(c))+path('M-120 -130 L-40 -130 L-30 -112 L-110 -110Z',**S('#22252D'))
    s+=ln('M100 -170 L80 -190 M100 -170 L120 -176',INK,6)+R(108,-160,20,16,'#FFE7A8',rx=5)+path('M-60 -60 L-170 -70 L-176 -56 L-70 -48Z',fill='#C9CED6',stroke=METAL_D,stroke_width=2)
    if night: s=beams(126,-152,L=380)+s
    return s
def scooter_vespa(c='#9FD3C8',night=False):
    s=wheel(-112,34,'#C9CED6',5)+wheel(118,34,'#C9CED6',5)
    s+=path('M-170 -64 Q-176 -150 -90 -156 L-20 -150 Q0 -120 -10 -80 L80 -80 Q100 -84 104 -110 L112 -236 L132 -236 L134 -110 Q140 -70 160 -60 L160 -48 L-160 -48 Q-172 -52 -170 -64Z',**S(c))
    s+=path('M-150 -150 Q-90 -178 -20 -158 L-24 -146 L-146 -140Z',**S('#3A2E26'))+hi('M-150 -110 Q-120 -140 -70 -140','#fff','.5',4)
    s+=ln('M122 -236 L92 -250 M122 -236 L152 -244',INK,6)+C(140,-206,10,'#FFE7A8')+R(-176,-120,14,18,'#E2493B',rx=4)
    s+=path('M96 -60 Q118 -110 140 -60Z',fill='#14161B')
    if night: s=beams(150,-206,L=360)+s
    return s
def kick_scooter(c='#3A3E47'):
    return wheel(-80,16,'#9AA3AF',4)+wheel(80,16,'#9AA3AF',4)+ln('M-90 -22 L70 -22 L80 -16 M70 -22 L50 -200 M30 -200 L72 -200',c,8)+C(52,-150,6,'#7FE0A8')
def bicycle_road(c='#2F6FB8'):
    s=''
    for x in (-95,95): s+=circ(x,-66,64,fill='none',stroke='#22252D',stroke_width=7)+circ(x,-66,58,fill='none',stroke='#9AA3AF',stroke_width=1.5)+C(x,-66,6,METAL_D)
    s+=ln('M-95 -66 L-20 -66 L50 -150 L-40 -150 L-95 -66 M-20 -66 L-48 -170 M50 -150 L95 -66 M50 -150 L46 -184',c,7)+R(-70,-182,46,10,'#22252D',rx=5)+path('M30 -186 Q60 -196 64 -174',fill='none',stroke='#22252D',stroke_width=6,stroke_linecap='round')
    return s
def car_front(c='#D6453A',night=False,taxi_=False):
    s=path('M-170 -40 L-170 -130 Q-170 -150 -150 -156 L-120 -230 Q-112 -250 -90 -250 L90 -250 Q112 -250 120 -230 L150 -156 Q170 -150 170 -130 L170 -40Z',**S(c))
    s+=path('M-104 -236 L104 -236 L130 -164 L-130 -164Z',fill=GLASS,stroke=dark(c,.5),stroke_width=2.4)+hi('M-80 -226 L-100 -176','#fff','.6',5)
    s+=R(-90,-120,180,40,'#22252D',rx=10)+''.join(ln(f'M{x} -116 L{x} -84',METAL_D,3) for x in range(-80,90,20))
    for sx in (-1,1): s+=E(sx*130,-118,26,18,'#FFF3C4' if night else '#FFE7A8')+R(sx*150-(18 if sx>0 else 0),-34,18,36,'#22252D',rx=6)+path(f'M{sx*170} -150 l{sx*24} -6 l0 18 l{-sx*24} 0Z',**S(c))
    s+=R(-176,-70,352,26,'#3A3E47',rx=8)+R(-30,-66,60,18,'#F3F1EC',rx=3)
    if taxi_: s+=R(-40,-276,80,26,'#F7F6F2',rx=6)+text('TAXI',0,-257,size=18,fill='#22252D',weight=900,anchor='middle')
    if night: s=ell(-130,-118,90,60,fill='#FFF3C4',opacity='.25')+ell(130,-118,90,60,fill='#FFF3C4',opacity='.25')+s
    return s
def car_back(c='#3E6A8A'):
    s=path('M-170 -40 L-170 -140 Q-170 -156 -150 -160 L-116 -228 Q-108 -246 -88 -246 L88 -246 Q108 -246 116 -228 L150 -160 Q170 -156 170 -140 L170 -40Z',**S(c))
    s+=path('M-100 -232 L100 -232 L124 -170 L-124 -170Z',fill=GLASS,stroke=dark(c,.5),stroke_width=2.4)
    for sx in (-1,1): s+=R(sx*120-24,-140,48,22,'#E2493B',rx=5)+R(sx*150-(18 if sx>0 else 0),-34,18,36,'#22252D',rx=6)
    return s+R(-50,-110,100,26,'#F3F1EC',rx=3)+text('8DE 214',0,-91,size=16,fill='#22252D',weight=800,anchor='middle')+R(-176,-70,352,24,'#3A3E47',rx=8)
def items():
    o={}
    for nm,fn,cols in (('sedan',sedan,('#D6453A','#3E6A8A','#F3F4F6','#2A2D35')),('hatchback',hatchback,('#3FA3A0','#F2A65A','#7C5CD6')),('suv',suv,('#3A4258','#F3F4F6','#8A1F2A')),
                       ('sports',sports,('#F2C230','#D6453A','#22252D')),('convertible',convertible,('#C8577A','#9FD3E8')),('beetle',beetle,('#7FB3A6','#F2C27A')),('pickup',pickup,('#4E7A5A','#B8463A')),('jeep',jeep,('#7A8A4E','#C9B48A')),
                       ('motorcycle',motorcycle,('#D6453A','#22252D')),('scooter_vespa',scooter_vespa,('#9FD3C8','#F2A6B8'))):
        for i,c in enumerate(cols): o[f'{nm}_{i+1}']=fn(c)
        o[f'{nm}_night']=fn(cols[0],night=True)
    for nm,fn in (('taxi',taxi),('police_car',police),('ambulance',ambulance),('ice_cream_truck',ice_cream_truck),('city_bus',bus),('delivery_truck',box_truck),('fire_truck',fire_truck)):
        o[nm]=fn(); o[nm+'_night']=fn(night=True)
    o['school_bus']=bus(school=True); o['van']=van(); o['van_blue']=van('#3E6A8A')
    o['kick_scooter']=kick_scooter(); o['bicycle_road']=bicycle_road(); o['bicycle_red']=bicycle_road('#D6453A')
    o['car_front_red']=car_front(); o['car_front_blue']=car_front('#3E6A8A'); o['car_front_night']=car_front('#F3F4F6',True); o['taxi_front']=car_front('#F2C230',taxi_=True)
    o['car_back_blue']=car_back(); o['car_back_red']=car_back('#D6453A')
    return o
