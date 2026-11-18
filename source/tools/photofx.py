"""照片的传统处理（不使用 AI）：裁切、撕纸边、白边、色调、颗粒。
Traditional processing of the user's ORIGINAL photos only:
crop, procedural torn-paper alpha masks, white paper fringe, tint, grain.
Every function returns a PIL RGBA image; render.py caches the result in cache/.
"""
from __future__ import annotations
import hashlib, json, math, random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

SRC = Path(__file__).resolve().parent.parent
PHOTOS = SRC / "photos"
CACHE = SRC / "cache"
CACHE.mkdir(exist_ok=True)


# ---------- helpers ----------
def crop_frac(im, box):
    """box = [x0, y0, x1, y1] as fractions of the photo (0-1)."""
    w, h = im.size
    x0, y0, x1, y1 = box
    return im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))


def fit_cover(im, w, h):
    return ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, 0.5))


def torn_line(p0, p1, rng, amp, step=7):
    """Jagged line from p0 to p1: random walk perpendicular + fine jitter."""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    n = max(2, int(L / step))
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    pts, off = [], 0.0
    for i in range(n + 1):
        t = i / n
        off += rng.uniform(-amp, amp) * 0.55
        off *= 0.86
        j = off + rng.uniform(-amp, amp) * 0.35
        if i in (0, n):
            j = 0
        pts.append((x0 + (x1 - x0) * t + nx * j, y0 + (y1 - y0) * t + ny * j))
    return pts


def torn_polygon(w, h, inset, rng, amp, sides="trbl"):
    corners = [(inset, inset), (w - inset, inset), (w - inset, h - inset), (inset, h - inset)]
    names = "trbl"
    pts = []
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]
        if names[i] in sides:
            seg = torn_line(a, b, rng, amp)
        else:
            seg = torn_line(a, b, rng, amp * 0.12, step=30)
        pts.extend(seg[:-1])
    return pts


def poly_mask(size, pts, scale=2):
    w, h = size
    m = Image.new("L", (w * scale, h * scale), 0)
    ImageDraw.Draw(m).polygon([(x * scale, y * scale) for x, y in pts], fill=255)
    return m.resize((w, h), Image.LANCZOS)


def fibrous(mask, rng, strength=0.55, blur=2.2):
    """Make a mask edge look like torn paper fibres."""
    a = np.asarray(mask.filter(ImageFilter.GaussianBlur(blur))).astype(np.float32) / 255
    noise = np.random.default_rng(rng.randint(0, 10**6)).random(a.shape).astype(np.float32)
    noise = np.asarray(Image.fromarray((noise * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255
    v = a + (noise - 0.5) * strength
    out = np.clip((v - 0.45) * 6, 0, 1)
    return Image.fromarray((out * 255).astype(np.uint8))


# ---------- colour treatments ----------
def tint(im, mode):
    """mode: none | warm | faded | duo:<dark hex>:<light hex> | cyan"""
    if not mode or mode == "none":
        return im
    rgb = im.convert("RGB")
    if mode == "warm":
        r, g, b = rgb.split()
        rgb = Image.merge("RGB", (r.point(lambda v: min(255, v * 1.04 + 6)), g, b.point(lambda v: v * 0.93)))
        return ImageEnhance.Color(rgb).enhance(0.9)
    if mode == "faded":
        rgb = ImageEnhance.Color(rgb).enhance(0.75)
        arr = np.asarray(rgb).astype(np.float32)
        arr = arr * 0.86 + np.array([34, 28, 18])
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if mode.startswith("duo") or mode == "cyan":
        if mode == "cyan":
            dark, light = "#1d3b5c", "#f1ead8"
        else:
            _, dark, light = mode.split(":")
        g = ImageOps.autocontrast(rgb.convert("L"), cutoff=1)
        return ImageOps.colorize(g, dark, light)
    return rgb


def grain(im, amount=7, seed=1):
    arr = np.asarray(im).astype(np.int16)
    n = np.random.default_rng(seed).normal(0, amount, arr.shape[:2])[..., None]
    arr[..., :3] = np.clip(arr[..., :3] + n, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), im.mode)


# ---------- the pieces ----------
def torn_photo(photo, box, w, h, seed=1, sides="trbl", fringe=16, amp=7, fx="none"):
    """Photo fragment with torn edges and a rough white paper fringe."""
    rng = random.Random(seed)
    im = Image.open(PHOTOS / photo).convert("RGB")
    im = tint(fit_cover(crop_frac(im, box), w, h), fx)
    im = grain(im, 4, seed)
    outer = torn_polygon(w, h, 3, rng, amp, sides)
    inner = torn_polygon(w, h, 3 + fringe, rng, amp * 0.8, sides if fringe else sides)
    om = fibrous(poly_mask((w, h), outer), rng, 0.7, 1.6)
    im_mask = fibrous(poly_mask((w, h), inner), rng, 0.35, 1.0) if fringe else om
    paper = Image.new("RGB", (w, h), (250, 247, 239))
    pn = np.asarray(paper).astype(np.int16)
    pn = np.clip(pn + np.random.default_rng(seed).normal(0, 4, pn.shape[:2])[..., None], 0, 255)
    paper = Image.fromarray(pn.astype(np.uint8))
    base = Image.composite(im, paper, im_mask)
    base.putalpha(om)
    return base


def polaroid(photo, box, w, h, border=26, bottom=110, seed=1, fx="none"):
    """White instant-print frame around a crop of the photo."""
    im = Image.open(PHOTOS / photo).convert("RGB")
    iw, ih = w - 2 * border, h - border - bottom
    im = tint(fit_cover(crop_frac(im, box), iw, ih), fx)
    frame = Image.new("RGB", (w, h), (251, 249, 244))
    fn = np.asarray(frame).astype(np.int16)
    fn = np.clip(fn + np.random.default_rng(seed).normal(0, 3, fn.shape[:2])[..., None], 0, 255)
    frame = Image.fromarray(fn.astype(np.uint8))
    frame.paste(grain(im, 3, seed), (border, border))
    # faint inner shadow line
    d = ImageDraw.Draw(frame)
    d.rectangle([border - 1, border - 1, border + iw, border + ih], outline=(225, 220, 210))
    frame.putalpha(255)
    return frame


def mini_print(photo, box, w, h, border=12, seed=1, fx="none", deckle=True):
    """Small print with a narrow white (optionally deckled) border."""
    rng = random.Random(seed)
    im = Image.open(PHOTOS / photo).convert("RGB")
    im = tint(fit_cover(crop_frac(im, box), w - 2 * border, h - 2 * border), fx)
    card = Image.new("RGB", (w, h), (250, 247, 240))
    card.paste(grain(im, 3, seed), (border, border))
    if deckle:
        m = fibrous(poly_mask((w, h), torn_polygon(w, h, 2, rng, 1.6)), rng, 0.4, 0.8)
    else:
        m = Image.new("L", (w, h), 255)
    card.putalpha(m)
    return card


def paper_scrap(w, h, kind="kraft", seed=1, sides="trbl", amp=8, color=None):
    """Torn scrap of plain, kraft, grid, lined or coloured paper (no photo)."""
    rng = random.Random(seed)
    nrng = np.random.default_rng(seed)
    base = {
        "kraft": (196, 160, 118), "cream": (243, 234, 214), "grid": (247, 243, 232),
        "lined": (248, 244, 234), "blue": (186, 207, 222), "pink": (240, 214, 214),
        "sage": (205, 214, 190), "ink": (52, 74, 104), "sand": (234, 214, 176),
    }.get(kind, (240, 234, 220))
    if color:
        base = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
    arr = np.ones((h, w, 3), np.float32) * np.array(base, np.float32)
    lo = nrng.normal(0, 1, (max(2, h // 40), max(2, w // 40)))
    lo = np.asarray(Image.fromarray(((lo - lo.min()) / (np.ptp(lo) + 1e-6) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    arr += (lo[..., None] - 0.5) * 16 + nrng.normal(0, 5, (h, w, 1))
    if kind == "kraft":
        fib = nrng.random((h, w)) > 0.996
        arr[fib] -= 35
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    if kind == "grid":
        for x in range(0, w, 28):
            d.line([(x, 0), (x, h)], fill=(196, 214, 222), width=1)
        for y in range(0, h, 28):
            d.line([(0, y), (w, y)], fill=(196, 214, 222), width=1)
    if kind == "lined":
        for y in range(40, h, 34):
            d.line([(0, y), (w, y)], fill=(190, 205, 220), width=1)
        d.line([(46, 0), (46, h)], fill=(226, 160, 160), width=1)
    m = fibrous(poly_mask((w, h), torn_polygon(w, h, 3, rng, amp, sides)), rng, 0.7, 1.6)
    # pale torn rim: inner layer is the paper core, outer 6px is lighter fibre
    rim = Image.new("RGB", (w, h), tuple(min(255, c + 22) for c in base))
    core = fibrous(poly_mask((w, h), torn_polygon(w, h, 9, random.Random(seed + 7), amp * 0.8, sides)), rng, 0.4, 1.2)
    im = Image.composite(im, rim, core)
    im.putalpha(m)
    return im


# ---------- cache front door ----------
def piece(_kind, **spec):
    """Return a cached PNG path (relative to source/) for this piece spec."""
    kind = _kind
    key = hashlib.md5(json.dumps([kind, spec], sort_keys=True).encode()).hexdigest()[:12]
    name = f"{kind}_{spec.get('photo', spec.get('kind', 'x')).split('.')[0]}_{key}.png"
    out = CACHE / name
    if not out.exists():
        fn = {"torn": torn_photo, "polaroid": polaroid, "mini": mini_print, "scrap": paper_scrap}[kind]
        fn(**spec).save(out, optimize=False, compress_level=3)
    return f"../cache/{name}"


# ---------- page paper ----------
def page_paper(path, w=1200, h=1600, base=(244, 237, 222), grid=None, seed=3, vignette=0.10):
    """Aged journal paper. grid = None | 'grid' | 'dots' | 'lines'.

    Internal marks (grid spacing, foxing, line weight) scale with w so a
    2x paper looks the same as the 1x paper, just sharper.
    """
    s = max(w / 1200.0, 1e-6)
    nrng = np.random.default_rng(seed)
    arr = np.ones((h, w, 3), np.float32) * np.array(base, np.float32)
    for scale, amp in ((int(round(60 * s)), 10), (int(round(14 * s)), 4)):
        scale = max(scale, 2)
        lo = nrng.normal(0, 1, (h // scale + 2, w // scale + 2))
        lo = np.asarray(Image.fromarray(((lo - lo.min()) / (np.ptp(lo)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
        arr += (lo[..., None] - 0.5) * amp
    arr += nrng.normal(0, 3.2, (h, w, 1))
    # foxing spots
    for _ in range(14):
        cx, cy, r = nrng.uniform(0, w), nrng.uniform(0, h), nrng.uniform(6 * s, 26 * s)
        yy, xx = np.ogrid[:h, :w]
        d = np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * r * r)))
        arr -= d[..., None] * np.array([8, 12, 20]) * nrng.uniform(0.3, 1)
    yy, xx = np.mgrid[:h, :w]
    v = ((xx / w - 0.5) ** 2 + (yy / h - 0.5) ** 2) ** 0.5
    arr *= (1 - vignette * np.clip(v - 0.25, 0, 1) * 2.2)[..., None]
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if grid:
        ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        col = (120, 160, 175, 46)
        step = max(1, int(round(40 * s)))
        lw = max(1, int(round(s)))
        if grid == "grid":
            for x in range(0, w, step):
                d.line([(x, 0), (x, h)], fill=col, width=lw)
            for y in range(0, h, step):
                d.line([(0, y), (w, y)], fill=col, width=lw)
        elif grid == "dots":
            rad = 1.6 * s
            for x in range(step // 2, w, step):
                for y in range(step // 2, h, step):
                    d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=(120, 130, 140, 70))
        elif grid == "lines":
            y0 = int(round(120 * s))
            ystep = max(1, int(round(44 * s)))
            for y in range(y0, h, ystep):
                d.line([(0, y), (w, y)], fill=col, width=lw)
        im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    im.save(path, quality=92, subsampling=0)
    return path
