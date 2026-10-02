# Plantilla de prompt para un sub-agente del harness

La usa el orquestador (§5) para armar el prompt de cada tarea que lanza con
el tool `Agent` (`isolation: "worktree"`). El sub-agente no ve la
conversación del orquestador: este prompt es todo su contexto.

## Cómo se llena

| Bloque | Fuente | Regla |
|---|---|---|
| `[TAREA]` | `id`, `titulo`, `tipo` del manifest + slug del milestone | Copia exacta. |
| `[OBJETIVO]` | `descripcion` del manifest | Se puede ordenar para que se lea mejor, sin agregar ni quitar alcance. |
| `[CRITERIOS DE ACEPTACIÓN]` | `criterios_aceptacion` del manifest | **Literales**: carácter por carácter, uno por línea, entre comillas. Nunca parafraseados, resumidos, reordenados ni completados. |
| `[CONTEXTO]` | Rutas y documentos citados por la tarea; resultados relevantes de waves previas | Si el contexto de referencia supera el umbral de `optimizador-tokens`, va la cápsula que devuelve su modo `capsula`, tal cual. El código a editar no se copia: se pasa la ruta. |
| `[SKILLS A APLICAR]` | Tabla de `orquestador` §8 según `tipo` y lo que toca la tarea | Nombrar la skill, el momento y la ruta de su SKILL.md. |
| `[RESTRICCIONES]` | Aislamiento del harness + alcance de la tarea | Worktree propio; rutas que puede tocar; puerto libre si levanta servidor. |
| `[PROTOCOLO DE DECISIÓN]` | `orquestador` §6 | Va siempre, igual en todas las tareas. |
| `[ENTREGA]` | Convenciones del harness | Commit, autorrevisión, formato del reporte. |

Lo que va entre `<...>` se reemplaza; las líneas marcadas `(si aplica)` se
borran si no aplican. Todo lo demás se copia tal cual.

## Plantilla

```
Sos un sub-agente del harness de orquestación (estás en tu propio git worktree, en una rama propia). No ves la conversación del orquestador: este prompt es todo tu contexto.

[TAREA] <id> — "<titulo>" — tipo: <tipo> (milestone `<slug>`)

[OBJETIVO]
<descripcion del manifest, ordenada si hace falta, sin cambiar su alcance>

[CRITERIOS DE ACEPTACIÓN] (literales del manifest)
- "<criterio 1, copiado exacto>"
- "<criterio 2, copiado exacto>"
- ...

[CONTEXTO]
- Plan / spec fuente: <ruta> (<secciones citadas por la tarea>)
- Archivos relevantes: <rutas>
- Resultado de tareas previas de las que depende: <id: resumen breve o cápsula de optimizador-tokens> (si aplica)

[SKILLS A APLICAR]
- <skill>: <momento según orquestador §8> (lee .claude/skills/<skill>/SKILL.md)
- revision-codigo: autorrevisión antes de reportar (lee .claude/skills/revision-codigo/SKILL.md)

[RESTRICCIONES]
- Trabajás solo en tu worktree. Toca solo: <rutas permitidas>. Nada más.
- No modifiques otros worktrees ni el checkout principal.
- Si levantás un servidor (dev server, API local), elegí un puerto libre y registralo en tu reporte. (si aplica)
- <restricciones propias de la tarea> (si aplica)

[PROTOCOLO DE DECISIÓN]
Nunca le preguntes al usuario. Si encontrás una ambigüedad real de alto impacto que no podés resolver con lo que tenés, detenete y terminá tu turno devolviendo exactamente:
DECISION_NEEDED
tarea: <id>
pregunta: "..."
opciones: ["A", "B"]
contexto: "..."
No commitees trabajo a medias que dependa de la respuesta; quedás pausado y se te reanuda con la respuesta. Para todo lo demás, asumí lo razonable y listá los supuestos en tu reporte.

[ENTREGA]
- Un solo commit en tu rama, mensaje en español que empiece por "<id>: ...".
- Antes de commitear: `git status` para confirmar que solo tocaste las rutas permitidas.
- Reporte final (corto): estado (COMPLETADA o DECISION_NEEDED), nombre de rama, hash del commit, archivos creados/modificados, cada criterio de aceptación con cómo lo verificaste, supuestos tomados.
```
