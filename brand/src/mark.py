import sys, math, pathlib, pathops
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from geom import *

def poly_to_skpath(poly):
    p = pathops.Path()
    pen = p.getPen()
    pen.moveTo(poly[0])
    for pt in poly[1:]:
        pen.lineTo(pt)
    pen.closePath()
    return p

def rect_path(x0,y0,x1,y1):
    p = pathops.Path(); pen = p.getPen()
    pen.moveTo((x0,y0)); pen.lineTo((x1,y0)); pen.lineTo((x1,y1)); pen.lineTo((x0,y1)); pen.closePath()
    return p

def sk_to_d(p, prec=2):
    def f(v):
        s = f"{v:.{prec}f}".rstrip('0').rstrip('.')
        return '0' if s in ('-0','','-') else s
    out=[]
    for verb, pts in p.segments:
        if verb == 'moveTo':  out.append(f"M{f(pts[0][0])} {f(pts[0][1])}")
        elif verb == 'lineTo':out.append(f"L{f(pts[0][0])} {f(pts[0][1])}")
        elif verb == 'qCurveTo':
            for i in range(len(pts)-1):
                out.append(f"Q{f(pts[i][0])} {f(pts[i][1])} {f(pts[i+1][0])} {f(pts[i+1][1])}")
        elif verb == 'curveTo':
            out.append("C"+" ".join(f"{f(a)} {f(b)}" for a,b in pts))
        elif verb == 'closePath': out.append("Z")
    return "".join(out)

def sk_bbox(p):
    return p.bounds  # (xmin, ymin, xmax, ymax)

def gust(w=14.0, dx=22.0, h=76.0, over=0.0, apex_cut=12.0, valley_cut=0.0, lean=0.0):
    """Zigzag 'M'. Flat feet, flat-clipped apexes.
    over      = y-offset of the middle vertex relative to the foot baseline
                (negative lifts the valley above the feet, like a normal 'M').
    apex_cut  = units of the top miter spike removed (0 = fully pointed).
    valley_cut= units removed from the bottom (only meaningful if the valley
                dips below the feet)."""
    cap, base = 0.0, h
    xs = [i*dx for i in range(5)]
    ys = [base, cap, base+over, cap, base]
    pts = [(x + (base-y)*math.tan(math.radians(lean)), y) for x, y in zip(xs, ys)]
    poly = monoline_flatfoot(pts, w, base)
    p = poly_to_skpath(poly)
    x0,y0,x1,y1 = p.bounds
    top = y0 + apex_cut
    bot = max(y1 - valley_cut, base)
    clip = rect_path(x0-50, top, x1+50, bot)
    return pathops.op(p, clip, pathops.PathOp.INTERSECTION)

def place(p, box=128.0, pad=0.0):
    """Scale + center a skia path inside a square box."""
    x0,y0,x1,y1 = p.bounds
    W,H = x1-x0, y1-y0
    s = (box - 2*pad)/max(W,H)
    ox = pad + (box-2*pad - W*s)/2 - x0*s
    oy = pad + (box-2*pad - H*s)/2 - y0*s
    return p.transform(s,0,0,s,ox,oy)

def tight(p, prec=2):
    """Return (d, viewBox) with the path translated to a tight origin."""
    x0,y0,x1,y1 = p.bounds
    q = p.transform(1,0,0,1,-x0,-y0)
    return sk_to_d(q,prec), f"0 0 {x1-x0:.2f} {y1-y0:.2f}"


def stroked(pts, w, closed=False, cap=None, join=None, miter=8.0):
    """Stroke an open polyline into a filled path using Skia."""
    q = pathops.Path(); pen = q.getPen()
    pen.moveTo(pts[0])
    for pt in pts[1:]: pen.lineTo(pt)
    if closed: pen.closePath()
    else: pen.endPath()
    q.stroke(w, cap if cap is not None else pathops.LineCap.BUTT_CAP,
             join if join is not None else pathops.LineJoin.MITER_JOIN, miter)
    return pathops.simplify(q)

def chevrons(n=3, w=11.0, dx=27.0, h=42.0, gap=21.0):
    """Nested chevrons (isobars / pressure lines) pointing up."""
    out = None
    for i in range(n):
        y = i*gap
        pp = stroked([(0.0, y+h), (dx, y), (2*dx, y+h)], w)
        out = pp if out is None else pathops.op(out, pp, pathops.PathOp.UNION)
    return out

def barb(w=12.0, shaft_h=100.0, flags=3, flag_dx=36.0, flag_dy=20.0, gap=21.0):
    """Meteorological wind barb: a shaft with raking flags."""
    out = stroked([(0.0, 0.0), (0.0, shaft_h)], w)
    for i in range(flags):
        y = 6.0 + i*gap
        pp = stroked([(0.0, y), (flag_dx, y - flag_dy)], w)
        out = pathops.op(out, pp, pathops.PathOp.UNION)
    return out

def kite(w=13.0, span=104.0, rise=40.0, tail=0.0):
    """Kite canopy / sail leech: a bowed arc."""
    q = pathops.Path(); pen = q.getPen()
    pen.moveTo((0.0, rise))
    pen.curveTo((span*0.18, -rise*0.42), (span*0.82, -rise*0.42), (span, rise))
    pen.endPath()
    q.stroke(w, pathops.LineCap.BUTT_CAP, pathops.LineJoin.MITER_JOIN, 8.0)
    return pathops.simplify(q)
