# -*- coding: utf-8 -*-
# Pozadi pro barva-CMYK.html: modrosedy prechod + SAMETOVY AKCENT
#
# 3.9.2026 - majitel: lestena ocel (v2, gen-pozadi-cmyk-ocel.py) casto pusobila
# rusive - ostre trpytky a jasna hrana lesku pritahovaly pozornost na sebe misto
# na obsah. Tenhle skript pouziva STEJNOU generacni funkci (steel()) a STEJNE
# barevne prechody, jen s vyrazne potlacenymi ostrymi slozkami (glint, ridge,
# sweep) a lehkym rozmazanim navic, aby textura pusobila jako jemna latka
# s tichym leskem, ne jako zrcadlici se plech. Puvodni ocelova varianta
# zustava zachovana v _STARE/pozadi-pred-sametem-2026-09-03/.
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import uniform_filter1d, gaussian_filter1d

OUT = r"C:\Users\thoma\OneDrive\Plocha\Claude projekty\GLASSFLOOR\GLASSFLOOR-web\img"


def hexc(h):
    return np.array([int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)], dtype=np.float64)


def steel(W, H, deg, stops, seed=7,
          fiber=9.0, bands=7.0, glint=26.0,
          sweep=(0.72, 0.10, 30.0), ridge_amp=62.0, contrast=1.08):
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
    ridge = np.exp(-(((t - 0.84) / 0.085) ** 2)) * right
    ridge += 0.45 * np.exp(-(((t - 0.62) / 0.055) ** 2)) * right
    ridge += 0.22 * np.exp(-(((t - 0.40) / 0.09) ** 2)) * right

    f = uniform_filter1d(rng.normal(0, 1, size=(H, W)), size=260, axis=1)
    f += 0.55 * uniform_filter1d(rng.normal(0, 1, size=(H, W)), size=48, axis=1)
    f += 0.30 * uniform_filter1d(rng.normal(0, 1, size=(H, W)), size=11, axis=1)
    f /= f.std()

    g = uniform_filter1d(rng.normal(0, 1, size=(H, W)), size=80, axis=1)
    g += 0.8 * uniform_filter1d(rng.normal(0, 1, size=(H, W)), size=6, axis=1)
    g /= g.std()
    gl = np.clip(g, 0, None) ** 3.2
    gl /= (gl.max() + 1e-9)

    lit = 0.30 + 1.55 * spec
    lum = base.mean(axis=-1)

    add = (band * bands * (0.55 + 0.9 * spec)
           + f * fiber * np.clip(lum / 105.0, 0.45, 1.35)
           + gl * glint * (lit + 2.2 * ridge)
           + spec * amp
           + ridge * ridge_amp)

    img = base + add[..., None]

    mid = img.mean()
    img = mid + (img - mid) * contrast

    l = np.clip(img.mean(axis=-1) / 200.0, 0, 1.4)
    img[..., 0] = img[..., 0] + (l - 0.5) * -6.0
    img[..., 2] = img[..., 2] + (l - 0.5) * 9.0

    img = img + rng.normal(0, 1.5, size=(H, W, 1))
    return np.clip(img, 0, 255).astype(np.uint8)


def sametovy(arr, blur_radius=2.2):
    """Jemne rozmaze zrno textury do latkoveho vzhledu, barvy a sirsi prechody
    zustavaji ostre (blur jde jen na jemny detail, ne na velke plochy)."""
    im = Image.fromarray(arr)
    soft = im.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return soft


# --- hlavni pozadi stranky (body), 118deg — stejne barvy jako ocelova verze,
#     ale glint/ridge/sweep vyrazne dolu a navic mekke rozmazani ---
hlavni = steel(2560, 1440, 118.0, [
    (0.00, '#151f27'), (0.34, '#27343e'), (0.62, '#3b4d5a'), (0.88, '#66798a'), (1.00, '#8090a0'),
], seed=7, fiber=4.0, bands=3.0, glint=4.0, sweep=(0.72, 0.10, 14.0), ridge_amp=18.0, contrast=1.0)
sametovy(hlavni, blur_radius=2.4).save(OUT + r"\pozadi-cmyk-samet.jpg", quality=94, subsampling=0, optimize=True)

# --- levy panel hero, 105deg ---
hero = steel(1200, 1600, 105.0, [
    (0.00, '#1c2630'), (0.46, '#30404c'), (0.82, '#657a88'), (1.00, '#98a6b0'),
], seed=19, fiber=3.6, bands=2.6, glint=4.0, sweep=(0.86, 0.12, 12.0), ridge_amp=14.0, contrast=1.0)
sametovy(hero, blur_radius=2.0).save(OUT + r"\pozadi-cmyk-samet-hero.jpg", quality=94, subsampling=0, optimize=True)

print("HOTOVO")
