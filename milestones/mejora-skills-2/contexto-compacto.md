# Contexto compacto — mejora-skills-2
Actualizado: 2026-10-05 · cierre de wave 2 · fuentes: estado.yaml, decisiones.md, bloqueos-externos.md

## Estado
wave_actual: 3 | siguiente: 3 [N5] → 4 [N6] | cap: 3
manifest_snapshot_sha256: e36f21def60a7c9356ce635462909b009f62cc20e8cb74df60a65d08833c0d21 (re-preflight OK tras 5fe0fad)
N1: COMPLETADA · commit 800eb89 · merge 8d07a9c · `.claude/skills/backend-datos/` + `milestones/mejora-skills-2/pruebas/backend-datos.md`
N2: COMPLETADA · commit 94dae97 · merge 6fc17bc · `.claude/skills/despliegue/` + `.github/workflows/pages-enigma-go.yml` + `landing/enigma-go/404.html` + `milestones/mejora-skills-2/pruebas/despliegue.md`
N3: COMPLETADA · commit 4370787 · merge be4e628 · `.claude/skills/trabajo-academico/` + `milestones/mejora-skills-2/pruebas/trabajo-academico.md`
N4: COMPLETADA · commit 7b62886 · merge 5a496b0 · rama `worktree-agent-ae1ff4a878d8656c6` · tipos `devops`/`academico`, `norma_citacion` (`apa7`|`icontec`), filas §1/§8 en `.claude/skills/orquestador/SKILL.md`, `.claude/skills/triage-proyecto/` (preflight, schema, tests 29 OK; optimizador-tokens 21 OK; 5 manifests PASA)
Cierre wave 1: d8730a4 (`.gitignore` con `!.env.example`, estado, decisiones)
Verificador: N1 ligera 5 ✅ / 1 no verificable (`keys().hasOnly` / `request.time`, nota de emulador); N2 ligera sin hallazgos; N3 completa 17 ✅ / 3 🟡 / 0 ❌ / 0 inventadas.

## Decisiones vigentes (literales del gate, wave 1)
- N1 — `.gitignore` ignora `.env.example` → **Sí: el orquestador agrega la excepción al integrar la wave.**
- N3 (§7.4) — docx/pdf de anthropics/skills (licencia propietaria) → **No se vendorizan; `trabajo-academico` usa pandoc y solo las referencia.**
- §7.1–7.3 — Supabase por defecto, GitHub Pages para estáticas (Vercel con funciones de servidor), APA 7 por defecto cambiable → **Confirmadas las tres.**
- N2 (§7.5) — publicar landing de Enigma Go → **Solo preparada: nada se publica ni se hace push.**

## Pendiente
- Wave 2 cerrada sin decisiones ni `verificacion_manual`; supuestos N4: `devops` → `sonnet`/`ninguna` (`opus` si hay arquitectura), `academico` → `sonnet`/`completa`. Wave 3: N5 (docs raíz, PLAN-MEJORA-SKILLS-2.md §4 N5).
- Verificación manual (informativa): N2 activar Pages solo si se aprueba publicar (no aprobado); N3 revisar sentido del esqueleto `milestones/mejora-skills-2/pruebas/trabajo-academico/documento.md`.
- Bloqueos externos: ninguno.
- Ramas integradas (worktrees no borrados): N1 `worktree-agent-a57954e5a4943dfeb` (sobre WIP 9acb444, `.claude/worktrees/agent-ae78a04b9aaa48a43`); N2 `worktree-agent-a4ce2ba0d7e863d78` (sobre WIP 7a15bac, `.claude/worktrees/agent-a8a7ef11e4888d79e`); N3 `worktree-agent-ad2f2d5dd8f79a0f7` (sobre WIP 4612eb3, `.claude/worktrees/agent-afefa586e23a0d53c`). Todo ya en `main`.
- Manifest mutado en 5fe0fad: N3 `verificacion: completa`; N1 se reabrió una vez por faltar `verificador-datos` ligera. `.gitignore` tenía `.env.*` (resuelto).

## Rutas clave
- `PLAN-MEJORA-SKILLS-2.md`: plan fuente (§4 por tarea, §7 decisiones).
- `milestones/mejora-skills-2/estado.yaml`: fuente de verdad.
- `milestones/mejora-skills-2/decisiones.md`: bitácora del gate.


<!-- metricas: tokens_original 1154, tokens_final 790, ahorro 32%, metodo estimado; entidades_preservadas true -->
