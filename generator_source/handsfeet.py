from sv import *
import rig
TONES=['cream','warm','tan','brown','deep']
def hand_svg(spec,skin,mirror=1,h=180,sc=3):
    sk,lc=rig.SKINS[skin]; L=rig.Layer(lc); rig.hand(L,[0,0],h,spec,sk,mirror=mirror); return g(L.out(),transform=f'scale({sc})')
def seq(keys,n):
    """keys: list of hand names; evenly blended into n frames (ease in/out)"""
    out=[]; segs=len(keys)-1
    for i in range(n):
        t=i/(n-1)*segs; j=min(int(t),segs-1); u=t-j; u=.5-.5*math.cos(u*math.pi)
        out.append(rig.hand_lerp(keys[j],keys[j+1],u))
    return out
ANIMS={
 'open_to_fist':(['open','relax','grip','fist'],12),
 'fist_to_point':(['fist','point'],12),
 'count_1_to_5':(['fist','count_1','count_2','count_3','count_4','count_5'],20),
 'wave_loop':(['wave_a','wave_b','wave_a','wave_b','wave_a'],16),
 'grab':(['spread','grab','fist'],12),
 'ok_pop':(['relax','ok'],10),
 'finger_tap':(['point','tap','point','tap','point'],12),
 'beckon_loop':(['point','beckon','point','beckon','point'],16),
 'pinch_zoom':(['pinch','spread','pinch'],14),
 'thumbs_up_pop':(['fist','thumb'],10),
}
def shoes():
    o={}
    for st in ('sneaker','boot','heel','dress','sandal','slipper','flat','hightop'):
        for i,c in enumerate(('#E9A23B','#2F333B','#B8463A')):
            o[f'{st}_{i+1}_side']=rig.shoe([0,0],90,c,'#F4EFE6',sc=3,style=st)
            o[f'{st}_{i+1}_front']=g(rig.shoe_front([0,0],c,'#F4EFE6',style=st),transform='scale(3)')
    for t in TONES:
        sk,lc=rig.SKINS[t]
        L=rig.Layer(lc); L.st('M-5 0 Q10 2.5 25 0',15.5,sk); L.st('M0 -40 L0 -2',21,sk)
        o[f'barefoot_{t}_side']=g(L.out()+''.join(circ(20+i*2.2,5-i*.4,1.2,fill=lc,opacity='.5') for i in range(3)),transform='scale(3)')
        L=rig.Layer(lc); L.st('M0 -40 L0 -2',21,sk); L.e(0,4,10,7,0,sk)
        o[f'barefoot_{t}_front']=g(L.out()+''.join(path(f'M{x} 6 l0 3',stroke=lc,stroke_width=1,opacity='.6') for x in (-6,-2,2,6)),transform='scale(3)')
    return o
