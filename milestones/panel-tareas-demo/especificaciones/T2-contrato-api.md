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
