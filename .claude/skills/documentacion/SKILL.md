---
name: documentacion
description: Genera README, documentación técnica de arquitectura/decisiones, o comentarios inline a partir del código existente. Úsala al cerrar una tarea que agrega una funcionalidad visible, o al cerrar un milestone completo.
---

# Documentación

Generás la documentación que le falta a un proyecto, a partir de lo que el
código ya hace — nunca inventando comportamiento que el código no tiene.

## Primero: identificá qué tipo de documentación hace falta

No todo pedido de "documentar esto" es lo mismo. Antes de escribir, decidí
cuál de estas tres cosas falta:

| Tipo | Para quién | Cuándo generarla |
|---|---|---|
| **README** | Alguien que llega al repo por primera vez | Falta o quedó desactualizado tras cambios visibles (nuevo comando, nueva forma de correr el proyecto, nuevo requisito) |
| **Docs técnicas / decisiones** | Alguien que va a modificar esto después | Una decisión de arquitectura no es obvia leyendo el código (por qué esta librería y no otra, por qué este trade-off) |
| **Comentarios inline** | Alguien leyendo esa función específica | Una línea tiene una razón de ser que el código no comunica por sí solo (un workaround, una invariante no evidente, un caso borde no obvio) |

Si el código ya se explica solo (nombres claros, estructura obvia), **no
generes documentación de relleno** — un README con secciones vacías o
comentarios que repiten el nombre de la función son peor que no tener nada.

## README

Estructura mínima, sin secciones que no apliquen:
- Qué es el proyecto, en una o dos frases.
- Cómo correrlo (setup + comando, no una narrativa).
- Cómo está organizado, si no es evidente por la estructura de carpetas.
- Cómo correr los tests, si el proyecto los tiene.

## Docs técnicas / decisiones

Un documento de decisión (ADR corto) responde: qué se decidió, qué otras
opciones se consideraron, por qué esta y no otra, qué trade-off se aceptó a
cambio. No es una descripción de cómo funciona el código — para eso está el
código mismo y los comentarios inline.

## Comentarios inline

Regla por defecto: **no comentar.** Un comentario solo se justifica cuando
explica un PORQUÉ que no es obvio leyendo el código — una restricción
externa, un workaround de un bug específico, una invariante que no se ve a
simple vista. Si borrar el comentario no confundiría a quien lea el código
después, no lo escribas. Nunca expliques el QUÉ (el código ya lo dice) ni
referencias la tarea/ticket que lo originó (eso rota; va en el commit o el
PR, no en el código).

## Dónde vive el resultado

- README: raíz del proyecto (o del paquete, en un monorepo).
- Docs técnicas: `docs/decisiones/<slug>.md`.
- Comentarios: inline, en el archivo correspondiente — nunca como archivo
  aparte.
