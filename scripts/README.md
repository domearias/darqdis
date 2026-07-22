# Biblioteca 3D — publicar en un comando

Objetivo: subes un modelo a tu perfil de **3D Warehouse** y, con **un solo
comando**, se actualiza `darqdis.com/biblioteca` **y** se genera el carrusel de
Instagram (imágenes + caption) listo para postear.

## El flujo (desde el celu o la compu)

1. Subes el modelo a **3D Warehouse** y copias su link.
2. Guardas tu render (el que usaste para 3DW — tu propia imagen, en alta).
3. Le pasas a Claude (o corres tú) **un comando**:

```bash
python scripts/publicar.py \
  --url "https://3dwarehouse.sketchup.com/model/xxxx/Follow-Me" \
  --nombre "Follow Me" \
  --render ~/Downloads/follow-me.jpg \
  --categoria iluminacion \
  --fuente "Marset" --fuente-url "https://www.marset.com/follow-me" \
  --tip "Bájale la resolución de la malla antes de repetirla por la escena." \
  --commit
```

Eso hace **todo**:

- Copia tu render a `img/biblioteca/` con nombre limpio.
- Lo añade a `biblioteca.json` y regenera `biblioteca.html`.
- Genera el **carrusel** en `build/carrusel-NNN/` — slides PNG **1080×1350**
  on-brand + `caption.txt`.
- Con `--commit`: `git commit` + `push` → sale en vivo en darqdis.com.

Luego solo subes los PNG de `build/carrusel-NNN/` a Instagram y pegas el caption.

> Trabajando con Claude en el celu: dile *"sube este modelo a la biblioteca"* +
> el link + adjunta el render + la categoría. Claude corre el comando y te manda
> los PNG del carrusel de vuelta al chat.

## Opciones útiles

| Flag | Para qué |
|------|----------|
| `--render` (repetible) | Varios ángulos → más slides de imagen en el carrusel. El 1º va a la card del sitio. |
| `--categoria` | `asientos · mesas · almacenaje · iluminacion · cocina · baño · exterior · decoracion` |
| `--fuente` / `--fuente-url` | El **crédito** al autor original (obligatorio: la biblioteca es curada, no modelada por ti). |
| `--tip` | Consejo corto de uso → se vuelve un slide y va en el caption. |
| `--commit` | Publica (commit + push). Sin él, deja todo listo para que revises antes. |
| `--no-carrusel` | Solo actualiza la biblioteca, sin generar el carrusel. |

## Estructura del carrusel

Portada oscura (render a sangre + nombre + #NNN) → slides de más renders (si
pasas varios) → slide de *tip* (si hay) → cierre beige con CTA "Link en bio".
Sigue las plantillas del BRANDBOOK §09 (Playfair + Archivo, paleta y ritmo).

## Editar los carruseles dentro de Canva (Bulk Create)

Si quieres que el carrusel sea **editable en Canva** (no una imagen plana), usa
**Bulk Create** (función de Canva Pro). El pipeline ya te deja el CSV listo:

- Por modelo: `build/carrusel-NNN/datos.csv`
- Todos de una: `python scripts/carrusel.py --csv-todos` → `build/biblioteca.csv`

Setup **una sola vez** en Canva:

1. Crea una plantilla de carrusel 1080×1350 con tu marca (Playfair + Archivo,
   paleta). Deja campos de texto para: **nombre, numero, categoria, tip, cta,
   handle, dominio** y un marcador de **imagen** para el render.
2. **Apps → Bulk Create → subir CSV.** Sube `datos.csv` (o `biblioteca.csv`).
3. Conecta cada columna a su campo (la columna `render` es una **URL pública**
   de darqdis.com → Canva jala la imagen sola).
4. **Generar** → cada carrusel sale como diseño **nativo y 100% editable**.

> Ojo: importar el PNG a Canva NO es editable (entra como imagen plana). Para
> editar de verdad dentro de Canva hay que ir por Bulk Create con el CSV.
> El `render` debe estar ya **pusheado** para que su URL pública exista.

## Scripts

- **`publicar.py`** — orquestador. El comando que usas normalmente.
- **`add_model.py`** — motor de la biblioteca (JSON → HTML). Lo llama `publicar.py`.
- **`carrusel.py`** — generador de slides + caption + `datos.csv`. Lo llama
  `publicar.py`. También `--csv-todos` para volcar todos los modelos a un CSV.
- **`assets/fonts/`** — Playfair + Archivo cacheadas (los PNG salen idénticos
  a la marca sin depender de red).

## Notas

- **Carpeta `build/`** está en `.gitignore`: los PNG del carrusel son salida
  para postear, no assets del sitio.
- **Requiere Chromium** para renderizar los PNG. En el entorno cloud de Claude
  ya viene instalado. En local (Windows) sin Chromium, deja los slides como
  HTML individuales para capturar a mano.
- **3D Warehouse no se puede raspar** (bloquea bots). Por eso pasas el nombre y
  tu render — que además es mejor calidad que la miniatura de 3DW.
