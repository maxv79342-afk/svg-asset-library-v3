from sv import *
SW,SH=390,844
BG='#0E1118'; CARD='#1B2030'; TXT='#EEF1F7'; MUT='#8A93A8'; ACC='#4F8CFF'
def status(t='2:47',bat=.15,dark_=True):
    c=TXT if dark_ else '#111'
    s=text(t,34,34,size=16,fill=c,weight=700)
    s+=rect(SW/2-60,12,120,32,rx=16,fill='#000')
    bc='#E5484D' if bat<.2 else c
    s+=rect(SW-62,22,28,14,rx=4,fill='none',stroke=c,stroke_width=1.6,opacity='.8')+rect(SW-60,24,24*bat,10,rx=2,fill=bc)+rect(SW-33,26,2.5,6,rx=1,fill=c,opacity='.8')
    for i in range(4): s+=rect(SW-100+i*6,32-i*3,4,4+i*3,rx=1,fill=c,opacity='.85' if i<3 else '.3')
    return s
def avatar(x,y,r,c,initial=''):
    return circ(x,y,r,fill=c)+(text(initial,x,y+r*.36,size=r,fill='#fff',weight=700,anchor='middle') if initial else '')
def person_photo(x,y,w,h,bg1,bg2,skin='#ECE4D6',shirt='#C8573E',hair='#3A2A22',idx=0):
    id_=uid('ph'); s=f'<defs>{lg(id_,[(0,bg1),(1,bg2)])}<clipPath id="{id_}c"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="10"/></clipPath></defs>'
    cx=x+w/2; inner=rect(x,y,w,h,fill=f'url(#{id_})')
    inner+=path(f'M{f(cx-w*.32)} {f(y+h)} Q{f(cx-w*.3)} {f(y+h*.62)} {f(cx)} {f(y+h*.6)} Q{f(cx+w*.3)} {f(y+h*.62)} {f(cx+w*.32)} {f(y+h)}Z',fill=shirt)
    inner+=circ(cx,y+h*.42,w*.14,fill=skin,stroke='#8C8273',stroke_width=2)+path(f'M{f(cx-w*.14)} {f(y+h*.4)} A{f(w*.14)} {f(w*.14)} 0 0 1 {f(cx+w*.14)} {f(y+h*.4)}Z',fill=hair)
    inner+=path(f'M{f(cx-8)} {f(y+h*.47)} Q{f(cx)} {f(y+h*.5)} {f(cx+8)} {f(y+h*.47)}',fill='none',stroke='#4A3530',stroke_width=2.4,stroke_linecap='round')
    inner+=circ(cx-7,y+h*.42,2.4,fill='#221E1B')+circ(cx+7,y+h*.42,2.4,fill='#221E1B')
    return s+g(inner,clip_path=f'url(#{id_}c)')
def icon_heart(x,y,k=1,c='#FF3B5C',fillit=True):
    return g(path('M0 6 C-10 -2 -7 -10 0 -5 C7 -10 10 -2 0 6Z',fill=c if fillit else 'none',stroke=c,stroke_width=1.8),transform=f'translate({f(x)} {f(y)}) scale({k})')
def navbar(dark_=True):
    return rect(SW/2-68,SH-16,136,5,rx=2.5,fill=TXT if dark_ else '#111',opacity='.8')
# ---------- screens ----------
def scr_lock(notifs=True):
    id_=uid('lk')
    s=f'<defs>{lg(id_,[(0,"#2A2350"),(.6,"#4A2E5E"),(1,"#B5576A")])}</defs>'+rect(0,0,SW,SH,fill=f'url(#{id_})')
    s+=circ(300,640,160,fill='#F2A65A',opacity='.25')+path(f'M0 700 Q120 640 220 700 T{SW} 680 L{SW} {SH} L0 {SH}Z',fill='#1E1838',opacity='.8')
    s+=status('2:47',.12)
    s+=text('Wednesday, March 6',SW/2,120,size=18,fill=TXT,weight=500,anchor='middle',opacity='.85')
    s+=text('2:47',SW/2,210,size=96,fill=TXT,weight=700,anchor='middle')
    if notifs:
        items=[('#25D366','The Old Crew','Priya: Dinner this Friday!!'),('#E1306C','Instagram','sam_lifts posted a new story'),('#4F8CFF','Bank','Your balance is low: $0.00'),('#FF9F0A','Reminder','Assignment due TOMORROW')]
        for i,(c,a,b) in enumerate(items):
            y=280+i*86
            s+=rect(16,y,SW-32,74,rx=18,fill='#fff',opacity='.16')+rect(30,y+16,40,40,rx=10,fill=c)
            s+=text(a,84,y+32,size=15,fill=TXT,weight=700)+text(b,84,y+54,size=14,fill=TXT,opacity='.85')+text('now',SW-34,y+32,size=12,fill=TXT,anchor='end',opacity='.6')
    s+=circ(70,SH-90,24,fill='#fff',opacity='.18')+circ(SW-70,SH-90,24,fill='#fff',opacity='.18')
    return s+navbar()
APPS=[('Chat','#25D366'),('Photos','#F2B53A'),('Insta','grad'),('Mail','#4F8CFF'),('Bank','#2E7D5B'),('Maps','#5FB55A'),('Music','#FF3B5C'),('Video','#E5484D'),('Clock','#222'),('Notes','#F2D45A'),('Fitness','#B5E655'),('Settings','#8A93A8'),('Calendar','#fff'),('Shop','#FF9F0A'),('Games','#7B5CFF'),('Weather','#5AC8FA')]
def app_icon(name,c,x,y,sz=64):
    id_=uid('ai'); s=''
    if c=='grad': s+=f'<defs>{lg(id_,[(0,"#F9CE34"),(.45,"#EE2A7B"),(1,"#6228D7")],0,1,1,0)}</defs>'; fillc=f'url(#{id_})'
    else: fillc=c
    s+=rect(x,y,sz,sz,rx=sz*.24,fill=fillc)
    cx,cy=x+sz/2,y+sz/2; k=sz/64
    gl={'Chat':path(f'M{f(cx-14*k)} {f(cy+12*k)} l3 -9 a15 15 0 1 1 7 6Z',fill='#fff'),
        'Photos':''.join(ell(cx+math.cos(a)*9*k,cy+math.sin(a)*9*k,7*k,11*k,fill=cc,opacity='.85',transform=f'rotate({f(a/D+90)} {f(cx+math.cos(a)*9*k)} {f(cy+math.sin(a)*9*k)})') for a,cc in zip([i*math.pi/3 for i in range(6)],['#E5484D','#FF9F0A','#F2D45A','#5FB55A','#4F8CFF','#7B5CFF'])),
        'Insta':rect(cx-16*k,cy-16*k,32*k,32*k,rx=9*k,fill='none',stroke='#fff',stroke_width=3.5*k)+circ(cx,cy,7*k,fill='none',stroke='#fff',stroke_width=3.5*k)+circ(cx+9*k,cy-9*k,2*k,fill='#fff'),
        'Mail':rect(cx-17*k,cy-12*k,34*k,24*k,rx=3*k,fill='#fff')+path(f'M{f(cx-17*k)} {f(cy-10*k)} L{f(cx)} {f(cy+3*k)} L{f(cx+17*k)} {f(cy-10*k)}',fill='none',stroke=c,stroke_width=2.6*k),
        'Bank':path(f'M{f(cx-18*k)} {f(cy-6*k)} L{f(cx)} {f(cy-18*k)} L{f(cx+18*k)} {f(cy-6*k)}Z',fill='#fff')+''.join(rect(cx+dx*k-2.5*k,cy-4*k,5*k,16*k,fill='#fff') for dx in (-12,-4,4,12))+rect(cx-18*k,cy+13*k,36*k,4*k,fill='#fff'),
        'Clock':circ(cx,cy,18*k,fill='#fff')+path(f'M{f(cx)} {f(cy-12*k)} L{f(cx)} {f(cy)} L{f(cx+9*k)} {f(cy+5*k)}',fill='none',stroke='#222',stroke_width=3*k,stroke_linecap='round'),
        'Music':path(f'M{f(cx-6*k)} {f(cy+10*k)} L{f(cx-6*k)} {f(cy-14*k)} L{f(cx+12*k)} {f(cy-18*k)} L{f(cx+12*k)} {f(cy+6*k)}',fill='none',stroke='#fff',stroke_width=3.4*k)+circ(cx-10*k,cy+11*k,5*k,fill='#fff')+circ(cx+8*k,cy+7*k,5*k,fill='#fff'),
        'Video':path(f'M{f(cx-8*k)} {f(cy-12*k)} L{f(cx+13*k)} {f(cy)} L{f(cx-8*k)} {f(cy+12*k)}Z',fill='#fff'),
        'Settings':circ(cx,cy,14*k,fill='none',stroke='#fff',stroke_width=6*k,stroke_dasharray=f'{f(5*k)} {f(3.5*k)}')+circ(cx,cy,6*k,fill='#fff'),
        'Calendar':text('6',cx,cy+14*k,size=f(34*k),fill='#111',weight=300,anchor='middle')+text('WED',cx,cy-12*k,size=f(10*k),fill='#E5484D',weight=700,anchor='middle'),
        'Notes':''.join(rect(cx-16*k,cy-10*k+i*9*k,32*k,2.4*k,fill='#8A6A2A',opacity='.6') for i in range(3)),
        'Maps':path(f'M{f(cx)} {f(cy+16*k)} C{f(cx-16*k)} {f(cy)} {f(cx-12*k)} {f(cy-16*k)} {f(cx)} {f(cy-16*k)} C{f(cx+12*k)} {f(cy-16*k)} {f(cx+16*k)} {f(cy)} {f(cx)} {f(cy+16*k)}Z',fill='#fff')+circ(cx,cy-5*k,5*k,fill=c),
        'Fitness':''.join(circ(cx,cy,r_*k,fill='none',stroke=cc,stroke_width=5*k) for r_,cc in ((18,'#1E1E1E'),(11,'#1E1E1E'))),
        'Shop':path(f'M{f(cx-14*k)} {f(cy-6*k)} L{f(cx+14*k)} {f(cy-6*k)} L{f(cx+11*k)} {f(cy+16*k)} L{f(cx-11*k)} {f(cy+16*k)}Z',fill='#fff')+path(f'M{f(cx-6*k)} {f(cy-6*k)} Q{f(cx-6*k)} {f(cy-16*k)} {f(cx)} {f(cy-16*k)} Q{f(cx+6*k)} {f(cy-16*k)} {f(cx+6*k)} {f(cy-6*k)}',fill='none',stroke='#fff',stroke_width=3*k),
        'Games':rect(cx-18*k,cy-9*k,36*k,18*k,rx=9*k,fill='#fff')+circ(cx+8*k,cy,3*k,fill=c)+rect(cx-13*k,cy-1.5*k,10*k,3*k,fill=c)+rect(cx-9.5*k,cy-5*k,3*k,10*k,fill=c),
        'Weather':circ(cx-4*k,cy-4*k,10*k,fill='#FFD86B')+circ(cx+6*k,cy+6*k,9*k,fill='#fff')+circ(cx-4*k,cy+8*k,7*k,fill='#fff')+rect(cx-12*k,cy+8*k,26*k,7*k,rx=3*k,fill='#fff')}
    s+=gl.get(name,'')
    return s
def scr_home(badges=True,delete_mode=False):
    id_=uid('hm')
    s=f'<defs>{lg(id_,[(0,"#1B2A4A"),(1,"#3B2A5A")])}</defs>'+rect(0,0,SW,SH,fill=f'url(#{id_})')+status('2:47',.15)
    for i,(n,c) in enumerate(APPS):
        x=28+(i%4)*88; y=90+(i//4)*104
        s+=g(app_icon(n,c,x,y),transform=f'rotate({-2 if (i%2) else 2} {x+32} {y+32})' if delete_mode else None)
        s+=text(n,x+32,y+84,size=12,fill=TXT,anchor='middle',opacity='.9')
        if delete_mode and n in('Insta','Video','Games','Shop'):
            s+=circ(x+4,y+4,11,fill='#8A93A8')+rect(x-2.5,y+2.5,13,3,fill='#111',rx=1)
        elif badges and n in ('Chat','Insta','Mail'):
            s+=circ(x+60,y+4,11,fill='#E5484D')+text({'Chat':'12','Insta':'99+','Mail':'3'}[n],x+60,y+8.5,size=10 if n=='Insta' else 12,fill='#fff',weight=700,anchor='middle')
    s+=rect(16,SH-120,SW-32,96,rx=30,fill='#fff',opacity='.15')
    for i,(n,c) in enumerate([('Chat','#25D366'),('Insta','grad'),('Music','#FF3B5C'),('Clock','#222')]): s+=app_icon(n,c,36+i*86,SH-104)
    if delete_mode:
        s+=rect(40,320,SW-80,170,rx=20,fill='#2A2E3A',opacity='.97')+text('Delete "Insta"?',SW/2,364,size=18,fill=TXT,weight=700,anchor='middle')+text('Removing it will delete all its data.',SW/2,392,size=13,fill=MUT,anchor='middle')
        s+=line([40,420],[SW-40,420],stroke='#3A3F4E')+text('Delete App',SW/2,460,size=17,fill='#FF453A',weight=700,anchor='middle')
    return s+navbar()
def chat_header(title,sub,c='#E2A33B',initial='O'):
    return rect(0,52,SW,76,fill=CARD)+path('M22 90 l10 -10 M22 90 l10 10',stroke=ACC,stroke_width=3,stroke_linecap='round')+avatar(66,90,22,c,initial)+text(title,98,86,size=16,fill=TXT,weight=700)+text(sub,98,106,size=12,fill=MUT)
def bubble(x,y,w,lines,me=False,name=None,nc='#E2A33B'):
    h=24+len(lines)*20+(16 if name else 0)
    c='#2F6FEB' if me else '#252B3B'
    s=rect(x,y,w,h,rx=18,fill=c)
    yy=y+24
    if name: s+=text(name,x+14,yy-2,size=12,fill=nc,weight=700); yy+=16
    for l in lines: s+=text(l,x+14,yy+4,size=15,fill=TXT); yy+=20
    return s,h
def scr_group_chat():
    s=rect(0,0,SW,SH,fill=BG)+status()+chat_header('THE OLD CREW','Sam, Priya, Leo, Mia +4')
    y=150
    for nm,nc,ls in [('Priya','#F2A65A',['Dinner this Friday!!','Everyone is coming 🎉'.replace(' 🎉','')]),('Leo','#5AC8FA',['Finally. I have so much','to tell you guys. New job!!']),('Mia','#C58CFF',["Can't wait to hear what","everyone's up to"]),('Sam','#7BD88F',['Hey, you in?? We haven\'t','seen you in forever'])]:
        b,h=bubble(56,y,250,ls,name=nm,nc=nc); s+=avatar(30,y+h-16,14,nc,nm[0])+b; y+=h+14
    s+=rect(56,y,70,38,rx=19,fill='#252B3B')+''.join(circ(76+i*15,y+19,4,fill=MUT) for i in range(3))
    s+=rect(16,SH-80,SW-32,48,rx=24,fill=CARD)+text('Message',40,SH-50,size=15,fill=MUT)+circ(SW-44,SH-56,18,fill=ACC)
    return s+navbar()
def scr_dm(name='Mom',msgs=None):
    msgs=msgs or [(False,['Hi sweetie, are you eating ok?']),(False,['Call me when you can ❤'.replace(' ❤','')]),(True,['sorry mom, busy week']),(False,['Your cousin got promoted!','Thought you should know']),(True,['...'])]
    s=rect(0,0,SW,SH,fill=BG)+status()+chat_header(name,'online','#C8577A',name[0])
    y=160
    for me,ls in msgs:
        w=max(len(l) for l in ls)*8.2+30
        b,h=bubble(SW-20-w if me else 20,y,w,ls,me=me); s+=b; y+=h+12
    s+=text('Read 11:42 PM',SW-24,y+8,size=11,fill=MUT,anchor='end')
    s+=rect(16,SH-80,SW-32,48,rx=24,fill=CARD)+text('Message',40,SH-50,size=15,fill=MUT)
    return s+navbar()
def post(y,user,c,caption,likes,bg=('#F2A65A','#C8577A'),shirt='#3E6A8A',extra=''):
    s=avatar(36,y+24,18,c,user[0])+text(user,64,y+30,size=15,fill=TXT,weight=700)+''.join(circ(SW-40+i*7,y+24,2.2,fill=TXT) for i in range(3))
    s+=person_photo(0,y+52,SW,SW*.85,bg[0],bg[1],shirt=shirt)+extra
    yy=y+52+SW*.85+28
    s+=icon_heart(30,yy,1.8,fillit=True)+path(f'M62 {yy-10} a12 11 0 1 1 6 18 l-9 3 l3 -8Z',fill='none',stroke=TXT,stroke_width=2.2)+path(f'M104 {yy-12} L124 {yy} L104 {yy+10} L108 {yy}Z',fill='none',stroke=TXT,stroke_width=2.2,stroke_linejoin='round')
    s+=text(f'{likes} likes',20,yy+32,size=14,fill=TXT,weight=700)+text(caption,20,yy+54,size=14,fill=TXT)
    return s
def scr_feed():
    s=rect(0,0,SW,SH,fill=BG)+status()+text('Instagram',20,92,size=26,fill=TXT,weight=700,family="'Billabong', 'Brush Script MT', cursive")
    for i,(n,c) in enumerate([('Your story','#555'),('sam','#7BD88F'),('priya','#F2A65A'),('leo','#5AC8FA'),('mia','#C58CFF')]):
        x=44+i*76; s+=circ(x,150,31,fill='none',stroke='url(#igRing)' if i else '#555',stroke_width=3)+avatar(x,150,26,c,n[0].upper())+text(n,x,198,size=11,fill=TXT,anchor='middle')
    s+=f'<defs>{lg("igRing",[(0,"#feda75"),(.5,"#d62976"),(1,"#4f5bd5")],0,1,1,0)}</defs>'
    s+=post(214,'leo.builds','#5AC8FA','leo.builds  Day 1 at the new firm 💼'.replace(' 💼',''),'2,481',('#5AC8FA','#2A4A7A'),'#2F3545')
    return s+navbar()
def scr_story_gym():
    id_=uid('gy')
    s=f'<defs>{lg(id_,[(0,"#3A2C22"),(1,"#14100D")])}</defs>'+rect(0,0,SW,SH,fill=f'url(#{id_})')
    # gym guy flex
    s+=rect(0,560,SW,SH-560,fill='#241B15')
    for x in (40,330): s+=rect(x,300,16,260,fill='#4A3A2E')
    s+=rect(30,330,330,10,fill='#8D939C')
    s+=circ(195,330,48,fill='#D9A877',stroke='#8A6340',stroke_width=3)+path('M147 322 A48 48 0 0 1 243 322Z',fill='#1E1712')
    s+=path('M110 560 L110 430 Q110 380 195 378 Q280 380 280 430 L280 560Z',fill='#2E2E35',stroke='#111',stroke_width=3)
    for sx in (-1,1): s+=path(f'M{195+sx*80} 410 Q{195+sx*150} 400 {195+sx*150} 330',fill='none',stroke='#8A6340',stroke_width=40,stroke_linecap='round')+path(f'M{195+sx*80} 410 Q{195+sx*150} 400 {195+sx*150} 330',fill='none',stroke='#D9A877',stroke_width=34,stroke_linecap='round')+circ(195+sx*150,316,20,fill='#D9A877',stroke='#8A6340',stroke_width=3)+ell(195+sx*118,388,22,16,fill='#E8BC8C')
    s+=path('M178 345 Q195 356 212 345',fill='none',stroke='#4A3530',stroke_width=3,stroke_linecap='round')+circ(181,328,3,fill='#221E1B')+circ(209,328,3,fill='#221E1B')
    # story chrome
    for i in range(3): s+=rect(12+i*124,56,116,3,rx=1.5,fill='#fff',opacity='1' if i<1 else '.35')
    s+=avatar(34,90,16,'#7BD88F','S')+text('sam_lifts',58,96,size=14,fill='#fff',weight=700)+text('2h',140,96,size=13,fill='#fff',opacity='.7')
    s+=g(rect(-130,-26,260,52,rx=8,fill='#fff')+text('DAY 365 💪'.replace(' 💪',''),0,10,size=26,fill='#111',weight=900,anchor='middle'),transform=f'translate({SW/2} 200) rotate(-4)')
    s+=text('no days off. what\'s YOUR excuse?',SW/2,640,size=17,fill='#fff',weight=700,anchor='middle')
    s+=rect(16,SH-80,SW-90,46,rx=23,fill='none',stroke='#fff',stroke_width=1.5,opacity='.7')+text('Send message',38,SH-51,size=14,fill='#fff',opacity='.8')+icon_heart(SW-40,SH-58,2,'#fff',False)
    return s
def scr_bank_zero():
    s=rect(0,0,SW,SH,fill='#0B1512')+status(dark_=True)
    s+=text('Hello, Alex',24,100,size=16,fill=MUT)+text('Checking account',24,128,size=20,fill=TXT,weight=700)
    s+=rect(16,150,SW-32,190,rx=22,fill='#13241E',stroke='#1F3A30')
    s+=text('Available balance',40,196,size=14,fill=MUT)+text('$0.00',40,268,size=60,fill='#FF5A4E',weight=800)
    s+=rect(40,292,140,28,rx=14,fill='#3A1A1A')+text('⚠ Overdraft risk'.replace('⚠ ','! '),110,311,size=12,fill='#FF8A80',weight=700,anchor='middle')
    s+=text('Recent',24,384,size=16,fill=TXT,weight=700)
    for i,(n,a) in enumerate([('Rent – March','-$950.00'),('Food delivery','-$23.40'),('Streaming','-$15.99'),('Gym (unused)','-$39.00'),('Phone bill','-$60.00')]):
        y=410+i*66; s+=rect(16,y,SW-32,56,rx=14,fill='#13241E')+circ(46,y+28,14,fill='#1F3A30')+text(n,72,y+33,size=15,fill=TXT)+text(a,SW-32,y+33,size=15,fill='#FF8A80',weight=700,anchor='end')
    return s+navbar()
def scr_keys_post():
    s=rect(0,0,SW,SH,fill=BG)+status()
    extra=g(circ(0,0,22,fill='none',stroke='#D7B270',stroke_width=6)+rect(-5,20,10,60,fill='#D7B270')+rect(5,60,12,7,fill='#D7B270')+rect(5,72,9,7,fill='#D7B270'),transform=f'translate({SW*.72} {130+SW*.35}) rotate(-20)')
    s+=post(70,'mia.home','#C58CFF','mia.home  We bought our first house!! 🏡'.replace(' 🏡',''),'5,902',('#9FCBEB','#5E8A5A'),'#C8577A',extra)
    return s+navbar()
def scr_graduation():
    s=rect(0,0,SW,SH,fill=BG)+status()
    extra=''.join(g(path('M-30 0 L0 -12 L30 0 L0 12Z',fill='#141a2e')+rect(-14,4,28,10,fill='#141a2e'),transform=f'translate({x} {y}) rotate({r})') for x,y,r in ((80,170,-20),(300,150,25),(220,120,8)))
    s+=post(70,'priya.codes','#F2A65A','priya.codes  WE DID IT!! Class of 2026','3,117',('#6fb3ff','#cfe6ff'),'#141a2e',extra)
    return s+navbar()
def scr_incoming_call(name='Mom'):
    id_=uid('cl')
    s=f'<defs>{lg(id_,[(0,"#2A3A5A"),(1,"#0E1118")])}</defs>'+rect(0,0,SW,SH,fill=f'url(#{id_})')+status()
    s+=text(name,SW/2,190,size=40,fill=TXT,weight=600,anchor='middle')+text('mobile',SW/2,224,size=17,fill=MUT,anchor='middle')
    s+=avatar(SW/2,360,70,'#C8577A',name[0])
    for x,c,lb in ((100,'#FF453A','Decline'),(SW-100,'#30D158','Accept')):
        s+=circ(x,SH-170,38,fill=c)+text(lb,x,SH-110,size=14,fill=TXT,anchor='middle')
        s+=g(path('M-14 -4 C-14 -12 14 -12 14 -4 L10 2 L5 -2 L-5 -2 L-10 2Z',fill='#fff'),transform=f'translate({x} {SH-170}) rotate({135 if c=="#FF453A" else 0})')
    return s+navbar()
def scr_alarm():
    s=rect(0,0,SW,SH,fill='#140E0A')+status('7:00',.4)
    s+=circ(SW/2,320,140,fill='#FF9F0A',opacity='.12')+circ(SW/2,320,100,fill='#FF9F0A',opacity='.16')
    s+=text('Alarm',SW/2,180,size=20,fill=MUT,anchor='middle')+text('7:00',SW/2,350,size=90,fill=TXT,weight=700,anchor='middle')+text('AM',SW/2,390,size=20,fill=MUT,anchor='middle')
    s+=text('"Today is the day."',SW/2,450,size=17,fill=TXT,anchor='middle',opacity='.8')
    s+=rect(40,SH-250,SW-80,70,rx=35,fill='#FF9F0A')+text('Snooze',SW/2,SH-206,size=22,fill='#140E0A',weight=700,anchor='middle')
    s+=text('Swipe up to stop',SW/2,SH-120,size=15,fill=MUT,anchor='middle')
    return s+navbar()
def scr_low_battery():
    s=rect(0,0,SW,SH,fill='#000')+status('3:12',.02)
    s+=rect(SW/2-90,330,180,80,rx=14,fill='none',stroke='#555',stroke_width=5)+rect(SW/2+92,352,12,36,rx=3,fill='#555')+rect(SW/2-82,338,12,64,rx=4,fill='#E5484D')
    s+=text('1%',SW/2,470,size=28,fill='#E5484D',weight=700,anchor='middle')+text('Connect to power',SW/2,504,size=15,fill=MUT,anchor='middle')
    return s
def scr_notifications():
    s=rect(0,0,SW,SH,fill='#0B0D13')+status()+text('Notifications',24,110,size=30,fill=TXT,weight=800)
    items=[('#E1306C','Instagram','leo.builds and 14 others posted','2m'),('#25D366','The Old Crew','Sam: hello?? 👀'.replace(' 👀',''),'5m'),('#4F8CFF','Bank','Payment declined: $23.40','12m'),('#E1306C','Instagram','You have 3 new followers... (bots)','20m'),('#FF9F0A','Reminder','Gym – you skipped 21 days','1h'),('#2E7D5B','LinkedIn','Your classmate started a new position','2h'),('#8A93A8','Screen Time','You averaged 9h 41m yesterday','3h'),('#5AC8FA','Mail','Re: Application – Unfortunately...','5h')]
    for i,(c,a,b,t) in enumerate(items):
        y=140+i*82; s+=rect(14,y,SW-28,72,rx=18,fill='#1A1E29')+rect(28,y+16,40,40,rx=10,fill=c)+text(a,82,y+31,size=15,fill=TXT,weight=700)+text(b,82,y+53,size=13.5,fill=TXT,opacity='.8')+text(t,SW-30,y+31,size=12,fill=MUT,anchor='end')
    return s+navbar()
def scr_screen_time():
    s=rect(0,0,SW,SH,fill=BG)+status()+text('Screen Time',24,110,size=30,fill=TXT,weight=800)+text('Daily average',24,150,size=14,fill=MUT)+text('9h 41m',24,200,size=48,fill=TXT,weight=800)+text('▲ 38% from last week'.replace('▲','+'),24,228,size=14,fill='#FF5A4E',weight=600)
    hs=[6,7.5,8,9,11,10.5,9.6]
    for i,h in enumerate(hs):
        x=34+i*48; bh=h*18
        s+=rect(x,460-bh,30,bh,rx=6,fill='#4F8CFF')+rect(x,460-bh*.45,30,bh*.45,rx=0,fill='#E1306C')+text('MTWTFSS'[i],x+15,486,size=13,fill=MUT,anchor='middle')
    for i,(n,t,c) in enumerate([('Insta','4h 12m','#E1306C'),('Video','3h 05m','#E5484D'),('Chat','1h 20m','#25D366'),('Games','58m','#7B5CFF')]):
        y=530+i*62; s+=rect(24,y,40,40,rx=10,fill=c)+text(n,80,y+26,size=16,fill=TXT)+text(t,SW-28,y+26,size=16,fill=MUT,anchor='end')
    return s+navbar()
def scr_calendar_deadline():
    s=rect(0,0,SW,SH,fill='#F6F4EF')+status(dark_=False)+text('March',24,110,size=32,fill='#111',weight=800)
    for i,d in enumerate('SMTWTFS'): s+=text(d,40+i*50,150,size=13,fill='#888',anchor='middle',weight=600)
    for i in range(31):
        k=i+3; x=40+(k%7)*50; y=196+(k//7)*58
        today=i==5; dl=i==6
        if today: s+=circ(x,y-6,20,fill='#E5484D')
        if dl: s+=circ(x,y-6,20,fill='none',stroke='#E5484D',stroke_width=2.5)
        s+=text(str(i+1),x,y,size=17,fill='#fff' if today else '#111',anchor='middle',weight=600)
    s+=rect(16,560,SW-32,90,rx=16,fill='#fff',stroke='#E5E2DA')+rect(16,560,8,90,rx=4,fill='#E5484D')+text('FINAL PROJECT DUE',40,598,size=17,fill='#111',weight=800)+text('Tomorrow · 9:00 AM  ·  0% done',40,626,size=14,fill='#E5484D',weight=600)
    s+=rect(16,664,SW-32,70,rx=16,fill='#fff',stroke='#E5E2DA')+rect(16,664,8,70,rx=4,fill='#4F8CFF')+text('Rent',40,706,size=16,fill='#111',weight=700)
    return s+navbar(False)
def scr_video_call():
    s=rect(0,0,SW,SH,fill='#000')+person_photo(0,0,SW,SH,'#5A6A8A','#2A3040',shirt='#C8577A',skin='#F2D3B8')
    s+=rect(SW-130,70,110,160,rx=14,fill='#333',stroke='#fff',stroke_width=2)+text('camera off',SW-75,156,size=12,fill='#bbb',anchor='middle')
    s+=text('Mia',SW/2,90,size=20,fill='#fff',weight=700,anchor='middle')+text('04:12',SW/2,114,size=14,fill='#fff',anchor='middle',opacity='.8')
    for i,c in enumerate(('#3A3A3C','#3A3A3C','#FF453A')): s+=circ(100+i*95,SH-110,32,fill=c)
    return s+navbar()
def scr_music():
    id_=uid('mu')
    s=f'<defs>{lg(id_,[(0,"#4A2E5E"),(1,"#0E1118")])}</defs>'+rect(0,0,SW,SH,fill=f'url(#{id_})')+status()
    s+=rect(40,120,SW-80,SW-80,rx=18,fill='#2A3A6A')+circ(SW/2,120+(SW-80)/2,90,fill='#F2A65A',opacity='.8')+circ(SW/2,120+(SW-80)/2,24,fill='#2A3A6A')
    s+=text('sad songs for 3am',40,SW+90,size=22,fill=TXT,weight=700)+text('Playlist · 214 songs',40,SW+116,size=15,fill=MUT)
    s+=rect(40,SW+150,SW-80,5,rx=2.5,fill='#fff',opacity='.25')+rect(40,SW+150,120,5,rx=2.5,fill='#fff')+circ(160,SW+152,8,fill='#fff')
    s+=circ(SW/2,SW+250,38,fill='#fff')+rect(SW/2-12,SW+234,8,32,fill='#111')+rect(SW/2+4,SW+234,8,32,fill='#111')
    s+=path(f'M{SW/2-130} {SW+250} l22 -16 l0 32Z M{SW/2-152} {SW+250} l22 -16 l0 32Z M{SW/2+130} {SW+250} l-22 -16 l0 32Z M{SW/2+152} {SW+250} l-22 -16 l0 32Z',fill='#fff')
    return s+navbar()
def scr_job_rejection():
    s=rect(0,0,SW,SH,fill='#fff')+status(dark_=False)
    s+=text('Inbox',24,104,size=30,fill='#111',weight=800)
    s+=rect(0,124,SW,1,fill='#e5e5e5')+text('Hiring Team',24,166,size=17,fill='#111',weight=700)+text('Re: Your application',24,192,size=15,fill='#111')
    lines=['Dear Alex,','','Thank you for your interest in the','Junior Designer position.','','After careful consideration, we have','decided to move forward with other','candidates whose experience more','closely matches our needs.','','We wish you the best in your search.']
    for i,l in enumerate(lines): s+=text(l,24,240+i*26,size=15,fill='#333')
    s+=rect(18,354,300,26,fill='#FFE38A',opacity='.6')
    return s+navbar(False)
def scr_blank(c='#0B0D13'): return rect(0,0,SW,SH,fill=c)
def scr_off(): return rect(0,0,SW,SH,fill='#050608')+path(f'M0 0 L{SW*.6} 0 L0 {SH*.4}Z',fill='#fff',opacity='.04')
def scr_delete_apps(): return scr_home(badges=False,delete_mode=True)
def scr_journal():
    s=rect(0,0,SW,SH,fill='#F6F1E3')+status(dark_=False)+text('Reality audit',24,110,size=28,fill='#111',weight=800)
    lines=[('What I actually have:',True),('- a roof, a bed, a phone',False),('- 2 friends who still text me',False),('- 26 years of experience being me',False),('',False),('What I am comparing:',True),('- their best 1% moments',False),('- vs my worst 3am thoughts',False),('',False),('One thing today:',True),('- 10 minutes outside. no phone.',False)]
    for i,(l,b) in enumerate(lines): s+=text(l,24,160+i*34,size=17 if b else 16,fill='#111' if b else '#3A3A3A',weight=800 if b else 400,family="'Caveat', 'Comic Sans MS', cursive")
    for i in range(16): s+=rect(0,172+i*34,SW,1,fill='#C9BFA8',opacity='.5')
    return s+navbar(False)
SCREENS={
 'lock_screen_notifications':scr_lock,'home_screen':scr_home,'home_delete_apps':scr_delete_apps,'group_chat':scr_group_chat,'dm_mom':scr_dm,
 'social_feed_new_job':scr_feed,'story_gym':scr_story_gym,'post_new_house':scr_keys_post,'post_graduation':scr_graduation,'bank_balance_zero':scr_bank_zero,
 'incoming_call':scr_incoming_call,'alarm_ringing':scr_alarm,'battery_1_percent':scr_low_battery,'notifications_list':scr_notifications,'screen_time':scr_screen_time,
 'calendar_deadline':scr_calendar_deadline,'video_call':scr_video_call,'music_player':scr_music,'email_rejection':scr_job_rejection,'notes_reality_audit':scr_journal,'screen_off':scr_off,
}
# ---------- device ----------
def phone_device(screen_svg,frame='#1A1D24',scale=1,glow=False):
    id_=uid('scr')
    W,H=SW+28,SH+28
    s=''
    if glow: s+=ell(0,0,W*1.1,H*.75,fill='url(#screenGlow)')
    s+=rect(-W/2-3,-H/2+150,4,60,rx=2,fill=dark(frame,.2))+rect(W/2-1,-H/2+190,4,90,rx=2,fill=dark(frame,.2))+rect(-W/2-3,-H/2+230,4,60,rx=2,fill=dark(frame,.2))
    s+=rect(-W/2,-H/2,W,H,rx=58,fill=frame,stroke='#0A0B0F',stroke_width=3)
    s+=rect(-W/2+5,-H/2+5,W-10,H-10,rx=54,fill='none',stroke=light(frame,.15),stroke_width=2)
    s+=f'<defs><clipPath id="{id_}"><rect x="0" y="0" width="{SW}" height="{SH}" rx="46"/></clipPath></defs>'
    s+=g(g(screen_svg,clip_path=f'url(#{id_})'),transform=f'translate({-SW/2} {-SH/2})')
    s+=path(f'M{-SW/2+20} {-SH/2} L{-SW/2+190} {-SH/2} L{-SW/2} {-SH/2+330}Z',fill='#fff',opacity='.05')
    return g(s,transform=f'scale({scale})')
def phone_back(c='#2B3040'):
    W,H=SW+28,SH+28
    s=rect(-W/2,-H/2,W,H,rx=58,fill=c,stroke='#0A0B0F',stroke_width=3)
    s+=rect(-W/2+26,-H/2+26,160,160,rx=40,fill=dark(c,.25))
    for (x,y) in ((-W/2+66,-H/2+66),(-W/2+146,-H/2+66),(-W/2+66,-H/2+146)): s+=circ(x,y,30,fill='#111',stroke=light(c,.2),stroke_width=4)+circ(x,y,12,fill='#1E2A4A')+circ(x-5,y-5,4,fill='#fff',opacity='.4')
    s+=circ(-W/2+146,-H/2+146,10,fill='#FFF3CF',opacity='.8')
    s+=g(path('M0 -28 C-6 -40 -26 -40 -26 -18 C-26 0 0 18 0 18 C0 18 26 0 26 -18 C26 -40 6 -40 0 -28Z',fill=light(c,.15)),transform='translate(0 20)')
    s+=path(f'M{W/2-80} {-H/2} L{W/2} {-H/2} L{W/2} {-H/2+300}Z',fill='#fff',opacity='.06')
    return s
def phone_side(c='#2B3040'):
    return rect(-14,-436,28,872,rx=12,fill=c,stroke='#0A0B0F',stroke_width=3)+rect(-16,-300,4,100,rx=2,fill=dark(c,.3))+rect(12,-250,4,60,rx=2,fill=dark(c,.3))+rect(-4,-436,8,872,fill=light(c,.1),opacity='.4')
def hand_holding_phone(screen_svg,skin='#ECE4D6',line='#8C8273'):
    """big close-up hand from bottom-right holding phone (like the source film)"""
    ph=phone_device(screen_svg,glow=True)
    s=ph
    # fingers wrapping left edge
    for i,y in enumerate((-120,-20,80,170)):
        s+=ell(-SW/2-14,y,24,22,fill=skin,stroke=line,stroke_width=3)
    # palm + thumb (bottom right)
    s+=path(f'M{SW/2-60} {SH/2+260} C{SW/2-100} {SH/2+60} {SW/2-40} {SH/2-160} {SW/2+60} {SH/2-140} C{SW/2+200} {SH/2-100} {SW/2+220} {SH/2+120} {SW/2+200} {SH/2+260}Z',fill=skin,stroke=line,stroke_width=3)
    s+=path(f'M{SW/2-10} {SH/2-120} C{SW/2-60} {SH/2-190} {SW/2-110} {SH/2-250} {SW/2-150} {SH/2-262} C{SW/2-180} {SH/2-270} {SW/2-190} {SH/2-236} {SW/2-160} {SH/2-212} C{SW/2-120} {SH/2-180} {SW/2-80} {SH/2-110} {SW/2-40} {SH/2-60}',fill=skin,stroke=line,stroke_width=3)
    return s
