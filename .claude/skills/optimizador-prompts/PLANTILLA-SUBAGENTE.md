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
| `[CONTEXTO]` | Rutas y documentos citados por la tarea; resultados relevantes de waves previas | Documentos largos: la ruta **con la sección** que toca (`PLAN.md §4 N1`), nunca "lee el plan". Si el contexto de referencia supera el umbral de `optimizador-tokens`, va la cápsula que devuelve su modo `capsula`, tal cual. El código a editar no se copia: se pasa la ruta. |
| `[SKILLS A APLICAR]` | Tabla de `orquestador` §8 según `tipo` y lo que toca la tarea | Nombrar la skill, el momento y la ruta de su SKILL.md. Si hay alguna skill de Emil Kowalski, agregar la línea de "Initial Response"; las que tienen `disable-model-invocation: true` (`review-animations`, `pick-ui-library`, `prototype`) se piden como lectura directa del archivo. |
| `[RESTRICCIONES]` | Aislamiento del harness + alcance de la tarea | Worktree propio; rutas que puede tocar; puerto libre si levanta servidor. |
| `[EFICIENCIA]` | Perfil de costo del harness (`orquestador` §1, `PROCESO.md` §15) | Va siempre, igual en todas las tareas. La línea de fuentes solo si la tarea investiga. |
| `[PROTOCOLO DE DECISIÓN]` | `orquestador` §6 | Va siempre, igual en todas las tareas. |
| `[ENTREGA]` | Convenciones del harness | Commits de avance, autorrevisión, formato del reporte. |

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
- revision-codigo: autorrevisión antes de reportar (lee .claude/skills/revision-codigo/SKILL.md) (si hay código)
- verificador-datos, nivel <ligera|completa>: antes de reportar (lee .claude/skills/verificador-datos/SKILL.md; aplica solo la sección de tu nivel) (si la verificacion de la tarea no es `ninguna`)
- Skills de Emil Kowalski: ignora su bloque "Initial Response" (el saludo inicial pensado para conversación); esta tarea es tu pregunta específica, aplica directamente el resto de la skill. Si chocan con frontend-design: brief del usuario > frontend-design en identidad visual > Emil en movimiento; stagger solo dentro de un grupo de elementos relacionados, nunca en cascada de secciones. (si aplica)

[RESTRICCIONES]
- Trabajas solo en tu worktree. Toca solo: <rutas permitidas>. Nada más.
- No modifiques otros worktrees ni el checkout principal.
- Si levantas un servidor (dev server, API local), elige un puerto libre y regístralo en tu reporte. (si aplica)
- <restricciones propias de la tarea> (si aplica)

[EFICIENCIA]
Cada llamada que haces relee todo tu contexto, así que:
- Agrupa comandos en un solo Bash (`cmd1 && cmd2 && cmd3`). No corras un comando para confirmar lo que el anterior ya mostró.
- Lee por secciones: `grep -n` para ubicar y Read con offset/limit. No leas completo un archivo de más de ~300 líneas salvo que tu tarea sea reescribirlo. No releas un archivo que no cambió.
- Si reescribes más de la mitad de un archivo, un Write completo en vez de muchos Edit.
- Fuentes (si la tarea investiga): al escribir cada dato, deja su URL o referencia junto a él. Una búsqueda por dato; no repitas búsquedas. El verificador usará esas URL en vez de buscar de nuevo. (si aplica)

[PROTOCOLO DE DECISIÓN]
Nunca le preguntes al usuario. Si encuentras una ambigüedad real de alto impacto que no puedes resolver con lo que tienes, detente y termina tu turno devolviendo exactamente:
DECISION_NEEDED
tarea: <id>
pregunta: "..."
opciones: ["A", "B"]
contexto: "..."
No commitees trabajo a medias que dependa de la respuesta; quedas pausado y se te reanuda con la respuesta. Para todo lo demás, asume lo razonable y lista los supuestos en tu reporte.

[ENTREGA]
- Commit de avance en tu rama cada vez que cierres un entregable completo (un archivo o una prueba terminada), con mensaje en español que empiece por "<id>: ...". Si la sesión se corta, ese trabajo no se pierde.
- Antes de cada commit: `git status --short` para confirmar que solo tocaste las rutas permitidas.
- Reporte final de máximo ~15 líneas, sin pegar contenido de archivos: estado (COMPLETADA o DECISION_NEEDED), nombre de rama, hash del último commit, archivos creados/modificados, cada criterio de aceptación con cómo lo verificaste (una línea cada uno), supuestos tomados.
```
