#!/usr/bin/env python3
"""Pack the flipbook into one album_standalone.html that works over file://."""
from __future__ import annotations
import base64, mimetypes, re
from pathlib import Path

SITE = Path(__file__).resolve().parents[2]
OUT = SITE / "album_standalone.html"

ASSET_PATHS = []
# pages first (stable order), then paper, then fonts (for ASSET_DATA completeness)
for sub in ("pages", "paper"):
    ASSET_PATHS += sorted((SITE / "assets" / sub).glob("*"))
ASSET_PATHS += [
    SITE / "assets" / "fonts" / "oswald-400.ttf",
    SITE / "assets" / "fonts" / "oswald-500.ttf",
]


def data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        mime = "image/jpeg"
    elif path.suffix.lower() == ".webp":
        mime = "image/webp"
    elif path.suffix.lower() == ".png":
        mime = "image/png"
    elif path.suffix.lower() == ".ttf":
        mime = "font/ttf"
    elif not mime:
        mime = "application/octet-stream"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def main():
    html = (SITE / "index.html").read_text(encoding="utf-8")
    css = (SITE / "book.css").read_text(encoding="utf-8")

    def font_repl(m):
        rel = m.group(1)
        path = (SITE / rel).resolve()
        return f'url("{data_uri(path)}")'

    css = re.sub(r'url\("([^"]+)"\)', font_repl, css)

    rows = []
    for p in ASSET_PATHS:
        if not p.is_file() or p.name.startswith("."):
            continue
        rel = p.relative_to(SITE).as_posix()
        rows.append(f"  '{rel}': '{data_uri(p)}'")
        print(f"  packed {rel} ({p.stat().st_size / 1024:.0f} KB)")

    asset_js = "window.ASSET_DATA = {\n" + ",\n".join(rows) + "\n};\n"
    asset_js += """function assetUrl(path) {
  return (window.ASSET_DATA && window.ASSET_DATA[path]) || path;
}
(function patchTextureLoader() {
  if (typeof THREE === "undefined" || !THREE.TextureLoader) return;
  var orig = THREE.TextureLoader.prototype.load;
  THREE.TextureLoader.prototype.load = function (url, onLoad, onProgress, onError) {
    if (typeof url === "string" && window.ASSET_DATA && window.ASSET_DATA[url]) {
      url = window.ASSET_DATA[url];
    }
    return orig.call(this, url, onLoad, onProgress, onError);
  };
})();
"""

    three = (SITE / "assets" / "vendor" / "three-r128.min.js").read_text(encoding="utf-8")
    data = (SITE / "book-data.js").read_text(encoding="utf-8")
    book = (SITE / "book.js").read_text(encoding="utf-8")

    def wrap_tex(m):
        # tex("assets/...") or texLoader.load("assets/...")
        fn, inner = m.group(1), m.group(2)
        return f'{fn}(assetUrl({inner})'

    book = re.sub(
        r'\b(tex|texLoader\.load)\((("assets/[^"]+"|\'assets/[^\']+\'|"assets/" \+ [^,)]+|\'assets/\' \+ [^,)]+))',
        wrap_tex,
        book,
    )
    # CSS paper swatch: `url("assets/paper/${st.map || st.swatch}.webp")`
    old_swatch = '`url("assets/paper/${st.map || st.swatch}.webp")`'
    new_swatch = '`url("${assetUrl("assets/paper/" + (st.map || st.swatch) + ".webp")}")`'
    if old_swatch not in book:
        raise SystemExit("paper swatch url pattern not found in book.js")
    book = book.replace(old_swatch, new_swatch, 1)
    if book.count("assetUrl(") < 7:
        raise SystemExit(f"expected at least 7 assetUrl() wraps, got {book.count('assetUrl(')}")

    html = html.replace(
        '<link rel="stylesheet" href="book.css">',
        "<style>\n" + css + "\n</style>",
        1,
    )
    html = html.replace(
        '<script src="assets/vendor/three-r128.min.js"></script>\n'
        '<script src="book-data.js"></script>\n'
        '<script src="book.js"></script>',
        "<script>\n" + three + "\n</script>\n"
        "<script>\n" + asset_js + "\n</script>\n"
        "<script>\n" + data + "\n</script>\n"
        "<script>\n" + book + "\n</script>",
        1,
    )
    if "<script src=" in html:
        raise SystemExit("leftover external script tags")
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
