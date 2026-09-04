# -*- coding: utf-8 -*-
# UKAZKA 25.8.2026: PUVODNI (nezt tmavena) barevnost + VELMI JEMNA struktura lestene oceli.
# Stejny princip jako gen-pozadi-cmyk-ocel.py, jen vsechny slozky vyrazne ztlumene,
# aby ocel byla citit spis jako povrch nez jako vyrazna kresba.
import numpy as np
from PIL import Image
from scipy.ndimage import uniform_filter1d, gaussian_filter1d

OUT = r"C:\Users\thoma\OneDrive\Plocha\Claude projekty\GLASSFLOOR\GLASSFLOOR-web\img"


def hexc(h):
    return np.array([int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)], dtype=np.float64)


def steel(W, H, deg, stops, seed=7,
          fiber=4.0, bands=1.8, glint=7.0,
          sweep=(0.72, 0.10, 6.0), ridge_amp=8.0, contrast=1.01):
    ang = np.deg2rad(deg)
    dx, dy = np.sin(ang), np.cos(ang)
    xs = np.linspace(0, 1, W)[None, :]
    ys = np.linspace(0, 1, H)[:, None]
    t = xs * dx * (W / H) + ys * dy
    t = (t - t.min()) / (t.max() - t.min())

    pos = np.array([p for p, _ in stops])
    cols = np.stack([hexc(c) for _, c in stops])
    base = np.stack([np.interp(t, pos, cols[:, i]) for i in range(3)], axis=-1)

    rng = np.random.default_rng(seed)

    band = gaussian_filter1d(rng.normal(0, 1, size=(H, 1)), sigma=H / 7.0, axis=0)
    band /= band.std()
    band = band + 0.40 * (lambda b: b / b.std())(
        gaussian_filter1d(rng.normal(0, 1, size=(H, 1)), sigma=H / 22.0, axis=0))
    band /= band.std()

    cx, cy, amp = sweep[0] * W, sweep[1] * H, sweep[2]
    spec = np.clip(1 - np.sqrt(((np.arange(W)[None, :] - cx) / (0.95 * W)) ** 2 +
                               ((np.arange(H)[:, None] - cy) / (0.85 * H)) ** 2), 0, 1) ** 2.2
    spec = spec + 0.45 * np.clip(1 - np.sqrt(((np.arange(W)[None, :] - 0.30 * W) / (0.55 * W)) ** 2 +
                                             ((np.arange(H)[:, None] - 0.92 * H) / (0.45 * H)) ** 2), 0, 1) ** 3.0

    right = np.clip((np.arange(W)[None, :] / W - 0.10) / 0.75, 0, 1) ** 1.3
    ridge = np.exp(-(((t - 0.84) / 0.10) ** 2)) * right
    ridge += 0.40 * np.exp(-(((t - 0.60) / 0.07) ** 2)) * right

    f = uniform_filter1d(rng.normal(0, 1, size=(H, W)), size=260, axis=1)
    f += 0.55 * uniform_filter1d(rng.normal(0, 1, size=(H, W)), size=48, axis=1)
    f += 0.30 * uniform_filter1d(rng.normal(0, 1, size=(H, W)), size=11, axis=1)
    f /= f.std()

    g = uniform_filter1d(rng.normal(0, 1, size=(H, W)), size=80, axis=1)
    g += 0.8 * uniform_filter1d(rng.normal(0, 1, size=(H, W)), size=6, axis=1)
    g /= g.std()
    gl = np.clip(g, 0, None) ** 3.2
    gl /= (gl.max() + 1e-9)

    lum = base.mean(axis=-1)
    img = base + (band * bands * (0.55 + 0.9 * spec)
                  + f * fiber * np.clip(lum / 130.0, 0.55, 1.15)
                  + gl * glint * (0.30 + 1.2 * spec + 1.4 * ridge)
                  + spec * amp
                  + ridge * ridge_amp)[..., None]

    mid = img.mean()
    img = mid + (img - mid) * contrast

    l = np.clip(img.mean(axis=-1) / 200.0, 0, 1.4)
    img[..., 0] = img[..., 0] + (l - 0.5) * -2.0
    img[..., 2] = img[..., 2] + (l - 0.5) * 3.0

    img = img + rng.normal(0, 1.2, size=(H, W, 1))
    return np.clip(img, 0, 255).astype(np.uint8)


# PUVODNI barevnost (pred ztmavenim z 25.8.2026)
Image.fromarray(steel(2560, 1440, 118.0, [
    (0.00, '#1f2a33'), (0.34, '#33434f'), (0.62, '#4a5f6e'), (0.88, '#7b93a2'), (1.00, '#96acba'),
], seed=7)).save(OUT + r"\pozadi-puvodni-ocel.jpg", quality=94, subsampling=0, optimize=True)

# pomer strany odpovida levemu panelu hero (1/3 sirky okna), aby se pri
# oreznuti 'cover' neztratil svetly konec prechodu
Image.fromarray(steel(760, 1400, 105.0, [
    (0.00, '#26323c'), (0.46, '#3d505e'), (0.82, '#7d95a4'), (1.00, '#b7c6cf'),
], seed=19, fiber=3.6, bands=1.6, glint=6.0, sweep=(0.86, 0.12, 5.0), ridge_amp=6.0)).save(
    OUT + r"\pozadi-puvodni-ocel-hero.jpg", quality=94, subsampling=0, optimize=True)

print("HOTOVO")
