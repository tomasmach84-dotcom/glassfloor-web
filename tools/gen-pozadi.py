# Vygeneruje pozadí "kovová deska" — diagonální přechod + odlesk + dithering
# Výstup: img/pozadi-kovova-deska.jpg (2560x1440)
import numpy as np
from PIL import Image

W, H = 2560, 1440

# diagonální souřadnice 0..1 pod úhlem 118° (CSS úhel: 0deg = nahoru, po směru hod. ručiček)
# CSS 118deg ≈ směr vektoru (sin118, -cos118) v obrazových souřadnicích (y dolů)
ang = np.deg2rad(118.0)
dx, dy = np.sin(ang), np.cos(ang)  # y roste dolů → cos se nepřevrací dvakrát
xs = np.linspace(0, 1, W)[None, :]
ys = np.linspace(0, 1, H)[:, None]
t = xs * dx * (W / H) + ys * dy
t = (t - t.min()) / (t.max() - t.min())

# zarážky přechodu (pozice 0..1, šedá 0..255) — kovová deska se světlým pásem v ~70 %
# 20.7.2026 v3: TMAVÁ broušená ocel (antracit) — textura broušení v celé ploše,
# ale jas držený tak, aby bílé písmo zůstalo čitelné přímo na kovu
stops = [
    (0.00,   0), (0.10,  10), (0.20,  22), (0.29,  36), (0.38,  52),
    (0.47,  70), (0.55,  88), (0.62, 104), (0.68, 118), (0.72, 126),
    (0.77, 118), (0.83, 100), (0.89,  76), (0.94,  56), (1.00,  38),
]
pos = np.array([p for p, v in stops])
val = np.array([v for p, v in stops], dtype=np.float64)
base = np.interp(t, pos, val)

# kosinová interpolace mezi zarážkami by byla hladší; np.interp je lineární,
# proto přechod lehce rozostříme filtrací po diagonále (stačí jemný blur přes t)
# — jednodušší: převzorkovat přes hladkou křivku pomocí konvoluce není nutné,
#   dithering níže schody stejně rozbije.

# šikmý světelný odlesk (elipsa u pravého horního rohu)
cx, cy = 0.76 * W, 0.08 * H
rx, ry = 1.10 * W, 0.90 * H
d2 = ((np.arange(W)[None, :] - cx) / rx) ** 2 + ((np.arange(H)[:, None] - cy) / ry) ** 2
sheen = np.clip(1 - np.sqrt(d2), 0, 1) ** 1.6 * 14.0  # max +14 úrovní

img = base + sheen

# textura broušené oceli: jemná vodorovná vlákna (šum silně rozmazaný podél X)
from scipy.ndimage import uniform_filter1d
rng_b = np.random.default_rng(7)
fibers = rng_b.normal(0, 1, size=(H, W))
fibers = uniform_filter1d(fibers, size=220, axis=1)   # protáhnout do vláken
fibers += 0.45 * uniform_filter1d(rng_b.normal(0, 1, size=(H, W)), size=40, axis=1)
fibers /= fibers.std()
img = img + fibers * 6.0 * np.clip(img / 100.0, 0.15, 1.0)  # vlákna viditelná i v tmavším kovu

# okraje vlevo i vpravo do ČISTÉ ČERNÉ (přání majitele) — kosinový náběh přes 30 % šířky
xs_pix = np.linspace(0, 1, W)[None, :]
ramp_l = np.clip(xs_pix / 0.30, 0, 1)
ramp_r = np.clip((1 - xs_pix) / 0.30, 0, 1)
smooth = lambda u: 0.5 - 0.5 * np.cos(np.pi * u)   # plynulý náběh bez zlomů
edge = smooth(ramp_l) * smooth(ramp_r)
img = img * edge

# mírný tmavý nádech do modrozelena? NE — neutrální šedá (přání: černá/šedá)
# dithering: gaussovský šum ~1.4 úrovně PŘED kvantizací → žádné viditelné schody
rng = np.random.default_rng(42)
noise = rng.normal(0, 1.4, size=(H, W)) * edge   # na černých okrajích žádný šum
img = np.clip(img + noise, 0, 255)

# tři kanály (neutrální šedá s nepatrným ochlazením, ať ladí s webem)
r = img * 0.985
g = img * 1.000
b = img * 1.010
out = np.stack([r, g, b], axis=-1)
out = np.clip(out, 0, 255).astype(np.uint8)

Image.fromarray(out).save(
    r"C:\Users\thoma\OneDrive\Plocha\Claude projekty\GLASSFLOOR\GLASSFLOOR-web\img\pozadi-kovova-deska.jpg",
    quality=93, subsampling=0, optimize=True)
print("HOTOVO")
