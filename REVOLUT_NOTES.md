# Revolut application page — contexto y estado

Notas para retomar el trabajo de `revolut.html` desde cualquier dispositivo
(móvil vía `claude.ai/code` o la app de GitHub). Última actualización: **2026-07-02**.

---

## Qué es
`revolut.html` = página CV + portfolio de **Doménica Arias** para aplicar al rol
**Spatial & Interior Designer en Revolut**. Vive en la misma carpeta que el resto
del sitio darqdis.com pero es independiente: `noindex` y **sin enlace** desde el
menú de la home.

## Dónde verla (live)
- **https://darqdis.com/revolut** (URL limpia)
- también https://darqdis.com/revolut.html
- Subdominio `revolut.darqdis.com` → **pendiente** (ver más abajo).

---

## Cómo se publica (deploy)
Push a `main` en GitHub **`domearias/darqdis`** → **Netlify** publica solo en ~1–2 min.
- La web de verdad vive en la subcarpeta **`WEBSITE/`** del repo.
- Netlify site: `gregarious-sable-9e3803` (sirve darqdis.com).
- DNS en **Namecheap** (no en Netlify).
- Regla en `_redirects`: `/revolut` → `/revolut.html`.

**Regla de oro:** trabaja en un dispositivo a la vez y haz **push** antes de cambiar
de móvil ↔ PC, para no crear conflictos en git.

---

## Diseño (Revolut × darqdis)
Base editorial crema + Playfair de darqdis, con la marca Revolut encima.
- **Paleta** (variables CSS en el `<style>` de `revolut.html`):
  - Lila `#CACCFB` (bloques firma) · Mid Purple `#A7AAF8` · Accent Purple `#9539F2`
  - Deep Blue `#1326FD` (acento: chip nav, links, hovers, divisor CV)
  - Black `#161618` (tarjetas/secciones) · Lime `#BFFF37` (un solo pop en el footer)
- **Fuentes:** Space Grotesk (titulares) + Playfair Display (italics) + Archivo (cuerpo).
- Botones tipo píldora, tarjetas negras redondeadas, wordmark gigante.

## Estructura de la página
Nav (chip "Prepared for Revolut") → Hero → wordmark → **Video** → Pitch →
**Selected Work** (4 proyectos) → Manifesto → **CV** → Contacto → Footer.

---

## Imágenes (todas ya en la carpeta `WEBSITE/` y live)
| Uso | Archivo |
|---|---|
| Hero (SOLO esta página; la home usa `portrait.png`) | `portrait-2.png` |
| Proyecto 01 · Reforma en BCN | `reforma-bcn.jpg` |
| Proyecto 02 · Sisters Kitchen | `sisters-kitchen.jpg` |
| Proyecto 03 · Piza | `piza.jpg` |
| Proyecto 04 · Holy Cow | `holy-cow.jpg` |

Las tarjetas usan `onerror` → si falta el archivo, muestran placeholder (no se rompe).

## CV — contenido actual
**Experiencia:**
1. 2025 — Now · **LUV Studio, Barcelona** — Interior & Spatial Designer
2. 2023 — 2024 · **Bauden Architects** — Project Manager
3. 2022 — 2023 · **Marina Group, Ecuador** — Architect (Retail & Commercial)
4. 2021 — 2022 · **OMAH Creative Design** — Designer

**Educación:** Máster Interior Design · ELISAVA (2024) · Arquitectura · USFQ (2017–2022).
**Contacto:** hola@darqdis.com · +34 653 237 082 · LinkedIn · Instagram.

---

## PENDIENTE

### 1. Video de aplicación (vertical 9:16)
- Sección `#video` ya montada, esperando el archivo.
- **Acción:** subir el video a `WEBSITE/` con el nombre exacto **`revolut-application.mp4`**,
  luego commit + push. Mientras no exista, se ve un placeholder.
- (Opcional) portada: guardar `revolut-poster.jpg` y añadir `poster="revolut-poster.jpg"` al `<video>`.

### 2. Subdominio `revolut.darqdis.com` (opcional — el código ya está listo)
El redirect ya está pusheado; faltan 2 pasos manuales (requieren tus cuentas):
- **Netlify** → sitio `gregarious-sable-9e3803` → *Domain management* → *Add domain alias*
  → `revolut.darqdis.com`.
- **Namecheap** → darqdis.com → *Advanced DNS* → *Add New Record*:
  `CNAME` · Host `revolut` · Value `gregarious-sable-9e3803.netlify.app` · TTL Automatic.
- Al propagar (minutos–1h) Netlify emite el SSL y el subdominio cae directo en la página.
- Alternativa: quedarte con `darqdis.com/revolut` (ya funciona, es buena URL para la aplicación).

---

## Cómo retomar desde el móvil
1. Abre **`claude.ai/code`** en el navegador del móvil, inicia sesión.
2. Elige el repo **`domearias/darqdis`**, carpeta **`WEBSITE/`**.
3. Di algo como: *"seguimos con revolut.html, la página de aplicación a Revolut — lee REVOLUT_NOTES.md"*.
4. Pide los cambios; se commitean y hacen push → Netlify publica solo.
