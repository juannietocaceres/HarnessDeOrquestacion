# Decisiones — Panel de administración de tareas (demo)

Bitácora del batched gate: cada entrada es una decisión real que un
sub-agente escaló durante la ejecución de una wave, con la tarea que la
originó, lo que se preguntó y lo que se respondió.

## Wave 1

- **T1**: sin decisiones. El sub-agente completó directo — el propio
  enunciado ya resolvía la única ambigüedad posible (si agregar campos no
  pedidos al esquema) de forma explícita, así que no había nada genuino que
  escalar. No todas las tareas generan una decisión; el batched gate de la
  wave 1 no tuvo preguntas que hacer.

## Wave 2

- **T2**: sin decisiones. La especificación generada con `especificacion`
  (§8 de PROCESO.md) dejó el contrato sin ambigüedad real — la wave 2
  tampoco tuvo preguntas que hacer. Muestra que invertir en una buena
  especificación *antes* de implementar reduce cuántas decisiones llegan al
  batched gate más adelante.

## Wave 3

Las 3 tareas de la wave (T3, T4, T5) llegaron a estado terminal antes de
abrir el gate — T5 completó directo, T3 y T4 escalaron una decisión real
cada una. Ambas se presentaron **juntas, en una sola interacción**:

- **T3** — ¿agregar filtro/orden por estado en la lista, o mantenerla
  simple? → **Respuesta: agregar filtro/orden por estado**, del lado del
  cliente, sin tocar el contrato de T2.
- **T4** — ¿validar el título también en el cliente, o confiar solo en la
  respuesta 400 del servidor? → **Respuesta: confiar solo en el servidor**
  (sin validación de cliente).

Cada respuesta se ruteó de vuelta a su propio sub-agente (`SendMessage` al
`agentId` que generó cada `DECISION_NEEDED`), y cada uno retomó su propio
punto de espera de forma independiente — ninguno vio la decisión del otro.
