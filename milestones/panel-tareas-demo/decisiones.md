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
