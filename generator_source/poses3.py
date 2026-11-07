"""v3 poses: hand-sign gestures, action poses and new front poses (all characters)."""
from sv import *
import poses as PO
def _sit(**o): d=dict(y=70,legIkN=[66,70],legIkF=[58,72]); d.update(o); return d
def wheel_mid(G):
    a=G['handN']; b=G['handF']; c=[(a[0]+b[0])/2+4,(a[1]+b[1])/2+10]
    s=ell(c[0],c[1],8,30,fill='none',stroke='#22252D',stroke_width='7',transform=f'rotate(-14 {f(c[0])} {f(c[1])})')
    s+=path(f'M{f(c[0])} {f(c[1])}L{f(c[0]+40)} {f(c[1]+44)}',stroke='#3A3E47',stroke_width='7',stroke_linecap='round')
    return s
POSES3={
 'peace_sign':   ('Peace sign',dict(aN=[52,104],hN='peace',wN=-6,aF=[-6,14],expr='happy')),
 'ok_sign':      ('OK sign',dict(aN=[44,98],hN='ok',wN=-10,aF=[-6,14],expr='content')),
 'rock_on':      ('Rock on!',dict(lean=-6,head=-10,aN=[132,30],hN='rock',aF=[-10,30],hF='fist',expr='excited',mouth='tongue')),
 'finger_gun':   ('Finger guns',dict(lean=-2,aN=[86,6],hN='finger_gun',wN=0,aF=[-8,14],expr='smug')),
 'call_me':      ('"Call me" sign',dict(head=-4,ikN=[22,-126],hN='call_me',wN=-170,aF=[-6,14],expr='wink')),
 'shh':          ('Shh – finger on lips',dict(head=4,ikN=[34,-118],hN='shh',wN=-184,aF=[-6,14],expr='shy')),
 'beckon':       ('Come here (beckon)',dict(lean=-3,aN=[64,44],hN='beckon',wN=-70,aF=[-6,14],expr='smug')),
 'count_three':  ('Counting on fingers',dict(aN=[56,96],hN='count_3',wN=-4,aF=[30,60],hF='point',wF=-40,expr='thinking',look=(.6,-.4))),
 'salute':       ('Salute',dict(lean=-2,head=-4,ikN=[30,-142],hN='karate',wN=-150,aF=[-4,6],expr='determined')),
 'knock_door':   ('Knocking on a door',dict(lean=4,aN=[78,62],hN='knock',wN=-40,aF=[-6,14],expr='nervous')),
 'punch':        ('Punch',dict(lean=12,head=-6,aN=[92,2],hN='fist',aF=[40,96],hF='fist',lN=[22,10],lF=[-28,8],expr='furious')),
 'kick':         ('Kick',dict(lean=-12,head=-6,lN=[84,4],fN=-20,lF=[-6,4],aN=[-40,40],aF=[50,70],hN='fist',hF='fist',expr='determined')),
 'push':         ('Pushing hard',dict(lean=28,head=-10,ikN=[72,-72],ikF=[68,-66],hN='flat',hF='flat',wN=-90,wF=-90,lN=[18,18],lF=[-36,8],fF=-10,expr='determined',fx=['sweat'])),
 'pull':         ('Pulling a rope',dict(lean=-16,head=-6,ikN=[60,-52],ikF=[52,-48],hN='fist',hF='fist',wN=-90,wF=-90,lN=[24,10],lF=[-12,14],expr='determined',fx=['sweat'])),
 'drive':        ('Driving (seated, wheel)',_sit(lean=4,head=-2,ikN=[78,-60],ikF=[72,-56],hN='grip',hF='grip',wN=-110,wF=-110,expr='focused',mid=wheel_mid)),
 'phone_call':   ('On a phone call',dict(head=6,ikN=[24,-124],hN='grip',wN=-170,holdN=PO.phone_in_hand(glow=False),aF=[-6,14],expr='focused')),
 'idea':         ('Got an idea! (point up)',dict(lean=-4,head=-12,aN=[166,2],hN='point',wN=0,aF=[-6,14],expr='excited',look=(.4,-1))),
 'tie_shoe':     ('Bending to tie a shoe',dict(lean=72,curl=.3,head=14,aN=[-6,22],aF=[2,26],hN='pinch',hF='pinch',lN=[10,6],lF=[-14,4],expr='focused')),
 'sit_crossed':  ('Sitting, legs crossed',_sit(lean=-2,legIkN=[70,40,-1],aN=[30,50],aF=[24,54],hN='relax',hF='relax',expr='smug')),
 'pray_side':    ('Hands together (please)',dict(head=8,ikN=[34,-74],ikF=[32,-72],hN='flat',hF='flat',wN=-160,wF=-160,expr='hopeful')),
 'mic_drop':     ('Mic drop',dict(lean=-6,head=-12,aN=[70,10],hN='open',aF=[-6,14],expr='smug')),
 'stretch_side': ('Side stretch',dict(lean=-6,head=-10,aN=[166,-6],hN='spread',aF=[150,-20],hF='spread',expr='content')),
}
FRONT3={
 'front_peace':    ('Front – peace sign',dict(aN=[30,124],hN='peace',expr='wink')),
 'front_ok':       ('Front – OK sign',dict(aN=[30,112],hN='ok',expr='content')),
 'front_rock':     ('Front – rock on',dict(aN=[160,0],hN='rock',expr='excited',mouth='tongue')),
 'front_count_3':  ('Front – counting three',dict(aN=[26,126],hN='count_3',expr='thinking')),
 'front_salute':   ('Front – salute',dict(ikN=[18,-150,-1],hN='karate',expr='determined')),
 'front_namaste':  ('Front – hands together',dict(ikN=[4,-62,-1],ikF=[-4,-62,-1],hN='flat',hF='flat',expr='content')),
 'front_shh':      ('Front – shh',dict(ikN=[3,-118,-1],hN='shh',expr='shy')),
 'front_wave_both':('Front – waving both hands',dict(aN=[150,-30],aF=[150,-30],hN='spread',hF='spread',expr='joy')),
 'front_shy':      ('Front – shy, hands together',dict(ikN=[-8,-34,-1],ikF=[8,-34,-1],hN='relax',hF='relax',head=10,expr='shy')),
 'front_flex':     ('Front – flexing',dict(aN=[90,92],aF=[90,92],hN='fist',hF='fist',expr='proud')),
 'front_call_me':  ('Front – call me',dict(aN=[30,126],hN='call_me',expr='wink')),
 'front_dance':    ('Front – dance move',dict(aN=[150,20],hN='point',aF=[40,-70],hF='fist',lN=[12,14],expr='joy')),
 'front_finger_gun':('Front – finger gun',dict(aN=[86,0],hN='finger_gun',expr='smug')),
}
