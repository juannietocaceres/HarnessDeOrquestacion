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

Hay 21 carpetas de skills: 10 propias del harness, `frontend-design`
(vendorizada de Anthropic) y 10 de la suite de Emil Kowalski (vendorizadas).

| Skill | Cuándo se usa |
|---|---|
| `/triage-proyecto` | Puerta de entrada cuando el usuario trae una idea, un plan en prosa o un pedido sin manifest. Produce un `triage.json` y un `milestone.yaml` borrador que pasa el preflight, sin escribir código. |
| `/orquestador` | Para correr un milestone completo: recibe un manifest de tareas y lo ejecuta en waves. Es el punto de entrada cuando ya hay manifest. |
| `/especificacion` | Antes de implementar una tarea ambigua o sin criterios de aceptación claros. Convierte una idea en lenguaje natural en un documento de especificación técnica. |
| `/optimizador-prompts` | Al escribir u ordenar una instrucción para una IA; el orquestador la usa para armar el prompt de cada sub-agente (`PLANTILLA-SUBAGENTE.md`). |
| `/optimizador-tokens` | Cuando el contexto de referencia de un sub-agente supera ~4.000 tokens estimados (cápsula) y al cerrar cada wave (`contexto-compacto.md`). Mide el ahorro con scripts. |
| `/revision-codigo` | Antes de cerrar cualquier tarea con cambios de código. Checklist de calidad, seguridad básica y legibilidad. |
| `/testing` | Al implementar cualquier lógica con comportamiento verificable. Genera casos y estrategia de prueba según el tipo de proyecto. |
| `/documentacion` | Al cerrar una tarea o milestone que necesita README, docs técnicas o comentarios. |
| `/verificador-datos` | Antes de publicar o de cerrar una tarea `docs`, `presentacion` o `contenido` con afirmaciones verificables, y al cerrar un milestone. Clasifica cada afirmación y propone correcciones. |
| `/presentaciones-visuales` | Al crear o mejorar un deck o material para exponer (`tipo: presentacion`). Genera un HTML autocontenido en `presentaciones/<slug>.html`. |
| `/frontend-design` | Al construir o rediseñar cualquier UI. Copiada tal cual del repo público de Anthropic (`plugins/frontend-design`). |
| Suite Emil Kowalski (10 skills) | Pulido de UI, animación web y Expo, revisión de motion: `emil-design-eng`, `animate`, `animate-expo`, `review-animations`, `improve-animations`, `find-animation-opportunities`, `mobile-native`, `pick-ui-library`, `prototype`, `animation-vocabulary`. `review-animations`, `pick-ui-library` y `prototype` no se disparan solas (`disable-model-invocation: true`). Vendorizadas sin cambios, en inglés; origen, hash y reglas de convivencia en [docs/vendor/emilkowalski-skills.md](docs/vendor/emilkowalski-skills.md). |

El `orquestador` es quien decide **cuándo** dentro de una wave se invoca cada
skill de apoyo (ver la sección "Tipos de proyecto" de su propio SKILL.md, §8) —
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
  - `contexto-compacto.md` — resumen compacto del estado que
    `optimizador-tokens` regenera al cerrar cada wave; una sesión que
    reanuda lo lee primero.
- **Aislamiento**: cada tarea corre en su propio git worktree (vía el Agent
  tool con `isolation: "worktree"`). Los cambios de una wave se integran a
  `main` antes de que arranque la siguiente wave — es lo que permite que la
  wave siguiente vea el trabajo de la anterior. Como los worktrees pueden
  arrancar desde un commit viejo, cada sub-agente corre primero
  `git merge --ff-only main` (paso 0, ver `PROCESO.md` §14).
- **Cap de concurrencia**: configurable por milestone (`cap_concurrencia` en
  el manifest), por defecto 3.
- **Nada avanza sobre una decisión sin responder.** Ver la política de
  no-respuesta en el SKILL.md del orquestador y en RESUMEN-HARNESS.md.

## Estructura del repo

```
.claude/skills/          # las 21 skills (10 propias + 11 vendorizadas)
docs/vendor/             # registro de las skills vendorizadas de Emil Kowalski
milestones/<slug>/       # manifest + estado + decisiones por milestone
presentaciones/          # decks HTML generados con presentaciones-visuales
PROCESO.md               # bitácora de decisiones de diseño del harness
RESUMEN-HARNESS.md        # entregable final: mapa de skills + diagrama
```
