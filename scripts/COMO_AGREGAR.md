# Cómo agregar a la Biblioteca 3D

Guía rápida para sumar piezas. La fuente de verdad es `biblioteca.json`;
`biblioteca.html` se **regenera solo** con el script, no lo edites a mano.

---

## Los dos tipos de entrada

| Tipo | Cuándo usarlo | Qué necesitas |
|------|---------------|----------------|
| **link** 🔴 | Rápido. La pieza ya se descarga en otro sitio (marca, blog, etc.) | Link de descarga + imagen |
| **warehouse** 🔵 | Cuando TÚ subiste el bloque a tu 3D Warehouse | Link de 3D Warehouse + imagen + fuente |

---

## Receta 1 — Link directo (lo rápido) ⭐

```bash
python3 scripts/add_model.py \
  --tipo link \
  --nombre "NOMBRE DE LA PIEZA" \
  --url "https://link-de-descarga.com/..." \
  --imagen "/img/biblioteca/NOMBRE-ARCHIVO.jpg" \
  --categoria celosias \
  --fuente "Marca o autor"          # opcional en link
```

Mínimo imprescindible en un link: `--tipo link --nombre --url --imagen --categoria`.

## Receta 2 — Modelo en TU 3D Warehouse

```bash
python3 scripts/add_model.py \
  --nombre "NOMBRE DE LA PIEZA" \
  --url "https://3dwarehouse.sketchup.com/model/XXXX" \
  --imagen "/img/biblioteca/NOMBRE-ARCHIVO.jpg" \
  --categoria iluminacion \
  --fuente "Marca original" \
  --fuente-url "https://web-de-la-marca.com/..." \
  --tip "Un consejo corto y opcional para usar la pieza."
```

(Sin `--tipo` = warehouse por defecto.)

---

## Los 3 pasos, siempre iguales

1. **Sube la imagen** a `img/biblioteca/` con un nombre en minúsculas y guiones
   (ej. `wishbone-ch24.jpg`). Ese mismo nombre va en `--imagen`.
2. **Corre el comando** de la receta que toque.
3. **Guarda los cambios** (commit + push). Se regeneran solos `biblioteca.html`
   y el contador de modelos.

> Si solo quieres regenerar el HTML sin agregar nada:
> `python3 scripts/add_model.py --rebuild`

---

## Categorías válidas

`asientos` · `mesas` · `almacenaje` · `iluminacion` · `cocina` ·
`baño` · `exterior` · `decoracion` · `celosias`

**¿Categoría nueva?** Dos sitios (o pídemelo y lo hago yo):
1. En `scripts/add_model.py`, añádela a la lista `CATEGORIAS`.
2. En `biblioteca.html`, añade un botón en `<nav id="bibFiltros">`:
   `<button class="bib-filtro" data-f="minueva" aria-pressed="false">Mi Nueva</button>`

---

## Plantilla para ir juntando piezas (cópiala y ve llenando)

```
- Nombre:      
  Tipo:        link | warehouse
  Link:        
  Imagen:      img/biblioteca/________.jpg   (súbela con ese nombre)
  Categoría:   
  Fuente:      
  Fuente-URL:  
  Tip:         (opcional)
```

Cuando tengas varias llenas, me las pasas y las publico todas de una.
