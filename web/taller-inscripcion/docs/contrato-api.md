---
documento: contrato-api
recurso: "talleres e inscripciones"
proyecto: "e2e-skills-2"
tarea: "T1"
modelo_de_datos: "docs/modelo-datos.md"
estilo: "operaciones sobre el proveedor (supabase-js desde el navegador)"
fecha: "2026-10-05"
fuentes_consultadas: []   # sin consulta externa; confirmar nombres de métodos de supabase-js en la doc oficial al implementar T2
---

# Contrato de API: talleres e inscripciones

Operaciones que usa el cliente (`supabase-js`, clave anon + sesión del usuario) sobre el modelo `docs/modelo-datos.md`. La UI (T2) y las pruebas (`pruebas-rls.md`) se construyen contra este documento.

## Alcance

**Incluye:** registro, login y logout (Supabase Auth), listar talleres, cupos disponibles, listar mis inscripciones, inscribirse, cancelar.

**No incluye:** editar inscripción, listar inscripciones ajenas (solo panel), administrar talleres.

## Convenciones generales

- Fechas en UTC, ISO 8601.
- Los campos `id`, `user_id`, `creado_en` los asigna siempre el servidor; un insert que los envíe es rechazado por permisos de columna (`42501`).
- Autenticación: sesión de Supabase Auth (email y contraseña); el SDK envía el JWT. Sin hashing ni tokens propios.
- Errores: los del proveedor, como `{ code, message }` en `error` de supabase-js. La UI los traduce a mensajes humanos y no muestra `message` crudo.

## Resumen de operaciones

| Operación | Tabla / función | Auth | Éxito | Errores |
|---|---|:-:|---|---|
| Registrarse | `auth.signUp({ email, password })` | No | usuario (sesión según confirmación de correo) | email inválido, contraseña corta, usuario ya existe |
| Iniciar sesión | `auth.signInWithPassword({ email, password })` | No | sesión | credenciales inválidas |
| Cerrar sesión | `auth.signOut()` | Sí | — | — |
| Listar talleres | `from('talleres').select('id,titulo,descripcion,inicia_en,cupo').order('inicia_en')` | Sí | arreglo (puede ser `[]`) | sin sesión: `[]` o `401` |
| Cupos disponibles | `rpc('cupos_disponibles', { p_taller_id })` | Sí | entero (>= 0), `null` si el taller no existe | sin sesión: `42501` |
| Mis inscripciones | `from('inscripciones').select('id,taller_id,nombre,creado_en')` | Sí | solo filas propias (`[]` si no hay) | sin sesión: `[]` o `401` |
| Inscribirse | `from('inscripciones').insert({ taller_id, nombre })` | Sí | fila creada (con `.select()`) | `23505`, `23503`, `23514`, `P0001`, `42501` |
| Cancelar | `from('inscripciones').delete().eq('id', id).select()` | Sí | arreglo con la fila borrada | ajena o inexistente: arreglo vacío, sin error |

## Inscribirse

Crea la inscripción del usuario en un taller.

**Autenticación**: requerida; `user_id` lo pone el servidor.

### Request

```json
{ "taller_id": "11111111-1111-4111-8111-111111111111", "nombre": "Ana Pérez" }
```

| Campo | Tipo | Requerido | Validación |
|---|---|:-:|---|
| `taller_id` | uuid | Sí | Debe existir en `talleres`. |
| `nombre` | texto | Sí | 1 a 100 caracteres sin espacios extremos. |

### Response: fila creada

```json
{ "id": "00000000-0000-4000-8000-000000000000", "taller_id": "11111111-1111-4111-8111-111111111111", "nombre": "Ana Pérez", "creado_en": "2026-10-05T12:00:00Z" }
```

### Errores

| Código | Significado | Cuándo | Efecto |
|---|---|---|---|
| `23505` | inscripción duplicada | Ya inscrito en ese taller (`inscripciones_user_taller_key`) | No se crea nada |
| `P0001`, mensaje `taller_lleno` | cupo agotado | El taller ya tiene `cupo` inscritos | No se crea nada |
| `23503` | taller inexistente | `taller_id` no existe | No se crea nada |
| `23514` | dato inválido | `nombre` vacío o demasiado largo | No se crea nada |
| `42501` | prohibido | Sin sesión, o envía `user_id`/`id`/`creado_en`, o `user_id` distinto al propio | No se crea nada |

## Cancelar inscripción

`delete().eq('id', id).select()`: RLS limita el borrado a filas propias. Si el `id` es ajeno o no existe, borra 0 filas y no devuelve error; la UI trata el arreglo vacío como "no encontrada". Sin sesión: no borra nada. Al cancelar, el cupo se libera.

## Listados (talleres, mis inscripciones, cupos)

Solo lectura, sin parámetros de negocio: no tienen error de negocio. Su "caso de error" es el caso borde principal: lista vacía (sin talleres o sin inscripciones).

## Pruebas de contrato

Los casos de acceso RLS (otro usuario, sin sesión, columnas protegidas) están en `pruebas-rls.md` (R1 a R14). Se ejecutan contra una base local de Supabase, no contra mocks.

| # | Operación | Caso | Entrada | Esperado |
|---|---|---|---|---|
| C1 | Inscribirse | feliz | taller válido, nombre válido | fila creada con `user_id` propio |
| C2 | Inscribirse | duplicado | mismo taller dos veces | `23505`; una sola fila |
| C3 | Inscribirse | cupo lleno | taller con cupo 1 ya ocupado por otro usuario | `P0001` `taller_lleno` |
| C4 | Inscribirse | nombre inválido | `"   "` | `23514`; nada creado |
| C5 | Inscribirse | taller inexistente | uuid aleatorio | `23503` |
| C6 | Cancelar | feliz | id propio | fila desaparece; el cupo se libera |
| C7 | Cancelar | ajena | id de otro usuario | arreglo vacío; la fila de A sigue |
| C8 | Mis inscripciones | feliz y borde | usuario con y sin inscripciones | solo las propias / `[]` |
| C9 | Talleres | feliz y borde | con sesión | lista del seed / `[]` si no hay talleres |
| C10 | Cupos | feliz | taller del seed con 1 inscripción | `cupo - 1` |
| C11 | Cualquiera | sin sesión | clave anon sin login | lecturas: `[]` o `42501`; insert rechazado |

## Supuestos

- Sin sesión, supabase-js devuelve lista vacía o error de permisos; la UI trata ambos como "inicia sesión".
- La confirmación de correo se configura en el panel (verificación manual del milestone).
- Los nombres exactos de métodos de supabase-js se confirman en la doc oficial durante T2.
