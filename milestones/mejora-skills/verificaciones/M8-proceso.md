# Verificación — PROCESO.md (M8)

- **Documento verificado**: `PROCESO.md`, versión final de M8 (incluye la
  nueva §14 "Ampliación de skills").
- **Commit del repo**: `ba1e1e7` más los cambios de M8 en el working tree
  de la rama `worktree-agent-ac04f35ea18d555c6`.
- **Fecha**: 2026-10-01
- **Fuentes**: repo (`git log`, `git rev-list`, `git reflog`, `ls`, SKILL.md
  y scripts de las skills), `PLAN-MEJORA-SKILLS.md`,
  `milestones/mejora-skills/{decisiones.md,contexto-compacto.md,pruebas/*.md}`,
  `docs/vendor/emilkowalski-skills.md`, informe previo
  `verificaciones/M3-resumen-harness.md`. Sin web.
- **Alcance**: el texto supera las 800 palabras. Se verificaron **todas**
  las afirmaciones de §14 (nueva) y las afirmaciones sobre el repo de
  §1–§13 que podían haber quedado desactualizadas (conteos, referencias a
  secciones, procedencia). La narrativa histórica de §1–§13 (qué se le
  preguntó al usuario, qué falló en la sesión original) no tiene otra
  fuente que esta misma bitácora y no se reclasifica.
- **Tarea**: M8 (milestone `mejora-skills`).

**Conteo por categoría** (30 afirmaciones): ✅ 26 · 🟡 0 · ⚠️ 3 · 🔶 0 · ❌ 0 · 💬 1

## 1. Resumen general

Limpio. Durante la verificación se corrigieron en el borrador de §14 tres
frases antes de cerrar: "es la única skill nueva que puede preguntar"
(falso: `optimizador-prompts` y `presentaciones-visuales` también preguntan
cuando corren sueltas; se reformuló como "a diferencia de las otras skills
nuevas cuando corren dentro del orquestador"), "si falta una entidad, la
cápsula no se usa" (la skill dice que se corrige; se ajustó) y la causa
del umbral nuevo (se pasó de "de ahí que" a "con esos datos sobre la mesa,
el gate subió…"). Quedan tres ⚠️ históricos sin cambio. `PROCESO.md` sigue
sin §8 (salta de §7 a §9); no se renumeró, por instrucción de la tarea.

## 2. Tabla de verificación

| # | Afirmación | Clasificación | Evidencia o motivo | Corrección sugerida |
|---|---|---|---|---|
| 1 | §3 `git init -b main` porque los worktrees necesitan un repo con commits | ✅ | `PROCESO.md` §7 y §12 lo confirman; primer commit `cbe94b6`. | — |
| 2 | §4 referencias a `orquestador` SKILL.md §2 y §6 | ✅ | §2 "Algoritmo general", §6 "batched gate". | — |
| 3 | §5 `frontend-design` copiada sin modificar desde `anthropics/claude-code` | ✅ | M3 #4 (blob `a5333457…`); `git log` de la carpeta: solo `cbe94b6`. | — |
| 4 | §6 W1={T1}, W2={T2}, W3={T3,T4,T5}, cap 2 | ✅ | Preflight sobre `panel-tareas-demo/milestone.yaml` (PASA, 3 waves); `cap_concurrencia: 2`. | — |
| 5 | §9 especificación de T2 enlazada | ✅ | `milestones/panel-tareas-demo/especificaciones/T2-contrato-api.md` existe. La cita "§8 de PROCESO.md" de `panel-tareas-demo/decisiones.md` se corrigió a §9. | — |
| 6 | §10 las 5 tareas `COMPLETADA`, cada una en su commit | ✅ | `estado.yaml` (5 × `COMPLETADA`); commits de M3 #20. | — |
| 7 | §11 "un deck de 10 slides" | ⚠️ | El deck de entonces no está en el repo (el actual, `presentaciones/harness-clase.html`, es de M1). Sin fuente para contar. | Sin cambio. |
| 8 | §11 "La tabla de las 6 skills pasó a una grilla de tarjetas" | ✅ | Histórico: en ese momento había 6 (M3 #1, commit `3b659f7`). No es un conteo vigente. | — |
| 9 | §12 aislamiento por worktree confirmado en sesión nueva | ✅ | Igual que M3 #22. | — |
| 10 | §13 "los 12 commits reales" al momento de GitHub Desktop | ⚠️ | `git rev-list --count 792c517` = 13 y `620ac25` (el commit que documenta la publicación) = 14; el momento exacto del intento no quedó registrado. | Sin cambio. |
| 11 | §13 `gh` no instalada, push desde la terminal del usuario | ⚠️ | Hecho del entorno en ese momento; no hay registro reproducible. | Sin cambio. |
| 12 | §14 de 6 a 21 skills; plan con 9 tareas M1–M9 en 5 waves | ✅ | `ls .claude/skills` → 21; preflight de `mejora-skills/milestone.yaml`: "PASA (9 tareas, 5 waves)". | — |
| 13 | §14 10 propias (5 originales + 5 nuevas), 1 de Anthropic, 10 de Emil | ✅ | `ls`; originales propias: orquestador, especificacion, revision-codigo, documentacion, testing (`cbe94b6`). | — |
| 14 | §14 el insumo original del triage devolvía solo JSON, con catálogo de agentes y `orchestration_plan` como lista de textos | ✅ | `PLAN-MEJORA-SKILLS.md` §4 M5, tabla "Mapeo del plan original al harness". | — |
| 15 | §14 `triage.json` solo para clasificación; el borrador pasa el mismo preflight (`preflight_manifest.py` aplica `orquestador` §4) | ✅ | `triage-proyecto/SKILL.md`; docstring de `preflight_manifest.py`. | — |
| 16 | §14 el triage puede preguntar (máx. 3 de opción múltiple) a diferencia de las otras skills nuevas dentro del orquestador | ✅ | `triage-proyecto/SKILL.md` ("Máximo 3 preguntas, todas de opción múltiple"); `optimizador-prompts` y `presentaciones-visuales`: "no preguntes" en modo no interactivo / dentro de un sub-agente. | — |
| 17 | §14 `medir_tokens.py` (caracteres / 4, `estimado`; con `--api` y `ANTHROPIC_API_KEY`, conteo oficial) y `verificar_entidades.py`; código ≠ 0 si falta una entidad y la cápsula se corrige | ✅ | Docstring de `medir_tokens.py`; `optimizador-tokens/SKILL.md` §"Modo `capsula`" paso de corrección y tabla de scripts (código 1 = falta una entidad). | — |
| 18 | §14 Emil copiado byte a byte desde `d16ebe60d09a5ba2afcb7054ede9d0a10c9f6128`, `LICENSE` en cada carpeta, `diff -r` | ✅ | `docs/vendor/emilkowalski-skills.md`, "Origen" y "Verificación". | — |
| 19 | §14 se descartó `npx skills@latest add` por no dejar clara la versión | ✅ | `PLAN-MEJORA-SKILLS.md` §4 M4, "Alternativa descartada". | — |
| 20 | §14 10 de 13; ~807 tokens por sesión; dejar fuera 3 ahorra ~340 | ✅ | `docs/vendor/emilkowalski-skills.md`, "Costo final con lo vendorizado". | — |
| 21 | §14 decisiones de los gates de las waves 1 y 2 (incluida la pregunta de seguimiento y la precisión sobre `verificacion_manual`) | ✅ | Comparadas una por una con `milestones/mejora-skills/decisiones.md`; respuestas literales. | — |
| 22 | §14 wave 3 (M7) sin decisiones | ✅ | `decisiones.md`, "Wave 3". | — |
| 23 | §14 contradicción stagger y su resolución; hover en tarjetas como choque aparente | ✅ | `docs/vendor/emilkowalski-skills.md`, contradicciones 1 y 2; `orquestador` §8. | — |
| 24 | §14 "Initial Response" y la regla del orquestador | ✅ | `docs/vendor/emilkowalski-skills.md` contradicción 3; `orquestador` §8, "Initial Response". | — |
| 25 | §14 registro mezclado: 4 skills previas, M1 y M2 con voseo, M3 con "tú", orquestador mezclado; M8 reescribió las 4 | ✅ | `decisiones.md`, wave 1; diff de M8 sobre las 4 SKILL.md (solo verbos, sin cambios de reglas). | — |
| 26 | §14 criterios no verificables por sub-agente; lo destapó el reporte de M5; el plan de `enigma-go` trae criterios así | ✅ | `decisiones.md`, wave 2; `pruebas/triage.md` §2 (input: `milestones/enigma-go/plan.md`; F0 "abre en Expo Go", F3 "cámara real"). | — |
| 27 | §14 resultados: prompts 5 criterios literales + control negativo; triage 3 de estrés + regresión, 4 manifests pasan; tokens 2.210→1.024 (−54 %), 2.735→1.549 (−43 %), 13/13, ~5 % (48.127→45.594); umbral ~2.000→~4.000 | ✅ | `pruebas/optimizador-prompts.md` "Veredicto"; `pruebas/triage.md` "Resumen"; `pruebas/tokens.md` §2; `PLAN-MEJORA-SKILLS.md` §4 M6 (umbral original ~2.000); `decisiones.md` wave 2. | — |
| 28 | §14 `contexto-compacto.md` de la wave 3: 1.516 → 766 (−49 %), 85 entidades preservadas; M7: 3 manifests pasan y las skills de §8 existen | ✅ | Comentario de métricas al final de `contexto-compacto.md`; `pruebas/orquestador.md`. | — |
| 29 | §14 worktrees nacen en `46fa018` (18 de septiembre, anterior al milestone); registrado en la prueba de M7 y repetido en M8; paso 0 en la plantilla y en `orquestador` §5 | ✅ | `git log -1 46fa018` (2026-09-18); `pruebas/orquestador.md` ("46fa018 → e6de756"); `git reflog` de este worktree (`46fa018` → `ba1e1e7`); `PLANTILLA-SUBAGENTE.md` `[PASO 0]`; `orquestador` §5 línea 200. | — |
| 30 | §14 "un porcentaje de ahorro estimado a ojo no se puede auditar" | 💬 | Argumento de diseño. | — |

Nota de registro: las citas literales de prompts históricos en §10
("escalalo", "DETENÉTE y planteá") conservan el voseo a propósito: son
citas de lo que se escribió entonces, no texto del documento.

## 3. Errores o riesgos principales

Ninguno abierto. Los ⚠️ #7, #10 y #11 son hechos históricos sin registro
en el repo; no cambian el sentido del texto.

## 4. Versión corregida

Aplicada en el borrador de §14 antes de cerrar (ver "Resumen general").

## 5. Recomendación final

✅ **Publicar tal cual.**
