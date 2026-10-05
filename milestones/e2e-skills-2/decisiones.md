# Decisiones — Inscripción a taller universitario (e2e-skills-2)

Bitácora del batched gate de la validación N6 de `mejora-skills-2`.

## Triage (2026-10-05)

| Pregunta | Respuesta |
|---|---|
| ¿Con qué se construye la web? | Estático + Supabase JS (GitHub Pages) |
| ¿Quién ve la lista de inscritos? | Solo estudiantes: cada uno ve y cancela su inscripción; la lista completa se consulta en el panel de Supabase |
| ¿Hay lineamientos del docente o del programa para el informe APA? | No: informe corto genérico |

## Wave 1 — cierre (2026-10-05)

T1 integrada a `main` (838fd5c), gate sin decisiones. Supuestos de T1:
talleres legibles solo por autenticados; cupo validado con trigger
`SECURITY DEFINER` (`set search_path = ''`) y `cupos_disponibles` para la UI;
inscripción no editable (se cancela y se crea otra); variables
`SUPABASE_URL` y `SUPABASE_ANON_KEY`.

Checklist de verificación manual (informativo, no bloquea):
- **T1**: "Crear el proyecto en Supabase, aplicar la migración y copiar la URL y la anon key"
