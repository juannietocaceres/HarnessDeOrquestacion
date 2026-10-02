---
name: presentaciones-visuales
description: Convierte una idea, documento, esquema, transcripción o deck existente en una presentación HTML autocontenida (un archivo en `presentaciones/<slug>.html`) con narrativa clara, navegación por teclado y exportable a PDF. Se activa cuando hay que crear, convertir o mejorar slides, un deck o material para exponer en una reunión, clase, charla, pitch o video.
---

# Presentaciones visuales

Armas presentaciones HTML de un solo archivo, con una narrativa clara y una
legibilidad que aguante una sala con proyector, una videollamada o un PDF
impreso. Esta skill se ocupa de **qué se cuenta y en qué orden**, de la
**estructura de cada slide** y de las **reglas de legibilidad**; la
dirección estética la decide `frontend-design` (ver "Precedencia").

## Precedencia con `frontend-design`

Las dos skills se usan juntas. Cuando dicen cosas distintas, manda esto:

| Tema | Quién decide |
|---|---|
| Paleta, tipografía, concepto visual, evitar plantillas genéricas | `frontend-design` |
| Narrativa, cantidad y orden de slides, una idea por slide | esta skill |
| Tamaños mínimos de letra, límites de texto por slide, contraste, impresión | esta skill |
| Guía de marca del usuario o del brief | el usuario, por encima de las dos |

Contradicciones ya resueltas (no las reabras en cada deck):

- **Números grandes**: solo si el dato *es* el mensaje de la slide (por
  ejemplo, "2 de 5 tareas necesitaron a una persona"). Nunca como
  decoración de una estadística secundaria, ni la combinación "número
  enorme + etiqueta chica + acento en degradé" por defecto.
- **Emojis e íconos**: solo si aportan información que el texto no da (un
  ícono que distingue categorías que el público tiene que reconocer de un
  vistazo). Nunca como relleno al lado de cada punto.
- **Numeración**: el contador de slides ("3 / 10") siempre va, porque un
  deck es una secuencia. Los marcadores numerados *dentro* de una slide
  (01 / 02 / 03) solo si el contenido es un proceso o una línea de tiempo.
- **Movimiento**: como máximo un momento de animación orquestado por slide,
  y solo cuando ayuda a seguir la idea. Un escalonado (stagger) se permite
  solo dentro de un grupo de elementos relacionados (por ejemplo, los pasos
  de un proceso que aparecen uno tras otro); nunca una cascada decorativa de
  secciones o bloques, ni efectos al pasar el mouse sobre cada bloque.
- **Tarjetas y degradés**: está bien una grilla de tarjetas si la jerarquía
  se nota (no todas iguales, con el mismo radio y la misma sombra). Fondo
  liso por defecto; un degradé solo si representa algo del tema.

## Modo de trabajo: interactivo o dentro de un sub-agente

- **Sesión con el usuario**: si falta información crítica (público,
  objetivo, duración), pregunta antes de generar. Si no es crítica, asume
  lo razonable y sigue.
- **Dentro de un sub-agente del orquestador**: no preguntes nunca. Asume lo
  razonable, lista los supuestos al principio del "Resumen de enfoque" y
  sigue. Si un supuesto es de alto impacto (cambia el público, el mensaje
  central o algo que el usuario va a mostrar en público), termina el turno
  devolviendo un `DECISION_NEEDED` con el formato de `orquestador/SKILL.md`
  §6, sin entregar el deck a medias.
- Lo mismo aplica cuando `frontend-design` pide "confirmar con el cliente"
  el tema o el público: en un sub-agente, se asume y se lista.

---

## Proceso paso a paso

### 1. Analizá el input

Lee el contenido o la idea. Extrae:
- **Tema y objetivo** de la presentación
- **Público** (si se puede inferir)
- **Cantidad aproximada de slides**
- **Tono**: formal, divulgativo, comercial, educativo, técnico...
- **Uso previsto**: reunión, video, clase, capacitación, pitch, propuesta
- **Guion**: si existe un guion hablado para este deck (por ejemplo,
  `GUION-PRESENTACION.md`), las notas del presentador salen de ahí, y la
  estructura de slides debería coincidir con la del guion.

Ante información faltante, sigue "Modo de trabajo" (arriba).

### 2. Define la estructura narrativa

Toda presentación tiene un arco claro:

| Sección | Propósito |
|---|---|
| Apertura / portada | Captar atención, enmarcar el tema |
| Contexto / problema | Por qué importa esto |
| Desarrollo | El contenido principal, las ideas clave |
| Ejemplos o datos | Prueba, evidencia, caso real |
| Cierre / conclusión | Resumen o llamada a la acción |

Adapta este esquema al tipo de presentación: un pitch no es lo mismo que
una capacitación.

### 3. Elige un estilo visual

El estilo de partida sale de esta tabla; la paleta y la tipografía
concretas las define `frontend-design` (su plan de tokens y su lista de
clichés aplican tal cual). Si el usuario trae marca, colores o estilo
propios, se respetan por encima de todo.

| Estilo | Cuándo usarlo |
|---|---|
| Profesional minimalista | Propuestas, reuniones corporativas |
| Tecnológico / oscuro | IA, producto digital, startups |
| Educativo / claro | Capacitaciones, clases, explicaciones |
| Premium / editorial | Marca personal, consultoría |
| Creativo | Agencias, diseño, contenido |
| Corporativo | Empresas grandes, informes internos |

**Fuentes**: por defecto, el stack del sistema. Google Fonts está permitido
siempre que se declare un fallback del sistema en el mismo `font-family`,
para que el deck se siga leyendo bien sin conexión.

### 4. Reglas de diseño que se aplican siempre

**Estructura visual:**
- Una sola idea principal por slide
- Jerarquía clara: título → subtítulo → contenido → nota opcional
- Márgenes amplios, espacio en blanco generoso
- Letra legible: mínimo 16px para el cuerpo (en la práctica, 20px o más
  en un lienzo de 1280×720), 28–48px para títulos
- Nada de texto desbordado: todo entra en un lienzo de 1280×720

**Variedad de layouts.** No repitas el mismo layout en todas las slides.
Combina, según lo que pida el contenido:
- Slide centrada con título grande + frase
- Dos columnas (concepto + explicación)
- Bloques o tarjetas con jerarquía visible
- Lista corta
- Dato clave (solo si el dato es el mensaje, ver "Precedencia")
- Línea de tiempo o proceso en pasos
- Comparación entre dos opciones
- Cierre con llamada a la acción o frase fuerte

**Elementos visuales permitidos:**
- Íconos SVG inline cuando aportan información
- Diagramas SVG inline (flujos, grafos) dibujados con el mecanismo real
- Bloques de color para destacar conceptos clave
- Barra de progreso o contador de slides

**Prohibido:**
- Párrafos largos en una slide
- Más de 5–6 puntos en una lista
- Colores sin coherencia con la paleta definida
- Imágenes externas (no hay garantía de que carguen)
- Estilo infantil, salvo pedido expreso

### 5. Genera el HTML y escríbelo a disco

La salida es **un único archivo HTML autocontenido** en
`presentaciones/<slug>.html` (crear la carpeta si no existe). El HTML no se
pega en el chat.

Requisitos técnicos:
- CSS y JS dentro del mismo archivo (`<style>`, `<script>`); sin
  dependencias externas salvo Google Fonts con fallback.
- Lienzo fijo de 1280×720 escalado al tamaño de la ventana, para que lo
  que se verifica sea lo que se proyecta.
- Navegación con ← → (también Re Pág / Av Pág, espacio, Inicio / Fin) y
  botones visibles con `aria-label`; foco de teclado visible.
- Contador de slides visible ("3 / 10") y, si suma, barra de progreso.
- `@media print`: una slide por página (`@page` del tamaño del lienzo,
  `break-after: page`), sin botones ni contador flotante, para exportar a
  PDF desde el navegador.
- `@media (prefers-reduced-motion: reduce)`: sin transiciones ni
  animaciones.
- Notas del presentador opcionales en `<aside class="notas">` dentro de
  cada slide, ocultas por defecto; la tecla `N` las muestra u oculta. No se
  imprimen.

Estructura mínima:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nombre de la presentación</title>
  <style>
    :root { /* tokens de color y tipografía del plan de frontend-design */ }
    /* lienzo 1280×720 + escalado, slides, navegación, notas */
    @media print { /* una slide por página */ }
    @media (prefers-reduced-motion: reduce) { /* sin movimiento */ }
  </style>
</head>
<body>
  <main class="deck">
    <section class="slide" aria-label="Slide 1 de N">
      ...
      <aside class="notas">Lo que dice el presentador en esta slide.</aside>
    </section>
  </main>
  <nav><!-- botones anterior / siguiente + contador --></nav>
  <script>/* teclado, botones, contador, tecla N, #hash por slide */</script>
</body>
</html>
```

### 6. Presentaciones para video

Si el deck es para video o pantalla:
- Frases muy cortas, una por slide
- Elementos grandes, tipografía al tamaño máximo cómodo
- Fondo liso (degradé solo si significa algo, ver "Precedencia")
- Máximo 3 puntos por slide
- Un único momento de animación por slide (puede ser un escalonado dentro
  de un grupo relacionado, ver "Precedencia"), siempre respetando
  `prefers-reduced-motion`

### 7. Presentaciones para reunión o clase

Si el uso es reunión, clase o capacitación:
- Claridad y orden por encima de la espectacularidad
- Puede llevar más contenido por slide que en video
- Contador de slides visible
- Notas del presentador si el usuario las pide o si existe un guion

---

## Checklist obligatorio antes de entregar

No es opcional ni se cumple "invocándolo de nombre": cada punto se
comprueba sobre el HTML final. Salen de lo que falló en el deck anterior
del harness (ver `PROCESO.md` §11).

1. **Contraste.** Toda combinación de texto y fondo que aparece en el deck
   da ≥ 4.5:1 (≥ 3:1 solo para texto de 24px o más, o 18.66px en negrita).
   Se comprueba en **cada** fondo donde se usa un color: si un acento
   aparece sobre fondo claro y sobre fondo oscuro, se definen dos variantes
   del mismo color, una por fondo. Para calcularlo:
   `python .claude/skills/presentaciones-visuales/scripts/contraste.py "#texto" "#fondo" ...`
2. **Clichés.** Busca y elimina los patrones que lista `frontend-design`,
   en especial:
   - etiquetas tipo "PALABRA — fragmento" con guion largo;
   - metadatos unidos con punto medio ("A · B · C");
   - una etiqueta en mayúsculas (eyebrow) arriba de cada título;
   - una sola palabra del título resaltada en otro color o en cursiva;
   - "→" pegado al texto de botones o enlaces;
   - grilla de tarjetas idénticas con la misma sombra gris.
   Una búsqueda de texto de ` · `, ` — ` y `text-transform: uppercase` en
   el HTML ayuda, pero no reemplaza mirar cada slide.
3. **Lenguaje llano.** Relee cada slide preguntando "¿esto lo entiende
   alguien que no escribió el sistema?". Reemplaza la jerga interna por la
   metáfora del propio tema (por ejemplo, "tandas, como las olas" en vez
   de "waves con cap de concurrencia").
4. **Datos.** Si el deck cita cifras o afirmaciones verificables, invoca
   `verificador-datos` antes de entregar. Si esa skill no está disponible,
   verifica a mano cada cifra contra su fuente (el repo, el documento de
   origen) y no inventes ninguna: si falta un dato, dilo.
5. **Desborde e impresión.** Ningún texto se sale de su slide a 1280×720,
   y la vista de impresión da exactamente una slide por página. Si el
   entorno permite capturas (por ejemplo, Chrome headless con
   `--window-size=1280,720`), mira cada slide; si no, di explícitamente
   que no se verificó.

---

## Formato de salida en el chat

El HTML queda en disco; en el chat va solo esto:

**Resumen de enfoque:**
> Objetivo, público asumido, estilo visual elegido y por qué. Si corres
> dentro de un sub-agente, también la lista de supuestos.

**Estructura de slides:**
> Lista numerada con el título de cada slide.

**Archivo:**
> Ruta `presentaciones/<slug>.html` y cómo abrirlo (doble clic; `N` para
> notas; Ctrl+P para PDF).

**Recomendaciones opcionales:**
> Ajustes de marca, logos o mejoras que el usuario podría aplicar.

---

## Casos especiales

**Si el usuario trae un documento o transcripción larga:** extrae las ideas
principales; no intentes meter todo el texto en las slides. Resume,
prioriza, jerarquiza.

**Si el usuario trae un PowerPoint o esquema:** respeta la estructura y los
mensajes clave, pero mejora el diseño y la jerarquía visual.

**Si el usuario no da estilo:** elige el más adecuado al tema, explícalo
brevemente en el resumen de enfoque y úsalo de forma coherente.

**Si el usuario da una guía de marca:** colores, fuentes y tono de la marca
van por encima de cualquier otra preferencia de diseño, incluida
`frontend-design`. El checklist de contraste sigue aplicando: si un color
de marca no llega a 4.5:1 sobre un fondo, úsalo solo en texto grande o
como color de fondo, y dilo en las recomendaciones.

**Si el contenido necesita datos o fuentes que no tienes:** indica
claramente qué datos faltan. No inventes cifras.
