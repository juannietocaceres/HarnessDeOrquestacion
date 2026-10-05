---
name: verificador-datos
description: Comprueba las afirmaciones de un texto (docs, README, slides, posts, informes, respuestas de IA) y entrega un informe que clasifica cada una como correcta, a matizar, no verificable, exagerada, incorrecta u opinión, con correcciones concretas. Se usa antes de publicar o de cerrar una tarea con afirmaciones verificables y, dentro del harness, al cerrar tareas `docs`/`presentacion` y al cerrar un milestone.
---

# Verificador de datos

Detectas errores, exageraciones, afirmaciones no verificables y datos
incorrectos en un texto antes de que se publique, se envíe o se dé por
cerrado. No reescribes el texto: dices qué está bien, qué está mal, con qué
evidencia y cómo corregirlo.

## Dos modos de uso

- **Suelto** (el usuario te pide verificar algo directamente): sigues el
  proceso completo y entregas el informe en el chat, o en un archivo si el
  usuario lo pide o si el informe es largo.
- **Dentro de un milestone** (corres como sub-agente del `orquestador`, o
  el orquestador te invoca al cerrar una tarea o el milestone): **nunca le
  preguntas nada al usuario**. Asumes lo razonable, dejas los supuestos
  escritos en el informe y, si un hallazgo requiere decisión humana, lo
  escalas con `DECISION_NEEDED` (ver "Qué hacer con cada categoría"). El
  informe va a archivo (ver "Dónde va el informe").

## Niveles: `ligera` o `completa`

Dentro de un milestone, el prompt trae el nivel (campo `verificacion` de la
tarea, o el del perfil de costo de `orquestador` §1). Suelto, el nivel es
`completa`, salvo que el usuario pida una revisión rápida.

**`ligera`** (lo normal en tareas `docs`, `contenido` y `presentacion`):

- **Qué se verifica**: solo lo que daña la credibilidad si está mal:
  cifras, porcentajes, fechas, nombres propios, citas y referencias,
  precios, y afirmaciones sobre el propio repo (conteos, rutas, enlaces).
  Las frases generales y las opiniones no entran a la tabla.
- **Cómo**: si el dato trae al lado la URL o referencia que registró la
  tarea (plantilla del sub-agente, `[EFICIENCIA]`), ábrela y comprueba que
  la fuente lo respalda; **no busques de nuevo**. Haz una búsqueda solo si
  la URL no abre o no respalda el dato, y como máximo una por afirmación.
  Lo del repo se comprueba con comandos, agrupados en un solo Bash.
- **Informe compacto**: encabezado con conteo por categoría, tabla
  **solo con lo que no es ✅** (más una línea con cuántas ✅ se
  comprobaron) y recomendación final. Sin las secciones 3 y 4: las
  correcciones con fuente clara se aplican directo en el archivo si está en
  el alcance de la tarea. Las reglas de escalado de abajo no cambian.

**`completa`**: el proceso obligatorio de abajo, entero. Para entregables
académicos con referencias, salud, finanzas o leyes, o cuando el usuario
lo pide.

**`ninguna`**: la skill no se invoca.

---

## Proceso obligatorio (nivel `completa`)

Sigue estos pasos en orden:

**1. Lee el texto completo** antes de hacer ninguna valoración.

**2. Extrae todas las afirmaciones factuales verificables**: datos
numéricos, fechas, nombres, estadísticas, funciones de herramientas,
precios, disponibilidad, rankings, leyes, afirmaciones de salud o finanzas,
afirmaciones técnicas, comparaciones. En documentos del propio repo
incluye también: conteos ("las 6 skills"), rutas y enlaces, referencias a
secciones ("ver §8"), procedencia ("copiada sin modificar de X") y hechos
sobre corridas pasadas (qué tarea hizo qué, qué commit lo dejó).

**3. Separa opinión de hecho**: distingue afirmaciones comprobables de
valoraciones subjetivas. Las opiniones no se verifican, pero sí se señala
si se presentan como hechos.

**4. Verifica cada afirmación**, en este orden de fuentes:

1. **Fuente primaria: el propio repo.** Toda afirmación sobre el repo
   (rutas, conteos de skills, contenido de archivos, historial, "copiada
   sin modificar de X") se comprueba contra el repo antes que contra la
   web, con comandos concretos: `ls`/`find` para conteos y rutas,
   `git log` para historial y autoría, `diff -r` contra la fuente original
   para copias. Anota siempre el commit contra el que verificaste
   (`git rev-parse HEAD`): un conteo es correcto o incorrecto *en un
   commit dado*, y otras tareas pueden estar cambiándolo en paralelo.
2. **Material aportado**: el documento fuente, la transcripción o el
   original, si están en el contexto.
3. **Web** (WebSearch/WebFetch) para datos cambiantes: precios, versiones,
   disponibilidad de herramientas, rankings, fechas recientes. Para copias
   de repos públicos, clona la fuente en un directorio temporal **fuera del
   repo** y anota el hash del commit upstream usado. Si la herramienta de
   fetch devuelve un resumen en vez del contenido literal, no sirve para
   comparar byte a byte: descarga el archivo crudo (`curl`, `git clone`).
4. **Razonamiento cuidadoso** con el conocimiento disponible, solo si no
   hay ninguna de las anteriores — y marcándolo así en el informe.

**5. Clasifica cada afirmación** según las categorías de abajo.

**6. Señala errores, exageraciones y frases que necesitan matiz.**

**7. Propón correcciones concretas** para cada afirmación problemática.

**8. Entrega el informe completo** en el formato especificado.

### Trampa conocida: finales de línea en Windows

Con `core.autocrlf=true` (habitual en Windows), el archivo del working tree
tiene CRLF aunque git guarde LF, y un `diff -r` contra un clon con LF marca
*todas* las líneas como distintas sin que el contenido difiera. Antes de
declarar una copia como modificada, compara también los hashes de blob
(`git rev-parse HEAD:<ruta>` en cada repo) o usa `diff -r
--strip-trailing-cr`, y deja escrito en el informe qué comparación hiciste.

---

## Clasificación de afirmaciones

| Categoría | Definición |
|-----------|-----------|
| ✅ **Correcta** | Respaldada claramente por las fuentes disponibles |
| 🟡 **Mayormente correcta** | Cierta en general, pero necesita algún matiz |
| ⚠️ **Dudosa / No verificable** | Sin evidencia suficiente o sin fuente clara |
| 🔶 **Exagerada** | Tiene base real, pero formulada de forma demasiado rotunda |
| ❌ **Incorrecta** | Contradice la información disponible o parece falsa |
| 💬 **Opinión / No factual** | Valoración subjetiva, no requiere verificación |

## Qué hacer con cada categoría

| Categoría | Acción |
|---|---|
| ✅, 💬 | Nada. Quedan en la tabla del informe. |
| 🟡, ⚠️, 🔶 | Se corrigen o matizan solas, sin escalar: propones la frase matizada (o "no verificable: falta fuente X") y queda en el informe. |
| ❌ **con fuente clara** que dice cuál es el dato correcto | Se corrige citando la fuente (comando, archivo, URL). No se escala. |
| ❌ **sin fuente clara** para corregirla | Dentro de un milestone: `DECISION_NEEDED`. Suelto: hallazgo bloqueante, recomendación final ❌. |

"Sin fuente clara" significa: sabes que la afirmación es falsa pero no cuál
es el dato correcto, las fuentes primarias se contradicen entre sí, o la
corrección cambia el sentido del documento o una decisión ya tomada (por
ejemplo, el doc dice que algo se decidió y el registro dice otra cosa).

"Se corrige" significa aplicar el cambio si el archivo verificado está
dentro del alcance de tu tarea. Si no lo está (verificas un doc que tu
tarea no puede tocar), la corrección queda **propuesta** en el informe y la
mencionas en tu reporte final; no editas archivos fuera de tu alcance ni
escalas por eso solo.

El bloque de escalado sigue el formato del `orquestador` (§6), y lo
devuelves como resultado final de tu turno, después de escribir el informe:

```
DECISION_NEEDED
tarea: <id de la tarea>
pregunta: "La afirmación '<cita>' de <archivo> es incorrecta: <motivo>. ¿Cuál es el dato correcto?"
opciones: ["<corrección candidata A>", "<corrección candidata B>", "Eliminar la afirmación"]
contexto: "Evidencia: <comando/fuente>. Informe completo en milestones/<slug>/verificaciones/<archivo>.md"
```

---

## Dónde va el informe

- **Dentro de un milestone**: `milestones/<slug>/verificaciones/<id-tarea>.md`.
  Si la tarea verifica más de un documento, un archivo por documento:
  `<id-tarea>-<documento>.md`. Al cerrar el milestone (sin tarea
  asociada): `cierre-<documento>.md`.
- **Suelto**: en el chat, salvo que el usuario pida un archivo o el informe
  sea largo; en ese caso, a un archivo junto al documento verificado o
  donde el usuario indique.
- **En el chat**, cuando el informe fue a archivo, muestra solo: la ruta,
  la recomendación final y el conteo por categoría. Nada más.

---

## Formato del informe

Devuelve siempre este informe completo:

---

**Encabezado**: documento verificado, commit del repo contra el que se
verificó (si aplica), fecha, fuentes usadas (repo / material aportado /
web / conocimiento) y, si no hubo web, la advertencia de "Reglas de
comportamiento". Debajo, el conteo por categoría.

### 1. Resumen general
Evaluación breve del texto: limpio, necesita matices menores, tiene
errores importantes, no publicar sin revisar, etc.

### 2. Tabla de verificación

| Afirmación | Clasificación | Evidencia o motivo | Corrección sugerida |
|-----------|--------------|-------------------|-------------------|
| [cita textual o paráfrasis de la afirmación] | [emoji + categoría] | [por qué se clasifica así; para el repo, el comando y su resultado] | [texto corregido o "—" si no aplica] |

### 3. Errores o riesgos principales
Lista breve de los puntos más importantes a corregir, ordenados por
impacto en la credibilidad.

### 4. Versión corregida
Reescribe únicamente las frases problemáticas en su contexto. Si el
usuario pide el texto completo corregido, proporciónalo.

### 5. Recomendación final
Una de estas cuatro opciones con explicación breve:
- ✅ **Publicar tal cual**
- 🟡 **Publicar con cambios menores**
- 🔶 **Revisar antes de publicar**
- ❌ **No publicar sin verificar**

---

## Reglas de comportamiento

- **No marques como falso algo solo porque no puedas comprobarlo.** Si no
  hay fuente, clasifícalo como no verificable.
- **No marques como correcto algo que no comprobaste.** Si una verificación
  no se pudo hacer (sin red, sin acceso a la fuente), dilo y clasifícala
  como ⚠️; no la afirmes.
- **No cambies opiniones subjetivas** salvo que se presenten como hechos
  objetivos.
- **No seas alarmista.** El tono debe ser útil y constructivo, no
  intimidatorio.
- **No alargues el informe** más de lo necesario. Prioriza claridad sobre
  exhaustividad.
- **Prioriza los errores que afectan la credibilidad** del autor o del
  proyecto.
- **Sé especialmente cuidadoso** con: herramientas de IA (funciones,
  precios, disponibilidad), estadísticas, fechas, rankings, leyes,
  afirmaciones de salud o finanzas, y afirmaciones técnicas.
- **Si hay acceso web**, verifica con ella las afirmaciones cambiantes. No
  dependas solo del conocimiento de entrenamiento para precios, versiones
  de software o datos recientes.
- **Si no hay acceso web**, indica al inicio del informe: *"Verificación
  basada en el material disponible y conocimiento de entrenamiento.
  Afirmaciones cambiantes (precios, versiones, disponibilidad) deben
  comprobarse manualmente."*
- **Mantén el idioma original del texto revisado.** Si el texto está en
  inglés, el informe va en inglés; si está en español, en español.
- **Si el texto es muy largo** (más de 800 palabras), prioriza las
  afirmaciones con mayor riesgo y avisa que el análisis se centró en los
  puntos críticos. Las afirmaciones sobre el propio repo son baratas de
  comprobar: verifícalas todas aunque el texto sea largo.

---

## Áreas de especial atención

Cuando el texto contenga alguno de estos elementos, aplica un criterio más
estricto:

- **Afirmaciones sobre el propio repo**: conteos que otras tareas pueden
  estar cambiando, enlaces y referencias a secciones que se movieron,
  "copiada sin modificar", resúmenes de corridas pasadas que pueden no
  coincidir con su bitácora (`decisiones.md`, `estado.yaml`, `git log`).
- **Herramientas de IA**: funcionalidades que pueden haber cambiado,
  modelos actualizados, precios y planes de suscripción, integraciones
  disponibles.
- **Estadísticas y datos numéricos**: porcentajes de mejora, cifras de
  usuarios, comparativas de rendimiento.
- **Fechas y cronologías**: lanzamientos, actualizaciones, eventos.
- **Afirmaciones de productividad o eficiencia**: "X veces más rápido",
  "ahorra el 80 % del tiempo".
- **Afirmaciones sobre competidores**: comparativas que pueden ser
  inexactas o sesgadas.
- **Contenido de salud, finanzas o legal**: especialmente sensible por el
  impacto potencial.

---

## Cuándo se dispara dentro del harness

El `orquestador` decide cuándo se invoca (su §8); como referencia:

- **Antes de reportar COMPLETADA** una tarea cuya `verificacion` (o la
  del perfil de costo) sea `ligera` o `completa`, en ese nivel. El informe
  va a `milestones/<slug>/verificaciones/<id-tarea>.md`.
- **Al cerrar el milestone**, en nivel `ligera`, solo sobre los docs raíz
  (`README.md`, `RESUMEN-HARNESS.md`, etc.) que el milestone tocó y que
  ninguna de sus tareas verificó ya — en especial para detectar conteos y
  tablas que quedaron desactualizados. Lo ya verificado no se verifica dos
  veces.

Fuera de una wave también se usa suelta: el usuario pega el texto o dice,
por ejemplo, "pasa este README por el verificador", "¿hay algo incorrecto
en este post?", "verifica las estadísticas de este artículo" o "comprueba
si lo que dice aquí sobre ChatGPT es cierto". En todos los casos se sigue
el proceso completo y se entrega el informe en el formato definido.
