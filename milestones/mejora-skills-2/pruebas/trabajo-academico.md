# Prueba N3 — skill `trabajo-academico`

Fecha de las consultas: 2026-10-05. Tema: modelo predictivo de IA para zonas de riesgo de dengue por comuna en Santiago de Cali.

## Entregables de la prueba

- Esqueleto: `pruebas/trabajo-academico/documento.md` (anteproyecto, APA 7, todo lo no respaldado como `[POR COMPLETAR]` o `[CITA PENDIENTE]`).
- Bibliografía: `pruebas/trabajo-academico/referencias.bib` (6 entradas verificadas).
- Objetivos (punto 4 de §4 N3): 1 general + 5 específicos, un verbo medible cada uno (construir, compilar, caracterizar, comparar, evaluar, clasificar), tabla objetivo → actividad → entregable.
- `apa.csl` NO se deja en el repo: §4 N3 punto 6 dice descargarlo del repo oficial de CSL por proyecto, y la skill ya lo documenta (`https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl`, CC BY-SA 3.0). Se eliminó la copia de 2.273 líneas que traía la rama WIP.
- pandoc: NO está instalado en este equipo (`which pandoc` sin resultado), así que no se generó `.docx`. Comando documentado en `SKILL.md` §6:
  `pandoc documento.md --citeproc --bibliography referencias.bib --csl apa.csl -o documento.docx` (instalación Windows: `winget install --source winget --exact --id JohnMacFarlane.Pandoc`, a confirmar en https://pandoc.org/installing.html).

## Verificación de referencias (verificador-datos, nivel completa)

Metadatos contrastados con la API de Crossref (`https://api.crossref.org/works/<doi>`, consultada el 2026-10-05) y las URL con petición HTTP 200.

| Clave | Fuente comprobada | Resultado |
|---|---|---|
| bhatt2013 | https://doi.org/10.1038/nature12060 (Crossref: Nature 496(7446), 504–507, abril 2013, 18 autores) | ✅ |
| delmelle2016 | https://doi.org/10.1016/j.actatropica.2016.08.028 (Acta Tropica 164, 169–176, 4 autores) | ✅ |
| bahos2025 | https://doi.org/10.15446/rsap.v27n5.117662 (Rev. Salud Pública 27(5), 1–13; resumen leído) | ✅ |
| breiman2001 | https://doi.org/10.1023/A:1010933404324 (Machine Learning 45(1), 5–32) | ✅ |
| oms2024dengue | https://www.who.int/news-room/fact-sheets/detail/dengue-and-severe-dengue (HTTP 200) | ✅ (el año de la ficha no se fijó; se cita por fecha de consulta) |
| ins-sivigila | https://www.ins.gov.co/Direcciones/Vigilancia/Paginas/SIVIGILA.aspx (HTTP 200, página "SIVIGILA" del INS) | ✅ |

Afirmaciones del esqueleto contra su fuente:

| Afirmación | Fuente | Resultado |
|---|---|---|
| Mitad de la población en riesgo; 100–400 millones de infecciones/año | Ficha OMS (texto leído) | ✅ |
| 390 millones de infecciones anuales (estudio de modelado) | Ficha OMS la menciona como "one modelling estimate"; Bhatt 2013 es el estudio original (el resumen no vino en Crossref) | 🟡 La cifra se atribuye a Bhatt 2013 por conocimiento del artículo; confirmar leyendo su resumen. No es incorrecta ni inventada |
| Delmelle: modelo espacial de determinantes socioeconómicos y ambientales en Cali | Título del artículo | ✅ (solo a nivel de título; no se afirma ningún hallazgo) |
| Bahos: datos 2018–2019, temperatura superficial e insalubridad urbana | Resumen leído | ✅ |
| Breiman: bosques aleatorios como método candidato | Título/DOI | ✅ |

Afirmaciones normativas de `CHECKLIST-APA7.md` (búsquedas restringidas a apastyle.apa.org; las páginas directas bloquean la descarga automática, se usaron los resúmenes del buscador):

| Afirmación | Resultado |
|---|---|
| Fuentes aceptadas: Aptos 12, Calibri 11, Arial 11, Times New Roman 12, Georgia 11 | ✅ |
| Márgenes 1 in; doble espacio en todo, incluidos citas en bloque y referencias | ✅ |
| 3+ autores: "et al." desde la primera cita; `&` entre paréntesis, "and" en narrativa | ✅ |
| 21+ autores: primeros 19, puntos suspensivos, último | ✅ |
| Referencias: página nueva, "References" negrita y centrado, sangría francesa 0,5 in, orden alfabético | ✅ |
| DOI como enlace `https://doi.org/...`, sin etiqueta "DOI:" | ✅ |
| "Sin 'Recuperado de'" y "copiar DOI sin cambiar mayúsculas" | 🟡 No confirmados textualmente en esta corrida; consistentes con la guía de DOIs. Releer https://apastyle.apa.org/style-grammar-guidelines/references/dois-urls al usarlos |
| Portada de estudiante: título, autores, afiliación, curso, docente, fecha, nº de página arriba a la derecha | ✅ |
| 5 niveles de títulos (centrado/negrita; izq./negrita; izq./negrita-cursiva; sangría/negrita/punto; sangría/negrita-cursiva/punto) | ✅ |

Conteo: ✅ 17, 🟡 3, ⚠️ 0, 🔶 0, ❌ 0 (incorrectas), inventadas 0. Meta cumplida.

## Revisión de licencia de las skills `docx` y `pdf` (insumo para la decisión §7.4; no se decide aquí)

Fuentes: `https://raw.githubusercontent.com/anthropics/skills/main/skills/docx/LICENSE.txt`, `.../skills/pdf/LICENSE.txt` y `.../README.md` (leídos el 2026-10-05).

- Ambas llevan el mismo `LICENSE.txt` propietario: "© 2025 Anthropic, PBC. All rights reserved". El uso se rige por el acuerdo del usuario con Anthropic (Términos de Servicio de consumidor o comerciales).
- Restricciones adicionales textuales: no extraer los materiales de los Servicios ni conservar copias fuera de ellos; no distribuir, sublicenciar ni transferirlos a terceros; no crear obras derivadas.
- El README del repo las describe como "source-available, not open source", incluidas "as a reference" (a diferencia de "many skills in this repo are open source (Apache 2.0)").
- Conclusión para §7.4: NO se pueden vendorizar en este repo (copiar a `.claude/skills/` es retener copias fuera de los Servicios y redistribuir). Solo referenciarlas por nombre/URL. Alternativa gratuita: pandoc. (La interpretación jurídica final es del usuario.)

## Supuestos

- Norma APA 7 provisional (decisión §7.3 pendiente); no hay `lineamientos.md`, por eso el esqueleto es de prueba y no un documento formal entregable.
- Se conserva el tema de Cali en el repo; es borrador sin datos personales.

## Verificación manual pendiente (informativa)

Revisar que el esqueleto tenga sentido para el tema y el programa.
