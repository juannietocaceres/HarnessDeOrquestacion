# Esquema de datos: Tarea

Este documento define la forma de una tarea del panel de administración de
tareas: los campos que la componen, sus tipos y las validaciones que deben
cumplir. Es la base de la que dependen el contrato de API (T2) y los
componentes de UI (T3, T4, T5) del mismo milestone.

## Campos

| Campo            | Tipo             | Requerido | Descripción                                              | Validaciones |
|-------------------|------------------|:---------:|------------------------------------------------------------|--------------|
| `id`              | string           | Sí        | Identificador único de la tarea.                           | No vacío; único dentro del sistema. Formato recomendado: UUID v4. |
| `titulo`          | string           | Sí        | Título corto y descriptivo de la tarea.                    | No vacío (longitud mínima 1 carácter, sin contar espacios); longitud máxima 200 caracteres. |
| `estado`          | enum (string)    | Sí        | Estado actual de la tarea dentro de su ciclo de vida.       | Debe ser exactamente uno de estos tres valores: `pendiente`, `en_curso`, `hecha`. |
| `fecha_creacion`  | string (fecha y hora) | Sí   | Momento en el que la tarea fue creada.                      | Formato ISO 8601 con zona horaria UTC (`YYYY-MM-DDThh:mm:ssZ`); la asigna el sistema al crear la tarea; inmutable una vez creada. |

### Detalle de `estado`

`estado` es un enum cerrado con exactamente estos tres valores (sin
variantes, sin mayúsculas, sin sinónimos):

- `pendiente` — la tarea fue creada y todavía no se empezó a trabajar en ella.
- `en_curso` — la tarea está siendo trabajada actualmente.
- `hecha` — la tarea se completó.

Cualquier otro valor es inválido.

## Ejemplo de objeto válido (JSON)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "titulo": "Revisar informe de gastos de septiembre",
  "estado": "pendiente",
  "fecha_creacion": "2026-09-17T14:30:00Z"
}
```

Ejemplos adicionales, mostrando los otros dos valores de `estado`:

```json
{
  "id": "b3f1c2d4-9a3e-4f2b-8c1d-2e5f6a7b8c9d",
  "titulo": "Actualizar dependencias del proyecto",
  "estado": "en_curso",
  "fecha_creacion": "2026-09-15T09:00:00Z"
}
```

```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "titulo": "Preparar demo para la clase",
  "estado": "hecha",
  "fecha_creacion": "2026-09-10T18:45:00Z"
}
```

## Alcance

Este esquema incluye únicamente los campos pedidos por los criterios de
aceptación de T1: `id`, `titulo`, `estado` y `fecha_creacion`. No agrega
campos adicionales (por ejemplo: descripción extendida, prioridad,
responsable asignado, fecha de vencimiento, etiquetas, fecha de
actualización). Si alguno de esos campos resulta necesario para una tarea
posterior del milestone, esa ampliación del esquema se decide en ese
momento, no acá.
