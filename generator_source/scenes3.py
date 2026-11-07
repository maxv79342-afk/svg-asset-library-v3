from sv import *
import rig, poses as PO, poses3 as P3, cycles3 as CY, env as EN, env3 as E3, props as PR, fx as FX, fx3
from scenes import C as Cold
FL=EN.FL; S=1.25
ALLP=dict(PO.POSES); ALLP.update(PO.FRONT); ALLP.update(PO.BACK); ALLP.update(P3.POSES3); ALLP.update(P3.FRONT3)
def C(ck,pk=None,x=960,s=S,ground=FL,face=1,**kw):
    a=rig.cast_args(ck); pp={}
    if pk:
        pp=dict(ALLP[pk][1])
        if pk.startswith('front'): pp.setdefault('view','front')
        if pk in ('phone_look','phone_shock','phone_scroll_sad','sit_phone','lie_phone'): pp['holdN']=PO.phone_in_hand()
    q=dict(a); q.update(pp); q.update(kw)
    if a.get('acc') or pp.get('acc'): q['acc']=list(dict.fromkeys(list(a.get('acc') or [])+list(pp.get('acc') or [])))
    dy=q.pop('y',0)
    q['x']=x; q['y']=ground-(rig.hip_h(a)-dy)*s; q['s']=s; q['face']=face*q.get('face',1)
    c,_=rig.char(**q); return c
def CF(ck,cyc,i,x=960,s=S,ground=FL,face=1):
    a=rig.cast_args(ck); q=CY.frame_params(a,ck,cyc,i,phone_fn=lambda: PO.phone_in_hand())
    hy=rig.hip_h(a); q['x']=x; q['y']=ground+(q['y'])*s; q['s']=s; q['face']=face
    c,_=rig.char(**q); return c
T=EN.T
def tattoo_session():
    return E3.tattoo_studio()+g(C('luna','sit_crossed',x=900,ground=FL+40,s=1.2),id='client')+g(C('kai','talk',x=600,ground=FL+60,s=1.25),id='artist')
def gym_buddies():
    return E3.gym()+g(C('sam','dumbbell_curl',x=820,ground=FL+60),id='sam')+g(CF('jay','jog',5,x=300,ground=FL-40,s=1.1),id='jay')+g(C('kai','flex' if False else 'front_flex',x=1380,ground=FL+70),id='kai')
def hospital_visit():
    return E3.hospital_room()+g(C('dr_hana','talk',x=1240,ground=FL+40,face=-1),id='doctor')+g(C('grandma','pray_side',x=560,ground=FL+60),id='visitor')
def tehran_night_walk():
    return E3.tehran('night')+g(CF('reza','walk',3,x=760,ground=990,s=1.15),id='reza')+g(CF('sara','walk',9,x=960,ground=990,s=1.15),id='sara')
def persian_tea_time():
    return E3.persian_living_room('day')+g(C('grandpa','sit_coffee',x=430,ground=FL+20,s=1.2),id='grandpa')+g(C('grandma','sit_chair',x=1530,ground=FL+20,s=1.2,face=-1,expr='happy'),id='grandma')+g(C('zoe','front_wave',x=1180,ground=FL+90,s=1.15),id='zoe')
def podcast_live():
    return E3.podcast_studio()+g(C('elena','sit_think',x=820,ground=FL,s=1.15),id='host')+g(C('leo','talk',x=1180,ground=FL+40,s=1.15,face=-1),id='guest')
def beach_sunset_friends():
    return E3.beach('sunset')+g(C('luna','front_peace',x=760,ground=980),id='luna')+g(C('kai','cheer',x=1080,ground=990),id='kai')+g(T(fx3.confetti(.4),920,560),id='fx')
def rock_concert():
    return E3.concert_stage()+g(C('rocky','rock_on',x=620,ground=780,s=1.2),id='singer')+g(C('kai','front_rock',x=1300,ground=780,s=1.2),id='guitar')
def snow_day():
    return E3.snow_park()+g(CF('kid','jump',12,x=1300,ground=1000,s=1.2),id='kid')+g(C('grandpa','stand',x=1600,ground=1000,s=1.2,face=-1,expr='happy'),id='grandpa')
def police_stop():
    return E3.highway('night')+g(C('officer_dan','front_salute',x=1500,ground=1060,s=1.15),id='officer')
SCENES3=dict(tattoo_session=tattoo_session,gym_buddies=gym_buddies,hospital_visit=hospital_visit,tehran_night_walk=tehran_night_walk,persian_tea_time=persian_tea_time,podcast_live=podcast_live,beach_sunset_friends=beach_sunset_friends,rock_concert=rock_concert,snow_day=snow_day,police_stop=police_stop)
