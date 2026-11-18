"""每一页的拼贴图层 —— 在这里调整位置 / 大小 / 角度 / 裁切。
Each spread = one function returning (left_page_html, right_page_html).
单页 1200 x 1600 像素，(0,0) 在左上角。每一行 R.append(...) / L.append(...) 就是一个图层。

常用写法（照片 key 见 config.json → photos）：
  K.polaroid("japan_me", [0,0.05,1,0.85], x, y, w, h, rot, caption=...)   拍立得
  K.torn("japan_lake", [左,上,右,下], x, y, w, h, rot, seed=..)          撕边照片碎片
  K.mini("japan_tower", box, x, y, w, h, rot)                            小相片
  K.scrap("kraft", x, y, w, h, rot)        纸片: kraft grid lined cream blue pink sage sand ink
  K.art("japan_landscape", x, y, w, rot)   水彩插画（art/ 文件夹）
  K.sticker("japan_mascot", x, y, w, rot)  贴纸
  K.stamp / K.postmark / K.ticket / K.vlabel / K.washi / K.paperclip / K.brush / K.text
裁切 box 用比例：[0,0,1,1] = 整张照片；[0,0,1,0.5] = 上半张。
z = 叠放顺序（大的在上面）。seed = 撕边形状的随机种子，换个数字就换一种撕法。
"""
import kit as K


def P(pid):
    return K.CFG["place"][pid]


# ------------------------------------------------------------------ shared opener (left page)
def opener_left(pid, folio, bg, title_size=230, ink="#24252d", brush_col="#b3342c",
                branch=None, stamp_at=(840, 330, 250, 7), pm_at=(630, 470, 220, -12), pm_col="#7a2e2a",
                land_y=820, land_x=-40, land_w=1280, notes_y=None, extra=()):
    p = P(pid)
    lines = p["title"].split(" ")
    L = [K.header("left", folio)]
    L.append(K.text(f'No. {p["no"]} &nbsp;·&nbsp; {p["region"]}', 96, 190, cls="kicker", size=21, z=36))
    L.append(K.text("<br>".join(lines), 86, 238, cls="title", size=title_size, color=ink, z=36))
    last = lines[-1]
    ty = 238 + title_size * 0.9 * (len(lines) - 1)
    bw = min(660, 120 + max(len(last), 4) * title_size * 0.64)
    L.append(K.brush(92, ty + title_size * 0.93, bw, 44, brush_col, -1.5))
    L.append(K.text(p["hand"], 112, ty + title_size * 1.14, cls="hand", size=33, rot=-2, z=36))
    ny = notes_y or ty + title_size * 1.14 + 92
    L.append(K.text(p["coords"], 112, ny, cls="type", size=21, z=36))
    L.append(K.text("· " + "<br>· ".join(p["notes"]), 112, ny + 44, cls="type", size=19, z=36,
                    style="line-height:1.75;opacity:.85"))
    if branch:
        L.append(branch)
    sx, sy, sw, sr = stamp_at
    L.append(K.stamp(pid, sx, sy, sw, sr))
    px, py, ps, pr = pm_at
    L.append(K.postmark(pid, px, py, ps, pr, color=pm_col))
    L.append(K.art(f"{pid}_landscape", land_x, land_y, land_w, 0, 3))
    L.extend(extra)
    return K.page("left", bg, L)


# ================================================================== COVER
def cover():
    c = K.CFG["cover"]
    bg = K.paper_bg("cover", (238, 228, 208), None, 1)
    # back cover (left)
    L = [K.scrap("kraft", 160, 260, 880, 1080, -1.5, z=2, seed=91)]
    L.append(K.text("THE PLACES", 260, 360, cls="kicker", size=24, z=30))
    rows = ""
    for pid in ["japan", "semporna", "bali", "dali", "shenzhenbay", "jeju"]:
        p = P(pid)
        rows += (f'<div style="display:flex;gap:24px;align-items:baseline;margin:0 0 30px">'
                 f'<span style="font:400 20px var(--font-type);opacity:.7">{p["no"]}</span>'
                 f'<span style="font:500 54px var(--font-display);letter-spacing:.04em">{p["title"].title()}</span>'
                 f'<span class="cjk" style="font-size:26px;opacity:.7">{p["label"]}</span></div>')
    L.append(K.text(rows, 260, 430, 700, cls="", size=20, z=30, color="#2b2a2f"))
    L.append(K.postmark("japan", 640, 1130, 210, -14, color="#7a2e2a"))
    L.append(K.text(K.CFG["title"] + " · " + K.CFG["year"], 260, 1240, cls="type", size=20, z=30))
    L.append(K.art("jeju_branch", 760, -60, 520, 20, 20))
    L.append(K.art("dali_branch", -80, 1250, 460, 160, 20))
    left = K.page("left", bg, L)

    bgf = K.paper_bg("cover_front", (240, 232, 214), "grid", 4)
    R = []
    R.append(K.text(c["kicker"], 110, 150, cls="kicker", size=22, z=30))
    R.append(K.text(c["line1"] + "<br>" + c["line2"], 100, 200, cls="title", size=168, z=30))
    R.append(K.brush(110, 520, 560, 44, "#b3342c", -1.5))
    R.append(K.text(c["hand"], 140, 575, cls="hand", size=36, rot=-2, z=30))
    # 封面拼贴：三张他的照片 + 邮票 + 邮戳
    R.append(K.scrap("kraft", 90, 700, 1000, 640, -2, z=2, seed=92))
    R.append(K.polaroid("japan_me", [0.0, 0.05, 1.0, 0.80], 130, 720, 400, 520, -8, z=10, caption="Japan", cap_size=28, bottom=100, seed=3))
    R.append(K.polaroid("bali_cliff", [0.0, 0.0, 1.0, 0.75], 420, 690, 400, 520, 3, z=11, caption="Bali", cap_size=28, bottom=100, seed=4))
    R.append(K.torn("dali_peak", [0.0, 0.1, 1.0, 0.75], 760, 760, 320, 440, 7, z=9, seed=95, fringe=14))
    R.append(K.paperclip(600, 650, 150, 6, z=40))
    R.append(K.washi(110, 740, 180, 44, -35, "#e7b3bc", "dots", z=41, seed=9))
    R.append(K.washi(900, 740, 170, 40, 30, "#cfe0e6", "stripe", z=41, seed=10))
    R.append(K.stamp("japan", 860, 470, 200, 10, z=22))
    R.append(K.stamp("jeju", 90, 1180, 190, -9, z=22))
    R.append(K.stamp("semporna", 300, 1230, 180, 5, z=23))
    R.append(K.postmark("bali", 470, 1220, 200, -14, color="#7a2e2a"))
    R.append(K.sticker("japan_mascot", 1000, 1010, 160, 10))
    R.append(K.ticket("dali", 600, 1300, 480, 170, -4, z=26, accent="#2c4a7e"))
    R.append(K.text(c["places_line"], 0, 1515, 1200, cls="type", size=20, z=30, align="center"))
    R.append(K.art("japan_branch", 760, -80, 560, 8, 31, flip=True))
    return left, K.page("right", bgf, R)


# ================================================================== CONTENTS
def contents():
    ct = K.CFG["contents"]
    bg = K.paper_bg("contents", (245, 239, 226), "grid", 2)
    L = [K.header("left", "02")]
    L.append(K.text(ct["title"], 92, 170, cls="title", size=150, z=30))
    L.append(K.brush(96, 330, 460, 40, "#b3342c", -1))
    L.append(K.text(ct["hand"], 110, 380, cls="hand", size=30, rot=-2, z=30))
    folios = {"japan": "04", "semporna": "08", "bali": "12", "dali": "16", "shenzhenbay": "20", "jeju": "24"}
    y = 500
    for pid in ["japan", "semporna", "bali", "dali", "shenzhenbay", "jeju"]:
        p = P(pid)
        L.append(K.text(f'<span style="font:400 20px var(--font-type);opacity:.6">{p["no"]}</span>&nbsp;&nbsp;'
                        f'<span style="font:500 50px var(--font-display);letter-spacing:.05em">{p["title"].title()}</span>'
                        f'&nbsp;&nbsp;<span class="cjk" style="font-size:24px;opacity:.65">{p["label"]}</span>',
                        110, y, 760, cls="", size=20, z=30))
        L.append(K.text(f'{p["coords"]} &nbsp;····· p.{folios[pid]}', 150, y + 66, cls="type", size=17, z=30, style="opacity:.75"))
        y += 150
    L.append(K.art("japan_branch", 640, -60, 600, 6, 20, flip=True))
    L.append(K.ink(760, 470, 380, 900,
                   '<path d="M40 40 C 200 120, 120 260, 260 330 S 140 520, 300 600 S 120 760, 250 860" stroke-dasharray="2 12"/>',
                   z=6, color="#b3342c", sw=3))
    left = K.page("left", bg, L)

    bg_r = K.paper_bg("contents_r", (246, 240, 229), None, 3)
    R = [K.header("right", "03")]
    R.append(K.scrap("kraft", 150, 160, 900, 620, -2, z=2, seed=93))
    tiles = [("japan_me", [0, 0.05, 1, 0.7]), ("semporna_jetty", [0.1, 0, 0.9, 1]), ("bali_cliff", [0, 0.05, 1, 0.75]),
             ("dali_peak", [0, 0.15, 1, 0.65]), ("sz_gold", [0.1, 0, 0.9, 1]), ("jeju_rocks", [0, 0.1, 1, 0.8])]
    for i, (k, b) in enumerate(tiles):
        cx, cy = 210 + (i % 3) * 270, 220 + (i // 3) * 270
        R.append(K.mini(k, b, cx, cy, 240, 240, [-5, 3, -2, 4, -4, 6][i], z=10 + i, seed=60 + i))
    R.append(K.washi(180, 190, 170, 40, -25, "#cfe0e6", "stripe", z=40, seed=11))
    R.append(K.washi(830, 720, 170, 40, 20, "#e7b3bc", "dots", z=40, seed=12))
    R.append(K.text(ct["intro"], 180, 860, 840, cls="note", size=46, rot=-1.5, z=30))
    R.append(K.ticket("jeju", 160, 1030, 560, 190, -5, z=24))
    R.append(K.ticket("japan", 470, 1230, 560, 190, 4, z=25))
    R.append(K.sticker("semporna_mascot", 900, 980, 220, 12))
    R.append(K.art("semporna_branch", -60, 1300, 380, 0, 8))
    return left, K.page("right", bg_r, R)


# ================================================================== JAPAN
def japan_a():
    pid = "japan"; p = P(pid)
    bg_l = K.paper_bg("grid_warm", (245, 238, 224), "grid", 11)
    left = opener_left(pid, "04", bg_l, branch=K.art("japan_branch", 520, -70, 760, 4, 30, flip=True),
                       extra=[K.ink(860, 700, 200, 60, K.birds(3, 2), z=4)])
    bg_r = K.paper_bg("cream_r1", (246, 240, 228), None, 12)
    R = [K.header("right", "05")]
    R.append(K.torn("japan_lake", [0.05, 0.0, 0.75, 0.42], 150, 140, 720, 470, -6, z=2, seed=21, fringe=12, fx="faded"))
    R.append(K.scrap("kraft", 640, 120, 420, 330, 9, z=3, seed=4))
    R.append(K.scrap("grid", 70, 640, 360, 470, -7, z=3, seed=5))
    R.append(K.scrap("pink", 760, 980, 360, 260, 6, z=3, seed=6))
    R.append(K.polaroid("japan_me", [0.0, 0.04, 1.0, 0.86], 300, 250, 600, 800, 3.5, z=12, caption=p["cap_a"], cap_size=34))
    R.append(K.paperclip(560, 190, 160, 6, z=40))
    R.append(K.washi(250, 300, 210, 46, -38, "#e7b3bc", "dots", z=41, seed=2))
    R.append(K.torn("japan_lake", [0.30, 0.10, 0.80, 0.55], 50, 1040, 420, 320, -7, z=16, seed=22, fringe=14))
    R.append(K.washi(90, 1025, 150, 40, 12, "#cfe0e6", "stripe", z=42, seed=3))
    R.append(K.vlabel(pid, 1010, 170, 62, 2, z=30, color="#b3342c"))
    R.append(K.art("japan_branch", 860, 60, 300, 20, 31))
    R.append(K.art("japan_landmark", 820, 1040, 360, 4, 9))
    R.append(K.ticket(pid, 520, 1310, 560, 190, -4, z=26))
    R.append(K.sticker("japan_mascot", 410, 1150, 170, -8))
    R.append(K.text(p["notes"][0], 470, 1105, cls="note", size=36, rot=-3, z=36))
    return left, K.page("right", bg_r, R)


def japan_b():
    pid = "japan"; p = P(pid)
    bg_l = K.paper_bg("lined_l2", (243, 236, 221), "lines", 13)
    L = [K.header("left", "06")]
    L.append(K.torn("japan_lake", [0.0, 0.0, 1.0, 0.92], 50, 150, 1100, 680, -1.5, z=5, seed=31, sides="tb", fringe=14, amp=10))
    L.append(K.torn("japan_lake", [0.40, 0.18, 0.72, 0.46], 660, 640, 430, 300, 5, z=8, seed=32, fringe=12))
    L.append(K.washi(860, 620, 180, 42, 18, "#e7b3bc", "dots", z=40, seed=4))
    L.append(K.text(p["cap_b"], 700, 950, cls="hand", size=30, rot=3, z=36))
    L.append(K.scrap("cream", 90, 900, 560, 470, -2.5, z=6, seed=33))
    L.append(K.text("FIG. 01 — LAKESHORE", 140, 950, cls="type", size=20, rot=-2.5, z=36))
    L.append(K.text(p["journal"], 140, 1000, 460, cls="note", size=40, rot=-2.5, z=36))
    L.append(K.text("· " + "<br>· ".join(p["notes"]), 140, 1200, 460, cls="type", size=20, rot=-2.5, z=36, style="line-height:1.7"))
    L.append(K.postmark(pid, 690, 1120, 200, 14, color="#2f4f74", lines=False))
    L.append(K.art("japan_branch", -120, 1250, 520, -160, 4))
    L.append(K.mini("japan_me", [0.25, 0.30, 0.75, 0.62], 900, 1180, 200, 230, 8, z=12, seed=34))
    L.append(K.washi(920, 1160, 140, 36, -6, "#d9c9a3", "grid", z=41, seed=5))
    L.append(K.text("me, very cold", 880, 1440, cls="hand", size=24, rot=6, z=36))
    left = K.page("left", bg_l, L)

    bg_r = K.paper_bg("ink_r2", (236, 230, 220), "dots", 14)
    R = [K.header("right", "07")]
    R.append(K.scrap("ink", 300, 110, 700, 1060, 2, z=2, seed=41, color="#2c3446"))
    R.append(K.torn("japan_tower", [0.0, 0.0, 1.0, 0.92], 360, 160, 600, 870, -2, z=6, seed=42, fringe=16))
    R.append(K.text(p["cap_c"], 420, 1050, cls="hand", size=34, rot=-3, z=36, color="#f3ead8"))
    for i, (b, yy, s, r) in enumerate([([0.30, 0.05, 0.70, 0.35], 220, 200, -6), ([0.25, 0.30, 0.75, 0.62], 470, 170, 4), ([0.10, 0.62, 0.90, 0.98], 690, 190, -3)]):
        R.append(K.mini("japan_tower", b, 90 + i * 14, yy, s, int(s * 1.15), r, z=14, seed=43 + i))
    R.append(K.washi(110, 200, 140, 38, -20, "#e3c27a", "stripe", z=41, seed=6))
    R.append(K.art("japan_landmark", 20, 930, 430, -3, 9))
    R.append(K.postmark(pid, 640, 1230, 210, -20))
    R.append(K.art("japan_branch", 700, -40, 520, 12, 30, flip=True))
    R.append(K.sticker("japan_mascot", 960, 1150, 160, 8))
    R.append(K.text("FIG. 02 — THE TOWER AT NIGHT", 480, 1470, cls="type", size=19, rot=-1, z=36))
    return left, K.page("right", bg_r, R)


# ================================================================== SEMPORNA
def semporna_a():
    pid = "semporna"; p = P(pid)
    bg_l = K.paper_bg("aqua_grid", (236, 242, 237), "grid", 21)
    left = opener_left(pid, "08", bg_l, title_size=140, brush_col="#cf6a62", ink="#1f3d45",
                       branch=K.art("semporna_branch", 840, -100, 380, 8, 30),
                       stamp_at=(860, 420, 240, -6), pm_at=(640, 560, 210, 10), pm_col="#25677a", land_y=860)
    bg_r = K.paper_bg("aqua_r", (240, 243, 236), "dots", 22)
    R = [K.header("right", "09")]
    R.append(K.scrap("blue", 120, 120, 820, 520, 4, z=2, seed=23, color="#a9d3d2"))
    R.append(K.torn("semporna_jetty", [0.0, 0.0, 0.5, 0.55], 640, 100, 460, 380, 7, z=4, seed=24, fringe=12, fx="faded"))
    R.append(K.scrap("sand", 60, 760, 420, 520, -6, z=3, seed=25))
    R.append(K.polaroid("semporna_me", [0.0, 0.05, 1.0, 0.80], 300, 230, 600, 800, -3, z=12, caption=p["cap_a"]))
    R.append(K.paperclip(540, 170, 160, -6, z=40))
    R.append(K.washi(760, 240, 200, 46, 36, "#f2b8a8", "stripe", z=41, seed=7))
    R.append(K.torn("semporna_jetty", [0.30, 0.25, 0.80, 0.95], 60, 1030, 470, 320, 5, z=16, seed=26, fringe=14))
    R.append(K.vlabel(pid, 1030, 600, 52, -2, z=30, color="#2f8c8a"))
    R.append(K.art("semporna_landmark", 800, 1000, 380, -3, 9))
    R.append(K.ticket(pid, 440, 1320, 640, 190, 3, z=26, accent="#2f8c8a"))
    R.append(K.sticker("semporna_mascot", 70, 820, 230, -10))
    R.append(K.text(p["notes"][1], 560, 1090, cls="note", size=36, rot=-3, z=36))
    return left, K.page("right", bg_r, R)


def semporna_b():
    pid = "semporna"; p = P(pid)
    bg_l = K.paper_bg("sand_l", (245, 238, 222), None, 27)
    L = [K.header("left", "10")]
    L.append(K.scrap("blue", 40, 160, 1120, 760, -1, z=2, seed=28, color="#bfe0dc", sides="tb"))
    L.append(K.torn("semporna_jetty", [0.0, 0.0, 1.0, 1.0], 80, 200, 1040, 600, 1.5, z=5, seed=29, fringe=16, amp=9))
    L.append(K.torn("semporna_jetty", [0.62, 0.0, 1.0, 0.6], 820, 660, 330, 290, -6, z=8, seed=30, fringe=12))
    L.append(K.text(p["cap_b"], 110, 840, cls="hand", size=32, rot=-2, z=36))
    L.append(K.scrap("lined", 110, 960, 600, 440, 2, z=6, seed=31))
    L.append(K.text("LOG — DAY 2", 170, 1010, cls="type", size=20, rot=2, z=36))
    L.append(K.text(p["journal"], 170, 1060, 500, cls="note", size=42, rot=2, z=36))
    L.append(K.text("· " + "<br>· ".join(p["notes"]), 170, 1240, 500, cls="type", size=19, rot=2, z=36, style="line-height:1.7"))
    L.append(K.art("semporna_branch", 720, 1050, 480, -6, 5))
    L.append(K.postmark(pid, 760, 1390, 160, -8, color="#25677a", lines=False))
    L.append(K.ink(900, 980, 220, 60, K.birds(3, 5), z=4, color="#25677a"))
    left = K.page("left", bg_l, L)

    bg_r = K.paper_bg("aqua_r2", (238, 243, 239), "grid", 32)
    R = [K.header("right", "11")]
    R.append(K.art("semporna_landmark", 520, 120, 620, 3, 3))
    R.append(K.scrap("pink", 80, 160, 460, 560, -5, z=4, seed=33))
    R.append(K.torn("semporna_me", [0.05, 0.05, 0.95, 0.60], 110, 200, 400, 470, -3, z=8, seed=34, fringe=14))
    R.append(K.washi(140, 180, 160, 40, -18, "#f2b8a8", "dots", z=41, seed=8))
    for i, (b, x, y, r) in enumerate([([0.05, 0.3, 0.45, 0.9], 120, 820, -4), ([0.45, 0.2, 0.85, 0.8], 380, 860, 5), ([0.0, 0.0, 0.4, 0.5], 640, 800, -2)]):
        R.append(K.mini("semporna_jetty", b, x, y, 240, 240, r, z=10 + i, seed=35 + i))
    R.append(K.text(p["cap_c"], 140, 1110, cls="hand", size=30, rot=-2, z=36))
    R.append(K.stamp(pid, 880, 820, 220, 8, z=22))
    R.append(K.sticker("semporna_mascot", 150, 1230, 260, -6))
    R.append(K.postmark(pid, 620, 1200, 200, 10, color="#25677a"))
    R.append(K.text("FIG. 03 — STILT VILLAGE", 640, 1500, cls="type", size=19, rot=-1, z=36))
    return left, K.page("right", bg_r, R)


# ================================================================== BALI
def bali_a():
    pid = "bali"; p = P(pid)
    bg_l = K.paper_bg("sand_dots", (247, 236, 216), "dots", 41)
    left = opener_left(pid, "12", bg_l, title_size=250, brush_col="#d9782f", ink="#3a2a22",
                       branch=K.art("bali_branch", 560, -30, 640, 10, 30, flip=True),
                       stamp_at=(830, 390, 250, -5), pm_at=(600, 520, 220, 12), pm_col="#9a4a22", land_y=840)
    bg_r = K.paper_bg("sand_r", (246, 238, 222), None, 42)
    R = [K.header("right", "13")]
    R.append(K.torn("bali_beach", [0.0, 0.0, 1.0, 0.35], 120, 120, 640, 440, -5, z=2, seed=43, fringe=12, fx="faded"))
    R.append(K.scrap("kraft", 680, 160, 420, 360, 7, z=3, seed=44))
    R.append(K.scrap("sage", 60, 700, 380, 520, 5, z=3, seed=45))
    R.append(K.polaroid("bali_cliff", [0.0, 0.0, 1.0, 0.78], 330, 220, 600, 820, 2.5, z=12, caption=p["cap_a"]))
    R.append(K.paperclip(600, 160, 160, 10, z=40))
    R.append(K.washi(800, 260, 210, 46, 40, "#f0c27a", "stripe", z=41, seed=10))
    R.append(K.torn("bali_beach", [0.0, 0.38, 1.0, 0.70], 60, 1030, 400, 360, -6, z=16, seed=46, fringe=14))
    R.append(K.vlabel(pid, 1040, 640, 50, 2, z=30, color="#c4622d"))
    R.append(K.art("bali_landmark", 800, 1010, 380, 3, 9))
    R.append(K.ticket(pid, 460, 1320, 620, 190, -3, z=26, accent="#c4622d"))
    R.append(K.sticker("bali_mascot", 90, 760, 230, -8))
    R.append(K.text(p["notes"][2], 520, 1100, cls="note", size=36, rot=-3, z=36))
    return left, K.page("right", bg_r, R)


def bali_b():
    pid = "bali"; p = P(pid)
    bg_l = K.paper_bg("peach_l", (248, 236, 220), "lines", 47)
    L = [K.header("left", "14")]
    L.append(K.scrap("sand", 80, 150, 620, 1220, -2, z=2, seed=48))
    L.append(K.torn("bali_beach", [0.0, 0.0, 1.0, 1.0], 130, 190, 520, 1000, -1, z=6, seed=49, fringe=16))
    L.append(K.text(p["cap_c"], 170, 1210, cls="hand", size=32, rot=-2, z=36))
    for i, (b, y, r) in enumerate([([0.1, 0.25, 0.9, 0.48], 220, 5), ([0.0, 0.55, 0.8, 0.8], 520, -4), ([0.2, 0.0, 1.0, 0.2], 820, 6)]):
        R_ = K.mini("bali_beach", b, 760, y, 300, 240, r, z=10 + i, seed=50 + i)
        L.append(R_)
    L.append(K.washi(790, 200, 150, 38, -14, "#f0c27a", "dots", z=41, seed=11))
    L.append(K.text(p["journal"], 720, 1100, 400, cls="note", size=38, rot=3, z=36))
    L.append(K.art("bali_branch", 640, 1300, 560, 0, 5))
    L.append(K.postmark(pid, 90, 1360, 170, -10, color="#9a4a22", lines=False))
    left = K.page("left", bg_l, L)

    bg_r = K.paper_bg("sand_r2", (246, 237, 220), "grid", 53)
    R = [K.header("right", "15")]
    R.append(K.art("bali_landscape", -60, 60, 1300, 0, 2, opacity=.95))
    R.append(K.torn("bali_cliff", [0.0, 0.0, 1.0, 1.0], 160, 520, 540, 720, 3, z=8, seed=54, fringe=16))
    R.append(K.torn("bali_cliff", [0.15, 0.05, 0.85, 0.45], 640, 760, 400, 300, -6, z=10, seed=55, fringe=12))
    R.append(K.washi(180, 500, 180, 42, -10, "#cfe0e6", "stripe", z=41, seed=12))
    R.append(K.text(p["cap_b"], 650, 1080, cls="hand", size=30, rot=-4, z=36))
    R.append(K.stamp(pid, 880, 1180, 210, 9, z=22))
    R.append(K.sticker("bali_mascot", 80, 1250, 200, -6))
    R.append(K.text("FIG. 04 — KELINGKING, NUSA PENIDA", 330, 1300, cls="type", size=19, rot=-1, z=36))
    R.append(K.text("· " + "<br>· ".join(p["notes"]), 330, 1350, cls="type", size=19, z=36, style="line-height:1.7"))
    return left, K.page("right", bg_r, R)


# ================================================================== DALI  (more white space)
def dali_a():
    pid = "dali"; p = P(pid)
    bg_l = K.paper_bg("dali_l", (247, 246, 241), None, 61)
    left = opener_left(pid, "16", bg_l, title_size=250, brush_col="#2f4f88", ink="#1f2a44",
                       branch=K.art("dali_branch", 700, 40, 460, 14, 30),
                       stamp_at=(820, 520, 240, 5), pm_at=(600, 620, 210, -10), pm_col="#2f4f88",
                       land_y=930)
    bg_r = K.paper_bg("dali_r", (246, 245, 240), "dots", 62)
    R = [K.header("right", "17")]
    R.append(K.scrap("blue", 220, 130, 760, 300, -3, z=2, seed=63, color="#c9d5e6"))
    R.append(K.polaroid("dali_peak", [0.0, 0.0, 1.0, 0.70], 320, 200, 560, 760, -2, z=12, caption=p["cap_b"], cap_size=30))
    R.append(K.paperclip(580, 140, 150, -4, z=40))
    R.append(K.torn("dali_peak", [0.2, 0.25, 0.8, 0.45], 100, 880, 380, 220, -5, z=14, seed=64, fringe=12))
    R.append(K.vlabel(pid, 100, 230, 66, -2, z=30, color="#2c4a7e"))
    R.append(K.art("dali_landmark", 760, 920, 380, 0, 8))
    R.append(K.ticket(pid, 300, 1290, 560, 190, -2, z=26, accent="#2c4a7e"))
    R.append(K.sticker("dali_mascot", 80, 1130, 220, -6))
    R.append(K.text(p["notes"][2], 560, 1070, cls="note", size=34, rot=-2, z=36))
    return left, K.page("right", bg_r, R)


def dali_b():
    pid = "dali"; p = P(pid)
    bg_l = K.paper_bg("dali_l2", (247, 246, 241), "grid", 65)
    L = [K.header("left", "18")]
    L.append(K.polaroid("dali_lamb", [0.0, 0.0, 1.0, 1.0], 120, 220, 960, 760, -1.5, z=10, caption=p["cap_a"], cap_size=34, bottom=130))
    L.append(K.washi(100, 210, 200, 44, -30, "#9fb3d6", "dots", z=41, seed=13))
    L.append(K.washi(920, 200, 200, 44, 28, "#9fb3d6", "dots", z=41, seed=14))
    L.append(K.mini("dali_lamb", [0.35, 0.35, 0.65, 0.85], 860, 920, 220, 260, 7, z=14, seed=66))
    L.append(K.text(p["journal"], 140, 1110, 620, cls="note", size=44, rot=-1, z=36))
    L.append(K.art("dali_branch", -80, 1250, 460, -8, 5))
    L.append(K.postmark(pid, 660, 1300, 190, 8, color="#2f4f88"))
    left = K.page("left", bg_l, L)

    bg_r = K.paper_bg("dali_r2", (247, 246, 242), None, 67)
    R = [K.header("right", "19")]
    R.append(K.torn("dali_peak", [0.0, 0.0, 1.0, 1.0], 620, 140, 460, 690, 3, z=6, seed=68, fringe=16))
    R.append(K.torn("dali_lamb", [0.0, 0.62, 0.42, 1.0], 140, 200, 420, 300, -4, z=6, seed=69, fringe=12))
    R.append(K.text("cosmos, everywhere", 160, 540, cls="hand", size=30, rot=-3, z=36))
    R.append(K.art("dali_landmark", 120, 640, 440, -2, 4))
    R.append(K.text("· " + "<br>· ".join(p["notes"]), 640, 900, cls="type", size=19, z=36, style="line-height:1.75"))
    R.append(K.stamp(pid, 660, 1080, 220, -6, z=22))
    R.append(K.sticker("dali_mascot", 900, 1230, 200, 8))
    R.append(K.text("FIG. 05 — CANGSHAN · ERHAI", 140, 1460, cls="type", size=19, z=36))
    return left, K.page("right", bg_r, R)


# ================================================================== SHENZHEN BAY
def sz_a():
    pid = "shenzhenbay"; p = P(pid)
    bg_l = K.paper_bg("sz_l", (243, 236, 232), "lines", 71)
    left = opener_left(pid, "20", bg_l, title_size=150, brush_col="#c98a2b", ink="#2c2740",
                       branch=K.art("shenzhenbay_branch", 990, 470, 230, 0, 30),
                       stamp_at=(860, 560, 230, -6), pm_at=(640, 640, 200, 12), pm_col="#5b4a86", land_y=900)
    bg_r = K.paper_bg("sz_r", (242, 236, 234), "dots", 72)
    R = [K.header("right", "21")]
    # before / during / after: three torn strips stacked as a sky gradient
    R.append(K.torn("sz_clouds", [0.0, 0.0, 1.0, 0.65], 90, 110, 600, 300, -3, z=3, seed=73, fringe=10, fx="faded"))
    R.append(K.scrap("pink", 640, 140, 460, 300, 6, z=2, seed=74, color="#e8c9a8"))
    R.append(K.polaroid("sz_tripod", [0.05, 0.0, 0.95, 1.0], 280, 300, 700, 620, 3, z=12, caption=p["cap_a"], bottom=110))
    R.append(K.paperclip(600, 250, 150, 8, z=40))
    R.append(K.washi(240, 330, 200, 44, -32, "#c9b6e0", "stripe", z=41, seed=15))
    R.append(K.torn("sz_gold", [0.25, 0.1, 0.75, 0.7], 60, 900, 420, 300, -6, z=16, seed=75, fringe=14))
    R.append(K.vlabel(pid, 1040, 560, 48, 2, z=30, color="#6b5b95"))
    R.append(K.art("shenzhenbay_landmark", 800, 960, 360, 3, 9))
    R.append(K.ticket(pid, 420, 1320, 620, 190, -3, z=26, accent="#6b5b95"))
    R.append(K.sticker("shenzhenbay_mascot", 120, 1200, 210, -8))
    R.append(K.text(p["notes"][0] + " · " + p["notes"][1], 480, 1010, cls="note", size=32, rot=-3, z=36))
    return left, K.page("right", bg_r, R)


def sz_b():
    pid = "shenzhenbay"; p = P(pid)
    bg_l = K.paper_bg("sz_l2", (244, 238, 233), "grid", 76)
    L = [K.header("left", "22")]
    # the three moments of the evening as three wide torn strips
    strips = [("sz_tripod", [0.0, 0.15, 1.0, 0.85], "before", -2), ("sz_gold", [0.0, 0.0, 1.0, 0.75], "during", 1.5), ("sz_clouds", [0.0, 0.0, 1.0, 0.8], "after", -1)]
    for i, (k, b, lab, r) in enumerate(strips):
        y = 150 + i * 400
        L.append(K.torn(k, b, 70, y, 1060, 400, r, z=5 + i, seed=77 + i, sides="tb", fringe=12, amp=10))
        L.append(K.text(lab, 100 + i * 20, y + 330, cls="hand", size=34, rot=-3, z=36, color="#fbf4e6"))
    L.append(K.washi(930, 140, 190, 44, 22, "#e3c27a", "stripe", z=41, seed=16))
    L.append(K.text(p["journal"], 110, 1380, 760, cls="note", size=38, rot=-1, z=36))
    L.append(K.postmark(pid, 860, 1300, 190, -8, color="#5b4a86", lines=False))
    left = K.page("left", bg_l, L)

    bg_r = K.paper_bg("sz_r2", (243, 237, 233), None, 80)
    R = [K.header("right", "23")]
    R.append(K.art("shenzhenbay_landscape", -60, 80, 1300, 0, 2))
    R.append(K.polaroid("sz_gold", [0.1, 0.0, 0.9, 1.0], 120, 700, 520, 520, -4, z=10, caption=p["cap_b"], bottom=100, cap_size=28))
    R.append(K.polaroid("sz_clouds", [0.15, 0.0, 0.85, 1.0], 560, 760, 480, 480, 5, z=11, caption=p["cap_c"], bottom=96, cap_size=28))
    R.append(K.washi(300, 690, 160, 40, -6, "#c9b6e0", "dots", z=41, seed=17))
    R.append(K.washi(760, 745, 160, 40, 8, "#e3c27a", "stripe", z=41, seed=18))
    R.append(K.stamp(pid, 900, 1240, 200, 7, z=22))
    R.append(K.art("shenzhenbay_branch", -40, 1200, 420, 0, 6))
    R.append(K.sticker("shenzhenbay_mascot", 560, 1290, 180, 6))
    R.append(K.text("FIG. 06 — SHENZHEN BAY PARK", 380, 1500, cls="type", size=19, z=36))
    return left, K.page("right", bg_r, R)


# ================================================================== JEJU
def jeju_a():
    pid = "jeju"; p = P(pid)
    bg_l = K.paper_bg("jeju_l", (241, 239, 226), "grid", 81)
    left = opener_left(pid, "24", bg_l, title_size=250, brush_col="#e07b22", ink="#26282a",
                       branch=K.art("jeju_branch", 640, -60, 600, 10, 30),
                       stamp_at=(840, 440, 240, 6), pm_at=(620, 560, 210, -12), pm_col="#3b3b3f", land_y=900)
    bg_r = K.paper_bg("jeju_r", (242, 240, 229), None, 82)
    R = [K.header("right", "25")]
    R.append(K.torn("jeju_path", [0.0, 0.0, 0.6, 0.55], 120, 120, 640, 420, -5, z=2, seed=83, fringe=12, fx="faded"))
    R.append(K.scrap("kraft", 660, 120, 440, 360, 8, z=3, seed=84))
    R.append(K.scrap("sage", 60, 640, 380, 520, -6, z=3, seed=85))
    R.append(K.polaroid("jeju_rocks", [0.0, 0.0, 1.0, 0.85], 320, 220, 600, 820, 3, z=12, caption=p["cap_a"]))
    R.append(K.paperclip(580, 160, 160, 6, z=40))
    R.append(K.washi(780, 250, 200, 46, 40, "#f2b872", "dots", z=41, seed=19))
    R.append(K.torn("jeju_path", [0.35, 0.2, 0.95, 0.9], 50, 1040, 440, 320, -6, z=16, seed=86, fringe=14))
    R.append(K.vlabel(pid, 1040, 640, 50, 2, z=30, color="#3b3b3f"))
    R.append(K.art("jeju_landmark", 820, 1000, 360, 3, 9))
    R.append(K.ticket(pid, 480, 1320, 600, 190, -3, z=26, accent="#e07b22"))
    R.append(K.sticker("jeju_mascot", 80, 690, 190, -8))
    R.append(K.text(p["notes"][0], 540, 1100, cls="note", size=36, rot=-3, z=36))
    return left, K.page("right", bg_r, R)


def jeju_b():
    pid = "jeju"; p = P(pid)
    bg_l = K.paper_bg("jeju_l2", (242, 240, 228), "lines", 87)
    L = [K.header("left", "26")]
    L.append(K.torn("jeju_path", [0.0, 0.0, 1.0, 1.0], 60, 160, 1080, 720, -1, z=5, seed=88, sides="tb", fringe=14, amp=10))
    L.append(K.torn("jeju_path", [0.55, 0.3, 0.95, 0.85], 760, 760, 360, 300, 6, z=8, seed=89, fringe=12))
    L.append(K.text(p["cap_b"], 110, 900, cls="hand", size=32, rot=-2, z=36))
    L.append(K.scrap("cream", 100, 990, 560, 420, -2, z=6, seed=90))
    L.append(K.text("NOTE — THE ISLAND", 150, 1040, cls="type", size=20, rot=-2, z=36))
    L.append(K.text(p["journal"], 150, 1090, 470, cls="note", size=40, rot=-2, z=36))
    L.append(K.art("jeju_branch", 640, 1130, 520, -10, 5))
    L.append(K.postmark(pid, 760, 1400, 150, 10, color="#3b3b3f", lines=False))
    left = K.page("left", bg_l, L)

    bg_r = K.paper_bg("jeju_r2", (241, 239, 227), "dots", 91)
    R = [K.header("right", "27")]
    R.append(K.scrap("ink", 120, 120, 560, 840, -3, z=2, seed=92, color="#3a3b3f"))
    R.append(K.polaroid("jeju_wall", [0.0, 0.0, 1.0, 0.9], 170, 160, 480, 700, -1, z=10, caption=p["cap_c"], cap_size=36))
    R.append(K.paperclip(390, 110, 150, 4, z=40))
    R.append(K.torn("jeju_rocks", [0.0, 0.45, 1.0, 1.0], 700, 220, 400, 420, 5, z=8, seed=93, fringe=14))
    R.append(K.torn("jeju_rocks", [0.0, 0.0, 1.0, 0.4], 720, 640, 360, 260, -4, z=9, seed=94, fringe=12, fx="faded"))
    R.append(K.art("jeju_landmark", 80, 940, 380, -2, 7))
    R.append(K.stamp(pid, 880, 960, 220, 8, z=22))
    R.append(K.sticker("jeju_mascot", 500, 1090, 180, -6))
    R.append(K.art("jeju_landscape", 560, 1250, 620, 0, 5))
    R.append(K.text("· " + "<br>· ".join(p["notes"]), 470, 960, cls="type", size=19, z=36, style="line-height:1.7"))
    R.append(K.text("FIG. 07 — SEONGSAN · HALLASAN", 120, 1500, cls="type", size=19, z=36))
    return left, K.page("right", bg_r, R)


# ================================================================== CLOSING
def closing():
    cl = K.CFG["closing"]
    bg = K.paper_bg("closing_l", (245, 239, 226), "grid", 95)
    L = [K.header("left", "28")]
    L.append(K.scrap("kraft", 120, 200, 960, 1100, 1.5, z=2, seed=96))
    tickets = ["japan", "semporna", "bali", "dali", "shenzhenbay", "jeju"]
    for i, pid in enumerate(tickets):
        L.append(K.ticket(pid, 170 + (i % 2) * 40, 250 + i * 165, 600, 180, [-4, 3, -2, 5, -3, 2][i], z=10 + i))
    L.append(K.sticker("bali_mascot", 860, 300, 200, 8))
    L.append(K.sticker("dali_mascot", 860, 760, 210, -6))
    L.append(K.sticker("shenzhenbay_mascot", 860, 1150, 200, 6))
    left = K.page("left", bg, L)

    bg_r = K.paper_bg("closing_r", (246, 240, 229), None, 97)
    R = [K.header("right", "29")]
    R.append(K.text(cl["title"], 120, 280, cls="title", size=120, z=30))
    R.append(K.brush(126, 400, 640, 42, "#b3342c", -1))
    R.append(K.text(cl["hand"], 140, 460, cls="hand", size=34, rot=-2, z=30))
    R.append(K.art("jeju_landscape", -40, 620, 1280, 0, 3))
    R.append(K.postmark("dali", 700, 140, 200, 12, color="#2f4f88", lines=False))
    R.append(K.text(cl["note"], 0, 1420, 1200, cls="type", size=20, z=30, align="center"))
    R.append(K.sticker("japan_mascot", 950, 1180, 160, 8))
    R.append(K.sticker("jeju_mascot", 120, 1180, 150, -8))
    return left, K.page("right", bg_r, R)


SPREADS = [
    ("cover", cover),
    ("s01", contents),
    ("s02", japan_a), ("s03", japan_b),
    ("s04", semporna_a), ("s05", semporna_b),
    ("s06", bali_a), ("s07", bali_b),
    ("s08", dali_a), ("s09", dali_b),
    ("s10", sz_a), ("s11", sz_b),
    ("s12", jeju_a), ("s13", jeju_b),
    ("s14", closing),
]

# 给读屏/无障碍用的页面描述 (left, right)
ALTS = {
    "cover": ("Back cover: list of the six places on kraft paper.", "Front cover: TRAVEL JOURNAL with six watercolor stamps, a postmark, a sakura branch and a lucky-cat sticker."),
    "s01": ("Contents: six places with coordinates and a dotted red route line.", "Six small prints, two ticket stubs and a turtle sticker."),
    "s02": ("Japan title page: JAPAN, red brush line, Fuji stamp, postmark, sakura branch, watercolor of Fuji, lake and torii.", "Polaroid of him in a red scarf before Mount Fuji, torn Fuji fragments, vertical 日本 label, ticket TOKYO → MT. FUJI, lucky-cat sticker."),
    "s03": ("Wide torn photograph of Fuji across the lake, a larger torn cut of the peak, a journal card.", "Tokyo Tower at night on dark paper, three small prints of the tower, pagoda watercolor."),
    "s04": ("Semporna title page with turtle stamp, coral and the stilt-village watercolor.", "Polaroid of him on the deck, torn jetty pieces, 仙本那 label, boat ticket, turtle sticker."),
    "s05": ("Wide torn photograph of the flower jetty over turquoise water and a log card.", "Stilt house watercolor, torn portrait, three small jetty prints, stamp, turtle sticker."),
    "s06": ("Bali title page with temple-gate stamp, frangipani and a sunset rice-terrace watercolor.", "Polaroid at Kelingking cliff, torn beach pieces, 巴厘岛 label, fast-boat ticket, gecko sticker."),
    "s07": ("Tall torn aerial of the beach and surf with three small prints.", "Sunset watercolor with torn cliff photographs, stamp and gecko sticker."),
    "s08": ("Dali title page with Three Pagodas stamp, cosmos and Cangshan–Erhai watercolor; lots of white space.", "Polaroid of the peak at first light, 大理 label, Bai house watercolor, train ticket, black-lamb sticker."),
    "s09": ("Wide polaroid of him with a black lamb in a flower field.", "Torn peak photograph, Bai gate watercolor, stamp and lamb sticker."),
    "s10": ("Shenzhen Bay title page with bridge stamp and a sunset skyline watercolor.", "Polaroid of the camera on its tripod at dusk, torn sky pieces, 深圳湾 label, metro ticket, egret sticker."),
    "s11": ("Three torn strips: before, during and after sunset.", "Skyline watercolor with two polaroids of gold and violet skies."),
    "s12": ("Jeju title page with Seongsan stamp, tangerine branch and Hallasan watercolor.", "Polaroid of the black volcanic beach, torn green-path pieces, 济州岛 label, flight ticket, stone-grandfather sticker."),
    "s13": ("Wide torn photograph of the green seaside path and a note card.", "Polaroid of the YES wall, torn basalt-beach pieces, haenyeo watercolor, stamp."),
    "s14": ("Six ticket stubs on kraft paper with three mascot stickers.", "Until next time, with a Jeju watercolor and two stickers."),
}
