---
documento: modelo-datos
recurso: "favoritos"
proyecto: "app Expo con login y favoritos (prueba de backend-datos)"
tarea: "prueba-expo"
stack: "Supabase (Postgres + Supabase Auth)"
fecha: "2026-10-02"
fuentes_consultadas:
  - {url: "https://supabase.com/docs/guides/database/postgres/row-level-security", fecha: "2026-10-02", para: "sintaxis de políticas RLS con (select auth.uid()) y to authenticated"}
  - {url: "https://docs.postgrest.org/en/stable/references/errors.html", fecha: "2026-10-02", para: "códigos HTTP de 23505 y 42501"}
---

# Modelo de datos: Favoritos

Lista de favoritos de cada usuario de la app, guardada en la nube para que
se vea igual en todos sus dispositivos. De este documento dependen
`contrato-favoritos.md` y la migración `20261002000000_crear_favoritos.sql`.

## Entidades

### `favoritos`

Dueño de cada fila: `user_id` (referencia a `auth.users.id`, el usuario de
Supabase Auth; no hay tabla propia de usuarios ni contraseñas).

| Campo | Tipo | Requerido | Por defecto | Lo asigna | Descripción | Validaciones / restricciones |
|---|---|:-:|---|---|---|---|
| `id` | uuid | Sí | `gen_random_uuid()` | servidor | Identificador del favorito. | Clave primaria. |
| `user_id` | uuid | Sí | `auth.uid()` | servidor | Dueño de la fila. | FK a `auth.users(id)`, `on delete cascade`; el cliente no puede escribirlo. |
| `item_id` | text | Sí | — | cliente | Id del elemento marcado (de la fuente de contenido de la app). | No vacío sin espacios; máximo 100 caracteres. |
| `titulo` | text | Sí | — | cliente | Título del elemento, guardado para mostrar la lista sin otra consulta. | No vacío sin espacios; máximo 200 caracteres. |
| `creado_en` | timestamptz | Sí | `now()` | servidor | Momento en que se marcó. | Inmutable. |

## Relaciones

| Desde | Hacia | Cardinalidad | Al borrar el padre | Notas |
|---|---|---|---|---|
| `favoritos.user_id` | `auth.users.id` | N:1 | cascade | Si el usuario borra su cuenta, sus favoritos se van con ella. |

## Restricciones e índices

| Nombre | Tipo | Columnas | Para qué |
|---|---|---|---|
| `favoritos_pkey` | clave primaria | `(id)` | Unicidad del id. |
| `favoritos_user_item_key` | unique | `(user_id, item_id)` | Un elemento se marca una sola vez por usuario. |
| `favoritos_item_id_check` | check | `item_id` | 1–100 caracteres sin contar espacios de los bordes. |
| `favoritos_titulo_check` | check | `titulo` | 1–200 caracteres sin contar espacios de los bordes. |
| `favoritos_user_creado_idx` | índice | `(user_id, creado_en desc)` | La consulta "mis favoritos, más recientes primero". |

## Reglas de acceso (resumen)

| Operación | Quién puede | Condición |
|---|---|---|
| Leer | autenticado | solo filas con `user_id = auth.uid()` |
| Crear | autenticado | `user_id = auth.uid()`; solo puede enviar `item_id` y `titulo` |
| Actualizar | nadie | un favorito no se edita: se quita y se vuelve a marcar |
| Borrar | autenticado | solo filas propias |
| Cualquiera | sin sesión (`anon`) | ninguna: sin permisos sobre la tabla |

Detalle ejecutable en la migración.

## Ejemplo de objeto válido (JSON)

```json
{
  "id": "00000000-0000-4000-8000-000000000001",
  "user_id": "00000000-0000-4000-8000-0000000000a1",
  "item_id": "receta-42",
  "titulo": "Arepas de queso",
  "creado_en": "2026-10-02T15:00:00Z"
}
```

## Ejemplo de objeto inválido y por qué

```json
{ "item_id": "receta-42", "titulo": "" }
```

Inválido porque `titulo` está vacío (rompe `favoritos_titulo_check`). Si
`item_id` ya estaba marcado por ese usuario, además rompe
`favoritos_user_item_key`.

## Fuera de alcance

Perfiles de usuario, carpetas o etiquetas de favoritos, orden manual,
compartir listas, notificaciones. El catálogo de elementos (`item_id`) es
externo a este modelo.

## Supuestos

- "Sincronizada" = la lista vive en la nube y la app la recarga al abrir o
  al volver a primer plano. Actualización en vivo entre dispositivos
  (Realtime) queda fuera de alcance.
- Los elementos favoritos vienen de un catálogo ajeno a este backend; por
  eso `item_id` es texto y no una FK.
- Se guarda `titulo` para mostrar la lista sin consultar el catálogo.
