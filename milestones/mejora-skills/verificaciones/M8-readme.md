# Verificación — README.md (M8)

- **Documento verificado**: `README.md`, versión final de M8.
- **Commit del repo**: `ba1e1e7` más los cambios de M8 en el working tree
  de la rama `worktree-agent-ac04f35ea18d555c6`.
- **Fecha**: 2026-10-01
- **Fuentes**: repo (`ls`, `git log`, bitácoras de milestones). Sin web: no
  hay afirmaciones cambiantes.
- **Tarea**: M8 (milestone `mejora-skills`).

**Conteo por categoría** (10 afirmaciones): ✅ 9 · 🟡 0 · ⚠️ 0 · 🔶 0 · ❌ 0 · 💬 1

## 1. Resumen general

Limpio. El conteo de skills ("las 6") se actualizó a 21 con su desglose,
y se agregó la puerta de entrada (`triage-proyecto`) en el texto y en el
diagrama.

## 2. Tabla de verificación

| # | Afirmación | Clasificación | Evidencia o motivo | Corrección sugerida |
|---|---|---|---|---|
| 1 | "Hecho para la Electiva …, Septiembre 2026" | ✅ | `git log` de `main`: los commits del scaffold y del milestone de ejemplo son de septiembre de 2026 (p. ej. `46fa018`, 2026-09-18). | — |
| 2 | RESUMEN-HARNESS.md: "mapa de las 21 skills (10 propias y 11 vendorizadas)" | ✅ | `ls .claude/skills` → 21; 10 de Emil + `frontend-design` = 11 vendorizadas; `RESUMEN-HARNESS.md` §1 tiene ese mapa. | — |
| 3 | PROCESO.md es la bitácora de decisiones de diseño con el porqué | ✅ | Contenido de `PROCESO.md` §1–§14. | — |
| 4 | CLAUDE.md explica cómo se invoca cada skill | ✅ | `CLAUDE.md`, sección "Cómo se invoca cada skill". | — |
| 5 | Diagrama: idea sin manifest → `triage-proyecto` → milestone → preflight → waves → gate | ✅ | `orquestador` §0 y §2. | — |
| 6 | `triage-proyecto` convierte una idea ambigua o un plan en prosa en un `milestone.yaml` que pasa el preflight, y después lo ejecuta el orquestador | ✅ | `triage-proyecto/SKILL.md`, `description`; `orquestador` §0. | — |
| 7 | Estructura: 21 skills = 10 propias (orquestador, triage-proyecto y 8 de apoyo) + `frontend-design` + 10 de Emil | ✅ | `ls .claude/skills` (10 propias − 2 = 8 de apoyo). | — |
| 8 | `docs/vendor/`, `milestones/`, `presentaciones/`, `schema/ api/ ui/` existen con lo que se dice | ✅ | `ls`; `schema/tareas.md`, `api/contrato-tareas.md`, `ui/*.html` son los artefactos de `panel-tareas-demo` (RESUMEN §6). | — |
| 9 | El ejemplo real: milestone de 5 tareas con dependencias, corridas por sub-agentes reales | ✅ | `milestones/panel-tareas-demo/milestone.yaml` (5 tareas), `decisiones.md`, commits `2cb9723`, `b6c7e47`, `ef837a5`, `5374913`, `dff84e6`. | — |
| 10 | "Un sistema reutilizable para … cualquier tipo de proyecto" | 💬 | Objetivo de diseño; respaldado por la tabla por tipo de `orquestador` §8, pero es una valoración. | — |

## 3. Errores o riesgos principales

Ninguno.

## 4. Versión corregida

No aplica.

## 5. Recomendación final

✅ **Publicar tal cual.**
