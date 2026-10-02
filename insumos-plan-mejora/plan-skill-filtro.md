# Plan de Desarrollo: Skill "Project Triage & Scoping Router"

## Visión General
Esta skill actuará como el punto de entrada (front-door) para cualquier nueva idea de proyecto. Su objetivo es transformar requerimientos ambiguos o incompletos en un manifiesto estructurado (JSON) que un sistema orquestador pueda leer para inicializar agentes, asignar tareas y definir arquitecturas.

---

## Fase 1: Diseño y Definición de Restricciones (Día 1)
Antes de programar el prompt, necesitamos definir los límites exactos de lo que la skill debe y no debe hacer.

*   **Definir el Catálogo de Agentes:** Listar qué agentes existen en tu sistema (ej. `Frontend_Agent`, `DBA_Agent`, `QA_Agent`). La skill solo podrá sugerir agentes de esta lista.
*   **Definir Taxonomía de Clasificación:** 
    *   *Dominios:* Web, Mobile, Data, DevOps, Scripting.
    *   *Complejidades:* Baja (1 agente), Media (2-3 agentes), Alta (Microservicios).
*   **Regla de Oro:** La skill tiene prohibido escribir código. Su único trabajo es planificar y clasificar.

## Fase 2: Ingeniería del Prompt (Días 2-3)
Construcción del "cerebro" de la skill mediante instrucciones claras para el LLM.

*   **Definición del Rol:** "Eres un Technical Product Manager y Arquitecto de Software Senior..."
*   **Lógica de Clarificación:** Instruir al modelo para que, si el *prompt* del usuario tiene menos de 30 palabras o carece de plataforma/tecnología, responda con máximo 3 preguntas de opción múltiple antes de generar el JSON.
*   **Reglas de Extracción:** Enseñar al modelo a inferir requerimientos no funcionales (seguridad, escalabilidad) basados en el caso de uso del usuario.

## Fase 3: Estructuración del Output (Día 4)
Definir el esquema estricto (JSON Schema) que la skill debe devolver.

*   **Campos Obligatorios:**
    *   `project_name` (String)
    *   `status` (Enum: `requires_clarification`, `ready_for_orchestration`)
    *   `classification` (Object: domain, complexity, scope)
    *   `technical_requirements` (Object: frontend, backend, database)
    *   `required_agents` (Array de Strings)
    *   `orchestration_plan` (Array de Strings)
*   **Formato de Salida:** Configurar la skill para que el output sea *únicamente* el bloque JSON válido, sin texto introductorio ni conclusiones, garantizando que sea *machine-readable*.

## Fase 4: Pruebas de Estrés (Día 5)
Validar el comportamiento de la skill con diferentes tipos de inputs.

*   **Prueba 1 (El usuario vago):** Input: *"Quiero un clon de Twitter"*. 
    *   *Resultado esperado:* La skill cambia el `status` a `requires_clarification` y hace preguntas sobre la escala y el stack preferido.
*   **Prueba 2 (El usuario sobre-detallado):** Input: Un texto de 3 páginas con historias de usuario detalladas.
    *   *Resultado esperado:* La skill sintetiza todo perfectamente en el esquema JSON sin perder el alcance.
*   **Prueba 3 (El proyecto imposible):** Input: *"Quiero una IA consciente de sí misma en HTML"*.
    *   *Resultado esperado:* Manejo de expectativas y ajuste a un plan realista de desarrollo web.

## Fase 5: Integración con el Orquestador (Día 6+)
Conectar la salida de esta skill con el motor que maneja los agentes.

*   **Paso 1 (Parseo):** El orquestador lee la salida de la skill y valida el JSON.
*   **Paso 2 (Reclutamiento):** El orquestador itera sobre el array `required_agents` y levanta las instancias necesarias.
*   **Paso 3 (Asignación):** El orquestador toma el `orchestration_plan`, lo convierte en "tickets" y se los inyecta como contexto a los agentes reclutados.