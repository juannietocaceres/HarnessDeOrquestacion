# Plantilla de prompt para un sub-agente del harness

La usa el orquestador (§5) para armar el prompt de cada tarea que lanza con
el tool `Agent` (`isolation: "worktree"`). El sub-agente no ve la
conversación del orquestador: este prompt es todo su contexto.

Si la tarea trae `modelo:` en el manifest, el orquestador lo pasa como
parámetro `model` de la llamada a `Agent`. **No** se escribe en el texto
del prompt: no hay bloque para él.

## Cómo se llena

| Bloque | Fuente | Regla |
|---|---|---|
| `[PASO 0]` | Archivos que integró a `main` la wave anterior | Va siempre. Los worktrees pueden arrancar desde un commit viejo: el sub-agente corre `git merge --ff-only main` y comprueba que existen esos archivos, nombrados uno por uno (en la wave 1, los archivos base que la tarea necesita). |
| `[TAREA]` | `id`, `titulo`, `tipo` del manifest + slug del milestone | Copia exacta. |
| `[OBJETIVO]` | `descripcion` del manifest | Se puede ordenar para que se lea mejor, sin agregar ni quitar alcance. |
| `[CRITERIOS DE ACEPTACIÓN]` | `criterios_aceptacion` del manifest | **Literales**: carácter por carácter, uno por línea, entre comillas. Nunca parafraseados, resumidos, reordenados ni completados. |
| `[VERIFICACIÓN MANUAL]` | `verificacion_manual` del manifest | **Literal**, como los criterios. Solo si la tarea la declara. Es informativa: el sub-agente no la verifica ni bloquea su cierre por ella; el orquestador la lista al cierre de la wave. |
| `[CONTEXTO]` | Rutas y documentos citados por la tarea; resultados relevantes de waves previas | Si el contexto de referencia supera el umbral de `optimizador-tokens`, va la cápsula que devuelve su modo `capsula`, tal cual. El código a editar no se copia: se pasa la ruta. |
| `[SKILLS A APLICAR]` | Tabla de `orquestador` §8 según `tipo` y lo que toca la tarea | Nombrar la skill, el momento y la ruta de su SKILL.md. Si hay alguna skill de Emil Kowalski, agregar la línea de "Initial Response"; las que tienen `disable-model-invocation: true` (`review-animations`, `pick-ui-library`, `prototype`) se piden como lectura directa del archivo. |
| `[RESTRICCIONES]` | Aislamiento del harness + alcance de la tarea | Worktree propio; rutas que puede tocar; puerto libre si levanta servidor. |
| `[PROTOCOLO DE DECISIÓN]` | `orquestador` §6 | Va siempre, igual en todas las tareas. |
| `[ENTREGA]` | Convenciones del harness | Commit, autorrevisión, formato del reporte. |

Lo que va entre `<...>` se reemplaza; las líneas marcadas `(si aplica)` se
borran si no aplican. Todo lo demás se copia tal cual.

## Plantilla

```
Eres un sub-agente del harness de orquestación (estás en tu propio git worktree, en una rama propia). No ves la conversación del orquestador: este prompt es todo tu contexto.

[PASO 0 — OBLIGATORIO] Antes de nada, ejecuta `git merge --ff-only main` y confirma que existen <rutas integradas por la wave anterior>. Si el merge falla o falta alguna, no sigas: devuelve DECISION_NEEDED con la salida del comando.

[TAREA] <id> — "<titulo>" — tipo: <tipo> (milestone `<slug>`)

[OBJETIVO]
<descripcion del manifest, ordenada si hace falta, sin cambiar su alcance>

[CRITERIOS DE ACEPTACIÓN] (literales del manifest)
- "<criterio 1, copiado exacto>"
- "<criterio 2, copiado exacto>"
- ...

[VERIFICACIÓN MANUAL] (si aplica; literal del manifest, informativa: no la verificas tú ni bloquea tu cierre)
- "<verificación 1, copiada exacta>"

[CONTEXTO]
- Plan / spec fuente: <ruta> (<secciones citadas por la tarea>)
- Archivos relevantes: <rutas>
- Resultado de tareas previas de las que depende: <id: resumen breve o cápsula de optimizador-tokens> (si aplica)

[SKILLS A APLICAR]
- <skill>: <momento según orquestador §8> (lee .claude/skills/<skill>/SKILL.md)
- <skill con disable-model-invocation>: <momento> (lee y aplica .claude/skills/<skill>/SKILL.md; no se invoca, se lee) (si aplica)
- revision-codigo: autorrevisión antes de reportar (lee .claude/skills/revision-codigo/SKILL.md)
- Skills de Emil Kowalski: ignora su bloque "Initial Response" (el saludo inicial pensado para conversación); esta tarea es tu pregunta específica, aplica directamente el resto de la skill. Si chocan con frontend-design: brief del usuario > frontend-design en identidad visual > Emil en movimiento; stagger solo dentro de un grupo de elementos relacionados, nunca en cascada de secciones. (si aplica)

[RESTRICCIONES]
- Trabajas solo en tu worktree. Toca solo: <rutas permitidas>. Nada más.
- No modifiques otros worktrees ni el checkout principal.
- Si levantas un servidor (dev server, API local), elige un puerto libre y regístralo en tu reporte. (si aplica)
- <restricciones propias de la tarea> (si aplica)

[PROTOCOLO DE DECISIÓN]
Nunca le preguntes al usuario. Si encuentras una ambigüedad real de alto impacto que no puedes resolver con lo que tienes, detente y termina tu turno devolviendo exactamente:
DECISION_NEEDED
tarea: <id>
pregunta: "..."
opciones: ["A", "B"]
contexto: "..."
No commitees trabajo a medias que dependa de la respuesta; quedas pausado y se te reanuda con la respuesta. Para todo lo demás, asume lo razonable y lista los supuestos en tu reporte.

[ENTREGA]
- Un solo commit en tu rama, mensaje en español que empiece por "<id>: ...".
- Antes de commitear: `git status` para confirmar que solo tocaste las rutas permitidas.
- Reporte final (corto): estado (COMPLETADA o DECISION_NEEDED), nombre de rama, hash del commit, archivos creados/modificados, cada criterio de aceptación con cómo lo verificaste, supuestos tomados.
```
