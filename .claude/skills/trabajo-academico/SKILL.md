---
name: trabajo-academico
description: Estructura y redacta borradores de documentos universitarios (anteproyecto, informe, artículo, ensayo, trabajo de grado) con objetivos medibles, norma de citación fija por proyecto y solo referencias verificadas, y los exporta a Word con pandoc. Se usa en tareas `tipo: academico` o cuando hay que escribir un documento para la universidad.
---

# Trabajo académico

Armas documentos universitarios con la estructura correcta, objetivos bien
formulados y **referencias reales**. Estructuras, redactas borradores y
verificas fuentes; el contenido final lo revisa y lo asume el estudiante.

Material de apoyo en esta carpeta:

- [ESTRUCTURAS.md](ESTRUCTURAS.md): secciones de cada tipo de documento.
- [CHECKLIST-APA7.md](CHECKLIST-APA7.md): revisión de formato y citas APA 7.

## Modo de trabajo: interactivo o dentro de un sub-agente

- **Sesión con el usuario**: si falta algo crítico (tipo de documento,
  tema, programa, norma, lineamientos del docente), pregúntalo antes de
  escribir. Lo no crítico lo asumes y lo listas.
- **Dentro de un sub-agente del orquestador**: no preguntes nunca. Asume lo
  razonable y lista los supuestos en tu reporte. Si el supuesto es de alto
  impacto (faltan lineamientos de un documento formal, la norma no está
  fijada y el programa podría exigir otra), termina el turno con un
  `DECISION_NEEDED` en el formato de `orquestador/SKILL.md` §6, sin
  entregar el documento a medias.

## 1. Qué manda sobre qué

De mayor a menor prioridad:

1. **`docs/academico/lineamientos.md`** del proyecto: guía del programa,
   modalidad de grado, formato que exige el docente. Si existe, manda sobre
   todo lo de esta skill (estructura, norma, extensión, portada).
2. **El manifest**: campo `norma_citacion:` de la tarea (`apa7 | icontec`).
3. **Esta skill**: estructuras de `ESTRUCTURAS.md` y norma por defecto
   (sección 3).

Si el documento es **formal** (anteproyecto, trabajo de grado) y no existe
`lineamientos.md`, no asumas el formato de la institución: pídelo
(`DECISION_NEEDED` dentro de un sub-agente, pregunta directa en sesión).
Para documentos de clase (informe, ensayo) puedes seguir con la estructura
de `ESTRUCTURAS.md` y anotar el supuesto.

## 2. Proceso

1. **Identifica el tipo de documento** y toma su estructura de
   `ESTRUCTURAS.md` (o la de `lineamientos.md`, si existe).
2. **Fija la norma de citación** (sección 3). Una sola por documento.
3. **Escribe el esqueleto** en `academico/<slug>/documento.md` con todas
   las secciones del tipo. Lo que todavía no tiene contenido queda como
   `[POR COMPLETAR: qué va aquí]`, no como relleno genérico.
4. **Formula los objetivos** con las reglas de la sección 4.
5. **Busca y verifica las referencias** con las reglas de la sección 5.
   Cada una entra a `referencias.bib` solo después de verificarla.
6. **Corre `verificador-datos`** sobre todas las referencias y las
   afirmaciones que se apoyan en ellas (sección 5).
7. **Revisa el formato** con `CHECKLIST-APA7.md` (o el checklist de la
   norma fijada).
8. **Exporta** a Word si hay pandoc (sección 6).
9. **Reporta** qué secciones son borrador para revisión humana (sección 7).

## 3. Norma de citación

| Campo | Valor |
|---|---|
| Norma por defecto | **APA 7** (decisión §7.3 confirmada; cambiable por proyecto) |
| Alternativa | ICONTEC (NTC 1486 y normas asociadas) |
| Dónde se fija | `norma_citacion:` en la tarea del manifest, o en `lineamientos.md` |

- **Una norma por documento, nunca mezcladas.** Si el manifest dice una y
  `lineamientos.md` otra, manda `lineamientos.md` y lo anotas en el
  reporte.
- **APA 7**: el formato de las citas y de la lista de referencias lo pone
  pandoc con `apa.csl` (sección 6); tú revisas con `CHECKLIST-APA7.md` lo
  que el CSL no controla (portada, títulos, tablas, márgenes).
- **ICONTEC**: el repositorio oficial de estilos CSL
  (`citation-style-language/styles`) no trae un estilo ICONTEC al momento
  de escribir esta skill. Antes de usar un CSL de terceros, busca uno de
  fuente confiable (biblioteca universitaria, repositorio con autor
  identificable) y anota de dónde salió y la fecha de consulta. Si no hay
  uno confiable, exporta sin CSL de ICONTEC y aplica el formato con un
  checklist manual basado en la guía que entregue el programa
  (`lineamientos.md`); si tampoco hay guía, es `DECISION_NEEDED`.

## 4. Objetivos bien formulados

- **Un objetivo general y de 3 a 5 específicos.**
- Cada uno empieza con **un verbo en infinitivo medible** (taxonomía de
  Bloom): identificar, describir, comparar, clasificar, analizar,
  construir, diseñar, implementar, evaluar, validar, estimar.
- **Prohibidos los verbos vagos**: conocer, entender, comprender, saber,
  aprender, explorar (sin decir qué se produce), profundizar.
- **Un verbo por objetivo.** "Analizar y diseñar..." son dos objetivos.
- **Cada específico se liga a un entregable o actividad de la
  metodología.** En el documento, deja una tabla objetivo → actividad →
  entregable. Un específico sin actividad que lo cumpla, o una actividad
  sin objetivo, es una señal de que algo sobra o falta.
- El general responde la pregunta de investigación; los específicos son
  los pasos para llegar a él, no objetivos más chicos sueltos.

## 5. Referencias: regla dura contra inventarlas

- **Solo entran fuentes verificadas**: DOI que resuelve en
  `https://doi.org/<doi>`, URL que existe, o libro con ISBN comprobado.
- **Verificar es comprobar los metadatos**, no solo que el enlace abra:
  título, autores, año, revista, volumen y páginas contra la fuente
  (`https://api.crossref.org/works/<doi>`, la página de la editorial,
  Europe PMC o el catálogo con el ISBN). Lo que escribes en
  `referencias.bib` sale de ahí, no de memoria.
- **Lo que afirmas con una cita debe estar en la fuente.** Si la apoyas
  en el resumen, léelo; no le atribuyas a un artículo algo que solo
  supones que dice.
- **Si no encuentras fuente** para una afirmación, escribe en el texto
  `[CITA PENDIENTE: qué hace falta respaldar]`. Nunca una referencia
  aproximada, "probable" o reconstruida de memoria.
- Las referencias viven en **`referencias.bib`** (BibTeX) dentro de la
  carpeta del documento. En el texto se citan con `[@clave]`.
- Corre **`verificador-datos`** sobre cada referencia y cada afirmación
  que se apoya en ella. El resultado esperado es **0 incorrectas y 0
  inventadas**; una ❌ no se entrega, se corrige o se reemplaza por
  `[CITA PENDIENTE: ...]`.
- Fuentes de datos (portales de datos abiertos, sistemas de vigilancia)
  se mencionan con su URL comprobada; si el acceso a los datos o su
  licencia no está confirmado, va como `verificacion_manual`.

## 6. Formato de trabajo y exportación

Se escribe en **Markdown** con citas `[@clave]` y un bloque YAML al
inicio (`title`, `author`, `date`, `lang`, `bibliography`). El estilo de
citas **no** va en el YAML: el comando de abajo pasa siempre el `apa.csl`
de la skill con `--csl` (un `csl:` en el YAML apuntaría a un archivo que no
existe junto al documento).

Export a Word con **pandoc** (gratis):

```
pandoc documento.md --citeproc --bibliography referencias.bib --csl .claude/skills/trabajo-academico/apa.csl --reference-doc .claude/skills/trabajo-academico/plantilla-apa7.docx -o documento.docx
```

(Desde la carpeta del documento, con rutas absolutas o relativas a la
skill. En PowerShell, `$skill = "<repo>\.claude\skills\trabajo-academico"`
y `--csl "$skill\apa.csl" --reference-doc "$skill\plantilla-apa7.docx"`.)

- **`plantilla-apa7.docx`** (en esta carpeta) trae los estilos APA 7:
  Times New Roman 12, interlineado doble, sin espacio entre párrafos,
  sangría de primera línea de 1,27 cm en el texto (`Body Text`,
  `First Paragraph`), título y `Heading 1` en negrita centrados,
  `Heading 2` en negrita a la izquierda, tablas (`Compact`) a espacio
  sencillo sin sangría, márgenes de 1 in (2,54 cm) y papel carta. Pandoc
  solo toma sus estilos, no su contenido. Sin `--reference-doc` el Word
  sale con el estilo por defecto de pandoc (Aptos, títulos grandes): no
  es APA.
- **`apa.csl`** (en esta carpeta) formatea citas y referencias. Viene del
  repositorio oficial de estilos CSL
  (`https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl`,
  licencia CC BY-SA 3.0, anotada en el propio archivo). No se descarga
  por documento.
- Sin `--citeproc` las citas quedan crudas (`[@clave]`) y no se arma la
  lista de referencias.
- **Si pandoc no está instalado**, entrega el Markdown igual y deja el
  comando de instalación. Según la página oficial
  (`https://pandoc.org/installing.html`):
  - Windows: `winget install --source winget --exact --id JohnMacFarlane.Pandoc`
    (o `choco install pandoc`).
  - macOS: `brew install pandoc`.
  - Linux: el paquete `pandoc` de la distribución.
  Los comandos de instalación cambian: confírmalos en esa página al
  usarlos y anota la fecha.
- **`.docx` y `.pdf` se producen con pandoc.** Las skills `docx` y `pdf` de
  `anthropics/skills` no se vendorizan: su licencia (propietaria, "All
  rights reserved") prohíbe copiarlas, redistribuirlas y crear obras
  derivadas (decisión §7.4). Solo se enlazan como referencia externa:
  https://github.com/anthropics/skills/tree/main/skills/docx y
  https://github.com/anthropics/skills/tree/main/skills/pdf.
- Si la institución da su propia plantilla (o pide ICONTEC), se pasa esa
  en `--reference-doc` en lugar de `plantilla-apa7.docx`.

## 7. Integridad académica

- Esta skill **estructura, redacta borradores y verifica fuentes**. El
  contenido final lo revisa, lo corrige y lo asume el estudiante.
- No entregues un documento como terminado: el reporte de la tarea lista
  **qué secciones son borrador** para revisión humana. Dentro del
  harness, esa lista va como `verificacion_manual` de la tarea.
- Si el programa tiene reglas sobre el uso de IA (declararlo, limitarlo),
  están en `lineamientos.md` y mandan.

## 8. Salida

En `academico/<slug>/` (o la carpeta que fije la tarea):

| Archivo | Contenido |
|---|---|
| `documento.md` | El documento en Markdown con citas `[@clave]` |
| `referencias.bib` | Solo referencias verificadas |
| `apa.csl` (o el CSL de la norma) | Estilo descargado del repositorio oficial |
| `documento.docx` | Solo si hay pandoc |
| Informe de `verificador-datos` | Dentro de un milestone, donde lo indica `verificador-datos` (`milestones/<slug>/verificaciones/<id-tarea>.md`); suelto, `academico/<slug>/verificacion-referencias.md` |

En el chat muestra solo: la ruta, el conteo de referencias verificadas,
las `[CITA PENDIENTE]` que quedaron, el resultado del verificador y la
lista de secciones para revisión humana.
