# Auto-publicar la Biblioteca 3D en Pinterest

Cada modelo que agregas a la biblioteca puede convertirse **solo** en un Pin de
tu cuenta de Pinterest. Lo hace `scripts/publish_pinterest.py`, y el workflow
`.github/workflows/pinterest.yml` lo dispara cada vez que cambia
`biblioteca.json` en `main`.

- **Fuente de verdad:** `biblioteca.json` (la misma de siempre).
- **Qué se publica:** solo los modelos que aún no tienen pin.
- **Anti-duplicados:** `scripts/pinterest_state.json` guarda `numero → pin_id`.
  Un modelo ya publicado nunca se vuelve a publicar.

> Mientras no configures los secrets, el sitio y el flujo de la biblioteca
> siguen funcionando igual. El paso de Pinterest simplemente no publica nada
> hasta que le des acceso.

---

## Paso 1 — Crear la app de Pinterest (una sola vez)

1. Entra a **https://developers.pinterest.com/apps/** con tu cuenta.
2. **Connect app** / **Create app**. Ponle un nombre (ej. `darqdis biblioteca`).
3. Cuando esté creada, anota:
   - **App ID**
   - **App secret**
4. En la configuración de la app, agrega una **Redirect URI**. Sirve para el
   paso 2; vale cualquiera que controles, por ejemplo:
   `https://darqdis.com/` (o `https://localhost/`).
5. Pide/activa los **scopes**: `boards:read`, `pins:read`, `pins:write`.

---

## Paso 2 — Conseguir el refresh token (una sola vez)

El refresh token dura ~1 año y se renueva solo en cada publicación.

**2.1** Abre esta URL en el navegador (reemplaza `APP_ID` y, si cambiaste la
redirect, `REDIRECT_URI`):

```
https://www.pinterest.com/oauth/?client_id=APP_ID&redirect_uri=https://darqdis.com/&response_type=code&scope=boards:read,pins:read,pins:write
```

Autoriza. Pinterest te redirige a `https://darqdis.com/?code=XXXX...`.
Copia el valor de **`code`** de la barra de direcciones.

**2.2** Cambia ese `code` por el refresh token (pega tu App ID, secret y code):

```bash
APP_ID="tu_app_id"
APP_SECRET="tu_app_secret"
CODE="el_code_de_la_url"
REDIRECT="https://darqdis.com/"

curl -s -X POST https://api.pinterest.com/v5/oauth/token \
  -u "$APP_ID:$APP_SECRET" \
  -d grant_type=authorization_code \
  -d code="$CODE" \
  --data-urlencode redirect_uri="$REDIRECT"
```

En la respuesta JSON copia **`refresh_token`**.

---

## Paso 3 — Elegir el tablero

Con el refresh token ya puedes preguntar tus tableros. En tu compu, en la raíz
del repo:

```bash
export PINTEREST_APP_ID="..."
export PINTEREST_APP_SECRET="..."
export PINTEREST_REFRESH_TOKEN="..."
python3 scripts/publish_pinterest.py --list-boards
```

Copia el **ID** del tablero donde quieres que caigan los pines
(ej. tu tablero "Biblioteca 3D"). Si no tienes uno, créalo en pinterest.com.

---

## Paso 4 — Guardar los secrets en GitHub

En el repo: **Settings → Secrets and variables → Actions → New repository secret**.
Crea estos cuatro:

| Secret | Valor |
|---|---|
| `PINTEREST_APP_ID` | App ID del paso 1 |
| `PINTEREST_APP_SECRET` | App secret del paso 1 |
| `PINTEREST_REFRESH_TOKEN` | refresh token del paso 2 |
| `PINTEREST_BOARD_ID` | ID del tablero del paso 3 |

Listo. A partir de aquí, cada push que cambie `biblioteca.json` publica los
modelos nuevos en Pinterest automáticamente.

---

## Cómo se ve un Pin

- **Imagen:** la misma de la card (`img/biblioteca/…`, servida desde darqdis.com).
- **Título:** `#004 · Travertine Base and Wood Shelves`
- **Texto:** categoría + fuente + tip + llamada a tu web + hashtags.
- **Link (al hacer clic):** tu página `darqdis.com/biblioteca.html`.
  Para que apunte a la descarga directa del modelo, corre el script con
  `--link-mode modelo` (o cambia el default en `publish_pinterest.py`).

---

## Probar sin publicar (recomendado la primera vez)

`--dry-run` te muestra exactamente el texto de cada pin **sin** tocar Pinterest
ni el estado, y **no** necesita credenciales:

```bash
python3 scripts/publish_pinterest.py --dry-run
```

## Publicar a mano (sin esperar al workflow)

```bash
export PINTEREST_APP_ID="..."
export PINTEREST_APP_SECRET="..."
export PINTEREST_REFRESH_TOKEN="..."
export PINTEREST_BOARD_ID="..."
python3 scripts/publish_pinterest.py
```

---

## Preguntas rápidas

**¿Republica lo que ya estaba?** No. Solo modelos sin entrada en
`pinterest_state.json`. Los 4 modelos actuales se publicarán la primera vez que
corra con credenciales; a partir de ahí, solo los nuevos.

**¿Y si quiero re-publicar uno?** Borra su línea en
`scripts/pinterest_state.json` y vuelve a correr.

**¿Se rompe algo si no configuro Pinterest?** No. El workflow intenta publicar,
no encuentra credenciales y termina sin error visible en tu sitio. La web y
`add_model.py` siguen igual.
