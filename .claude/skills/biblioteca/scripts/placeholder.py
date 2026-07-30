#!/usr/bin/env python3
"""
placeholder.py — genera una imagen provisional de marca para una card de la
Biblioteca 3D, para que la card nunca se vea rota mientras llega la foto real.

Usa la paleta del brandbook (bone / oxblood / oliva / tinta) y el formato 4:3
que pide `.bib-card__media`. La foto definitiva se sube luego con el MISMO
nombre de archivo y sobrescribe este placeholder.

Uso:
  python3 placeholder.py \
    --nombre "Column Floor 175-4" \
    --categoria iluminacion \
    --fuente "A-N-D" \
    --salida "img/biblioteca/005-column-floor.jpg"

Requiere Pillow (pip install Pillow).
"""

import argparse
import pathlib

from PIL import Image, ImageDraw, ImageFont

# Paleta del brandbook (_meta/BRANDBOOK.html)
BONE = (240, 237, 230)      # #F0EDE6
INK = (26, 23, 20)          # #1A1714
OLIVE = (110, 106, 77)      # #6E6A4D
OXBLOOD = (92, 46, 38)      # #5C2E26

# Fuentes del sistema (DejaVu/Liberation vienen en el contenedor).
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def _font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _centrar(draw, text, font, y, fill, width):
    bb = draw.textbbox((0, 0), text, font=font)
    draw.text(((width - (bb[2] - bb[0])) / 2, y), text, font=font, fill=fill)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--nombre", required=True)
    p.add_argument("--categoria", default="")
    p.add_argument("--fuente", default="")
    p.add_argument("--salida", required=True)
    a = p.parse_args()

    W, H = 1200, 900  # 4:3, el aspect-ratio de la card
    img = Image.new("RGB", (W, H), BONE)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=OXBLOOD)  # filete superior

    f_kick = _font(SANS, 30)
    f_title = _font(SERIF_BOLD, 92)
    f_sub = _font(SERIF_ITALIC, 40)
    f_note = _font(SANS, 26)

    # Kicker: "FUENTE  —  CATEGORIA"
    partes = [x for x in (a.fuente.strip(), a.categoria.strip().upper()) if x]
    if partes:
        _centrar(d, "  —  ".join(partes), f_kick, 300, OLIVE, W)

    # Título en dos líneas si es largo, para que no se salga.
    palabras = a.nombre.split()
    if len(a.nombre) > 16 and len(palabras) > 1:
        mid = len(palabras) // 2 + len(palabras) % 2
        lineas = [" ".join(palabras[:mid]), " ".join(palabras[mid:])]
    else:
        lineas = [a.nombre]
    y = 360
    for ln in lineas:
        _centrar(d, ln, f_title, y, INK, W)
        y += 100

    _centrar(d, "modelo 3D · SketchUp", f_sub, y + 30, OXBLOOD, W)
    d.line([(W / 2 - 120), y + 105, (W / 2 + 120), y + 105], fill=OLIVE, width=2)
    _centrar(d, "Imagen en camino", f_note, y + 140, OLIVE, W)

    out = pathlib.Path(a.salida)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=90)
    print(f"placeholder -> {out}")


if __name__ == "__main__":
    main()
