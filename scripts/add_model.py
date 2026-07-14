#!/usr/bin/env python3
"""
add_model.py — añade un modelo a la Biblioteca 3D de darqdis.com

Fuente de verdad: biblioteca.json
La página biblioteca.html se REGENERA desde el JSON en cada ejecución,
así que las bandas ArquiLab siempre caen cada 6 cards sin desalinearse.

Uso:
  python scripts/add_model.py \
    --nombre "Sofá modular bouclé" \
    --url "https://3dwarehouse.sketchup.com/model/xxxx" \
    --imagen "img/biblioteca/sofa-boucle.jpg" \
    --categoria asientos \
    --tip "Guárdalo como componente antes de copiarlo."

Opciones:
  --root DIR     raíz del sitio (default: .)
  --rebuild      no añade nada, solo regenera el HTML desde el JSON
"""

import argparse
import html
import json
import pathlib
import sys

CATEGORIAS = [
    "asientos", "mesas", "almacenaje", "iluminacion",
    "cocina", "baño", "exterior", "decoracion",
]

GRID_START = "<!-- GRID:START -->"
GRID_END = "<!-- GRID:END -->"
COUNT_START = "<!-- COUNT:START -->"
COUNT_END = "<!-- COUNT:END -->"

ARQUILAB_URL = "https://pay.hotmart.com/L102711072Y?off=q5ahpkm3"
BANDA_CADA = 6


def card_html(m: dict) -> str:
    n = f"{m['numero']:03d}"
    nombre = html.escape(m["nombre"])
    cat = html.escape(m["categoria"])
    img = html.escape(m["imagen"])
    url = html.escape(m["url"])
    tip = html.escape(m.get("tip", ""))
    tip_block = f'\n          <p class="bib-card__tip">{tip}</p>' if tip else ""
    return f"""      <article class="bib-card reveal" data-cat="{cat}">
        <a class="bib-card__media" href="{url}" target="_blank" rel="noopener" aria-label="Descargar {nombre} en 3D Warehouse">
          <img src="{img}" alt="{nombre} — modelo 3D para SketchUp" loading="lazy">
        </a>
        <div class="bib-card__body">
          <span class="bib-card__kicker">#{n} &middot; <b>{cat}</b></span>
          <h3 class="bib-card__title">{nombre}</h3>{tip_block}
          <a class="bib-card__cta" href="{url}" target="_blank" rel="noopener">
            <span>Descargar en 3D&nbsp;Warehouse</span> <span class="arrow">&rarr;</span>
          </a>
        </div>
      </article>"""


def banda_html() -> str:
    return f"""      <aside class="bib-banda">
        <div>
          <p class="kicker">ArquiLab</p>
          <h3 class="bib-banda__title">Modelarlo ya está resuelto.<br><em>Ahora documéntalo.</em></h3>
        </div>
        <div>
          <p class="bib-banda__body">El 3D te lo llevas gratis. Los planos, las cotas y las láminas que entregas al cliente se hacen en Layout.</p>
          <a class="btn btn--oxblood" href="{ARQUILAB_URL}" target="_blank" rel="noopener" style="margin-top:1.4rem;">Aprender Layout <span class="arrow">&rarr;</span></a>
        </div>
      </aside>"""


def render_grid(modelos: list) -> str:
    if not modelos:
        return '      <p class="bib-empty">Los primeros modelos llegan esta semana.</p>'
    # más nuevo primero
    ordenados = sorted(modelos, key=lambda m: m["numero"], reverse=True)
    partes = []
    for i, m in enumerate(ordenados):
        partes.append(card_html(m))
        if (i + 1) % BANDA_CADA == 0 and (i + 1) < len(ordenados):
            partes.append(banda_html())
    return "\n".join(partes)


def splice(doc: str, start: str, end: str, contenido: str, etiqueta: str) -> str:
    a, b = doc.find(start), doc.find(end)
    if a == -1 or b == -1:
        sys.exit(f"ERROR: faltan los marcadores {etiqueta} en biblioteca.html")
    return doc[: a + len(start)] + "\n" + contenido + "\n" + doc[b:]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--nombre")
    p.add_argument("--url")
    p.add_argument("--imagen")
    p.add_argument("--categoria", choices=CATEGORIAS)
    p.add_argument("--tip", default="")
    p.add_argument("--root", default=".")
    p.add_argument("--rebuild", action="store_true")
    a = p.parse_args()

    root = pathlib.Path(a.root)
    data_f = root / "biblioteca.json"
    page_f = root / "biblioteca.html"

    if not page_f.exists():
        sys.exit(
            f"ERROR: no existe {page_f}\n"
            "Setup inicial: copia assets/biblioteca.html a la raíz del sitio."
        )

    modelos = json.loads(data_f.read_text("utf-8")) if data_f.exists() else []

    if not a.rebuild:
        faltan = [f for f in ("nombre", "url", "imagen", "categoria") if not getattr(a, f)]
        if faltan:
            sys.exit(f"ERROR: faltan argumentos: {', '.join('--' + f for f in faltan)}")

        if any(m["url"] == a.url for m in modelos):
            sys.exit("ERROR: ese link de 3D Warehouse ya está en la biblioteca.")

        numero = max((m["numero"] for m in modelos), default=0) + 1
        modelos.append({
            "numero": numero,
            "nombre": a.nombre,
            "url": a.url,
            "imagen": a.imagen,
            "categoria": a.categoria,
            "tip": a.tip,
        })
        data_f.write_text(json.dumps(modelos, ensure_ascii=False, indent=2), "utf-8")

    doc = page_f.read_text("utf-8")
    doc = splice(doc, GRID_START, GRID_END, render_grid(modelos), "GRID")
    doc = splice(doc, COUNT_START, COUNT_END, str(len(modelos)), "COUNT")
    page_f.write_text(doc, "utf-8")

    if a.rebuild:
        print(f"Regenerada la biblioteca. {len(modelos)} modelos.")
        return

    n = f"{modelos[-1]['numero']:03d}"
    print(f"\n  Publicado: MODELO #{n} — {a.nombre}")
    print(f"  Total en la biblioteca: {len(modelos)}")
    print(f"\n  Usa #{n} en la slide 1 del carrusel y en el caption.")
    print(f"  Commit sugerido: biblioteca: #{n} {a.nombre.lower()}\n")


if __name__ == "__main__":
    main()
