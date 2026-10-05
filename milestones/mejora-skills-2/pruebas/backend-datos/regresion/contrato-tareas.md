---
documento: contrato-api
recurso: "tareas"
proyecto: "panel-tareas-demo (regresión de backend-datos)"
tarea: "T2"
modelo_de_datos: "pruebas/backend-datos/regresion/schema-tareas.md"
estilo: "REST propio"
fecha: "2026-10-02"
fuentes_consultadas: []
---

# Contrato de API: tareas

Crear y listar tareas del panel, sobre el modelo `schema-tareas.md`. La UI
(T3, T4, T5) se construye contra este documento. No asume motor de
persistencia: sirve en memoria o contra una base real.

## Alcance

**Incluye:** `POST /tareas`, `GET /tareas`.

**No incluye:** actualizar o borrar, autenticación, paginación/filtros/orden
(la descripción de T2 solo pide crear y listar).

## Convenciones generales

- `Content-Type: application/json` en todo request y response con body.
- Fechas en UTC, ISO 8601.
- Campos que asigna siempre el servidor: `id`, `estado` (inicial
  `pendiente`), `fecha_creacion`. Si el cliente los envía, se **ignoran**.
- Autenticación: ninguna (fuera de alcance).
- Formato único de error:

```json
{ "error": "<codigo_maquina>", "campo": "<campo o null>", "mensaje": "<texto para humanos>" }
```

## Resumen de endpoints

| Método | Ruta | Auth | Éxito | Errores |
|---|---|:-:|---|---|
| `POST` | `/tareas` | No | `201` | `400` |
| `GET` | `/tareas` | No | `200` | — (caso borde: lista vacía) |

## `POST /tareas`

Crea una tarea.

### Request

```json
{ "titulo": "Revisar informe de gastos de septiembre" }
```

| Campo | Tipo | Requerido | Validación |
|---|---|:-:|---|
| `titulo` | string | Sí | No vacío sin contar espacios; máximo 200 caracteres. |

### Response — `201 Created`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "titulo": "Revisar informe de gastos de septiembre",
  "estado": "pendiente",
  "fecha_creacion": "2026-09-17T14:30:00Z"
}
```

### Errores

| Código | `error` | Cuándo | Efecto |
|---|---|---|---|
| `400` | `titulo_invalido` | `titulo` falta, es vacío/solo espacios o supera 200 caracteres | No se crea nada |

```json
{ "error": "titulo_invalido", "campo": "titulo", "mensaje": "El campo 'titulo' es requerido y no puede estar vacío." }
```

## `GET /tareas`

Lista todas las tareas.

### Response — `200 OK`

Array de objetos con la forma del modelo. Sin tareas: `200` con `[]`.

### Errores

Ninguno de negocio: no hay parámetros ni auth. El caso borde cubierto es la
lista vacía.

## Pruebas de contrato

| # | Endpoint | Caso | Entrada | Esperado |
|---|---|---|---|---|
| C1 | `POST /tareas` | feliz | `{"titulo": "Comprar café"}` | `201`; `estado: "pendiente"`; `id` UUID; `fecha_creacion` ISO 8601 UTC |
| C2 | `POST /tareas` | error: vacío | `{"titulo": ""}` | `400`, `error: titulo_invalido`, `campo: titulo`; `GET` no la lista |
| C3 | `POST /tareas` | error: solo espacios | `{"titulo": "   "}` | igual que C2 |
| C4 | `POST /tareas` | error: falta | `{}` | igual que C2 |
| C5 | `POST /tareas` | borde: 200 / 201 caracteres | `titulo` de 200 y de 201 | `201` y `400` respectivamente |
| C6 | `POST /tareas` | campos del servidor ignorados | `{"titulo": "x", "estado": "hecha", "id": "abc"}` | `201` con `estado: "pendiente"` e `id` generado |
| C7 | `GET /tareas` | feliz | tras C1 | `200`, array que incluye la tarea de C1 con la forma exacta |
| C8 | `GET /tareas` | borde (sin error de negocio) | almacenamiento vacío | `200` con `[]` |

## Supuestos

- Campos de servidor enviados por el cliente se ignoran (no se rechazan):
  es lo menos sorpresivo para una UI de demo.
