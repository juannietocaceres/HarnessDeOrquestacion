---
name: optimizador-tokens
description: Compacta contexto de referencia largo sin perder entidades críticas, como cápsula para el prompt de un sub-agente o como contexto-compacto.md al cerrar una wave o un milestone, y mide el ahorro con scripts. Se usa cuando el contexto que va a leer otra IA supera el umbral o al empaquetar una sesión para reanudarla.
---

# Optimizador de tokens

Reduces el contexto que va a leer otra IA sin cambiar lo que dice. El foco es
la **densidad**: el mismo contenido en menos tokens, con las entidades
críticas intactas y el ahorro medido por script, nunca estimado a ojo.

## Frontera con `optimizador-prompts`

Las dos skills trabajan sobre texto que va a leer una IA, pero optimizan
cosas distintas y no se pisan:

| | `optimizador-prompts` | `optimizador-tokens` (esta) |
|---|---|---|
| Optimiza | **Claridad** (humano → IA) | **Densidad** (IA → IA) |
| Entrada típica | Una idea, un pedido mal escrito, una tarea del manifest | Contexto de referencia ya claro pero largo (resultados de waves, decisiones, docs) |
| Puede alargar el texto | Sí, si falta información (objetivo, criterios, formato) | No: solo poda, nunca agrega información |
| Salida | Un prompt estructurado | Un bloque compacto (`[CONTEXTO]` del sub-agente o `contexto-compacto.md`) |

Regla de convivencia: `optimizador-prompts` arma la estructura del prompt
([PLANTILLA-SUBAGENTE.md](../optimizador-prompts/PLANTILLA-SUBAGENTE.md));
esta skill solo llena el bloque `[CONTEXTO]` cuando el contexto de referencia
supera el umbral. Esta skill **no toca** `[TAREA]`, `[OBJETIVO]`,
`[CRITERIOS DE ACEPTACIÓN]`, `[RESTRICCIONES]`, `[PROTOCOLO DE DECISIÓN]` ni
`[ENTREGA]`, y no reescribe criterios, objetivos ni restricciones aunque
aparezcan dentro del contexto: van literales.

## Modo de ejecución: interactivo o no interactivo

- **Interactivo** (invocada suelta por el usuario): si no está claro qué
  contexto hay que compactar o para quién, puedes preguntar (máximo 2).
- **No interactivo** (dentro del orquestador o de un sub-agente): **no
  preguntes**. Asume lo razonable y lista los supuestos junto al JSON de
  salida. Si para compactar tendrías que decidir algo de alto impacto (p. ej.
  qué decisión vigente reemplaza a otra cuando se contradicen), no lo
  decidas: devuelve un bloque `DECISION_NEEDED` con el formato de
  `orquestador` §6.

## Cuándo comprimir (y cuándo no)

Comprimir también gasta tokens: el modelo lee el original y escribe la
cápsula (tokens de salida). Por eso:

1. Mide el contexto crudo con `scripts/medir_tokens.py`.
2. Si queda **por debajo de ~4.000 tokens estimados**, no comprimas: pasa el
   contexto tal cual (con rutas en vez de código). El umbral se subió desde
   ~2.000 en el gate de la wave 2 de `mejora-skills`: en la prueba de
   retención sobre T2 (contexto de 2.210 tokens), el sub-agente gastó en total
   solo ~5% menos, poco frente al costo de escribir la cápsula (ver
   `milestones/mejora-skills/pruebas/tokens.md`).
3. Si queda por encima, aplica el modo que corresponda (abajo).

El número de tokens siempre sale del script. No escribas "ahorro ~90%" sin
haber corrido `medir_tokens.py --comparar`.

## Qué nunca se toca

Lista dura. Si una regla de poda choca con esta lista, gana la lista.

- **Código que el sub-agente va a editar**: no se copia ni se minifica; se
  pasa la ruta.
- **`criterios_aceptacion`, `verificacion_manual` y respuestas del batched
  gate**: siempre literales, carácter por carácter.
- **IDs de tarea, rutas, URLs, versiones, puertos, hashes, UUIDs, nombres de
  ramas** y todo valor exacto entre `comillas invertidas` (enums, nombres de
  campo, códigos de estado, comandos).
- **Credenciales**: ni se comprimen ni se copian. Si aparecen en el contexto
  (claves de API, tokens, contraseñas, llaves privadas), se omiten y se avisa
  en la salida ("credencial omitida en <fuente>"). `verificar_entidades.py`
  falla con código 3 si la cápsula contiene algo con forma de credencial.

## Niveles

| Nivel | Qué hace | Cuándo |
|---|---|---|
| `suave` | Quita relleno (saludos, confirmaciones, repeticiones, frases de transición), pasa prosa a viñetas o `clave: valor`, minifica JSON/YAML de ejemplo a una línea, fusiona secciones que repiten lo mismo. **No elimina hechos**: cada requisito, regla, ejemplo y entidad del original sigue estando, y el porqué se conserva en una línea cuando condiciona una decisión. | Por defecto para prompts de sub-agentes (modo `capsula`). |
| `medio` | Lo de `suave` más: consolida el historial en el estado actual (decisiones reemplazadas, intentos descartados y pasos ya cerrados se reducen a su resultado), deja un solo ejemplo cuando hay varios equivalentes. Cada entidad que se pierde a propósito se declara con `--ignorar` al verificar. | Por defecto para empaquetar sesión (modo `empaquetar`). |
| `agresivo` | Formato `Clave:[valores]|Clave:valor` sin prosa. | Solo con una prueba de retención aprobada para ese tipo de tarea. |

## Modo `capsula`

El orquestador va a lanzar un sub-agente y el contexto de referencia
(resultados de waves previas, decisiones, docs relacionados) supera el umbral.

1. Junta el contexto crudo en un archivo temporal (en el scratchpad, no en el
   repo), con un encabezado por fuente que diga su ruta.
2. `python scripts/medir_tokens.py <crudo>` → si está bajo el umbral, termina
   aquí y pasa el crudo.
3. Escribe la cápsula en nivel `suave` en otro archivo temporal: misma
   información, una sección por fuente (encabezado con la ruta), reglas de
   poda de abajo.
4. `python scripts/verificar_entidades.py <crudo> <capsula>`. Si sale con
   código ≠ 0, corrige la cápsula (agrega lo que falta, quita la credencial) y
   repite. No entregues una cápsula que no pasó.
5. `python scripts/medir_tokens.py --comparar <crudo> <capsula>` → métricas.
6. Devuelve el JSON de salida. El `payload` va tal cual al bloque
   `[CONTEXTO]` del prompt, sin reescribirlo.

## Modo `empaquetar`

Cierre de cada wave y del milestone. Deja un resumen que una sesión
reanudada lee **primero**, antes que `estado.yaml` y `decisiones.md`.

- **Entrada**: `milestones/<slug>/estado.yaml`, `decisiones.md`,
  `bloqueos-externos.md` y los reportes de las tareas de la wave.
- **Salida**: `milestones/<slug>/contexto-compacto.md`, nivel `medio`, con
  esta forma:

```markdown
# Contexto compacto — <slug>
Actualizado: <fecha> · cierre de wave <n> · fuentes: estado.yaml, decisiones.md, bloqueos-externos.md

## Estado
wave_actual: <n> | siguiente: <n+1> [<ids>] | cap: <n>
<id>: <ESTADO> · commit <hash> · <entregable principal (ruta)>

## Decisiones vigentes (literales del gate)
- <id> — <pregunta corta> → **<respuesta literal>**

## Pendiente
- <decisiones abiertas, bloqueos externos, hallazgos que pasan a otra tarea>

## Rutas clave
- <ruta>: <qué es>
```

- Verifica contra la concatenación de las fuentes:
  `verificar_entidades.py <fuentes-concatenadas> contexto-compacto.md`
  (con `--ignorar` para lo que el nivel `medio` descarta a propósito, p. ej.
  hashes de intentos superados). Las métricas van en una línea HTML al final
  del archivo (`<!-- metricas: ... -->`), no en el cuerpo.
- `contexto-compacto.md` es un índice para retomar, no reemplaza las fuentes:
  ante cualquier duda, manda `estado.yaml` / `decisiones.md`.

## Reglas de poda

- **Minificación estructural**: JSON, YAML y HTML de *ejemplo* (no el código
  a editar) a una línea, sin espacios sobrantes.
- **Prosa a clave-valor**: "El cliente prefiere modo oscuro por defecto y que
  cargue rápido" → `UI: modo_oscuro, carga_rapida`. Solo cuando la relación es
  inequívoca; si la frase tiene matices (condiciones, excepciones), se queda
  como viñeta corta.
- **Poda de historial**: fuera saludos, disculpas, confirmaciones ("Entendido,
  trabajo en ello") y turnos superados; varios turnos se consolidan en el
  estado actual.
- **Por tipo de contenido**: código o configuración → no se resume (ruta, o
  minificación sin cambiar la sintaxis si es un ejemplo); lenguaje natural →
  resumen extractivo (se reutilizan las frases del original, no se
  parafrasean los valores).
- **Sin inventar**: la cápsula no agrega datos, supuestos ni conclusiones
  que no estén en el original.

## Formato de salida

```json
{
  "modo": "capsula",
  "nivel": "suave",
  "payload": "<la cápsula>",
  "metricas": { "tokens_original": 2210, "tokens_final": 1024, "ahorro": "54%", "metodo": "estimado" },
  "entidades_preservadas": true,
  "avisos": []
}
```

`metricas` se copia de la salida de `medir_tokens.py --comparar`;
`entidades_preservadas` de la de `verificar_entidades.py`; `avisos` lista
credenciales omitidas y entidades ignoradas a propósito. En modo
`empaquetar`, `payload` es la ruta de `contexto-compacto.md` (regla de
salidas a archivo: en el chat solo va el resumen y la ruta).

## Scripts

Solo biblioteca estándar de Python 3. Se corren desde la raíz del repo.

| Script | Qué hace | Salida |
|---|---|---|
| `scripts/medir_tokens.py <archivos>` | Caracteres y tokens estimados (caracteres // 4) | JSON |
| `scripts/medir_tokens.py --comparar <orig> <final>` | Métricas para el JSON de salida | JSON (`metricas`) |
| `scripts/medir_tokens.py --descriptions .claude/skills` | Costo fijo de la lista de skills: `name` + `description` de cada skill que el modelo ve, con desglose por origen (propias, Emil, otras vendorizadas) | JSON |
| `scripts/verificar_entidades.py <orig> <capsula>` | Extrae entidades protegidas del original y comprueba que estén en la cápsula | JSON; código 0 ok, 1 falta una entidad, 2 error de uso, 3 credencial en la cápsula |
| `scripts/test_scripts.py` | Pruebas de los dos scripts | `python -m unittest discover -s .claude/skills/optimizador-tokens/scripts` |

**Conteo oficial (opcional)**: `medir_tokens.py --api` usa
`POST /v1/messages/count_tokens` si existe `ANTHROPIC_API_KEY` y marca
`"metodo": "api"`; si no existe o la llamada falla, vuelve a `"estimado"` y
lo avisa en el JSON (nunca mezcla métodos en una corrida). Según la
documentación vigente el endpoint es gratuito, tiene límite de requests por
minuto según el tier, y su resultado también es una estimación; además
cuenta con el tokenizador del modelo que se le pasa (`--modelo`, por defecto
`claude-opus-5-5`), y los modelos desde Claude Opus 4.7 producen ~30% más
tokens para el mismo texto. La clave nunca se imprime.

**Limitaciones de `verificar_entidades.py`**: comprueba presencia literal,
no significado (una cápsula puede conservar `T3` y aun así atribuirle algo
mal); la detección de rutas descarta pares de prosa con barra
("filtro/orden", "HTML/CSS/JS"), y los nombres de rama solo se detectan si
tienen forma de ruta (`feature/x`) o van entre comillas invertidas. Por eso
el nivel por defecto es `suave` y `agresivo` exige prueba de retención.

## Palancas nativas de Claude Code

Suelen ahorrar más que comprimir texto. Verificadas el 2026-10-01 contra
`code.claude.com/docs/en/skills`, `/costs` y `/sub-agents`:

- **`CLAUDE.md` corto; el detalle en skills.** `CLAUDE.md` se carga al inicio
  de cada sesión; las skills cargan su cuerpo solo al invocarse. La
  documentación recomienda mantener `CLAUDE.md` por debajo de 200 líneas.
- **`description` corta.** En una sesión normal solo `name` + `description`
  están siempre en contexto. `description` + `when_to_use` se truncan a 1.536
  caracteres en la lista, y la lista entera tiene un presupuesto de
  caracteres (1% de la ventana de contexto del modelo): si se pasa, Claude
  Code descarta descripciones y el modelo pierde las palabras clave para
  elegir la skill. Lo primero de la descripción debe ser el caso de uso.
- **`disable-model-invocation: true` en skills propias de uso raro.** Su
  descripción no entra en el contexto, pero el modelo tampoco puede
  invocarlas: solo el usuario con `/nombre`. Para que un sub-agente use una
  así, el prompt le indica leer su `SKILL.md` por ruta. Las skills de Emil no
  se editan (copia idéntica, ver `docs/vendor/emilkowalski-skills.md`).
- **Modelo por sub-agente: campo `modelo:` del manifest.** Cada tarea del
  manifest puede llevar un campo opcional `modelo:`. El orquestador lo pasa
  como parámetro `model` al tool `Agent` (`orquestador` §1, integrado en M7).
  Si falta, el sub-agente hereda el modelo del orquestador. Valores: alias
  `sonnet`, `opus`, `haiku`, `fable` o un ID completo. Verificado: el `model`
  por invocación tiene precedencia sobre la definición del sub-agente y se
  mantiene si se reanuda el sub-agente. Cuándo usar uno más liviano:
  - `haiku`: tareas `docs` simples (README, comentarios, ajustes de texto
    acotados) y tareas de solo lectura o búsqueda sin decisiones de diseño.
  - `sonnet`: la mayoría de las tareas de código con criterios claros (la
    guía de costos de Claude Code dice que rinde en la mayoría de las tareas
    de programación y cuesta menos que Opus).
  - Sin `modelo:` (hereda el principal): lógica compleja, decisiones de
    arquitectura, razonamiento de varios pasos o tareas con alto riesgo de
    `DECISION_NEEDED`.
  Si dos corridas se van a comparar (como en la prueba de retención), van
  con el mismo modelo.
- **Exploración amplia con sub-agentes de búsqueda.** El sub-agente `Explore`
  (solo lectura) deja los volcados de archivos en su propio contexto y
  devuelve un resumen; además no carga `CLAUDE.md`. Lo mismo para correr
  tests o leer logs largos.

## Reglas

- Nada de métricas sin script.
- Una cápsula que no pasa `verificar_entidades.py` no se entrega.
- No comprimas por debajo del umbral.
- No reescribas criterios, respuestas del gate ni restricciones.
- No copies credenciales; avisa que las omitiste.
- No subas de nivel sin la prueba de retención correspondiente.
