"""SVG Asset Library v3 – master build.  python build3.py [OUTDIR]"""
import os, re, sys, math, json, shutil, time
from multiprocessing import Pool
from sv import *
import props2 as P2, acc as AC, acc2 as AC2, tattoo as TT
import rig, face as FX, poses as PO, poses3 as P3, cycles3 as CY, props as PR, screens as SC, env as EN, env3 as E3, fx as FXS, fx3, export as E, prev
import props3_beds as PB, props3_vehicles as PV, props3_home as PH, props3_world as PW, handsfeet as HF, puppet as PU
OUT=sys.argv[1] if len(sys.argv)>1 else '/home/user/build/SVG_Asset_Library_v3'
def P_(*a):
    p=os.path.join(OUT,*a); os.makedirs(os.path.dirname(p),exist_ok=True); return p
def strip_ids(svg): return re.sub(r'<g id="[^"]+"',"<g",svg)
_D=re.compile(r' d="([^"]*)"')
def mini(svg):
    svg=svg.replace(' stroke-linecap="round"','').replace(' stroke-linejoin="round"','')
    svg=_D.sub(lambda m: ' d="'+m.group(1).replace(' -','-')+'"',svg)
    i=svg.index('>',svg.index('<svg'))+1
    j=svg.find('</defs>',i); 
    if svg.startswith('<defs>',i) or svg.startswith('<title>',i):
        k=svg.find('</defs>') if '<defs>' in svg[:i+4000] else -1
        k2=svg.find('</title>')
        cut=max(k+7 if k>0 else i, k2+8 if k2>0 else i)
        if svg.startswith('<defs>',i) and k<0: cut=i
    else: cut=i
    return svg[:cut]+'<g stroke-linecap="round" stroke-linejoin="round">'+svg[cut:-6]+'</g></svg>'

class Ctx:
    def __init__(s): s.MAN=[]
    def save(s,rel,inner,vb=None,title=None,cat='',sub='',probe=None,defs_extra='',**meta):
        if vb is None: vb=E.tight(inner,probe or (-1200,-1400,2400,2000))
        d=E.used_defs(inner)+defs_extra
        open(P_(rel),'w').write(mini(doc(inner,vb,defs=d,title=title)))
        m=dict(cat=cat,sub=sub,name=os.path.splitext(os.path.basename(rel))[0],path=rel); m.update(meta); s.MAN.append(m)
        return vb
    def sheet(s,rel,cells,cols,cw,ch,title,bg='#1C2233',label=True,cat='',sub='',write=True):
        rows=(len(cells)-1)//cols+1; Wd=cols*cw; Ht=rows*ch+90
        o=rect(0,0,Wd,Ht,fill=bg)+text(title,40,58,size=34,fill='#ECE4D6',weight=800)
        for i,(name,inner,vb) in enumerate(cells):
            cx=(i%cols)*cw; cy=90+(i//cols)*ch
            o+=rect(cx+8,cy+8,cw-16,ch-16,rx=14,fill=light(bg,.04))
            if vb is None: vb=E.tight(inner)
            sc=min((cw-40)/vb[2],(ch-(70 if label else 40))/vb[3])
            o+=g(strip_ids(inner),transform=f'translate({f(cx+cw/2-(vb[0]+vb[2]/2)*sc)} {f(cy+(ch-(30 if label else 0))/2-(vb[1]+vb[3]/2)*sc)}) scale({f(sc)})')
            if label: o+=text(name,cx+cw/2,cy+ch-22,size=16,fill='#9AA3B8',anchor='middle')
        svg=doc(o,(0,0,Wd,Ht),defs=E.GDEFS+EN.DEFS,title=title)
        if not write: return svg
        open(P_(rel),'w').write(mini(svg))
        s.MAN.append(dict(cat=cat,sub=sub,name=os.path.splitext(os.path.basename(rel))[0],path=rel,sheet=True))
        return svg
def preview(name,svg,w=2400): prev.png(svg,w,P_('_previews',name+'.png'))
PHONE_POSES={'phone_look','phone_shock','phone_scroll_sad','sit_phone','lie_phone','front_call'}
GROUND={'kneel','sit_floor_hug','front_meditate','sneak','bow','tie_shoe'}
ALLPOSES=dict(PO.POSES); ALLPOSES.update(P3.POSES3); ALLPOSES.update(PO.FRONT); ALLPOSES.update(P3.FRONT3); ALLPOSES.update(PO.BACK)
def pose_args(ck,pk,pp):
    a=rig.cast_args(ck)
    q=dict(a); q.update(pp)
    if a.get('acc') or pp.get('acc'): q['acc']=list(dict.fromkeys(list(a.get('acc') or [])+list(pp.get('acc') or [])))
    if pk.startswith('front'): q.setdefault('view','front')
    if pk in PHONE_POSES: q['holdN']=PO.phone_in_hand(glow=pk!='front_call')
    if ck=='shadow': q['eyes']='glow'; q['brow']='none'; q['fx']=[]
    q['x']=q.pop('x',0); q['y']=-rig.hip_h(a)+q.pop('y',0)
    return q
PREV_POSES={'alex_hoodie','kai','sara','luna','rocky','zoe'}
PREV_CYC={'alex_hoodie','kai','sara','jay'}
def build_char(ck):
    t0=time.time(); X=Ctx(); cinfo=rig.CAST[ck]; nm=cinfo['name']; base=f'01_characters/{ck}'
    built={}
    for pk,(desc,pp) in ALLPOSES.items():
        q=pose_args(ck,pk,pp); c,_=rig.char(**q)
        if pk.startswith('lie') or pk in GROUND:
            q2=dict(q); q2['holdN']=None; q2['holdF']=None; q2['mid']=None
            c2,_=rig.char(**q2); vb=E.tight(c2,pad=0); q['y']-=(vb[1]+vb[3])-2; c,_=rig.char(**q)
        built[pk]=c
    vbs=[E.tight(c) for c in built.values()]
    x0=min(v[0] for v in vbs); y0=min(v[1] for v in vbs); x1=max(v[0]+v[2] for v in vbs); y1=max(v[1]+v[3] for v in vbs)
    Xm=max(abs(x0),abs(x1)); canvas=(-Xm,y0,2*Xm,max(y1,30)-y0)
    for pk,c in built.items(): X.save(f'{base}/poses/{pk}.svg',c,vb=canvas,title=f'{nm} – {ALLPOSES[pk][0]}',cat='Characters',sub=nm)
    sv_=X.sheet(f'{base}/SHEET_poses.svg',[(pk,built[pk],canvas) for pk in built],10,280,400,f'{nm} · pose sheet ({len(built)} poses)',cat='Characters',sub=nm)
    if ck in PREV_POSES: preview(f'{ck}_poses',sv_,2400)
    a=rig.cast_args(ck)
    if ck=='shadow': a.update(eyes='glow',brow='none')
    hy=rig.hip_h(a); tcells=[]
    for nmv,extra in (('front',dict(view='front')),('three_quarter',dict(view='side',turn=.35)),('side',dict(view='side',turn=-1)),('back',dict(view='back'))):
        q=dict(a); q.update(extra); q['y']=-hy; c,_=rig.char(**q); tcells.append((nmv,c,None))
        X.save(f'{base}/turnaround/{nmv}.svg',c,title=f'{nm} – {nmv}',cat='Characters',sub=nm)
    X.sheet(f'{base}/SHEET_turnaround.svg',tcells,4,360,520,f'{nm} · turnaround',cat='Characters',sub=nm)
    if ck!='shadow':
        ecells=[]
        for ek in FX.EXPR:
            hf=rig.head_only(turn=1,view='front',expr=ek,**a); h3=rig.head_only(turn=.15,view='side',expr=ek,**a)
            X.save(f'{base}/expressions/front/{ek}.svg',hf,title=f'{nm} – {ek}',cat='Characters',sub=nm)
            X.save(f'{base}/expressions/three_quarter/{ek}.svg',h3,title=f'{nm} – {ek} (3/4)',cat='Characters',sub=nm)
            ecells.append((ek,hf,None))
        X.sheet(f'{base}/SHEET_expressions.svg',ecells,8,220,230,f'{nm} · {len(ecells)} expressions',cat='Characters',sub=nm)
        vcells=[]
        for vk in FX.VISEMES:
            h=rig.head_only(turn=.15,view='side',expr='neutral',mouth=vk,**a)
            X.save(f'{base}/lipsync_visemes/{vk}.svg',h,title=f'{nm} – viseme {FX.VISEME_LABEL[vk]}',cat='Characters',sub=nm); vcells.append((FX.VISEME_LABEL[vk],h,None))
        X.sheet(f'{base}/SHEET_lipsync.svg',vcells,6,240,250,f'{nm} · lip-sync mouth chart',cat='Characters',sub=nm)
    # cycles: 24 fps loops
    ccells=[]
    for cyc in CY.CYCLES:
        frames=[]
        for i in range(CY.N):
            q=CY.frame_params(a,ck,cyc,i,phone_fn=lambda: PO.phone_in_hand())
            c,_=rig.char(**q); frames.append(c)
        vbs=[E.tight(frames[i]) for i in range(0,CY.N,3)]
        Xm=max(max(abs(v[0]),abs(v[0]+v[2])) for v in vbs)+16; y0=min(v[1] for v in vbs)-16
        cv=(-Xm,y0,2*Xm,30-y0)
        for i,c in enumerate(frames):
            X.save(f'{base}/cycles/{cyc}/{cyc}_{i+1:02d}.svg',c,vb=cv,title=f'{nm} – {cyc} frame {i+1}/{CY.N}',cat='Characters',sub=nm,anim=f'{ck}/{cyc}',frame=i,fps=24)
            if i%3==0: ccells.append((f'{cyc} {i+1}',c,cv))
    sv_=X.sheet(f'{base}/SHEET_cycles.svg',ccells,16,170,300,f'{nm} · {len(CY.CYCLES)} motion loops @24fps (every 3rd frame shown)',cat='Characters',sub=nm,write=False)
    from PIL import Image
    im=prev.png(sv_,2720).convert('RGB'); jp=P_(f'{base}/PREVIEW_cycles.jpg'); im.save(jp,quality=84)
    X.MAN.append(dict(cat='Characters',sub=nm,name='PREVIEW_cycles',path=f'{base}/PREVIEW_cycles.jpg',sheet=True))
    if ck in PREV_CYC: preview(f'{ck}_cycles',sv_,2720)
    if ck!='shadow':
        sk,lc=rig.SKINS[a.get('skin','cream')]; hcells=[]
        for hk in rig.HAND_SPEC:
            L=rig.Layer(lc); rig.hand(L,[0,0],180,hk,sk,sc=1); inner=g(L.out(),transform='scale(3)')
            hcells.append((hk,inner,None)); X.save(f'{base}/hands/{hk}.svg',inner,title=f'{nm} – hand {hk}',cat='Characters',sub=nm)
        X.sheet(f'{base}/SHEET_hands.svg',hcells,8,200,230,f'{nm} · {len(hcells)} hand shapes',cat='Characters',sub=nm)
    # puppet kit
    parts,rj=PU.parts(ck); vbsP={}
    for pn,inner in parts.items():
        vb=X.save(f'10_puppet_rigs/{ck}/{pn}.svg',inner,title=f'{nm} – puppet part {pn}',cat='Puppet rigs',sub=nm,probe=(-400,-500,800,800))
        vbsP[pn]=vb
    rj['viewBoxes']=vbsP
    json.dump(rj,open(P_(f'10_puppet_rigs/{ck}/rig.json'),'w'),indent=1)
    return X.MAN,ck,round(time.time()-t0,1),rj
def build_misc():
    X=Ctx()
    # ---------------- cast lineup
    cells=[]
    for ck,cinfo in rig.CAST.items():
        a=rig.cast_args(ck)
        if ck=='shadow': a.update(eyes='glow',brow='none')
        q=dict(a); q['y']=-rig.hip_h(a); q['expr']='happy' if ck!='shadow' else 'neutral'
        c,_=rig.char(**q); cells.append((cinfo['name'],c,(-110,-480,220,510)))
    sv_=X.sheet('01_characters/SHEET_cast_lineup.svg',cells,13,220,560,f'Cast line-up ({len(cells)} characters)',cat='Characters',sub='Cast')
    preview('cast_lineup',sv_,2860)
    cells=[]
    for ck,cinfo in rig.CAST.items():
        a=rig.cast_args(ck)
        if ck=='shadow': a.update(eyes='glow',brow='none')
        q=dict(a); q['y']=-rig.hip_h(a); q['view']='front'; q['expr']='happy' if ck!='shadow' else 'neutral'
        c,_=rig.char(**q); cells.append((cinfo['name'],c,(-110,-480,220,510)))
    X.sheet('01_characters/SHEET_cast_lineup_front.svg',cells,13,220,560,'Cast line-up – front',cat='Characters',sub='Cast')
    # ---------------- face parts
    sk='#ECE4D6'
    eye_kinds=['normal','wide','shock','tiny','happy','closed','tight','squint','sad','angry','tired','sly','worried','teary','dizzy','dead','heart','star','money','glow']
    cells=[]
    for ek in eye_kinds:
        inner=g(ell(0,0,46,30,fill=sk,stroke='#8C8273',stroke_width=1)+FX.eye(ek,-11.5,0,1,0,0,-1,sk,None)+FX.eye(ek,11.5,0,1,0,0,1,sk,None),transform='scale(3)')
        X.save(f'02_face_parts/eyes/eyes_{ek}.svg',inner,cat='Face parts',sub='Eyes'); cells.append((ek,inner,None))
    X.sheet('02_face_parts/SHEET_eyes.svg',cells,5,260,200,'Eyes (pairs) – mix & match',cat='Face parts',sub='Eyes')
    cells=[]
    for bk in [k for k in FX.BROWS if k!='none']:
        inner=g(FX.brow(bk,-11.5,0,1,-1)+FX.brow(bk,11.5,0,1,1),transform='scale(4)')
        X.save(f'02_face_parts/brows/brows_{bk}.svg',inner,cat='Face parts',sub='Brows'); cells.append((bk,inner,None))
    X.sheet('02_face_parts/SHEET_brows.svg',cells,5,240,170,'Eyebrows',bg='#2A3148',cat='Face parts',sub='Brows')
    mouths=['neutral','smile','softsmile','grin','laugh','teeth','frown','bigfrown','flat','tiny','o','O','shout','scream','sadopen','cry','wavy','grit','smirk','tongue','pout','yawn','drool']+FX.VISEMES
    cells=[]
    for mk in mouths:
        inner=g(FX.mouth(mk,0,0,1,sk),transform='scale(4)')
        X.save(f'02_face_parts/mouths/mouth_{mk}.svg',inner,cat='Face parts',sub='Mouths'); cells.append((mk,inner,None))
    X.sheet('02_face_parts/SHEET_mouths.svg',cells,8,200,170,'Mouths + lip-sync visemes',bg='#E6DDCC',cat='Face parts',sub='Mouths')
    cells=[]
    for xk in ['blush','tears','tear','sweat','sweats','gloom','vein','bags','pale','sick','sparkle']:
        inner=g(circ(0,0,39,fill=sk,stroke='#8C8273',stroke_width=2.6)+FX.extras([xk],0,11.5,1,39,sk),transform='scale(2.4)')
        X.save(f'02_face_parts/overlays/fx_{xk}.svg',g(FX.extras([xk],0,11.5,1,39,sk),transform='scale(2.4)'),cat='Face parts',sub='Overlays'); cells.append((xk,inner,None))
    X.sheet('02_face_parts/SHEET_face_overlays.svg',cells,6,220,230,'Face overlays',cat='Face parts',sub='Overlays')
    cells=[]
    HSTY=['short','buzz','spiky','curly','afro','bun','ponytail','pigtails','long','bob','cap','beanie']+list(rig.HAIR_V3)
    for hs in HSTY:
        for vw in ('side','front','back'):
            B,Fh=rig.hair_paths(hs,39,vw,'#3A2A22' if hs!='hijab' else '#7A3B4E')
            inner=g(B+circ(0,0,39,fill=sk,stroke='#8C8273',stroke_width=2.6)+Fh,transform='scale(2.4)')
            X.save(f'02_face_parts/hair/{hs}_{vw}.svg',inner,cat='Face parts',sub='Hair')
            if vw!='back': cells.append((f'{hs} {vw}',inner,None))
    sv_=X.sheet('02_face_parts/SHEET_hair.svg',cells,8,220,240,f'Hair styles ({len(HSTY)}) – side / front (back views in folder)',cat='Face parts',sub='Hair')
    preview('hair_styles',sv_,1760)
    cells=[]
    for bk in ['stubble','full','mustache']+list(rig.BEARD_V3):
        for vw,t in (('front',1),('three_quarter',.15)):
            inner=g(rig.head_only(turn=t,view='front' if vw=='front' else 'side',expr='neutral',**dict(rig.cast_args('alex_hoodie'),beard=bk,hairCol='#3A2A22')),transform='scale(2.4)')
            X.save(f'02_face_parts/beards/{bk}_{vw}.svg',inner,cat='Face parts',sub='Beards'); cells.append((f'{bk} {vw}',inner,None))
    X.sheet('02_face_parts/SHEET_beards.svg',cells,6,220,240,'Beards & moustaches',cat='Face parts',sub='Beards')
    cells=[]
    for ak in AC.HEAD_ACC:
        if ak=='headphones_neck': continue
        for vw,t in (('front',1),('three_quarter',.15),('profile',-1)):
            inner=g(rig.head_only(turn=t,view='front' if vw=='front' else 'side',expr='neutral',**dict(rig.cast_args('alex'),acc=[ak])),transform='scale(2.4)')
            X.save(f'02_face_parts/accessories_on_head/{ak}_{vw}.svg',inner,cat='Face parts',sub='Accessories on head')
            if vw!='profile': cells.append((f'{ak} {vw}',inner,None))
    sv_=X.sheet('02_face_parts/SHEET_accessories_on_head.svg',cells,10,200,230,f'Head accessories ({len(AC.HEAD_ACC)-1}) – front / 3/4 / profile',cat='Face parts',sub='Accessories on head')
    preview('accessories_on_head',sv_,2000)
    # body accessories demo on alex (front + side)
    cells=[]
    for ak in list(AC.BODY_ACC)+list(AC2.BODY2)+list(AC2.WRIST2):
        for vw in ('side','front'):
            a=rig.cast_args('alex_hoodie'); q=dict(a); q['acc']=[ak]; q['y']=-rig.hip_h(a); q['outfit']='tee'
            if vw=='front': q['view']='front'
            c,_=rig.char(**q); X.save(f'02_face_parts/accessories_on_body/{ak}_{vw}.svg',c,cat='Face parts',sub='Accessories on body'); cells.append((f'{ak} {vw}',c,None))
    X.sheet('02_face_parts/SHEET_accessories_on_body.svg',cells,10,180,330,'Body & wrist accessories (worn)',cat='Face parts',sub='Accessories on body')
    # ---------------- props
    PROPS={
     'bedroom':dict(bed_single=PR.bed(),bed_messy=PR.bed(messy=True),bed_someone_under_blanket=PR.bed(lump=True),bed_double=PR.double_bed(),nightstand=PR.nightstand(),lamp_on=PR.lamp(True),lamp_off=PR.lamp(False),wardrobe=PR.wardrobe(),rug=PR.rug(),curtains_open=PR.curtains(openness=.8),curtains_closed=PR.curtains(openness=0),mirror=PR.mirror()),
     'furniture':dict(desk=PR.desk(),table=PR.table(),chair_wood=PR.chair_wood(),office_chair=PR.office_chair(),sofa=PR.sofa(),armchair=PR.armchair(),bookshelf=PR.bookshelf(),wall_shelf=PR.wall_shelf(),wall_shelf_empty=PR.wall_shelf(False),tv_on=PR.tv(),tv_off=PR.tv(on=False),fridge=PR.fridge(),kitchen_counter=PR.kitchen_counter(),stove_pot=PR.stove_pot(),bench=PR.bench()),
     'tech':dict(laptop_open=PR.laptop(),laptop_closed=PR.laptop(False),monitor=PR.monitor(),keyboard=PR.keyboard(),desk_lamp_on=PR.desk_lamp(True),desk_lamp_off=PR.desk_lamp(False),headphones=PR.headphones(),game_controller=PR.game_controller(),battery_low=PR.battery(.1),battery_full=PR.battery(.95)),
     'time':dict(wall_clock=PR.wall_clock(),wall_clock_late=PR.wall_clock(3,47),wall_clock_broken=PR.wall_clock(broken=True),alarm_clock=PR.alarm_clock(),alarm_clock_ringing=PR.alarm_clock(True),digital_clock_0700=PR.digital_clock(),digital_clock_0347=PR.digital_clock('03:47'),hourglass_full=PR.hourglass(.9),hourglass_running_out=PR.hourglass(.15),calendar_deadline=PR.calendar_page(),calendar_month_crossed=PR.calendar_month()),
     'walls_decor':dict(window_night=PR.window(),window_day=PR.window(mode='day'),window_sunset=PR.window(mode='sunset'),window_dawn=PR.window(mode='dawn'),window_night_curtains=PR.window(curtain=.7),window_closed_curtains=PR.window(curtain=0),door_closed=PR.door(),door_half_open=PR.door(.45),door_open=PR.door(.8),picture_landscape=PR.picture_frame(),picture_family=PR.picture_frame('family'),picture_diploma=PR.picture_frame('diploma'),picture_heart=PR.picture_frame('heart'),poster_dream_big=PR.poster(),poster_hustle=PR.poster('HUSTLE 24/7','#4A2A2A'),ceiling_lamp_on=PR.ceiling_lamp(True),ceiling_lamp_off=PR.ceiling_lamp(False),light_switch=PR.light_switch(),wall_outlet=PR.wall_outlet()),
     'objects':dict(mug=PR.mug(),mug_cold=PR.mug(steam=False),coffee_to_go=PR.coffee_cup_togo(),plant_monstera=PR.plant(),plant_cactus=PR.plant('cactus'),plant_dead=PR.plant('dead'),trash_bin=PR.trash_bin(),trash_bin_full=PR.trash_bin(True),crumpled_paper=PR.crumpled_paper(),book_stack=PR.book_stack(5),book_stack_dusty=PR.book_stack(4,True),book_open=PR.book_open(),backpack=PR.backpack(),sneakers=PR.sneakers(),dumbbell=PR.dumbbell(),guitar=PR.guitar(),pizza_box=PR.pizza_box(),water_bottle=PR.water_bottle(),soda_can=PR.soda_can(),pills=PR.pills(),umbrella=PR.umbrella(),box_cardboard=PR.box_cardboard(),shopping_bag=PR.shopping_bag(),scale=PR.scale_weight(),sticky_note=PR.sticky_note(),clipboard_checklist=PR.clipboard(),lightbulb_on=PR.lightbulb(True),lightbulb_off=PR.lightbulb(False)),
     'money_success':dict(money_stack=PR.money_stack(),banknote=PR.banknote(),coins=PR.coins(),wallet_empty=PR.wallet(),wallet_cash=PR.wallet(False),credit_card=PR.credit_card(),house_keys=PR.keys(),graduation_cap=PR.grad_cap(),diploma=PR.diploma_roll(),trophy=PR.trophy(),gift_box=PR.gift_box(),heart=PR.heart_icon(),heart_broken=PR.heart_icon(broken=True)),
     'outdoor':dict(house_day=EN.house(),house_lit=EN.house(lit=True),car=PR.car(),car_blue=PR.car('#3E6A8A'),bicycle=PR.bicycle(),tree_round=PR.tree(),tree_pine=PR.tree('pine'),tree_bare=PR.tree('bare'),street_lamp_on=PR.street_lamp(True),street_lamp_off=PR.street_lamp(False),mailbox=PR.mailbox(),door_mat=PR.door_mat(),cloud=PR.cloud(),rain_cloud=PR.rain_cloud(),sun=PR.sun(),moon=PR.moon(),stars=PR.stars()),
    }
    for cat in PROPS:
        for k in list(PROPS[cat]):
            if k in P2.UPGRADED: PROPS[cat][k]=P2.UPGRADED[k]()
    for cat,items in P2.NEW.items(): PROPS[cat]=dict(items)
    PROPS['beds']=PB.items(); PROPS['vehicles']=PV.items()
    for k,v in PH.GROUPS.items(): PROPS[k]=dict(v)
    for k,v in PW.GROUPS.items(): PROPS[k]=dict(v)
    allcells=[]
    for cat,items in PROPS.items():
        cells=[]
        for k,inner in items.items():
            vb=X.save(f'03_props/{cat}/{k}.svg',inner,title=k.replace('_',' '),cat='Props',sub=cat.replace('_',' '),probe=(-1400,-1400,2800,2000)); cells.append((k,inner,vb)); allcells.append((k,inner,vb))
        sv_=X.sheet(f'03_props/SHEET_{cat}.svg',cells,7,280,280,f'Props · {cat.replace("_"," ")} ({len(cells)})',cat='Props',sub=cat.replace('_',' '))
        if cat in('beds','vehicles','animals','kitchen'): preview(f'props_{cat}',sv_,1960)
    X.sheet('03_props/SHEET_all_props.svg',allcells,16,180,190,f'All props ({len(allcells)})',cat='Props',sub='All')
    # ---------------- phone
    cells=[]
    for k,fn in SC.SCREENS.items():
        scr=fn()
        X.save(f'04_phone/screens_raw_390x844/{k}.svg',scr,vb=(0,0,SC.SW,SC.SH),title=f'Phone screen – {k}',cat='Phone',sub='Screens (raw)')
        dev=SC.phone_device(scr); vb=X.save(f'04_phone/phone_with_screen/{k}.svg',dev,title=f'Phone – {k}',cat='Phone',sub='Phone + screen'); cells.append((k,dev,vb))
    X.sheet('04_phone/SHEET_phone_screens.svg',cells,7,300,560,f'Phone screens ({len(cells)})',cat='Phone',sub='Phone + screen')
    dev_items=dict(phone_front_blank=SC.phone_device(SC.scr_blank()),phone_front_glow=SC.phone_device(SC.scr_lock(),glow=True),phone_back=SC.phone_back(),phone_back_white=SC.phone_back('#E6E2DA'),phone_side=SC.phone_side(),
                   hand_holding_phone_chat=SC.hand_holding_phone(SC.scr_group_chat()),hand_holding_phone_feed=SC.hand_holding_phone(SC.scr_feed()),hand_holding_phone_bank=SC.hand_holding_phone(SC.scr_bank_zero()))
    cells=[]
    for k,inner in dev_items.items(): vb=X.save(f'04_phone/device/{k}.svg',inner,title=k,cat='Phone',sub='Device'); cells.append((k,inner,vb))
    for n,c in SC.APPS: X.save(f'04_phone/app_icons/app_{n.lower()}.svg',SC.app_icon(n,c,-32,-32),title=n,cat='Phone',sub='App icons')
    X.sheet('04_phone/SHEET_device_and_icons.svg',cells+[(f'app_{n.lower()}',SC.app_icon(n,c,-32,-32),None) for n,c in SC.APPS],8,260,420,'Phone device, close-ups, app icons',cat='Phone',sub='Device')
    # ---------------- backgrounds
    cells=[]
    allenv=dict(EN.ENVS); allenv.update(E3.ENVS3)
    for k,fn in allenv.items():
        inner=fn(); X.save(f'05_backgrounds/{k}.svg',inner,vb=(0,0,1920,1080),title=k.replace('_',' '),cat='Backgrounds',sub='Scenes' if k in EN.ENVS else 'Scenes v3',defs_extra=EN.DEFS)
        cells.append((k,f'<defs><clipPath id="cl_{k}"><rect width="1920" height="1080"/></clipPath></defs>'+g(inner,clip_path=f'url(#cl_{k})'),(0,0,1920,1080)))
    sv_=X.sheet('05_backgrounds/SHEET_backgrounds.svg',cells,5,480,300,f'Backgrounds 1920×1080 ({len(cells)})',cat='Backgrounds',sub='Scenes')
    preview('backgrounds',sv_,2400)
    cells=[]
    for k,fn in list(EN.WALLS.items())+list(EN.FLOORS.items()):
        inner=fn(); vb=(0,0,1920,1080) if k.startswith('wall') else (0,0,1920,400)
        X.save(f'05_backgrounds/walls_floors/{k}.svg',inner,vb=vb,cat='Backgrounds',sub='Walls & floors',defs_extra=EN.DEFS)
        cells.append((k,f'<defs><clipPath id="cl_{k}"><rect width="{vb[2]}" height="{vb[3]}"/></clipPath></defs>'+g(inner,clip_path=f'url(#cl_{k})'),vb))
    X.sheet('05_backgrounds/SHEET_walls_floors.svg',cells,4,480,300,'Walls & floors (tileable strips)',cat='Backgrounds',sub='Walls & floors')
    # ---------------- fx
    cells=[]
    for k,fn in FXS.FXS.items():
        inner=fn(); vb=X.save(f'06_fx_icons_bubbles/{k}.svg',inner,title=k,cat='FX & bubbles',sub=k.split('_')[0],probe=(-900,-900,1800,1800)); cells.append((k,inner,vb))
    X.sheet('06_fx_icons_bubbles/SHEET_fx.svg',cells,8,240,230,f'Speech bubbles, emotion icons, FX, UI ({len(cells)})',bg='#3A4560',cat='FX & bubbles',sub='All')
    cells=[]
    for k,fn in fx3.SEQ.items():
        frames=[fn(i/fx3.NF) if k in fx3.LOOPING else fn(i/(fx3.NF-1)) for i in range(fx3.NF)]
        if k=='lightning': vb=(-960,-540,1920,1080)
        else:
            vv=[E.tight(fr,(-900,-900,1800,1800)) for fr in frames[::2]]
            vb=(min(v[0] for v in vv),min(v[1] for v in vv),0,0); vb=(vb[0],vb[1],max(v[0]+v[2] for v in vv)-vb[0],max(v[1]+v[3] for v in vv)-vb[1])
        for i,fr in enumerate(frames):
            X.save(f'06_fx_icons_bubbles/animated/{k}/{k}_{i+1:02d}.svg',fr,vb=vb,cat='FX & bubbles',sub='Animated FX (12 frames)',anim=f'fx/{k}',frame=i,fps=12)
            if i%2==0: cells.append((f'{k} {i+1}',fr,vb))
    sv_=X.sheet('06_fx_icons_bubbles/SHEET_fx_animated.svg',cells,12,180,200,'Animated FX sequences (12 frames, every 2nd shown)',bg='#3A4560',cat='FX & bubbles',sub='Animated FX (12 frames)')
    preview('fx_animated',sv_,2160)
    for k,fn in fx3.OVERLAYS.items(): X.save(f'06_fx_icons_bubbles/overlays_1920x1080/{k}.svg',fn(),vb=(0,0,1920,1080),cat='FX & bubbles',sub='Full-frame overlays')
    # ---------------- example scenes
    import scenes as SCN, scenes3 as SC3
    cells=[]
    allsc=dict(SCN.SCENES); allsc.update(SC3.SCENES3)
    for k,fn in allsc.items():
        inner=fn(); X.save(f'07_example_scenes/{k}.svg',inner,vb=(0,0,1920,1080),title=k.replace('_',' '),cat='Example scenes',sub='Scenes',defs_extra=EN.DEFS)
        cells.append((k,f'<defs><clipPath id="cl_{k}"><rect width="1920" height="1080"/></clipPath></defs>'+g(inner,clip_path=f'url(#cl_{k})'),(0,0,1920,1080)))
    sv_=X.sheet('07_example_scenes/SHEET_example_scenes.svg',cells,4,480,300,f'Example scenes ({len(cells)})',cat='Example scenes',sub='Scenes')
    preview('example_scenes',sv_,1920)
    # ---------------- 08 hands & feet
    cells=[]
    for t in HF.TONES:
        for hk in rig.HAND_SPEC:
            for side,m in (('right',1),('left',-1)):
                inner=HF.hand_svg(hk,t,mirror=m); X.save(f'08_hands_feet/hand_shapes/{t}/{side}/{hk}.svg',inner,cat='Hands & feet',sub=f'Hand shapes – {t}')
                if t=='warm' and side=='right': cells.append((hk,inner,None))
    sv_=X.sheet('08_hands_feet/SHEET_hand_shapes.svg',cells,8,200,230,f'{len(rig.HAND_SPEC)} hand shapes × 5 skin tones × left/right',cat='Hands & feet',sub='Hand shapes – warm')
    preview('hand_shapes',sv_,1600)
    cells=[]
    for t in HF.TONES:
        for an,(keys,n) in HF.ANIMS.items():
            for i,spec in enumerate(HF.seq(keys,n)):
                inner=HF.hand_svg(spec,t); X.save(f'08_hands_feet/finger_animations/{t}/{an}/{an}_{i+1:02d}.svg',inner,vb=(-110,-140,220,190),cat='Hands & feet',sub=f'Finger animations – {t}',anim=f'hand/{t}/{an}',frame=i,fps=12)
                if t=='warm' and i%2==0: cells.append((f'{an} {i+1}',inner,(-110,-140,220,190)))
    sv_=X.sheet('08_hands_feet/SHEET_finger_animations.svg',cells,10,170,200,'Finger animations (blended frame by frame)',cat='Hands & feet',sub='Finger animations – warm')
    preview('finger_animations',sv_,1700)
    cells=[]
    for k,inner in HF.shoes().items():
        vb=X.save(f'08_hands_feet/feet_shoes/{k}.svg',inner,cat='Hands & feet',sub='Feet & shoes'); cells.append((k,inner,vb))
    sv_=X.sheet('08_hands_feet/SHEET_feet_shoes.svg',cells,8,200,170,'Shoes (8 styles × 3 colours, side + front) and bare feet',cat='Hands & feet',sub='Feet & shoes')
    preview('feet_shoes',sv_,1600)
    # ---------------- 09 tattoos
    cells=[]
    for d in TT.DESIGNS:
        inner=TT.flash(d,8); vb=X.save(f'09_tattoos/flash/{d}.svg',inner,cat='Tattoos',sub='Flash designs'); cells.append((d,rect(-80,-90,160,180,rx=6,fill='#F3EAD7')+inner,(-90,-100,180,200)))
    sv_=X.sheet('09_tattoos/SHEET_tattoo_flash.svg',cells,9,200,230,f'Tattoo flash ({len(cells)} designs) – usable on any character via tattoo=["design@slot"]',bg='#2A2224',cat='Tattoos',sub='Flash designs')
    preview('tattoo_flash',sv_,1800)
    cells=[]
    demos=dict(full_sleeves=['sleeve@arm_near','sleeve@arm_far'],forearm_rose=['rose@forearm_near'],upperarm_heart=['heart@upperarm_near','anchor@forearm_far'],wrist_band=['band@wrist_near','infinity@forearm_far'],
               hand_star=['star@hand_near','star@hand_far'],neck_swallow=['swallow@neck'],calf_koi=['koi@calf_near','wave@calf_far'],face_tear=['heart@face'],mixed=['snake@forearm_near','compass@upperarm_near','lotus@forearm_far','moon@neck'])
    for k,tl in demos.items():
        for vw in ('side','front'):
            a=rig.cast_args('alex_hoodie'); q=dict(a); q.update(outfit='summer',tattoo=tl,y=-rig.hip_h(a))
            if vw=='front': q['view']='front'
            c,_=rig.char(**q); X.save(f'09_tattoos/on_body/{k}_{vw}.svg',c,cat='Tattoos',sub='Worn on body'); cells.append((f'{k} {vw}',c,None))
    X.sheet('09_tattoos/SHEET_tattoos_on_body.svg',cells,9,200,330,'Tattoo placement examples (arm, wrist, hand, neck, calf, face)',cat='Tattoos',sub='Worn on body')
    return X.MAN
if __name__=='__main__':
    t0=time.time()
    shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
    keys=list(rig.CAST)
    if len(sys.argv)>2: keys=sys.argv[2].split(',')
    MAN=[]; RIGS={}
    with Pool(4) as pool:
        fut_misc=pool.apply_async(build_misc)
        for man,ck,dt,rj in pool.imap_unordered(build_char,keys):
            MAN+=man; RIGS[ck]=rj; print('char',ck,dt,'s',flush=True)
        MAN+=fut_misc.get(); print('misc done',flush=True)
    json.dump(MAN,open(os.path.join(OUT,'manifest.json'),'w'))
    json.dump(RIGS,open(os.path.join(OUT,'10_puppet_rigs','rigs_all.json'),'w'))
    print('files',len(MAN),'time',round(time.time()-t0))
