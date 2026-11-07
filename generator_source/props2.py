"""v2 props: upgraded versions of the simplest props + new items. Ground/bottom at y=0 unless noted."""
from sv import *
import math
LW = 2.6
def S(c, k=.55, w=LW): return dict(fill=c, stroke=dark(c, k), stroke_width=w, stroke_linejoin='round')
def hi(d, c='#ffffff', op='.45', w=3): return path(d, fill='none', stroke=c, stroke_width=w, stroke_linecap='round', opacity=op)
def shade(d, op='.18'): return path(d, fill='#000', opacity=op)
INK = '#2C2A30'; GOLD = '#E3B24A'

# ------------------------------------------------ upgraded
def headphones(c='#2F333B', pad='#E2725B'):
    s = path('M-78 -70 Q-80 -178 0 -180 Q80 -178 78 -70', fill='none', stroke=dark(c, .45), stroke_width=20, stroke_linecap='round')
    s += path('M-78 -70 Q-80 -178 0 -180 Q80 -178 78 -70', fill='none', stroke=c, stroke_width=13, stroke_linecap='round')
    s += path('M-50 -160 Q0 -186 50 -160', fill='none', stroke=pad, stroke_width=6, stroke_linecap='round', opacity='.9')
    for sx in (-1, 1):
        x = sx * 84
        s += rect(x - 22, -102, 44, 82, rx=20, **S(c))
        s += rect(x - 14 - sx * 4, -92, 26, 62, rx=12, fill=pad, stroke=dark(pad, .45), stroke_width=2)
        s += hi(f'M{x-sx*12} -88 L{x-sx*12} -40', '#fff', '.35', 3)
    return s

def umbrella(c='#3E6A8A'):
    ln = dark(c, .55)
    s = path('M0 -300 L0 -40', stroke='#3A3E47', stroke_width=7, stroke_linecap='round')
    s += path('M0 -40 Q0 -6 -28 -10', fill='none', stroke='#5A3E2A', stroke_width=10, stroke_linecap='round')
    s += path('M-150 -260 Q-140 -372 0 -380 Q140 -372 150 -260 Q125 -276 100 -260 Q75 -278 50 -260 Q25 -278 0 -260 Q-25 -278 -50 -260 Q-75 -278 -100 -260 Q-125 -276 -150 -260Z', fill=c, stroke=ln, stroke_width=3, stroke_linejoin='round')
    for x in (-100, -50, 0, 50, 100):
        s += path(f'M0 -380 Q{x*.55} -330 {x} -260', fill='none', stroke=ln, stroke_width=2, opacity='.5')
    s += path('M-50 -380 Q-140 -360 -150 -260 Q-125 -276 -100 -260 Q-90 -340 -50 -380Z', fill=light(c, .2), opacity='.6')
    s += path('M0 -380 L0 -400', stroke='#3A3E47', stroke_width=6, stroke_linecap='round')
    return s

def water_bottle(c='#8FC9F5'):
    s = rect(-28, -196, 56, 192, rx=18, fill=c, fill_opacity='.7', stroke=dark(c, .55), stroke_width=LW)
    s += rect(-28, -120, 56, 52, fill='#3E6A8A', opacity='.85')
    s += path('M-28 -60 Q0 -52 28 -60 L28 -20 Q0 -12 -28 -20Z', fill=light(c, .2), opacity='.6')
    s += rect(-18, -224, 36, 32, rx=7, **S('#2F333B'))
    s += path('M18 -214 Q36 -214 36 -196 Q36 -186 22 -186', fill='none', stroke='#2F333B', stroke_width=5)
    s += hi('M-14 -180 L-14 -30', '#fff', '.6', 5)
    s += text('H2O', 0, -88, size=18, fill='#EAF4FF', weight=800, anchor='middle')
    return s

def soda_can(c='#D6453A'):
    s = path('M-28 -120 L28 -120 L30 -110 L30 -12 L26 0 L-26 0 L-30 -12 L-30 -110Z', **S(c))
    s += ell(0, -120, 28, 7, fill='#C9CED6', stroke='#8A9099', stroke_width=2)
    s += ell(6, -121, 7, 3, fill='#8A9099')
    s += path('M-30 -46 C-10 -80 10 -30 30 -64 L30 -48 C10 -14 -10 -64 -30 -30Z', fill='#fff')
    s += rect(-30, -12, 60, 8, fill='#C9CED6')
    s += hi('M-18 -104 L-18 -20', '#fff', '.35', 5)
    return s

def shopping_bag(c='#E8C468', logo='#C8573E'):
    ln = dark(c, .5)
    s = path('M-34 -150 Q-34 -210 0 -210 Q34 -210 34 -150', fill='none', stroke=ln, stroke_width=8)
    s += path('M-74 -152 L74 -152 L84 0 L-84 0Z', **S(c))
    s += path('M74 -152 L96 -136 L104 -12 L84 0Z', **S(dark(c, .15)))
    s += path('M-74 -152 L-58 -132 L58 -132 L74 -152', fill=dark(c, .1), stroke=ln, stroke_width=2)
    s += circ(0, -70, 30, fill='none', stroke=logo, stroke_width=6) + path('M-14 -70 L14 -70', stroke=logo, stroke_width=6, stroke_linecap='round')
    return s

def backpack(c='#C8573E'):
    ln = dark(c, .55)
    s = path('M-30 -176 Q0 -206 30 -176', fill='none', stroke=ln, stroke_width=9, stroke_linecap='round')
    s += rect(-70, -180, 140, 180, rx=46, **S(c))
    s += rect(-52, -82, 104, 70, rx=18, **S(dark(c, .12)))
    s += path('M-52 -62 L52 -62', stroke=ln, stroke_width=2.4)
    s += rect(-10, -70, 20, 10, rx=3, fill=GOLD, stroke=ln, stroke_width=1.6)
    s += path('M-70 -120 Q0 -136 70 -120', fill='none', stroke=ln, stroke_width=2.4)
    s += rect(-82, -110, 14, 74, rx=6, **S(dark(c, .2))) + rect(68, -110, 14, 74, rx=6, **S(dark(c, .2)))
    s += hi('M-46 -160 Q-30 -170 -12 -172', '#fff', '.4', 5)
    return s

def coffee_cup_togo(cup='#F3EEE2', sleeve='#8A5A3C', lid='#3A2E26'):
    s = path('M-42 -150 L42 -150 L32 0 L-32 0Z', **S(cup))
    s += path('M-38 -104 L38 -104 L35 -54 L-35 -54Z', **S(sleeve))
    s += circ(0, -79, 13, fill='none', stroke=light(sleeve, .5), stroke_width=3)
    s += rect(-50, -172, 100, 24, rx=8, **S(lid)) + rect(-24, -184, 48, 14, rx=5, fill=dark(lid, .2))
    s += hi('M-24 -140 L-20 -14', '#fff', '.5', 5)
    s += path('M-10 -200 q10 -16 0 -32 M14 -204 q10 -16 0 -32', fill='none', stroke='#ECE4D6', stroke_width=5, stroke_linecap='round', opacity='.5')
    return s

def dumbbell(c='#3A3E47'):
    s = rect(-70, -56, 140, 16, rx=6, **S('#9AA3AF'))
    for sx in (-1, 1):
        s += rect(sx * 70 - (24 if sx > 0 else 0) - (0 if sx > 0 else -0), -94, 24, 92, rx=8, **S(c)) if False else ''
        s += rect(sx * 66 - 12, -96, 24, 96, rx=8, **S(c))
        s += rect(sx * 92 - 9, -82, 18, 68, rx=6, **S(light(c, .1)))
    s += hi('M-40 -50 L40 -50', '#fff', '.35', 3)
    return s

def game_controller(c='#3A3E47'):
    s = path('M-120 -36 C-140 -112 -96 -132 -64 -120 L64 -120 C96 -132 140 -112 120 -36 C108 2 74 4 56 -30 L-56 -30 C-74 4 -108 2 -120 -36Z', **S(c))
    s += rect(-86, -98, 12, 40, rx=3, fill='#9AA3AF') + rect(-100, -84, 40, 12, rx=3, fill='#9AA3AF')
    for (x, y, k) in ((64, -96, '#D6453A'), (86, -76, '#5FB55A'), (42, -76, '#3E6A8A'), (64, -56, '#E9A23B')):
        s += circ(x, y, 9, fill=k, stroke=dark(k, .5), stroke_width=2)
    s += circ(-30, -56, 14, **S('#2A2D35')) + circ(26, -56, 14, **S('#2A2D35'))
    s += rect(-14, -100, 28, 8, rx=4, fill='#9AA3AF')
    return s

def sneakers(c='#E9A23B'):
    def one(x, k):
        col = dark(c, .1) if k else c; ln = dark(c, .6)
        return g(path('M-60 -10 C-62 -48 -20 -56 0 -50 L30 -44 C52 -38 72 -30 82 -14 L82 0 L-60 0Z', fill=col, stroke=ln, stroke_width=LW, stroke_linejoin='round') +
                 rect(-64, -14, 150, 16, rx=7, fill='#F4EFE6', stroke=ln, stroke_width=2) +
                 path('M-6 -46 L4 -30 M8 -44 L18 -28 M22 -40 L30 -26', stroke='#F4EFE6', stroke_width=4, stroke_linecap='round') +
                 path('M40 -30 Q58 -28 70 -18', fill='none', stroke='#F4EFE6', stroke_width=4, stroke_linecap='round'), transform=f'translate({x} 0)')
    return one(-40, 1) + one(30, 0)

# ------------------------------------------------ new wearables (standalone)
def glasses_item(kind='round'):
    fr = {'round': INK, 'square': INK, 'cat': '#7A2F4A', 'sun': '#111', 'aviator': GOLD}[kind]
    s = path('M-34 -6 Q0 -18 34 -6', fill='none', stroke=fr, stroke_width=5, stroke_linecap='round')
    s += path('M-86 -14 L-112 -22 M86 -14 L112 -22', stroke=fr, stroke_width=5, stroke_linecap='round')
    for sx in (-1, 1):
        x = sx * 58
        if kind == 'round': s += circ(x, 0, 30, fill='#DDEBFA', fill_opacity='.35', stroke=fr, stroke_width=6)
        elif kind == 'square': s += rect(x - 32, -24, 64, 48, rx=10, fill='#DDEBFA', fill_opacity='.35', stroke=fr, stroke_width=6)
        elif kind == 'cat': s += path(f'M{x-32} -12 Q{x} -32 {x+sx*36 if sx>0 else x+36} -30 Q{x+30} 28 {x} 24 Q{x-32} 20 {x-32} -12Z', fill='#F5D7E3', fill_opacity='.4', stroke=fr, stroke_width=6, stroke_linejoin='round')
        elif kind == 'sun': s += path(f'M{x-34} -22 L{x+34} -22 Q{x+34} 30 {x} 28 Q{x-34} 26 {x-34} -22Z', fill='#1E2230', stroke=fr, stroke_width=4)
        else: s += path(f'M{x-34} -20 Q{x} -28 {x+34} -20 Q{x+34} 34 {x+2} 32 Q{x-36} 26 {x-34} -20Z', fill='#3A4A5E', stroke=fr, stroke_width=4)
        s += hi(f'M{x-16} -10 L{x-4} -16', '#fff', '.6', 4)
    return g(s, transform='translate(0 -40)')

def wristwatch(c='#2F333B', face='#F3F1EC'):
    s = rect(-20, -150, 40, 150, rx=10, **S(c))
    for y in (-130, -110, -40, -20): s += path(f'M-12 {y} L12 {y}', stroke=light(c, .2), stroke_width=2)
    s += circ(0, -75, 36, **S('#C9CED6')) + circ(0, -75, 28, fill=face, stroke='#8A9099', stroke_width=2)
    s += path('M0 -75 L0 -95 M0 -75 L14 -68', stroke=INK, stroke_width=4, stroke_linecap='round')
    for a in range(0, 360, 90): p0 = add([0, -75], mul(dirv(a), 23)); s += circ(p0[0], p0[1], 2.4, fill=INK)
    s += rect(36, -82, 8, 14, rx=2, fill='#9AA3AF')
    return s

def cap_item(c='#3E6A8A'):
    s = path('M-80 -20 C-84 -120 70 -124 76 -24Z', **S(c))
    s += path('M60 -30 Q140 -36 150 -14 Q110 -6 60 -16Z', **S(dark(c, .2)))
    s += path('M-2 -110 L-6 -24 M-50 -86 Q-30 -60 -36 -22', fill='none', stroke=dark(c, .4), stroke_width=2)
    s += circ(-4, -112, 7, fill=dark(c, .3))
    return s

def beanie_item(c='#C8573E'):
    s = path('M-80 -30 C-86 -150 86 -150 80 -30Z', **S(c))
    s += rect(-86, -42, 172, 34, rx=12, **S(dark(c, .15)))
    for x in range(-64, 80, 20): s += path(f'M{x} -38 L{x} -12', stroke=dark(c, .35), stroke_width=2.4)
    s += circ(0, -150, 22, **S(light(c, .25)))
    return s

def scarf_item(c='#D9A23B'):
    ln = dark(c, .5)
    s = path('M-90 -150 Q0 -110 90 -150 L90 -116 Q0 -76 -90 -116Z', **S(c))
    s += path('M30 -110 L60 -10 L20 0 L4 -104Z', **S(c))
    for x in (26, 36, 46): s += path(f'M{x} 0 L{x+2} 14', stroke=ln, stroke_width=3, stroke_linecap='round')
    s += path('M-60 -134 L-60 -102 M-20 -122 L-20 -92 M20 -122 L20 -94', stroke=dark(c, .2), stroke_width=3, opacity='.6')
    return s

def crossbody_item(c='#8A5A3C'):
    ln = dark(c, .55)
    s = path('M-50 -90 Q0 -260 50 -90', fill='none', stroke=ln, stroke_width=8)
    s += rect(-70, -100, 140, 100, rx=20, **S(c))
    s += path('M-70 -64 Q0 -30 70 -64 L70 -94 Q70 -100 62 -100 L-62 -100 Q-70 -100 -70 -94Z', **S(dark(c, .12)))
    s += circ(0, -44, 8, fill=GOLD, stroke=ln, stroke_width=2)
    return s

def tote_item(c='#E8DCC0'):
    ln = dark(c, .55)
    s = path('M-40 -150 Q-40 -230 0 -230 Q40 -230 40 -150', fill='none', stroke=ln, stroke_width=7)
    s += path('M-80 -150 L80 -150 L90 0 L-90 0Z', **S(c))
    s += circ(0, -76, 30, fill='none', stroke='#C8573E', stroke_width=6) + circ(0, -76, 12, fill='#E9A23B')
    return s

def earrings_item():
    s = ''
    for x in (-40, 40):
        s += circ(x, -60, 6, fill=GOLD) + circ(x, -30, 26, fill='none', stroke=dark(GOLD, .3), stroke_width=9) + circ(x, -30, 26, fill='none', stroke=GOLD, stroke_width=5)
    return s

def necklace_item():
    s = path('M-90 -170 Q0 -30 90 -170', fill='none', stroke=GOLD, stroke_width=5)
    s += path('M0 -84 L18 -60 L0 -30 L-18 -60Z', **S('#7FC6E8'))
    return s

def lanyard_item():
    s = path('M-50 -220 L0 -110 L50 -220', fill='none', stroke='#3E6A8A', stroke_width=10, stroke_linejoin='round')
    s += rect(-44, -112, 88, 112, rx=10, **S('#F3F1EC')) + rect(-30, -94, 60, 40, rx=6, fill='#8EA6C9') + circ(0, -78, 10, fill='#ECE4D6')
    s += path('M-28 -38 L28 -38 M-28 -22 L12 -22', stroke='#9AA3AF', stroke_width=5, stroke_linecap='round')
    return s

# ------------------------------------------------ new objects
def briefcase(c='#5A3E2A'):
    ln = dark(c, .55)
    s = path('M-34 -140 L-34 -158 Q-34 -168 -24 -168 L24 -168 Q34 -168 34 -158 L34 -140', fill='none', stroke=ln, stroke_width=10)
    s += rect(-110, -142, 220, 142, rx=14, **S(c))
    s += path('M-110 -92 L110 -92', stroke=ln, stroke_width=3) + rect(-18, -104, 36, 26, rx=4, fill=GOLD, stroke=ln, stroke_width=2)
    s += hi('M-92 -128 L-30 -128', '#fff', '.3', 5)
    return s

def suitcase(c='#3E6A8A'):
    ln = dark(c, .55)
    s = path('M-24 -230 L-24 -300 L24 -300 L24 -230', fill='none', stroke='#9AA3AF', stroke_width=8, stroke_linejoin='round')
    s += rect(-80, -232, 160, 216, rx=20, **S(c))
    for x in (-40, 0, 40): s += path(f'M{x} -224 L{x} -24', stroke=dark(c, .25), stroke_width=4)
    s += circ(-56, -6, 12, **S('#2A2D35')) + circ(56, -6, 12, **S('#2A2D35'))
    s += rect(-58, -160, 30, 22, rx=4, fill='#F2D45A', stroke=ln, stroke_width=2)
    return s

def envelope(open_=False):
    s = rect(-90, -120, 180, 120, rx=6, **S('#F3EEE2', .45))
    if open_:
        s = rect(-70, -180, 140, 110, rx=4, **S('#FBF8F0', .4)) + ''.join(path(f'M-52 {y} L52 {y}', stroke='#B8AE9C', stroke_width=3) for y in (-158, -142, -126)) + s
        s += path('M-90 -120 L0 -60 L90 -120', fill='none', stroke=dark('#F3EEE2', .45), stroke_width=LW)
    else:
        s += path('M-90 -120 L0 -48 L90 -120', fill='#E9E2D2', stroke=dark('#F3EEE2', .45), stroke_width=LW, stroke_linejoin='round')
        s += circ(0, -58, 12, fill='#C8463A', stroke=dark('#C8463A', .4), stroke_width=2)
    return s

def rose(c='#E8455A'):
    s = path('M0 0 Q10 -80 2 -180', fill='none', stroke='#4E8A48', stroke_width=7, stroke_linecap='round')
    s += path('M4 -90 Q44 -110 52 -80 Q24 -70 4 -90Z', **S('#5FB55A')) + path('M4 -56 Q-36 -76 -44 -46 Q-16 -36 4 -56Z', **S('#5FB55A'))
    s += path('M-36 -190 Q-40 -240 4 -236 Q44 -244 40 -194 Q38 -160 2 -160 Q-32 -160 -36 -190Z', **S(c))
    s += path('M-14 -214 Q4 -184 22 -214 M-24 -196 Q4 -172 30 -196 M-6 -228 Q8 -216 14 -230', fill='none', stroke=dark(c, .4), stroke_width=3, stroke_linecap='round')
    return s

def bouquet():
    s = path('M-40 -100 L0 0 L40 -100Z', **S('#F3EEE2', .4))
    cols = ['#E8455A', '#F2A65A', '#C8577A', '#F2D45A', '#E8455A']
    for i, (x, y) in enumerate(((-36, -130), (0, -150), (36, -130), (-18, -110), (20, -108))):
        for k in range(5):
            a = k * 72 * D; s += circ(x + math.cos(a) * 12, y + math.sin(a) * 12, 11, **S(cols[i], .45, 2))
        s += circ(x, y, 8, fill='#FFE07A')
    s += path('M-24 -60 L24 -60', stroke='#C8463A', stroke_width=8, stroke_linecap='round')
    return s

def pizza_slice():
    s = path('M-70 -150 Q0 -180 70 -150 L0 0Z', **S('#F2C46A', .45))
    s += path('M-70 -150 Q0 -180 70 -150 Q0 -168 -70 -150Z', fill='#C98A3E')
    s += path('M-74 -152 Q0 -186 74 -152 L70 -138 Q0 -168 -70 -138Z', **S('#D9A055', .5))
    for (x, y) in ((-24, -110), (18, -120), (0, -70), (-6, -140)): s += circ(x, y, 12, **S('#C8463A', .45, 2))
    return s

def burger():
    s = path('M-90 -40 Q-90 -10 -60 -6 L60 -6 Q90 -10 90 -40Z', **S('#D9A055'))
    s += rect(-96, -62, 192, 22, rx=11, **S('#6B3E2A'))
    s += path('M-100 -66 Q-80 -50 -60 -66 Q-40 -50 -20 -66 Q0 -50 20 -66 Q40 -50 60 -66 Q80 -50 100 -66 L100 -74 L-100 -74Z', **S('#5FB55A'))
    s += path('M-92 -74 L92 -74 L80 -88 L-80 -88Z', **S('#F2D45A'))
    s += path('M-90 -88 Q-90 -170 0 -170 Q90 -170 90 -88Z', **S('#E0A85A'))
    for (x, y) in ((-40, -130), (0, -146), (36, -124), (-10, -112), (56, -108)): s += ell(x, y, 5, 3, fill='#FBF3DC')
    return s

def donut(c='#E88AA8'):
    s = ell(0, -60, 90, 56, **S('#D9A055'))
    s += path('M-84 -66 Q-90 -110 -40 -112 Q0 -118 40 -112 Q90 -110 84 -66 Q70 -40 40 -54 Q20 -30 -10 -48 Q-40 -30 -60 -52 Q-80 -44 -84 -66Z', **S(c, .45))
    s += ell(0, -66, 26, 14, fill='#1C2233', stroke=dark('#D9A055', .5), stroke_width=2)
    for i, (x, y) in enumerate(((-50, -86), (-20, -100), (30, -96), (56, -80), (-60, -64), (40, -68))):
        s += rect(x - 7, y - 2.5, 14, 5, rx=2.5, fill=['#FFE07A', '#7FC6E8', '#5FB55A'][i % 3], transform=f'rotate({i*37} {x} {y})')
    return s

def basketball():
    s = circ(0, -80, 78, **S('#E9823B'))
    s += path('M-78 -80 L78 -80 M0 -158 L0 -2 M-54 -136 Q-20 -80 -54 -24 M54 -136 Q20 -80 54 -24', fill='none', stroke=dark('#E9823B', .55), stroke_width=4)
    s += hi('M-40 -134 Q-20 -148 4 -150', '#fff', '.4', 6)
    return s

def soccer_ball():
    s = circ(0, -80, 78, **S('#F3F1EC', .6))
    pent = lambda cx, cy, r: path('M' + 'L'.join(P([cx + math.cos((a * 72 - 90) * D) * r, cy + math.sin((a * 72 - 90) * D) * r]) for a in range(5)) + 'Z', fill='#2A2D35')
    s += pent(0, -80, 24)
    for a in range(5):
        c = add([0, -80], mul([math.cos((a * 72 + 90) * D), math.sin((a * 72 + 90) * D)], 62)); s += pent(c[0], c[1], 14)
    return s

def camera(c='#2F333B'):
    s = rect(-100, -140, 200, 130, rx=18, **S(c))
    s += rect(-40, -164, 80, 30, rx=8, **S(c)) + rect(60, -158, 26, 14, rx=4, fill='#D6453A')
    s += circ(0, -76, 48, **S('#5A6070')) + circ(0, -76, 34, fill='#1A1D24', stroke='#9AA3AF', stroke_width=3) + circ(-10, -86, 9, fill='#8FB6F0', opacity='.8')
    s += rect(-84, -128, 30, 14, rx=4, fill='#E9EDF2')
    return s

def candle(lit=True):
    s = rect(-24, -140, 48, 140, rx=6, **S('#F3EEE2', .4))
    s += path('M-24 -128 Q-10 -110 -16 -90 Q-6 -110 6 -128', fill='#E9E2D2')
    s += path('M0 -140 L0 -156', stroke=INK, stroke_width=3)
    if lit:
        s = circ(0, -170, 60, fill='url(#bulbGlow)') + s
        s += path('M0 -200 Q16 -172 0 -154 Q-16 -172 0 -200Z', fill='#FFB13B') + path('M0 -184 Q7 -170 0 -160 Q-7 -170 0 -184Z', fill='#FFE98A')
    return s

def teddy_bear(c='#B8794A'):
    ln = dark(c, .55)
    s = ell(0, -60, 64, 60, **S(c))
    for sx in (-1, 1):
        s += circ(sx * 50, -10, 26, **S(c)) + circ(sx * 66, -80, 22, **S(c)) + circ(sx * 50, -186, 22, **S(c)) + circ(sx * 50, -186, 11, fill=light(c, .3))
    s += circ(0, -150, 56, **S(c)) + ell(0, -130, 26, 20, fill=light(c, .35), stroke=ln, stroke_width=2)
    s += circ(-20, -160, 6, fill=INK) + circ(20, -160, 6, fill=INK) + ell(0, -138, 9, 6, fill=INK) + path('M0 -132 L0 -122 M-8 -118 Q0 -112 8 -118', fill='none', stroke=INK, stroke_width=3, stroke_linecap='round')
    s += ell(0, -56, 30, 26, fill=light(c, .3))
    s += path('M-30 -100 L30 -100 L22 -86 L0 -94 L-22 -86Z', **S('#C8463A', .45, 2))
    return s

def piggy_bank(c='#F2A6B8'):
    ln = dark(c, .55)
    s = rect(-60, -40, 26, 40, rx=8, **S(c)) + rect(30, -40, 26, 40, rx=8, **S(c))
    s += ell(0, -80, 100, 66, **S(c))
    s += ell(96, -84, 22, 26, **S(dark(c, .1))) + circ(90, -84, 4, fill=ln) + circ(102, -84, 4, fill=ln)
    s += path('M30 -142 L46 -170 L58 -130Z', **S(c)) + circ(54, -104, 6, fill=INK)
    s += rect(-20, -150, 46, 10, rx=5, fill=ln)
    s += path('M-100 -86 q-26 -10 -18 -30 q14 -4 8 12', fill='none', stroke=ln, stroke_width=4, stroke_linecap='round')
    s += circ(4, -176, 20, **S(GOLD, .45)) + text('$', 4, -168, size=22, fill=dark(GOLD, .45), weight=900, anchor='middle')
    return s

def megaphone(c='#E9A23B'):
    s = path('M-90 -110 L40 -170 L40 -10 L-90 -70Z', **S(c))
    s += ell(40, -90, 20, 80, **S(dark(c, .15))) + rect(-120, -110, 34, 40, rx=8, **S('#3A3E47'))
    s += path('M-70 -70 L-60 -10 L-36 -10 L-44 -66', **S('#3A3E47'))
    for i, k in enumerate((40, 64, 88)): s += path(f'M{70+i*16} {-90-k*.6} Q{90+i*22} -90 {70+i*16} {-90+k*.6}', fill='none', stroke='#ECE4D6', stroke_width=5, stroke_linecap='round', opacity='.6')
    return s

def sign_blank(c='#F3EEE2', t=''):
    s = rect(-8, -170, 16, 170, rx=4, **S('#8A6A4A'))
    s += rect(-120, -320, 240, 160, rx=10, **S(c, .45))
    if t: s += text(t, 0, -228, size=40, fill='#2C2A30', weight=900, anchor='middle')
    return s

def toothbrush():
    s = rect(-12, -220, 24, 220, rx=12, **S('#7FC6E8'))
    s += rect(-14, -268, 28, 54, rx=6, **S('#F3F1EC', .45))
    for y in range(-262, -222, 10): s += path(f'M14 {y} L30 {y}', stroke='#9FD3FF', stroke_width=5, stroke_linecap='round')
    return s

def medal(c=GOLD):
    s = path('M-40 -200 L-10 -100 L10 -100 L40 -200 L16 -200 L0 -140 L-16 -200Z', **S('#3E6A8A'))
    s += circ(0, -64, 56, **S(c, .45)) + circ(0, -64, 40, fill='none', stroke=dark(c, .3), stroke_width=4)
    s += text('1', 0, -48, size=48, fill=dark(c, .45), weight=900, anchor='middle')
    return s

def balloon(c='#E8455A'):
    s = path('M0 -120 Q-10 -60 6 0', fill='none', stroke='#ECE4D6', stroke_width=3)
    s += ell(0, -200, 62, 76, **S(c)) + path('M-10 -122 L10 -122 L0 -134Z', **S(c))
    s += hi('M-30 -240 Q-20 -260 0 -262', '#fff', '.5', 7)
    return s

def plant_snake():
    s = path('M-60 -100 L60 -100 L48 0 L-48 0Z', **S('#E9E2D4')) + rect(-66, -112, 132, 18, rx=6, **S('#D9D2C4'))
    for i, (x, h, a) in enumerate(((-30, 170, -8), (-8, 220, -2), (16, 200, 6), (36, 150, 12))):
        s += g(path(f'M-12 0 Q-16 {-h*.6} 0 {-h} Q16 {-h*.6} 12 0Z', **S('#4E8A48')) + path(f'M-4 {-h*.2} L4 {-h*.3} M-6 {-h*.5} L4 {-h*.6}', stroke='#B8D47A', stroke_width=3), transform=f'translate({x} -104) rotate({a})')
    return s

def laptop_stickers():
    s = rect(-130, -170, 260, 160, rx=12, **S('#B8BEC8', .5))
    s += circ(0, -96, 16, fill='#E9EDF2')
    s += circ(-80, -140, 18, fill='#E9A23B') + rect(54, -60, 46, 30, rx=6, fill='#5FB55A', transform='rotate(-10 77 -45)') + path('M-90 -60 L-60 -80 L-50 -46Z', fill='#C8577A')
    s += rect(-150, -14, 300, 14, rx=6, **S('#9AA3AF', .5))
    return s

def phone_charger():
    s = rect(-30, -60, 60, 60, rx=10, **S('#F3F1EC', .45))
    s += path('M0 -60 Q0 -120 60 -140 Q120 -160 120 -220', fill='none', stroke='#F3F1EC', stroke_width=8, stroke_linecap='round')
    s += path('M0 -60 Q0 -120 60 -140 Q120 -160 120 -220', fill='none', stroke='#8A8F99', stroke_width=2, opacity='.5')
    s += rect(110, -250, 20, 34, rx=4, **S('#F3F1EC', .45))
    s += path('M-14 -22 L-14 -42 M14 -22 L14 -42', stroke='#9AA3AF', stroke_width=5)
    return s

UPGRADED = dict(headphones=headphones, umbrella=umbrella, water_bottle=water_bottle, soda_can=soda_can, shopping_bag=shopping_bag,
                backpack=backpack, coffee_to_go=coffee_cup_togo, dumbbell=dumbbell, game_controller=game_controller, sneakers=sneakers)
NEW = {
 'accessories': dict(glasses_round=glasses_item('round'), glasses_square=glasses_item('square'), glasses_cat=glasses_item('cat'), sunglasses=glasses_item('sun'),
                     sunglasses_aviator=glasses_item('aviator'), wristwatch=wristwatch(), smartwatch=wristwatch('#3E6A8A', '#1A1D24'), cap=cap_item(), cap_red=cap_item('#C8463A'),
                     beanie=beanie_item(), beanie_blue=beanie_item('#5B6C8F'), scarf=scarf_item(), scarf_red=scarf_item('#C8463A'), crossbody_bag=crossbody_item(), tote_bag=tote_item(),
                     earrings_hoops=earrings_item(), necklace=necklace_item(), lanyard_badge=lanyard_item(), headphones_red=headphones('#C8463A', '#2F333B'), backpack_blue=backpack('#3E6A8A')),
 'food': dict(pizza_slice=pizza_slice(), burger=burger(), donut=donut(), donut_choco=donut('#6B3E2A'), soda_can_blue=soda_can('#3E6A8A'), soda_can_green=soda_can('#4E8A48')),
 'misc': dict(briefcase=briefcase(), suitcase=suitcase(), suitcase_red=suitcase('#C8463A'), envelope_closed=envelope(), envelope_letter=envelope(True), rose=rose(), bouquet=bouquet(),
              basketball=basketball(), soccer_ball=soccer_ball(), camera=camera(), candle_lit=candle(), candle_out=candle(False), teddy_bear=teddy_bear(), piggy_bank=piggy_bank(),
              megaphone=megaphone(), sign_blank=sign_blank(), sign_help=sign_blank(t='HELP'), toothbrush=toothbrush(), medal=medal(), balloon=balloon(), balloon_blue=balloon('#3E6A8A'),
              plant_snake=plant_snake(), laptop_stickers=laptop_stickers(), phone_charger=phone_charger()),
}
