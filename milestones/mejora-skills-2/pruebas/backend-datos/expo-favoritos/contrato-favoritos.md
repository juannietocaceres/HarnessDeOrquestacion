---
documento: contrato-api
recurso: "favoritos"
proyecto: "app Expo con login y favoritos (prueba de backend-datos)"
tarea: "prueba-expo"
modelo_de_datos: "schema-favoritos.md"
estilo: "operaciones sobre el proveedor (supabase-js), sin servidor propio"
fecha: "2026-10-02"
fuentes_consultadas:
  - {url: "https://docs.postgrest.org/en/stable/references/errors.html", fecha: "2026-10-02", para: "23505 -> 409; 42501 -> 403 autenticado / 401 anónimo"}
  - {url: "https://supabase.com/docs/guides/api/api-keys", fecha: "2026-10-02", para: "clave publicable segura en el cliente; secreta nunca"}
---

# Contrato de API: favoritos

La app Expo habla directo con Supabase mediante `supabase-js`: no hay
servidor propio. Cada "endpoint" es una operación del cliente sobre la
tabla `public.favoritos` (modelo en `schema-favoritos.md`). La API REST
que hay debajo la genera Supabase; los códigos HTTP de abajo son los que
esa API devuelve y que `supabase-js` expone en `error`.

## Alcance

**Incluye:** sesión (operaciones de Supabase Auth, no implementadas por
nosotros), listar, agregar y quitar favoritos.

**No incluye:** editar un favorito, actualización en vivo entre
dispositivos, recuperación de contraseña personalizada.

## Convenciones generales

- Toda operación sobre `favoritos` requiere sesión: el cliente de Supabase
  envía el token de la sesión automáticamente.
- Fechas en UTC, ISO 8601.
- Campos que asigna **siempre el servidor**: `id`, `user_id`, `creado_en`.
  Si el cliente los envía, la operación **se rechaza** (`403`): solo tiene
  permiso de insertar `item_id` y `titulo`.
- La app traduce los errores del proveedor al formato único de la UI; el
  texto nunca muestra SQL ni nombres internos:

```json
{ "error": "<codigo_maquina>", "campo": "<campo o null>", "mensaje": "<texto para humanos>" }
```

## Autenticación (del proveedor, no se implementa)

| Operación | Llamada | Notas |
|---|---|---|
| Registrarse | `supabase.auth.signUp({ email, password })` | Si el proyecto exige confirmar correo, la sesión llega después de confirmar (configuración del proyecto: `verificacion_manual`). |
| Iniciar sesión | `supabase.auth.signInWithPassword({ email, password })` | Error del proveedor → `error: "credenciales_invalidas"`. |
| Cerrar sesión | `supabase.auth.signOut()` | — |
| Sesión actual | `supabase.auth.getSession()` / `onAuthStateChange` | La sesión se guarda en el almacenamiento del dispositivo que indique la guía oficial de Supabase para Expo. |

Nada de hashing, tokens ni tabla de usuarios propios.

## Resumen de operaciones

| Operación | Llamada `supabase-js` | Auth | Éxito | Errores |
|---|---|:-:|---|---|
| Listar | `from('favoritos').select('id,item_id,titulo,creado_en').order('creado_en', { ascending: false })` | Sí | `200` + array | `401` |
| Agregar | `from('favoritos').insert({ item_id, titulo }).select('id,item_id,titulo,creado_en').single()` | Sí | `201` + objeto | `400`, `401`, `403`, `409` |
| Quitar | `from('favoritos').delete().eq('id', id)` | Sí | `204` | `401` |

## Listar

Devuelve los favoritos del usuario de la sesión, más recientes primero. La
regla RLS filtra: nunca aparecen filas de otro usuario, aunque el cliente
no filtre por `user_id`.

**Response — `200`**

```json
[
  { "id": "00000000-0000-4000-8000-000000000001", "item_id": "receta-2", "titulo": "Sancocho", "creado_en": "2026-10-02T15:05:00Z" },
  { "id": "00000000-0000-4000-8000-000000000002", "item_id": "receta-1", "titulo": "Arepas de queso", "creado_en": "2026-10-02T15:00:00Z" }
]
```

Sin favoritos: `200` con `[]`.

| Código | `error` (UI) | Cuándo |
|---|---|---|
| `401` | `no_autenticado` | Sin sesión (rol `anon` sin permisos sobre la tabla). |

## Agregar

**Request**

```json
{ "item_id": "receta-42", "titulo": "Arepas de queso" }
```

| Campo | Tipo | Requerido | Validación (heredada del modelo) |
|---|---|:-:|---|
| `item_id` | string | Sí | 1–100 caracteres sin espacios de borde. |
| `titulo` | string | Sí | 1–200 caracteres sin espacios de borde. |

La app valida lo mismo antes de enviar (solo UX); la validación que manda
es la de la base (`check`, `unique`, permisos por columna, RLS).

**Response — `201`**

```json
{ "id": "00000000-0000-4000-8000-000000000003", "item_id": "receta-42", "titulo": "Arepas de queso", "creado_en": "2026-10-02T15:10:00Z" }
```

| Código | `error` (UI) | Cuándo | Efecto |
|---|---|---|---|
| `400` | `item_id_invalido` / `titulo_invalido` | Vacío, solo espacios o largo de más (viola un `check`; Postgres `23514`) | No se crea nada |
| `401` | `no_autenticado` | Sin sesión | — |
| `403` | `prohibido` | Envía `id`, `user_id` o `creado_en` (sin permiso de columna), o `user_id` ajeno (RLS); Postgres `42501` | No se crea nada |
| `409` | `favorito_duplicado` | Ese `item_id` ya está en sus favoritos (Postgres `23505`) | No se crea otro |

## Quitar

**Request**: `id` del favorito.

**Response — `204`**, sin body. Si el `id` no existe o es de otro usuario,
RLS hace que no coincida ninguna fila: también `204` y no se borra nada (no
se filtra si el id existe). La app trata "no estaba" igual que "quitado".

| Código | `error` (UI) | Cuándo |
|---|---|---|
| `401` | `no_autenticado` | Sin sesión |

## Pruebas de contrato

Contra una base Supabase **local** con la migración y dos usuarios de
prueba (A y B), sin mocks del proveedor.

| # | Operación | Caso | Entrada | Esperado |
|---|---|---|---|---|
| C1 | Listar | feliz | sesión de A con 2 favoritos | `200`, 2 filas, más reciente primero |
| C2 | Listar | error: sin sesión | sin sesión | `401` |
| C3 | Listar | acceso: otro usuario | sesión de B | solo filas de B, ninguna de A |
| C4 | Listar | borde: vacío | usuario sin favoritos | `200` con `[]` |
| C5 | Agregar | feliz | A, `{item_id: "receta-9", titulo: "Bandeja"}` | `201`; `user_id` = A; `creado_en` del servidor |
| C6 | Agregar | error: `titulo` vacío | `{item_id: "x", titulo: "  "}` | `400`, nada creado |
| C7 | Agregar | error: duplicado | repetir C5 | `409` |
| C8 | Agregar | error: campo del servidor | `{item_id: "y", titulo: "Y", user_id: <B>}` con sesión de A | `403`, nada creado |
| C9 | Agregar | error: sin sesión | sin sesión | `401` |
| C10 | Quitar | feliz | A quita su favorito | `204`; ya no aparece en Listar |
| C11 | Quitar | acceso: otro usuario | B quita un `id` de A | `204` y la fila de A **sigue** existiendo |
| C12 | Quitar | error: sin sesión | sin sesión | `401` |

## Supuestos

- Los códigos `400` para `23514` y `401` para operaciones sin sesión se
  infieren de la tabla de errores de PostgREST (códigos no listados → `400`;
  `42501` anónimo → `401`). C2, C6, C9 y C12 son justamente las pruebas que
  lo confirman contra la base local antes de construir la UI.
- Supabase no devuelve el payload de error de la UI: la traducción
  (`23505` → `favorito_duplicado`, etc.) vive en una función de la app y
  tiene sus propias pruebas unitarias.
