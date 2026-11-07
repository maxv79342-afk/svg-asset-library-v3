import os, re, math, json, shutil
from sv import *
import props2 as P2, acc as AC
import rig, face as FX, poses as PO, props as PR, screens as SC, env as EN, fx as FXS, export as E, prev
OUT='/home/user/build_orig'
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
MAN=[]  # manifest entries: (category, sub, name, relpath)
def P_(*a):
    p=os.path.join(OUT,*a); os.makedirs(os.path.dirname(p),exist_ok=True); return p
def strip_ids(svg): return re.sub(r'<g id="[^"]+"',"<g",svg)
def save(rel,inner,vb=None,title=None,cat='',sub='',probe=None,defs_extra=''):
    full=P_(rel)
    if vb is None: vb=E.tight(inner,probe or (-1200,-1400,2400,2000))
    d=E.used_defs(inner)+defs_extra
    open(full,'w').write(doc(inner,vb,defs=d,title=title))
    MAN.append(dict(cat=cat,sub=sub,name=os.path.splitext(os.path.basename(rel))[0],path=rel))
    return vb
def sheet(rel,cells,cols,cw,ch,title,bg='#1C2233',label=True,cat='',sub='',scale_to_fit=True):
    rows=(len(cells)-1)//cols+1; Wd=cols*cw; Ht=rows*ch+90
    s=rect(0,0,Wd,Ht,fill=bg)+text(title,40,58,size=34,fill='#ECE4D6',weight=800)
    for i,(name,inner,vb) in enumerate(cells):
        cx=(i%cols)*cw; cy=90+(i//cols)*ch
        s+=rect(cx+8,cy+8,cw-16,ch-16,rx=14,fill=light(bg,.04))
        if vb is None: vb=E.tight(inner)
        sc=min((cw-40)/vb[2],(ch-(70 if label else 40))/vb[3]) if scale_to_fit else 1
        s+=g(strip_ids(inner),transform=f'translate({f(cx+cw/2-(vb[0]+vb[2]/2)*sc)} {f(cy+(ch-(30 if label else 0))/2-(vb[1]+vb[3]/2)*sc)}) scale({f(sc)})')
        if label: s+=text(name,cx+cw/2,cy+ch-22,size=16,fill='#9AA3B8',anchor='middle')
    defs=E.used_defs(s)+(EN.DEFS if 'url(#wallShade' in s or 'url(#sky' in s else '')
    open(P_(rel),'w').write(doc(s,(0,0,Wd,Ht),defs=E.GDEFS+EN.DEFS,title=title))
    MAN.append(dict(cat=cat,sub=sub,name=os.path.splitext(os.path.basename(rel))[0],path=rel,sheet=True))
    return doc(s,(0,0,Wd,Ht),defs=E.GDEFS+EN.DEFS)
PREV=[]
def preview(name,svg,w=2400):
    p=P_('_previews',name+'.png'); prev.png(svg,w,p); PREV.append(p)
PHONE_POSES={'phone_look','phone_shock','phone_scroll_sad','sit_phone','lie_phone','front_call'}
def pose_args(ck,pk,pp):
    a=rig.cast_args(ck)
    if ck=='shadow': a['eyes']='glow'; a['brow']='none'
    q=dict(a); q.update(pp)
    if a.get('acc') or pp.get('acc'): q['acc']=list(dict.fromkeys(list(a.get('acc') or [])+list(pp.get('acc') or [])))
    if pk.startswith('front'): q.setdefault('view','front')
    if pk in PHONE_POSES: q['holdN']=PO.phone_in_hand(glow=pk!='front_call')
    if ck=='shadow': q['expr']=q.get('expr','neutral'); q['eyes']='glow'; q['brow']='none'; q['fx']=[]
    hy=rig.hip_h(a)
    q['x']=q.pop('x',0); q['y']=-hy+q.pop('y',0)
    return q
GROUND={'kneel','sit_floor_hug','front_meditate','sneak','bow'}
ALLPOSES=dict(PO.POSES); ALLPOSES.update(PO.FRONT); ALLPOSES.update(PO.BACK)
# ======================= CHARACTERS =======================
for ck,cinfo in rig.CAST.items():
    base=f'01_characters/{ck}'
    nm=cinfo['name']
    # --- poses (fixed canvas per character)
    built={}
    for pk,(desc,pp) in ALLPOSES.items():
        q=pose_args(ck,pk,pp); c,_=rig.char(**q)
        if pk.startswith('lie') or pk in GROUND:
            q2=dict(q); q2['holdN']=None; q2['holdF']=None; q2['mid']=None
            c2,_=rig.char(**q2); vb=E.tight(c2,pad=0)
            q['y']-=(vb[1]+vb[3])-2; c,_=rig.char(**q)
        built[pk]=c
    vbs=[E.tight(c) for c in built.values()]
    x0=min(v[0] for v in vbs); y0=min(v[1] for v in vbs); x1=max(v[0]+v[2] for v in vbs); y1=max(v[1]+v[3] for v in vbs)
    X=max(abs(x0),abs(x1)); canvas=(-X,y0,2*X,max(y1,30)-y0)
    for pk,c in built.items():
        save(f'{base}/poses/{pk}.svg',c,vb=canvas,title=f'{nm} – {ALLPOSES[pk][0]}',cat='Characters',sub=nm)
    cells=[(pk,built[pk],canvas) for pk in built]
    sv_=sheet(f'{base}/SHEET_poses.svg',cells,8,300,420,f'{nm} · pose sheet ({len(cells)} poses)',cat='Characters',sub=nm)
    if ck in('alex','maya_dressed','alex_hoodie','alex_commute','nora'): preview(f'{ck}_poses',sv_)
    # --- turnaround
    a=rig.cast_args(ck)
    if ck=='shadow': a.update(eyes='glow',brow='none')
    hy=rig.hip_h(a)
    tcells=[]
    for nmv,extra in (('front',dict(view='front')),('three_quarter',dict(view='side',turn=.35)),('side',dict(view='side',turn=-1)),('back',dict(view='back'))):
        q=dict(a); q.update(extra); q['y']=-hy
        c,_=rig.char(**q); tcells.append((nmv,c,None))
        save(f'{base}/turnaround/{nmv}.svg',c,title=f'{nm} – {nmv}',cat='Characters',sub=nm)
    sv_=sheet(f'{base}/SHEET_turnaround.svg',tcells,4,360,520,f'{nm} · turnaround',cat='Characters',sub=nm)
    if ck=='alex': preview('cast_turnaround_alex',sv_,1440)
    # --- expressions (front + 3/4 heads)
    if ck!='shadow':
        ecells=[]
        for ek in FX.EXPR:
            hf=rig.head_only(turn=1,view='front',expr=ek,**a); h3=rig.head_only(turn=.15,view='side',expr=ek,**a)
            save(f'{base}/expressions/front/{ek}.svg',hf,title=f'{nm} – {ek}',cat='Characters',sub=nm)
            save(f'{base}/expressions/three_quarter/{ek}.svg',h3,title=f'{nm} – {ek} (3/4)',cat='Characters',sub=nm)
            ecells.append((ek,hf,None))
        sv_=sheet(f'{base}/SHEET_expressions.svg',ecells,8,220,230,f'{nm} · {len(ecells)} expressions',cat='Characters',sub=nm)
        if ck in('alex','maya_dressed','leo'): preview(f'{ck}_expressions',sv_,1760)
        vcells=[]
        for vk in FX.VISEMES:
            h=rig.head_only(turn=.15,view='side',expr='neutral',mouth=vk,**a)
            save(f'{base}/lipsync_visemes/{vk}.svg',h,title=f'{nm} – viseme {FX.VISEME_LABEL[vk]}',cat='Characters',sub=nm)
            vcells.append((FX.VISEME_LABEL[vk],h,None))
        sheet(f'{base}/SHEET_lipsync.svg',vcells,6,240,250,f'{nm} · lip-sync mouth chart',cat='Characters',sub=nm)
    # --- cycles
    ccells=[]
    for kind,fn in (('walk',PO.walk),('walk_sad',lambda ph: PO.walk(ph,sad=True)),('run',PO.run)):
        frames=[]
        for i in range(8):
            q=dict(a); q.update(fn(i/8*2*math.pi)); q['y']=-hy+q.pop('y',0)
            c,_=rig.char(**q); frames.append(c)
        vbs=[E.tight(c) for c in frames]
        X=max(max(abs(v[0]),abs(v[0]+v[2])) for v in vbs); y0=min(v[1] for v in vbs)
        cv=(-X,y0,2*X,30-y0)
        for i,c in enumerate(frames):
            save(f'{base}/cycles/{kind}_{i+1:02d}.svg',c,vb=cv,title=f'{nm} – {kind} frame {i+1}/8',cat='Characters',sub=nm)
            ccells.append((f'{kind} {i+1}',c,cv))
    sv_=sheet(f'{base}/SHEET_cycles.svg',ccells,8,240,400,f'{nm} · walk / sad walk / run cycles (8 frames, loop)',cat='Characters',sub=nm)
    if ck=='alex_hoodie': preview('alex_hoodie_cycles',sv_,1920)
    # --- hands
    if ck!='shadow':
        sk,lc=rig.SKINS[a.get('skin','cream')]
        hcells=[]
        for hk in rig.HANDS:
            L=rig.Layer(lc); rig.hand(L,[0,0],180,hk,sk,sc=1); inner=g(L.out(),transform='scale(3)')
            hcells.append((hk,inner,None))
            save(f'{base}/hands/{hk}.svg',inner,title=f'{nm} – hand {hk}',cat='Characters',sub=nm)
        sheet(f'{base}/SHEET_hands.svg',hcells,5,220,240,f'{nm} · hand shapes',cat='Characters',sub=nm)
# cast lineup
cells=[]
for ck,cinfo in rig.CAST.items():
    a=rig.cast_args(ck)
    if ck=='shadow': a.update(eyes='glow',brow='none')
    q=dict(a); q['y']=-rig.hip_h(a); q['expr']='happy' if ck!='shadow' else 'neutral'
    c,_=rig.char(**q); cells.append((cinfo['name'],c,(-110,-470,220,500)))
sv_=sheet('01_characters/SHEET_cast_lineup.svg',cells,13,220,560,'Cast line-up',cat='Characters',sub='Cast')
preview('cast_lineup',sv_,2420)
# ======================= FACE PARTS =======================
sk='#ECE4D6'
eye_kinds=['normal','wide','shock','tiny','happy','closed','tight','squint','sad','angry','tired','sly','worried','teary','dizzy','dead','heart','star','money','glow']
cells=[]
for ek in eye_kinds:
    inner=g(ell(0,0,46,30,fill=sk,stroke='#8C8273',stroke_width=1)+FX.eye(ek,-11.5,0,1,0,0,-1,sk,None)+FX.eye(ek,11.5,0,1,0,0,1,sk,None),transform='scale(3)')
    save(f'02_face_parts/eyes/eyes_{ek}.svg',inner,cat='Face parts',sub='Eyes'); cells.append((ek,inner,None))
sheet('02_face_parts/SHEET_eyes.svg',cells,5,260,200,'Eyes (pairs) – mix & match',cat='Face parts',sub='Eyes')
cells=[]
for bk in [k for k in FX.BROWS if k!='none']:
    inner=g(FX.brow(bk,-11.5,0,1,-1)+FX.brow(bk,11.5,0,1,1),transform='scale(4)')
    save(f'02_face_parts/brows/brows_{bk}.svg',inner,cat='Face parts',sub='Brows'); cells.append((bk,inner,None))
sheet('02_face_parts/SHEET_brows.svg',cells,5,240,170,'Eyebrows',bg='#ECE4D6' if False else '#2A3148',cat='Face parts',sub='Brows')
mouths=['neutral','smile','softsmile','grin','laugh','teeth','frown','bigfrown','flat','tiny','o','O','shout','scream','sadopen','cry','wavy','grit','smirk','tongue','pout','yawn','drool']+FX.VISEMES
cells=[]
for mk in mouths:
    inner=g(FX.mouth(mk,0,0,1,sk),transform='scale(4)')
    save(f'02_face_parts/mouths/mouth_{mk}.svg',inner,cat='Face parts',sub='Mouths'); cells.append((mk,inner,None))
sv_=sheet('02_face_parts/SHEET_mouths.svg',cells,8,200,170,'Mouths + lip-sync visemes',bg='#E6DDCC',cat='Face parts',sub='Mouths')
preview('face_parts_mouths',sv_,1600)
cells=[]
for xk in ['blush','tears','tear','sweat','sweats','gloom','vein','bags','pale','sick','sparkle']:
    inner=g(circ(0,0,39,fill=sk,stroke='#8C8273',stroke_width=2.6)+FX.extras([xk],0,11.5,1,39,sk),transform='scale(2.4)')
    save(f'02_face_parts/overlays/fx_{xk}.svg',g(FX.extras([xk],0,11.5,1,39,sk),transform='scale(2.4)'),cat='Face parts',sub='Overlays'); cells.append((xk,inner,None))
sheet('02_face_parts/SHEET_face_overlays.svg',cells,6,220,230,'Face overlays (blush, tears, sweat, gloom...)',cat='Face parts',sub='Overlays')
# hair
cells=[]
for hs in ['short','buzz','spiky','curly','afro','bun','ponytail','pigtails','long','bob','cap','beanie']:
    for vw in ('side','front','back'):
        B,Fh=rig.hair_paths(hs,39,vw,'#3A2A22')
        inner=g(B+circ(0,0,39,fill=sk,stroke='#8C8273',stroke_width=2.6)+Fh,transform='scale(2.4)')
        save(f'02_face_parts/hair/{hs}_{vw}.svg',inner,cat='Face parts',sub='Hair')
        if vw!='back': cells.append((f'{hs} {vw}',inner,None))
sheet('02_face_parts/SHEET_hair.svg',cells,8,220,240,'Hair styles (side / front, back views in folder)',cat='Face parts',sub='Hair')
cells=[]
for ak in AC.HEAD_ACC:
    if ak=='headphones_neck': continue
    for vw,t in (('front',1),('three_quarter',.15),('profile',-1)):
        inner=g(rig.head_only(turn=t,view='front' if vw=='front' else 'side',expr='neutral',**dict(rig.cast_args('alex'),acc=[ak])),transform='scale(2.4)')
        save(f'02_face_parts/accessories_on_head/{ak}_{vw}.svg',inner,cat='Face parts',sub='Accessories on head')
        if vw!='profile': cells.append((f'{ak} {vw}',inner,None))
sv_=sheet('02_face_parts/SHEET_accessories_on_head.svg',cells,8,220,240,'Head accessories (glasses, headphones, earrings, clips) – front / 3/4 / profile',cat='Face parts',sub='Accessories on head')
preview('accessories_on_head',sv_,1760)
# ======================= PROPS =======================
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
allcells=[]
for cat,items in PROPS.items():
    cells=[]
    for k,inner in items.items():
        vb=save(f'03_props/{cat}/{k}.svg',inner,title=k.replace('_',' '),cat='Props',sub=cat.replace('_',' ')); cells.append((k,inner,vb)); allcells.append((k,inner,vb))
    sheet(f'03_props/SHEET_{cat}.svg',cells,6,280,280,f'Props · {cat.replace("_"," ")}',cat='Props',sub=cat.replace('_',' '))
sv_=sheet('03_props/SHEET_all_props.svg',allcells,12,220,230,f'All props ({len(allcells)})',cat='Props',sub='All')
preview('props_all',sv_,2640)
# ======================= PHONE =======================
cells=[];cells2=[]
for k,fn in SC.SCREENS.items():
    scr=fn()
    save(f'04_phone/screens_raw_390x844/{k}.svg',scr,vb=(0,0,SC.SW,SC.SH),title=f'Phone screen – {k}',cat='Phone',sub='Screens (raw)')
    dev=SC.phone_device(scr); vb=save(f'04_phone/phone_with_screen/{k}.svg',dev,title=f'Phone – {k}',cat='Phone',sub='Phone + screen'); cells.append((k,dev,vb))
sv_=sheet('04_phone/SHEET_phone_screens.svg',cells,7,300,560,f'Phone screens ({len(cells)})',cat='Phone',sub='Phone + screen')
preview('phone_screens',sv_,2100)
dev_items=dict(phone_front_blank=SC.phone_device(SC.scr_blank()),phone_front_glow=SC.phone_device(SC.scr_lock(),glow=True),phone_back=SC.phone_back(),phone_back_white=SC.phone_back('#E6E2DA'),phone_side=SC.phone_side(),
               hand_holding_phone_chat=SC.hand_holding_phone(SC.scr_group_chat()),hand_holding_phone_feed=SC.hand_holding_phone(SC.scr_feed()),hand_holding_phone_bank=SC.hand_holding_phone(SC.scr_bank_zero()))
cells=[]
for k,inner in dev_items.items(): vb=save(f'04_phone/device/{k}.svg',inner,title=k,cat='Phone',sub='Device'); cells.append((k,inner,vb))
cells+= [(f'app_{n.lower()}',SC.app_icon(n,c,-32,-32),None) for n,c in SC.APPS]
for n,c in SC.APPS: save(f'04_phone/app_icons/app_{n.lower()}.svg',SC.app_icon(n,c,-32,-32),title=n,cat='Phone',sub='App icons')
sheet('04_phone/SHEET_device_and_icons.svg',cells,8,260,420,'Phone device, close-ups, app icons',cat='Phone',sub='Device')
# ======================= BACKGROUNDS =======================
cells=[]
for k,fn in EN.ENVS.items():
    inner=fn(); save(f'05_backgrounds/{k}.svg',inner,vb=(0,0,1920,1080),title=k.replace('_',' '),cat='Backgrounds',sub='Scenes',defs_extra=EN.DEFS)
    cells.append((k,f'<defs><clipPath id="cl_{k}"><rect width="1920" height="1080"/></clipPath></defs>'+g(inner,clip_path=f'url(#cl_{k})'),(0,0,1920,1080)))
sv_=sheet('05_backgrounds/SHEET_backgrounds.svg',cells,4,480,300,f'Backgrounds 1920×1080 ({len(cells)})',cat='Backgrounds',sub='Scenes')
preview('backgrounds',sv_,1920)
cells=[]
for k,fn in list(EN.WALLS.items())+list(EN.FLOORS.items()):
    inner=fn(); vb=(0,0,1920,1080) if k.startswith('wall') else (0,0,1920,400)
    save(f'05_backgrounds/walls_floors/{k}.svg',inner,vb=vb,cat='Backgrounds',sub='Walls & floors',defs_extra=EN.DEFS)
    cells.append((k,f'<defs><clipPath id="cl_{k}"><rect width="{vb[2]}" height="{vb[3]}"/></clipPath></defs>'+g(inner,clip_path=f'url(#cl_{k})'),vb))
sheet('05_backgrounds/SHEET_walls_floors.svg',cells,4,480,300,'Walls & floors (tileable strips)',cat='Backgrounds',sub='Walls & floors')
# ======================= FX =======================
cells=[]
for k,fn in FXS.FXS.items():
    inner=fn(); vb=save(f'06_fx_icons_bubbles/{k}.svg',inner,title=k,cat='FX & bubbles',sub=k.split('_')[0],probe=(-900,-900,1800,1800)); cells.append((k,inner,vb))
sv_=sheet('06_fx_icons_bubbles/SHEET_fx.svg',cells,8,240,230,f'Speech bubbles, emotion icons, FX, UI ({len(cells)})',bg='#3A4560',cat='FX & bubbles',sub='All')
preview('fx_bubbles',sv_,1920)
print('files',len(MAN))
# ======================= EXAMPLE SCENES =======================
import scenes as SCN
cells=[]
for k,fn in SCN.SCENES.items():
    inner=fn(); save(f'07_example_scenes/{k}.svg',inner,vb=(0,0,1920,1080),title=k.replace('_',' '),cat='Example scenes',sub='Scenes',defs_extra=EN.DEFS)
    cells.append((k,f'<defs><clipPath id="cl_{k}"><rect width="1920" height="1080"/></clipPath></defs>'+g(inner,clip_path=f'url(#cl_{k})'),(0,0,1920,1080)))
sv_=sheet('07_example_scenes/SHEET_example_scenes.svg',cells,4,480,300,'Example scenes – everything combined',cat='Example scenes',sub='Scenes')
preview('example_scenes',sv_,1920)
json.dump(MAN,open(os.path.join(OUT,'manifest.json'),'w'))
print('files',len(MAN))
