# Pruebas de políticas RLS (skill `testing`)

Se ejecutan contra una base local (`supabase start`), con dos usuarios de prueba A y B creados por Supabase Auth, usando el cliente con clave anon y la sesión de cada uno (no mocks). Cada fila es un caso: lo que debe permitir (OK) o negar (NO).

| # | Actor | Operación | Esperado |
|---|---|---|---|
| R1 | A | insert inscripción propia (`taller_id`, `nombre`) | OK; `user_id` = A |
| R2 | A | select inscripciones | OK; solo las de A |
| R3 | B | select inscripciones tras R1 | OK; `[]`, no ve la de A |
| R4 | B | delete inscripción de A (por id) | 0 filas borradas; la de A sigue |
| R5 | A | delete inscripción propia | OK; fila borrada |
| R6 | A | update inscripción propia (cambiar `nombre`) | NO (`42501`): sin política ni permiso de columna |
| R7 | A | insert enviando `user_id` de B | NO (`42501`) |
| R8 | A | insert enviando `id` o `creado_en` | NO (`42501`) |
| R9 | A | insert duplicado en el mismo taller | NO (`23505`) |
| R10 | B | insert en taller con cupo 1 ya ocupado por A | NO (`P0001` `taller_lleno`) |
| R11 | A | select talleres | OK; ve el taller del seed |
| R12 | A | insert, update o delete en `talleres` | NO (`42501`) |
| R13 | anon (sin sesión) | select talleres / inscripciones | `[]` o `42501`; nunca datos |
| R14 | anon (sin sesión) | insert inscripción; rpc `cupos_disponibles` | NO (`42501`) |

Casos extra: tras cancelar (R5), otro usuario puede inscribirse en un taller antes lleno (el cupo se libera); borrar un taller en el panel elimina sus inscripciones (cascade).
