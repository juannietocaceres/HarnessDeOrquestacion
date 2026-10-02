---
name: optimizador-prompts
description: Convierte ideas desordenadas, notas o instrucciones incompletas en prompts claros y estructurados para la herramienta de IA destino, incluido el prompt autocontenido de un sub-agente del harness. Se usa cuando hay que escribir, ordenar o mejorar una instrucción para una IA, o cuando el orquestador arma el prompt de una tarea.
---

# Optimizador de prompts

Conviertes ideas caóticas, notas rápidas o instrucciones incompletas en
prompts precisos y listos para usar. El foco es la **claridad**: que la IA
que recibe el prompt entienda qué se quiere, con qué límites y cómo se sabe
que terminó bien.

## Frontera con `optimizador-tokens`

Las dos skills trabajan sobre texto que va a leer una IA, pero optimizan
cosas distintas y no se pisan:

| | `optimizador-prompts` (esta) | `optimizador-tokens` |
|---|---|---|
| Optimiza | **Claridad** (humano → IA) | **Densidad** (IA → IA) |
| Entrada típica | Una idea, un pedido mal escrito, una tarea del manifest | Contexto de referencia ya claro pero largo (resultados de waves, decisiones, docs) |
| Puede alargar el texto | Sí, si falta información (objetivo, criterios, formato) | No: solo poda, nunca agrega |
| Salida | Un prompt estructurado | Un bloque compacto (`[CONTEXTO]` del sub-agente o `contexto-compacto.md`) |

Regla de convivencia: esta skill **arma la estructura** del prompt; si el
contexto de referencia supera el umbral de `optimizador-tokens`, el bloque
`[CONTEXTO]` se llena con la cápsula que devuelve esa skill, sin reescribirla.
Esta skill no comprime, y `optimizador-tokens` no reescribe criterios,
objetivos ni restricciones.

## Modo de ejecución: interactivo o no interactivo

- **Interactivo** (invocada suelta por el usuario): si falta información
  imprescindible, puedes preguntar (máximo 2–3 preguntas, en "Dudas
  opcionales").
- **No interactivo** (corre dentro del orquestador o de un sub-agente del
  harness): **no hagas preguntas**. Asume lo razonable, sigue, y lista los
  supuestos en la sección "Supuestos" de la respuesta. Si un supuesto es de
  alto impacto (cambiaría el objetivo, el alcance o los criterios de la
  tarea), no lo asumas: devuelve un bloque `DECISION_NEEDED` con el formato de
  `orquestador` §6 para que entre al batched gate de la wave.

Ante la duda sobre en qué modo estás: si el pedido llega desde un prompt del
orquestador o de un sub-agente (no del usuario en el chat), es no interactivo.

## Proceso

### 1. Detecta la herramienta objetivo

Antes de generar el prompt, identifica **para qué herramienta o modelo** se
va a usar:

- Claude, ChatGPT, Gemini (conversacionales/texto)
- Claude Code u otras herramientas de programación
- **Sub-agente del harness** (una tarea de un milestone; ver la sección
  propia más abajo)
- Midjourney, Flux, Stable Diffusion, Firefly (imagen)
- Sora, Kling, Runway (video)
- n8n, Make, Zapier (automatizaciones)

Si no queda claro: en modo interactivo, pregunta; en modo no interactivo,
elige la más probable y anótala como supuesto.

### 2. Extrae los componentes del prompt

Del input, identifica:

1. **Objetivo real**: qué se quiere conseguir.
2. **Contexto relevante**: rol, situación, datos de partida.
3. **Tarea concreta**: acción específica que debe ejecutar la IA.
4. **Especificaciones**: detalles técnicos, restricciones, tono, estilo.
5. **Formato de salida**: cómo debe presentarse el resultado.
6. **Criterios de calidad**: qué hace que el resultado sea bueno.
7. **Cosas a evitar**: errores frecuentes, restricciones, exclusiones.
8. **Verificación final**: si aplica, instrucción de autocomprobación.

Si falta algo imprescindible, aplica la regla del modo de ejecución (arriba).
Si no es crítico, asume lo razonable y sigue.

### 3. Construye el prompt final

Estructura general (adáptala según la herramienta y la complejidad):

```
[CONTEXTO Y ROL]
Quién es la IA, desde qué perspectiva actúa y en qué situación.

[TAREA CONCRETA]
Qué debe hacer exactamente.

[ESPECIFICACIONES]
Detalles importantes: tono, estilo, longitud, idioma, público objetivo, restricciones.

[CRITERIOS DE CALIDAD]
Cómo saber si el resultado es bueno.

[FORMATO DE RESPUESTA]
Cómo debe estructurarse la salida: listas, párrafos, tablas, JSON, etc.

[VERIFICACIÓN FINAL] (opcional)
Instrucción de autocomprobación antes de responder.
```

Para un sub-agente del harness no se usa esta estructura sino la plantilla
fija de la sección siguiente.

## Adaptación por herramienta

### Sub-agente del harness

Es el prompt que el orquestador le pasa al tool `Agent` para cada tarea de
una wave (`orquestador` §5). El sub-agente no ve la conversación del
orquestador: el prompt es **todo** su contexto, así que tiene que ser
autocontenido.

Se arma siempre con [PLANTILLA-SUBAGENTE.md](PLANTILLA-SUBAGENTE.md), con
estos bloques en este orden:

```
[PASO 0] git merge --ff-only main + comprobar archivos de la wave anterior
[TAREA] id, título, tipo
[OBJETIVO] descripción
[CRITERIOS DE ACEPTACIÓN] lista literal del manifest (nunca parafrasear)
[VERIFICACIÓN MANUAL] lista literal, informativa (solo si la tarea la declara)
[CONTEXTO] cápsula de optimizador-tokens + rutas relevantes
[SKILLS A APLICAR] según orquestador §8
[RESTRICCIONES] worktree propio, puerto libre si levanta servidor, no tocar otras carpetas
[PROTOCOLO DE DECISIÓN] bloque DECISION_NEEDED si hay ambigüedad real
[ENTREGA] qué archivos, qué commit, autorrevisión antes de reportar
```

Reglas específicas de este destino:

- **Criterios de aceptación literales.** Se copian carácter por carácter
  desde `criterios_aceptacion` del manifest, uno por línea, entre comillas.
  Nunca se parafrasean, resumen, reordenan por "claridad" ni se completan.
  Si un criterio parece ambiguo, se deja igual y la ambigüedad se señala
  aparte (o se resuelve con `especificacion` antes de lanzar la tarea), nunca
  reescribiéndolo.
- **La claridad se agrega alrededor, no encima.** Donde esta skill aporta es
  en `[OBJETIVO]` (ordenar la `descripcion` si viene desprolija, sin cambiar
  su alcance), en `[CONTEXTO]` (rutas concretas, secciones del plan citadas)
  y en `[RESTRICCIONES]` (qué carpetas puede tocar y cuáles no).
- **IDs, rutas, puertos, versiones y nombres de ramas** se copian exactos.
- **`verificacion_manual`** se copia literal, igual que los criterios, y se
  marca como informativa: el sub-agente no la verifica ni bloquea su cierre
  por ella (`orquestador` §1).
- **`modelo`** no va en el texto del prompt: el orquestador lo pasa como
  parámetro `model` del tool `Agent` (`orquestador` §5).
- **`[PASO 0]`** va siempre: los worktrees pueden arrancar desde un commit
  viejo, así que el sub-agente sincroniza con `main` y comprueba los
  archivos de la wave anterior antes de empezar (`orquestador` §5).
- **`[SKILLS A APLICAR]`** sale de la tabla de `orquestador` §8 según el
  `tipo` de la tarea y lo que toca (p. ej. `revision-codigo` siempre que hay
  cambios de código; `frontend-design` si toca UI; `testing` si hay lógica
  verificable).
- **`[PROTOCOLO DE DECISIÓN]`** va siempre, aunque la tarea parezca obvia:
  el sub-agente nunca le pregunta al usuario (`orquestador` §6).
- No se agregan saludos, explicaciones sobre prompting ni disclaimers: el
  sub-agente necesita instrucciones, no contexto de cortesía.

### Claude / ChatGPT / Gemini (texto y conversacional)

- Prioriza contexto claro, pasos definidos y formato de salida explícito.
- Agrega instrucción de rol si el caso lo requiere.
- Si es un sistema de prompts, separa el system prompt del user message.

### Claude Code / herramientas de programación

- Incluye: objetivo del código, lenguaje/framework, estructura del proyecto si
  se conoce.
- Agrega restricciones técnicas, comportamiento esperado, archivos afectados.
- Define criterios de validación y casos límite.
- Especifica si debe explicar el código o solo entregarlo.

### Midjourney / Flux / Stable Diffusion / herramientas de imagen

- Estructura: sujeto principal → composición → estilo visual → iluminación →
  encuadre → relación de aspecto → ambiente.
- Agrega elementos obligatorios y lista de elementos a evitar (negative
  prompts si aplica).
- Adapta el formato a la herramienta (Midjourney usa `--ar`, `--style`; SD
  usa `negative prompt:`).

### Sora / Kling / Runway / herramientas de video

- Incluye: escena de apertura, movimiento de cámara, acción principal,
  progresión visual.
- Agrega estilo, duración aproximada, ambiente sonoro si aplica.
- Especifica continuidad visual si es parte de una secuencia.

### n8n / Make / Zapier / automatizaciones

- Incluye: trigger, inputs, pasos del flujo en orden, herramientas conectadas,
  output esperado.
- Agrega casos límite, manejo de errores y qué debe pasar si falla un paso.

## Formato de respuesta

Devuelve **siempre** en este orden:

---

**Prompt optimizado:**

[Prompt final limpio, listo para copiar y pegar]

---

**Cambios principales realizados:**

[Lista breve de 3 a 5 mejoras aplicadas: qué faltaba, qué se ordenó, qué se agregó]

---

**Dudas opcionales:** *(solo en modo interactivo, y solo si hay información que mejoraría mucho el resultado)*

[Preguntas concretas, máximo 2–3]

**Supuestos:** *(en modo no interactivo, en lugar de las dudas)*

[Cada supuesto que tomaste en vez de preguntar]

---

Cuando el orquestador usa esta skill para armar el prompt de un sub-agente,
solo le hace falta el **Prompt optimizado** (va directo al tool `Agent`); los
cambios y supuestos se registran en el estado de la tarea si son relevantes,
no se le pasan al sub-agente.

## Reglas

- No inventes detalles críticos que no se dieron.
- No cambies el objetivo original.
- No parafrasees criterios de aceptación: van literales.
- No hagas el prompt más largo de lo necesario (pero tampoco lo comprimas:
  eso es trabajo de `optimizador-tokens`).
- No uses lenguaje corporativo, genérico o artificioso si se busca
  naturalidad.
- No metas disclaimers ni advertencias innecesarias dentro del prompt.
- No des varias versiones salvo que se pidan explícitamente.
- No expliques metodologías ni teorías sobre prompting si no se pidió.
- El resultado debe ser inmediatamente usable.
