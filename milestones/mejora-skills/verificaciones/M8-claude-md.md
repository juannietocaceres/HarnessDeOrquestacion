# Verificación — CLAUDE.md (M8)

- **Documento verificado**: `CLAUDE.md`, versión final de M8.
- **Commit del repo**: `ba1e1e7` (`main` tras la wave 3) más los cambios de
  M8 en el working tree de la rama `worktree-agent-ac04f35ea18d555c6`.
- **Fecha**: 2026-10-01
- **Fuentes**: repo (`ls`, `git log`, `git rev-parse`, lectura de los
  SKILL.md, `docs/vendor/emilkowalski-skills.md`), informe previo
  `verificaciones/M3-resumen-harness.md`. Sin web: no hubo afirmaciones
  cambiantes que la requieran (la procedencia de `frontend-design` se apoya
  en el hash de blob ya comparado con upstream por M3).
- **Tarea**: M8 (milestone `mejora-skills`).

**Conteo por categoría** (20 afirmaciones): ✅ 20 · 🟡 0 · ⚠️ 0 · 🔶 0 · ❌ 0 · 💬 0

## 1. Resumen general

Limpio. El conteo y la tabla de skills coinciden con `.claude/skills/`, y
todas las rutas y referencias resuelven. Durante la verificación se añadió
`contexto-compacto.md` a la lista de archivos de un milestone (antes
faltaba, sin ser incorrecto) y la nota del paso 0; ambos quedan verificados
abajo.

## 2. Tabla de verificación

| # | Afirmación | Clasificación | Evidencia o motivo | Corrección sugerida |
|---|---|---|---|---|
| 1 | "Hay 21 carpetas de skills: 10 propias, `frontend-design` (Anthropic) y 10 de Emil" | ✅ | `ls .claude/skills` → 21. Emil: las 10 listadas en `docs/vendor/emilkowalski-skills.md`. Anthropic: `frontend-design`. Propias (10): documentacion, especificacion, optimizador-prompts, optimizador-tokens, orquestador, presentaciones-visuales, revision-codigo, testing, triage-proyecto, verificador-datos. | — |
| 2 | `/triage-proyecto`: puerta de entrada; `triage.json` + `milestone.yaml` que pasa el preflight, sin código | ✅ | `description` de `triage-proyecto/SKILL.md`; `orquestador` §0. | — |
| 3 | `/orquestador`: punto de entrada cuando ya hay manifest | ✅ | `orquestador` §0–§1. | — |
| 4 | `/especificacion`: tareas ambiguas o sin criterios | ✅ | `especificacion/SKILL.md`, `description`. | — |
| 5 | `/optimizador-prompts`: arma el prompt de cada sub-agente con `PLANTILLA-SUBAGENTE.md` | ✅ | El archivo existe; `orquestador` §8, fila "Al armar el prompt … Siempre". | — |
| 6 | `/optimizador-tokens`: cápsula sobre ~4.000 tokens, `contexto-compacto.md` al cerrar cada wave, ahorro medido por scripts | ✅ | `orquestador` §8 (umbral ~4.000; fila "Al cerrar cada wave"); `optimizador-tokens/scripts/medir_tokens.py`. | — |
| 7 | `/revision-codigo`, `/testing`, `/documentacion`: cuándo se usan | ✅ | `description` de cada SKILL.md. | — |
| 8 | `/verificador-datos`: tareas `docs`/`presentacion`/`contenido` y cierre de milestone | ✅ | `orquestador` §8, filas "Antes de reportarse COMPLETADA" y "Al cerrar el milestone". | — |
| 9 | `/presentaciones-visuales`: `tipo: presentacion`, HTML en `presentaciones/<slug>.html` | ✅ | `description` de la skill; `orquestador` §8. | — |
| 10 | `/frontend-design` "copiada tal cual" de `plugins/frontend-design` | ✅ | `git log -- .claude/skills/frontend-design` → solo `cbe94b6` (scaffold); blob `a5333457…` igual al upstream según M3 (#4). | — |
| 11 | Suite Emil: los 10 nombres listados | ✅ | `docs/vendor/emilkowalski-skills.md`, tabla "Skills copiadas"; carpetas existen. | — |
| 12 | `review-animations`, `pick-ui-library`, `prototype` no se disparan solas | ✅ | Solo esas 3 tienen `disable-model-invocation: true` en el frontmatter (awk sobre los 21 SKILL.md). | — |
| 13 | "Vendorizadas sin cambios, en inglés"; enlace a `docs/vendor/emilkowalski-skills.md` | ✅ | Registro de vendor, sección "Verificación" (`diff -r` limpio salvo `LICENSE.txt`); el enlace resuelve. | — |
| 14 | Mapeo de cuándo se invoca cada skill en "Tipos de proyecto", §8 del orquestador | ✅ | `orquestador/SKILL.md` §8 "Tipos de proyecto: qué skill se activa y cuándo". | — |
| 15 | Archivos de un milestone: `milestone.yaml`, `estado.yaml`, `decisiones.md`, `bloqueos-externos.md` | ✅ | `ls milestones/mejora-skills/`. | — |
| 16 | `contexto-compacto.md` lo regenera `optimizador-tokens` al cerrar cada wave y una sesión que reanuda lo lee primero | ✅ | `orquestador` §2 paso 6 y §9 ("lee **primero** `contexto-compacto.md`"). | — |
| 17 | Aislamiento por worktree, integración a `main` antes de la wave siguiente | ✅ | `orquestador` §2 y §5. | — |
| 18 | Los worktrees pueden arrancar desde un commit viejo; paso 0 `git merge --ff-only main`; ver `PROCESO.md` §14 | ✅ | `git reflog` de este worktree: `46fa018` → `ba1e1e7` por fast-forward; `orquestador` §5; `PROCESO.md` §14. | — |
| 19 | `cap_concurrencia` por defecto 3; política de no-respuesta en orquestador y RESUMEN | ✅ | `orquestador` §1 (línea 36) y §7; `RESUMEN-HARNESS.md` §3. | — |
| 20 | Estructura: `.claude/skills/` (21 = 10 + 11), `docs/vendor/`, `milestones/`, `presentaciones/`, `PROCESO.md`, `RESUMEN-HARNESS.md` | ✅ | `ls` en la raíz. | — |

## 3. Errores o riesgos principales

Ninguno. Riesgo a futuro: el número 21 aparece en tres lugares del
archivo (texto, tabla, estructura); si se agrega una skill hay que
actualizar los tres.

## 4. Versión corregida

No aplica.

## 5. Recomendación final

✅ **Publicar tal cual.**
