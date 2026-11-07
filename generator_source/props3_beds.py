from p3base import *
# all beds: side elevation, head at the left, origin = floor at x=0 (left end), y=0
def bedding(x0,x1,top,state='made',blanket='#3F5A8C',pillow='#E6E9F0',sheet='#D9DEE8',pillows=1,deco=None):
    s=R(x0,top,x1-x0,34,sheet,rx=14,k=.4)+rect(x0+4,top+22,x1-x0-8,8,fill='#000',opacity='.1')
    for i in range(pillows):
        px=x0+12+i*26
        s+=path(f'M{px} {top} C{px-8} {top-46} {px+130} {top-52} {px+136} {top-6} C{px+140} {top+12} {px+4} {top+14} {px} {top}Z',**S(dark(pillow,.06*i),.42))+hi(f'M{px+18} {top-24} Q{px+66} {top-42} {px+116} {top-26}','#fff','.6')
    if deco: s+=path(f'M{x0+70} {top-2} C{x0+60} {top-40} {x0+150} {top-44} {x0+158} {top-4}Z',**S(deco,.45))+circ(x0+112,top-20,4,fill=dark(deco,.3))
    if state=='made':
        bx=x0+150
        s+=path(f'M{bx} {top-4} L{x1+8} {top-4} L{x1+12} {top+52} Q{(bx+x1)/2} {top+60} {bx-4} {top+50}Z',**S(blanket,.5))
        s+=path(f'M{bx} {top-4} L{x1+8} {top-4} L{x1+8} {top+12} L{bx-2} {top+12}Z',fill=light(blanket,.25))
        s+=hi(f'M{bx+70} {top+18} Q{bx+80} {top+34} {bx+74} {top+48} M{bx+150} {top+18} Q{bx+160} {top+34} {bx+154} {top+48}',dark(blanket,.25),'.6',3)
    elif state=='messy':
        pts=[[x0+140,top-20],[x0+200,top-40],[x0+262,top-18],[x0+320,top-46],[x0+380,top-16],[x1+12,top+8]]
        s+=path(smooth(pts,False)+f'L{x1+14} {top+56} Q{(x0+x1)*.6} {top+64} {x0+130} {top+52} Q{x0+112} {top+20} {x0+140} {top-20}Z',**S(blanket,.5))
        for x in (x0+210,x0+290,x0+360): s+=hi(f'M{x} {top-18} Q{x+18} {top+16} {x+6} {top+48}',dark(blanket,.25),'.7',4)
        s+=hi(smooth(pts,False),light(blanket,.3),'.6',3)
    elif state=='occupied':
        s+=path(f'M{x0+110} {top-2} C{x0+140} {top-100} {x0+320} {top-100} {x0+372} {top-20} C{x0+400} {top-10} {x1+10} {top-6} {x1+12} {top+12} L{x1+14} {top+56} Q{(x0+x1)*.6} {top+64} {x0+100} {top+52} Q{x0+86} {top+26} {x0+110} {top-2}Z',**S(blanket,.5))
        s+=hi(f'M{x0+160} {top-60} Q{x0+240} {top-100} {x0+330} {top-50}',light(blanket,.3),'.6',4)+hi(f'M{x0+250} {top-70} Q{x0+270} {top} {x0+258} {top+48}',dark(blanket,.25),'.6',4)
        s+=path(f'M{x0+60} {top-38} Q{x0+70} {top-62} {x0+100} {top-58} Q{x0+124} {top-50} {x0+118} {top-24}Z',fill='#3A2A22',stroke='#22170f',stroke_width=2)
    elif state=='bare':
        s+=''.join(circ(x,top+16,2.4,fill=dark(sheet,.25)) for x in range(x0+40,x1-20,46))
    return s
def bed_platform(state='made',w=460,frame='#5C6470',blanket='#C8573E',head='#8A93A3'):
    s=R(-10,-220,34,220,head,rx=10)+R(-6,-212,26,180,light(head,.08),rx=8,k=.3)
    for y in (-180,-140,-100): s+=ln(f'M-4 {y} L18 {y}',dark(head,.25),1.6,'.6')
    s+=R(0,-62,w,40,frame,rx=6)+R(18,-22,w-36,22,dark(frame,.35),rx=3)
    s+=R(4,-112,w-8,56,'#EEF0F4',rx=16,k=.35)+hi(f'M20 -96 L{w-20} -96','#000','.08',3)
    s+=bedding(4,w-4,-128,state,blanket,'#F2F3F6','#E6E9F0',pillows=2)
    return s
def bed_king(state='made',w=600,blanket='#E8DCC6',head='#6E5A8A'):
    s=path(f'M-30 0 L-30 -280 Q-30 -320 10 -320 L60 -320 Q100 -320 100 -280 L100 -120 L-30 -120Z',**S(head))
    s=R(-36,-330,60,330,head,rx=22)
    for y in range(-300,-130,34):
        for x in (-20,8): s+=circ(x,y+(17 if x>0 else 0),3,fill=dark(head,.35))
    s+=R(0,-70,w,50,WOOD_D,rx=6)+R(w-10,-150,30,150,head,rx=12)+R(10,-20,20,20,dark(WOOD_D,.3))+R(w-40,-20,20,20,dark(WOOD_D,.3))
    s+=R(4,-126,w-8,60,'#F4F1EA',rx=18,k=.35)
    s+=bedding(4,w-4,-142,state,blanket,'#F7F4EC','#EFEAE0',pillows=3,deco='#C8577A')
    return s
def bed_bunk(state='made'):
    s=''
    for x in (-12,452): s+=R(x,-520,26,520,WOOD,rx=6)+R(x-2,-530,30,14,light(WOOD,.15),rx=6)
    for y,st,bl in ((-60,state,'#3F5A8C'),(-320,'made' if state!='bare' else 'bare','#C8573E')):
        s+=R(0,y-10,466,26,WOOD_L,rx=5)
        s+=bedding(10,456,y-50,st,bl,'#E6E9F0','#D9DEE8')
    s+=R(14,-430,430,14,WOOD,rx=5)+''.join(R(x,-430,8,64,WOOD,rx=3) for x in (60,140,220))
    lx=360
    s+=ln(f'M{lx} -322 L{lx+30} -60 M{lx+60} -322 L{lx+90} -60',WOOD_D,8)
    for k in range(1,5): y=-322+k*52; s+=ln(f'M{lx+k*6} {y} L{lx+60+k*6} {y}',WOOD_D,6)
    return s
def bed_canopy(state='made',w=520,drape='#C8A6D9',blanket='#8A4F5E'):
    s=''
    for x in (-14,w-6): s+=R(x,-560,22,560,WOOD_D,rx=6)+C(x+11,-566,12,WOOD_D)
    s+=R(-20,-560,w+34,20,WOOD_D,rx=6)
    s+=R(-8,-260,24,200,WOOD,rx=8)
    s+=R(0,-70,w,48,WOOD,rx=6)+R(4,-122,w-8,56,'#F4F1EA',rx=16,k=.35)+bedding(4,w-4,-138,state,blanket,'#F7F4EC','#EFEAE0',pillows=2)
    for x0,dirx in ((-6,1),(w-4,-1)):
        d=f'M{x0} -540 Q{x0+dirx*90} -520 {x0+dirx*70} -400 Q{x0+dirx*40} -250 {x0+dirx*60} -150 L{x0} -150Z'
        s+=path(d,**S(drape,.45),opacity='.92')+ln(f'M{x0+dirx*20} -530 Q{x0+dirx*44} -400 {x0+dirx*24} -170',dark(drape,.2),2.4,'.7')
    s+=path(f'M-20 -540 Q{w/2} -470 {w+14} -540Z',**S(drape,.45),opacity='.95')
    return s
def bed_hospital(state='made',w=470):
    s=''
    for x in (20,w-40): s+=R(x,-110,16,90,METAL,rx=4)+C(x+8,-14,14,'#3A3E47')+C(x+8,-14,5,METAL)
    s+=R(0,-130,w,26,'#D8DEE6',rx=8)
    s+=path(f'M10 -150 L150 -150 L120 -290 Q118 -300 106 -296 L20 -250 Q6 -240 10 -224Z',**S('#E6EBF2',.35))
    s+=R(140,-180,w-150,52,'#E6EBF2',rx=14,k=.35)
    s+=path(f'M30 -262 C26 -300 140 -320 124 -280 C118 -260 40 -244 30 -262Z',**S('#F7F8FA',.4))
    if state!='bare': s+=path(f'M150 -196 L{w+6} -196 L{w+10} -140 Q{w*.6} -132 146 -140Z',**S('#9FC4E8',.5))+path(f'M150 -196 L{w+6} -196 L{w+6} -182 L150 -182Z',fill='#F7F8FA')
    s+=R(-10,-300,20,180,'#C9CED6',rx=6)+R(w-10,-230,20,110,'#C9CED6',rx=6)
    s+=ln(f'M190 -212 L{w-40} -212 M190 -212 L190 -170 M{w-40} -212 L{w-40} -170 M260 -212 L260 -176 M330 -212 L330 -176',METAL_D,4)
    s+=R(-80,-560,8,560,METAL,rx=3)+R(-104,-14,56,10,METAL_D,rx=4)+path('M-76 -540 l-22 0 M-76 -540 l22 0',stroke=METAL_D,stroke_width=4)+R(-100,-540,40,62,'#DDEFFC',rx=10,k=.4,opacity='.9')+ln('M-80 -478 Q-60 -380 40 -250','#9FC4E8',2.4)
    return s
def bed_crib(state='made',w=300):
    s=R(-6,-300,22,300,'#F2EDE4',rx=6,k=.35)+R(w-16,-300,22,300,'#F2EDE4',rx=6,k=.35)
    s+=R(0,-80,w,20,'#F2EDE4',rx=4,k=.35)+R(10,-120,w-20,44,'#BFE0D4',rx=12,k=.4)
    if state!='bare': s+=path(f'M60 -118 C70 -170 200 -170 240 -120Z',**S('#F2A6B8',.45))+''.join(circ(x,-138,4,fill='#fff',opacity='.8') for x in (100,140,180))
    s+=R(0,-290,w,16,'#F2EDE4',rx=6,k=.35)
    for x in range(26,w-10,28): s+=R(x,-280,8,200,'#F2EDE4',rx=3,k=.35)
    s+=R(0,-16,w,10,'#E3DCCC',rx=3)
    # mobile
    s+=ln(f'M{w-30} -300 L{w-30} -400 L{w/2} -400 L{w/2} -380',METAL_D,3)
    for i,(x,c) in enumerate(((w/2-50,'#FFE07A'),(w/2,'#F2A6B8'),(w/2+50,'#9FC4E8'))):
        s+=ln(f'M{w/2} -380 L{x} -368 L{x} -340',METAL_D,1.6)+(path(f'M{x} -340 l6 12 l13 2 l-10 9 l3 13 l-12 -7 l-12 7 l3 -13 l-10 -9 l13 -2Z',**S(c,.4,1.6)) if i==0 else C(x,-330,12,c,.4))
    return s
def bed_futon(state='made',w=440):
    s=R(0,-26,w,26,'#C9A16E',rx=4)+R(4,-74,w-8,52,'#E8DCC6',rx=22,k=.4)
    for x in range(40,w,60): s+=circ(x,-48,3,fill='#B8AE9C')
    s+=bedding(4,w-4,-88,state,'#5A8A7A','#F2EDE4','#E8DCC6')
    return s
def bed_metal(state='made',w=440,c='#3A3E47'):
    s=ln('M0 0 L0 -270 M30 0 L30 -270',c,8)+path('M0 -270 Q15 -300 30 -270',fill='none',stroke=c,stroke_width=8)
    for y in (-240,-200,-160): s+=ln(f'M0 {y} Q15 {y-14} 30 {y}',c,4)
    s+=C(15,-286,7,'#C9A23B')
    s+=ln(f'M{w} 0 L{w} -170 M{w-30} 0 L{w-30} -170',c,8)+C(w-15,-178,7,'#C9A23B')
    s+=R(0,-70,w,16,c,rx=4)+R(4,-122,w-8,54,'#F4F1EA',rx=16,k=.35)+bedding(4,w-4,-138,state,'#B8463A','#F7F4EC','#EFEAE0')
    return s
def bed_kids_car(state='made',w=480,c='#D6453A'):
    s=path(f'M-20 -40 L-20 -170 Q-20 -200 10 -200 L120 -200 Q150 -200 170 -160 L{w-80} -150 Q{w-20} -146 {w} -100 L{w+10} -40Z',**S(c))
    s+=path('M30 -196 L110 -196 Q130 -196 142 -168 L30 -168Z',fill=GLASS,stroke=dark(c,.5),stroke_width=2)
    s+=bedding(150,w-24,-150,state,'#3F5A8C','#F2F3F6','#E6E9F0') if state!='bare' else ''
    s+=path(f'M-20 -60 L{w+10} -60 L{w+10} -40 L-20 -40Z',fill=dark(c,.2))
    for x in (70,w-90): s+=C(x,-40,44,'#22252D')+C(x,-40,20,'#C9CED6')+C(x,-40,7,'#5A606C')
    s+=R(w-14,-108,22,16,'#FFE7A8',rx=5)+path(f'M190 -110 L{w-120} -110',stroke='#fff',stroke_width=10)+text('7',230,-74,size=40,fill='#fff',weight=900,anchor='middle')
    return s
def bed_loft(state='made',w=460):
    s=''
    for x in (-10,w-14): s+=R(x,-560,24,560,'#4A5260',rx=5)
    s+=R(0,-390,w,22,'#4A5260',rx=5)+R(6,-440,w-12,52,'#EEF0F4',rx=14,k=.35)+bedding(6,w-6,-456,state,'#5A8A7A','#F2F3F6','#E6E9F0')
    s+=R(0,-520,w,12,'#4A5260',rx=4)+''.join(R(x,-520,8,70,'#4A5260',rx=3) for x in (80,180,280))
    s+=R(20,-200,w-60,18,WOOD_L,rx=4)+R(30,-182,14,182,WOOD_D)+R(w-70,-182,14,182,WOOD_D)
    s+=R(120,-290,120,82,'#2A2D35',rx=6)+R(128,-282,104,64,'#3B5B8A',rx=3)+R(170,-208,20,8,'#2A2D35')
    s+=ln('M330 -230 L330 -200 M318 -230 L342 -230',METAL_D,5)+path('M300 -260 Q330 -300 360 -260 Z',**S('#F2C230'))
    return s
def hammock(state='made',w=500):
    s=ln(f'M0 0 L60 -300 L120 0 M{w} 0 L{w-60} -300 L{w-120} 0',WOOD_D,12)
    s+=ln(f'M60 -290 L120 -200 M{w-60} -290 L{w-120} -200',INK,2.4)
    s+=path(f'M110 -210 Q{w/2} -60 {w-110} -210 Q{w/2} -110 110 -210Z',**S('#E9A23B'))
    for x in range(140,w-120,26): s+=ln(f'M{x} {-200+((x-w/2)**2)/(w*1.6)*0+20} L{x} -170',dark('#E9A23B',.3),1.4,'.4')
    if state=='occupied': s+=path(f'M170 -175 Q{w/2} -90 {w-160} -176 Q{w/2} -150 170 -175Z',**S('#3F5A8C'))+C(150,-198,22,'#ECE4D6',k=.4)
    return s
def sleeping_bag(state='made',w=380):
    s=path(f'M0 -10 Q-10 -70 50 -76 L{w-30} -66 Q{w+10} -50 {w} -10Z',**S('#3E8A6E'))+path(f'M0 -10 Q-6 -60 40 -70 L120 -66 L110 -12Z',fill='#F2C230',stroke=dark('#F2C230',.5),stroke_width=2)
    s+=ln(f'M120 -66 L{w-30} -60',dark('#3E8A6E',.4),2.4,'.7')+''.join(ln(f'M{x} -64 L{x} -10',dark('#3E8A6E',.3),2,'.5') for x in range(170,w-30,60))
    if state=='occupied': s+=C(50,-56,24,'#ECE4D6',k=.4)+path('M28 -66 Q46 -88 72 -70Z',fill='#3A2A22')
    return s
def air_mattress(state='made',w=420):
    s=R(0,-80,w,80,'#5A8ACF',rx=30)+''.join(ln(f'M{x} -70 L{x} -10',dark('#5A8ACF',.25),3,'.6') for x in range(60,w,60))+hi(f'M30 -66 L{w-30} -66','#fff','.5',4)
    s+=R(w-16,-50,18,16,'#2F333B',rx=4)
    if state!='bare': s+=bedding(10,w-10,-96,state,'#E2725B','#F2F3F6','#E6E9F0')
    return s
BEDS=dict(platform=bed_platform,king_tufted=bed_king,bunk=bed_bunk,canopy=bed_canopy,hospital=bed_hospital,crib=bed_crib,futon=bed_futon,metal_vintage=bed_metal,kids_car=bed_kids_car,loft_desk=bed_loft,hammock=hammock,sleeping_bag=sleeping_bag,air_mattress=air_mattress)
def items():
    out={}
    for k,fn in BEDS.items():
        states=('made','messy','occupied','bare') if k in('platform','king_tufted','metal_vintage','futon','canopy','bunk') else (('made','occupied') if k in('hammock','sleeping_bag') else ('made','bare'))
        for st in states: out[f'bed_{k}_{st}']=fn(st)
    out['bed_platform_made_green']=bed_platform('made',blanket='#5A8A7A',head='#C9B79A')
    out['bed_king_tufted_made_navy']=bed_king('made',blanket='#3F5A8C',head='#3A4258')
    return out
