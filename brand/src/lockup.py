import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from wordmark import *
from mark import gust, place, sk_to_d, rect_path, poly_to_skpath
import pathops

UPEM=1000; ASC=723.0; XH=526.0
GUST = dict(w=17.0, dx=28.0, h=76.0, over=-14.0, apex_cut=12.0)

def word(text="meltemic", wght=700, wdth=100, tracking=-18, custom=True,
         cx=265.0, ca=18.0):
    f = load(wght, wdth)
    out=None; x=0.0
    for i,ch in enumerate(text):
        if custom and ch=='c' and i==len(text)-1:
            gp,w = custom_c(f, apex_x=cx, half_angle=ca)
        else:
            gp,w = glyph_path(f,ch)
        gp = gp.transform(1,0,0,1,x,0)
        out = gp if out is None else pathops.op(out,gp,pathops.PathOp.UNION)
        x += w + tracking
    return out.transform(1,0,0,-1,0,0)   # y-down, baseline at y=0

def lockup(lean=7.0, mark_h=None, gap_ratio=0.42, mw_stroke=17.0, **wkw):
    """Horizontal lockup: mark + wordmark, baseline aligned, in y-down units."""
    wm = word(**wkw)
    wb = wm.bounds                       # y-down: top is negative
    mark_h = mark_h or ASC
    m = gust(lean=lean, **{**GUST,'w':mw_stroke})
    mb = m.bounds
    s = mark_h/(mb[3]-mb[1])
    m = m.transform(s,0,0,s,-mb[0]*s, -mb[1]*s)   # origin at 0,0 size mark_h
    mw = m.bounds[2]-m.bounds[0]
    m = m.transform(1,0,0,1,0,-mark_h)            # sit on baseline y=0
    gap = mark_h*gap_ratio
    wm = wm.transform(1,0,0,1, mw+gap - wb[0], 0)
    return pathops.op(m, wm, pathops.PathOp.UNION), mw+gap

def tight_svg(p, prec=2, pad=0.0):
    x0,y0,x1,y1 = p.bounds
    q = p.transform(1,0,0,1,-x0+pad,-y0+pad)
    return sk_to_d(q,prec), f"0 0 {x1-x0+2*pad:.2f} {y1-y0+2*pad:.2f}"
