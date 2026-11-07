from sv import *
import rig, poses as PO, props as PR, env as EN, fx as FX
S=1.25; FL=EN.FL
def C(ck,pk=None,x=960,s=S,ground=FL,face=1,over=None,**kw):
    a=rig.cast_args(ck)
    if ck=='shadow': a.update(eyes='glow',brow='none')
    pp={}
    if pk:
        allp=dict(PO.POSES); allp.update(PO.FRONT); allp.update(PO.BACK)
        pp=dict(allp[pk][1])
        if pk.startswith('front'): pp.setdefault('view','front')
        if pk in ('phone_look','phone_shock','phone_scroll_sad','sit_phone','lie_phone'): pp['holdN']=PO.phone_in_hand()
    q=dict(a); q.update(pp); q.update(kw)
    dy=q.pop('y',0)
    q['x']=x; q['y']=ground-(rig.hip_h(a)-dy)*s; q['s']=s; q['face']=face*q.get('face',1)
    c,_=rig.char(**q); return c
def T(svg,x,y,s=1,flip=False): return EN.T(svg,x,y,s,flip=flip)
def night_doomscroll():
    bg=EN.bedroom('night',True)
    bedx=150; top=FL-128
    ch=C('alex_hoodie','lie_phone',x=0,ground=0)
    # place: head on pillow
    char=g(ch,transform=f'translate({bedx+300} {top-30*S+4})')
    blanket=path(f'M{bedx+300} {top-46} C{bedx+360} {top-80} {bedx+440} {top-62} {bedx+480} {top-40} L{bedx+484} {top+56} Q{bedx+380} {top+64} {bedx+290} {top+56}Z',**PR.S('#3F5A8C',k=.5))+PR.hi(f'M{bedx+330} {top-40} Q{bedx+400} {top-70} {bedx+470} {top-38}','#7088B5','.6',4)
    glow=ell(bedx+150,top-140,260,200,fill='url(#screenGlow)')
    return bg+g(char,id='character')+g(blanket,id='blanket')+g(glow,id='phone_glow')+g(EN.vignette(),id='vignette')
def morning_alarm():
    return EN.bedroom('day')+g(C('alex_hoodie','stretch',x=980,expr='sleepy'),id='character')+g(T(FX.FXS['icon_zzz'](),1060,330,.7),id='fx')
def office_typing():
    s=EN.office('day',chairs=False)
    s+=T(PR.office_chair(),860,FL,.55)+g(C('leo','sit_typing',x=880),id='leo')
    s+=T(PR.desk(380),1080,FL,.65)+T(PR.laptop(True,'#5B7BB0'),1010,FL-200*.65,.6)+T(PR.mug(),1150,FL-130,.45)
    s+=g(C('boss','point',x=1500,face=-1,expr='angry',mouth='shout'),id='boss')+g(T(FX.shout(300,170,'DEADLINE!'),1290,330,.9),id='bubble')
    return s
def street_walk():
    s=EN.street('day')
    s+=g(C('maya_dressed',None,x=600,**PO.walk(1.2)),id='maya')+g(C('sam',None,x=1100,**PO.run(.6)),id='sam')+g(C('priya','front_wave',x=1500),id='priya')
    s+=g(T(FX.speech(200,100,'tail',txt='Hi!!'),1600,380,.9),id='bubble')
    return s
def talking_head():
    s=EN.void_spot()+g(C('alex','front_shrug',x=960,s=1.6,ground=900,expr='confused'),id='character')+g(T(FX.thought(360,170,'so... what now?'),1320,300),id='bubble')
    return s
def inner_voice():
    s=EN.void_dark()+g(T(FX.FXS['dark_shadow_creature'](),1240,420,1.1),id='shadow')
    s+=g(C('alex','sit_floor_hug',x=760,s=1.5,ground=900,expr='crying'),id='character')+g(T(FX.inner_voice(420,140,'you started too late.'),1300,170),id='bubble')
    return s
def family_evening():
    s=EN.living_room('evening')
    s+=g(C('grandpa','coffee',x=700),id='grandpa')+g(C('kid','front_wave',x=1000,expr='joy'),id='kid')+g(C('maya_dressed','front_hips',x=1300,expr='happy'),id='maya')
    return s
def new_house():
    s=EN.house_exterior('day')+g(C('priya','front_cheer',x=760,expr='excited'),id='priya')+g(C('alex_hoodie','phone_shock',x=1300,face=-1),id='alex')
    s+=g(T(PR.keys(),860,330,.9),id='keys')
    return s
SCENES=dict(night_doomscroll=night_doomscroll,morning_alarm=morning_alarm,office_deadline=office_typing,street_meetup=street_walk,talking_head_explainer=talking_head,inner_voice_shadow=inner_voice,family_evening=family_evening,friends_new_house=new_house)
