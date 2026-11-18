#!/usr/bin/env python3
"""把 art_raw/ 里的装饰插画（白底/灰底 JPG）抠成透明 WebP，存到 art/。
Decorative illustrations only — the user's own photos are never touched here.

  watercolor (landscape / branch / landmark): white -> transparent (color-to-alpha)
  stamp / mascot: flood-fill the background from the corners, keep the paper/sticker edge
"""
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageFilter

SRC = Path(__file__).resolve().parent.parent
RAW, OUT = SRC / "art_raw", SRC / "art"
OUT.mkdir(exist_ok=True)


def color_to_alpha_white(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    # treat near-white paper (>= 0.94) as fully transparent
    lift = np.clip((a - 0.0) / 0.94, 0, 1)
    alpha = np.max(1.0 - lift, axis=2)
    alpha = np.clip(alpha * 1.15, 0, 1)
    safe = np.maximum(alpha, 1e-4)[..., None]
    rgb = (lift - (1 - alpha[..., None])) / safe
    rgb = np.clip(rgb * 0.94, 0, 1)
    out = np.dstack([rgb, alpha])
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


def flood_cutout(im, mode="mascot", feather=1.0):
    """Background = colour of the corners. Foreground = anything clearly
    different (brighter white sticker border, or coloured/darker stamp paper).
    Outer contours are filled so the inside of the shape stays solid."""
    rgb = np.asarray(im.convert("RGB")).astype(np.int16)
    h, w = rgb.shape[:2]
    c = 12
    corners = np.concatenate([rgb[:c, :c].reshape(-1, 3), rgb[:c, -c:].reshape(-1, 3),
                              rgb[-c:, :c].reshape(-1, 3), rgb[-c:, -c:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    L = rgb.mean(axis=2)
    Lbg = bg.mean()
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    if mode == "mascot":
        cand = (L - Lbg > 9) | (chroma > 28) | (Lbg - L > 60)
    else:  # stamp: white background, cream perforated paper
        cand = (Lbg - L > 6) | (chroma > 10)
    m = cand.astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    fill = np.zeros_like(m)
    for cn in cnts:
        if cv2.contourArea(cn) > 0.01 * h * w:
            cv2.drawContours(fill, [cn], -1, 255, -1)
    fill = cv2.erode(fill, np.ones((3, 3), np.uint8), iterations=1)
    a = Image.fromarray(fill).filter(ImageFilter.GaussianBlur(feather))
    out = im.convert("RGB").copy()
    out.putalpha(a)
    return out


def trim(im, pad=6):
    bbox = im.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox()
    if not bbox:
        return im
    x0, y0, x1, y1 = bbox
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def main():
    for f in sorted(RAW.glob("*.jpg")):
        kind = f.stem.split("_")[-1]
        im = Image.open(f)
        if kind in ("stamp",):
            out = flood_cutout(im, "stamp", 0.7)
        elif kind == "mascot":
            out = flood_cutout(im, "mascot", 1.0)
        else:
            out = color_to_alpha_white(im)
        out = trim(out)
        dst = OUT / (f.stem + ".webp")
        out.save(dst, "WEBP", quality=92, method=6)
        print("  art:", dst.name, out.size)


if __name__ == "__main__":
    main()
