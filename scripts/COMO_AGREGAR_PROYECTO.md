# Cómo añadir un proyecto al portafolio (solo renders)

El portafolio tiene dos piezas:

- `proyectos.html` — la lista principal (la parrilla de proyectos con foto + texto).
- `proyecto.html` — la página de detalle que se abre al dar click. Es **una sola
  página** que se rellena sola según el `?p=<slug>` de la URL, leyendo el objeto
  `DATA` que está dentro del propio archivo.

Añadir un proyecto son **3 pasos**. No hace falta duplicar páginas ni tocar CSS.

---

## 1. Sube los renders

Crea una carpeta con el nombre corto (slug) del proyecto y mete ahí tus renders:

```
img/proyectos/<slug>/01.jpg
img/proyectos/<slug>/02.jpg
img/proyectos/<slug>/03.jpg
...
```

- El `slug` es el nombre en minúsculas y con guiones: `casa-turo`, `loft-eixample`, etc.
- Elige el mejor render como **principal** (será el hero a pantalla completa). Puede
  ser uno de los mismos (ej. `01.jpg`) o uno aparte tipo `hero.jpg`.
- Formato recomendado: **JPG**, horizontal si es posible, máx ~1600 px de ancho para
  que pese poco. (Los de la biblioteca se optimizan a ~1400 px / JPG; mismo criterio.)

## 2. Añade la entrada en `proyecto.html`

Abre `proyecto.html`, busca `var DATA = {` y añade tu proyecto. Copia esta plantilla:

```js
'casa-turo': {
  name: 'Casa <em>Turó</em>',            // <em> pone la palabra en cursiva
  type: 'Residencial · Interiorismo', typeEn: 'Residential', year: '2025',
  loc: 'Barcelona, España', locShort: 'Barcelona, ES',
  role: 'Interiorismo · Render', area: 'Vivienda',
  hero: 'img/proyectos/casa-turo/01.jpg',        // render principal (pantalla completa)
  gallery: [                                     // el resto de renders
    'img/proyectos/casa-turo/02.jpg',
    'img/proyectos/casa-turo/03.jpg',
    'img/proyectos/casa-turo/04.jpg'
  ],
  conceptTitle: 'Un apartamento <em>mediterráneo</em>',
  conceptLead: 'Frase corta que resume la idea del proyecto.',
  conceptEs: 'Párrafo en español sobre el concepto, materiales, atmósfera…',
  conceptEn: 'Same paragraph in English (optional but recomendado).',
  quote: 'Cita del cliente. Puedes resaltar algo <em>así</em>.',
  clientName: 'Nombre del cliente', clientRole: 'Cliente · Residencial'
}
```

Luego añade el slug al array `ORDER` (controla el orden y el botón
"siguiente proyecto"):

```js
var ORDER = ['sisters-kitchen', 'piza', 'holy-cow', 'casa-turo'];
```

> Las secciones de **Plano**, **Boceto** y **Materiales** se ocultan solas mientras
> no las definas, así que un proyecto solo con renders queda limpio, sin recuadros
> vacíos. Si algún día quieres mostrarlas, avísame y las activamos.

## 3. Añade la fila en `proyectos.html`

En `proyectos.html`, dentro de `<main class="work">`, copia un bloque
`<article class="work-row">` existente y cámbialo. Lo importante:

```html
<article class="work-row reveal">
  <div class="work-row__body">
    <p class="work-row__num">04</p>                          <!-- número correlativo -->
    <h2 class="work-row__name">Casa <em>Turó</em></h2>
    <p class="work-row__hook">Una frase gancho del proyecto.</p>
    <p class="work-row__desc">Descripción de 2–3 líneas.</p>
    <div class="work-row__foot">
      <span class="work-row__tags">Residencial · Barcelona · 2025</span>
      <a href="/proyecto?p=casa-turo" class="work-row__link">Ver proyecto <span class="arrow">→</span></a>
    </div>
  </div>
  <a href="/proyecto?p=casa-turo" class="work-row__media" aria-label="Ver Casa Turó">
    <img src="img/proyectos/casa-turo/01.jpg" alt="Casa Turó — interiorismo, Barcelona">
  </a>
</article>
```

> El `?p=casa-turo` debe coincidir **exactamente** con el slug del `DATA`.

---

## Resumen mental

```
slug  →  carpeta img/proyectos/<slug>/ con renders
      →  entrada en DATA (proyecto.html) + añadir a ORDER
      →  fila <article> en proyectos.html
```

Con eso el proyecto aparece en la lista y, al dar click, se abre su detalle con el
render grande arriba y la galería de renders debajo.
