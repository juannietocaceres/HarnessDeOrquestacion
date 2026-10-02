# Decisiones — Landing y deck de Enigma Go (validación E2E)

Bitácora del batched gate de la corrida de punta a punta (M9 de
`mejora-skills`). Entrada: idea en lenguaje natural → `triage-proyecto`
(sin preguntas: plataforma, objetivo y alcance venían en la idea; supuestos
en `triage.json`) → este manifest.

## Wave 1 (T1)

- **T1**: sin decisiones. `verificador-datos` sobre `contenido.md`: ✅ 28,
  ❌ 0, 💬 2. Hallazgo: el `milestones/enigma-go/estado.yaml` commiteado aún
  dice T1 `EN_CURSO`; la versión "COMPLETADA/pausado" es un cambio local sin
  commitear del usuario (no se toca: fuera de este milestone). T1 basó sus
  afirmaciones en git. Sin `verificacion_manual` en la wave.

## Wave 2 (T2, T3)

- **T2** y **T3**: sin decisiones; el batched gate de la wave no tuvo
  preguntas. T2 pasó `review-animations` (veredicto Approve) y aplicó la
  regla de stagger del gate de `mejora-skills` (solo dentro de grupos de la
  portada; las secciones no se animan). T3 pasó `verificador-datos` (✅ 27,
  ❌ 0, 💬 2).

### Checklist de verificación manual (informativo, no bloquea)

- [ ] **T2** — "Proyectar la landing en el aula y confirmar que la animación de entrada se ve fluida y el texto se lee desde el fondo."
- [ ] **T3** — "Ensayar el deck en el proyector del aula: 5 slides legibles y notas del presentador con la tecla N."

## Milestone cerrado

3 tareas, 2 waves, 0 decisiones en el gate. Al cierre: `verificador-datos`
sobre los documentos tocados. El único documento de texto es
`presentaciones/enigma-go/contenido.md`, ya verificado en T1 (✅ 28, ❌ 0).
La landing y el deck se verificaron contra él (T2 a mano y T3 con informe).
