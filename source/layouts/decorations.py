"""Place-specific SVG decorations. All drawn as original vectors, no AI images."""

import itertools
_uid = itertools.count(1)

def uid(prefix="d"):
    return f"{prefix}{next(_uid)}"


def svg(inner, w=100, h=100, view=None, cls="", style="", opacity=1):
    vb = view or f"0 0 {w} {h}"
    c = f' class="{cls}"' if cls else ""
    s = f' style="{style}"' if style else ""
    op = f' opacity="{opacity}"' if opacity != 1 else ""
    return f'<svg{c}{s}{op} viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{inner}</svg>'


# ---------- Japan: Fuji, sakura, pagoda, torii, lake, pine, hanko, washi ----------

def fuji(fill="#4a6b86", snow="#f7f4ef", line="#2a3d4d", reflect=False):
    # Classic snow-capped cone
    mountain = f'''
    <path d="M8 78 L42 18 C46 12 54 12 58 18 L92 78 Z" fill="{fill}" stroke="{line}" stroke-width="1.2" stroke-linejoin="round"/>
    <path d="M42 18 C46 12 54 12 58 18 L64 28 L56 24 L50 30 L44 24 L36 29 Z" fill="{snow}"/>
    <path d="M20 58 Q50 50 80 58" fill="none" stroke="{snow}" stroke-width="1" opacity=".45"/>
    '''
    if reflect:
        mountain += f'''
        <g opacity=".35" transform="translate(0,80) scale(1,-0.55) translate(0,-78)">
            <path d="M8 78 L42 18 C46 12 54 12 58 18 L92 78 Z" fill="{fill}"/>
            <path d="M42 18 C46 12 54 12 58 18 L64 28 L56 24 L50 30 L44 24 L36 29 Z" fill="{snow}"/>
        </g>
        <path d="M6 78 H94" stroke="{line}" stroke-width=".6" opacity=".4"/>
        '''
        return svg(mountain, view="0 0 100 115")
    return svg(mountain, view="0 0 100 90")


def sakura_flower(fill="#f3b6c4", line="#d4899a", size=24):
    petals = []
    # 5 heart-ish petals around a small center
    for i, ang in enumerate(range(0, 360, 72)):
        petals.append(
            f'<ellipse cx="0" cy="-7" rx="4.2" ry="7.2" fill="{fill}" stroke="{line}" '
            f'stroke-width=".5" transform="rotate({ang})"/>'
        )
    inner = "".join(petals) + f'<circle cx="0" cy="0" r="2.1" fill="#f6e3a1"/>'
    return f'<svg class="sticker sakura" width="{size}" height="{size}" viewBox="-12 -12 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{inner}</svg>'


def sakura_petal(fill="#f3b6c4", rot=0):
    return (
        f'<svg class="sticker petal" viewBox="0 0 12 16" style="transform:rotate({rot}deg)" '
        f'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        f'<path d="M6 1 C9 4 11 8 6 15 C1 8 3 4 6 1Z" fill="{fill}" opacity=".9"/>'
        f'</svg>'
    )


def pagoda_five():
    # Five-story Japanese pagoda: wide flared eaves and a sorin spire
    d = """
    <g stroke="#1a241f" stroke-width=".7" stroke-linejoin="round">
      <rect x="44" y="90" width="12" height="8" fill="#2c3a32"/>
      <path d="M18 90 L50 82 L82 90 L76 86 L24 86 Z" fill="#2c3a32"/>
      <rect x="40" y="74" width="20" height="12" fill="#3d4f44"/>
      <path d="M20 74 L50 66 L80 74 L74 70 L26 70 Z" fill="#2c3a32"/>
      <rect x="42" y="60" width="16" height="10" fill="#3d4f44"/>
      <path d="M24 60 L50 52 L76 60 L70 56 L30 56 Z" fill="#2c3a32"/>
      <rect x="43" y="48" width="14" height="8" fill="#3d4f44"/>
      <path d="M28 48 L50 40 L72 48 L66 44 L34 44 Z" fill="#2c3a32"/>
      <rect x="44" y="36" width="12" height="8" fill="#3d4f44"/>
      <path d="M32 36 L50 28 L68 36 L62 32 L38 32 Z" fill="#2c3a32"/>
      <path d="M50 28 V12" stroke="#2c3a32" stroke-width="1.4" fill="none"/>
      <circle cx="50" cy="10" r="2.2" fill="#c45a3a" stroke="none"/>
    </g>
    <g fill="none" stroke="#c45a3a" stroke-width="1" opacity=".8">
      <path d="M22 86 H78"/>
      <path d="M24 70 H76"/>
      <path d="M28 56 H72"/>
      <path d="M32 44 H68"/>
      <path d="M36 32 H64"/>
    </g>
    """
    return svg(d, view="12 6 76 96")


def torii(color="#c44536"):
    d = f'''
    <g fill="none" stroke="{color}" stroke-width="4" stroke-linecap="square" stroke-linejoin="miter">
      <path d="M10 18 H90"/>
      <path d="M16 26 H84" stroke-width="3"/>
      <path d="M28 18 V88"/>
      <path d="M72 18 V88"/>
    </g>
    <path d="M8 14 L12 18 H88 L92 14" fill="{color}"/>
    '''
    return svg(d, view="0 0 100 96")


def pine_branch(color="#1f3a2c"):
    d = f'''
    <path d="M2 60 Q40 50 98 20" fill="none" stroke="{color}" stroke-width="1.6"/>
    <g fill="{color}">
      <path d="M20 56 l8 -14 l4 2 l-6 14z" opacity=".9"/>
      <path d="M30 54 l10 -16 l4 2 l-8 16z"/>
      <path d="M42 50 l10 -18 l4 2 l-8 17z"/>
      <path d="M54 44 l11 -16 l3.5 2 l-8 15z"/>
      <path d="M66 38 l12 -16 l3 2 l-9 15z"/>
      <path d="M78 30 l10 -14 l3 2 l-8 13z"/>
      <path d="M26 58 l-6 -10 l-3 1 l6 11z" opacity=".8"/>
      <path d="M48 49 l-7 -12 l-3 1 l7 13z" opacity=".8"/>
      <path d="M70 36 l-6 -11 l-3 1 l7 12z" opacity=".8"/>
    </g>
    '''
    return svg(d, view="0 0 100 70")


def mist_clouds(fill="#dfe7ee"):
    d = f'''
    <g fill="{fill}" opacity=".85">
      <ellipse cx="30" cy="20" rx="28" ry="10"/>
      <ellipse cx="55" cy="16" rx="22" ry="8"/>
      <ellipse cx="70" cy="24" rx="26" ry="9"/>
      <ellipse cx="40" cy="36" rx="36" ry="9"/>
    </g>
    '''
    return svg(d, view="0 0 100 50")


def hanko(text="旅", color="#c41e3a"):
    # Square/round vermilion seal
    glyphs = ""
    if text:
        glyphs = f'<text x="50" y="58" text-anchor="middle" font-family="serif" font-size="36" font-weight="700" fill="{color}">{text}</text>'
    d = f'''
    <rect x="8" y="8" width="84" height="84" rx="6" fill="none" stroke="{color}" stroke-width="6"/>
    <rect x="16" y="16" width="68" height="68" rx="2" fill="none" stroke="{color}" stroke-width="1.2" opacity=".7"/>
    {glyphs}
    '''
    return svg(d, view="0 0 100 100", cls="sticker hanko")


def washi_tape(width=220, height=36, color="#f3c1cd", pattern="dots", rot=-8):
    # Torn-end washi tape as inline SVG
    pid, cid = uid("wp"), uid("wc")
    if pattern == "dots":
        pat = f'''
        <pattern id="{pid}" width="10" height="10" patternUnits="userSpaceOnUse">
          <circle cx="3" cy="3" r="1.3" fill="#ffffff" opacity=".55"/>
        </pattern>
        <rect x="0" y="0" width="{width}" height="{height}" fill="url(#{pid})"/>
        '''
    elif pattern == "stripe":
        pat = f'''
        <pattern id="{pid}" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(25)">
          <rect width="4" height="8" fill="#ffffff" opacity=".35"/>
        </pattern>
        <rect x="0" y="0" width="{width}" height="{height}" fill="url(#{pid})"/>
        '''
    else:  # sakura mini
        pat = f'''
        <pattern id="{pid}" width="18" height="18" patternUnits="userSpaceOnUse">
          <circle cx="6" cy="6" r="2.2" fill="#ffffff" opacity=".45"/>
        </pattern>
        <rect x="0" y="0" width="{width}" height="{height}" fill="url(#{pid})"/>
        '''
    # jagged torn ends via clip
    d = f'''
    <defs>
      <clipPath id="{cid}">
        <path d="M6 0 L{width-6} 0 L{width} 8 L{width-4} 16 L{width} 24 L{width-6} {height} L6 {height} L0 {height-6} L4 {height/2} L0 8 Z"/>
      </clipPath>
    </defs>
    <g clip-path="url(#{cid})">
      <rect width="{width}" height="{height}" fill="{color}" opacity=".82"/>
      {pat}
    </g>
    <path d="M6 0 L{width-6} 0 M6 {height} L{width-6} {height}" fill="none" stroke="#000" opacity=".06" stroke-width="1"/>
    '''
    return (
        f'<svg class="sticker washi" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'style="transform:rotate({rot}deg)" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{d}</svg>'
    )


# ---------- Semporna: turtle, coral, stilt village, waves, shells ----------

def sea_turtle(fill="#2a7a72", line="#163d39"):
    d = f'''
    <g fill="{fill}" stroke="{line}" stroke-width="1.2" stroke-linejoin="round">
      <ellipse cx="50" cy="50" rx="26" ry="20"/>
      <path d="M72 42 Q92 38 88 52 Q84 62 70 58" />
      <circle cx="86" cy="48" r="1.6" fill="{line}"/>
      <path d="M28 40 Q10 28 14 44 Q16 52 30 48"/>
      <path d="M28 58 Q10 72 18 68 Q28 66 34 60"/>
      <path d="M68 62 Q78 80 70 76 Q60 70 58 64"/>
    </g>
    <g fill="none" stroke="#cdeee6" stroke-width="1.1">
      <polygon points="50,36 60,44 56,56 44,56 40,44"/>
      <path d="M50 36 L50 56 M40 44 L60 44 M44 56 L50 44 L56 56"/>
    </g>
    '''
    return svg(d, view="0 10 100 86")


def coral(color="#d46a8a"):
    d = f'''
    <g fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round">
      <path d="M50 92 V48"/>
      <path d="M50 70 Q30 62 28 44 Q27 30 36 32"/>
      <path d="M50 62 Q70 56 74 38 Q76 24 64 28"/>
      <path d="M50 52 Q40 40 44 26"/>
      <path d="M50 52 Q62 36 58 22"/>
    </g>
    <g fill="{color}" opacity=".85">
      <circle cx="36" cy="32" r="4"/>
      <circle cx="64" cy="28" r="4"/>
      <circle cx="44" cy="26" r="3.2"/>
      <circle cx="58" cy="22" r="3.2"/>
    </g>
    '''
    return svg(d, view="18 16 64 84")


def stilt_village(fill="#6b3f2a", water="#5ec6c0"):
    d = f'''
    <g fill="{fill}">
      <!-- houses -->
      <rect x="8" y="40" width="22" height="16"/>
      <path d="M6 40 L19 28 L32 40 Z"/>
      <rect x="36" y="36" width="26" height="20"/>
      <path d="M34 36 L49 22 L64 36 Z"/>
      <rect x="68" y="42" width="22" height="14"/>
      <path d="M66 42 L79 30 L92 42 Z"/>
      <!-- stilts -->
      <g stroke="{fill}" stroke-width="1.6">
        <path d="M12 56 V78 M24 56 V80 M42 56 V82 M56 56 V80 M74 56 V78 M86 56 V81"/>
      </g>
    </g>
    <path d="M0 78 Q25 72 50 78 T100 76 V100 H0 Z" fill="{water}" opacity=".7"/>
    <path d="M0 84 Q20 80 40 85 T100 82" fill="none" stroke="#fff" stroke-width="1" opacity=".5"/>
    '''
    return svg(d, view="0 18 100 82")


def waves(color="#2aa8b0", n=3):
    paths = []
    for i in range(n):
        y = 18 + i * 16
        paths.append(f'<path d="M0 {y} Q12 {y-10} 24 {y} T48 {y} T72 {y} T96 {y} T120 {y}" fill="none" stroke="{color}" stroke-width="2" opacity="{0.9 - i*0.2}"/>')
    return svg("".join(paths), view="0 0 120 64")


def shell(color="#e7c9a8"):
    d = f'''
    <path d="M50 88 C20 70 16 40 32 24 C40 16 50 20 50 20 C50 20 60 16 68 24 C84 40 80 70 50 88Z" fill="{color}" stroke="#b88968" stroke-width="1.2"/>
    <g fill="none" stroke="#b88968" stroke-width=".8">
      <path d="M50 84 C34 66 32 44 44 30"/>
      <path d="M50 84 C50 64 50 44 50 28"/>
      <path d="M50 84 C66 66 68 44 56 30"/>
    </g>
    '''
    return svg(d, view="14 14 72 80")


# ---------- Bali: frangipani, candi bentar, rice terraces, palms, volcano, sunset ----------

def frangipani(fill="#f7efe3", center="#f2c14e", line="#d9c9b0"):
    d = f'''
    <g>
    '''
    for ang in (0, 72, 144, 216, 288):
        d += f'<ellipse cx="0" cy="-11" rx="6" ry="13" fill="{fill}" stroke="{line}" stroke-width=".6" transform="translate(50 50) rotate({ang})"/>'
    d += f'<circle cx="50" cy="50" r="5" fill="{center}"/></g>'
    return svg(d, view="20 18 60 64")


def candi_bentar(color="#4a2e1c"):
    # Balinese split gate (candi bentar): two mirrored, multi-tiered towers with a gap
    def half(x, flip):
        return f"""
        <g transform="translate({x},0) scale({flip},1)">
          <path d="M2 96 H40 V84 H8 L2 96Z" fill="{color}"/>
          <path d="M8 84 H36 L32 72 H12 Z" fill="{color}"/>
          <path d="M12 72 H32 L28 60 H16 Z" fill="{color}"/>
          <path d="M16 60 H28 L25 50 H19 Z" fill="{color}"/>
          <path d="M19 50 L22 36 L25 50 Z" fill="{color}"/>
          <path d="M22 36 L22 26 L26 32 L22 36" fill="#e8c98a"/>
          <g fill="none" stroke="#e8c98a" stroke-width="1.1" opacity=".85">
            <path d="M10 84 H34 M14 72 H30 M18 60 H26"/>
          </g>
        </g>
        """
    d = half(6, 1) + half(94, -1)
    # threshold / path between the gates
    d += f'<rect x="40" y="92" width="20" height="4" fill="#c4a574" opacity=".7"/>'
    return svg(d, view="0 20 100 80")


def rice_terraces(color="#5a8a45"):
    d = f'''
    <g fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round">
      <path d="M0 80 Q25 70 50 78 T100 74"/>
      <path d="M0 68 Q30 58 55 66 T100 62"/>
      <path d="M0 56 Q28 46 50 54 T100 50"/>
      <path d="M0 44 Q22 36 48 42 T100 38"/>
      <path d="M0 32 Q30 24 60 30 T100 26"/>
    </g>
    '''
    return svg(d, view="0 18 100 70")


def palm(color="#1e5a32"):
    d = f'''
    <path d="M50 98 V42" stroke="#6b4226" stroke-width="3" fill="none"/>
    <g fill="{color}">
      <path d="M50 44 Q20 20 8 36 Q28 34 50 44Z"/>
      <path d="M50 44 Q24 8 18 24 Q36 24 50 44Z"/>
      <path d="M50 44 Q50 2 40 16 Q48 22 50 44Z"/>
      <path d="M50 44 Q50 2 60 16 Q52 22 50 44Z"/>
      <path d="M50 44 Q76 8 82 24 Q64 24 50 44Z"/>
      <path d="M50 44 Q80 20 92 36 Q72 34 50 44Z"/>
    </g>
    '''
    return svg(d, view="4 0 92 100")


def volcano_distant(fill="#6b5a55", sky_line="#c9894a"):
    d = f'''
    <path d="M4 80 L38 28 L46 40 L54 26 L96 80 Z" fill="{fill}" opacity=".85"/>
    <path d="M38 28 L46 40 L54 26 L50 22 Z" fill="#f0e6d8" opacity=".7"/>
    <path d="M0 80 H100" stroke="{sky_line}" stroke-width=".6" opacity=".5"/>
    '''
    return svg(d, view="0 18 100 82")


def sun_disk(color="#f0a04a", r=18):
    return svg(f'<circle cx="50" cy="50" r="{r}" fill="{color}"/>', view="20 20 60 60")


# ---------- Dali: Cangshan, Erhai, Bai pattern, three pagodas, bike, ink wash ----------

def cangshan_range(fill="#8b9399"):
    gid = uid("ink")
    d = f'''
    <defs>
      <linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="{fill}" stop-opacity=".85"/>
        <stop offset="1" stop-color="{fill}" stop-opacity=".15"/>
      </linearGradient>
    </defs>
    <path d="M0 80 L12 62 L22 70 L38 36 L46 48 L58 28 L70 50 L82 40 L100 68 L100 100 H0 Z" fill="url(#{gid})"/>
    <path d="M0 86 L18 74 L30 80 L48 58 L62 72 L80 60 L100 78 L100 100 H0 Z" fill="{fill}" opacity=".28"/>
    '''
    return svg(d, view="0 20 100 80")


def erhai_lake(water="#5ea0c0"):
    d = f'''
    <path d="M0 40 C20 28 40 48 60 36 C78 26 90 40 100 34 V90 H0 Z" fill="{water}" opacity=".55"/>
    <path d="M0 52 C24 44 40 60 64 50 C80 44 90 54 100 48" fill="none" stroke="#fff" stroke-width="1.2" opacity=".5"/>
    <path d="M0 38 C18 30 30 36 48 30" fill="none" stroke="#2f5770" stroke-width="1" opacity=".45"/>
    '''
    return svg(d, view="0 20 100 80")


def three_pagodas():
    # Three Pagodas of Chongsheng: white square towers, many close flared eaves
    def pag(x, h, w, stories):
        body = 90 - h
        eaves = []
        for i in range(stories):
            y = 90 - (i + 0.15) * (h / stories)
            half = (w / 2) + 5 - i * 0.25
            eaves.append(
                f'<path d="M{x-half} {y} L{x} {y-3.5} L{x+half} {y}" '
                f'fill="#f3efe6" stroke="#6a624e" stroke-width=".7" stroke-linejoin="round"/>'
            )
        return f"""
        <rect x="{x-w/2}" y="{body}" width="{w}" height="{h}" fill="#f7f3ea" stroke="#8a8374" stroke-width=".6"/>
        {''.join(eaves)}
        <path d="M{x} {body} L{x} {body-7}" stroke="#8a8374" stroke-width="1.1"/>
        <circle cx="{x}" cy="{body-8}" r="1.6" fill="#8a8374"/>
        """
    d = pag(22, 46, 11, 9) + pag(50, 70, 13, 13) + pag(78, 46, 11, 9)
    d += '<rect x="10" y="90" width="80" height="3.5" fill="#cfc6b4"/>'
    return svg(d, view="4 6 92 92")


def bai_pattern(tile="#3a6ea5", wall="#f4efe6"):
    # Geometric blue-tile / floral diamond pattern of Bai architecture
    d = f'''
    <rect width="100" height="100" fill="{wall}"/>
    <g fill="none" stroke="{tile}" stroke-width="1.6">
      <rect x="20" y="20" width="60" height="60" transform="rotate(45 50 50)"/>
      <rect x="32" y="32" width="36" height="36" transform="rotate(45 50 50)"/>
    </g>
    <circle cx="50" cy="50" r="5" fill="{tile}"/>
    <g fill="{tile}">
      <path d="M50 18 l3 8 h-6z M50 82 l3 -8 h-6z M18 50 l8 3 v-6z M82 50 l-8 3 v-6z"/>
    </g>
    '''
    return svg(d, view="0 0 100 100")


def bicycle(color="#2c3a42"):
    d = f'''
    <g fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="28" cy="70" r="16"/>
      <circle cx="78" cy="70" r="16"/>
      <path d="M28 70 L46 70 L62 42 H50"/>
      <path d="M46 70 L58 70 L78 70"/>
      <path d="M62 42 L78 70"/>
      <path d="M50 42 L40 58"/>
      <path d="M58 42 V36 H68"/>
    </g>
    '''
    return svg(d, view="8 24 92 70")


def ink_wash_cloud(fill="#9aa8b3"):
    d = f'''
    <g fill="{fill}" opacity=".35">
      <ellipse cx="40" cy="30" rx="36" ry="16"/>
      <ellipse cx="62" cy="24" rx="28" ry="12"/>
      <ellipse cx="50" cy="40" rx="40" ry="10"/>
    </g>
    '''
    return svg(d, view="0 8 100 56")


# ---------- Shenzhen Bay: skyline, bridge, sun, mangroves, cyclist, egrets ----------

def skyline(color="#2a2e35"):
    # Simplified Shenzhen-ish skyline with a tall center tower
    d = f'''
    <g fill="{color}">
      <rect x="2" y="58" width="8" height="32"/>
      <rect x="12" y="48" width="7" height="42"/>
      <rect x="21" y="40" width="10" height="50"/>
      <rect x="33" y="28" width="8" height="62"/>
      <path d="M37 28 L37 10 L39 28 Z"/> <!-- KK100-ish spire -->
      <rect x="44" y="44" width="12" height="46"/>
      <rect x="58" y="36" width="9" height="54"/>
      <rect x="69" y="50" width="8" height="40"/>
      <rect x="79" y="42" width="7" height="48"/>
      <rect x="88" y="56" width="10" height="34"/>
    </g>
    '''
    return svg(d, view="0 8 100 92")


def bay_bridge(color="#2a2e35"):
    # Cable-stayed bridge
    d = f'''
    <g fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round">
      <path d="M0 78 H100"/>
      <path d="M36 78 V28 M70 78 V36"/>
      <path d="M36 30 L8 78 M36 30 L20 78 M36 30 L50 78 M36 30 L62 78"/>
      <path d="M70 38 L50 78 M70 38 L62 78 M70 38 L82 78 M70 38 L94 78"/>
    </g>
    <rect x="33" y="24" width="6" height="54" fill="{color}"/>
    <rect x="67" y="32" width="5" height="46" fill="{color}"/>
    '''
    return svg(d, view="0 16 100 80")


def mangrove(color="#1e4a36"):
    d = f'''
    <g fill="{color}">
      <path d="M30 80 Q20 50 34 30 Q40 50 46 30 Q58 52 50 80 Z"/>
      <path d="M58 82 Q54 58 66 36 Q70 56 80 40 Q86 60 78 82 Z"/>
    </g>
    <g fill="none" stroke="{color}" stroke-width="1.4">
      <path d="M36 80 Q32 92 24 98 M40 80 Q40 94 40 100 M44 80 Q50 94 56 98"/>
      <path d="M64 82 Q60 94 54 100 M70 82 Q74 96 80 100"/>
    </g>
    '''
    return svg(d, view="16 24 76 80")


def cyclist(color="#2a2e35"):
    d = f'''
    <g fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="30" cy="72" r="14"/>
      <circle cx="74" cy="72" r="14"/>
      <path d="M30 72 L44 72 L58 44 H50"/>
      <path d="M44 72 L74 72"/>
      <path d="M58 44 L74 72"/>
      <circle cx="54" cy="28" r="5" fill="{color}"/>
      <path d="M54 33 L50 50 L62 50"/>
      <path d="M50 50 L42 66"/>
      <path d="M62 44 L74 40"/>
    </g>
    '''
    return svg(d, view="10 18 86 78")


def egret(color="#f4f1ea"):
    d = f'''
    <g fill="{color}" stroke="#6a6a66" stroke-width=".8" stroke-linejoin="round">
      <path d="M40 70 Q30 50 42 40 Q60 36 58 52 Q70 48 66 36 Q62 28 70 22"/>
      <path d="M42 40 L36 30"/>
    </g>
    <path d="M36 30 L22 26" stroke="#e0a040" stroke-width="1.4" fill="none" stroke-linecap="round"/>
    <path d="M40 70 L38 90 M44 70 L48 90" stroke="#6a6a66" stroke-width="1.2"/>
    '''
    return svg(d, view="16 16 64 80")


def horizon_sun(color="#f08a3a"):
    d = f'''
    <circle cx="50" cy="42" r="22" fill="{color}"/>
    <g fill="{color}" opacity=".35">
      <rect x="20" y="64" width="60" height="3"/>
      <rect x="24" y="72" width="52" height="2.2"/>
      <rect x="28" y="80" width="44" height="1.6"/>
    </g>
    '''
    return svg(d, view="16 16 68 72")


# ---------- Jeju: Hallasan, basalt, dol hareubang, tangerine, Seongsan, hills, shells ----------

def hallasan(fill="#4d5c4a", snow="#eef2ee"):
    d = f'''
    <path d="M2 86 L18 64 L30 72 L48 28 L58 44 L70 34 L98 86 Z" fill="{fill}"/>
    <path d="M48 28 L58 44 L54 36 L50 42 L46 34 Z" fill="{snow}" opacity=".85"/>
    <path d="M0 86 H100" stroke="#2f3a2e" stroke-width=".6" opacity=".4"/>
    '''
    return svg(d, view="0 20 100 80")


def seongsan(fill="#3f6b4a"):
    # Crater cone / sunrise peak
    d = f'''
    <path d="M8 88 L28 40 Q40 22 50 26 Q64 22 72 42 L92 88 Z" fill="{fill}"/>
    <path d="M32 48 Q50 34 68 50 Q50 44 32 48Z" fill="#2a4a32" opacity=".7"/>
    <ellipse cx="50" cy="44" rx="14" ry="5" fill="#2a4a32" opacity=".55"/>
    '''
    return svg(d, view="4 18 92 76")


def dol_hareubang(stone="#5c5c58"):
    # Stone grandfather: hat, dotted eyes, hands on belly
    d = f'''
    <g fill="{stone}" stroke="#2e2e2c" stroke-width="1.2" stroke-linejoin="round">
      <ellipse cx="50" cy="22" rx="26" ry="10"/>
      <rect x="28" y="20" width="44" height="10" rx="2"/>
      <path d="M30 30 Q26 44 32 58 L28 96 H72 L68 58 Q74 44 70 30 Z"/>
      <!-- hat brim shadow -->
    </g>
    <g fill="#2e2e2c">
      <circle cx="40" cy="48" r="3.2"/>
      <circle cx="60" cy="48" r="3.2"/>
      <path d="M42 60 Q50 64 58 60" fill="none" stroke="#2e2e2c" stroke-width="1.6" stroke-linecap="round"/>
    </g>
    <!-- hands on belly -->
    <ellipse cx="38" cy="76" rx="8" ry="6" fill="#6a6a66" stroke="#2e2e2c" stroke-width="1"/>
    <ellipse cx="62" cy="76" rx="8" ry="6" fill="#6a6a66" stroke="#2e2e2c" stroke-width="1"/>
    '''
    return svg(d, view="18 8 64 96")


def tangerine(fill="#f08a2a", leaf="#3a7a3a"):
    d = f'''
    <circle cx="50" cy="58" r="28" fill="{fill}" stroke="#d06c14" stroke-width="1.2"/>
    <path d="M50 30 Q54 22 50 16 Q46 22 50 30" fill="#3a5a20"/>
    <path d="M50 24 Q66 10 78 22 Q62 22 50 28" fill="{leaf}"/>
    <path d="M40 50 Q50 54 58 48" fill="none" stroke="#d06c14" stroke-width="1" opacity=".5"/>
    '''
    return svg(d, view="16 8 70 86")


def basalt(color="#2a2a2c"):
    # Hexagonal / irregular volcanic rock cluster
    d = f'''
    <g fill="{color}" stroke="#111" stroke-width=".8">
      <polygon points="50,8 70,20 70,44 50,56 30,44 30,20"/>
      <polygon points="20,48 38,58 34,80 14,88 4,68 10,52"/>
      <polygon points="66,58 86,50 98,68 88,90 66,88 58,70"/>
      <polygon points="40,70 58,68 62,92 36,96 30,82"/>
    </g>
    '''
    return svg(d, view="0 4 100 100")


def grass_hills(color="#4a8a4a"):
    d = f'''
    <path d="M0 70 C18 50 30 58 48 44 C64 32 78 50 100 40 V100 H0 Z" fill="{color}"/>
    <path d="M0 82 C22 70 40 86 60 72 C78 62 90 76 100 70 V100 H0 Z" fill="{color}" opacity=".7"/>
    '''
    return svg(d, view="0 30 100 70")


def tag_label(text, w=140, h=36, fill="#f6efe2", ink="#2a2420", rot=-6):
    d = f'''
    <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="3" fill="{fill}" stroke="#2a2420" stroke-width="1.2"/>
    <circle cx="16" cy="{h/2}" r="4.5" fill="none" stroke="#2a2420" stroke-width="1.2"/>
    <circle cx="16" cy="{h/2}" r="1.6" fill="#2a2420" opacity=".35"/>
    <text x="28" y="{h*0.66}" font-family="Oswald, sans-serif" font-size="13" letter-spacing="1.6" fill="{ink}">{text}</text>
    '''
    return (
        f'<svg class="sticker tag" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'style="transform:rotate({rot}deg)" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{d}</svg>'
    )


def postage_stamp(inner_svg, w=90, h=110, stroke="#2a2420"):
    # Perforated stamp frame
    teeth = []
    step = 8
    for x in range(4, w-2, step):
        teeth.append(f'<circle cx="{x}" cy="3" r="2" fill="white"/>')
        teeth.append(f'<circle cx="{x}" cy="{h-3}" r="2" fill="white"/>')
    for y in range(4, h-2, step):
        teeth.append(f'<circle cx="3" cy="{y}" r="2" fill="white"/>')
        teeth.append(f'<circle cx="{w-3}" cy="{y}" r="2" fill="white"/>')
    d = f'''
    <rect x="1" y="1" width="{w-2}" height="{h-2}" fill="#f7f1e6" stroke="{stroke}" stroke-width="1.4"/>
    {''.join(teeth)}
    <g transform="translate(10,10) scale(0.7)">{inner_svg}</g>
    '''
    return f'<svg class="sticker stamp" width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{d}</svg>'
