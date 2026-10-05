---
documento: modelo-datos
recurso: "<nombre del recurso, p. ej. favoritos>"
proyecto: "<slug del proyecto o milestone>"
tarea: "<id de la tarea, p. ej. T1>"
stack: "<p. ej. Supabase (Postgres) | Firebase (Firestore) | Postgres | SQLite | mock JSON>"
fecha: "<AAAA-MM-DD>"
fuentes_consultadas: []   # [{url: "...", fecha: "AAAA-MM-DD", para: "qué se verificó"}]
---

# Modelo de datos: <Recurso>

<!--
Plantilla de la skill backend-datos (paso 2). Copia este archivo a
schema/<recurso>.md (o la convención del proyecto), llena el frontmatter y
borra los comentarios. Ejemplo de referencia: schema/tareas.md.
Regla: solo los campos que piden los criterios de aceptación; lo demás va
en "Fuera de alcance".
-->

Qué representa esta entidad en una o dos frases, y qué documentos dependen
de este (contrato de API, componentes de UI).

## Entidades

### `<entidad>`

Dueño de cada fila: `<campo que referencia al usuario del proveedor, o "sin dueño: datos públicos/compartidos">`.

| Campo | Tipo | Requerido | Por defecto | Lo asigna | Descripción | Validaciones / restricciones |
|---|---|:-:|---|---|---|---|
| `id` | uuid | Sí | generado | servidor | Identificador único. | Clave primaria. |
| `<campo>` | <tipo> | <Sí/No> | <valor o —> | <cliente/servidor> | <qué es> | <no vacío, longitud, enum, rango, formato> |
| `creado_en` | fecha y hora (UTC) | Sí | ahora | servidor | Momento de creación. | ISO 8601 UTC; inmutable. |

#### Enums

`<campo>`: valores exactos `<a>`, `<b>`, `<c>`. Cualquier otro valor es inválido.

## Relaciones

| Desde | Hacia | Cardinalidad | Al borrar el padre | Notas |
|---|---|---|---|---|
| `<entidad>.<campo>` | `<otra>.id` | N:1 | cascade / restrict / set null | <por qué esa acción> |

## Restricciones e índices

| Nombre | Tipo | Columnas | Para qué |
|---|---|---|---|
| `<entidad>_<campos>_key` | unique | `(<a>, <b>)` | <regla de negocio que impide duplicados> |
| `<entidad>_<campo>_idx` | índice | `(<campo>)` | <consulta del contrato que lo usa> |

Cada fila de esta tabla existe como restricción real en la base (o en las
reglas de acceso, si el proveedor no la soporta de forma nativa), no solo
como validación del cliente.

## Reglas de acceso (resumen)

| Operación | Quién puede | Condición |
|---|---|---|
| Leer | <autenticado / público> | <p. ej. solo filas propias> |
| Crear | | |
| Actualizar | | |
| Borrar | | |

El detalle ejecutable (políticas RLS o Security Rules) va en la migración
o en el archivo de reglas, no aquí.

## Ejemplo de objeto válido (JSON)

```json
{
  "id": "00000000-0000-4000-8000-000000000000",
  "<campo>": "<valor>",
  "creado_en": "2026-01-01T00:00:00Z"
}
```

## Ejemplo de objeto inválido y por qué

```json
{ "<campo>": "" }
```

Inválido porque: <restricción que rompe>.

## Fuera de alcance

Campos o entidades que no pidieron los criterios de aceptación y cuándo se
decidirían (p. ej. "prioridad: se decide si una tarea posterior la pide").

## Supuestos

- <supuesto tomado sin confirmación del usuario y por qué es razonable>
