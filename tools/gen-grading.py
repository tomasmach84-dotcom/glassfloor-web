# Sjednocené barevné ladění fotek GLASSFLOOR (prémiový chladný look)
# Vstup:  img/*.jpg   Výstup: img/graded/*.jpg (originály nedotčeny)
# Recept: 1) jemné vyvážení bílé (50 % gray-world, omezené zisky)
#         2) ztlumení sytosti na 85 %
#         3) chladnější tón (−1.5 % červená, +1.5 % modrá)
#         4) jednotný černý bod + mírný kontrast
import os
import numpy as np
from PIL import Image

SRC = r"C:\Users\thoma\OneDrive\Plocha\Claude projekty\GLASSFLOOR\GLASSFLOOR-web\img"
DST = os.path.join(SRC, "graded")
os.makedirs(DST, exist_ok=True)

SKIP = {"pozadi-kovova-deska.jpg"}  # pozadí jen zkopírovat beze změny

for name in sorted(os.listdir(SRC)):
    if not name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue
    src_path = os.path.join(SRC, name)
    dst_path = os.path.join(DST, name)
    if not os.path.isfile(src_path):
        continue
    im = Image.open(src_path).convert("RGB")
    if name in SKIP:
        im.save(dst_path, quality=93, subsampling=0)
        print("kopie:", name)
        continue

    x = np.asarray(im).astype(np.float64) / 255.0

    # 1) vyvážení bílé — gray-world na 50 %, zisky omezeny na ±8 %
    means = x.reshape(-1, 3).mean(axis=0)
    gray = means.mean()
    gain = gray / np.maximum(means, 1e-6)
    gain = 1 + 0.5 * (gain - 1)
    gain = np.clip(gain, 0.92, 1.08)
    x = x * gain[None, None, :]

    # 2) sytost 85 %
    y = x @ np.array([0.2126, 0.7152, 0.0722])
    x = y[..., None] + 0.85 * (x - y[..., None])

    # 3) chladnější tón
    x[..., 0] *= 0.985
    x[..., 2] *= 1.015

    # 4) jednotný černý bod (0.4. percentil jasu → 0) + mírný kontrast
    lo = np.percentile(y, 0.4)
    lo = float(np.clip(lo, 0.0, 0.06))
    x = (x - lo) / (1 - lo)
    x = 0.5 + (x - 0.5) * 1.045

    out = (np.clip(x, 0, 1) * 255).round().astype(np.uint8)
    Image.fromarray(out).save(dst_path, quality=90, subsampling=0, optimize=True)
    print("ladeno:", name)

print("HOTOVO")
