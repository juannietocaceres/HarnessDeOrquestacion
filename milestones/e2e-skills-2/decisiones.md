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

## Wave 2 — batched gate (2026-10-05)

| # | Tarea | Pregunta | Respuesta |
|---|---|---|---|
| 1 | T2 | El contrato de T1 no lista `auth.getSession()`; T2 detectaba la sesión con un sondeo `rpc('cupos_disponibles')` + error 42501. ¿Qué hacer? | Add getSession to the contract (Recommended): T2 agrega `auth.getSession()` y `onAuthStateChange` al contrato y reemplaza el sondeo. |

### Cierre de wave 2

T2 (ffbdb6c, con la decisión aplicada en ee7b075) y T4 (7a626a1) integradas
a `main`. Tests de T2 en `main`: 5 pass, 0 fail. T4: verificador completa,
0 incorrectas, 0 inventadas; pandoc no instalado (comando documentado).

Checklist de verificación manual (informativo, no bloquea):
- **T2**: "Abrir la web publicada (si se aprobó publicar) desde el celular y probar la inscripción"
- **T4**: "Revisar que el informe tenga sentido para el curso"
