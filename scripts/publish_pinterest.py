#!/usr/bin/env python3
"""
publish_pinterest.py — publica en Pinterest los modelos de la Biblioteca 3D.

Fuente de verdad: biblioteca.json (la misma que usa add_model.py).
Estado publicado: scripts/pinterest_state.json  (numero -> pin_id).
Solo se publican los modelos que TODAVÍA no tienen pin. Nunca se duplica.

No usa dependencias externas: solo la stdlib (urllib), así corre igual en
tu máquina y en GitHub Actions sin `pip install`.

────────────────────────────────────────────────────────────────────────
CONFIGURACIÓN (variables de entorno / secrets del repo)
────────────────────────────────────────────────────────────────────────
  PINTEREST_APP_ID         ID de tu app de Pinterest
  PINTEREST_APP_SECRET     Secret de tu app
  PINTEREST_REFRESH_TOKEN  Refresh token (dura ~1 año)
  PINTEREST_BOARD_ID       Tablero donde caen los pines
  SITE_BASE_URL            (opcional) por defecto https://darqdis.com

La guía para conseguir todo esto está en scripts/PINTEREST_SETUP.md

────────────────────────────────────────────────────────────────────────
USO
────────────────────────────────────────────────────────────────────────
  # ver qué se publicaría, sin tocar Pinterest ni el estado:
  python3 scripts/publish_pinterest.py --dry-run

  # publicar de verdad los modelos nuevos:
  python3 scripts/publish_pinterest.py

  # averiguar el ID de tu tablero (para PINTEREST_BOARD_ID):
  python3 scripts/publish_pinterest.py --list-boards

  # a dónde apunta cada pin al hacer clic:
  #   --link-mode biblioteca  (default) -> tu página de biblioteca
  #   --link-mode modelo               -> la descarga directa del modelo
"""

import argparse
import base64
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.pinterest.com/v5"

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_F = ROOT / "biblioteca.json"
STATE_F = pathlib.Path(__file__).resolve().parent / "pinterest_state.json"

# Nombre "bonito" de cada categoría para el texto del pin.
CAT_LABEL = {
    "asientos": "Asientos",
    "mesas": "Mesas",
    "almacenaje": "Almacenaje",
    "iluminacion": "Iluminación",
    "cocina": "Cocina",
    "baño": "Baño",
    "exterior": "Exterior",
    "decoracion": "Decoración",
    "celosias": "Celosías",
}


# ───────────────────────────── HTTP helpers ─────────────────────────────
def _request(method: str, url: str, headers: dict, data: bytes | None = None) -> dict:
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", "replace")
        sys.exit(f"ERROR Pinterest {e.code} en {method} {url}\n{detalle}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR de red hablando con Pinterest: {e.reason}")


def get_access_token(app_id: str, app_secret: str, refresh_token: str) -> str:
    """Cambia el refresh token (largo) por un access token (corto) al vuelo."""
    basic = base64.b64encode(f"{app_id}:{app_secret}".encode()).decode()
    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }).encode()
    headers = {
        "Authorization": f"Basic {basic}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    res = _request("POST", f"{API}/oauth/token", headers, data)
    token = res.get("access_token")
    if not token:
        sys.exit(f"ERROR: Pinterest no devolvió access_token: {res}")
    return token


def list_boards(token: str) -> list:
    headers = {"Authorization": f"Bearer {token}"}
    res = _request("GET", f"{API}/boards?page_size=100", headers)
    return res.get("items", [])


def create_pin(token: str, board_id: str, title: str, description: str,
               link: str, image_url: str) -> str:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = json.dumps({
        "board_id": board_id,
        "title": title[:100],
        "description": description[:800],
        "link": link,
        "media_source": {"source_type": "image_url", "url": image_url},
    }).encode()
    res = _request("POST", f"{API}/pins", headers, body)
    return res.get("id", "")


# ─────────────────────────── contenido del pin ──────────────────────────
def image_url_for(m: dict, base: str) -> str:
    """URL pública de la imagen, con los espacios/acentos bien escapados."""
    ruta = m["imagen"].lstrip("/")
    # Escapa cada segmento por separado para respetar las barras.
    ruta = "/".join(urllib.parse.quote(seg) for seg in ruta.split("/"))
    return f"{base.rstrip('/')}/{ruta}"


def pin_title(m: dict) -> str:
    n = f"{m['numero']:03d}"
    return f"#{n} · {m['nombre']}"


def pin_description(m: dict) -> str:
    cat = CAT_LABEL.get(m.get("categoria", ""), m.get("categoria", "").title())
    partes = [f"Modelo 3D para SketchUp · {cat}."]
    if m.get("fuente"):
        partes.append(f"Fuente: {m['fuente']}.")
    if m.get("tip"):
        partes.append(m["tip"])
    partes.append("Biblioteca 3D de darqdis — descarga gratis en darqdis.com/biblioteca")
    tags = f"#sketchup #3d #interiorismo #arquitectura #{m.get('categoria', 'diseno')}"
    return " ".join(partes) + "\n\n" + tags


def pin_link(m: dict, base: str, mode: str) -> str:
    if mode == "modelo":
        return m["url"]
    return f"{base.rstrip('/')}/biblioteca.html"


# ──────────────────────────────── estado ────────────────────────────────
def load_state() -> dict:
    if STATE_F.exists():
        return json.loads(STATE_F.read_text("utf-8"))
    return {}


def save_state(state: dict) -> None:
    STATE_F.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", "utf-8")


# ───────────────────────────────── main ─────────────────────────────────
def main() -> None:
    p = argparse.ArgumentParser(description="Publica la Biblioteca 3D en Pinterest.")
    p.add_argument("--dry-run", action="store_true",
                   help="muestra qué se publicaría, sin llamar a Pinterest ni tocar el estado")
    p.add_argument("--list-boards", action="store_true",
                   help="lista tus tableros con su ID y termina")
    p.add_argument("--link-mode", choices=["biblioteca", "modelo"], default="biblioteca",
                   help="a dónde lleva el pin al hacer clic (default: biblioteca)")
    p.add_argument("--base-url", default=os.environ.get("SITE_BASE_URL", "https://darqdis.com"))
    a = p.parse_args()

    app_id = os.environ.get("PINTEREST_APP_ID", "")
    app_secret = os.environ.get("PINTEREST_APP_SECRET", "")
    refresh = os.environ.get("PINTEREST_REFRESH_TOKEN", "")
    board_id = os.environ.get("PINTEREST_BOARD_ID", "")

    creds_ok = all([app_id, app_secret, refresh])

    # --list-boards: necesita credenciales sí o sí.
    if a.list_boards:
        if not creds_ok:
            sys.exit("ERROR: faltan PINTEREST_APP_ID / PINTEREST_APP_SECRET / "
                     "PINTEREST_REFRESH_TOKEN. Mira scripts/PINTEREST_SETUP.md")
        token = get_access_token(app_id, app_secret, refresh)
        boards = list_boards(token)
        if not boards:
            print("No tienes tableros todavía. Crea uno en pinterest.com y reintenta.")
            return
        print("\n  Tus tableros (usa el ID en PINTEREST_BOARD_ID):\n")
        for b in boards:
            print(f"    {b.get('id')}   {b.get('name')}")
        print()
        return

    modelos = json.loads(DATA_F.read_text("utf-8")) if DATA_F.exists() else []
    state = load_state()

    pendientes = [m for m in modelos if str(m["numero"]) not in state]
    pendientes.sort(key=lambda m: m["numero"])  # más antiguos primero

    if not pendientes:
        print("Nada nuevo que publicar. Todos los modelos ya tienen pin. ✓")
        return

    print(f"\n  Modelos sin pin: {len(pendientes)}")
    for m in pendientes:
        print(f"    · #{m['numero']:03d} {m['nombre']}")
    print()

    # Modo simulación: no necesita credenciales, ideal para revisar el texto.
    if a.dry_run:
        for m in pendientes:
            print("  ── DRY-RUN ─────────────────────────────────────────────")
            print(f"  título:  {pin_title(m)}")
            print(f"  imagen:  {image_url_for(m, a.base_url)}")
            print(f"  link:    {pin_link(m, a.base_url, a.link_mode)}")
            print(f"  texto:   {pin_description(m)}")
            print()
        print("  (dry-run: no se publicó nada ni se tocó el estado)\n")
        return

    if not creds_ok:
        sys.exit("ERROR: faltan credenciales de Pinterest. Corre con --dry-run para "
                 "revisar el texto, o configura los secrets (scripts/PINTEREST_SETUP.md).")
    if not board_id:
        sys.exit("ERROR: falta PINTEREST_BOARD_ID. Sácalo con --list-boards.")

    token = get_access_token(app_id, app_secret, refresh)

    publicados = 0
    for m in pendientes:
        pin_id = create_pin(
            token, board_id,
            title=pin_title(m),
            description=pin_description(m),
            link=pin_link(m, a.base_url, a.link_mode),
            image_url=image_url_for(m, a.base_url),
        )
        state[str(m["numero"])] = pin_id
        save_state(state)  # guarda tras cada pin: si algo falla, no re-publica lo hecho
        publicados += 1
        print(f"  ✓ Pin publicado: #{m['numero']:03d} {m['nombre']}  (pin {pin_id})")

    print(f"\n  Listo. {publicados} pin(es) nuevos en Pinterest.\n")


if __name__ == "__main__":
    main()
