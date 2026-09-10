import sys, json, pathlib; sys.path.insert(0,'.')
from lockup import *
from mark import gust, place, chevrons, barb, kite, sk_to_d
from wordmark import load, glyph_path, custom_c
from build import roundsq, GUST
import pathops

F = {}
def add(key, p, pad=0.0):
    d, vb = tight_svg(p, pad=pad)
    F[key] = {"d": d, "vb": vb}

E = dict(w=17.0, dx=28.0, h=76.0, over=-14.0, apex_cut=12.0)
FIN = {**GUST, 'w':19.0}

add("c_gust",     gust(**E))
add("c_lean",     gust(**{**E,'lean':7.0}))
add("c_barb",     barb())
add("c_isobar",   chevrons())
add("c_kite",     kite())
add("mark",       gust(lean=7.0, **FIN))
add("lockup",     lockup(lean=7.0, tracking=-26, mark_h=ASC*1.14, mw_stroke=19.0, gap_ratio=0.40)[0])
add("wordmark",   word(tracking=-26))
add("rule",       __import__('build').tack_rule(periods=3, w=13.0, dx=46.0, h=46.0, over=-8.0, lean=7.0))

# sails knockout (needs even-odd)
sails = pathops.op(roundsq(128, 128*0.22), place(gust(lean=7.0, **FIN), 128, 128*0.185),
                   pathops.PathOp.DIFFERENCE)
F["c_sails"] = {"d": sk_to_d(sails), "vb": "0 0 128 128", "evenodd": True}
icon = pathops.op(roundsq(512, 512*0.22), place(gust(lean=7.0, **FIN), 512, 512*0.185),
                  pathops.PathOp.DIFFERENCE)
F["icon"] = {"d": sk_to_d(icon), "vb": "0 0 512 512", "evenodd": True}

f = load(700, 100)
stock, _ = glyph_path(f, 'c')
cust,  _ = custom_c(f, apex_x=265.0, half_angle=18.0)
# shared coordinate space: same viewBox for both, so the re-cut is legible
_s = stock.transform(1,0,0,-1,0,0); _c = cust.transform(1,0,0,-1,0,0)
sb, cb = _s.bounds, _c.bounds
x0, y0 = min(sb[0],cb[0])-14, min(sb[1],cb[1])-14
x1, y1 = max(sb[2],cb[2])+14, max(sb[3],cb[3])+14
vb = f"{x0:.2f} {y0:.2f} {x1-x0:.2f} {y1-y0:.2f}"
F["c_stock"]  = {"d": sk_to_d(_s), "vb": vb}
F["c_custom"] = {"d": sk_to_d(_c), "vb": vb}

# old logo, for the before/after
F["_meta"] = {"count": len(F)}
pathlib.Path("figs.json").write_text(json.dumps(F), encoding="utf-8")
print("figures:", ", ".join(k for k in F if not k.startswith('_')))
print("bytes:", pathlib.Path("figs.json").stat().st_size)
