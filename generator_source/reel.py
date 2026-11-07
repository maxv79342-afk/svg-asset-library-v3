import sys,os,subprocess; sys.path.insert(0,'/home/user/gen')
from sv import *
import rig, cycles3 as CY, poses as PO, env as EN, env3 as E3, export as E, cairosvg
OUT=sys.argv[1]; tmp='/home/user/reel_frames'; os.makedirs(tmp,exist_ok=True)
cast=[('alex_hoodie','walk_happy'),('sara','walk'),('kai','dance'),('luna','wave'),('jay','run'),('zoe','jump'),('rocky','cheer'),('dr_hana','talk'),('grandma','walk_sad'),('chef_marco','laugh'),('officer_dan','nod_yes'),('elena','walk_strut')]
bg=E3.tehran('night')
NF=48
for fi in range(NF):
    s=bg+rect(0,0,1920,1080,fill='#000',opacity='.25')
    for j,(ck,cy) in enumerate(cast):
        a=rig.cast_args(ck); q=CY.frame_params(a,ck,cy,fi%24,phone_fn=lambda: PO.phone_in_hand())
        col=j%6; row=j//6; x=190+col*308; ground=560+row*470; sc=.92
        q['x']=x; q['y']=ground+q['y']*sc; q['s']=sc
        c,_=rig.char(**q); s+=c+text(f'{ck} · {cy}',x,ground+34,size=20,fill='#ECE4D6',anchor='middle',weight=700)
    svg=doc(s,(0,0,1920,1080),defs=E.GDEFS+EN.DEFS)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f'{tmp}/f{fi:03d}.png',output_width=1280)
os.makedirs(os.path.dirname(OUT),exist_ok=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','24','-stream_loop','2','-i',f'{tmp}/f%03d.png','-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-movflags','+faststart',OUT],check=True)
print('ok')
