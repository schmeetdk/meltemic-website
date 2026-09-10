import json, re, pathlib
F = json.loads(pathlib.Path("figs.json").read_text(encoding="utf-8"))
tpl = pathlib.Path("artifact.tpl.html").read_text(encoding="utf-8")

def fig(m):
    parts = m.group(1).split("|")
    key, opts = parts[0], parts[1:]
    if key not in F:
        raise KeyError(key)
    f = F[key]
    style, rule = "", ""
    for o in opts:
        if o.startswith("height:"):
            style = f'height:{o.split(":")[1]};width:auto;'
        elif o.startswith("w"):
            style = "width:100%;height:100%;display:block;"
        elif o == "evenodd":
            rule = ' fill-rule="evenodd"'
    if f.get("evenodd"):
        rule = ' fill-rule="evenodd"'
    st = f' style="{style}"' if style else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f["vb"]}" '
            f'aria-hidden="true"{st}><path{rule} d="{f["d"]}"/></svg>')

out = re.sub(r"\{\{FIG:([^}]+)\}\}", fig, tpl)

# all six families the page actually sets
out = out.replace(
  "family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap",
  "family=Archivo:wght@700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Inter:wght@400&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Orbitron:wght@700&display=swap")

# flatten the nested dark-theme media query for wider support
out = out.replace('''    :root:not([data-theme="light"]) {
        @media (prefers-color-scheme: dark) {''','''    @media (prefers-color-scheme: dark) {
        :root:not([data-theme="light"]) {''')

assert "{{" not in out, "unsubstituted placeholder"
pathlib.Path("artifact.html").write_text(out, encoding="utf-8")
print("artifact.html", len(out), "bytes ·", out.count("<svg"), "figures")
