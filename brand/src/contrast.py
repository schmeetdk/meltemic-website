def lin(c):
    c/=255
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def L(h):
    h=h.lstrip('#'); r,g,b=(int(h[i:i+2],16) for i in (0,2,4))
    return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
def ratio(a,b):
    la,lb=L(a),L(b)
    hi,lo=max(la,lb),min(la,lb)
    return (hi+0.05)/(lo+0.05)

P = dict(ink='#0B2733', sea='#14607A', gust='#8FBFCE',
         clay='#C24A26', clay2='#D4552E', clay3='#B8431F',
         limestone='#F4F1EA', salt='#FFFFFF', slate='#54707C')
pairs = [('ink','limestone'),('ink','salt'),('sea','limestone'),('sea','salt'),
         ('slate','limestone'),('salt','clay'),('salt','clay2'),('salt','clay3'),
         ('salt','ink'),('salt','sea'),('gust','ink'),('limestone','ink'),
         ('clay','ink'),('clay2','ink')]
for a,b in pairs:
    r=ratio(P[a],P[b])
    tag = 'AAA' if r>=7 else 'AA' if r>=4.5 else 'AA-large' if r>=3 else 'FAIL'
    print(f"{a:10}({P[a]}) on {b:10}({P[b]}) = {r:5.2f}  {tag}")
