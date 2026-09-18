---
name: testing
description: Genera casos de prueba y estrategia de testing adaptada al tipo de proyecto (web, backend/API, CLI, datos, mobile). Úsala al implementar cualquier lógica con comportamiento verificable.
---

# Testing

Generás pruebas a partir de comportamiento verificable, no cobertura por
cobertura. Cada caso de prueba tiene que trazar a algo concreto: un criterio
de aceptación, un caso borde real, o un bug que ya pasó.

## De dónde salen los casos

1. **Los criterios de aceptación de la tarea** (si vienen de `especificacion`
   o de un manifest de `orquestador`) son la primera fuente — cada uno debe
   tener al menos un caso que lo verifique.
2. **Los casos borde del propio dominio**: vacío, nulo/None, cero, negativo,
   el valor más grande permitido, el límite exacto de una condición (`<` vs
   `<=`), la primera y la última iteración de un loop.
3. **Los caminos de error**, no solo el camino feliz: qué pasa cuando la
   dependencia externa falla, el input no valida, el permiso no está.

No dupliques el mismo caso con distintos nombres, y no generes un test que
solo repite la implementación en otras palabras (eso no detecta regresiones,
solo se rompe junto con el código).

## Estrategia según el tipo de proyecto

| Tipo | Foco principal | Qué NO hacer |
|---|---|---|
| **Web frontend** | Tests de componente (render + interacción del usuario) sobre lo esencial; e2e solo para el flujo crítico completo | No testear detalles de implementación (estado interno, nombres de clases CSS) |
| **Backend / API** | Tests de integración contra una dependencia real (DB de test, etc.) para el camino de datos; unitarios para lógica de negocio pura | No mockear la dependencia principal solo para que el test corra más rápido si eso puede ocultar un bug real de integración |
| **CLI** | Invocar el comando real con distintos argumentos/flags y verificar salida + código de salida | No testear solo el "happy path" de parseo de argumentos |
| **Datos / pipelines** | Property-based o basado en fixtures: invariantes que deben sostenerse pase lo que pase (esquema de salida, no perder filas sin razón, idempotencia si aplica) | No testear solo con el dataset "feliz"; probar con datos sucios/faltantes |
| **Mobile** | Tests de lógica de negocio y de componente aislados de la plataforma; e2e solo para flujos críticos (login, compra, etc.) | No depender de un dispositivo/emulador específico para lógica que no lo necesita |

## Qué falta para poder generar los tests

Si la tarea no trae criterios de aceptación claros y el comportamiento
esperado es ambiguo, no inventes el comportamiento para poder testearlo:
señalalo (como `DECISION_NEEDED` si estás dentro de una wave del
orquestador) o remití primero a `especificacion`.

## Dónde vive el resultado

Junto al código que prueban, siguiendo la convención ya existente en el
proyecto destino (carpeta `tests/`, sufijo `.test.`, etc.) — no introduzcas
una convención nueva si el proyecto ya tiene una.
