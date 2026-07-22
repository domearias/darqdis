# darqdis.com — RESUMEN VIVO DEL PROYECTO

> **Para Claude:** lee este archivo al iniciar cada sesión en vez de releer el chat (ahorra créditos). **Actualízalo al final de cada avance.**
> **Para Doménica:** este es el estado real del sitio, las decisiones y lo pendiente.
>
> **Última actualización:** 2026-07-22
>
> 📘 **Brand Book visual:** abre `BRANDBOOK.html` (en esta misma carpeta) — logo, color, tipografía, componentes, voz, y **plantillas de carrusel**. Es la referencia de diseño para el sitio Y para las redes.

---

## 1. QUÉ ES Y DÓNDE VIVE

- Sitio de **Doménica Arias** — arquitecta, retail & interior designer (Quito / Barcelona) + **ArquiLab** (su curso de SketchUp + Layout).
- **Carpeta de trabajo (repo):** `G:\Mi unidad\01 DOMENICA\01 ARQUITECTURA\10 DARQDIS\01 WEBSITE\WEBSITE\`
- **Deploy:** git push a `main` → GitHub `domearias/darqdis` → **GitHub Pages** (auto-deploy). Dominio **darqdis.com** (DNS en Namecheap). No hay Netlify.
- **Publicar = `git push origin main`** desde la carpeta `WEBSITE\`. Sale en vivo en ~1–2 min.
- **Google Analytics:** gtag `G-GLL4M44JNR` en todas las páginas.

## 2. PÁGINAS (todas en vivo)

| URL | Archivo | Qué es |
|-----|---------|--------|
| `/` | index.html | **Home** — embudo de ArquiLab (público: estudiantes) |
| `/arquilab` | arquilab.html | Página de ventas del curso |
| `/proyectos` | proyectos.html | Portafolio índice — **fondo oscuro** (público: clientes/estudios) |
| `/proyecto?p=slug` | proyecto.html | Ficha individual (slugs: sisters-kitchen, piza, holy-cow). **NO TOCAR** — usa paleta vieja (cream) a propósito |
| `/biblioteca` | biblioteca.html | Buscador de modelos 3D curados |
| `/contacto` | contacto.html | Página de contacto |
| ocultas | revolut.html, application/, coming-soon.html | Sin enlazar, noindex |

## 3. SISTEMA VISUAL (reglas duras)

- **Tipografía:** Playfair Display (títulos serif) + **Archivo peso 400** (texto). Base **17px** (`html { font-size: 106.25% }`). NO usar Archivo 300 (se ve delgada/pequeña).
- **Ritmo de fondos** (todas las páginas menos /proyectos que es todo oscuro):
  - **Blanco `#FAFAF7`** = fondo por defecto (dominante) — token `--bone`
  - **Beige `#F0EDE6`** = acento, solo algunas bandas — token `--beige`
  - **Espresso `#1A1714`** = impacto (resultados, oferta, footer) — token `--espresso`
  - **REGLA: nunca 3 secciones seguidas del mismo tono.**
- **Acentos:**
  - **Oxblood `#5C2E26`** = **acento de marca + dinero** (actualizado 2026-07-22). Úsalo libre como acento editorial: itálicas de títulos (sobre fondos claros), números, comillas, líneas, detalles. Sigue siendo el color del dinero. **Guardrail:** el BOTÓN sólido oxblood se reserva para comprar (Hotmart); acciones gratis = botón neutro. **Contraste:** sobre fondo espresso el oxblood no se lee → ahí el acento va claro.
  - **Olivo `#6E6A4D`** = detalle estructural (punto del logo, algunos kickers, bordes activos). No en botón ni fondo grande.
- **Texto:** `--ink #111009` (principal), `--ink-soft #3D3830` (secundario).
- **Nav uniforme en TODAS las páginas:** logo `doménica.arqdis` + **ArquiLab · Proyectos · Biblioteca · Contacto** + botón **Inscríbete** (oxblood). Todo lleva a páginas (nunca scroll interno). Sin scroll-spy (no cambia de color al hacer scroll). Logo → `/`.

## 4. ARQUILAB — CÓMO SE VENDE

- **Ángulo héroe = EFICIENCIA / recuperar el tiempo.** No vender "láminas bonitas" (eso es consecuencia).
- **Metodología 3D** (su mayor activo): **Definir · Diseñar · Detallar.** Un solo flujo SketchUp + Layout, de la idea a los planos ejecutivos, con checkpoints con el cliente.
- **Prueba:** proyecto de 3 semanas → 2 fines de semana. "Dos sueldos al mes". Reemplaza 5 programas por uno.
- **Historia:** BN → OMA → Neo → Marina → Bauden → independiente en Barcelona (máster en negocios, Elisava, beca).
- **Precio:** $180 USD. Cupón general `HELLOARQUI` = 10% off. Garantía Hotmart 7 días. Link: `https://pay.hotmart.com/L102711072Y?off=q5ahpkm3`
- **Embajadora:** Gabriela Calvera (bloque destacado en resultados): PDF de su Passion Project (Drive `1BzwWLFsGThelwfVi9QvoANHvtUXBWf3E`), IG `@gabriela.calvera.arq`, cupón **GABYARQUILAB** (10%, precargado con `&coupon=GABYARQUILAB`). Patrón replicable para más embajadoras.
- **Masterclass gratis:** YouTube `PFnLW7rxm_g`.
- **Mockups del Passion Project de Domenica:** `/00.png`–`/04.png` (03 en el hero, resto en galería).

## 5. BIBLIOTECA 3D

- Es un **buscador curado**: modelos rehospedados de terceros (Marset, Minotti…), **NO modelados por Doménica**. Cada card acredita su **fuente**. Nunca decir que ella los modeló.
- Datos en `biblioteca.json`. Modelos: **#001 Pace Pendant** (A-N-D), **#002 Minotti Block Outdoor**.
- **Publicar = UN comando** (`scripts/publicar.py`): copia el render → añade a `biblioteca.json` + regenera `biblioteca.html` → genera el **carrusel de IG en PNG 1080×1350** + `caption.txt` → (con `--commit`) push. Ver `scripts/README.md`.
  - Desde el celu con Claude: *"sube este modelo"* + link de 3DW + adjunta el render + categoría → Claude corre el comando y devuelve los PNG.
  - 3D Warehouse NO se puede raspar (bloquea bots) → siempre pasas el nombre + tu render propio (mejor calidad que la miniatura de 3DW de todos modos).
  - Instagram: flujo **listo-para-postear** (auto todo menos el toque final de "publicar"). Auto-post 100% vía Graph API quedó como opción futura (necesita cuenta IG business + app de Meta + token que se renueva c/60 días).

## 6. CONTENIDO / TESTIMONIOS

- **SIEMPRE usar mensajes REALES** de la carpeta de DMs de Doménica en Drive (folder `1-hr5xT4SiQK1Adddog3DbFaCMpPPwh4K`). Nunca inventar nombres/handles.
- Doménica **prefiere screenshots** de los DMs (más creíbles) sobre texto transcrito.
- Los DMs son anónimos (sin @ visible) → atribuir por rol + "nombres reservados por privacidad".
- Capturas ya usadas en /arquilab (`img/arquilab/`): dm-passion, dm-capa, dm-cliente.
- Foto oficial de Doménica: `portrait-transparente.png` (blazer negro, fondo transparente) — en hero del home y en "Quién te va a enseñar".

## 6.b TRABAJAR DESDE EL CELULAR / REMOTO

- **Este resumen y el brand book viven ahora en `WEBSITE/_meta/`** (dentro del repo). GitHub los guarda pero GitHub Pages NO los publica (Jekyll ignora carpetas que empiezan con `_`, y no hay `.nojekyll`). Así viajan con el repo a cualquier dispositivo. (La carpeta vieja `01 WEBSITE/_RESUMEN_DARQDIS/` quedó como copia; se puede borrar.)
- **Desde el celu:** abrir **claude.ai/code** en el navegador (o la app de Claude), entrar con la misma cuenta, y abrir el repo `domearias/darqdis`. Se trabaja sobre el mismo sitio; al hacer commit + push, se despliega igual a darqdis.com.
- **Ojo:** la versión web/cloud trabaja desde el **repo de GitHub**, no desde los archivos locales de la unidad G:. Todo lo que el sitio necesita está en el repo (por eso movimos el resumen a `_meta/`). Archivos sueltos en el Drive local (que no estén en el repo) no se ven desde el celu.

## 7. TRUCOS TÉCNICOS

- **Bajar imágenes grandes de Drive:** `curl -sL "https://drive.google.com/uc?export=download&id=FILEID" -o archivo` (funciona si el archivo es público por enlace). Verificar firma PNG/JPG. NO usar el MCP de Drive para binarios grandes (satura el contexto).
- **Leer texto de screenshots de DMs:** el MCP de Drive (`search_files`) ya devuelve el texto OCR en `contentSnippet`.

## 8. PREFERENCIAS DE DOMÉNICA (cómo trabajar)

- Publicar rápido e **iterar en vivo** (salvo que pida revisar antes).
- Textos con **impacto, no muy largos**.
- Fuentes: le gusta Playfair + Archivo; le molestan las tipografías "muy de IA/template".
- Testimonios: reales, con screenshots.
- **Mantener este RESUMEN.md actualizado** cada vez que se avanza.

## 8.b GENERACIÓN DE CARRUSELES / POSTS (flujo)

Doménica envía inspo + info → Claude genera carruseles on-brand (ver plantillas en `BRANDBOOK.html` §09).
- Formato **4:5 (1080×1350)**. Portada oscura (gancho) → 3–6 slides claros (valor, numerados) → cierre beige con CTA ("link en bio").
- Playfair en titulares, Archivo en cuerpo, paleta y reglas de acento del brand book. 1 idea por slide, títulos cortos, mucho aire.
- Se generan como HTML/slides que Doménica exporta como imágenes (o se ajustan juntas antes).
- **Carruseles de biblioteca**: automatizados por `scripts/carrusel.py` (lo llama `publicar.py`). Renderiza los slides a PNG 1080×1350 con Chromium + tipografía de marca incrustada. Portada oscura (render + #NNN) → tip → cierre beige CTA.

## 9. PENDIENTES / BUGS CONOCIDOS

- ⚠️ **Minotti #002:** falta subir `img/biblioteca/minoti-block-outdoor.png` al repo → imagen rota en vivo hasta que Doménica la suba.
- ⚠️ **Cupón GABYARQUILAB:** verificar en el checkout de Hotmart que el descuento se aplique solo con el link (la oferta debe tener el cupón activado en Hotmart).
- Encuadre de la foto en el hero/about: revisar en vivo, calibrable con `object-position`.
- `font-pairings.html` (comparador de fuentes) está en la carpeta pero NO se publica.

## 10. LOG DE AVANCES (breve, cronológico)

- **2026-07-14:** refactor v3 de index.html (bloques A–D): limpieza, tokens, estructura del home (Problema→Solución→Resultados→Biblioteca→Contacto).
- **2026-07-22:** /proyectos nuevo (work-row, oscuro); arreglados links rotos; cascada de tokens a biblioteca/arquilab; ritmo de color blanco/beige/oscuro; nav uniforme + /contacto; scroll-spy eliminado; **copy de ArquiLab reescrita (eficiencia + Metodología 3D + historia)**; embajadora Gaby; foto real; **DMs como screenshots**; tipografía Archivo 400 + base 17px. Todo publicado.
- **2026-07-22 (fin de sesión):** creado este RESUMEN.md + **BRANDBOOK.html** (brand book visual v1) en la carpeta `_RESUMEN_DARQDIS`. Tipografía marcada como provisional. Definido el flujo de generación de carruseles.
- **2026-07-22:** **automatización de la Biblioteca 3D** — `scripts/publicar.py` (un comando: render → biblioteca.json/html → carrusel PNG 1080×1350 + caption → push). Nuevos: `carrusel.py`, `scripts/README.md`, fuentes de marca cacheadas en `scripts/assets/fonts/`. `build/` en gitignore. Flujo listo-para-postear.
- **2026-07-22:** regla de **oxblood ampliada** (acento de marca, no solo dinero). Aplicado al sitio: itálicas de títulos en secciones claras pasan de gris a oxblood (las oscuras se quedan claras). Guardrail: botón sólido oxblood sigue reservado a CTAs de compra. Publicado.
