# Verificación — RESUMEN-HARNESS.md (M8)

- **Documento verificado**: `RESUMEN-HARNESS.md`, versión final de M8.
- **Commit del repo**: `ba1e1e7` más los cambios de M8 en el working tree
  de la rama `worktree-agent-ac04f35ea18d555c6`.
- **Fecha**: 2026-10-01
- **Fuentes**: repo (`ls`, `git log`, `git rev-parse`, SKILL.md de cada
  skill, bitácoras de `panel-tareas-demo` y `mejora-skills`), informe
  previo `verificaciones/M3-resumen-harness.md` (22 afirmaciones del texto
  anterior, que se reaprovechan donde el texto no cambió). Sin web: la única
  afirmación de procedencia externa (`frontend-design`) se apoya en el hash
  de blob que M3 comparó contra upstream.
- **Tarea**: M8 (milestone `mejora-skills`).

**Conteo por categoría** (26 afirmaciones): ✅ 24 · 🟡 0 · ⚠️ 1 · 🔶 0 · ❌ 0 · 💬 1

## 1. Resumen general

Limpio tras las correcciones de M8. Los dos ❌ del informe de M3 están
corregidos: "Las 6 skills" → 21, con tabla nueva, y "dos de las cinco
tareas" → tres (T1, T2, T5). El 🟡 de M3 (#21, la nota honesta de §6) se
matizó con el texto que proponía ese informe. Queda un ⚠️ heredado sin
cambio (la composición de los lotes de la wave 3), que M3 ya había dejado
así por falta de registro.

## 2. Tabla de verificación

| # | Afirmación | Clasificación | Evidencia o motivo | Corrección sugerida |
|---|---|---|---|---|
| 1 | §1 "Las 21 skills": 10 propias, 1 de Anthropic, 10 de Emil | ✅ | `ls .claude/skills` → 21 carpetas; desglose como en `M8-claude-md.md` #1. | — |
| 2 | §1 las 10 primeras filas son las propias, después `frontend-design` y la fila de Emil | ✅ | Lectura de la tabla: 10 filas propias, 1 de Anthropic, 1 agrupada. | — |
| 3 | §1 los 11 enlaces `.claude/skills/<nombre>/SKILL.md` y el de `docs/vendor/…` | ✅ | Todos los archivos existen. | — |
| 4 | §1 `triage-proyecto`: produce `triage.json` + `milestone.yaml`, sin código; puerta de entrada | ✅ | `description` de la skill; `orquestador` §0. | — |
| 5 | §1 `orquestador`: preflight → waves → batched gate → integración; acepta el manifest del triage o uno a mano | ✅ | `orquestador` §0–§6 ("el manifest resultante entra al preflight normal … igual que uno escrito a mano"). | — |
| 6 | §1 `optimizador-prompts` incluye `PLANTILLA-SUBAGENTE.md` y se usa siempre al armar el prompt | ✅ | Archivo existe; `orquestador` §8. | — |
| 7 | §1 `optimizador-tokens`: modos `capsula` (> ~4.000) y `empaquetar` (cierre de cada wave), ahorro medido por script | ✅ | `optimizador-tokens/SKILL.md` §"Modo `capsula`", §"Modo `empaquetar`", §"Scripts"; `orquestador` §8. | — |
| 8 | §1 `verificador-datos`: seis categorías; cierre de tareas `docs`/`presentacion`/`contenido` y del milestone | ✅ | `verificador-datos/SKILL.md`, "Clasificación"; `orquestador` §8. | — |
| 9 | §1 `presentaciones-visuales`: HTML autocontenido en `presentaciones/<slug>.html`, teclado, PDF | ✅ | `description` de la skill. | — |
| 10 | §1 `frontend-design` "Copiada sin modificar de `anthropics/claude-code`" | ✅ | M3 #4 (blob `a5333457…` idéntico al upstream `52c7644`); `git log` de la carpeta: solo `cbe94b6`. | — |
| 11 | §1 Emil: 10 nombres, commit `d16ebe6`, 5 con fila propia en §8, las otras 5 solo si la tarea lo pide, 3 no se disparan solas | ✅ | `docs/vendor/emilkowalski-skills.md`; `orquestador` §8 (filas de `emil-design-eng`, `animate`, `animate-expo`, `mobile-native`, `review-animations`; párrafo sobre las otras 5); frontmatter con `disable-model-invocation: true` solo en `review-animations`, `pick-ui-library`, `prototype`. | — |
| 12 | §1 mapeo por tipo en `orquestador` §8; porqué de la ampliación en `PROCESO.md` §14 | ✅ | Ambas secciones existen con ese contenido. | — |
| 13 | §2 diagrama: idea → `triage-proyecto` (máx. 3 preguntas) → manifest | ✅ | `triage-proyecto/SKILL.md` ("Máximo 3 preguntas"); `orquestador` §0. | — |
| 14 | §2 diagrama: armado del prompt con `optimizador-prompts` + cápsula de `optimizador-tokens` si > ~4.000 | ✅ | `orquestador` §8, filas "Al armar el prompt del sub-agente". | — |
| 15 | §2 diagrama: cierre de wave con checklist de `verificacion_manual` (no bloquea) + `empaquetar` | ✅ | `orquestador` §2 paso 6. | — |
| 16 | §2 diagrama: cierre del milestone con `verificador-datos` + reporte final | ✅ | `orquestador` §2 paso 5. | — |
| 17 | §3 sin timeout, sin default, silencio ≠ aprobación | ✅ | `orquestador` §7. | — |
| 18 | §3 "tres de las cinco tareas … —T1, T2 y T5— no generaron ninguna decisión" | ✅ | `milestones/panel-tareas-demo/decisiones.md`: T1, T2, T5 "sin decisiones"; T3 y T4 escalaron. (Corregido: decía "dos".) | — |
| 19 | §3 "Las decisiones que llegan al gate son, por construcción, las que importan" | 💬 | Argumento de diseño. | — |
| 20 | §4 `fuera_de_alcance_si_depende_de`, `BLOQUEADA_EXTERNA`, `bloqueos-externos.md`, "ver `orquestador/SKILL.md` §4" | ✅ | `orquestador` §4 (líneas 145, 171, 173). | — |
| 21 | §5 `cap_concurrencia` default 3; liberar slot; `orquestador` §5 y `PROCESO.md` §4 | ✅ | `orquestador` línea 36 y §5 (línea 219); `PROCESO.md` §4 "Qué cuenta como liberar un slot". | — |
| 22 | §6 manifest, cap 2, grafo y tabla de waves | ✅ | Igual que M3 #14–#15; el texto no cambió. | — |
| 23 | §6 wave 3 en "2 lotes (T3+T4, después T5)" | ⚠️ | Igual que M3 #16: hubo 2 lotes (`PROCESO.md` §6 y §10), pero la composición de cada lote no quedó registrada. | Sin cambio. |
| 24 | §6 gate de la wave 3 (preguntas, respuestas, ruteo con `SendMessage`) | ✅ | `panel-tareas-demo/decisiones.md`, wave 3. | — |
| 25 | §6 especificación de T2 y artefactos, cada uno con su commit | ✅ | Igual que M3 #19–#20. | — |
| 26 | §6 nota honesta: "la sesión fijó su detección del entorno al arrancar, cuando el proyecto todavía no era repositorio git y las skills nuevas no existían"; confirmado en sesión nueva (`PROCESO.md` §7, §12) | ✅ | `PROCESO.md` §7 (worktree: no era repo git; skills: listado fijado al arrancar) y §12. (Matizado según M3 #21.) | — |

## 3. Errores o riesgos principales

Ninguno abierto. El ⚠️ #23 no cambia el sentido del texto; se resolvería
registrando los lotes en `estado.yaml` en corridas futuras.

## 4. Versión corregida

Ya aplicada en el documento:

- §1: "## 1. Las 21 skills, qué producen y cuándo se usan", con desglose y
  tabla nueva.
- §3: "…tres de las cinco tareas del milestone de ejemplo —T1, T2 y T5— no
  generaron ninguna decisión)."
- §6: "…(la sesión fijó su detección del entorno al arrancar, cuando el
  proyecto todavía no era repositorio git y las skills nuevas no
  existían)."

## 5. Recomendación final

✅ **Publicar tal cual.**
