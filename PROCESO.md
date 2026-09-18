# PROCESO.md — Bitácora de construcción del harness

Registro cronológico de las decisiones de diseño tomadas al construir este
harness, y el porqué de cada una. Es material de apoyo para explicar en
clase el proceso de desarrollo asistido por IA — no describe *qué* hace el
harness (eso está en [RESUMEN-HARNESS.md](RESUMEN-HARNESS.md)), sino *por
qué* quedó diseñado así.

## 1. Punto de partida

`C:\Users\juand\Electiva\Harness` — carpeta vacía, sin repositorio git, sin
memoria previa de este proyecto. Objetivo: un sistema de orquestación
reutilizable para cualquier tipo de proyecto, modelo milestone → waves, con
aislamiento por tarea, cap de concurrencia, preflight y un gate de
aprobación por lotes.

## 2. Dos preguntas antes de escribir nada

Antes de crear cualquier archivo se plantearon dos preguntas al usuario,
porque ambas cambiaban sustancialmente el alcance y el costo del trabajo, y
no tenían una respuesta derivable del pedido original:

1. **¿El milestone de ejemplo (sección 4 del pedido) debía ejecutarse de
   verdad o simularse narrativamente?** → El usuario eligió **ejecución
   real con sub-agentes**: el orquestador invoca de verdad el tool `Agent`
   con aislamiento de git worktree para las tareas ficticias, en vez de
   narrar el proceso con tablas. Esto es una decisión de costo/tiempo real
   (varios sub-agentes reales corriendo, no una descripción), por eso se
   preguntó en vez de asumir la opción más barata.
2. **¿Sobre qué dominio debía tratar el milestone de ejemplo?** → Se eligió
   **web app** (un panel de administración de tareas), por ser el dominio
   más fácil de seguir para una audiencia de clase.

## 3. Infraestructura base

Se corrió `git init -b main`. **Por qué**: el punto (b) del pedido exige
aislamiento por *git worktree* por tarea — el tool `Agent` con
`isolation: "worktree"` requiere que el directorio ya sea un repositorio
git con al menos un commit para poder ramificar. Es una operación local, no
destructiva (la carpeta estaba vacía) y reversible, así que no ameritaba
una pregunta aparte.

## 4. Diseño de la skill `orquestador`

Decisiones no triviales tomadas al escribir
[.claude/skills/orquestador/SKILL.md](.claude/skills/orquestador/SKILL.md):

**Formato del manifest (YAML).** Se eligió YAML sobre una tabla Markdown
porque las listas de dependencias (`depende_de: [T1, T2]`) se expresan de
forma nativa y son fáciles de validar programáticamente en el preflight, sin
perder legibilidad humana.

**Dependencias externas como categoría explícita, no como error.** El punto
(a) del pedido dice que un bloqueo fuera del alcance del milestone "se
resuelve aparte y no detiene el resto". Se tradujo esto en una regla
concreta: toda dependencia que no resuelve a un `id` del propio manifest
debe estar *declarada* como externa (`fuera_de_alcance_si_depende_de`); si
no está declarada, es un error de preflight (dependencia ambigua), no una
externa implícita. Esto evita que una dependencia externa real termine
siendo, en la práctica, un typo en un `id` que nadie nota.

**Cierre de wave con merge a `main`, no con worktrees sueltos.** Este es el
hallazgo de diseño más importante del harness. Cada tarea corre en su propio
worktree/rama, aislada de las demás — pero si la wave 2 depende de archivos
que creó la wave 1, y cada worktree se crea desde el estado de `main` en el
momento del spawn, entonces **la wave 2 no va a ver el trabajo de la wave 1**
a menos que ese trabajo ya esté mergeado a `main` antes de lanzar la wave
siguiente. Por eso el algoritmo (SKILL.md, §2 y §6) mergea cada tarea
completada a `main` como parte del cierre de la wave, antes de calcular o
lanzar la wave siguiente. Sin este paso, el modelo de waves con aislamiento
por worktree simplemente no funciona para tareas con dependencias reales.

**Qué cuenta como "liberar un slot" del cap de concurrencia.** El pedido
dice que el cap limita cuántas tareas corren *simultáneamente*. Quedó
definido que un sub-agente libera su slot cuando su llamada retorna un
resultado — sea porque terminó (`COMPLETADA`) o porque se detuvo a pedir una
decisión (`ESPERANDO_DECISIÓN`). Esto importa porque, si "liberar el slot"
dependiera de que la decisión ya esté *resuelta*, una sola tarea pausada
podría trabar el avance de toda una wave con más tareas en cola que el cap
— exactamente el tipo de bloqueo en cascada que el batched gate busca
evitar. Separar "el sub-agente terminó su turno" de "la decisión que generó
ya se respondió" permite que el resto de la wave siga avanzando mientras el
batched gate espera.

**Mecánica del batched gate: `DECISION_NEEDED` + `AskUserQuestion` +
`SendMessage`.** Un sub-agente no tiene forma de preguntarle algo al usuario
directamente sin interrumpir el flujo tarea por tarea que el pedido
explícitamente quiere evitar. Se definió un protocolo simple: el sub-agente
termina su turno con un bloque `DECISION_NEEDED` estructurado en vez de
adivinar; el orquestador acumula todos los de la wave; cuando la wave entera
llegó a un estado terminal, arma **una sola** llamada a `AskUserQuestion`
con una pregunta por decisión pendiente, rotulada con la tarea de origen;
cada respuesta se rutea de vuelta a su sub-agente con `SendMessage` (que
retoma al agente con su contexto completo, incluyendo su propio worktree).
Esto satisface literalmente el pedido: "cada decisión debe quedar enrutada a
la tarea específica que la generó, y cada tarea retoma su propio punto de
espera de forma independiente".

**Preflight con snapshot del manifest, no solo validación inicial.** "Cero
sorpresas a mitad de camino" se interpretó como algo más fuerte que validar
una sola vez al principio: el orquestador guarda un snapshot del manifest ya
validado y lo vuelve a comparar antes de *cada* wave (no solo antes de la
primera), para detectar si alguien editó `milestone.yaml` en medio de la
corrida.

**Estado persistido en `estado.yaml` para poder reanudar.** No estaba
pedido explícitamente, pero se dedujo de "sin mutaciones erróneas... cero
sorpresas": si la sesión de Claude Code se corta a mitad de una wave (cierre
de la app, corte de red), sin un estado persistido el usuario perdería el
progreso de tareas ya completadas y tendría que reiniciar el milestone
completo. Es una extensión mínima y coherente con el resto del diseño, no
una feature nueva fuera de alcance.

## 5. Skills de apoyo

- **`especificacion`**: plantilla + proceso para pasar de idea informal a
  documento verificable. Incluye explícitamente "cuándo conviene saltarla"
  (si la tarea ya trae criterios de aceptación claros) para que el
  orquestador no la dispare como ceremonia en cada tarea trivial.
- **`frontend-design`**: copiada sin modificar desde
  `anthropics/claude-code` (`plugins/frontend-design/skills/frontend-design/SKILL.md`).
  Se verificó con `diff` contra una descarga fresca del archivo original que
  la copia es byte a byte idéntica antes de darla por buena — no se confió
  en una lectura resumida (el primer intento de traerla vía la herramienta
  de fetch la resumió en vez de traerla literal, así que se volvió a
  descargar con `curl` para obtener el contenido crudo).
- **`revision-codigo`**: checklist dividido en corrección / seguridad básica
  / legibilidad / convenciones / alcance, con una regla explícita de cuándo
  un hallazgo se corrige solo vs. cuándo se escala como `DECISION_NEEDED` —
  para que se enganche directo con el batched gate del orquestador en vez de
  ser un checklist aislado.
- **`documentacion`**: distingue README / docs técnicas (decisiones) /
  comentarios inline como tres cosas distintas con audiencias distintas, y
  mantiene la misma regla de "no comentar por defecto, salvo que el PORQUÉ
  no sea obvio" usada en el resto de este proceso, para que el harness no se
  contradiga a sí mismo entre skills.
- **`testing`**: la estrategia (qué testear, con qué profundidad) varía por
  tipo de proyecto (web/backend/CLI/datos/mobile) vía una tabla; el
  *origen* de los casos (criterios de aceptación → casos borde → caminos de
  error) es el mismo para cualquier dominio.

## 6. Próximos pasos de esta bitácora

Las secciones siguientes se agregan a medida que se ejecuta el milestone de
ejemplo real (preflight, waves, batched gates) y se genera el entregable de
muestra con `especificacion`.
