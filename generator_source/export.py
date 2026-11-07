from sv import *
import cairosvg, io, numpy as np
from PIL import Image
GDEFS=(rg('lampGlow',[(0,'#FFE2A8',.45),(1,'#FFE2A8',0)])+rg('bulbGlow',[(0,'#FFE98A',.5),(1,'#FFE98A',0)])+
       rg('phoneGlow',[(0,'#A9CBFF',.55),(1,'#6F9FE8',0)])+rg('screenGlow',[(0,'#A9CBFF',.6),(.5,'#6F9FE8',.2),(1,'#6F9FE8',0)])+
       rg('vignette',[(0,'#000',0),(.7,'#000',0),(1,'#000',.55)]))
def used_defs(inner):
    out=''
    import re
    for m in re.finditer(r'<(radialGradient|linearGradient) id="([^"]+)".*?</\1>',GDEFS):
        if f'url(#{m.group(2)})' in inner: out+=m.group(0)
    return out
def tight(inner, probe=(-1200,-1400,2400,2000), pad=12, scale=.5):
    x,y,W,H=probe
    svg=doc(inner,probe,defs=used_defs(inner),w=W*scale,h=H*scale)
    b=cairosvg.svg2png(bytestring=svg.encode())
    a=np.array(Image.open(io.BytesIO(b)).convert('RGBA'))[:,:,3]
    ys,xs=np.where(a>8)
    if len(xs)==0: return probe
    x0=x+xs.min()/scale-pad; x1=x+(xs.max()+1)/scale+pad
    y0=y+ys.min()/scale-pad; y1=y+(ys.max()+1)/scale+pad
    return (round(x0),round(y0),round(x1-x0),round(y1-y0))
def save(path_, inner, vb=None, title=None, probe=None):
    if vb is None: vb=tight(inner, probe or (-1200,-1400,2400,2000))
    svg=doc(inner,vb,defs=used_defs(inner),title=title)
    open(path_,'w').write(svg)
    return svg, vb
