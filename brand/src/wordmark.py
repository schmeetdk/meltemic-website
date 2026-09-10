import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fontTools.ttLib import TTFont

HERE = pathlib.Path(__file__).parent
from fontTools.varLib import instancer
from fontTools.pens.recordingPen import RecordingPen
import pathops, math
from mark import sk_to_d, rect_path, poly_to_skpath

def load(wght=700, wdth=100):
    f = TTFont(HERE / 'Archivo.ttf')
    instancer.instantiateVariableFont(f, {'wght':wght, 'wdth':wdth}, inplace=True)
    return f

def glyph_path(f, ch):
    gs = f.getGlyphSet()
    name = f.getBestCmap()[ord(ch)]
    p = pathops.Path(); gs[name].draw(p.getPen())
    return pathops.simplify(p), gs[name].width

def wordmark(text="meltemic", wght=700, wdth=100, tracking=-18, upem=1000):
    """Returns (skia path in y-DOWN svg space at upem scale, metrics dict)."""
    f = load(wght, wdth)
    out = None; x = 0.0; adv = []
    for ch in text:
        gp, w = glyph_path(f, ch)
        gp = gp.transform(1,0,0,1,x,0)
        out = gp if out is None else pathops.op(out, gp, pathops.PathOp.UNION)
        adv.append((ch, x, w)); x += w + tracking
    total = x - tracking
    # flip to SVG y-down
    out = out.transform(1,0,0,-1,0,0)
    os2 = f['OS/2']
    m = dict(total=total, upem=f['head'].unitsPerEm,
             xheight=getattr(os2,'sxHeight',None), cap=getattr(os2,'sCapHeight',None),
             adv=adv, bounds=out.bounds)
    return out, m

if __name__ == "__main__":
    for wg in (600,700,800):
        p, m = wordmark(wght=wg)
        b = m['bounds']
        print(f"wght {wg}: xh={m['xheight']} cap={m['cap']} adv={m['total']:.0f} "
              f"bbox {b[2]-b[0]:.0f} x {b[3]-b[1]:.0f}  (y {b[1]:.0f}..{b[3]:.0f})")

def wedge(apex, half_angle_deg=20.0, reach=1400.0):
    """Right-opening V wedge used to re-cut the 'c' aperture."""
    a = math.radians(half_angle_deg)
    ax, ay = apex
    up   = (ax + reach, ay - reach*math.tan(a))
    dn   = (ax + reach, ay + reach*math.tan(a))
    q = pathops.Path(); pen=q.getPen()
    pen.moveTo(apex); pen.lineTo(up); pen.lineTo((ax+reach, ay+reach*2)); pen.lineTo(dn)
    pen.closePath()
    # simple triangle apex->up->dn is enough
    q = pathops.Path(); pen=q.getPen()
    pen.moveTo(apex); pen.lineTo(up); pen.lineTo(dn); pen.closePath()
    return pathops.simplify(q)

def custom_c(f, apex_x=250.0, apex_y=263.0, half_angle=20.0):
    """Archivo 'c' with its aperture re-cut to the mark's apex angle."""
    p, w = glyph_path(f, 'c')
    return pathops.op(p, wedge((apex_x, apex_y), half_angle), pathops.PathOp.DIFFERENCE), w
