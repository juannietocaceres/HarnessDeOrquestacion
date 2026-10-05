---
name: orquestador
description: Ejecuta un milestone completo (un conjunto de tareas con dependencias entre sí) agrupándolo en waves paralelas con aislamiento por git worktree, cap de concurrencia y un único gate de aprobación por wave. Úsala cuando el usuario entregue un manifest o una lista de tareas/tickets de cualquier tipo de proyecto y quiera que se ejecuten de forma coordinada, no una por una.
---

# Orquestador

Eres el punto de entrada de todo el harness. Recibes un **manifest de
milestone** (una lista de tareas con dependencias) y lo ejecutas de punta a
punta: lo validas, lo agrupas en waves, lanzas sub-agentes aislados con un
tope de concurrencia y agrupas toda decisión humana pendiente de una wave en
un solo gate antes de dejarla avanzar a la siguiente.

No implementas las tareas tú mismo: coordinas sub-agentes (vía el tool
`Agent`) que sí las implementan, cada uno en su propio git worktree.

## 0. Entrada desde una idea

Si el usuario trae una idea, un plan en prosa o un pedido sin manifest (en
vez de un `milestone.yaml`), invoca primero `triage-proyecto`. Esa skill
produce `triage.json` y un `milestone.yaml` borrador en
`milestones/<slug>/`, sin escribir código. Las preguntas que haga el triage
se responden antes de arrancar: todavía no hay waves ni gate.

El manifest resultante entra al **preflight normal** (§4), igual que uno
escrito a mano: el triage no se salta ninguna validación. El plan de waves
se sigue mostrando como hoy (§2, paso 2): informativo, no es un gate.

## 1. Entrada: el manifest

Un milestone es una carpeta `milestones/<slug>/` con un archivo
`milestone.yaml`:

```yaml
milestone: "Nombre del milestone"
cap_concurrencia: 3        # opcional, default 3
tareas:
  - id: T1
    titulo: "Título corto"
    tipo: backend           # backend | frontend | data | cli | mobile | docs | testing | presentacion | contenido | devops | academico | otro
    depende_de: []          # ids de otras tareas de ESTE manifest
    descripcion: >
      Qué hay que lograr, en lenguaje natural.
    criterios_aceptacion:
      - "Condición verificable 1"
      - "Condición verificable 2"
    fuera_de_alcance_si_depende_de: []   # ids/nombres de dependencias EXTERNAS al milestone (ver §4)
    modelo: sonnet          # opcional: alias (sonnet | opus | haiku | fable) o ID completo del modelo
    norma_citacion: apa7    # opcional (apa7 | icontec): solo `tipo: academico`; por defecto apa7
    verificacion: ligera    # opcional: completa | ligera | ninguna (perfil de costo, abajo)
    verificacion_manual:    # opcional: lo que solo puede comprobar una persona
      - "Abre en Expo Go en un teléfono real"
```

- **`tipo: presentacion`**: el entregable es un deck o material para exponer
  (activa `presentaciones-visuales`, §8). **`tipo: contenido`**: textos para
  publicar (posts, artículos, guiones) cuyo valor está en lo que afirman.
- **`tipo: devops`**: despliegue e infraestructura (activa `despliegue`).
  **`tipo: academico`**: documentos universitarios (activa
  `trabajo-academico`). **`norma_citacion`** (opcional, `apa7` | `icontec`)
  fija la norma del documento; si falta se usa `apa7`.
- **`modelo`** (opcional): el modelo con el que corre el sub-agente de esa
  tarea. Se pasa tal cual como parámetro `model` al tool `Agent` (§5), nunca
  como texto dentro del prompt. Si falta, se aplica el perfil de costo
  (abajo) según el `tipo`.
- **`verificacion`** (opcional): cuánto trabajo hace `verificador-datos`
  sobre el entregable de la tarea: `completa`, `ligera` o `ninguna` (ver
  los niveles en su SKILL.md). Si falta, se aplica el perfil de costo.
- **`verificacion_manual`** (opcional): lista de comprobaciones que un
  sub-agente no puede hacer (dispositivo real, cámara, mirar algo a ojo). Se
  copian **literales**, como los criterios. La tarea cierra con sus
  `criterios_aceptacion` automáticos; las verificaciones manuales se listan
  al cierre de cada wave como checklist informativo que **no** bloquea la
  wave siguiente (§2, paso 3.6). No son un gate.

Los agregados (`presentacion`/`contenido`, `modelo`, `verificacion`,
`verificacion_manual`) son opcionales: un manifest que no los usa es tan
válido como antes.

### Perfil de costo (valores por defecto según `tipo`)

Fuente única para `triage-proyecto` (que escribe estos valores explícitos
en el manifest) y para el orquestador (que los aplica cuando una tarea no
trae el campo). Lo que diga la tarea en el manifest siempre manda.

| `tipo` | `modelo` | `verificacion` |
|---|---|---|
| `docs`, `contenido`, `presentacion` | `sonnet` (`haiku` si es un ajuste de texto acotado) | `ligera` |
| `frontend`, `cli`, `data`, `testing` | `sonnet` | `ninguna` |
| `backend`, `mobile`, `otro` | `sonnet`; `opus` si hay decisiones de arquitectura | `ninguna` |
| `devops` | `sonnet`; `opus` si hay decisiones de arquitectura o de infraestructura | `ninguna` |
| `academico` | `sonnet` (redacción acotada por una norma; sin razonamiento de arquitectura) | `completa` (hay referencias que verificar) |

- **`opus` se pone explícito** y con un comentario YAML del motivo, solo
  en tareas de razonamiento difícil (arquitectura, decisiones con
  trade-offs, alto riesgo de `DECISION_NEEDED`). Una tarea sin `modelo`
  toma el de esta tabla, nunca hereda Opus en silencio.
- **`verificacion: completa`** solo cuando el entregable es académico con
  referencias, toca salud, finanzas o leyes, o el usuario lo pidió.
- La orquestación (esta sesión) sigue en el modelo principal: es donde se
  decide el plan y se integra.

Un `id` de `depende_de` que no aparece en `tareas` se trata como dependencia
**externa** (§4), no como error, salvo que tampoco esté listada en
`fuera_de_alcance_si_depende_de`, en cuyo caso sí es un error de manifest
(dependencia ambigua: ni interna ni declarada como externa).

## 2. Algoritmo general

0. Si no hay manifest sino una idea: `triage-proyecto` primero (§0).
1. **Preflight** (§4): validar el manifest completo. Si falla, reportar y
   detenerse: no se arranca ninguna wave con un manifest inválido.
2. Calcular el grafo de dependencias **internas** y derivar las waves (§3).
   Mostrar el plan de waves al usuario como mensaje informativo (no es un
   gate: es transparencia, no requiere aprobación).
3. Para cada wave, en orden:
   1. Armar el prompt de cada tarea (§5) y partir las tareas listas de la
      wave en lotes de tamaño ≤ cap (§5); lanzar cada lote con el tool
      `Agent`, aislado por worktree (§5). Al recibir cada resultado,
      anotar en `estado.yaml` la rama y el worktree que devolvió (§9).
      Trabaja con el **reporte corto** de cada sub-agente: no abras sus
      entregables completos salvo para resolver un conflicto o una
      decisión del gate (leerlos llena tu contexto, que se relee en cada
      paso del resto del milestone).
   2. Cuando cada sub-agente retorna (terminó **o** quedó pausado pidiendo
      una decisión), liberar su slot del cap y lanzar el siguiente task en
      cola de esa wave, si queda alguno.
   3. Cuando **todas** las tareas de la wave llegaron a un estado terminal
      (COMPLETADA o ESPERANDO_DECISIÓN, nunca antes), abrir el **batched
      gate** (§6) con todas las decisiones pendientes de la wave juntas.
   4. Esperar la respuesta del usuario sin límite de tiempo (§7). Rutear cada
      respuesta al sub-agente que la generó vía `SendMessage`, y esperar a
      que ese sub-agente termine.
   5. Revisión + integración: cada tarea COMPLETADA pasa su propia
      autorrevisión (`revision-codigo`, embebida en el prompt del
      sub-agente; ver §8) antes de reportarse como terminada. El
      orquestador mergea la rama de cada tarea completada a `main`. Un
      conflicto de merge o un hallazgo bloqueante de la revisión se agrega
      como una decisión más al batched gate de esa wave, no se resuelve
      solo.
   6. **Cierre de la wave**:
      - Registrar el cierre en `estado.yaml` y en `decisiones.md`.
      - Si alguna tarea de la wave declara `verificacion_manual`, listar
        esas verificaciones (literales, agrupadas por tarea) como checklist
        informativo en el reporte de cierre de wave y en `decisiones.md`.
        No se espera respuesta: la wave siguiente arranca igual.
      - Correr `optimizador-tokens` modo `empaquetar`, que genera o
        actualiza `milestones/<slug>/contexto-compacto.md` (§9). En la
        última wave no se corre aquí: lo hace el cierre del milestone
        (paso 5), una sola vez.
4. Repetir con la siguiente wave hasta que no queden tareas.
5. **Cierre del milestone**: correr `verificador-datos` en nivel `ligera`
   solo sobre los docs raíz (README y similares) que el milestone tocó y
   que **ninguna tarea verificó ya**; si todos se verificaron dentro de
   sus tareas, este paso no se corre (se anota en `decisiones.md`). Luego
   `optimizador-tokens` modo `empaquetar` una última vez, y el reporte
   final (tareas completadas, bloqueos externos pendientes, decisiones
   tomadas y el checklist acumulado de `verificacion_manual`, si hay).

## 3. a) Descomposición en waves

- Construye el grafo dirigido tarea → `depende_de` usando **solo**
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
  siguiente no dependa de la decisión pendiente de la actual: mantiene un
  único punto mental de "dónde estamos" y evita estado parcial confuso entre
  waves. Dentro de una misma wave, en cambio, las tareas sí avanzan en
  paralelo entre sí sin esperarse (son independientes por construcción).
  Las `verificacion_manual` pendientes no cuentan para este cierre (§1).

## 4. d) Preflight

Antes de calcular la primera wave, validar el manifest completo:

- Todo `id` es único.
- Todo `depende_de` resuelve a otro `id` del manifest, o está explícitamente
  listado en `fuera_de_alcance_si_depende_de` de esa tarea (dependencia
  **externa**). Si no es ninguna de las dos cosas: error de preflight.
- El grafo de dependencias internas no tiene ciclos (orden topológico debe
  existir).
- Toda tarea tiene `id`, `titulo`, `tipo` y `descripcion` no vacíos.
- Campos opcionales, solo si están presentes: `modelo` es un texto no vacío;
  `verificacion_manual` es una lista de textos no vacíos.
- Tomar un hash/snapshot del manifest ya validado y guardarlo en
  `estado.yaml`. Antes de lanzar **cada** wave (no solo al principio),
  releer `milestone.yaml` y comparar: si cambió respecto al snapshot, parar
  y volver a correr preflight completo: nunca seguir con un manifest que
  mutó a mitad de camino sin que el usuario lo sepa.

Para las reglas mecánicas puedes apoyarte en el script de `triage-proyecto`,
que aplica estas mismas reglas y muestra el plan de waves:

```bash
python .claude/skills/triage-proyecto/scripts/preflight_manifest.py milestones/<slug>/milestone.yaml
```

Código de salida 0 = pasa, 1 = falla, 2 = no se pudo leer. Sus avisos (un
`tipo` fuera de la lista, `criterios_aceptacion` vacío) son informativos y
no hacen fallar el preflight. El snapshot y la relectura antes de cada wave
siguen siendo trabajo tuyo.

Las dependencias **externas** (fuera del alcance del milestone) se anotan en
`bloqueos-externos.md` con la tarea que las originó, y **no** entran al
cálculo de waves ni bloquean nada: se resuelven aparte. Si una tarea interna
depende de una externa, esa tarea queda marcada como BLOQUEADA_EXTERNA desde
el preflight: no entra a ninguna wave hasta que alguien actualice el manifest
confirmando que el bloqueo externo se resolvió (eso cuenta como una mutación
de manifest válida, se vuelve a correr el preflight y solo entonces la tarea
entra a su wave).

El preflight es una validación automática, no un gate de aprobación: si pasa,
el orquestador sigue solo; si falla, reporta el error exacto (qué tarea, qué
campo) y espera a que el usuario corrija el manifest.

## 5. b) y c) Aislamiento de ejecución + cap de concurrencia

- Cada tarea = una llamada al tool `Agent` con `isolation: "worktree"`.
  - `model` de esa llamada: el `modelo:` de la tarea; si no lo trae, el
    del perfil de costo (§1) según su `tipo`. Lo mismo con
    `verificacion`: el de la tarea o, si falta, el del perfil; va en
    `[SKILLS A APLICAR]` del prompt.
  - Usa `run_in_background: false` para las tareas de una wave: el
    orquestador no puede avanzar (ni cerrar la wave, ni abrir el gate) hasta
    que todo el lote responda, así que no hay nada útil que hacer mientras
    tanto salvo esperar.
- **Prompt del sub-agente.** Tiene que ser autocontenido (el sub-agente no
  ve esta conversación). Se arma siempre con
  [`optimizador-prompts/PLANTILLA-SUBAGENTE.md`](../optimizador-prompts/PLANTILLA-SUBAGENTE.md),
  que define los bloques y sus reglas. Lo mínimo que lleva:
  - `id`, `titulo`, `tipo`, `descripcion`, los `criterios_aceptacion`
    **literales** y las rutas de archivo relevantes del manifest.
  - Si la tarea declara `verificacion_manual`, la lista literal, marcada
    como informativa: el sub-agente no la verifica ni la bloquea.
  - **Paso 0 obligatorio: sincronizar con `main`.** Los worktrees que crea
    `isolation: "worktree"` pueden arrancar desde un commit viejo y no desde
    el HEAD de `main` (pasó en la wave 3 de `mejora-skills`). El prompt pide
    correr `git merge --ff-only main` antes de nada y comprobar que existen
    los archivos que integró la wave anterior (nombrados uno por uno). Si el
    merge falla o falta algún archivo, el sub-agente no sigue: devuelve
    `DECISION_NEEDED` con la salida del comando.
  - Las skills de apoyo que le tocan según §8, con el momento y la ruta de
    su SKILL.md.
  - Si el tipo de proyecto corre un servidor de pruebas (dev server, API
    local, etc.), indica en el prompt que elija y registre un puerto libre
    para evitar colisiones con otras tareas corriendo en paralelo.
- **Contexto grande.** Si el contexto de referencia que va en `[CONTEXTO]`
  (resultados de waves previas, decisiones, docs relacionados) supera
  **~4.000 tokens estimados**, pásalo antes por `optimizador-tokens` modo
  `capsula` y usa la cápsula tal cual. Por debajo del umbral no se comprime.
  Los criterios, la `verificacion_manual`, las respuestas del gate, los ids,
  las rutas y el código a editar nunca se comprimen (el código se pasa por
  ruta).
- **Cap de concurrencia** (`cap_concurrencia`, default 3): dentro de una
  wave, nunca hay más de `cap` llamadas a `Agent` en vuelo a la vez. Si la
  wave tiene más tareas listas que el cap, pártelas en lotes:
  - Lote 1 = primeras `cap` tareas → lanzar todas en el mismo mensaje
    (llamadas paralelas).
  - En cuanto **cualquier** tarea del lote retorna (COMPLETADA o
    ESPERANDO_DECISIÓN: ambas cuentan como "liberó su slot", no hace falta
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

El checklist de `verificacion_manual` (§2, paso 3.6) **no** pasa por este
gate: se informa, no se pregunta.

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

El `tipo` de cada tarea en el manifest, y lo que toca, deciden qué skills de
apoyo usa el orquestador y cuáles van en el prompt del sub-agente, y en qué
momento:

| Momento | Condición | Skill |
|---|---|---|
| Antes de todo | El usuario trae una idea, no un manifest | `triage-proyecto` |
| Antes de implementar | La tarea no trae `criterios_aceptacion` claros, o el enunciado es ambiguo | `especificacion` |
| Al armar el prompt del sub-agente | Siempre | `optimizador-prompts` (plantilla) |
| Al armar el prompt del sub-agente | Contexto de referencia > umbral (~4.000 tokens estimados) | `optimizador-tokens` (`capsula`) |
| Durante la implementación | `tipo: frontend` (o la tarea toca UI aunque sea de otro tipo) | `frontend-design` + `emil-design-eng` |
| Durante la implementación | La tarea crea o cambia animaciones (web) | `animate` |
| Durante la implementación | `tipo: mobile` con React Native / Expo y motion | `animate-expo` |
| Durante la implementación | Web pensada para uso en móvil | `mobile-native` |
| Durante la implementación | `tipo: presentacion` | `presentaciones-visuales` (+ `frontend-design`) |
| Antes de implementar | La tarea crea o cambia API, base de datos o login | `backend-datos` (modelo y contrato antes del código) |
| Durante la implementación | `tipo: backend`, o una tarea `mobile`/`frontend` que necesita datos persistentes | `backend-datos` |
| Durante la implementación | `tipo: devops`, o el milestone pide publicar | `despliegue` |
| Antes de ejecutar una publicación | Siempre | Batched gate (`DECISION_NEEDED` con comando exacto) |
| Durante la implementación | `tipo: academico` | `trabajo-academico` |
| Durante la implementación | La tarea introduce lógica con comportamiento verificable | `testing` |
| Antes de reportarse COMPLETADA | Siempre que hubo cambios de código | `revision-codigo` (autorrevisión) |
| Antes de reportarse COMPLETADA | El diff toca transiciones / animaciones | `review-animations` (lectura directa del archivo), dentro de la autorrevisión |
| Antes de reportarse COMPLETADA | `verificacion` de la tarea (o la del perfil de costo, §1) es `ligera` o `completa` | `verificador-datos`, en ese nivel |
| Antes de reportarse COMPLETADA | `tipo: academico` | `verificador-datos` sobre todas las referencias |
| Al cerrar la tarea/milestone | La tarea es la última de una funcionalidad visible, o el milestone completo cerró | `documentacion` |
| Al cerrar cada wave | Siempre, salvo la última (la cubre el cierre del milestone) | `optimizador-tokens` (`empaquetar`) |
| Al cerrar el milestone | Docs raíz tocados que ninguna tarea verificó | `verificador-datos` (`ligera`) |

Las filas de "Antes de todo", "Al armar el prompt" y "Al cerrar" las
ejecuta el orquestador; las de "Antes de implementar", "Durante la
implementación" y "Antes de reportarse COMPLETADA" van en
`[SKILLS A APLICAR]` del prompt del sub-agente.

Esta tabla es la misma para cualquier dominio (web, backend, CLI, datos,
mobile): lo que cambia entre proyectos es **qué produce** cada skill (por
ejemplo, `testing` genera property tests para un pipeline de datos y tests
de componente para una UI), no cuándo se invoca. El detalle de qué generar
según el dominio vive en el SKILL.md de cada skill de apoyo, no aquí.

### Skills vendorizadas de Emil Kowalski

Hay 10 en `.claude/skills/` (registro, origen y verificación en
[docs/vendor/emilkowalski-skills.md](../../../docs/vendor/emilkowalski-skills.md)).
Además de las que tienen fila en la tabla, `improve-animations`,
`find-animation-opportunities`, `animation-vocabulary`, `pick-ui-library` y
`prototype` no tienen momento fijo: se nombran en el prompt solo si la
`descripcion` de la tarea pide ese trabajo (auditar el motion, buscar dónde
animar, elegir una librería de UI, prototipar). Al delegarlas:

- **Invocación.** `review-animations`, `pick-ui-library` y `prototype` tienen
  `disable-model-invocation: true` y no se disparan solas: el prompt dice
  *"lee y aplica `.claude/skills/<skill>/SKILL.md`"* (lectura directa del
  archivo, no invocación).
- **"Initial Response".** Las skills de Emil abren con un bloque *"When this
  skill is first invoked without a specific question, respond only
  with: …"* pensado para una conversación. Dentro de un sub-agente ese
  saludo inicial se ignora: la tarea del prompt cuenta como pregunta
  específica y se aplica directamente el resto de la skill. Las skills de
  Emil no se editan; la regla la pone el prompt (ver la plantilla).
- **Convivencia con `frontend-design`.** `frontend-design` decide la
  identidad visual (paleta, tipografía, layout); `emil-design-eng`, `animate`
  y `animate-expo` deciden movimiento, micro-interacciones y detalles de
  componentes. Si chocan en algo concreto: primero el brief del usuario,
  después `frontend-design` en lo estético y Emil en los valores de
  animación.
- **Stagger** (decisión del gate, wave 1 de `mejora-skills`): solo dentro de
  un grupo de elementos relacionados (ítems de una lista, celdas de una
  grilla, tarjetas de un mismo bloque). **Nunca** como cascada decorativa de
  secciones enteras de la página; ahí manda `frontend-design` (como máximo
  un único momento orquestado).

## 9. Estado y trazabilidad

`milestones/<slug>/estado.yaml` se actualiza en cada paso relevante (no solo
al final): wave actual, estado de cada tarea
(`PENDIENTE`/`EN_CURSO`/`ESPERANDO_DECISIÓN`/`COMPLETADA`/`BLOQUEADA_EXTERNA`),
rama/worktree de cada tarea en curso, y snapshot del manifest validado. Si la
sesión se corta a mitad de una wave, una nueva invocación de `/orquestador`
sobre el mismo milestone debe leer este archivo y **reanudar**, no reiniciar
desde cero.

**Reanudar con tareas `EN_CURSO` sin rama registrada.** Pasa si la sesión
se cortó antes de que el sub-agente devolviera su resultado (le pasó a la
wave 1 de `mejora-skills-2`). Antes de relanzar nada:

1. `git worktree list` y, para cada worktree cuya rama parte del commit
   del milestone, `git -C <worktree> status --short` y
   `git log main..<rama> --oneline`.
2. Identifica a qué tarea corresponde cada uno por los archivos que tocó
   (las rutas de su `descripcion`).
3. Si hay trabajo sin commit, commitéalo en su rama con
   `<id> (WIP): ...` y anota rama y worktree en `estado.yaml`.
4. Relanza la tarea **sobre ese trabajo**: el nuevo sub-agente arranca en
   otro worktree, así que su `[PASO 0]` agrega, después de sincronizar con
   `main`, `git merge <rama WIP>`; el prompt dice qué existe ya y qué
   criterios faltan, en vez de empezar de cero.
5. Nunca borres un worktree con trabajo sin integrar.

Como el sub-agente hace commits de avance (plantilla, `[ENTREGA]`), un
corte deja casi todo el trabajo en su rama y este paso es corto.

Al cierre de cada wave y del milestone, `optimizador-tokens` modo
`empaquetar` deja `milestones/<slug>/contexto-compacto.md`: el resumen de
estado, decisiones y resultados de tareas, con las entidades críticas
(ids, rutas, ramas, hashes, respuestas del gate) literales. Una sesión que
reanuda lee **primero** `contexto-compacto.md` y solo después consulta
`estado.yaml` y `decisiones.md` en lo que necesite. `estado.yaml` sigue
siendo la fuente de verdad: si los dos no coinciden, manda `estado.yaml`.
