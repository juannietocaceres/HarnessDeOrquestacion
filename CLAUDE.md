# CLAUDE.md — Harness de orquestación

## Qué es este repositorio

Esto no es un proyecto de software: es un **harness de orquestación** para
dirigir trabajo de desarrollo asistido por IA sobre cualquier tipo de
proyecto (web, backend, apps móviles, análisis de datos, CLI, etc.).

El modelo central es **milestone → waves**: un conjunto de tareas con
dependencias entre sí se agrupa en oleadas ("waves"). Las tareas sin
dependencias pendientes corren en paralelo dentro de una misma wave; una wave
nueva no arranca hasta que la anterior cierra por completo. Las decisiones
humanas que surgen durante una wave se agrupan y se presentan **una sola vez
por wave**, no tarea por tarea.

Ver [RESUMEN-HARNESS.md](RESUMEN-HARNESS.md) para el mapa completo de skills
y el diagrama de flujo, y [PROCESO.md](PROCESO.md) para la bitácora de por
qué el harness quedó diseñado así.

## Cómo se invoca cada skill

Las skills viven en `.claude/skills/<nombre>/SKILL.md` y se invocan con
`/<nombre>` (o se disparan automáticamente cuando el contexto coincide con su
`description`).

| Skill | Cuándo se usa |
|---|---|
| `/orquestador` | Para correr un milestone completo: recibe un manifest de tareas y lo ejecuta en waves. Es el punto de entrada de todo el sistema. |
| `/especificacion` | Antes de implementar una tarea ambigua o sin criterios de aceptación claros. Convierte una idea en lenguaje natural en un documento de especificación técnica. |
| `/frontend-design` | Al construir o rediseñar cualquier UI. Copiada tal cual del repo público de Anthropic (`plugins/frontend-design`). |
| `/revision-codigo` | Antes de cerrar cualquier tarea con cambios de código. Checklist de calidad, seguridad básica y legibilidad. |
| `/documentacion` | Al cerrar una tarea o milestone que necesita README, docs técnicas o comentarios. |
| `/testing` | Al implementar cualquier lógica con comportamiento verificable. Genera casos y estrategia de prueba según el tipo de proyecto. |

El `orquestador` es quien decide **cuándo** dentro de una wave se invoca cada
skill de apoyo (ver la sección "Tipos de proyecto" de su propio SKILL.md) —
las demás skills también se pueden invocar sueltas, fuera de una wave, para
trabajo puntual.

## Convenciones generales

- **Idioma**: la documentación del harness (specs, PROCESO, decisiones) se
  escribe en español. El código sigue la convención del proyecto destino.
- **Milestones**: cada milestone vive en `milestones/<slug>/`, con:
  - `milestone.yaml` — el manifest de tareas (formato definido en el SKILL.md
    del orquestador).
  - `estado.yaml` — estado vivo de la corrida (wave actual, estado de cada
    tarea, decisiones pendientes). Permite reanudar si la sesión se corta.
  - `decisiones.md` — bitácora de cada decisión del batched gate: quién la
    pidió, qué se preguntó, qué se respondió.
  - `bloqueos-externos.md` — dependencias fuera del alcance del milestone
    actual, resueltas aparte, que nunca bloquean una wave.
- **Aislamiento**: cada tarea corre en su propio git worktree (vía el Agent
  tool con `isolation: "worktree"`). Los cambios de una wave se integran a
  `main` antes de que arranque la siguiente wave — es lo que permite que la
  wave siguiente vea el trabajo de la anterior.
- **Cap de concurrencia**: configurable por milestone (`cap_concurrencia` en
  el manifest), por defecto 3.
- **Nada avanza sobre una decisión sin responder.** Ver la política de
  no-respuesta en el SKILL.md del orquestador y en RESUMEN-HARNESS.md.

## Estructura del repo

```
.claude/skills/          # las 6 skills del harness
milestones/<slug>/       # manifest + estado + decisiones por milestone
PROCESO.md               # bitácora de decisiones de diseño del harness
RESUMEN-HARNESS.md        # entregable final: mapa de skills + diagrama
```
