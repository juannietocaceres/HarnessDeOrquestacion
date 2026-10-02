# Contrato de API: crear y listar tareas (T2)

Este documento define el contrato REST con el que un cliente (la UI del
panel: T3, T4 y T5) crea y consulta tareas. La forma de cada tarea es
exactamente la del esquema de T1 (`schema/tareas.md`): `id`, `titulo`,
`estado` y `fecha_creacion`.

El contrato no depende de cómo se guardan los datos. Se puede implementar en
memoria (para esta demo) o contra una base de datos real sin cambiar la forma
pública de la API.

## Convenciones generales

- **Formato**: todos los cuerpos de request y response son JSON
  (`Content-Type: application/json; charset=utf-8`).
- **Timestamps**: siempre en UTC, formato ISO 8601 `YYYY-MM-DDThh:mm:ssZ`
  (heredado de T1).
- **`estado`**: enum cerrado con exactamente tres valores: `pendiente`,
  `en_curso` o `hecha`.
- **Autenticación**: fuera de alcance; ningún endpoint la exige en este
  contrato.

## Campos que asigna el servidor

> **`id`, `estado` y `fecha_creacion` los asigna siempre el servidor, nunca
> el cliente.**

| Campo            | Valor que asigna el servidor al crear la tarea                     |
|------------------|--------------------------------------------------------------------|
| `id`             | UUID v4 nuevo y único.                                              |
| `estado`         | `"pendiente"` (siempre es el estado inicial).                       |
| `fecha_creacion` | Momento de la creación, en UTC e ISO 8601. No cambia nunca después. |

El único campo que envía el cliente al crear una tarea es `titulo`. Si el
request de `POST /tareas` trae además `id`, `estado` o `fecha_creacion`, el
servidor **los ignora** y usa sus propios valores. La respuesta `201` siempre
muestra los valores que asignó el servidor. Los clientes no deben enviar
estos campos.

---

## `POST /tareas` — crear una tarea

Crea una tarea nueva a partir de un título y devuelve el objeto completo.

### Request

**Cuerpo:**

| Campo    | Tipo   | Requerido | Validaciones (de T1)                                                                 |
|----------|--------|:---------:|--------------------------------------------------------------------------------------|
| `titulo` | string | Sí        | No vacío: al menos 1 carácter sin contar espacios. Máximo 200 caracteres. |

Ejemplo:

```http
POST /tareas HTTP/1.1
Content-Type: application/json
```

```json
{
  "titulo": "Revisar informe de gastos de septiembre"
}
```

### Response exitosa: `201 Created`

Devuelve la tarea completa recién creada, con los campos que asignó el
servidor. También incluye la cabecera `Location: /tareas/{id}` como
referencia. Este contrato no define `GET /tareas/{id}`, así que la cabecera
no promete que esa ruta exista.

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /tareas/550e8400-e29b-41d4-a716-446655440000
```

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "titulo": "Revisar informe de gastos de septiembre",
  "estado": "pendiente",
  "fecha_creacion": "2026-09-17T14:30:00Z"
}
```

### Errores de validación: `400 Bad Request`

Si la validación falla, el servidor responde `400 Bad Request` y **no crea la
tarea**, ni siquiera de forma parcial. La respuesta indica qué campo es
inválido y por qué.

**Forma del payload de error:**

| Campo                  | Tipo   | Descripción                                                    |
|------------------------|--------|----------------------------------------------------------------|
| `error`                | string | Código fijo del tipo de error: `"validacion"`.                 |
| `mensaje`              | string | Descripción general, para personas.                            |
| `detalles`             | array  | Un elemento por cada campo inválido.                           |
| `detalles[].campo`     | string | Nombre del campo inválido (por ejemplo, `"titulo"`).           |
| `detalles[].motivo`    | string | Código del motivo: `"requerido"`, `"vacio"` o `"muy_largo"`.   |
| `detalles[].mensaje`   | string | Explicación concreta para ese campo, para personas.            |

Los clientes deben basar su lógica en `error`, `campo` y `motivo`. Los
campos `mensaje` son solo para mostrar texto y pueden cambiar.

#### Caso 1: `titulo` faltante

Request:

```json
{}
```

Response `400 Bad Request`:

```json
{
  "error": "validacion",
  "mensaje": "El payload de la tarea no es válido.",
  "detalles": [
    {
      "campo": "titulo",
      "motivo": "requerido",
      "mensaje": "El campo titulo es obligatorio."
    }
  ]
}
```

#### Caso 2: `titulo` vacío (o solo con espacios)

Request:

```json
{
  "titulo": "   "
}
```

Response `400 Bad Request`:

```json
{
  "error": "validacion",
  "mensaje": "El payload de la tarea no es válido.",
  "detalles": [
    {
      "campo": "titulo",
      "motivo": "vacio",
      "mensaje": "El campo titulo no puede estar vacío."
    }
  ]
}
```

#### Otros casos que devuelven `400`

- `titulo` con más de 200 caracteres: `motivo: "muy_largo"`.
- `titulo` que no es una cadena (por ejemplo, un número o `null`): se trata
  igual que un título faltante, con `motivo: "requerido"`.
- Un cuerpo que no es JSON válido, o que no es un objeto JSON: `400` con
  `error: "validacion"` y `detalles` vacío.

---

## `GET /tareas` — listar tareas

Devuelve todas las tareas. Este contrato no incluye paginación, filtros ni
ordenamiento (ver "Fuera de alcance").

### Request

```http
GET /tareas HTTP/1.1
```

No lleva cuerpo ni parámetros.

### Response exitosa: `200 OK`

El cuerpo es un **array** de tareas. Cada tarea tiene exactamente la forma
del esquema de T1. El orden de los elementos no está garantizado: si el
cliente necesita un orden, lo aplica él (por ejemplo, por `fecha_creacion`).

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

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

Si no hay tareas, la respuesta sigue siendo `200 OK` con un array vacío:

```json
[]
```

---

## Resumen de endpoints

| Método | Ruta      | Cuerpo del request      | Éxito                          | Errores                     |
|--------|-----------|-------------------------|--------------------------------|-----------------------------|
| `POST` | `/tareas` | `{ "titulo": string }`  | `201 Created` + tarea completa | `400 Bad Request` (validación) |
| `GET`  | `/tareas` | (ninguno)               | `200 OK` + array de tareas     | (ninguno en este contrato)  |

## Fuera de alcance

- Actualizar (`PATCH`/`PUT`) o borrar (`DELETE`) tareas, incluido el cambio
  de `estado`.
- Consultar una tarea individual (`GET /tareas/{id}`).
- Autenticación y autorización.
- Paginación, filtros u ordenamiento del listado. Si el panel crece más allá
  de la demo, la paginación es la primera extensión a evaluar.
