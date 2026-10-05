# Decisiones — Backend, despliegue y trabajo académico

Bitácora del batched gate: cada entrada es una decisión que un sub-agente
escaló durante una wave (o una decisión abierta de PLAN-MEJORA-SKILLS-2.md §7
que apareció en esa wave), con la tarea que la originó, lo que se preguntó y
lo que se respondió.

## Wave 1 — batched gate (2026-10-05)

Reanudación según orquestador §9: N1, N2 y N3 se relanzaron sobre sus ramas
WIP (9acb444, 7a15bac, 4612eb3). El manifest cambió en 5fe0fad (N3
`verificacion: completa`, descripciones de N4/N5); preflight re-corrido: PASA,
snapshot actualizado. N1 se reabrió una vez porque reportó COMPLETADA sin la
pasada formal de `verificador-datos` ligera (luego: 5 ✅, 1 no verificable).

| # | Tarea | Pregunta | Respuesta |
|---|---|---|---|
| 1 | N1 | `.gitignore` raíz (`.env.*`) ignora `.env.example`: ¿agregar `!.env.example`? | Sí: el orquestador agrega la excepción al integrar la wave. |
| 2 | N3 (§7.4) | docx/pdf de anthropics/skills tienen licencia propietaria (sin redistribución ni obras derivadas). ¿Qué hacer? | No se vendorizan; `trabajo-academico` usa pandoc y solo las referencia. |
| 3 | N1/N2/N3 (§7.1–7.3) | ¿Confirmar las propuestas: Supabase por defecto, GitHub Pages para estáticas (Vercel con funciones de servidor), APA 7 por defecto cambiable? | Confirmadas las tres. |
| 4 | N2 (§7.5) | ¿Publicar la landing de Enigma Go en GitHub Pages o solo dejarla preparada? | Solo preparada: nada se publica ni se hace push. |

### Cierre de wave 1

Integradas a `main`: N1 (8d07a9c), N2 (6fc17bc), N3 (be4e628), sin
conflictos. `.gitignore` raíz: agregado `!.env.example` (decisión 1).

Checklist de verificación manual (informativo, no bloquea la wave 2):

- **N2**: "Activar GitHub Pages en la configuración del repositorio si la publicación se aprueba" — por la decisión 4 la publicación **no** se aprobó: queda solo preparada.
- **N3**: "Revisar que el esqueleto del anteproyecto tenga sentido para el tema y el programa" — `milestones/mejora-skills-2/pruebas/trabajo-academico/documento.md`.

## Wave 2 — cierre (2026-10-05)

N4 integrada a `main` (5a496b0). Gate sin decisiones. En `main`: 5 manifests
pasan preflight; tests triage-proyecto y optimizador-tokens OK. Supuestos de
N4 (sin gate): `devops` → `sonnet`/`ninguna` (`opus` si hay arquitectura);
`academico` → `sonnet`/`completa`. Sin `verificacion_manual` en la wave.
