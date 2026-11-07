import cairosvg, io
from PIL import Image
def png(svg, w=None, out=None):
    b=cairosvg.svg2png(bytestring=svg.encode(), output_width=w)
    if out: open(out,'wb').write(b)
    return Image.open(io.BytesIO(b))
