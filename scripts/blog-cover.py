"""Genera la portada de un artículo del blog (1200x630 JPG) con la identidad de Fluxxo.

Uso:
  python3 scripts/blog-cover.py <slug> "<categoría>" "<título corto de portada>"
Salida: public/blog/<slug>.jpg  (se referencia en el frontmatter como image: "/blog/<slug>.jpg")
"""
import os, sys, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, S = 1200, 630, 2
BLUE, BONE, SOFT, BG = (77, 158, 255), (248, 245, 240), (165, 170, 178), (8, 8, 8)
FONT_DIRS = ['/usr/share/fonts/truetype/google-fonts/', '/usr/share/fonts/truetype/dejavu/', 'C:/Windows/Fonts/']

def font(names, size):
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size * S)
    return ImageFont.load_default()

def main(slug, category, title):
    img = Image.new('RGB', (W * S, H * S), BG)
    glow = Image.new('RGB', (W * S, H * S), BG)
    g = ImageDraw.Draw(glow)
    g.ellipse((650 * S, -300 * S, 1550 * S, 500 * S), fill=(28, 60, 104))
    g.ellipse((-300 * S, 420 * S, 400 * S, 1000 * S), fill=(14, 30, 54))
    img = glow.filter(ImageFilter.GaussianBlur(170 * S))
    d = ImageDraw.Draw(img)
    # rejilla sutil
    for x in range(0, W * S, 60 * S):
        d.line([(x, 0), (x, H * S)], fill=(20, 22, 26), width=1)
    for y in range(0, H * S, 60 * S):
        d.line([(0, y), (W * S, y)], fill=(20, 22, 26), width=1)
    # logo
    k, ox, oy = 2.4 * S, 80 * S, 70 * S
    P = lambda x, y: (ox + x * k, oy + y * k)
    w = int(2.4 * k)
    d.arc([P(3, 3), P(23, 23)], 90, 270, fill=BLUE, width=w)
    d.arc([P(4.5, 3), P(21.5, 23)], 270, 90, fill=BLUE, width=w)
    cx, cy = P(21.5, 13); r = 2.5 * k
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=BLUE)
    wf = font(['Poppins-Medium.ttf', 'DejaVuSans.ttf', 'arial.ttf'], 34)
    x = ox + 32 * k; y = oy + 4 * k
    for part, col in (('flu', BONE), ('xx', BLUE), ('o', BONE)):
        d.text((x, y), part, font=wf, fill=col); x += d.textlength(part, font=wf)
    # categoría (pastilla)
    cf = font(['Poppins-Medium.ttf', 'DejaVuSans.ttf', 'arial.ttf'], 20)
    label = category.upper()
    tw = d.textlength(label, font=cf)
    bx, by = 80 * S, 200 * S
    d.rounded_rectangle((bx, by, bx + tw + 36 * S, by + 44 * S), radius=22 * S, outline=(60, 110, 180), width=2 * S, fill=(14, 28, 48))
    d.text((bx + 18 * S, by + 8 * S), label, font=cf, fill=BLUE)
    # título
    size = 64
    while True:
        tf = font(['Poppins-SemiBold.ttf', 'Poppins-Medium.ttf', 'DejaVuSans-Bold.ttf', 'arialbd.ttf'], size)
        lines = textwrap.wrap(title, width=max(10, int(1900 / size)))
        if len(lines) <= 3 and all(d.textlength(l, font=tf) <= 1040 * S for l in lines) or size <= 40:
            break
        size -= 4
    ty = 280 * S
    for l in lines:
        d.text((80 * S, ty), l, font=tf, fill=BONE)
        ty += int(size * 1.22) * S
    # pie
    ff = font(['Poppins-Regular.ttf', 'DejaVuSans.ttf', 'arial.ttf'], 22)
    d.text((80 * S, 560 * S), 'fluxxoai.com/blog', font=ff, fill=SOFT)
    img = img.resize((W, H), Image.LANCZOS)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, 'public', 'blog', f'{slug}.jpg')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, 'JPEG', quality=86, optimize=True, progressive=True)
    print(out)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
