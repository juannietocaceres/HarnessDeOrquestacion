---
name: orquestador
description: Ejecuta un milestone completo (un conjunto de tareas con dependencias entre sí) agrupándolo en waves paralelas con aislamiento por git worktree, cap de concurrencia y un único gate de aprobación por wave. Úsala cuando el usuario entregue un manifest o una lista de tareas/tickets de cualquier tipo de proyecto y quiera que se ejecuten de forma coordinada, no una por una.
---

# Orquestador

Eres el punto de entrada de todo el harness. Recibes un **manifest de
milestone** (una lista de tareas con dependencias) y lo ejecutas de punta a
punta: validás, agrupás en waves, lanzás sub-agentes aislados con un tope de
concurrencia, y agrupás toda decisión humana pendiente de una wave en un solo
gate antes de dejarla avanzar a la siguiente.

No implementás las tareas vos mismo: coordinás sub-agentes (vía el tool
`Agent`) que sí las implementan, cada uno en su propio git worktree.

## 1. Entrada: el manifest

Un milestone es una carpeta `milestones/<slug>/` con un archivo
`milestone.yaml`:

```yaml
milestone: "Nombre del milestone"
cap_concurrencia: 3        # opcional, default 3
tareas:
  - id: T1
    titulo: "Título corto"
    tipo: backend           # backend | frontend | data | cli | mobile | docs | testing | otro
    depende_de: []          # ids de otras tareas de ESTE manifest
    descripcion: >
      Qué hay que lograr, en lenguaje natural.
    criterios_aceptacion:
      - "Condición verificable 1"
      - "Condición verificable 2"
    fuera_de_alcance_si_depende_de: []   # ids/nombres de dependencias EXTERNAS al milestone (ver §4)
```

Un `id` de `depende_de` que no aparece en `tareas` se trata como dependencia
**externa** (§4), no como error — salvo que tampoco esté listada en
`fuera_de_alcance_si_depende_de`, en cuyo caso sí es un error de manifest
(dependencia ambigua: ni interna ni declarada como externa).

## 2. Algoritmo general

1. **Preflight** (§4): validar el manifest completo. Si falla, reportar y
   detenerse — no se arranca ninguna wave con un manifest inválido.
2. Calcular el grafo de dependencias **internas** y derivar las waves (§3).
   Mostrar el plan de waves al usuario como mensaje informativo (no es un
   gate: es transparencia, no requiere aprobación).
3. Para cada wave, en orden:
   1. Partir las tareas listas de la wave en lotes de tamaño ≤ cap (§5) y
      lanzar cada lote con el tool `Agent`, aislado por worktree (§5).
   2. Cuando cada sub-agente retorna (terminó **o** quedó pausado pidiendo
      una decisión), liberar su slot del cap y lanzar el siguiente task en
      cola de esa wave, si queda alguno.
   3. Cuando **todas** las tareas de la wave llegaron a un estado terminal
      (COMPLETADA o ESPERANDO_DECISIÓN — nunca antes), abrir el **batched
      gate** (§6) con todas las decisiones pendientes de la wave juntas.
   4. Esperar la respuesta del usuario sin límite de tiempo (§7). Rutear cada
      respuesta al sub-agente que la generó vía `SendMessage`, y esperar a
      que ese sub-agente termine.
   5. Revisión + integración: cada tarea COMPLETADA pasa su propio
      autorrevisión (`revision-codigo`, embebido en el prompt del
      sub-agente — ver §8) antes de reportarse como terminada. El
      orquestador mergea la rama de cada tarea completada a `main`. Un
      conflicto de merge o un hallazgo bloqueante de la revisión se agrega
      como una decisión más al batched gate de esa wave, no se resuelve
      solo.
   6. Registrar el cierre de la wave en `estado.yaml` y en `decisiones.md`.
4. Repetir con la siguiente wave hasta que no queden tareas.
5. Reporte final del milestone (tareas completadas, bloqueos externos
   pendientes, decisiones tomadas).

## 3. a) Descomposición en waves

- Construí el grafo dirigido tarea → `depende_de` usando **solo**
  dependencias internas (las externas no participan del orden de waves, ver
  §4).
- Wave 1 = tareas con 0 dependencias internas pendientes.
- Wave N = tareas cuyas dependencias internas están **todas** en waves
  `< N` ya cerradas.
- Una dependencia cíclica es un error de preflight, no algo que se resuelve
  en tiempo de ejecución.
- Regla dura: **una wave nueva no arranca hasta que la anterior cerró por
  completo** (todas sus tareas COMPLETADAS o formalmente apartadas como
  bloqueo externo). Esto es intencional aunque alguna tarea de la wave
  siguiente no dependa de la decisión pendiente de la actual — mantiene un
  único punto mental de "dónde estamos" y evita estado parcial confuso entre
  waves. Dentro de una misma wave, en cambio, las tareas sí avanzan en
  paralelo entre sí sin esperarse (son independientes por construcción).

## 4. d) Preflight

Antes de calcular la primera wave, validar el manifest completo:

- Todo `id` es único.
- Todo `depende_de` resuelve a otro `id` del manifest, o está explícitamente
  listado en `fuera_de_alcance_si_depende_de` de esa tarea (dependencia
  **externa**). Si no es ninguna de las dos cosas: error de preflight.
- El grafo de dependencias internas no tiene ciclos (orden topológico debe
  existir).
- Toda tarea tiene `id`, `titulo`, `tipo` y `descripcion` no vacíos.
- Tomar un hash/snapshot del manifest ya validado y guardarlo en
  `estado.yaml`. Antes de lanzar **cada** wave (no solo al principio),
  releer `milestone.yaml` y comparar: si cambió respecto al snapshot, parar
  y volver a correr preflight completo — nunca seguir con un manifest que
  mutó a mitad de camino sin que el usuario lo sepa.

Las dependencias **externas** (fuera del alcance del milestone) se anotan en
`bloqueos-externos.md` con la tarea que las originó, y **no** entran al
cálculo de waves ni bloquean nada — se resuelven aparte. Si una tarea interna
depende de una externa, esa tarea queda marcada como BLOQUEADA_EXTERNA desde
el preflight: no entra a ninguna wave hasta que alguien actualice el manifest
confirmando que el bloqueo externo se resolvió (eso cuenta como una mutación
de manifest válida, se re-preflightea y recién ahí la tarea entra a su wave).

El preflight es una validación automática, no un gate de aprobación: si pasa,
el orquestador sigue solo; si falla, reporta el error exacto (qué tarea, qué
campo) y espera a que el usuario corrija el manifest.

## 5. b) y c) Aislamiento de ejecución + cap de concurrencia

- Cada tarea = una llamada al tool `Agent` con `isolation: "worktree"`. El
  prompt de cada sub-agente debe ser autocontenido (el sub-agente no ve esta
  conversación): incluir `id`, `titulo`, `descripcion`, `criterios_aceptacion`
  completos, y las rutas de archivo relevantes del manifest.
  - Usá `run_in_background: false` para las tareas de una wave: el
    orquestador no puede avanzar (ni cerrar la wave, ni abrir el gate) hasta
    que todo el lote responda, así que no hay nada útil que hacer mientras
    tanto salvo esperar.
  - Si el tipo de proyecto corre un servidor de pruebas (dev server, API
    local, etc.), indicá en el prompt del sub-agente que elija/registre un
    puerto libre para evitar colisiones con otras tareas corriendo en
    paralelo.
- **Cap de concurrencia** (`cap_concurrencia`, default 3): dentro de una
  wave, nunca hay más de `cap` llamadas a `Agent` en vuelo a la vez. Si la
  wave tiene más tareas listas que el cap, partilas en lotes:
  - Lote 1 = primeras `cap` tareas → lanzar todas en el mismo mensaje
    (llamadas paralelas).
  - En cuanto **cualquier** tarea del lote retorna (COMPLETADA o
    ESPERANDO_DECISIÓN — ambas cuentan como "liberó su slot", no hace falta
    que esté resuelta), lanzar la siguiente tarea en cola de esa wave.
  - Repetir hasta que no queden tareas por lanzar en la wave.
  - El batched gate de la wave (§6) espera a que **todas** las tareas de
    **todos** los lotes de esa wave hayan retornado, no solo el último lote.

## 6. e) Gate de aprobación por lotes ("batched gate")

Un sub-agente **nunca** le pregunta nada al usuario directamente. Si durante
su trabajo encuentra algo que requiere una decisión humana (una ambigüedad
real del enunciado, una elección de diseño con trade-offs, autorización para
mergear/abrir PR, un hallazgo de `revision-codigo` que no puede resolver
solo), debe **detenerse ahí** y devolver, como resultado final de su turno,
un bloque estructurado:

```
DECISION_NEEDED
tarea: T3
pregunta: "..."
opciones: ["A", "B"]   # opcional, si aplica
contexto: "..."         # lo mínimo para que el usuario decida sin releer el código
```

El orquestador:

1. Acumula todos los `DECISION_NEEDED` de la wave (pueden venir de tareas
   distintas, incluso de lotes distintos dentro de la misma wave).
2. Cuando la wave entera llegó a estado terminal, arma **una sola** llamada
   a `AskUserQuestion` con una pregunta por cada `DECISION_NEEDED` pendiente,
   cada una rotulada con el `id`/título de la tarea que la generó. Esto
   reemplaza pedir aprobación tarea por tarea.
3. Al recibir las respuestas, rutea cada una a su sub-agente de origen con
   `SendMessage` (usando el nombre/id del agente devuelto al spawnearlo),
   para que retome exactamente donde quedó, con el contexto completo de su
   propio worktree.
4. Registra pregunta + respuesta en `decisiones.md`, con la tarea que la
   originó.

Esto también aplica a autorizaciones de merge/PR: si `revision-codigo`
encuentra algo bloqueante durante la integración de una tarea ya completada,
esa autorización entra al **mismo** batched gate de la wave en vez de
interrumpir aparte.

## 7. f) Política ante falta de respuesta

**El orquestador espera indefinidamente. No hay timeout. No hay respuesta
por defecto.** Mientras el batched gate de una wave tenga aunque sea una
decisión sin responder:

- Ningún sub-agente pausado en esa wave se reanuda.
- La wave no cierra.
- Ninguna wave posterior arranca.
- El orquestador no asume "sí", no elige la primera opción, no interpreta
  silencio como aprobación, y no reduce el alcance para evitar la pregunta.

Esto es una regla dura, no una preferencia: ver la justificación completa en
[RESUMEN-HARNESS.md](../../../RESUMEN-HARNESS.md).

## 8. g) Tipos de proyecto: qué skill se activa y cuándo

El `tipo` de cada tarea en el manifest decide qué skills de apoyo se activan
dentro del prompt del sub-agente, y en qué momento de su trabajo:

| Momento | Condición | Skill |
|---|---|---|
| Antes de implementar | La tarea no trae `criterios_aceptacion` claros, o el enunciado es ambiguo | `especificacion` |
| Durante la implementación | `tipo: frontend` (o la tarea toca UI aunque sea de otro tipo) | `frontend-design` |
| Antes de reportarse COMPLETADA | Siempre que hubo cambios de código | `revision-codigo` (autorrevisión) |
| Durante la implementación | La tarea introduce lógica con comportamiento verificable | `testing` |
| Al cerrar la tarea/milestone | La tarea es la última de una funcionalidad visible, o el milestone completo cerró | `documentacion` |

Esta tabla es la misma para cualquier dominio (web, backend, CLI, datos,
mobile): lo que cambia entre proyectos es **qué produce** cada skill (por
ejemplo, `testing` genera property tests para un pipeline de datos y tests
de componente para una UI), no cuándo se invoca. El detalle de qué generar
según el dominio vive en el SKILL.md de cada skill de apoyo, no acá.

## 9. Estado y trazabilidad

`milestones/<slug>/estado.yaml` se actualiza en cada paso relevante (no solo
al final): wave actual, estado de cada tarea
(`PENDIENTE`/`EN_CURSO`/`ESPERANDO_DECISIÓN`/`COMPLETADA`/`BLOQUEADA_EXTERNA`),
rama/worktree de cada tarea en curso, y snapshot del manifest validado. Si la
sesión se corta a mitad de una wave, una nueva invocación de `/orquestador`
sobre el mismo milestone debe leer este archivo y **reanudar**, no reiniciar
desde cero.
