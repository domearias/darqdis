#!/usr/bin/env python3
"""
carrusel.py — genera el carrusel de Instagram de un modelo de la Biblioteca 3D.

A partir de un modelo (de biblioteca.json) + sus renders, produce:
  - slides on-brand en 1080x1350 (4:5) renderizados a PNG listos para postear
  - un caption.txt con el copy y los hashtags

On-brand: usa las plantillas del BRANDBOOK (§09) — Playfair en titulares,
Archivo en cuerpo, ritmo oscuro → render → cierre CTA beige. Tipografía
incrustada (base64) para que los PNG salgan idénticos sin depender de red.

Uso directo (normalmente lo llama publicar.py):
  python scripts/carrusel.py --numero 3 --render img/biblioteca/pace.jpg \
      --render extra1.jpg --root .

Salida: build/carrusel-003/{01.png, 02.png, ..., caption.txt, index.html}
"""

import argparse
import base64
import csv as csvmod
import html
import json
import mimetypes
import pathlib
import shutil
import subprocess
import sys
import tempfile

# ---------------------------------------------------------------- paleta / marca
BONE = "#FAFAF7"
BEIGE = "#F0EDE6"
ESPRESSO = "#1A1714"
INK = "#111009"
INK_SOFT = "#3D3830"
OLIVE = "#6E6A4D"
OXBLOOD = "#5C2E26"
HANDLE = "@domenica.arqdis"
DOMINIO = "darqdis.com/biblioteca"
SITIO = "https://darqdis.com"  # base para las URLs públicas de los renders

# Columnas del CSV de Canva Bulk Create. Los encabezados son los nombres de
# campo que Canva empareja con los marcadores de tu plantilla maestra.
CSV_COLS = ["nombre", "numero", "categoria", "tip", "fuente", "cta", "handle", "dominio", "render"]

W, H = 1080, 1350  # 4:5

CAT_LABEL = {
    "asientos": "Asientos", "mesas": "Mesas", "almacenaje": "Almacenaje",
    "iluminacion": "Iluminación", "cocina": "Cocina", "baño": "Baño",
    "exterior": "Exterior", "decoracion": "Decoración",
}

FONTS = [
    ("Archivo", "normal", 400, "archivo-400.ttf"),
    ("Archivo", "normal", 500, "archivo-500.ttf"),
    ("Archivo", "normal", 600, "archivo-600.ttf"),
    ("Playfair Display", "normal", 500, "playfair-500.ttf"),
    ("Playfair Display", "italic", 500, "playfair-500i.ttf"),
]

CHROME_CANDIDATES = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
    shutil.which("google-chrome"),
]


def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if c and pathlib.Path(c).exists():
            return c
    return None


def data_uri(path: pathlib.Path) -> str:
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def font_face_css(fonts_dir: pathlib.Path) -> str:
    bloques = []
    for fam, style, weight, fname in FONTS:
        f = fonts_dir / fname
        if not f.exists():
            continue
        b64 = base64.b64encode(f.read_bytes()).decode("ascii")
        bloques.append(
            "@font-face{font-family:'%s';font-style:%s;font-weight:%d;"
            "font-display:block;src:url(data:font/ttf;base64,%s) format('truetype');}"
            % (fam, style, weight, b64)
        )
    return "\n".join(bloques)


# ---------------------------------------------------------------- slides
def _page(inner: str, css_extra: str, fonts_css: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fonts_css}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;}}
.slide{{width:{W}px;height:{H}px;position:relative;overflow:hidden;
  font-family:'Archivo',sans-serif;-webkit-font-smoothing:antialiased;}}
.serif{{font-family:'Playfair Display',Georgia,serif;font-weight:500;}}
.it{{font-style:italic;}}
.k{{font-family:'Archivo',sans-serif;font-weight:600;font-size:24px;
  letter-spacing:6px;text-transform:uppercase;}}
{css_extra}
</style></head><body>{inner}</body></html>"""


def slide_cover(m, render_uri, fonts_css) -> str:
    nombre = html.escape(m["nombre"])
    n = f"{m['numero']:03d}"
    cat = CAT_LABEL.get(m["categoria"], m["categoria"].title())
    inner = f"""<div class="slide">
      <img src="{render_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
      <div style="position:absolute;inset:0;background:
        linear-gradient(180deg,rgba(26,23,20,.55) 0%,rgba(26,23,20,0) 34%,rgba(26,23,20,.15) 60%,rgba(26,23,20,.92) 100%);"></div>
      <div style="position:absolute;inset:0;padding:82px 78px;display:flex;flex-direction:column;color:{BONE};">
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <span class="k" style="color:rgba(250,250,247,.9);">Biblioteca 3D</span>
          <span class="k" style="color:{BONE};background:{OXBLOOD};padding:12px 20px;letter-spacing:4px;">#{n}</span>
        </div>
        <div style="margin-top:auto;">
          <span class="k" style="color:rgba(250,250,247,.6);font-size:21px;">{cat} · Gratis para SketchUp</span>
          <h1 class="serif" style="font-size:104px;line-height:.98;margin-top:20px;letter-spacing:-1px;">{nombre}</h1>
          <div style="margin-top:40px;display:flex;justify-content:space-between;align-items:flex-end;">
            <span style="font-weight:500;font-size:26px;letter-spacing:1px;">{HANDLE}</span>
            <span style="font-weight:400;font-size:24px;color:rgba(250,250,247,.7);">Desliza →</span>
          </div>
        </div>
      </div>
    </div>"""
    return _page(inner, "", fonts_css)


def slide_render(m, render_uri, idx, total, fonts_css) -> str:
    nombre = html.escape(m["nombre"])
    inner = f"""<div class="slide" style="background:{ESPRESSO};">
      <img src="{render_uri}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">
      <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(26,23,20,0) 62%,rgba(26,23,20,.88) 100%);"></div>
      <div style="position:absolute;left:78px;right:78px;bottom:78px;display:flex;justify-content:space-between;align-items:center;color:{BONE};">
        <span class="serif" style="font-size:40px;">{nombre}</span>
        <span class="k" style="font-size:20px;color:rgba(250,250,247,.7);">{idx}/{total}</span>
      </div>
    </div>"""
    return _page(inner, "", fonts_css)


def slide_tip(m, fonts_css) -> str:
    tip = html.escape(m.get("tip", ""))
    inner = f"""<div class="slide" style="background:{BONE};color:{INK};">
      <div style="padding:120px 92px;height:100%;display:flex;flex-direction:column;">
        <span class="serif it" style="font-size:180px;color:{OLIVE};line-height:.7;">01</span>
        <span class="k" style="font-size:22px;color:{INK_SOFT};margin-top:44px;">Cómo usarlo</span>
        <h2 class="serif" style="font-size:70px;line-height:1.06;margin-top:22px;color:{INK};max-width:14ch;">
          Un detalle para tu escena</h2>
        <p style="font-family:'Archivo';font-weight:400;font-size:36px;line-height:1.55;color:{INK_SOFT};margin-top:34px;max-width:24ch;">{tip}</p>
        <span class="k" style="font-size:19px;color:{INK_SOFT};margin-top:auto;opacity:.6;">{DOMINIO}</span>
      </div>
    </div>"""
    return _page(inner, "", fonts_css)


def slide_cta(m, fonts_css) -> str:
    fuente = html.escape(m.get("fuente", ""))
    credito = f"Fuente · {fuente}" if fuente else ""
    inner = f"""<div class="slide" style="background:{BEIGE};color:{INK};">
      <div style="padding:120px 92px;height:100%;display:flex;flex-direction:column;">
        <span class="k" style="font-size:22px;color:{OXBLOOD};">Biblioteca 3D · darqdis</span>
        <h2 class="serif" style="font-size:96px;line-height:1;margin-top:auto;letter-spacing:-1px;max-width:12ch;">
          Descárgalo <span class="it" style="color:{OXBLOOD};">gratis.</span></h2>
        <p style="font-weight:400;font-size:36px;line-height:1.5;color:{INK_SOFT};margin-top:30px;max-width:22ch;">
          Modelo listo para SketchUp, curado y con crédito a su autor.</p>
        <div style="margin-top:44px;display:inline-flex;align-self:flex-start;background:{OXBLOOD};color:{BONE};
          font-weight:600;font-size:24px;letter-spacing:4px;text-transform:uppercase;padding:26px 40px;">
          Link en bio →</div>
        <div style="margin-top:auto;padding-top:60px;display:flex;justify-content:space-between;align-items:flex-end;">
          <span style="font-weight:500;font-size:26px;">{HANDLE}</span>
          <span style="font-weight:400;font-size:22px;color:{INK_SOFT};">{credito}</span>
        </div>
      </div>
    </div>"""
    return _page(inner, "", fonts_css)


def build_slides(m, render_uris, fonts_css):
    """Devuelve lista de (nombre_archivo, html)."""
    slides = []
    slides.append(("01", slide_cover(m, render_uris[0], fonts_css)))
    extras = render_uris[1:]
    total = len(extras) + 1
    for i, uri in enumerate(extras, start=2):
        slides.append((f"{i:02d}", slide_render(m, uri, i, total, fonts_css)))
    if m.get("tip"):
        slides.append((f"{len(slides)+1:02d}", slide_tip(m, fonts_css)))
    slides.append((f"{len(slides)+1:02d}", slide_cta(m, fonts_css)))
    return slides


# ---------------------------------------------------------------- caption
def caption_text(m) -> str:
    n = f"{m['numero']:03d}"
    cat = CAT_LABEL.get(m["categoria"], m["categoria"].title())
    fuente = m.get("fuente", "")
    tip = m.get("tip", "").strip()
    lineas = [f"{m['nombre']} · Modelo #{n} para SketchUp"]
    if tip:
        lineas += ["", tip]
    lineas += [
        "",
        "Descárgalo gratis en la Biblioteca 3D de darqdis — modelo curado y "
        + (f"con crédito a {fuente}." if fuente else "listo para tu escena."),
        "",
        "Link en bio → darqdis.com/biblioteca",
        "",
        f"#sketchup #diseñointerior #interiorismo #render3d #modelo3d "
        f"#{cat.lower().replace('ó','o').replace('ñ','n')} #arquitectura "
        f"#3dwarehouse #mobiliario #darqdis #arquilab",
    ]
    return "\n".join(lineas)


# ---------------------------------------------------------------- CSV Bulk Create
def csv_row(m, sitio=SITIO) -> dict:
    """Una fila = un carrusel en Canva Bulk Create. `render` es la URL pública."""
    render_url = sitio.rstrip("/") + "/" + m["imagen"].lstrip("/")
    return {
        "nombre": m["nombre"],
        "numero": f"#{m['numero']:03d}",
        "categoria": CAT_LABEL.get(m["categoria"], m["categoria"].title()),
        "tip": m.get("tip", ""),
        "fuente": (f"Fuente · {m['fuente']}" if m.get("fuente") else ""),
        "cta": "Link en bio →",
        "handle": HANDLE,
        "dominio": DOMINIO,
        "render": render_url,
    }


def write_csv(rows, dest, sitio=SITIO):
    dest = pathlib.Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", newline="", encoding="utf-8-sig") as f:  # BOM: acentos ok en Canva/Excel
        w = csvmod.DictWriter(f, fieldnames=CSV_COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return dest


# ---------------------------------------------------------------- render PNG
def render_png(chrome, html_str, out_png):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html_str)
        tmp_html = tf.name
    cmd = [
        chrome, "--headless", "--no-sandbox", "--disable-gpu",
        "--hide-scrollbars", "--force-device-scale-factor=1",
        "--default-background-color=00000000",
        f"--window-size={W},{H}",
        f"--screenshot={out_png}", f"file://{tmp_html}",
    ]
    subprocess.run(cmd, capture_output=True, timeout=90)
    pathlib.Path(tmp_html).unlink(missing_ok=True)
    return pathlib.Path(out_png).exists()


def generar(numero, render_paths, root=".", out_dir=None):
    root = pathlib.Path(root)
    fonts_dir = pathlib.Path(__file__).parent / "assets" / "fonts"
    modelos = json.loads((root / "biblioteca.json").read_text("utf-8"))
    m = next((x for x in modelos if x["numero"] == numero), None)
    if not m:
        sys.exit(f"ERROR: no existe el modelo #{numero} en biblioteca.json")

    # renders: si no se pasan, usa la imagen del modelo
    if not render_paths:
        render_paths = [str(root / m["imagen"].lstrip("/"))]
    render_uris = []
    for rp in render_paths:
        p = pathlib.Path(rp)
        if not p.exists():
            sys.exit(f"ERROR: no existe el render {rp}")
        render_uris.append(data_uri(p))

    out = pathlib.Path(out_dir) if out_dir else (root / "build" / f"carrusel-{numero:03d}")
    out.mkdir(parents=True, exist_ok=True)

    fonts_css = font_face_css(fonts_dir)
    slides = build_slides(m, render_uris, fonts_css)

    # index.html (todos los slides juntos, para previsualizar / capturar a mano)
    preview = "".join(
        f'<div style="display:inline-block;margin:10px;box-shadow:0 10px 30px rgba(0,0,0,.2)">{h}</div>'
        for _, h in slides
    )
    (out / "index.html").write_text(
        f'<!doctype html><body style="background:#ddd;text-align:center">{preview}</body>',
        "utf-8",
    )

    chrome = find_chrome()
    pngs = []
    if chrome:
        for name, h in slides:
            png = out / f"{name}.png"
            if render_png(chrome, h, str(png)):
                pngs.append(png)
    else:
        # sin navegador: deja cada slide como HTML individual
        for name, h in slides:
            (out / f"{name}.html").write_text(h, "utf-8")

    cap = out / "caption.txt"
    cap.write_text(caption_text(m), "utf-8")

    # datos.csv → para Canva Bulk Create (diseño editable dentro de Canva)
    write_csv([csv_row(m)], out / "datos.csv")

    return {"out": out, "pngs": pngs, "slides": len(slides), "chrome": bool(chrome)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--numero", type=int, help="genera el carrusel de un modelo")
    p.add_argument("--render", action="append", default=[], help="ruta a un render (repetible)")
    p.add_argument("--root", default=".")
    p.add_argument("--out")
    p.add_argument("--csv-todos", action="store_true", dest="csv_todos",
                   help="vuelca TODOS los modelos a build/biblioteca.csv (Canva Bulk Create)")
    a = p.parse_args()

    # Modo lote: un solo CSV con todos los modelos, para Bulk Create de una.
    if a.csv_todos:
        root = pathlib.Path(a.root)
        modelos = json.loads((root / "biblioteca.json").read_text("utf-8"))
        modelos.sort(key=lambda m: m["numero"], reverse=True)
        dest = write_csv([csv_row(m) for m in modelos], root / "build" / "biblioteca.csv")
        print(f"\n  CSV para Canva Bulk Create: {dest} ({len(modelos)} modelos)\n")
        return

    if a.numero is None:
        p.error("indica --numero N (o --csv-todos)")
    r = generar(a.numero, a.render, a.root, a.out)
    print(f"\n  Carrusel #{a.numero:03d}: {r['slides']} slides → {r['out']}")
    if r["chrome"]:
        print(f"  PNG renderizados: {len(r['pngs'])} (1080×1350, listos para postear)")
    else:
        print("  Chromium no disponible: slides dejados como HTML (captura manual).")
    print(f"  Caption: {r['out']}/caption.txt")
    print(f"  CSV Canva Bulk Create: {r['out']}/datos.csv\n")


if __name__ == "__main__":
    main()
