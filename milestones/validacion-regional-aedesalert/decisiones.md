# Decisiones — validacion-regional-aedesalert

## Triage (antes de la wave 1)

Preguntas de triage-proyecto, respondidas por Diego con AskUserQuestion (2-oct-2026):

| Pregunta | Respuesta |
|---|---|
| ¿Qué alcance tiene "rehacer" el trabajo? | Rehacer todo: misma idea, re-verificar todas las cifras, nueva matriz y nuevo deck |
| ¿En qué formato va la presentación de 5 minutos? | HTML del harness (presentaciones-visuales) |
| ¿Cómo se ejecutan las waves? | Sub-agentes reales |

Pedido adicional durante el triage: "el guion de la presentación me lo dejas aparte" → tarea T8 (documento independiente).

## Wave 1 (T1–T4) — cerrada el 2-oct-2026

Batched gate: 1 decisión.

| Tarea | Pregunta | Respuesta |
|---|---|---|
| T2 | Desde mayo de 2026 la Secretaría de Salud de Cali usa DengueIA (Icesi + Univalle + Fundación Rockefeller): predice el dengue hasta 3 semanas antes, 93 % de efectividad reportada, mapa semáforo. La frase de la v1 "la vigilancia en Cali es reactiva" queda falsa. ¿Cómo se presenta AedesAlert frente a DengueIA? | **Complemento abierto**: misma idea, presentada como versión abierta y replicable (datos abiertos, código libre) para los otros municipios del Valle en riesgo muy alto; DengueIA se cita como prueba de que el enfoque funciona. Criterio 2: 4/5. |

Respuesta ruteada a T2 con SendMessage; T2 actualizó sus dos archivos y cerró COMPLETADA.

Avisos sin gate (no bloqueantes): T3 detectó DengueIA por su cuenta y lo usa a favor (alineación); T4 no lo menciona → T5 debe integrarlo. T1 deja de usar "9 iniciativas clúster" (la CCC hoy habla de siete).

Verificación manual: ninguna en esta wave.

Integración: el shell del PC no puede borrar archivos (index.lock, objetos temporales), así que git no puede commitear desde la sesión. Los archivos quedan escritos en el repo y los commits por tarea se dejan como comandos para que Diego los corra al final (mismo efecto de trazabilidad: un commit por tarea).

## Wave 2 (T5) — cerrada el 2-oct-2026

Batched gate: sin decisiones. T5 consolidó la matriz (5 · 4 · 5 · 4 = 18/20) y la escaleta (8 diapositivas, 4:50). Verificación T5: 42 afirmaciones, 0 incorrectas; recomendación "publicar con cambios menores" (ya aplicados).
Pendiente informativo: la URL del CONPES 4144 en el DNP no abrió en la wave 1 (se respaldó con MinTIC y otras fuentes).

## Wave 3 (T6, T7, T8) — cerrada el 2-oct-2026

Las 3 tareas se cortaron una vez por el límite de uso de la API; T6 se retomó con SendMessage y T7/T8 se relanzaron desde cero. Batched gate: sin decisiones.
Ajustes del orquestador al cierre (sin cambiar cifras ni puntajes): "la cofinanciación llega en el próximo ciclo" → "dependerá de un próximo ciclo" (matriz §3 y §7, deck diapositivas 6 y 7), por coherencia con §4.4 ("podría aplicar"; el ciclo no está anunciado), según avisos de T6 y T8.

Checklist de verificación manual (no bloquea):
- T7: Abrir el HTML en el PC del salón o en el proyector y pasar las diapositivas con las flechas.
- T7: Exportar a PDF con Ctrl+P como respaldo por si el PC del salón no abre el HTML.
- T8: Ensayar el guion en voz alta con cronómetro.
- Cierre: abrir a mano la URL del CONPES 4144 en el DNP (403/timeout desde la sesión); si no abre, citar solo MinTIC (2025).

## Ajuste posterior al cierre (2-oct-2026)

Pedido de Diego: "no importa si se sube la presentación a 8 minutos, pero me gustaría argumentar más cosas en el guion". El guion (T8) pasó de 594 a 987 palabras: ~7:36 leído, ~8:03 diciendo las cifras en voz alta; escaleta del guion 0:00–7:40. Mismas 8 diapositivas: el deck no cambia. Todas las cifras siguen en matriz-consolidada.md (comprobado con script). La escaleta de 4:50 de matriz-consolidada.md §7 queda como versión corta.
Segundo ajuste (mismo día): Diego pidió 10 minutos. Guion: 1.248 palabras, ~9:36 leído, ~10:04 con cifras en voz alta; escaleta del guion 0:00–10:00. Cifras verificadas contra matriz-consolidada.md con script (ninguna nueva).
