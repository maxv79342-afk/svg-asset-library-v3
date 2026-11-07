"""Wearable accessories for the rig (v2).
All head pieces are drawn in head-local coords (head centre = 0,0, face looks to +x in side views).
"""
from sv import *
import math

INK = '#2C2A30'
GOLD = '#E3B24A'
GLASS_STYLES = ('glasses_round', 'glasses_square', 'glasses_cat', 'sunglasses', 'sunglasses_aviator')
HEAD_ACC = GLASS_STYLES + ('headphones', 'headphones_neck', 'earrings', 'earrings_studs', 'headband', 'hair_clip', 'flower_clip')
import acc2 as _A2
HEAD_ACC = HEAD_ACC + _A2.HEAD2
BODY_ACC = ('watch', 'backpack', 'crossbody', 'scarf', 'necklace', 'lanyard', 'tote')
ALL_ACC = HEAD_ACC + BODY_ACC


def norm(p):
    """collect accessory list from pose params (old `glasses=True` still works)"""
    a = list(p.get('acc') or [])
    gl = p.get('glasses')
    if gl:
        a.append(gl if isinstance(gl, str) else 'glasses_round')
    return a


def eye_xy(r, turn):
    if turn < 0:
        return [r * .52], -3
    t = clamp(turn, 0, 1)
    cx = lerp(13, 0, t); sp = lerp(8.5, 11.5, t)
    return [cx - sp, cx + sp], -3


def ear_xy(r, turn, view):
    if view in ('front', 'back'):
        return None
    if turn < 0:
        return [-r * .06, r * .06]
    return [lerp(-r * .3, -r * .62, clamp(turn, 0, 1)), r * .08]


# ------------------------------------------------------------------ glasses
def _lens(kind, x, y, sc, squash=1.0):
    rx = 9.6 * sc * squash; ry = 9.0 * sc
    if kind == 'glasses_round':
        return ell(x, y, rx, ry + .6, fill='#DDEBFA', fill_opacity='.22', stroke=INK, stroke_width='2.6')
    if kind == 'glasses_square':
        return rect(x - rx - .5, y - ry * .78, 2 * rx + 1, ry * 1.56, rx=3.4, fill='#DDEBFA', fill_opacity='.22', stroke=INK, stroke_width='2.8')
    if kind == 'glasses_cat':
        d = f'M{f(x-rx)} {f(y-ry*.55)}Q{f(x)} {f(y-ry*.95)} {f(x+rx*1.15)} {f(y-ry*.95)}Q{f(x+rx*.9)} {f(y+ry*.9)} {f(x)} {f(y+ry*.75)}Q{f(x-rx*1.05)} {f(y+ry*.6)} {f(x-rx)} {f(y-ry*.55)}Z'
        return path(d, fill='#F5D7E3', fill_opacity='.3', stroke='#7A2F4A', stroke_width='2.8', stroke_linejoin='round')
    if kind == 'sunglasses':
        d = f'M{f(x-rx-1)} {f(y-ry*.7)}L{f(x+rx+1)} {f(y-ry*.7)}Q{f(x+rx+1)} {f(y+ry*.9)} {f(x)} {f(y+ry*.85)}Q{f(x-rx-1)} {f(y+ry*.8)} {f(x-rx-1)} {f(y-ry*.7)}Z'
        return path(d, fill='#1E2230', stroke='#111', stroke_width='2.2', stroke_linejoin='round') + \
            path(f'M{f(x-rx*.5)} {f(y-ry*.35)}L{f(x-rx*.05)} {f(y-ry*.35)}', stroke='#9FB4D8', stroke_width='2.2', stroke_linecap='round', opacity='.8')
    if kind == 'sunglasses_aviator':
        d = f'M{f(x-rx-1)} {f(y-ry*.65)}Q{f(x)} {f(y-ry*.9)} {f(x+rx+1)} {f(y-ry*.65)}Q{f(x+rx*1.05)} {f(y+ry*1.1)} {f(x+rx*.1)} {f(y+ry*1.05)}Q{f(x-rx*1.1)} {f(y+ry*.8)} {f(x-rx-1)} {f(y-ry*.65)}Z'
        return path(d, fill='#3A4A5E', fill_opacity='.92', stroke=GOLD, stroke_width='2.2', stroke_linejoin='round') + \
            path(f'M{f(x-rx*.45)} {f(y-ry*.3)}Q{f(x)} {f(y-ry*.45)} {f(x+rx*.3)} {f(y-ry*.3)}', fill='none', stroke='#C7D6EE', stroke_width='2', stroke_linecap='round', opacity='.75')
    return ''


def glasses(kind, r, turn, view):
    frame = '#7A2F4A' if kind == 'glasses_cat' else (GOLD if kind == 'sunglasses_aviator' else INK)
    s = ''
    if view == 'front' or turn >= .99:
        xs = [-11.5, 11.5]
        s += path(f'M{f(xs[0]+8)} -5 Q0 -9 {f(xs[1]-8)} -5', fill='none', stroke=frame, stroke_width='2.4', stroke_linecap='round')
        s += path(f'M{f(xs[0]-9.5)} -5 L{f(-r*.97)} -7 M{f(xs[1]+9.5)} -5 L{f(r*.97)} -7', stroke=frame, stroke_width='2.4', stroke_linecap='round')
        for x in xs: s += _lens(kind, x, -3, 1)
        return s
    ear = ear_xy(r, turn, view)
    if turn < 0:  # profile: one lens seen edge-on-ish + temple to ear
        ex = r * .55
        s += path(f'M{f(ex-7)} -5 L{f(ear[0]+3)} {f(ear[1]-9)}', stroke=frame, stroke_width='2.6', stroke_linecap='round')
        s += _lens(kind, ex + 1, -3, 1, squash=.5)
        return s
    xs, y = eye_xy(r, turn)
    t = clamp(turn, 0, 1)
    farSc = lerp(.78, 1, t)
    # temple arm from far lens to ear (drawn first, sits behind lenses)
    s += path(f'M{f(xs[0]-9.5*farSc*.75)} -5 L{f(ear[0]+4)} {f(ear[1]-9)}', stroke=frame, stroke_width='2.6', stroke_linecap='round')
    s += path(f'M{f(xs[0]+7*farSc)} -5 Q{f((xs[0]+xs[1])/2)} -9 {f(xs[1]-7.5)} -5', fill='none', stroke=frame, stroke_width='2.4', stroke_linecap='round')
    s += _lens(kind, xs[0], y, 1, squash=farSc * .82)
    s += _lens(kind, xs[1], y, 1)
    return s


# ------------------------------------------------------------------ head pieces
def headphones(r, turn, view, col='#2F333B', pad='#E2725B', neck=False):
    if neck:
        return ''  # drawn on the body instead
    s = ''
    if view in ('front', 'back'):
        s += path(f'M{f(-r-3)} 2 A{f(r+7)} {f(r+9)} 0 0 1 {f(r+3)} 2', fill='none', stroke=dark(col, .4), stroke_width='9.5', stroke_linecap='round')
        s += path(f'M{f(-r-3)} 2 A{f(r+7)} {f(r+9)} 0 0 1 {f(r+3)} 2', fill='none', stroke=col, stroke_width='5.5', stroke_linecap='round')
        for sx in (-1, 1):
            x = sx * (r + 2)
            s += rect(x - 8, -15, 16, 32, rx=7, fill=col, stroke=dark(col, .5), stroke_width='2.2')
            s += rect(x - 4 + sx * 2, -10, 6, 22, rx=3, fill=pad, opacity='.9')
        return s
    ear = ear_xy(r, turn, view)
    ex, ey = ear
    R_ = r + 3
    if turn < 0:
        band = f'M{f(ex)} {f(ey-14)}Q{f(ex-5)} {f(-r*.75)} {f(ex+3)} {f(-R_)}'
    else:
        a0 = math.atan2(ey - 15, ex); a1 = -52 * D
        p0 = [math.cos(a0) * R_, math.sin(a0) * R_]; p1 = [math.cos(a1) * R_, math.sin(a1) * R_]
        band = f'M{f(ex)} {f(ey-14)}L{P(p0)}A{f(R_)} {f(R_)} 0 0 1 {P(p1)}'
    s += path(band, fill='none', stroke=dark(col, .4), stroke_width='10', stroke_linecap='round', stroke_linejoin='round')
    s += path(band, fill='none', stroke=col, stroke_width='6', stroke_linecap='round', stroke_linejoin='round')
    s += ell(ex, ey, 14, 17, fill=col, stroke=dark(col, .5), stroke_width='2.4')
    s += ell(ex + 1, ey, 8, 11, fill=pad)
    s += path(f'M{f(ex-6)} {f(ey-8)}Q{f(ex-9)} {f(ey)} {f(ex-6)} {f(ey+8)}', fill='none', stroke=light(col, .35), stroke_width='2', stroke_linecap='round', opacity='.7')
    return s


def earrings(r, turn, view, studs=False):
    s = ''
    pts = [[-r * .97, r * .34], [r * .97, r * .34]] if view == 'front' else ([ear_xy(r, turn, view)] if view != 'back' else [])
    for (x, y) in pts:
        y2 = y + (r * .26 if view != 'front' else 0)
        if studs:
            s += circ(x, y2, 3.4, fill='#F3F1EC', stroke=GOLD, stroke_width='1.6')
        else:
            s += circ(x, y2 + 6, 5.6, fill='none', stroke=dark(GOLD, .3), stroke_width='4.2')
            s += circ(x, y2 + 6, 5.6, fill='none', stroke=GOLD, stroke_width='2.4')
    return s


def headband(r, turn, view, col='#C8577A'):
    if view in ('front', 'back'):
        return path(f'M{f(-r*.98)} {f(-r*.28)}Q0 {f(-r*1.28)} {f(r*.98)} {f(-r*.28)}', fill='none', stroke=dark(col, .4), stroke_width='9', stroke_linecap='round') + \
            path(f'M{f(-r*.98)} {f(-r*.28)}Q0 {f(-r*1.28)} {f(r*.98)} {f(-r*.28)}', fill='none', stroke=col, stroke_width='5.5', stroke_linecap='round')
    R_ = r * .97
    a0 = -168 * D; a1 = -48 * D
    d = f'M{f(math.cos(a0)*R_)} {f(math.sin(a0)*R_)}A{f(R_)} {f(R_)} 0 0 1 {f(math.cos(a1)*R_)} {f(math.sin(a1)*R_)}'
    return path(d, fill='none', stroke=dark(col, .4), stroke_width='9', stroke_linecap='round') + path(d, fill='none', stroke=col, stroke_width='5.5', stroke_linecap='round')


def flower_clip(r, turn, view, col='#F2A65A'):
    x, y = ((-r * .62, -r * .62) if view == 'front' else (-r * .35, -r * .78))
    s = ''
    for i in range(5):
        a = i * 72 * D
        s += circ(x + math.cos(a) * 5.5, y + math.sin(a) * 5.5, 4.6, fill=col, stroke=dark(col, .45), stroke_width='1.4')
    return s + circ(x, y, 3.4, fill='#FFE07A', stroke=dark(col, .45), stroke_width='1.2')


def hair_clip(r, turn, view, col='#5FB0A0'):
    x, y = ((r * .55, -r * .62) if view == 'front' else (r * .05, -r * .78))
    return g(rect(-9, -3.5, 18, 7, rx=3, fill=col, stroke=dark(col, .5), stroke_width='1.6'), transform=f'translate({f(x)} {f(y)}) rotate(-24)')


def head_layer(acc, r, turn, view):
    """returns svg for accessories that sit on top of face + hair"""
    s = ''
    for a in acc:
        if a in GLASS_STYLES and view != 'back': s += glasses(a, r, turn, view)
    for a in acc:
        if a == 'earrings': s += earrings(r, turn, view)
        elif a == 'earrings_studs': s += earrings(r, turn, view, studs=True)
        elif a == 'headband': s += headband(r, turn, view)
        elif a == 'flower_clip': s += flower_clip(r, turn, view)
        elif a == 'hair_clip': s += hair_clip(r, turn, view)
    if 'headphones' in acc: s += headphones(r, turn, view)
    import acc2 as AC2
    s += AC2.head(acc, r, turn, view)
    return s


# ------------------------------------------------------------------ body pieces (side view)
PACK = '#C8573E'
BAG = '#8A5A3C'
SCARF = '#D9A23B'


def backpack_side(top, bot, back, lean, col=PACK):
    """big pack behind the torso. top/bot = torso points, back = unit vector to the back"""
    c = lerp_(top, bot, .5)
    c = add(c, mul(back, 30))
    t = f'translate({f(c[0])} {f(c[1])}) rotate({f(lean)})'
    ln = dark(col, .55)
    s = rect(-20, -40, 40, 82, rx=16, fill=col, stroke=ln, stroke_width='2.6')
    s += rect(-24, -2, 14, 36, rx=6, fill=dark(col, .12), stroke=ln, stroke_width='2.2')
    s += path('M-14 -36 Q0 -50 14 -36', fill='none', stroke=ln, stroke_width='4', stroke_linecap='round')
    s += path('M-12 -18 L12 -18', stroke=light(col, .3), stroke_width='2.4', stroke_linecap='round', opacity='.7')
    return g(s, transform=t)


def lerp_(a, b, t): return [lerp(a[0], b[0], t), lerp(a[1], b[1], t)]


def strap_side(shoulder, low, col=PACK):
    ln = dark(col, .55)
    d = f'M{P(shoulder)}Q{P(add(lerp_(shoulder, low, .5), [10, 0]))} {P(low)}'
    return path(d, fill='none', stroke=ln, stroke_width='9', stroke_linecap='round') + path(d, fill='none', stroke=dark(col, .1), stroke_width='5.5', stroke_linecap='round')


def crossbody_strap(a, b, col=BAG):
    d = f'M{P(a)}L{P(b)}'
    return path(d, stroke=dark(col, .5), stroke_width='6.5', stroke_linecap='round') + path(d, stroke=col, stroke_width='3.5', stroke_linecap='round')


def crossbody_bag(c, lean=0, col=BAG):
    ln = dark(col, .55)
    s = rect(-15, -12, 30, 24, rx=6, fill=col, stroke=ln, stroke_width='2.4')
    s += path('M-15 -4 Q0 4 15 -4', fill='none', stroke=ln, stroke_width='2')
    s += circ(0, 1, 2.6, fill=GOLD, stroke=ln, stroke_width='1')
    return g(s, transform=f'translate({f(c[0])} {f(c[1])}) rotate({f(lean*.5)})')


def scarf_side(neck, back, sd, tw, col=SCARF):
    ln = dark(col, .5)
    n = add(neck, mul(sd, -2))
    left = add(n, mul(back, tw * .42)); right = add(n, mul(back, -tw * .42))
    s = path(f'M{P(left)}Q{P(add(n,mul(sd,9)))} {P(right)}', fill='none', stroke=ln, stroke_width='19', stroke_linecap='round')
    s += path(f'M{P(left)}Q{P(add(n,mul(sd,9)))} {P(right)}', fill='none', stroke=col, stroke_width='14', stroke_linecap='round')
    tail0 = add(right, mul(back, 6)); tail1 = add(add(tail0, mul(sd, -40)), mul(back, -4))
    s += path(f'M{P(tail0)}L{P(tail1)}', stroke=ln, stroke_width='15', stroke_linecap='round')
    s += path(f'M{P(tail0)}L{P(tail1)}', stroke=col, stroke_width='10.5', stroke_linecap='round')
    s += path(f'M{P(add(tail1,mul(back,5)))}L{P(add(tail1,mul(back,-5)))}', stroke=light(col, .4), stroke_width='2', opacity='.8')
    s += path(f'M{P(add(n,mul(back,tw*.2)))}l0 6M{P(add(n,mul(back,-tw*.05)))}l0 6', stroke=dark(col, .2), stroke_width='2', stroke_linecap='round', opacity='.7')
    return s


def necklace_side(neck, back, sd, tw):
    n = add(neck, mul(sd, -12))
    a = add(add(neck, mul(back, -tw * .1)), mul(sd, 2)); b = add(n, mul(back, -tw * .44))
    return path(f'M{P(a)}Q{P(add(b,mul(sd,6)))} {P(b)}', fill='none', stroke=GOLD, stroke_width='2', stroke_linecap='round') + circ(b[0], b[1] + 3, 3.4, fill='#7FC6E8', stroke=dark(GOLD, .3), stroke_width='1.2')


def lanyard_side(neck, back, sd, tw):
    a = add(neck, mul(back, -tw * .2)); b = add(add(neck, mul(sd, -46)), mul(back, -tw * .48))
    s = path(f'M{P(a)}L{P(b)}', stroke='#3E6A8A', stroke_width='3.4', stroke_linecap='round')
    s += g(rect(-9, 0, 18, 24, rx=3, fill='#F3F1EC', stroke='#5A6676', stroke_width='1.8') + rect(-6, 4, 12, 8, rx=1.5, fill='#8EA6C9') + path('M-5 16 L5 16 M-5 19.5 L2 19.5', stroke='#9AA3AF', stroke_width='1.4'), transform=f'translate({f(b[0])} {f(b[1])})')
    return s


def watch(W, ang, col='#2F333B', face='#DDEBFA'):
    """wrist watch strap across the forearm close to the wrist. W=wrist, ang=forearm angle (rig convention)"""
    c = add(W, mul(dirv(ang), -7))
    t = f'translate({f(c[0])} {f(c[1])}) rotate({f(-ang)})'
    s = rect(-11.5, -4.5, 23, 9, rx=3, fill=col, stroke=dark(col, .5), stroke_width='1.6')
    s += rect(-5.5, -6, 11, 12, rx=3, fill=face, stroke=dark(col, .5), stroke_width='1.8')
    s += path('M0 -3 L0 0 L2.5 1.5', fill='none', stroke=dark(col, .4), stroke_width='1.2', stroke_linecap='round')
    return g(s, transform=t)


def neck_headphones(neck, back, sd, col='#2F333B', pad='#E2725B'):
    n = add(neck, mul(sd, 2))
    a = add(n, mul(back, 14)); b = add(n, mul(back, -14))
    s = path(f'M{P(a)}Q{P(add(n,mul(sd,-22)))} {P(b)}', fill='none', stroke=dark(col, .4), stroke_width='9', stroke_linecap='round')
    s += path(f'M{P(a)}Q{P(add(n,mul(sd,-22)))} {P(b)}', fill='none', stroke=col, stroke_width='5.5', stroke_linecap='round')
    for c in (a, b):
        s += ell(c[0], c[1], 9, 12, fill=col, stroke=dark(col, .5), stroke_width='2') + ell(c[0], c[1], 5, 7.5, fill=pad)
    return s


def tote_bag(W, col='#E8DCC0'):
    c = add(W, [0, 30])
    ln = dark(col, .55)
    s = path(f'M{f(c[0]-8)} {f(c[1]-18)}Q{f(W[0]-6)} {f(W[1]-10)} {f(W[0])} {f(W[1]+4)}M{f(c[0]+8)} {f(c[1]-18)}Q{f(W[0]+6)} {f(W[1]-10)} {f(W[0])} {f(W[1]+4)}', fill='none', stroke=ln, stroke_width='3', stroke_linecap='round')
    s += path(f'M{f(c[0]-20)} {f(c[1]-18)}L{f(c[0]+20)} {f(c[1]-18)}L{f(c[0]+23)} {f(c[1]+26)}L{f(c[0]-23)} {f(c[1]+26)}Z', fill=col, stroke=ln, stroke_width='2.4', stroke_linejoin='round')
    s += circ(c[0], c[1] + 4, 7, fill='none', stroke='#C8573E', stroke_width='2.4')
    return s
