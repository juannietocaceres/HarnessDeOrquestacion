# Guion de presentación — Harness de orquestación IA

Guion hablado para acompañar el deck (10 slides). Pensado para ~8 minutos de
exposición + preguntas. Los tiempos son orientativos — ajustalos a tu ritmo,
pero tratá de no quedarte pegado en ninguna slide más de un minuto largo: el
deck está armado para que la metáfora de las olas haga el trabajo pesado de
explicar, no vos leyendo texto.

**Tono**: conversacional, como si le estuvieras explicando la idea a un
compañero, no leyendo un informe. Usá las pausas — después de una pregunta
retórica, dejá un segundo antes de responderla vos mismo.

---

## 1. Portada — *"Harness de orquestación IA"* (~30 seg)

> Buenas. Les vengo a mostrar un proyecto que armé para la electiva: un
> sistema para coordinar el trabajo cuando le delegás varias tareas a una
> inteligencia artificial al mismo tiempo. Le puse "harness de
> orquestación", que suena más complicado de lo que es — la idea central se
> resume en una palabra: **olas**. En un rato van a entender exactamente
> por qué.

**Nota**: no te detengas en el diagramita de la derecha — es un adelanto
visual de la slide 3, no hace falta explicarlo todavía.

---

## 2. El problema (~45 seg)

> Arranquemos por el problema. Hoy, cuando le pedís algo a un asistente de
> IA, lo normal es hacerlo tarea por tarea: le pedís algo, esperás, aprobás,
> le pedís lo siguiente. Eso tiene tres problemas grandes.
>
> Primero, **fricción**: te interrumpe todo el tiempo para que apruebes
> cada paso chiquito.
>
> Segundo, **colisión**: si le pedís varias cosas en paralelo para ir más
> rápido, esas tareas terminan pisándose — tocando los mismos archivos.
>
> Y tercero, trabajás **a ciegas**: no hay un momento claro donde decís
> "acá freno y reviso todo junto" — está todo disperso.
>
> Este sistema ataca las tres cosas a la vez, y arranca de una idea bastante
> simple.

**Transición**: "Y esa idea es la que sigue."

---

## 3. La idea central: como las olas (~70 seg — la slide más importante)

> Fíjense en cómo llegan las olas a la orilla: no llega toda el agua junta
> de una sola vez, pero tampoco llega gota por gota. Llega **en tandas**.
>
> Este sistema organiza el trabajo exactamente así. Agrupo todas las tareas
> que tengo que hacer, mapeo qué depende de qué, y las voy soltando en
> tandas: las que no necesitan esperar nada arrancan juntas, en paralelo. La
> tanda siguiente no arranca hasta que la anterior terminó del todo — así
> siempre sé en qué momento estoy parado.
>
> Y para que esto no se desborde — para que no intente hacer diez cosas a
> la vez y se vuelva un quilombo — hay un límite de cuántas tareas pueden
> avanzar juntas. Miren la tercera tanda: tiene tres tareas listas para
> arrancar, pero el límite acá es dos. Entonces, en vez de esperar a que las
> tres terminen para seguir, arrancan dos, y en cuanto una libera lugar,
> entra la tercera.

**Nota**: esta es LA slide. Si en algún momento sentís que perdiste al
público, volvé mentalmente a "como las olas" — es el ancla de todo lo que
sigue.

---

## 4. Seis ayudantes especializados (~40 seg)

> Para que esto funcione de verdad, no alcanza con solo ordenar el trabajo
> — cada tarea, cuando le toca su turno, tiene que saber hacer bien su
> trabajo. Por eso el sistema tiene seis ayudantes especializados: uno arma
> un plan claro antes de programar, cuando la idea todavía viene medio
> vaga. Otro se encarga de que el diseño visual sea deliberado, no
> genérico. Otro revisa el código como lo haría un compañero, antes de
> darlo por bueno. Otro escribe la documentación. Otro prueba que todo
> funcione, incluso en los casos raros. Y arriba de todos, el que coordina:
> el orquestador, que decide cuándo entra cada uno.

**Tip**: no leas las seis tarjetas una por una en voz alta — la gente ya
las está leyendo en pantalla mientras hablás. Nombralas rápido y seguí.

---

## 5. Así se mueve una tanda, paso a paso (~55 seg)

> ¿Y cómo se ve esto en la práctica? Primero, antes de arrancar cualquier
> tanda, se revisa que el plan esté completo — nada de sorpresas a mitad de
> camino. Después, varias tareas se ponen a trabajar en equipo, en
> paralelo, respetando ese límite del que hablamos. Cada una, al terminar,
> puede pasar dos cosas: o terminó bien y sigue, o se topó con algo que no
> le correspondía decidir sola — y ahí, en vez de adivinar, frena y anota
> la pregunta.
>
> Y acá está lo importante: en vez de venirme a interrumpir cada vez que
> una tarea tiene una duda, el sistema **junta todas esas dudas de toda la
> tanda** y me las trae todas juntas, de una sola vez. Yo respondo, cada
> pregunta vuelve exactamente a la tarea que la generó, y recién ahí se
> suma el trabajo y arranca la tanda siguiente.

---

## 6. La regla de oro (~45 seg)

> Y acá está la regla que más me importa de todo el sistema: mientras haya
> una sola pregunta sin responder, no avanza nada. Nada de límite de
> tiempo, nada de "si no contesta en cinco minutos seguimos igual", nada de
> asumir que el silencio es un sí.
>
> ¿Por qué tan estricto? Porque lo que llega hasta acá ya pasó el filtro de
> "esto lo puede resolver solo el sistema" — lo que queda son,
> literalmente, las decisiones que de verdad necesitan que una persona
> responda. Si el sistema adivinara ahí, no estaría ahorrando tiempo:
> estaría tomando una decisión importante sin que nadie se haga cargo de
> ella.

**Nota**: dejá un segundo de silencio después de leer la frase grande en
naranja de la slide. Es la línea más citable de toda la charla.

---

## 7. El ejemplo real (~55 seg)

> Todo esto que les conté no lo simulé para la presentación — lo corrí de
> verdad. Armé un mini-proyecto ficticio, un panel para administrar tareas,
> con cinco tareas conectadas por dependencias reales: primero se define
> cómo se guardan los datos, después el contrato de la API que los expone,
> y recién ahí — porque las tres dependen de ese contrato — se construyen
> en paralelo la lista, el formulario para crear tareas nuevas, y un
> contador de pendientes.
>
> Como esas tres últimas quedan listas al mismo tiempo pero el límite es de
> a dos, esa tercera tanda se corrió en dos turnos — exactamente como
> expliqué antes, pero con agentes de IA reales escribiendo archivos
> reales, no una animación.

---

## 8. Dos tareas, dos dudas, una sola consulta (~60 seg — el momento fuerte de la demo)

> Y en esa tercera tanda pasó justo lo que quería mostrarles. Dos de esas
> tareas, trabajando al mismo tiempo, se toparon cada una con algo que no
> podían decidir solas: una, si la lista de tareas debía tener un filtro
> por estado o quedarse simple; la otra, si el formulario debía validar el
> título ahí mismo en la pantalla, o confiar en lo que respondiera el
> servidor.
>
> Ninguna de las dos me interrumpió por separado. Las dos preguntas me
> llegaron **juntas**, en una sola consulta. Respondí las dos de una — que
> sí al filtro, y que confiara solo en el servidor — y cada respuesta
> volvió exactamente a la tarea que la había generado. Ninguna de las dos
> vio lo que había decidido la otra.

**Tip**: si el público parece técnico, este es el momento para mencionar
que las dos tareas corrieron en paralelo de verdad (subagentes distintos),
no una simulación secuencial disfrazada.

---

## 9. Esto es lo que quedó, de verdad (~35 seg)

> ¿Y qué quedó de todo esto? Las cinco tareas terminadas, corridas en tres
> tandas reales, con solo dos decisiones que de verdad necesitaron que yo
> interviniera — el resto el sistema lo resolvió solo. Once pasos guardados
> en el historial, uno por cada avance. Y algo que me gustó particularmente:
> los tres componentes de pantalla que se generaron en paralelo tienen tres
> identidades visuales completamente distintas — ninguno copió al otro,
> porque cada uno pensó su diseño desde cero.

---

## 10. Dos lecciones que no estaban en el plan (~55 seg — cierre)

> Para cerrar, dos cosas que no tenía planeadas y que aprendí en el camino.
>
> La primera: la forma exacta en que le escribís las instrucciones a la IA
> decide si una duda real se convierte en una pregunta para vos, o si la IA
> la resuelve calladita por su cuenta. Un matiz de redacción cambia todo el
> comportamiento.
>
> Y la segunda: el entorno técnico importa tanto como el diseño. Tuve un
> problema puntual porque arranqué la sesión antes de terminar de
> configurar el repositorio, y eso bloqueó una función. La idea estaba bien
> diseñada — lo que falló fue el orden de los pasos.
>
> Todo esto quedó anotado por escrito en el propio proyecto, con el porqué
> de cada decisión. Gracias, quedo abierto a preguntas.

---

## Preguntas probables, y cómo responderlas

**"¿Esto funciona para cualquier tipo de proyecto, o solo para apps web?"**
> El mecanismo (tandas, límite, consulta conjunta) es genérico. Lo que
> cambia según el proyecto es qué produce cada ayudante — por ejemplo,
> "testing" genera property tests para un pipeline de datos y tests de
> componente para una interfaz — pero el orden y las reglas son las mismas.

**"¿Qué pasa si dos tareas SÍ necesitan tocar el mismo archivo?"**
> Por diseño, las tareas de una misma tanda son independientes entre sí. Si
> dos tareas necesitan tocar lo mismo, hay una dependencia real que no se
> declaró — deberían quedar en tandas distintas, no en la misma.

**"¿Por qué separar en seis ayudantes en vez de que la IA resuelva todo junta?"**
> Cada uno encapsula un proceso específico y repetible — por ejemplo, la
> revisión de código tiene su propio checklist de seguridad. Separarlos
> hace que ese proceso sea consistente cada vez, en vez de depender de que
> la IA "se acuerde" de todo junto en una sola pasada.

**"¿Y si nunca respondés la pregunta?"**
> El sistema espera indefinidamente. Es la regla de oro — ni timeout, ni
> respuesta por defecto.

**"¿Lo probaste en un proyecto real, o es solo para la demo?"**
> El ejemplo de hoy es ficticio, pero el mecanismo es exactamente el mismo
> que usaría en un proyecto real — no hay nada especial del ejemplo que no
> se aplique a un caso real.
