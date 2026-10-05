# Verificación de datos (nivel completa): informe.md

Fecha: 2026-10-05. Fuentes consultadas hoy con WebFetch. Las referencias son documentación web sin DOI; se comprobó la URL y el contenido citado.

## Referencias

| Clave | URL | Resultado |
|---|---|---|
| supabase-rls | https://supabase.com/docs/guides/database/postgres/row-level-security | Correcta: título "Row Level Security"; "Enable RLS on every table in an exposed schema"; roles anon/authenticated; auth.uid() |
| supabase-auth | https://supabase.com/docs/guides/auth/passwords | Correcta: título "Password-based Auth"; signUp() y signInWithPassword() con correo y contraseña |
| postgres-rls | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | Correcta: sin políticas todas las filas disponibles; con RLS habilitado y sin políticas, default-deny |
| owasp-a01 | https://top10.owasp.org/2021/A01_2021-Broken_Access_Control | Correcta: título "A01 Broken Access Control - OWASP Top 10:2021"; "Except for public resources, deny by default"; subió desde la 5.ª posición (A01 = primera categoría). La URL antigua owasp.org/Top10/... redirige (308) a esta |
| github-pages | https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site | Correcta: título exacto; sección "Publishing with a custom GitHub Actions workflow"; ejecución manual desde la pestaña Actions |

## Afirmaciones técnicas del proyecto (contra la migración y docs/)

| Afirmación | Resultado |
|---|---|
| Cuatro políticas (talleres select; inscripciones select, insert, delete) | Correcta (migración, líneas 84-99) |
| Sin política de update; revoke insert/update a authenticated; grant insert (taller_id, nombre) | Correcta (líneas 108-112) |
| Trigger SECURITY DEFINER con `for update`; función cupos_disponibles | Correcta (líneas 34-76) |
| 14 casos R1-R14; 8 operaciones del contrato | Correcta (pruebas-rls.md; tabla del contrato) |
| Control de acceso defectuoso en primer lugar (A01) del Top 10 de 2021 | Correcta |
| Coincide con la recomendación de OWASP de denegar por defecto | Correcta |
| Inscripción manual expone riesgos (cupo, datos ajenos) | Planteamiento lógico, no dato; la evidencia está marcada [CITA PENDIENTE] |

## Conteo

Correctas: 5 referencias y 6 afirmaciones. A matizar: 0. No verificables: 0 (lo pendiente está marcado en el texto como [CITA PENDIENTE] o [POR COMPLETAR]). Exageradas: 0. **Incorrectas: 0. Inventadas: 0.**
