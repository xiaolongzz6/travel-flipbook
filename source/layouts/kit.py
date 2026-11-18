"""拼贴图层工具箱 —— collage layer kit.

每个函数返回一段 HTML（一个绝对定位的图层）。坐标单位是像素，
单页尺寸 1200 x 1600（CSS；照片碎片按 SCALE=2 生成），(0,0) 在页面左上角。
    x, y   = 图层左上角位置
    w      = 宽度（高度按图片比例自动）
    rot    = 旋转角度（正数 = 顺时针）
    z      = 叠放顺序（数字大的在上面）
"""
from __future__ import annotations
import hashlib, math, random, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC / "tools"))
import photofx as F  # noqa: E402

CFG = None   # render.py sets this to config.json
PHOTO = None  # key -> filename map

# Photo pieces and page paper are generated at this density so Playwright
# can screenshot the 1200x1600 CSS layout at device_scale_factor=SCALE
# without upscaling a smaller intermediate. CSS coordinates stay at 1x.
SCALE = 2

def _px(v):
    """Scale a generation-time pixel size; None stays None."""
    return None if v is None else int(round(v * SCALE))


def _photo(key):
    return CFG["photos"].get(key, key)


def _wrap(inner, x, y, w, h=None, rot=0, z=5, cls="", style=""):
    hh = f"height:{h}px;" if h else ""
    return (f'<div class="L {cls}" style="left:{x}px;top:{y}px;width:{w}px;{hh}'
            f'transform:rotate({rot}deg);z-index:{z};{style}">{inner}</div>')


# ---------------------------------------------------------------- photos
def torn(key, box, x, y, w, h, rot=0, z=5, seed=1, sides="trbl", fringe=16, amp=8, fx="none"):
    """他的照片 → 撕纸边碎片. box = 照片裁切范围 [左,上,右,下]（0~1 的比例）"""
    src = F.piece("torn", photo=_photo(key), box=box, w=_px(w), h=_px(h), seed=seed, sides=sides,
                  fringe=_px(fringe), amp=_px(amp), fx=fx)
    return _wrap(f'<img src="{src}">', x, y, w, None, rot, z, "sh")


def polaroid(key, box, x, y, w, h, rot=0, z=10, caption="", cap_size=30, seed=1, bottom=120, fx="none"):
    """白边拍立得 + 手写说明"""
    src = F.piece("polaroid", photo=_photo(key), box=box, w=_px(w), h=_px(h),
                  border=_px(26), bottom=_px(bottom), seed=seed, fx=fx)
    cap = f'<div class="cap" style="bottom:{bottom*0.28:.0f}px;font-size:{cap_size}px">{caption}</div>' if caption else ""
    return (f'<div class="pol sh" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z}">'
            f'<img src="{src}">{cap}</div>')


def mini(key, box, x, y, w, h, rot=0, z=8, seed=1, border=12, fx="none"):
    """小相片（窄白边）"""
    src = F.piece("mini", photo=_photo(key), box=box, w=_px(w), h=_px(h), seed=seed, border=_px(border), fx=fx)
    return _wrap(f'<img src="{src}">', x, y, w, None, rot, z, "sh")


def scrap(kind, x, y, w, h, rot=0, z=2, seed=1, sides="trbl", amp=9, color=None):
    """撕下来的纸片（牛皮纸 kraft / 方格 grid / 横线 lined / cream / blue / pink / sage / sand / ink）"""
    src = F.piece("scrap", kind=kind, w=_px(w), h=_px(h), seed=seed, sides=sides, amp=_px(amp), color=color)
    return _wrap(f'<img src="{src}">', x, y, w, None, rot, z, "sh-soft")


# ---------------------------------------------------------------- art (decorative illustrations)
def art(name, x, y, w, rot=0, z=3, opacity=1, flip=False, shadow=False, mult=False):
    """装饰插画：art/<name>.png（水彩风景、花枝、地标、贴纸、邮票）"""
    fl = "transform:scaleX(-1);" if flip else ""
    cls = ("sh-soft " if shadow else "") + ("mult" if mult else "")
    return _wrap(f'<img src="../art/{name}.webp" style="{fl}">', x, y, w, None, rot, z, cls, f"opacity:{opacity};")


def sticker(name, x, y, w, rot=0, z=30):
    return _wrap(f'<img src="../art/{name}.webp">', x, y, w, None, rot, z, "sh")


def stamp(place, x, y, w, rot=0, z=20):
    """邮票：图 art/<place>_stamp.png + 下方空白处的文字（config.json → stamp）"""
    s = CFG["place"][place]["stamp"]
    fs = w * 0.068
    return (f'<div class="stamp sh" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z};font-size:{fs:.1f}px">'
            f'<img src="../art/{place}_stamp.webp">'
            f'<div class="st" style="bottom:{w*0.17:.0f}px"><span class="c">{s["country"]}</span><span class="v">{s["value"]}</span></div></div>')


# ---------------------------------------------------------------- ink & paper bits (drawn in code)
def _rid(*a):
    return "i" + hashlib.md5(repr(a).encode()).hexdigest()[:8]


ICONS = {
    # tiny line icons used in the centre of postmarks (stroke-only, viewBox -20..20)
    "sakura": "".join(f'<ellipse cx="0" cy="-9" rx="5" ry="8" transform="rotate({a})"/>' for a in range(0, 360, 72)) + '<circle r="2.5"/>',
    "turtle": '<ellipse rx="11" ry="8"/><path d="M-4-8 0-3 4-8M-11 0h22M-4 8 0 3 4 8"/><circle cx="14" cy="0" r="3.5"/><path d="M-8-7-14-12M-8 7-14 12M8-7 12-12M8 7 12 12"/>',
    "frangipani": "".join(f'<path d="M0 0C-6-6-4-16 0-17C5-16 6-7 0 0" transform="rotate({a})"/>' for a in range(0, 360, 72)) + '<circle r="2"/>',
    "pagoda": '<path d="M0-17v4M-8-12h16l-3 3h-10zM-10-6h20l-3 3h-14zM-12 1h24l-3 3h-18zM-14 8h28M-8 8v8M8 8v8M-12 16h24"/>',
    "sun": '<circle r="7"/>' + "".join(f'<path d="M0-11v-5" transform="rotate({a})"/>' for a in range(0, 360, 45)) + '<path d="M-17 14h34M-12 18h24"/>',
    "tangerine": '<circle cy="3" r="12"/><path d="M0-9c-2-5 0-8 3-9M1-9c4-5 10-4 11-1-4 2-8 2-11 1"/><circle cx="-4" cy="0" r=".9"/><circle cx="4" cy="6" r=".9"/>',
    "mountain": '<path d="M-17 12 -5-8 0-2 6-12 17 12zM-8-3l3-5 3 4M3-7l3-5 4 6"/><path d="M-17 16h34"/>',
}


def postmark(place, x, y, size=210, rot=-10, z=24, color="#7a2e2a", lines=True):
    """圆形邮戳（文字来自 config.json → postmark）"""
    pm = CFG["place"][place]["postmark"]
    pid = _rid(place, x, y)
    r = 92
    icon = ICONS.get(pm.get("icon", "sakura"), ICONS["sakura"])
    wave = ""
    if lines:
        for i in range(4):
            yy = -24 + i * 16
            wave += f'<path d="M110 {yy} q 22 -12 44 0 t 44 0 t 44 0 t 44 0" />'
    svg = f'''<svg class="svgL" viewBox="-110 -110 {220 + (190 if lines else 0)} 220" width="{size * (1 + (0.86 if lines else 0)):.0f}" height="{size}" style="left:0;top:0">
<defs>
<filter id="{pid}" x="-20%" y="-20%" width="140%" height="140%">
 <feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="{len(place)}" result="n"/>
 <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.35" result="a"/>
 <feComposite in="SourceGraphic" in2="a" operator="in" result="t"/>
 <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="1" seed="3" result="w"/>
 <feDisplacementMap in="t" in2="w" scale="5"/>
</filter>
<path id="{pid}t" d="M-74 0a74 74 0 1 1 148 0"/>
<path id="{pid}b" d="M-78 0a78 78 0 1 0 156 0"/>
</defs>
<g filter="url(#{pid})" fill="none" stroke="{color}" stroke-width="3.2" opacity=".86">
 <circle r="{r}" /><circle r="{r - 9}" stroke-width="1.6"/>
 <circle r="44" stroke-width="1.6"/>
 <g transform="scale(1.6)" stroke-width="1.6">{icon}</g>
 <text fill="{color}" stroke="none" font-family="Special Elite, monospace" font-size="19" letter-spacing="4.5" text-anchor="middle"><textPath href="#{pid}t" startOffset="50%">{pm["top"]}</textPath></text>
 <text fill="{color}" stroke="none" font-family="Special Elite, monospace" font-size="17" letter-spacing="4" text-anchor="middle" dominant-baseline="hanging"><textPath href="#{pid}b" startOffset="50%" side="right">{pm["bottom"]}</textPath></text>
 <text fill="{color}" stroke="none" x="-64" y="7" font-family="Special Elite" font-size="15">★</text><text fill="{color}" stroke="none" x="52" y="7" font-family="Special Elite" font-size="15">★</text>
 {wave}
</g></svg>'''
    return _wrap(svg, x, y, size, size, rot, z, "", "pointer-events:none")


def brush(x, y, w, h=46, color="#b3342c", rot=-2, z=12, seed=2):
    """红色毛笔下划线（代码画的，带干笔飞白）"""
    rng = random.Random(seed)
    pid = _rid("brush", x, y, seed)
    top, bot = [], []
    n = 40
    for i in range(n + 1):
        t = i / n
        px = t * 1000
        thick = 22 * (math.sin(math.pi * min(1, t * 1.15)) ** 0.5) + 4
        cy = 30 + math.sin(t * 2.6) * 6
        top.append((px, cy - thick / 2 + rng.uniform(-1.5, 1.5)))
        bot.append((px, cy + thick / 2 + rng.uniform(-1.5, 1.5)))
    d = "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in top + bot[::-1]) + "Z"
    svg = f'''<svg viewBox="0 0 1000 60" preserveAspectRatio="none" width="{w}" height="{h}" style="display:block;overflow:visible">
<defs><filter id="{pid}"><feTurbulence type="fractalNoise" baseFrequency="0.035 0.9" numOctaves="2" seed="{seed}" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -2.2 1.75" result="a"/>
<feComposite in="SourceGraphic" in2="a" operator="in"/></filter></defs>
<path d="{d}" fill="{color}" filter="url(#{pid})" opacity=".9"/></svg>'''
    return _wrap(svg, x, y, w, h, rot, z, "mult")


def paperclip(x, y, h=150, rot=8, z=40, color="#9aa3ab"):
    svg = f'''<svg viewBox="0 0 40 120" width="{h/3:.0f}" height="{h}" style="display:block;overflow:visible">
<path d="M28 34 V96 a10 10 0 0 1 -20 0 V20 a13 13 0 0 1 26 0 V92 a6 6 0 0 1 -12 0 V34" fill="none" stroke="{color}" stroke-width="4.2" stroke-linecap="round"/>
<path d="M28 34 V96 a10 10 0 0 1 -20 0 V20 a13 13 0 0 1 26 0 V92" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.2" transform="translate(-1 -1)"/></svg>'''
    return _wrap(svg, x, y, h / 3, h, rot, z, "sh-soft")


WASHI = {
    "dots": "radial-gradient(circle at 6px 6px, rgba(255,255,255,.75) 2.4px, transparent 3px) 0 0/14px 14px",
    "stripe": "repeating-linear-gradient(90deg, rgba(255,255,255,.45) 0 6px, transparent 6px 14px)",
    "grid": "linear-gradient(rgba(255,255,255,.4) 1px, transparent 1px) 0 0/10px 10px, linear-gradient(90deg, rgba(255,255,255,.4) 1px, transparent 1px) 0 0/10px 10px",
    "plain": "none",
}


def washi(x, y, w, h=42, rot=-8, color="#e9b7bf", pattern="dots", z=45, seed=1):
    """和纸胶带（两端锯齿撕口）"""
    rng = random.Random(seed)
    pts = []
    k = 7
    for i in range(k + 1):
        pts.append((rng.uniform(0, 1.8), i / k * 100))
    left = ", ".join(f"{a:.1f}% {b:.1f}%" for a, b in pts)
    right = ", ".join(f"{100 - rng.uniform(0, 1.8):.1f}% {100 - i / k * 100:.1f}%" for i in range(k + 1))
    bg = WASHI.get(pattern, "none")
    style = (f"background:{bg}, {color};clip-path:polygon({left}, {right});")
    return f'<div class="washi" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z};{style}"></div>'


def barcode(text, w=150, h=46, color="#3a332b"):
    rng = random.Random(text)
    x, bars = 0, []
    while x < w:
        bw = rng.choice([1, 1, 2, 2, 3, 4])
        if rng.random() > 0.38:
            bars.append(f'<rect x="{x}" y="0" width="{bw}" height="{h}"/>')
        x += bw + rng.choice([1, 2, 2, 3])
    return f'<svg width="{w}" height="{h}" fill="{color}">{"".join(bars)}</svg>'


def ticket(place, x, y, w=520, h=190, rot=-4, z=26, paper="#f3e7cf", accent="#b3342c"):
    """车票/船票票根（文字来自 config.json → ticket）"""
    t = CFG["place"][place]["ticket"]
    notch = (f"-webkit-mask: radial-gradient(circle 13px at 74% 0, transparent 12px, #000 13px) top/100% 51% no-repeat,"
             f"radial-gradient(circle 13px at 74% 100%, transparent 12px, #000 13px) bottom/100% 51% no-repeat;")
    inner = f'''<div class="main"><div class="lbl" style="color:{accent}">{t["kind"]}</div>
<div class="route">{t["from"]} <span style="color:{accent}">→</span> {t["to"]}</div>
<div class="row"><div>CLASS<b>{t["class"]}</b></div><div>SEAT<b>{t["seat"]}</b></div><div>YEAR<b>{CFG["year"]}</b></div></div></div>
<div class="stub"><div class="lbl">No.</div><div style="font-size:16px;letter-spacing:.04em">{t["code"]}</div><div class="bar">{barcode(t["code"], int(w*0.2), 40)}</div></div>'''
    return (f'<div class="ticket sh" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z};'
            f'background:{paper};{notch}">{inner}</div>')


def vlabel(place, x, y, size=64, rot=0, z=28, color="#b3342c", flower=None):
    """竖排本地地名标签（config.json → label / label_sub）"""
    p = CFG["place"][place]
    fl = ""
    if flower:
        fl = _wrap(f'<img src="../art/{flower}.webp">', -30, -40, 110, None, -12, 2, "")
    return (f'<div class="vlabel sh-soft" style="left:{x}px;top:{y}px;font-size:{size}px;background:{color};transform:rotate({rot}deg);z-index:{z};'
            f'clip-path:polygon(0 0,100% 0,100% 100%,50% 94%,0 100%)">{p["label"]}<span class="sub">{p["label_sub"]}</span></div>')


def text(html, x, y, w=None, cls="hand", size=34, rot=0, z=35, color=None, align="left", style=""):
    ww = f"width:{w}px;" if w else ""
    col = f"color:{color};" if color else ""
    return (f'<div class="L {cls}" style="left:{x}px;top:{y}px;{ww}font-size:{size}px;transform:rotate({rot}deg);'
            f'z-index:{z};text-align:{align};{col}{style}">{html}</div>')


def header(side, folio, label="TRAVEL JOURNAL"):
    """左页：顶部 TRAVEL JOURNAL 页眉 + 页码；右页只有页码。"""
    head = (f'<div class="jhead"><span>{label}</span><span class="rule"></span><span>{CFG["year"]}</span></div>'
            if side == "left" else "")
    return head + f'<div class="folio">— {folio} —</div>'


def ink(x, y, w, h, svg_inner, z=4, rot=0, color="#3b4a66", sw=2.2, opacity=.75):
    """手绘线稿（简单的钢笔线条，用于小装饰：飞鸟、波浪、虚线路线）"""
    svg = (f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="display:block;overflow:visible">'
           f'<g fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}">{svg_inner}</g></svg>')
    return _wrap(svg, x, y, w, h, rot, z, "")


def birds(n=3, seed=1, s=1.0):
    rng = random.Random(seed)
    out = ""
    for i in range(n):
        x, y, k = 20 + i * 46 * s + rng.uniform(-10, 10), 20 + rng.uniform(-14, 14), s * rng.uniform(.7, 1.2)
        out += f'<path d="M{x-14*k:.0f} {y:.0f} q {7*k:.0f} {-8*k:.0f} {14*k:.0f} 0 q {7*k:.0f} {-8*k:.0f} {14*k:.0f} 0"/>'
    return out


def paper_bg(name, base=(244, 237, 222), grid=None, seed=3):
    """页面底纸（生成一次后缓存在 cache/）。按 SCALE 输出，避免底纸被放大。"""
    path = F.CACHE / f"paper_{name}_x{SCALE}.jpg"
    if not path.exists():
        F.page_paper(path, w=1200 * SCALE, h=1600 * SCALE, base=base, grid=grid, seed=seed)
    return f"../cache/{path.name}"


def page(side, bg, layers):
    return (f'<section class="page {side}" style="background-image:url({bg})">' + "".join(layers) + "</section>")
