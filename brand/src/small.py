import pathlib, subprocess
from PIL import Image
B = pathlib.Path("C:/Users/p_bon/Dev/meltemic-website/meltemic-site/brand")
SP = pathlib.Path(__file__).parent
CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe"

def render(svg_name, px, out):
    svg = (B/svg_name).read_text(encoding="utf-8")
    html = ("<html><body style='margin:0'>"
            f"<div style='width:{px}px;height:{px}px'>"
            + svg.replace('<svg', '<svg style="width:100%;height:100%;display:block"')
            + "</div></body></html>")
    tmp = SP/'_s.html'; tmp.write_text(html, encoding="utf-8")
    subprocess.run([CHROME,'--headless','--disable-gpu','--no-sandbox',
        '--user-data-dir='+str(SP/'chromeprofile'),'--hide-scrollbars',
        '--default-background-color=00000000','--force-device-scale-factor=1',
        '--screenshot='+str(out), f'--window-size={px},{px}', tmp.as_uri()],
        capture_output=True)

# render both sources at a comfortable size, then downsample with Lanczos
render('favicon.svg', 512, SP/'fav512.png')
render('icon-square.svg', 512, SP/'sq512.png')

fav = Image.open(SP/'fav512.png').convert('RGBA')
sq  = Image.open(SP/'sq512.png').convert('RGBA')
rnd = Image.open(B/'icon-512.png').convert('RGBA')

for img, size, name in [(fav,32,'favicon-32.png'), (fav,16,'favicon-16.png'),
                        (sq,180,'apple-touch-icon.png'), (rnd,192,'icon-192.png')]:
    img.resize((size,size), Image.LANCZOS).save(B/name, optimize=True)
    print(f"  {name}  {size}px  {(B/name).stat().st_size} bytes")

# multi-resolution .ico for legacy browsers
fav.resize((64,64), Image.LANCZOS).save(B/'favicon.ico',
    sizes=[(16,16),(32,32),(48,48)])
print(f"  favicon.ico  {(B/'favicon.ico').stat().st_size} bytes")
