---
documento: modelo-datos
recurso: "tareas"
proyecto: "panel-tareas-demo (regresión de backend-datos)"
tarea: "T1"
stack: "sin fijar: el manifest no lo fija y la demo no persiste nada real (opción por defecto de la tabla: datos mock en JSON / SQLite)"
fecha: "2026-10-02"
fuentes_consultadas: []
---

# Modelo de datos: Tarea

Una tarea del panel de administración de tareas. De este documento dependen
el contrato de API (T2) y los componentes de UI (T3, T4, T5).

## Entidades

### `tarea`

Dueño de cada fila: sin dueño (el manifest no pide usuarios ni login).

| Campo | Tipo | Requerido | Por defecto | Lo asigna | Descripción | Validaciones / restricciones |
|---|---|:-:|---|---|---|---|
| `id` | uuid (string) | Sí | generado (UUID v4) | servidor | Identificador único. | Clave primaria; único. |
| `titulo` | string | Sí | — | cliente | Título corto de la tarea. | No vacío sin contar espacios; máximo 200 caracteres. |
| `estado` | enum (string) | Sí | `pendiente` | servidor al crear | Estado del ciclo de vida. | Uno de `pendiente`, `en_curso`, `hecha`. |
| `fecha_creacion` | fecha y hora (UTC) | Sí | ahora | servidor | Momento de creación. | ISO 8601 UTC (`YYYY-MM-DDThh:mm:ssZ`); inmutable. |

#### Enums

`estado`: valores exactos `pendiente`, `en_curso`, `hecha`. Cualquier otro
valor es inválido (sin mayúsculas ni sinónimos).

## Relaciones

Ninguna: una sola entidad.

## Restricciones e índices

| Nombre | Tipo | Columnas | Para qué |
|---|---|---|---|
| `tarea_pkey` | clave primaria | `(id)` | Unicidad del id. |
| `tarea_titulo_check` | check | `titulo` | `char_length(btrim(titulo)) between 1 and 200`. |
| `tarea_estado_check` | check | `estado` | Enum cerrado de tres valores. |

Sin índices extra: el contrato solo lista todo, sin filtros ni orden.

## Reglas de acceso (resumen)

Sin autenticación (fuera de alcance según T2). Si el panel se publicara con
datos reales, la falta de reglas de acceso sería un bloqueante: ver
"Supuestos".

## Ejemplo de objeto válido (JSON)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "titulo": "Revisar informe de gastos de septiembre",
  "estado": "pendiente",
  "fecha_creacion": "2026-09-17T14:30:00Z"
}
```

## Ejemplo de objeto inválido y por qué

```json
{ "id": "550e8400-e29b-41d4-a716-446655440000", "titulo": "   ", "estado": "Pendiente", "fecha_creacion": "2026-09-17T14:30:00Z" }
```

Inválido porque `titulo` queda vacío sin espacios y `estado` no es uno de
los tres valores exactos (mayúscula).

## Fuera de alcance

Descripción extendida, prioridad, responsable, vencimiento, etiquetas,
fecha de actualización: no los piden los criterios de T1.

## Supuestos

- Máximo de 200 caracteres para `titulo`: el manifest no lo fija; es un
  límite razonable para un título corto.
- Sin dueño ni reglas de acceso: el manifest es una demo de clase sin
  login. Publicarlo con datos reales requeriría volver a pasar por la
  skill (auth + reglas de acceso).
