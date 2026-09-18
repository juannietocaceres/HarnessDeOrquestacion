---
name: revision-codigo
description: Checklist y proceso para revisar código antes de cerrar una tarea o integrar una rama — calidad, seguridad básica, legibilidad y convenciones del proyecto. Se ejecuta como autorrevisión al final de cada tarea, dentro del gate de aprobación del orquestador, antes de mergear.
---

# Revisión de código

Revisás el diff de una tarea ya "terminada" antes de que cuente como
COMPLETADA. El objetivo es separar lo que se puede corregir solo (hacelo y
seguí) de lo que requiere una decisión humana (no lo decidas solo: repórtalo
como un `DECISION_NEEDED` si estás corriendo dentro de una wave del
orquestador, o como un hallazgo bloqueante si es revisión suelta).

## Checklist

**Corrección**
- ¿El diff hace lo que pedían los criterios de aceptación — ni menos, ni de
  más? Cambios fuera del alcance de la tarea son una señal, no un bonus.
- ¿Hay casos borde obvios del propio enunciado sin cubrir (vacío, nulo,
  cero, el otro lado de un `if`)?

**Seguridad básica**
- ¿Alguna entrada externa (input de usuario, respuesta de API, argumento de
  CLI) se usa sin validar en una consulta, comando, ruta de archivo o HTML
  renderizado? (inyección SQL/comando, XSS, path traversal)
- ¿Quedó algún secreto, token o credencial hardcodeado?
- ¿Alguna dependencia nueva se agregó sin razón clara?

**Legibilidad**
- ¿Los nombres dicen qué es la cosa, no cómo llegamos a necesitarla?
- ¿Hay comentarios que explican el QUÉ (redundante) en vez del PORQUÉ (solo
  cuando no es obvio)?
- ¿Se podría borrar código sin que nadie lo note? Bórralo.

**Convenciones del proyecto**
- ¿Sigue el estilo, estructura de carpetas y patrones ya existentes en el
  repo, en vez de introducir uno nuevo para esta sola tarea?

**Alcance**
- ¿El diff toca solo lo que la tarea necesitaba? Un archivo "ya que estaba"
  tocado sin relación con la tarea es una bandera roja para revertir esa
  parte del cambio.

## Cómo se resuelve cada hallazgo

- **Corregible sin ambigüedad** (nombre confuso, comentario innecesario,
  falta un `null` check obvio): corregilo vos mismo y seguí — no hace falta
  interrumpir a nadie por esto.
- **Bloqueante con trade-offs reales** (una elección de seguridad con
  impacto en UX, un caso borde donde no está claro cuál es el comportamiento
  correcto, algo que cambia el contrato de la tarea): no lo resuelvas
  adivinando. Si estás dentro de una tarea orquestada, devolvé un
  `DECISION_NEEDED` (ver SKILL.md de `orquestador`, §6) en vez de mergear
  igual.

## Cuándo se ejecuta

Siempre como el último paso antes de reportar una tarea como terminada —
nunca después de mergear. Si encontrás algo bloqueante ya con el merge
hecho, es tarde: por eso va antes.
