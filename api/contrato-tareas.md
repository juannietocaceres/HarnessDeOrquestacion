# Contrato de API: tareas

Este documento define el contrato REST para crear y listar tareas del panel
de administración de tareas. Implementa la especificación
[T2 — Contrato de API](../milestones/panel-tareas-demo/especificaciones/T2-contrato-api.md)
sobre la forma de datos fijada en [schema/tareas.md](../schema/tareas.md) (T1).
La UI del panel (T3, T4, T5) se construye contra este documento.

## Alcance

**Incluye:**
- `POST /tareas` — crear una tarea.
- `GET /tareas` — listar todas las tareas.
- El caso de error de validación de `POST /tareas`.

**No incluye** (ver la especificación para el detalle): actualizar
(`PATCH`/`PUT`) o borrar (`DELETE`) una tarea; autenticación/autorización;
paginación, filtros u ordenamiento en el listado.

## Convenciones generales

- Todos los requests y responses con body usan `Content-Type: application/json`.
- Todo timestamp está en UTC, formato ISO 8601 (`YYYY-MM-DDThh:mm:ssZ`).
- `id`, `estado` y `fecha_creacion` los asigna **siempre el servidor**. El
  cliente nunca los envía ni puede fijar su valor; si los incluyera de todos
  modos en el body de `POST /tareas`, el servidor los ignora y calcula los
  suyos.
- Cada tarea devuelta por la API tiene la forma exacta definida en
  [schema/tareas.md](../schema/tareas.md): `id`, `titulo`, `estado`,
  `fecha_creacion`. Este contrato no agrega campos adicionales a esa forma.
- El contrato no asume un motor de persistencia específico: es
  implementable tanto en memoria (suficiente para esta demo) como contra una
  base de datos real, sin cambiar la forma pública descrita acá.

## Resumen de endpoints

| Método | Ruta      | Éxito         | Error             |
|--------|-----------|---------------|-------------------|
| POST   | `/tareas` | `201 Created` | `400 Bad Request` |
| GET    | `/tareas` | `200 OK`      | —                 |

## `POST /tareas`

Crea una tarea nueva.

### Request

```
POST /tareas
Content-Type: application/json
```

```json
{
  "titulo": "Revisar informe de gastos de septiembre"
}
```

| Campo    | Tipo   | Requerido | Validación |
|----------|--------|:---------:|------------|
| `titulo` | string | Sí        | No vacío sin contar espacios; máximo 200 caracteres (heredado de `schema/tareas.md`). |

Ningún otro campo del body es necesario ni tiene efecto: `id`, `estado` y
`fecha_creacion` los calcula el servidor (ver "Convenciones generales").

### Response — `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "titulo": "Revisar informe de gastos de septiembre",
  "estado": "pendiente",
  "fecha_creacion": "2026-09-17T14:30:00Z"
}
```

- `id`: generado por el servidor (UUID v4).
- `estado`: siempre `"pendiente"` — es el único estado inicial posible de una
  tarea recién creada.
- `fecha_creacion`: momento de creación en el servidor, UTC, ISO 8601.

### Response de error — `400 Bad Request`

Caso: `titulo` ausente o inválido según `schema/tareas.md` (cadena vacía o
compuesta solo de espacios). La tarea **no** se crea — no hay efecto
parcial.

Request de ejemplo (inválido):

```json
{
  "titulo": ""
}
```

Response:

```json
{
  "error": "titulo_invalido",
  "campo": "titulo",
  "mensaje": "El campo 'titulo' es requerido y no puede estar vacío."
}
```

El mismo patrón de error (mismo status `400`, misma forma de payload,
`campo: "titulo"`) aplica si `titulo` falta directamente del body, o si
excede el máximo de 200 caracteres definido en el esquema.

## `GET /tareas`

Lista todas las tareas existentes.

### Request

```
GET /tareas
```

Sin body y sin parámetros de consulta — el listado no admite paginación,
filtros ni ordenamiento en este contrato (fuera de alcance; ver "Preguntas
abiertas" de la especificación de T2).

### Response — `200 OK`

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "titulo": "Revisar informe de gastos de septiembre",
    "estado": "pendiente",
    "fecha_creacion": "2026-09-17T14:30:00Z"
  },
  {
    "id": "b3f1c2d4-9a3e-4f2b-8c1d-2e5f6a7b8c9d",
    "titulo": "Actualizar dependencias del proyecto",
    "estado": "en_curso",
    "fecha_creacion": "2026-09-15T09:00:00Z"
  },
  {
    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "titulo": "Preparar demo para la clase",
    "estado": "hecha",
    "fecha_creacion": "2026-09-10T18:45:00Z"
  }
]
```

Cada elemento tiene la forma exacta de `schema/tareas.md`. Si todavía no hay
tareas creadas, la respuesta es `200 OK` con un array vacío: `[]`.
