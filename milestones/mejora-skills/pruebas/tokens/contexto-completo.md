## Especificación de T2 (milestones/panel-tareas-demo/especificaciones/T2-contrato-api.md)

# Especificación: Contrato de API — crear y listar tareas (T2)

## Contexto

El manifest del milestone "Panel de administración de tareas" trajo la
tarea T2 sin `criterios_aceptacion` — solo el título y una descripción de
una línea. Antes de que un sub-agente la implemente hace falta un contrato
explícito: la UI (T3, T4, T5) va a construirse *contra* este documento, no
contra el código del backend, así que cualquier ambigüedad acá se propaga a
las tres tareas de la wave siguiente.

## Objetivo

Que un cliente (la UI del panel) pueda crear y consultar tareas de forma
predecible, sin conocer detalles internos de almacenamiento — usando
siempre la forma de datos ya fijada en [schema/tareas.md](../../../schema/tareas.md) (T1).

## Alcance

**Incluye:**
- `POST /tareas` — crear una tarea.
- `GET /tareas` — listar todas las tareas.
- Validación del payload de creación contra el esquema de T1.
- Al menos un caso de error de validación documentado.

**No incluye:**
- Actualizar (`PATCH`/`PUT`) o borrar (`DELETE`) una tarea.
- Autenticación/autorización.
- Paginación, filtros u ordenamiento en el listado (ver "Preguntas
  abiertas" — es una extensión futura, no parte de este contrato).

## Requisitos funcionales

- **RF1**: `POST /tareas` recibe `{ "titulo": string }` (requerido). El
  servidor asigna `id` (UUID v4), `estado` inicial (`"pendiente"`) y
  `fecha_creacion` (ISO 8601 UTC, momento de creación) — el cliente nunca
  los envía. Responde `201 Created` con el objeto completo.
- **RF2**: `GET /tareas` responde `200 OK` con un array de tareas, cada una
  con la forma exacta del esquema de T1.
- **RF3**: si `titulo` falta o es una cadena vacía, `POST /tareas` responde
  `400 Bad Request` con el campo inválido identificado — nunca crea la
  tarea parcialmente.

## Requisitos no funcionales

- Todos los timestamps en UTC, formato ISO 8601 (heredado de T1;
  consistencia obligatoria entre esquema y contrato).
- El contrato no asume un motor de persistencia específico — es
  implementable tanto en memoria (para esta demo) como contra una base de
  datos real, sin cambiar la forma pública de la API.

## Criterios de aceptación

- [ ] `POST /tareas` documentado con request y response de ejemplo en JSON.
- [ ] `GET /tareas` documentado con response de ejemplo en JSON (array).
- [ ] El caso de error de validación (`titulo` vacío/faltante) documentado
      con código de estado y payload de respuesta.
- [ ] Explícito que `id`, `estado` y `fecha_creacion` los asigna siempre el
      servidor — nunca el cliente.

## Preguntas abiertas

- ¿El listado necesita paginación? Fuera de alcance para esta demo (volumen
  bajo, milestone ficticio de clase). Si el panel creciera más allá de la
  demo, es la primera extensión a evaluar — no bloquea la implementación de
  T2 tal como está especificada acá.

## Resultado de T1, del que depende T2 (schema/tareas.md)

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

## Manifest del milestone (milestones/panel-tareas-demo/milestone.yaml)

```yaml
milestone: "Panel de administración de tareas (demo de clase)"
cap_concurrencia: 2   # deliberadamente menor al default (3), para forzar que la wave 3 (3 tareas listas) se parta en 2 lotes y se vea el cap en acción
tareas:
  - id: T1
    titulo: "Modelo de datos de tareas"
    tipo: backend
    depende_de: []
    descripcion: >
      Definir el esquema de datos de una tarea del panel (campos, tipos,
      validaciones) y dejarlo documentado en schema/tareas.md, con al menos
      un ejemplo en JSON.
    criterios_aceptacion:
      - "El esquema define al menos: id, titulo, estado, fecha_creacion."
      - "estado es un enum con estos valores exactos: pendiente, en_curso, hecha."
      - "Incluye al menos un ejemplo de objeto válido en JSON."

  - id: T2
    titulo: "Contrato de API: crear y listar tareas"
    tipo: backend
    depende_de: [T1]
    descripcion: >
      Documentar el contrato REST para crear y listar tareas del panel,
      basado en el esquema que resulte de T1.
    criterios_aceptacion: []   # deliberadamente vacío: dispara /especificacion antes de implementar (ver §8 de orquestador/SKILL.md)

  - id: T3
    titulo: "Componente UI: lista de tareas"
    tipo: frontend
    depende_de: [T2]
    descripcion: >
      Construir un componente estático (HTML/CSS/JS sin build step) que
      renderiza una lista de tareas de ejemplo usando la forma de datos del
      contrato de T2, en ui/lista-tareas.html.
    criterios_aceptacion:
      - "Renderiza al menos 3 tareas de ejemplo con su estado visualmente distinguible."
      - "Sigue los principios de la skill frontend-design (elección deliberada de tipografía/color, no defaults genéricos)."

  - id: T4
    titulo: "Componente UI: formulario de nueva tarea"
    tipo: frontend
    depende_de: [T2]
    descripcion: >
      Construir un componente estático (HTML/CSS/JS sin build step) con un
      formulario para crear una tarea, acorde al payload de POST /tareas
      definido en T2, en ui/nueva-tarea.html.
    criterios_aceptacion:
      - "El formulario incluye los campos requeridos por el contrato de T2."
      - "Sigue los principios de la skill frontend-design."

  - id: T5
    titulo: "Indicador de tareas pendientes"
    tipo: frontend
    depende_de: [T2]
    descripcion: >
      Construir un componente pequeño (badge/contador) que muestra cuántas
      tareas están pendientes, en ui/badge-pendientes.html.
    criterios_aceptacion:
      - "Muestra un número y una etiqueta clara del estado 'pendientes'."
```

## Decisiones de waves previas (milestones/panel-tareas-demo/decisiones.md)

## Wave 1

- **T1**: sin decisiones. El sub-agente completó directo — el propio
  enunciado ya resolvía la única ambigüedad posible (si agregar campos no
  pedidos al esquema) de forma explícita, así que no había nada genuino que
  escalar. No todas las tareas generan una decisión; el batched gate de la
  wave 1 no tuvo preguntas que hacer.
