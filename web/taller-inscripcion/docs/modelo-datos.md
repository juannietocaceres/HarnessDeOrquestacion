---
documento: modelo-datos
recurso: "talleres e inscripciones"
proyecto: "e2e-skills-2"
tarea: "T1"
stack: "Supabase (Postgres + Supabase Auth con email y contraseña)"
fecha: "2026-10-05"
fuentes_consultadas: []   # sin consulta externa; forma tomada de la referencia expo-favoritos
---

# Modelo de datos: talleres e inscripciones

Un estudiante autenticado ve los talleres y se inscribe (o cancela) en ellos. Dependen de este documento el contrato (`contrato-api.md`), las pruebas RLS (`pruebas-rls.md`) y la interfaz (T2). La lista completa de inscritos la consulta el organizador en el panel de Supabase, no la web.

## Entidades

### `talleres`

Sin dueño: datos compartidos, de solo lectura para el cliente. Los gestiona el organizador en el panel.

| Campo | Tipo | Requerido | Por defecto | Lo asigna | Descripción | Validaciones / restricciones |
|---|---|:-:|---|---|---|---|
| `id` | uuid | Sí | generado | servidor | Identificador. | Clave primaria. |
| `titulo` | texto | Sí | — | panel | Nombre del taller. | 1 a 150 caracteres sin contar espacios de los extremos. |
| `descripcion` | texto | Sí | `''` | panel | Detalle. | Máx. 1000 caracteres. |
| `inicia_en` | fecha y hora (UTC) | Sí | — | panel | Inicio del taller. | ISO 8601 UTC. |
| `cupo` | entero | Sí | — | panel | Plazas totales. | Entre 1 y 1000. |
| `creado_en` | fecha y hora (UTC) | Sí | ahora | servidor | Creación. | Inmutable. |

### `inscripciones`

Dueño de cada fila: `user_id` (referencia a `auth.users.id`; no se duplica el usuario ni hay contraseñas propias).

| Campo | Tipo | Requerido | Por defecto | Lo asigna | Descripción | Validaciones / restricciones |
|---|---|:-:|---|---|---|---|
| `id` | uuid | Sí | generado | servidor | Identificador. | Clave primaria. |
| `user_id` | uuid | Sí | `auth.uid()` | servidor | Estudiante dueño. | FK a `auth.users`; el cliente no lo envía. |
| `taller_id` | uuid | Sí | — | cliente | Taller elegido. | FK a `talleres.id`. |
| `nombre` | texto | Sí | — | cliente | Nombre con que se inscribe. | 1 a 100 caracteres sin espacios de los extremos. |
| `creado_en` | fecha y hora (UTC) | Sí | ahora | servidor | Creación. | Inmutable. |

## Relaciones

| Desde | Hacia | Cardinalidad | Al borrar el padre | Notas |
|---|---|---|---|---|
| `inscripciones.user_id` | `auth.users.id` | N:1 | cascade | Si se borra la cuenta, se van sus inscripciones. |
| `inscripciones.taller_id` | `talleres.id` | N:1 | cascade | Si el organizador borra un taller, se van sus inscripciones. |

## Restricciones e índices

| Nombre | Tipo | Columnas | Para qué |
|---|---|---|---|
| `inscripciones_user_taller_key` | unique | `(user_id, taller_id)` | Impide inscribirse dos veces al mismo taller. |
| `inscripciones_taller_idx` | índice | `(taller_id)` | Conteo de cupo por taller. |
| `inscripciones_validar_cupo` | trigger before insert | — | Rechaza la inscripción si el taller ya llegó a `cupo` (cuenta todas las filas y bloquea el taller para evitar carreras). |
| `talleres_cupo_check` y checks de texto | check | ver tablas | Validación en la base, no solo en el cliente. |

## Reglas de acceso (resumen)

| Operación | Quién puede | Condición |
|---|---|---|
| Leer `talleres` | autenticado | Todas las filas. Anónimo: no (la web exige login; no se expone el catálogo sin sesión). |
| Escribir `talleres` | nadie desde el cliente | Solo el panel. |
| Leer `inscripciones` | autenticado | Solo `user_id = auth.uid()`. |
| Crear `inscripciones` | autenticado | `user_id = auth.uid()`; el cliente solo envía `taller_id` y `nombre`. |
| Actualizar `inscripciones` | nadie | Sin política y sin permiso de columna. |
| Borrar `inscripciones` (cancelar) | autenticado | Solo las propias. |

El SQL ejecutable está en `supabase/migrations/20261005000000_crear_talleres_inscripciones.sql`.

## Ejemplo de objeto válido (JSON)

```json
{
  "id": "00000000-0000-4000-8000-000000000000",
  "user_id": "00000000-0000-4000-8000-0000000000aa",
  "taller_id": "11111111-1111-4111-8111-111111111111",
  "nombre": "Ana Pérez",
  "creado_en": "2026-10-05T12:00:00Z"
}
```

## Ejemplo de objeto inválido y por qué

```json
{ "taller_id": "11111111-1111-4111-8111-111111111111", "nombre": "   " }
```

Inválido porque: `nombre` vacío tras quitar espacios rompe `inscripciones_nombre_check`.

## Fuera de alcance

- Edición de inscripciones, lista de espera, correo de confirmación y roles de organizador en la web: no los piden los criterios; el organizador usa el panel.
- Cancelar con fecha límite: se decidiría si una tarea posterior lo pide.

## Supuestos

- Un estudiante se inscribe una vez por taller; puede estar en varios talleres distintos.
- El cupo se valida en la base con un trigger `SECURITY DEFINER` (necesita contar filas ajenas, que RLS le oculta al cliente).
- Talleres legibles solo con sesión: la web ya exige registro para inscribirse.
- Hay un solo taller en el seed; el resto se crea en el panel.
