# Contrato de API: crear y listar tareas

Milestone `panel-tareas-demo` · Tarea T2 · Basado en el esquema de T1 (`schema/tareas.md`).

Este documento define la forma pública de la API REST del panel de tareas para
**crear** (`POST /tareas`) y **listar** (`GET /tareas`) tareas. La UI del panel
(T3, T4, T5) se construye contra este contrato, no contra una implementación.

## 1. Convenciones generales

- Formato: JSON en request y response (`Content-Type: application/json; charset=utf-8`).
- Codificación: UTF-8.
- Fechas: siempre string ISO 8601 en UTC con el formato `YYYY-MM-DDThh:mm:ssZ`
  (por ejemplo `2026-09-17T14:30:00Z`), consistente con el esquema de T1.
- Persistencia: el contrato no asume ningún motor. Puede implementarse en
  memoria (demo) o con una base de datos real sin cambiar la forma pública.
- Sin autenticación ni autorización en este alcance.

## 2. Recurso `Tarea`

Forma exacta definida por T1. Los cuatro campos son siempre requeridos en las
respuestas y no existen campos adicionales.

| Campo | Tipo | Reglas | Quién lo asigna |
|---|---|---|---|
| `id` | string | Único, no vacío. UUID v4. | **Servidor** |
| `titulo` | string | No vacío (mín. 1 carácter sin contar espacios), máx. 200 caracteres. | Cliente |
| `estado` | string (enum) | Exactamente `pendiente`, `en_curso` o `hecha`. Cualquier otro valor es inválido. | **Servidor** (inicial `pendiente`) |
| `fecha_creacion` | string | ISO 8601 UTC (`YYYY-MM-DDThh:mm:ssZ`). Momento de creación. Inmutable. | **Servidor** |

### Campos asignados por el servidor

> **`id`, `estado` y `fecha_creacion` los asigna siempre el servidor — nunca el
> cliente.**
>
> - `id`: el servidor genera un UUID v4 al crear la tarea.
> - `estado`: el servidor fija el estado inicial en `"pendiente"`.
> - `fecha_creacion`: el servidor registra el momento de creación en UTC.
>
> El cliente nunca envía estos campos. Si el payload de `POST /tareas` los
> incluye, el servidor los **ignora** y usa siempre sus propios valores (ver
> §3.3). El único campo que controla el cliente es `titulo`.

## 3. `POST /tareas` — crear una tarea

Crea una tarea nueva a partir de un título.

### 3.1 Request

- Método y ruta: `POST /tareas`
- Headers: `Content-Type: application/json`
- Body:

| Campo | Tipo | Requerido | Reglas |
|---|---|---|---|
| `titulo` | string | Sí | No vacío (mín. 1 carácter sin contar espacios), máx. 200 caracteres. |

Ejemplo de request:

```json
{
  "titulo": "Revisar informe de gastos de septiembre"
}
```

### 3.2 Response exitosa — `201 Created`

Devuelve el objeto `Tarea` completo, con los campos asignados por el servidor.

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "titulo": "Revisar informe de gastos de septiembre",
  "estado": "pendiente",
  "fecha_creacion": "2026-09-17T14:30:00Z"
}
```

### 3.3 Reglas de validación

1. El body debe ser un objeto JSON.
2. `titulo` debe estar presente y ser de tipo string.
3. `titulo` no puede ser cadena vacía ni contener solo espacios.
4. `titulo` no puede superar los 200 caracteres.
5. Si el cliente envía `id`, `estado` o `fecha_creacion`, el servidor los
   ignora: no generan error y nunca sobrescriben los valores del servidor.
6. La operación es atómica: si alguna validación falla, **no se crea la tarea**
   (ni parcial ni totalmente) y se responde con error.

### 3.4 Error de validación — `400 Bad Request`

Se responde `400 Bad Request` cuando `titulo` falta, es cadena vacía (o solo
espacios), no es string o supera 200 caracteres. La respuesta identifica el
campo inválido.

Forma del payload de error:

| Campo | Tipo | Descripción |
|---|---|---|
| `error` | string | Código de error estable. Para validación: `"validacion"`. |
| `mensaje` | string | Descripción legible del problema. |
| `campo` | string | Nombre del campo inválido (`"titulo"`). |

Ejemplo — `titulo` faltante.

Request:

```json
{}
```

Response `400 Bad Request`:

```json
{
  "error": "validacion",
  "mensaje": "El campo 'titulo' es requerido.",
  "campo": "titulo"
}
```

Ejemplo — `titulo` vacío.

Request:

```json
{
  "titulo": ""
}
```

Response `400 Bad Request`:

```json
{
  "error": "validacion",
  "mensaje": "El campo 'titulo' no puede estar vacío.",
  "campo": "titulo"
}
```

Ejemplo — `titulo` demasiado largo (más de 200 caracteres): misma forma, con
`"mensaje": "El campo 'titulo' no puede superar 200 caracteres."`.

## 4. `GET /tareas` — listar tareas

Devuelve todas las tareas existentes.

### 4.1 Request

- Método y ruta: `GET /tareas`
- Sin body ni parámetros de query.

### 4.2 Response exitosa — `200 OK`

Un array JSON de objetos `Tarea`, cada uno con la forma exacta del esquema de
T1. Si no hay tareas, la respuesta es un array vacío `[]` (también `200 OK`).

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

El orden del array no está garantizado por este contrato (ver §5).

## 5. Fuera de alcance

- Actualizar (`PATCH` / `PUT`) y borrar (`DELETE`) tareas. Por eso, en este
  alcance toda tarea creada por la API nace y permanece en `pendiente`; los
  estados `en_curso` y `hecha` existen en el esquema y pueden aparecer en el
  listado (por ejemplo, en datos de demo).
- Autenticación y autorización.
- Paginación, filtros y ordenamiento del listado. La paginación es la primera
  extensión a evaluar si el volumen crece.

## 6. Resumen para la UI (T3, T4, T5)

| Necesidad | Endpoint | Dato usado |
|---|---|---|
| Lista de tareas (T3) | `GET /tareas` | Array de `Tarea`; `estado` para distinguir visualmente. |
| Formulario de alta (T4) | `POST /tareas` | Un único campo de entrada: `titulo` (requerido, 1–200 caracteres, no solo espacios). Mostrar `mensaje` del error `400`. |
| Contador de pendientes (T5) | `GET /tareas` | Contar elementos con `estado == "pendiente"`. |
