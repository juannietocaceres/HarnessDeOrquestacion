# Verificación — RESUMEN-HARNESS.md (prueba de M3)

- **Documento verificado**: `RESUMEN-HARNESS.md`
- **Commit del repo contra el que se verificó**: `3b659f7` (rama
  `worktree-agent-ada788e3e008969f9` avanzada en fast-forward a `main`,
  *antes* del commit de M3). Otras tareas de la wave 1 (M1, M2, M4) están
  agregando carpetas en `.claude/skills/` en sus propias ramas; los conteos
  de abajo valen para este commit.
- **Fecha**: 2026-10-01
- **Fuentes**: repo (`ls`, `git log`, `git show`, `git rev-parse`, `diff`),
  bitácoras del milestone `panel-tareas-demo` y web (clon de
  `anthropics/claude-code`, commit upstream
  `52c76441cae91f6891e4712306bffb057ff6fec5`, 2026-10-01).
- **Tarea**: M3 (milestone `mejora-skills`), corrida como sub-agente; el
  documento está fuera del alcance de la tarea, así que las correcciones
  quedan propuestas y no aplicadas.

**Conteo por categoría** (22 afirmaciones): ✅ 17 · 🟡 1 · ⚠️ 1 · 🔶 0 · ❌ 2 · 💬 1

## 1. Resumen general

El documento es sólido: todas las rutas y enlaces resuelven, las
referencias a secciones (`orquestador` §4, §5, §8; `PROCESO.md` §4, §7,
§12) apuntan a lo que dicen, y la afirmación más delicada —que
`frontend-design` es una copia sin modificar de la upstream— se confirma.
Hay dos errores puntuales con corrección clara: un conteo de tareas mal
hecho en §3 y el conteo de skills de §1, que queda desactualizado en cuanto
se integra esta misma tarea. Ninguno requiere decisión humana.

## 2. Tabla de verificación

| # | Afirmación | Clasificación | Evidencia o motivo | Corrección sugerida |
|---|---|---|---|---|
| 1 | §1 "Las 6 skills" | ✅ Correcta (en `3b659f7`) | `ls .claude/skills` → 6 carpetas: `documentacion`, `especificacion`, `frontend-design`, `orquestador`, `revision-codigo`, `testing`. | — |
| 2 | §1 "Las 6 skills", leído sobre la rama de M3 (`3b659f7` + este commit) | ❌ Incorrecta | Con `verificador-datos` hay 7 carpetas; con M1, M2, M4–M6 integradas serán más. Fuente clara (`ls`). | "Las N skills…" con N real tras integrar la wave; la tabla de §1 debe sumar las nuevas filas. Le corresponde a M8. |
| 3 | §1 los 6 enlaces `.claude/skills/<nombre>/SKILL.md` | ✅ Correcta | Los 6 archivos existen. | — |
| 4 | §1 `frontend-design` "Copiada sin modificar de `anthropics/claude-code`" | ✅ Correcta | Hash de blob idéntico en ambos repos: `git rev-parse HEAD:.claude/skills/frontend-design/SKILL.md` = `git rev-parse HEAD:plugins/frontend-design/skills/frontend-design/SKILL.md` (upstream `52c7644`) = `a5333457c414d20d625f307df945842c0952ecc3`. `diff -r` directo marca las 71 líneas como distintas, pero solo por finales de línea: el working tree tiene CRLF (`core.autocrlf=true`, `git ls-files --eol` → `i/lf w/crlf`); `diff -r --strip-trailing-cr` sale con código 0. `git log` muestra un solo commit sobre la carpeta (`cbe94b6`, el scaffold): nunca se editó. | — |
| 5 | §1 "el mapeo completo por tipo de proyecto está en su propio SKILL.md, §8" | ✅ Correcta | `orquestador/SKILL.md` §8 "Tipos de proyecto: qué skill se activa y cuándo". | — |
| 6 | §1 `orquestador`: "preflight → waves → batched gate → integración" | ✅ Correcta | §2–§6 del SKILL.md del orquestador. | — |
| 7 | §1 `revision-codigo`: "siempre antes de integrarla — nunca después" | ✅ Correcta | Sección "Cuándo se ejecuta" de `revision-codigo/SKILL.md`. | — |
| 8 | §3 sin timeout, sin default, silencio ≠ aprobación | ✅ Correcta | `orquestador/SKILL.md` §7, literal. | — |
| 9 | §3 "dos de las cinco tareas del milestone de ejemplo no generaron ninguna decisión" | ❌ Incorrecta | `milestones/panel-tareas-demo/decisiones.md`: T1, T2 y T5 "sin decisiones"; solo T3 y T4 escalaron. Son **tres** de cinco. Parece una confusión con "2 decisiones reales" del cierre de esa bitácora. Fuente clara. | "…tres de las cinco tareas del milestone de ejemplo no generaron ninguna decisión" |
| 10 | §3 "Las decisiones que llegan al gate son, por construcción, las que importan" | 💬 Opinión | Argumento de diseño, no un hecho comprobable. Se presenta como razonamiento, no como dato. | — |
| 11 | §4 `fuera_de_alcance_si_depende_de`, `BLOQUEADA_EXTERNA`, `bloqueos-externos.md`, "ver `orquestador/SKILL.md` §4" | ✅ Correcta | `orquestador/SKILL.md` líneas 35, 98, 112 (§4) y 222 (§9). | — |
| 12 | §5 `cap_concurrencia` "default 3"; detalle en `orquestador` §5 y `PROCESO.md` §4 | ✅ Correcta | `orquestador/SKILL.md` línea 24 y §5 (línea 135); `PROCESO.md` §4 discute el cap. | — |
| 13 | §5 una tarea pausada "libera su slot" | ✅ Correcta | `PROCESO.md` §4, "Qué cuenta como liberar un slot". | — |
| 14 | §6 manifest enlazado; cap 2; grafo T1→T2→{T3,T4,T5} | ✅ Correcta | `milestones/panel-tareas-demo/milestone.yaml`: `cap_concurrencia: 2`, `depende_de` coincide. | — |
| 15 | §6 tabla de waves: W1 T1 directo; W2 T2 con `especificacion` previa por criterios vacíos; W3 T5 directo, T3 y T4 escalaron | ✅ Correcta | Manifest (`T2.criterios_aceptacion: []`), `estado.yaml` y `decisiones.md`. | — |
| 16 | §6 wave 3 en "2 lotes (T3+T4, después T5)" | ⚠️ No verificable | Que hubo 2 lotes lo confirman `PROCESO.md` §6 y §10; la composición de cada lote no está registrada en `estado.yaml` ni en `decisiones.md`. El orden de commits (T5 23:33, T4 23:52, T3 23:55) es consistente, pero se explica igual por la pausa de T3/T4. | Sin cambio en el texto. Si se quiere respaldar, registrar los lotes en `estado.yaml` en corridas futuras. |
| 17 | §6 preguntas y respuestas del gate de la wave 3 (filtro sí; validación solo en servidor) | ✅ Correcta | `decisiones.md`, wave 3. | — |
| 18 | §6 respuestas ruteadas con `SendMessage`, cada sub-agente sin ver la otra decisión | ✅ Correcta (según bitácora) | `decisiones.md`, wave 3. No hay otra fuente primaria; la bitácora es el registro oficial. | — |
| 19 | §6 especificación de T2 "generada a partir del esquema real que produjo T1" | ✅ Correcta | `especificaciones/T2-contrato-api.md` cita `schema/tareas.md` (T1) en las líneas 16, 23, 39 y 46. | — |
| 20 | §6 artefactos enlazados, "cada uno con su propio commit de git, trazable a la tarea" | ✅ Correcta | Los 5 archivos existen; `git show --stat`: `2cb9723` (T1), `b6c7e47` (T2), `ef837a5` (T3), `5374913` (T4, además `.gitignore`), `dff84e6` (T5). | — |
| 21 | §6 nota honesta: worktree y registro de skills "chocaron con … (el proyecto no era un repositorio git cuando la sesión arrancó)" | 🟡 Mayormente correcta | `PROCESO.md` §7: la causa "no era repo git" explica el fallo de worktree; el de skills (`Unknown skill: especificacion`) se debió a que el listado de skills quedó fijado al arrancar, antes de que la carpeta existiera. Mismo patrón, causa distinta. | "…(la sesión fijó su detección del entorno al arrancar, cuando el proyecto todavía no era repositorio git y las skills nuevas no existían)" |
| 22 | §6 confirmado en sesión nueva, "detalle en PROCESO.md §12" | ✅ Correcta | `PROCESO.md` §12. | — |

## 3. Errores o riesgos principales

1. **#9 — "dos de las cinco" → "tres de las cinco".** Es el único error
   factual del texto actual, y está en el argumento central de §3
   (cuántas decisiones se resuelven solas): el dato real lo refuerza.
2. **#2 — conteo de skills.** Correcto hoy en `main`, pero queda viejo en
   cuanto se integre la wave 1 de `mejora-skills`. Ya está previsto en M8;
   esta verificación debería repetirse al cerrar el milestone
   (`cierre-resumen-harness.md`) para confirmar que M8 actualizó el número
   y la tabla.
3. **#21 — matiz en la nota honesta** (menor).

## 4. Versión corregida

- §3: "…(ver el ejemplo real en la sección 6: **tres** de las cinco tareas
  del milestone de ejemplo no generaron ninguna decisión)."
- §1 (tras integrar la wave): "## 1. Las **N** skills, qué producen y
  cuándo se usan", con una fila por skill nueva.
- §6, nota honesta: "…chocaron con una limitación puntual del entorno (la
  sesión fijó su detección del entorno al arrancar, cuando el proyecto
  todavía no era repositorio git y las skills nuevas no existían)."

## 5. Recomendación final

🟡 **Publicar con cambios menores.** Los dos ❌ tienen fuente clara y se
corrigen con una línea cada uno; no hay `DECISION_NEEDED`. Como
`RESUMEN-HARNESS.md` está fuera del alcance de M3, las correcciones quedan
propuestas para M8.

---

### Observaciones fuera del documento verificado (no corregidas)

- `milestones/panel-tareas-demo/decisiones.md` (wave 2) cita "§8 de
  PROCESO.md", pero `PROCESO.md` no tiene §8: salta de §7 a §9 ("Entregable
  de muestra: especificación de T2"). La referencia probablemente debía ser
  §9, o falta la sección 8.
- `CLAUDE.md` ("las 6 skills del harness" en la estructura del repo) tendrá
  el mismo desfase que el #2 cuando se integre la wave; también le
  corresponde a M8.
- El frontmatter de `frontend-design` dice `license: Complete terms in
  LICENSE.txt`, pero no hay `LICENSE.txt` en la carpeta. Es idéntico en la
  upstream (tampoco hay `LICENSE.txt` en
  `plugins/frontend-design/skills/frontend-design/`), así que no rompe la
  copia literal; solo queda anotado.
