---
documento: contrato-api
recurso: "<nombre del recurso, p. ej. favoritos>"
proyecto: "<slug del proyecto o milestone>"
tarea: "<id de la tarea, p. ej. T2>"
modelo_de_datos: "<ruta, p. ej. schema/favoritos.md>"
estilo: "<REST propio | operaciones sobre el proveedor (supabase-js / Firestore SDK)>"
fecha: "<AAAA-MM-DD>"
fuentes_consultadas: []   # [{url: "...", fecha: "AAAA-MM-DD", para: "qué se verificó"}]
---

# Contrato de API: <recurso>

<!--
Plantilla de la skill backend-datos (paso 3). Copia este archivo a
api/contrato-<recurso>.md (o la convención del proyecto), llena el
frontmatter y borra los comentarios. Ejemplo de referencia:
api/contrato-tareas.md.
Si el cliente habla directo con el proveedor (sin servidor propio), cada
"endpoint" es una operación del SDK: documenta tabla/colección, filtro y
columnas en lugar de método y ruta, y los errores que devuelve el proveedor.
-->

Qué cubre este contrato y sobre qué modelo de datos se apoya
(`<ruta del modelo>`). La UI y las pruebas se construyen contra este
documento.

## Alcance

**Incluye:** <lista de endpoints u operaciones>.

**No incluye:** <lo que queda fuera y por qué>.

## Convenciones generales

- `Content-Type: application/json` en todo request y response con body.
- Fechas en UTC, ISO 8601.
- Campos que asigna **siempre el servidor** (el cliente no los envía; si
  los envía, se ignoran o se rechazan — decide uno y escríbelo):
  `<id, creado_en, dueño>`.
- Autenticación: <ninguna | sesión del proveedor (token en `Authorization: Bearer`) | otra>.
- Formato único de error:

```json
{ "error": "<codigo_maquina>", "campo": "<campo o null>", "mensaje": "<texto para humanos, sin detalles internos>" }
```

## Resumen de endpoints

| Método / operación | Ruta / tabla | Auth | Éxito | Errores |
|---|---|:-:|---|---|
| `<POST>` | `/<recurso>` | Sí/No | `201` | `400`, `401`, `409` |
| `<GET>` | `/<recurso>` | Sí/No | `200` | `401` |

## `<MÉTODO> /<ruta>`

<Qué hace, en una frase.>

**Autenticación**: <requerida / no requerida; qué filas ve el usuario>.

### Request

```json
{ "<campo>": "<valor>" }
```

| Campo | Tipo | Requerido | Validación (heredada del modelo) |
|---|---|:-:|---|
| `<campo>` | <tipo> | Sí | <regla> |

### Response — `<código> <texto>`

```json
{ "id": "00000000-0000-4000-8000-000000000000", "<campo>": "<valor>" }
```

### Errores

| Código | `error` | Cuándo | Efecto |
|---|---|---|---|
| `400` | `<campo>_invalido` | <entrada no válida según el modelo> | No se crea nada (sin efecto parcial) |
| `401` | `no_autenticado` | Sin sesión válida | — |
| `403` | `prohibido` | Sesión válida pero la regla de acceso lo rechaza | — |
| `409` | `<recurso>_duplicado` | Rompe una restricción `unique` | — |

<!-- Repite la sección por cada endpoint u operación. -->

## Pruebas de contrato

Coordinadas con la skill `testing`. Cada endpoint u operación tiene al
menos un caso feliz y uno de error; cada código de error de arriba aparece
en al menos un caso; cada regla de acceso tiene su caso de "otro usuario"
y de "sin sesión".

| # | Endpoint / operación | Caso | Entrada | Esperado |
|---|---|---|---|---|
| C1 | `<POST /recurso>` | feliz | <entrada válida> | `201` + objeto con la forma del modelo |
| C2 | `<POST /recurso>` | error | <entrada inválida> | `400` + `error: <código>`; nada creado |
| C3 | `<GET /recurso>` | acceso: otro usuario | sesión de B | no devuelve filas de A |
| C4 | `<GET /recurso>` | acceso: sin sesión | sin token | `401` (o lista vacía, según el proveedor: escribe cuál) |

## Supuestos

- <supuesto y por qué es razonable>
