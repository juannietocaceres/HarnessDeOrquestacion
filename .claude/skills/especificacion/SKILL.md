---
name: especificacion
description: Convierte una idea o requerimiento en lenguaje natural en un documento de especificación técnica (objetivos, alcance, requisitos funcionales/no funcionales, criterios de aceptación). Úsala antes de implementar cualquier tarea ambigua, de alto impacto, o sin criterios de aceptación claros ya definidos.
---

# Especificación

Convertís una idea informal en un documento corto, verificable y sin relleno.
El objetivo no es "escribir mucho": es dejar por escrito las decisiones que,
si no se toman ahora, se van a tomar por accidente durante la implementación.

## Cuándo conviene saltarla

Si la tarea ya trae criterios de aceptación claros y no hay ambigüedad real
(p. ej. viene de un manifest de `orquestador` con `criterios_aceptacion`
completos), no generes una especificación nueva — sería ceremonia sin valor.
Usala cuando falta ese punto de apoyo.

## Proceso

1. **Entendé el pedido real.** Si el requerimiento es ambiguo en algo que
   cambia el resultado (alcance, audiencia, comportamiento ante error), no
   asumas en silencio: dejalo como pregunta abierta explícita en el
   documento (sección "Preguntas abiertas"), no lo resuelvas adivinando.
2. **Identificá el problema antes que la solución.** Un objetivo se escribe
   en términos del problema que resuelve, no de la implementación ("permitir
   que un usuario recupere su cuenta sin soporte humano", no "agregar un
   botón de reset password").
3. **Trazá el alcance con un borde explícito.** Qué incluye y qué
   deliberadamente no, en la misma sección — el "no incluye" evita que el
   alcance crezca solo durante la implementación.
4. **Los criterios de aceptación son el contrato.** Cada uno debe ser
   verificable por alguien que no escribió el documento: observable,
   binario (se cumple o no), sin adjetivos ("rápido", "intuitivo") sin una
   métrica detrás.

## Plantilla

```markdown
# Especificación: <título>

## Contexto
Por qué existe esta tarea; qué problema real resuelve.

## Objetivo
Qué se logra, en términos del problema — no de la implementación.

## Alcance
**Incluye:** ...
**No incluye:** ...

## Requisitos funcionales
- RF1: ...
- RF2: ...

## Requisitos no funcionales
- Rendimiento, seguridad, compatibilidad, etc. — solo los que de verdad
  aplican a esta tarea, no una lista genérica.

## Criterios de aceptación
- [ ] Condición verificable 1
- [ ] Condición verificable 2

## Preguntas abiertas
- Cualquier ambigüedad no resuelta en este documento, explícita, para que
  alguien la responda antes de implementar.
```

## Dónde vive el resultado

- Si la tarea viene de un milestone del `orquestador`:
  `milestones/<slug>/especificaciones/<id>-<slug-tarea>.md`.
- Si es trabajo suelto (fuera de una wave): `docs/especificaciones/<slug>.md`.

## Salida esperada

Un solo archivo Markdown siguiendo la plantilla de arriba. No generes código
ni empieces la implementación en el mismo paso — la especificación es la
entrada de la siguiente tarea, no parte de ella.
