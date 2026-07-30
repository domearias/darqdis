---
name: biblioteca
description: >-
  Publica una pieza en la Biblioteca 3D de darqdis.com de principio a fin sin que
  el usuario tenga que tocar GitHub ni nombrar imágenes. Úsalo SIEMPRE que el
  usuario mande un link de 3D Warehouse (3dwarehouse.sketchup.com) o un link de
  descarga directa de un modelo/mueble/lámpara y diga cosas como "añádelo a la
  web", "súbelo a la biblioteca", "agrégalo", "ponlo en darqdis", o simplemente
  pegue el link a secas. También aplica cuando adjunta o pega la foto del
  producto para esa pieza. El skill deduce nombre/categoría/fuente, nombra la
  imagen solo, corre el script del repo, y hace commit + push + PR + merge para
  que quede publicado. No lo uses para cambios de diseño del sitio ni para otras
  páginas que no sean la biblioteca.
---

# Publicar en la Biblioteca 3D

La Biblioteca 3D (`biblioteca.html`) es una galería de piezas para SketchUp. La
**fuente de verdad es `biblioteca.json`**; el HTML y el contador se **regeneran
solos** con `scripts/add_model.py`. Nunca edites `biblioteca.html` a mano.

Tu trabajo con este skill es quitarle al usuario los dos dolores que odia:
**abrir GitHub** y **nombrar imágenes**. Él manda un link (y a veces una foto);
tú haces el resto y le confirmas que ya está publicado.

## El flujo, de un vistazo

1. Leer el link → deducir tipo, nombre y marca.
2. Calcular el número siguiente y el nombre de archivo de la imagen (automático).
3. Conseguir la imagen en disco con ese nombre (aquí está la única trampa).
4. Confirmar categoría y fuente en **una sola** pregunta corta.
5. Correr `scripts/add_model.py` (regenera HTML + contador).
6. Commit → push → PR → merge. Reportar que está en vivo.

Trabaja en la raíz del repo (donde está `biblioteca.json`).

---

## Paso 1 — Leer el link

- `https://3dwarehouse.sketchup.com/model/<uuid>/<SLUG>` → **tipo `warehouse`**.
- Cualquier otro link de descarga (marca, blog, etc.) → **tipo `link`**.

Deduce el **nombre** del SLUG: separa por guiones, quita el prefijo de marca si
lo hay, y pásalo a formato título. Ejemplos reales:

- `AND-COLUMN-FLOOR-175-4` → marca **A-N-D**, nombre **"Column Floor 175-4"**.
- `MINOTI-BLOCK-OUTDOOR` → marca **Minotti**, nombre **"Block Outdoor"**.

El SLUG es una pista, no un dogma: si el nombre resultante queda raro, propón el
que tenga sentido. La red del sandbox **bloquea 3dwarehouse.sketchup.com y las
webs de marca**, así que no intentes hacer `curl`/WebFetch de esas páginas para
sacar metadatos o la imagen: fallará con 403. Trabaja con el SLUG y con lo que
te diga el usuario.

## Paso 2 — Número y nombre de archivo (automático)

Lee `biblioteca.json`. El **número** nuevo es `max(numero) + 1`, a tres dígitos
(`005`, `006`, …). El **nombre de archivo** de la imagen se deriva solo:

```
img/biblioteca/<NNN>-<nombre-en-kebab>.jpg
```

Ej.: número 5 + "Column Floor 175-4" → `img/biblioteca/005-column-floor.jpg`
(kebab = minúsculas, sin acentos, palabras unidas por guiones; recorta a ~4
palabras si el nombre es largo). El usuario **nunca** nombra la imagen: lo haces
tú con esta regla.

## Paso 3 — Conseguir la imagen (el canal correcto)

La card se ve rota si el archivo no existe, así que la foto tiene que quedar en
disco con el nombre del Paso 2. Aquí está la única trampa real, y está
**confirmada por pruebas** en este entorno:

> **En Claude Code web, las imágenes que el usuario pega O adjunta con el clip
> NO llegan al disco.** Me llegan solo como contenido visual; no queda ningún
> fichero que pueda commitear. No pierdas tiempo buscándolas en el filesystem:
> no están. Además, la red del sandbox **solo deja pasar GitHub** (Drive, Imgur,
> googleusercontent, webs de marca… todo da 403), y bajar la foto por el MCP de
> Google Drive tampoco sirve: la entrega en base64 y una foto de varios MB no
> cabe para reescribirla a disco. **Los bytes de la foto solo pueden entrar por
> GitHub.**

Por eso el flujo es: **el usuario sube la foto al repo por GitHub con el nombre
que sea** (una sola acción de arrastrar-y-soltar), y tú te encargas del resto:
detectarla, renombrarla sola y publicar. El usuario nunca nombra la imagen.

Cómo tomar la foto que el usuario subió:

1. **Trae el repo actualizado** (la subida del usuario es un commit nuevo):
   `git fetch origin && git pull` en la rama donde subió (normalmente `main`).

2. **Localiza la foto nueva.** Es un archivo de imagen dentro de `img/biblioteca/`
   que **todavía no está referenciado** en `biblioteca.json` (esos son los que
   ya están catalogados). Si hay una sola imagen sin catalogar, esa es. Si hay
   varias, o dudas, pregúntale al usuario cuál corresponde a esta pieza. Verifícala
   con la herramienta Read (muestra la imagen) antes de confiar.

3. **Renómbrala al nombre canónico** del Paso 2 con `git mv` y usa ese path en el
   Paso 5. Normaliza rarezas de la subida: doble extensión (`005-x.jpg.jpg`),
   espacios, mayúsculas. Si la foto real es `.png` y no `.jpg`, deja la extensión
   real y usa esa en el campo `imagen`.

**Si el usuario aún no subió foto** (solo la pegó, o quiere ir publicando):
genera un **placeholder de marca** con el nombre canónico para que la card no se
vea rota. Cuando después suba la foto real con ese mismo nombre, la sobrescribe
sin tocar nada más. Recuérdale que la única vía para la foto es subirla a
`img/biblioteca/` por GitHub (con cualquier nombre; tú la renombras).

```bash
pip install Pillow --quiet   # si hace falta
python3 .claude/skills/biblioteca/scripts/placeholder.py \
  --nombre "Column Floor 175-4" --categoria iluminacion --fuente "A-N-D" \
  --salida "img/biblioteca/005-column-floor.jpg"
```

La card es 4:3 y recorta al centro (`object-fit: cover`); una foto vertical se
recorta arriba y abajo, normalmente sin problema. Menciónalo si la foto es muy
apaisada o muy vertical, por si el usuario prefiere recortarla él.

## Paso 4 — Categoría y fuente (una sola pregunta)

Categoría y fuente no salen fiables del link, y meter datos equivocados es peor
que preguntar una vez. Haz **una** pregunta compacta (AskUserQuestion) con tu
mejor apuesta como opción por defecto:

- **Categoría** (obligatoria). Válidas: `asientos` · `mesas` · `almacenaje` ·
  `iluminacion` · `cocina` · `baño` · `exterior` · `decoracion` · `celosias`.
  (Una lámpara de pie → `iluminacion`; una estantería → `almacenaje`; etc.)
- **Fuente** (marca/autor). Deriva del SLUG y confírmala.

Si ya te dieron ambas en el mensaje, no preguntes: sigue.

Sobre `fuente_url`: **déjala vacía salvo que el usuario te dé el enlace exacto**
o estés seguro de que existe. No inventes rutas tipo `marca.com/PRODUCTO`: la red
está bloqueada y no puedes verificar que no den 404. Sobre `tip`: es opcional; no
te lo inventes, déjalo vacío si no tienes un consejo real de uso de la pieza.

## Paso 5 — Añadir con el script del repo

Corre el script; regenera `biblioteca.html` y el contador solo, y ordena las
cards con la más nueva primero:

```bash
python3 scripts/add_model.py \
  --nombre "Column Floor 175-4" \
  --url "https://3dwarehouse.sketchup.com/model/<uuid>/<SLUG>" \
  --imagen "/img/biblioteca/005-column-floor.jpg" \
  --categoria iluminacion \
  --fuente "A-N-D"            # para tipo warehouse la fuente es obligatoria
# --tipo link                 # añádelo si es descarga directa (fuente opcional)
# --fuente-url "..."          # solo si lo conoces con certeza
```

Verifica rápido que el JSON tiene la entrada nueva y que `biblioteca.html`
apunta a la imagen correcta (`grep <NNN>-<slug> biblioteca.html biblioteca.json`).

## Paso 6 — Publicar sin que el usuario toque GitHub

El sitio se sirve de `main` (GitHub Pages). Publica tú el cambio entero:

1. Rama de trabajo corta, p.ej. `git checkout -B biblioteca/<NNN>-<slug>`
   (o la rama que ya te haya indicado la sesión).
2. `git add -A && git commit` con un mensaje tipo
   `biblioteca: #<NNN> <nombre en minúsculas>`.
3. `git push -u origin <rama>` (reintenta con backoff si falla por red).
4. Abre el PR hacia `main` con las herramientas de GitHub (`create_pull_request`)
   y **mergéalo** (`merge_pull_request`, squash). Recuerda el pie de atribución
   de Claude Code en cualquier comentario/PR que escribas.
5. Confirma al usuario: pieza **#NNN publicada**, y que GitHub Pages republica
   darqdis.com/biblioteca en un par de minutos.

Si la foto todavía es el placeholder, díselo claramente y recuérdale cómo mandar
la definitiva (adjunta como archivo, con lo cual la subes tú; o por el link de
subida de GitHub con el mismo nombre de archivo).

---

## Reglas rápidas

- Nunca edites `biblioteca.html` a mano; siempre pasa por `add_model.py`.
- El nombre de la imagen lo pones tú (Paso 2); el usuario no nombra nada.
- Imágenes pegadas **o adjuntas con el clip** = no hay archivo en disco. La foto
  solo entra subiéndola al repo por GitHub (con cualquier nombre; tú la renombras).
- `fuente_url` y `tip`: vacíos salvo dato real. No inventes.
- Una sola pregunta al usuario (categoría/fuente) y solo si no los dio ya.
- Cierra el ciclo: no lo dejes en "pendiente de mergear" salvo que falte la foto
  real; el objetivo es que quede en vivo.
