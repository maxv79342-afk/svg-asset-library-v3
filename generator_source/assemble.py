import sys,json,os,re,math
sys.path.insert(0,'/home/user/gen')
from sv import *
def inner_of(path):
    s=open(path).read(); m=re.search(r'<svg[^>]*>(.*)</svg>',s,re.S); x=m.group(1)
    return re.sub(r'<title>.*?</title>','',x)
def assemble(root,ck,angles,hands=('relax','relax'),expr='happy'):
    R=json.load(open(f'{root}/10_puppet_rigs/{ck}/rig.json')); B=R['bones']
    P=lambda n: inner_of(f'{root}/10_puppet_rigs/{ck}/{n}.svg')
    def rot(a): return f'rotate({f(-a)})'
    def chain(side,z):
        ua=B['upper_arm_'+side]; fa=B['forearm_'+side]
        hand=g(P('hand_'+hands[0 if side=='near' else 1]),transform=f'translate(0 {f(fa["length"])}) {rot(angles.get("hand_"+side,0))}')
        fore=g(P('forearm_'+side)+hand,transform=f'translate(0 {f(ua["length"])}) {rot(angles.get("forearm_"+side,0))}')
        arm=g(P('upper_arm_'+side)+fore,transform=f'translate({f(ua["attach"][0])} {f(ua["attach"][1])}) {rot(angles.get("upper_arm_"+side,0))}')
        th=B['thigh_'+side]; sh=B['shin_'+side]
        foot=g(P('foot_'+side),transform=f'translate(0 {f(sh["length"])}) {rot(angles.get("foot_"+side,0))}')
        shin=g(P('shin_'+side)+foot,transform=f'translate(0 {f(th["length"])}) {rot(angles.get("shin_"+side,0))}')
        leg=g(P('thigh_'+side)+shin,transform=f'translate({f(th["attach"][0])} {f(th["attach"][1])}) {rot(angles.get("thigh_"+side,0))}')
        return arm,leg
    aF,lF=chain('far',0); aN,lN=chain('near',1)
    hp=B['head']['pivot_in_part']
    head=g(g(P('head_'+expr),transform=f'translate({f(-hp[0])} {f(-hp[1])})'),transform=f'translate({f(B["head"]["attach"][0])} {f(B["head"]["attach"][1])}) {rot(angles.get("head",0))}')
    return aF+lF+lN+P('torso')+head+aN
if __name__=='__main__':
    root=sys.argv[1]; import prev, export as E
    s=rect(0,0,1600,520,fill='#2A3148')
    poses=[{},dict(upper_arm_near=150,forearm_near=-30,thigh_near=20,shin_near=-30,thigh_far=-20,shin_far=-10),dict(upper_arm_near=-24,forearm_near=28,upper_arm_far=24,forearm_far=18,thigh_near=26,shin_near=-6,thigh_far=-26,shin_far=-50)]
    for i,ck in enumerate(['kai','sara','alex_hoodie','rocky','zoe']):
        for j,a in enumerate(poses[:2] if i else poses):
            x=120+i*300+j*120; s+=g(assemble(root,ck,a,hands=('peace' if j else 'relax','relax')),transform=f'translate({x} 330) scale(.9)')
    prev.png(doc(s,(0,0,1600,520),defs=E.GDEFS),1600,'/home/user/output/assembled.png')
