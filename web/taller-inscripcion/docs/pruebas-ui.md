---
documento: pruebas-ui
tarea: "T2"
proyecto: "e2e-skills-2"
---

# Pruebas de la UI de inscripción

Dos niveles: **automáticas** (lógica pura de `logic.js`, `node --test tests/logic.test.js`) y **manuales** (flujo con backend real, en el celular). Los casos de acceso a datos están en `pruebas-rls.md`.

## Automáticas (`tests/logic.test.js`)

| # | Función | Caso | Esperado |
|---|---|---|---|
| A1 | `configValida` | `undefined`, claves vacías, marcador `TU-...` | `false` |
| A2 | `configValida` | URL https y clave no vacía | `true` |
| A3 | `validarNombre` | `"   "`, 101 caracteres | `ok: false` |
| A4 | `validarNombre` | `"  Ana  "` | `ok: true`, valor `"Ana"` |
| A5 | `traducirError` | `23505` al inscribir (duplicado) | "Ya estás inscrito..." |
| A6 | `traducirError` | `P0001` + `taller_lleno` (cupo lleno) | "El taller ya no tiene cupos." |
| A7 | `traducirError` | `42501`, `invalid_credentials`, "Failed to fetch" | sesión expirada / credenciales / sin conexión |
| A8 | `traducirError` | código desconocido con `message` interno | mensaje genérico, sin el `message` crudo |
| A9 | `estadoTaller` | cupos 0 / inscrito / 3 / `null` | `lleno` / `inscrito` / `disponible` / `desconocido` |

## Manuales por estado (con backend y seed de T1)

| # | Estado | Pasos | Esperado |
|---|---|---|---|
| M1 | Sin config | Abrir sin `config.js` o con `config.example.js` | Aviso "Falta la configuración"; sin llamadas de red a Supabase; sin errores de consola salvo el 404 de `config.js` ausente |
| M2 | Sin sesión | Config válida, sin login | Formulario de acceso; no se ven talleres |
| M3 | Registro | "Crear cuenta" con correo y contraseña de 6+ caracteres | Con confirmación activa: aviso de revisar correo; sin ella: entra a la app |
| M4 | Login erróneo | Contraseña incorrecta | "Correo o contraseña incorrectos." |
| M5 | Inscrito | Escribir nombre y pulsar "Inscribirme" | Toast "Inscripción confirmada."; boleto en "Tu inscripción"; cupos bajan 1 |
| M6 | Nombre vacío | Pulsar "Inscribirme" sin nombre | Mensaje bajo el campo; no hay llamada de red |
| M7 | Duplicado | Inscribirse dos veces (segunda pestaña ya abierta) | "Ya estás inscrito en este taller." y la lista se actualiza |
| M8 | Cupo lleno | Taller con cupo 1 ocupado por otro usuario | Botón "Sin cupos" deshabilitado; si la carrera ocurre, "El taller ya no tiene cupos." |
| M9 | Cancelar | "Cancelar inscripción" y aceptar | Toast; el boleto desaparece; el cupo se libera |
| M10 | Sesión persistida | Recargar con sesión activa | Entra directo a la app (vía `getSession`, sin llamada de servidor para decidir) y el saludo muestra el correo |
| M11 | Cerrar sesión | "Cerrar sesión" | Vuelve al formulario de acceso (también si cierras sesión en otra pestaña, vía `onAuthStateChange`) |
| M12 | Sin conexión | Modo avión al inscribirse | "No hay conexión con el servidor..." |
| M13 | Celular | Teclado, zona segura, toques | Sin zoom al enfocar campos, botones de 44px+, sin parpadeo gris al tocar |

## Revisión de seguridad (código)

- Sin `innerHTML`, `eval` ni `document.write`: título, descripción y nombre entran con `textContent`.
- Solo `config.js` (ignorado por git) contiene claves; ninguna clave real en el repo.
