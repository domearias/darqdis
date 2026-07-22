#!/usr/bin/env python3
"""
publicar.py — UN comando para publicar un modelo de la Biblioteca 3D.

Hace, en un solo paso, todo lo que antes era manual:
  1. Copia tu render a img/biblioteca/ con un nombre limpio (slug).
  2. Lo añade a biblioteca.json y regenera biblioteca.html (vía add_model.py).
  3. Genera el carrusel de Instagram (PNG 1080×1350 listos) + el caption.
  4. (opcional) commit + push → sale en vivo en darqdis.com.

Flujo pensado para el celu/cloud: subes el modelo a 3D Warehouse, copias su
link, y le pasas a Claude el link + tu render + la categoría. Claude corre:

  python scripts/publicar.py \
    --url  "https://3dwarehouse.sketchup.com/model/xxxx/Follow-Me" \
    --nombre "Follow Me" \
    --render ~/Downloads/follow-me.jpg \
    --categoria iluminacion \
    --fuente "Marset" --fuente-url "https://www.marset.com/..." \
    --tip "Bájale la resolución de la malla antes de repetirla por la escena." \
    --commit

--render se puede repetir (varios ángulos → más slides en el carrusel).
El primer --render es el que va a la card del sitio.
Sin --commit, deja todo listo para que revises antes de publicar.
"""

import argparse
import pathlib
import re
import subprocess
import sys
import unicodedata

CATEGORIAS = [
    "asientos", "mesas", "almacenaje", "iluminacion",
    "cocina", "baño", "exterior", "decoracion",
]
SCRIPTS = pathlib.Path(__file__).parent


def slugify(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t or "modelo"


def run(cmd, **kw):
    return subprocess.run(cmd, **kw)


def main():
    p = argparse.ArgumentParser(description="Publica un modelo en la Biblioteca 3D (todo en uno).")
    p.add_argument("--url", required=True, help="link del modelo en 3D Warehouse")
    p.add_argument("--nombre", required=True)
    p.add_argument("--render", action="append", required=True,
                   help="ruta a un render (repetible; el 1º va a la card del sitio)")
    p.add_argument("--categoria", required=True, choices=CATEGORIAS)
    p.add_argument("--fuente", required=True, help="marca/autor original (el crédito)")
    p.add_argument("--fuente-url", default="", dest="fuente_url")
    p.add_argument("--tip", default="")
    p.add_argument("--root", default=".")
    p.add_argument("--commit", action="store_true", help="git add + commit + push")
    p.add_argument("--no-carrusel", action="store_true", help="solo biblioteca, sin carrusel")
    a = p.parse_args()

    root = pathlib.Path(a.root).resolve()

    # 1) copiar el primer render a img/biblioteca/<slug>.<ext>
    renders = [pathlib.Path(r).expanduser() for r in a.render]
    for r in renders:
        if not r.exists():
            sys.exit(f"ERROR: no existe el render {r}")
    slug = slugify(a.nombre)
    ext = renders[0].suffix.lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".webp"):
        ext = ".jpg"
    dest_rel = f"img/biblioteca/{slug}{ext}"
    dest_abs = root / dest_rel
    dest_abs.parent.mkdir(parents=True, exist_ok=True)
    if renders[0].resolve() != dest_abs.resolve():
        dest_abs.write_bytes(renders[0].read_bytes())

    # 2) añadir a biblioteca.json + regenerar biblioteca.html
    add = [
        sys.executable, str(SCRIPTS / "add_model.py"),
        "--nombre", a.nombre,
        "--url", a.url,
        "--imagen", "/" + dest_rel,
        "--categoria", a.categoria,
        "--fuente", a.fuente,
        "--root", str(root),
    ]
    if a.fuente_url:
        add += ["--fuente-url", a.fuente_url]
    if a.tip:
        add += ["--tip", a.tip]
    res = run(add, capture_output=True, text=True)
    sys.stdout.write(res.stdout)
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        sys.exit("ERROR: add_model.py falló (¿link duplicado?).")

    # número asignado = máximo actual
    import json
    modelos = json.loads((root / "biblioteca.json").read_text("utf-8"))
    numero = max(m["numero"] for m in modelos)

    # 3) carrusel + caption
    carpeta = None
    if not a.no_carrusel:
        sys.path.insert(0, str(SCRIPTS))
        import carrusel
        render_paths = [str(dest_abs)] + [str(r) for r in renders[1:]]
        r = carrusel.generar(numero, render_paths, root=str(root))
        carpeta = r["out"]
        print(f"  Carrusel: {r['slides']} slides", end="")
        print(f" · {len(r['pngs'])} PNG listos" if r["chrome"] else " (HTML, sin Chromium)")
        print(f"  Caption:  {carpeta}/caption.txt")

    # 4) commit + push (opcional)
    if a.commit:
        n = f"{numero:03d}"
        run(["git", "-C", str(root), "add", "-A"])
        msg = f"biblioteca: #{n} {a.nombre.lower()}"
        run(["git", "-C", str(root), "commit", "-m", msg])
        push = run(["git", "-C", str(root), "push"], capture_output=True, text=True)
        if push.returncode == 0:
            print(f"\n  ✓ Publicado y pusheado: #{n} {a.nombre}")
        else:
            sys.stderr.write(push.stderr)
            print(f"\n  ⚠ Commit hecho pero el push falló. Revisa la red y reintenta 'git push'.")
    else:
        print(f"\n  Todo listo (sin publicar). Revisa el carrusel y luego:")
        print(f"    git add -A && git commit -m 'biblioteca: #{numero:03d} {a.nombre.lower()}' && git push")

    if carpeta:
        print(f"\n  → Sube a Instagram los PNG de {carpeta} y pega el caption.")


if __name__ == "__main__":
    main()
