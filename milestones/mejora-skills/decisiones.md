# Decisiones — Ampliación de skills del harness

Bitácora del batched gate: cada entrada es una decisión que un sub-agente
escaló durante una wave (o una decisión abierta de PLAN-MEJORA-SKILLS.md §7
que apareció en esa wave), con la tarea que la originó, lo que se preguntó y
lo que se respondió.

## Wave 1 (M1, M2, M3, M4)

Lote 1: M1, M2, M3 en paralelo; M4 entró al liberarse el slot de M2. M1, M2 y
M3 completaron sin `DECISION_NEEDED`; M4 escaló las decisiones abiertas §7.1 y
§7.2 del plan con el costo de contexto medido. El orquestador sumó dos
decisiones más que surgieron al comparar los reportes de la wave. Las cuatro
se presentaron juntas en un solo gate (con una pregunta de seguimiento porque
una respuesta llegó incompleta).

- **M4 — §7.1 `write-swift`**: ¿vendorizarla o dejarla fuera? (~123 tokens
  fijos por sesión, ninguna skill la cita) → **Respuesta: dejarla fuera.**
- **M4 — §7.2 skills de uso raro** (`ask-sonner`, `apple-design`,
  `animation-vocabulary`; ~328 tokens juntas): → **Respuesta: "solo
  algunas"**, sin indicar cuáles. El orquestador no eligió: preguntó de nuevo.
  → **Seguimiento: vendorizar solo `animation-vocabulary`.** Quedan 10 skills
  de Emil (9 base + `animation-vocabulary`).
- **M1/M2/M3 — registro del español (regla §3.3)**: M2 y M1 escribieron con
  voseo (como `especificacion`, `revision-codigo`, `testing`,
  `documentacion`); M3 con "tú"; el orquestador mezcla ambos, así que la regla
  "unificar con el resto del harness" no alcanzaba para decidir. →
  **Respuesta: español neutro con "tú".** Ruteo: M1 y M2 reescriben su propia
  skill ahora (sus carpetas); M3 ya cumple; `orquestador` se ajusta en M7 y las
  4 skills previas en M8.
- **M4 — contradicción stagger** (`frontend-design` lo llama patrón genérico;
  `animate`/`emil-design-eng` lo exigen): → **Respuesta: Emil, acotado** —
  stagger solo dentro de un grupo de elementos relacionados (lista, grilla),
  nunca cascada decorativa de secciones enteras. Se escribe en
  `docs/vendor/emilkowalski-skills.md` y en la tabla de convivencia de M7.

Hallazgos de la wave que pasan a M8 (sin decisión, son correcciones con
fuente clara): `RESUMEN-HARNESS.md` §3 dice "dos de las cinco tareas" sin
decisiones y fueron tres (T1, T2, T5); el conteo "6 skills" queda
desactualizado; `panel-tareas-demo/decisiones.md` cita un §8 de `PROCESO.md`
que no existe. M4 propone además un `.gitattributes` para los finales de
línea de las skills vendorizadas (fuera de alcance, se anota).

## Wave 2 (M5, M6)

M5 completó sin `DECISION_NEEDED`, pero su reporte destapó un vacío real
entre skills. M6 escaló §7.3 y §7.4 con los datos medidos por script en la
prueba de retención. Las tres se presentaron juntas en un solo gate.

- **M6 — §7.3 campo `modelo:`**: ¿adoptarlo ya en el manifest o dejarlo como
  recomendación? → **Respuesta: adoptarlo ya.** M7 lo agrega como campo
  opcional en orquestador §1 y lo pasa como `model` al tool `Agent`; el
  preflight de triage lo acepta.
- **M6 — §7.4 umbral de compresión**: con datos de T2 (contexto 2.210 → 1.024
  tokens, −54 %; prompt 2.735 → 1.549, −43 %; retención 13/13 en ambas
  variantes; ahorro total del sub-agente ~5 %, 48.127 → 45.594) →
  **Respuesta: subir a ~4.000 tokens estimados.**
- **M5 — criterios no verificables por un sub-agente** (p. ej. "abre en Expo
  Go", "escanea con cámara real"; ni orquestador ni especificacion decían
  qué hacer) → **Respuesta: campo propio** `verificacion_manual:` opcional
  por tarea. La tarea cierra con sus criterios automáticos. **Precisión
  posterior del usuario**: las verificaciones manuales se listan al cierre de
  **cada wave** (no solo del milestone), como checklist informativo que **no
  bloquea** la wave siguiente. M6 lo trata como literal (lista
  "nunca se toca"), M5 lo genera y M7 lo integra en el orquestador.

Wave 2 cerrada: M5 y M6 integradas a `main`. Ninguna tarea de este milestone
declara `verificacion_manual`, así que no hay checklist manual de la wave.

## Wave 3 (M7)

- **M7**: sin decisiones. Integró en `orquestador/SKILL.md` las skills
  nuevas y todas las decisiones de los gates 1 y 2 (tipos `presentacion` y
  `contenido`, campos `modelo` y `verificacion_manual`, umbral ~4.000,
  paso 0 de sincronización con `main`, convivencia con Emil, registro "tú").
  Hallazgos que pasan a M8: `triage-proyecto` (SKILL.md y
  `preflight_manifest.py`) todavía dice que `presentacion`/`contenido`,
  `modelo` y `verificacion_manual` "requieren M7"; quedó desactualizado.
  Sin `verificacion_manual` en la wave. Desde este cierre se aplica
  `optimizador-tokens` en modo `empaquetar` (`contexto-compacto.md`).
