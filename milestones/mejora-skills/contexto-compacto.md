# Contexto compacto — mejora-skills
Actualizado: 2026-10-01 · cierre de wave 4 · fuentes: estado.yaml, decisiones.md, bloqueos-externos.md

## Estado
wave_actual: 5 | siguiente: 5 [M9] | cap: 3
manifest_snapshot_sha256: 0836eaf7dc2e0f249fcf4f4522ee38704570d88a4e5758bc219bfabfff17f06a
M1: COMPLETADA · commits 565567f, 448b188 · merge 0ba8ac3 · .claude/skills/presentaciones-visuales/, presentaciones/harness-clase.html
M2: COMPLETADA · commits 92531ee, f439ec0 · merge ec2c5e2 · .claude/skills/optimizador-prompts/ (+ PLANTILLA-SUBAGENTE.md)
M3: COMPLETADA · commit ae8f172 · merge 316c2b1 · .claude/skills/verificador-datos/
M4: COMPLETADA · commit 7be6d8e · merge 1c2c0d6 · 10 skills de Emil, upstream d16ebe6, docs/vendor/emilkowalski-skills.md
M5: COMPLETADA · commits 671cf30, 24c2c1b · merge 8b588ea · .claude/skills/triage-proyecto/
M6: COMPLETADA · commit 5031af3 · merge 3f7d539 · .claude/skills/optimizador-tokens/
M7: COMPLETADA · commit 16be2e3 · merge 515eecd · .claude/skills/orquestador/SKILL.md
M8: COMPLETADA · commit 05c5e5b · merge 3052107 · CLAUDE.md, README.md, RESUMEN-HARNESS.md, PROCESO.md §14
M9: EN_CURSO · milestones/e2e-skills/

## Decisiones vigentes (literales del gate)
- M4 §7.1 write-swift → **dejarla fuera.**
- M4 §7.2 skills de uso raro → **"solo algunas"**; seguimiento → **vendorizar solo `animation-vocabulary`.** (fuera: ask-sonner, apple-design)
- M1/M2/M3 registro del español (regla §3.3 de PLAN-MEJORA-SKILLS.md) → **español neutro con "tú".**
- M4 stagger (frontend-design vs animate/emil-design-eng) → **Emil, acotado**: stagger solo dentro de un grupo de elementos relacionados (lista, grilla), nunca cascada decorativa de secciones enteras.
- M6 §7.3 campo `modelo:` → **adoptarlo ya** (se pasa como `model` al tool Agent).
- M6 §7.4 umbral de compresión → **subir a ~4.000 tokens estimados.** Datos T2: contexto 2.210 → 1.024, prompt 2.735 → 1.549, retención 13/13, sub-agente 48.127 → 45.594 (~5 %).
- M5 criterios no verificables por un sub-agente → **campo propio** `verificacion_manual:`; precisión del usuario: se listan al cierre de **cada wave**, checklist informativo que **no bloquea**.

## Pendiente
- Protocolo: sub-agentes devuelven DECISION_NEEDED; cada worktree hace paso 0 `git merge --ff-only main`; al cierre de wave, `empaquetar` regenera contexto-compacto.md.
- M8 resolvió los pendientes de docs, triage-proyecto y registro (0 ❌ en verificador-datos).
- Propuesto, fuera de alcance: `.gitattributes` para finales de línea de skills vendorizadas.
- Bloqueos externos: ninguno.

## Rutas clave
- milestones/mejora-skills/pruebas/: optimizador-prompts.md, triage.md, tokens.md, orquestador.md
- milestones/mejora-skills/verificaciones/M3-resumen-harness.md
- docs/vendor/emilkowalski-skills.md: hash, convivencia, costo de contexto


<!-- metricas: tokens_original=1622 tokens_final=700 ahorro=57% metodo=estimado entidades_revisadas=88 entidades_preservadas=true ignoradas(pendientes resueltos por M8)=panel-tareas-demo/decisiones.md preflight_manifest.py T1 T5 especificacion revision-codigo testing documentacion contenido -->
