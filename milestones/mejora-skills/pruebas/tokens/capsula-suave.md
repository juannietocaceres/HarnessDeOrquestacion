Spec T2 (milestones/panel-tareas-demo/especificaciones/T2-contrato-api.md):
- Por qué: manifest trajo T2 sin `criterios_aceptacion`; T3, T4, T5 (UI) se construyen *contra este contrato*, no contra código → ambigüedad aquí se propaga a la wave siguiente.
- Objetivo: cliente (UI del panel) crea y consulta tareas de forma predecible, sin conocer el almacenamiento; forma de datos = schema/tareas.md (T1).
- Incluye: `POST /tareas` (crear); `GET /tareas` (listar todas); validación del payload de creación contra el esquema de T1; ≥1 caso de error de validación documentado.
- No incluye: actualizar (`PATCH`/`PUT`) ni borrar (`DELETE`); Autenticación/autorización; paginación, filtros u ordenamiento del listado (extensión futura).
- RF1: `POST /tareas` recibe `{ "titulo": string }` (requerido). Servidor asigna `id` (UUID v4), `estado` inicial (`"pendiente"`) y `fecha_creacion` (ISO 8601 UTC, momento de creación); el cliente nunca los envía. Responde `201 Created` con el objeto completo.
- RF2: `GET /tareas` → `200 OK` con array de tareas, cada una con la forma exacta del esquema de T1.
- RF3: `titulo` falta o es cadena vacía → `POST /tareas` responde `400 Bad Request` identificando el campo inválido; nunca crea la tarea parcialmente.
- RNF: timestamps UTC ISO 8601 (heredado de T1, consistencia obligatoria esquema/contrato). Sin motor de persistencia asumido: implementable en memoria (demo) o con BD real sin cambiar la forma pública.
- Criterios de aceptación de la spec (literales):
  - [ ] `POST /tareas` documentado con request y response de ejemplo en JSON.
  - [ ] `GET /tareas` documentado con response de ejemplo en JSON (array).
  - [ ] El caso de error de validación (`titulo` vacío/faltante) documentado
        con código de estado y payload de respuesta.
  - [ ] Explícito que `id`, `estado` y `fecha_creacion` los asigna siempre el
        servidor — nunca el cliente.
- Pregunta abierta: ¿paginación? Fuera de alcance (demo, volumen bajo); primera extensión a evaluar si crece; no bloquea T2.

Esquema T1 (schema/tareas.md) — base de T2 y de T3, T4, T5. Campos, todos requeridos:
- `id`: string; único, no vacío; recomendado UUID v4.
- `titulo`: string; no vacío (mín. 1 carácter sin contar espacios); máx. 200 caracteres.
- `estado`: enum cerrado, exactamente `pendiente` (creada, sin empezar) | `en_curso` (en trabajo) | `hecha` (completada); sin variantes, mayúsculas ni sinónimos; otro valor = inválido.
- `fecha_creacion`: string ISO 8601 UTC (`YYYY-MM-DDThh:mm:ssZ`); la asigna el sistema al crear; inmutable.
- Ejemplos válidos:
  `{"id":"550e8400-e29b-41d4-a716-446655440000","titulo":"Revisar informe de gastos de septiembre","estado":"pendiente","fecha_creacion":"2026-09-17T14:30:00Z"}`
  `{"id":"b3f1c2d4-9a3e-4f2b-8c1d-2e5f6a7b8c9d","titulo":"Actualizar dependencias del proyecto","estado":"en_curso","fecha_creacion":"2026-09-15T09:00:00Z"}`
  `{"id":"7c9e6679-7425-40de-944b-e07fc1f90ae7","titulo":"Preparar demo para la clase","estado":"hecha","fecha_creacion":"2026-09-10T18:45:00Z"}`
- Alcance: solo esos 4 campos; nada extra (descripción, prioridad, responsable, vencimiento, etiquetas, fecha de actualización). Ampliarlo se decide en la tarea que lo necesite.

Manifest (milestones/panel-tareas-demo/milestone.yaml), cap_concurrencia: 2:
- T1 backend, sin deps: esquema en schema/tareas.md.
- T2 backend, depende_de [T1]: contrato REST crear/listar basado en T1; `criterios_aceptacion: []` (vacío a propósito → /especificacion antes de implementar, ver §8 de orquestador/SKILL.md).
- T3 frontend [T2]: ui/lista-tareas.html, HTML/CSS/JS sin build step, lista ≥3 tareas de ejemplo con la forma de datos de T2, estado distinguible, principios frontend-design.
- T4 frontend [T2]: ui/nueva-tarea.html, formulario acorde al payload de `POST /tareas` de T2, con los campos requeridos por el contrato.
- T5 frontend [T2]: ui/badge-pendientes.html, badge/contador de tareas pendientes (número + etiqueta 'pendientes').

Decisiones previas (milestones/panel-tareas-demo/decisiones.md): Wave 1 / T1 sin decisiones; no se agregaron campos no pedidos al esquema.
