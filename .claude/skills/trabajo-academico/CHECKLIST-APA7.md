# Checklist APA 7

Revisión antes de entregar un documento con norma APA 7 (7.ª edición del
*Publication Manual* de la APA). Si `lineamientos.md` del programa dice
otra cosa en un punto, manda `lineamientos.md`.

Fuente: guías oficiales de `apastyle.apa.org` (consulta del 2026-10-02;
enlaces al final). Las reglas de estilo cambian poco, pero si una regla de
aquí se usa para corregir a alguien, confírmala en la página enlazada.

Leyenda: **[CSL]** lo resuelve pandoc con `apa.csl` (revisa el resultado,
no lo escribas a mano); **[Manual]** lo revisas tú o se ajusta en la
plantilla de Word (`--reference-doc`).

---

## Citas en el texto

- [ ] Sistema autor–fecha: `(Apellido, año)` entre paréntesis o
      `Apellido (año)` en la narración. **[CSL]** con `[@clave]` y
      `@clave`.
- [ ] Dos autores: `&` entre paréntesis, "and" en la narración (APA en
      inglés). En documentos en español, muchos programas usan "y": sigue
      `lineamientos.md` y, si no dice nada, anótalo como supuesto.
      **[CSL]**
- [ ] Tres o más autores: solo el primero + "et al." **desde la primera
      cita**. **[CSL]**
- [ ] Cada cita del texto está en la lista de referencias y cada
      referencia de la lista se cita en el texto (pandoc solo incluye las
      citadas). **[CSL]**
- [ ] Citas textuales con número de página o párrafo. **[Manual]**: en
      pandoc, `[@clave, p. 12]`.
- [ ] Ninguna `[CITA PENDIENTE: ...]` queda en la versión que se entrega
      como final; si quedan, el documento es borrador. **[Manual]**

## Lista de referencias

- [ ] Empieza en página nueva, con el título "Referencias" (o
      "References") en negrita y centrado. **[Manual]**: en pandoc, un
      encabezado `# Referencias` + salto de página en la plantilla.
- [ ] Orden alfabético por la primera palabra de la referencia
      (normalmente el apellido del primer autor). **[CSL]**
- [ ] Sangría francesa de 0,5 in (1,27 cm). **[CSL]** / **[Manual]**
      según la plantilla.
- [ ] Hasta 20 autores: todos. Con 21 o más: los primeros 19, puntos
      suspensivos y el último. **[CSL]**
- [ ] Nombre de la revista y volumen en cursiva; el número (issue) y su
      paréntesis sin cursiva. **[CSL]**
- [ ] DOI como enlace `https://doi.org/...`, sin "Recuperado de" ni
      "Retrieved from"; DOIs viejos (`doi:`, `http://dx.doi.org/`)
      normalizados al formato actual. **[CSL]** si el `.bib` tiene el
      campo `doi` sin prefijo.
- [ ] DOI y URL copiados de la fuente, sin cambiar mayúsculas ni
      puntuación. **[Manual]**
- [ ] Todas las referencias pasaron `verificador-datos` (`SKILL.md` §5).
      **[Manual]**

## Formato del documento (trabajo de estudiante)

- [ ] Portada de estudiante: título, autor(es), afiliación (programa y
      universidad), curso (número y nombre), docente, fecha de entrega y
      número de página. **[Manual]**
- [ ] Márgenes de 1 in (2,54 cm) en todos los lados. **[Manual]**
- [ ] Fuente legible y consistente; APA acepta, entre otras, Times New
      Roman 12, Calibri 11, Arial 11, Georgia 11 y Aptos 12. **[Manual]**
- [ ] Doble espacio en todo el documento (resumen, texto, citas en
      bloque, tablas y figuras, referencias), sin espacio extra antes o
      después de párrafos ni de títulos. **[Manual]**
- [ ] Primera línea de cada párrafo con sangría de 0,5 in. **[Manual]**
- [ ] Número de página arriba a la derecha en todas las páginas.
      **[Manual]**
- [ ] Títulos con los 5 niveles de APA (**[Manual]**, en la plantilla):

| Nivel | Formato |
|---|---|
| 1 | Centrado, negrita, mayúsculas iniciales de título |
| 2 | Alineado a la izquierda, negrita |
| 3 | Alineado a la izquierda, negrita y cursiva |
| 4 | Con sangría, negrita, termina en punto; el texto sigue en la misma línea |
| 5 | Con sangría, negrita y cursiva, termina en punto; el texto sigue en la misma línea |

- [ ] Tablas y figuras numeradas, con título, y citadas en el texto antes
      de aparecer. **[Manual]**

---

## Enlaces oficiales (apastyle.apa.org)

- Citas autor–fecha: https://apastyle.apa.org/style-grammar-guidelines/citations/basic-principles/author-date
- Citas parentéticas y narrativas: https://apastyle.apa.org/style-grammar-guidelines/citations/basic-principles/parenthetical-versus-narrative
- DOIs y URLs: https://apastyle.apa.org/style-grammar-guidelines/references/dois-urls
- Cuántos autores listar: https://apastyle.apa.org/blog/more-than-20-authors
- Lista de referencias: https://apastyle.apa.org/style-grammar-guidelines/paper-format/reference-list
- Portada: https://apastyle.apa.org/style-grammar-guidelines/paper-format/title-page
- Márgenes: https://apastyle.apa.org/style-grammar-guidelines/paper-format/margins
- Interlineado: https://apastyle.apa.org/style-grammar-guidelines/paper-format/line-spacing
- Títulos: https://apastyle.apa.org/style-grammar-guidelines/paper-format/headings
- Párrafos: https://apastyle.apa.org/style-grammar-guidelines/paper-format/paragraph-format
