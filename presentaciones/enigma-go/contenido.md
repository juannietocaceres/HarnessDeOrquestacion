# Enigma Go: contenido base verificado

Texto fuente para la landing (`landing/enigma-go/index.html`) y el deck
(`presentaciones/enigma-go-deck.html`). Público: compañeros de clase sin
contexto técnico.

**Cómo leer las marcas**

- **[planeado]**: está en el plan del MVP, pero todavía **no existe** en el
  código.
- **[implementado]**: existe en el repositorio (se indica dónde).
- **[estado real]**: hecho comprobado sobre la situación actual del
  proyecto (por ejemplo, qué no existe todavía).
- Entre paréntesis va la fuente. Las rutas son relativas a la raíz del repo;
  `plan.md` es `milestones/enigma-go/plan.md`.

> Regla para quien reutilice este texto: si copias una frase marcada
> [planeado], escríbela en futuro o como intención ("la app va a…",
> "el plan es…"), nunca como algo que ya funciona.

---

## 1. Titular

**Enigma Go: un juego de misterio nuevo cada vez, armado para tu grupo y tu
tiempo.** [planeado] (plan.md §1)

Variante corta: *"Tú pones el grupo y el tiempo; la app pone el misterio."*
[planeado] (plan.md §1)

---

## 2. Qué es Enigma Go

- Es una **app para el celular** que va a crear juegos de misterio
  personalizados. [planeado] (plan.md §1)
- Tú le dices **cuántos juegan (de 1 a 12)**, **cuánto tiempo tienen (15, 30,
  45, 60 o 90 minutos)**, **dónde se juega** (el modo) y **qué tan difícil**
  lo quieren (fácil, media o difícil). [planeado] (plan.md §1)
- Con eso la app arma un **caso único**: una historia, varios sospechosos,
  pistas y una solución. [planeado] (plan.md §1)
- Guía la partida y, al final, **revela quién fue el culpable** y muestra un
  **ranking**. [planeado] (plan.md §1)
- En el MVP los casos salen de **plantillas, sin IA**, para que funcione sin
  internet y gratis. [planeado] (plan.md §3)
- En el MVP se juega **pasando un solo celular** entre el grupo; jugar cada
  quien en su celular queda fuera. [planeado] (plan.md §3)
- Una condición del proyecto: usar **solo herramientas gratuitas** o con plan
  gratis. [planeado] (plan.md §1)

---

## 3. Cómo se juega, en 5 pasos

El flujo completo del MVP es **configurar → jugar → acusar → revelar →
ranking**. [planeado] (plan.md §3 y §9)

1. **Configurar.** Eliges número de jugadores, tiempo, modo y dificultad; la
   app te sugiere un tipo de juego y puedes cambiarlo. Luego escribes los
   nombres de los jugadores. [planeado] (plan.md §9, pantallas 2 y 3; §5)
2. **Jugar.** La app cuenta la historia inicial. Durante la partida ves un
   temporizador, las pistas se van desbloqueando una a una y tienes la lista
   de sospechosos para tomar notas. [planeado] (plan.md §9, pantallas 4 y 5)
3. **Acusar.** Cada jugador, o el grupo, elige a quién cree culpable. Si el
   tiempo llega a cero, la acusación es obligatoria. [planeado] (plan.md §9,
   pantalla 7; §6)
4. **Revelar.** La app dice "¡Caso resuelto!" o "El culpable escapó" y
   explica la solución. [planeado] (plan.md §9, pantalla 8)
5. **Ranking.** Se reparten puntos: acertar suma, terminar con tiempo de
   sobra da bonus y pedir pistas extra resta. [planeado] (plan.md §9,
   pantalla 8; §10)

---

## 4. Los 3 modos de juego

| Modo | Cómo se juega | Marca |
|---|---|---|
| **App** | Todo pasa dentro del celular. | [planeado] (plan.md §1) |
| **Exterior** | Las pistas son códigos QR impresos que se esconden en un lugar real; al escanear cada QR se desbloquea su pista. | [planeado] (plan.md §1, §3 y §9) |
| **Mixto** | Algunas pistas aparecen en la app y otras se consiguen escaneando QR. | [planeado] (plan.md §11, Fase 3) |

---

## 5. Tipos de juego

El plan define 3 tipos. La app sugiere uno según el número de jugadores y el
modo, y tú puedes cambiarlo. [planeado] (plan.md §5)

| Tipo | Modo | Jugadores | En una frase | Marca |
|---|---|---|---|---|
| **Detective** | App | 1–6 | El grupo investiga junto: lee pistas, interroga sospechosos y acusa. | [planeado] (plan.md §5) |
| **Asesinato con roles** | App o mixto | 4–12 | Cada jugador recibe un personaje secreto y uno de ellos es el culpable; hay rondas de pistas y votación. | [planeado] (plan.md §5) |
| **Búsqueda** | Exterior | 2–12 | El organizador esconde QR en un lugar; cada QR revela una pista y el orden de las pistas lleva a la solución. | [planeado] (plan.md §5) |

Detalle útil para el tipo con roles: el celular se pasa de mano en mano
("pasa el celular a…") y cada quien toca para ver su rol secreto y lo
vuelve a ocultar. [planeado] (plan.md §9, pantalla 4)

---

## 6. Estado real del proyecto

- **Hoy no hay ninguna parte del juego funcionando.** No se puede descargar
  ni jugar. [estado real: nada del juego está implementado en `main`; la
  carpeta `enigma-go/` no existe en `main`] (`git ls-tree main`)
- El desarrollo está **pausado**. [estado real] (`milestones/e2e-skills/milestone.yaml`,
  comentario inicial: "enigma-go está pausado (solo su T1 completada, sin
  mergear)")
- El trabajo está planeado en **7 tareas repartidas en 6 oleadas**, que
  cubren las fases 0 a 3 del plan. [planeado] (`milestones/enigma-go/milestone.yaml`,
  `milestones/enigma-go/estado.yaml`)
- **Solo la primera tarea está hecha**: el *proyecto base* (el esqueleto
  vacío de la app, con sus herramientas instaladas y una pantalla de inicio
  provisional). [implementado, pero **sin integrar a `main`**: vive en una
  rama aparte, commit `e2c6dda`] (`git show --stat e2c6dda`;
  `milestones/enigma-go/milestone.yaml`, T1; `milestones/e2e-skills/milestone.yaml`,
  comentario inicial)
- Las otras 6 tareas están **pendientes**: el motor que arma los casos, las
  plantillas de historias, el generador con su validador, las pantallas del
  modo app, el modo exterior/mixto con QR y el README. [planeado, sin
  empezar] (`milestones/enigma-go/estado.yaml`; `milestones/enigma-go/milestone.yaml`,
  T2–T7)
- La IA generativa (fase 4) y el pulido con versión instalable para Android
  (fase 5) son **opcionales** y quedan fuera de este milestone. [planeado,
  opcional] (`milestones/enigma-go/milestone.yaml`, cabecera; plan.md §13)

Frase lista para usar: *"Enigma Go es, por ahora, un plan detallado y un
proyecto base: el juego todavía no se puede jugar."*

---

## 7. Cierre

**Un misterio distinto en cada partida, para el grupo y el tiempo que
tengas.** Hoy Enigma Go está en fase de plan, con el esqueleto de la app
listo en una rama aparte; lo que viene es construir el motor de casos y las
pantallas para poder jugarlo. (plan.md §1 y §11;
`milestones/enigma-go/milestone.yaml`; `git show --stat e2c6dda`)
