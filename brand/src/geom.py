import math

def unit(v):
    l = math.hypot(*v)
    return (v[0]/l, v[1]/l)

def line_from_point_dir(p, d):
    # returns (a,b,c) for ax+by=c
    a, b = d[1], -d[0]
    return (a, b, a*p[0] + b*p[1])

def isect(L1, L2):
    a1,b1,c1 = L1; a2,b2,c2 = L2
    det = a1*b2 - a2*b1
    if abs(det) < 1e-12:
        return None
    return ((c1*b2 - c2*b1)/det, (a1*c2 - a2*c1)/det)

def offset_side(pts, d):
    """Offset an open polyline by distance d (signed, along left normal) with miter joins.
    Returns list of points, same count as input."""
    lines = []
    for i in range(len(pts)-1):
        p, q = pts[i], pts[i+1]
        dr = unit((q[0]-p[0], q[1]-p[1]))
        n = (-dr[1], dr[0])            # left normal
        op = (p[0] + n[0]*d, p[1] + n[1]*d)
        lines.append(line_from_point_dir(op, dr))
    out = []
    # first point: on first offset line, at perpendicular foot of pts[0]
    dr0 = unit((pts[1][0]-pts[0][0], pts[1][1]-pts[0][1]))
    n0 = (-dr0[1], dr0[0])
    out.append((pts[0][0] + n0[0]*d, pts[0][1] + n0[1]*d))
    for i in range(len(lines)-1):
        p = isect(lines[i], lines[i+1])
        out.append(p)
    drN = unit((pts[-1][0]-pts[-2][0], pts[-1][1]-pts[-2][1]))
    nN = (-drN[1], drN[0])
    out.append((pts[-1][0] + nN[0]*d, pts[-1][1] + nN[1]*d))
    return out

def extend_to_y(p, direction, y):
    """Move point p along `direction` until it hits horizontal line y."""
    if abs(direction[1]) < 1e-12:
        return p
    t = (y - p[1]) / direction[1]
    return (p[0] + direction[0]*t, y)

def monoline_flatfoot(pts, w, foot_y):
    """Outline of a monoline polyline of perpendicular width w,
    whose two terminals are cut flat (horizontally) at y=foot_y."""
    left  = offset_side(pts, +w/2)
    right = offset_side(pts, -w/2)
    d_start = unit((pts[1][0]-pts[0][0], pts[1][1]-pts[0][1]))
    d_end   = unit((pts[-1][0]-pts[-2][0], pts[-1][1]-pts[-2][1]))
    left[0]  = extend_to_y(left[0],  d_start, foot_y)
    right[0] = extend_to_y(right[0], d_start, foot_y)
    left[-1]  = extend_to_y(left[-1],  d_end, foot_y)
    right[-1] = extend_to_y(right[-1], d_end, foot_y)
    return left + list(reversed(right))

def path_d(poly, close=True, prec=3):
    def f(v): 
        s = f"{v:.{prec}f}".rstrip('0').rstrip('.')
        return s if s not in ('-0','') else '0'
    d = f"M{f(poly[0][0])} {f(poly[0][1])}"
    for p in poly[1:]:
        d += f"L{f(p[0])} {f(p[1])}"
    return d + ("Z" if close else "")

def bbox(poly):
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)
