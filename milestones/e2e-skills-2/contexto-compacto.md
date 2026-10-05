# Contexto compacto — e2e-skills-2
Actualizado: 2026-10-05 · cierre de wave 2 · fuentes: estado.yaml, decisiones.md, bloqueos-externos.md

## Estado
origen: N6 de `mejora-skills-2` (`PLAN-MEJORA-SKILLS-2.md` §4 N6) · manifest_snapshot_sha256: 567fb7675f85cd6c04a454726eaed329c541a8d50b06b04aff7060fea9af93e2 · integración en `main`
wave_actual: 3 | siguiente: 3 [T3] | cap: 3
T1: COMPLETADA · commit 87c3e4f · merge 838fd5c · rama `worktree-agent-a99af8671d35d81fb` · `web/taller-inscripcion/docs/`, `web/taller-inscripcion/supabase/`, `web/taller-inscripcion/.env.example`
T2: COMPLETADA · commit ee7b075 · merge ffbdb6c · rama `worktree-agent-a8a807b843a5c79f9` · web estática `web/taller-inscripcion/` (index.html, app.js, logic.js, config.example.js; 5 tests node OK)
T4: COMPLETADA · commit d072ebe · merge 7a626a1 · rama `worktree-agent-a99e35b8c6b5215ea` · `web/taller-inscripcion/informe/informe.md` (verificador completa: 0 incorrectas, 0 inventadas)

## Decisiones vigentes (triage)
- Stack → **Estático + Supabase JS (GitHub Pages)**
- Acceso → **Solo estudiantes: cada uno ve y cancela su inscripción; la lista completa se consulta en el panel de Supabase**
- Informe → **No: informe corto genérico**

## Decisiones vigentes (gate wave 2)
- T2 sesión (antes: sondeo `rpc('cupos_disponibles')` + 42501) → **Add getSession to the contract (Recommended)**: `auth.getSession()` + `onAuthStateChange` en el contrato

## Pendiente
- Supuestos T1: talleres solo autenticados; trigger `SECURITY DEFINER` (`set search_path = ''`) para cupo; `cupos_disponibles`; variables `SUPABASE_URL`, `SUPABASE_ANON_KEY`.
- Verificación manual T1: "Crear el proyecto en Supabase, aplicar la migración y copiar la URL y la anon key"
- Verificación manual T2: "Abrir la web publicada (si se aprobó publicar) desde el celular y probar la inscripción"; T4: "Revisar que el informe tenga sentido para el curso".
- Bloqueos externos: ninguno.

## Rutas clave
- `milestones/e2e-skills-2/milestone.yaml`, `milestones/e2e-skills-2/estado.yaml` (fuente de verdad), `milestones/e2e-skills-2/decisiones.md`


<!-- metricas: tokens_original 748, tokens_final 521, ahorro 30%, metodo estimado; entidades_preservadas true -->
