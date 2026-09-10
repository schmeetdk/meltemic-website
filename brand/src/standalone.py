import pathlib

src = pathlib.Path("artifact.html").read_text(encoding="utf-8")
out = pathlib.Path("C:/Users/p_bon/Dev/meltemic-website/meltemic-site/brand/brand-review.html")

# The published artifact is injected into a host-supplied skeleton, so the file
# starts at <title>. Split at the end of the stylesheet: everything before it is
# head material, everything after is the document body.
marker = "</style>"
i = src.index(marker) + len(marker)
head, body = src[:i], src[i:]

doc = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description"
        content="A brand and identity review of Meltemic OU conducted through Allan Peters' logo principles, with a rebuilt mark, wordmark and system.">
    <link rel="icon" href="favicon.svg" type="image/svg+xml">
    <link rel="icon" href="favicon.ico" sizes="16x16 32x32 48x48">
{head.strip()}
</head>

<body>
{body.strip()}
</body>

</html>
"""
out.write_text(doc, encoding="utf-8")
print(f"wrote {out}  ({len(doc):,} bytes)")

# make the README's cross-reference a real link now that the file exists
r = pathlib.Path("C:/Users/p_bon/Dev/meltemic-website/meltemic-site/brand/README.md")
s = r.read_text(encoding="utf-8")
s = s.replace(
  "See the build scripts referenced in the brand review; the parameters above are\nthe complete specification.",
  "The full brand review — the audit, the exploration and the reasoning behind\nevery number above — is in [`brand-review.html`](brand-review.html). The scripts\nthat generate the marks are in [`src/`](src/); run `python src/build.py` to\nregenerate every SVG from the parameters above.")
r.write_text(s, encoding="utf-8")
print("README cross-reference updated")
