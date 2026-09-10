import sys, os, math, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lockup import *
from mark import gust, place, sk_to_d
import pathops

OUT = r"C:\Users\p_bon\Dev\meltemic-website\meltemic-site\brand"
os.makedirs(OUT, exist_ok=True)

INK='#0B2733'; SEA='#14607A'; LIME='#F4F1EA'; CLAY='#C24A26'; SALT='#FFFFFF'
FINAL = dict(lean=7.0, tracking=-26, mark_h=ASC*1.14, mw_stroke=19.0, gap_ratio=0.40)

def svg(vb, body, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{extra}>'
            f'{body}</svg>\n')

def write(name, s):
    open(os.path.join(OUT,name),'w',encoding='utf-8').write(s)
    print(f"  {name}  {len(s):>6} bytes")

def roundsq(size, r):
    q=pathops.Path(); pen=q.getPen(); k=r*0.5523; s=size
    pen.moveTo((r,0)); pen.lineTo((s-r,0)); pen.curveTo((s-r+k,0),(s,r-k),(s,r))
    pen.lineTo((s,s-r)); pen.curveTo((s,s-r+k),(s-r+k,s),(s-r,s))
    pen.lineTo((r,s)); pen.curveTo((r-k,s),(0,s-r+k),(0,s-r))
    pen.lineTo((0,r)); pen.curveTo((0,r-k),(r-k,0),(r,0)); pen.closePath()
    return q

print("Building brand assets ->", OUT)

# 1. horizontal lockup
lp,_ = lockup(**FINAL)
d,vb = tight_svg(lp)
write('logo-lockup.svg', svg(vb, f'<path fill="currentColor" d="{d}"/>',
      ' role="img" aria-label="Meltemic"'))

# 2. mark alone
mk = gust(lean=7.0, **{**GUST,'w':19.0})
d,vb = tight_svg(mk)
write('logo-mark.svg', svg(vb, f'<path fill="currentColor" d="{d}"/>',
      ' role="img" aria-label="Meltemic"'))

# 3. wordmark alone
wm = word(tracking=-26)
d,vb = tight_svg(wm)
write('logo-wordmark.svg', svg(vb, f'<path fill="currentColor" d="{d}"/>',
      ' role="img" aria-label="meltemic"'))

# 4. stacked lockup
mb = mk.bounds; wb = wm.bounds
mh = ASC*1.30
s  = mh/(mb[3]-mb[1])
m2 = mk.transform(s,0,0,s,-mb[0]*s,-mb[1]*s)
mw = m2.bounds[2]
w2 = wm.transform(1,0,0,1,-wb[0],-wb[1])
ww = w2.bounds[2]
gap = mh*0.30
w2 = w2.transform(1,0,0,1,(mw-ww)/2, mh+gap)
m2 = m2.transform(1,0,0,1,max(0,(ww-mw)/2),0)
st = pathops.op(m2,w2,pathops.PathOp.UNION)
d,vb = tight_svg(st)
write('logo-stacked.svg', svg(vb, f'<path fill="currentColor" d="{d}"/>',
      ' role="img" aria-label="Meltemic"'))

# 5. app icon / avatar — mark knocked out of a rounded square
def icon(size=512, pad_ratio=0.185, r_ratio=0.22, bg=INK, fg=None):
    pad = size*pad_ratio
    m = place(gust(lean=7.0, **{**GUST,'w':19.0}), size, pad)
    if fg is None:
        p = pathops.op(roundsq(size, size*r_ratio), m, pathops.PathOp.DIFFERENCE)
        return svg(f"0 0 {size} {size}", f'<path fill="{bg}" fill-rule="evenodd" d="{sk_to_d(p)}"/>')
    return svg(f"0 0 {size} {size}",
        f'<path fill="{bg}" d="{sk_to_d(roundsq(size, size*r_ratio))}"/>'
        f'<path fill="{fg}" d="{sk_to_d(m)}"/>')

write('icon.svg', icon())
write('icon-sea.svg', icon(bg=SEA))
# favicon: tighter padding, squarer corners so the mark survives 16px
write('favicon.svg', icon(size=64, pad_ratio=0.115, r_ratio=0.16))

# 6. "tacking course" rule — the mark's geometry as a system device
def tack_rule(periods=3, w=13.0, dx=46.0, h=46.0, over=-8.0, lean=7.0):
    from geom import monoline_flatfoot
    from mark import poly_to_skpath, rect_path
    n = periods*2+1
    xs = [i*dx for i in range(n)]
    ys = [(h if i%2==0 else 0.0) for i in range(n)]
    ys = [(h+over if (i%2==0 and 0<i<n-1) else y) for i,y in enumerate(ys)]
    pts=[(x+(h-y)*math.tan(math.radians(lean)), y) for x,y in zip(xs,ys)]
    poly = monoline_flatfoot(pts, w, h)
    p = poly_to_skpath(poly)
    b=p.bounds
    p = pathops.op(p, rect_path(b[0]-9, b[1]+9, b[2]+9, b[3]+9), pathops.PathOp.INTERSECTION)
    return p
d,vb = tight_svg(tack_rule())
write('rule-tack.svg', svg(vb, f'<path fill="currentColor" d="{d}"/>'))

print("\nGeometry record:")
print(f"  mark: splay dx=28 h=76 stroke=19 apex_cut=12 vertex=-14 lean=7deg")
print(f"  lockup: mark_h = 1.14 x ascender({ASC}) = {ASC*1.14:.0f};  gap = 0.40 x mark_h")
print(f"  wordmark: Archivo wght700 wdth100, tracking -26/1000em, custom 'c' aperture 18deg @ x265")
