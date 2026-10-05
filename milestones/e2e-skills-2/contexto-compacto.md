# Contexto compacto — e2e-skills-2
Actualizado: 2026-10-05 · cierre de wave 1 · fuentes: estado.yaml, decisiones.md, bloqueos-externos.md

## Estado
origen: N6 de `mejora-skills-2` (`PLAN-MEJORA-SKILLS-2.md` §4 N6) · manifest_snapshot_sha256: 567fb7675f85cd6c04a454726eaed329c541a8d50b06b04aff7060fea9af93e2 · integración en `main`
wave_actual: 2 | siguiente: 2 [T2, T4] → 3 [T3] | cap: 3
T1: COMPLETADA · commit 87c3e4f · merge 838fd5c · rama `worktree-agent-a99af8671d35d81fb` · `web/taller-inscripcion/docs/`, `web/taller-inscripcion/supabase/`, `web/taller-inscripcion/.env.example`

## Decisiones vigentes (triage)
- Stack → **Estático + Supabase JS (GitHub Pages)**
- Acceso → **Solo estudiantes: cada uno ve y cancela su inscripción; la lista completa se consulta en el panel de Supabase**
- Informe → **No: informe corto genérico**

## Pendiente
- Supuestos T1: talleres solo autenticados; trigger `SECURITY DEFINER` (`set search_path = ''`) para cupo; `cupos_disponibles`; variables `SUPABASE_URL`, `SUPABASE_ANON_KEY`.
- Verificación manual T1: "Crear el proyecto en Supabase, aplicar la migración y copiar la URL y la anon key"
- Bloqueos externos: ninguno.

## Rutas clave
- `milestones/e2e-skills-2/milestone.yaml`, `milestones/e2e-skills-2/estado.yaml` (fuente de verdad), `milestones/e2e-skills-2/decisiones.md`

<!-- metricas: tokens_original 464, tokens_final 331, ahorro 29%, metodo estimado; entidades_preservadas true -->
