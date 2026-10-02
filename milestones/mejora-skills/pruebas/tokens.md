# Prueba de `optimizador-tokens` (M6)

Fecha: 2026-10-01. Todas las cifras de tokens salen de
`.claude/skills/optimizador-tokens/scripts/medir_tokens.py` (método
`estimado` = caracteres // 4; no hubo `ANTHROPIC_API_KEY` en la corrida).
Las salidas crudas de cada medición están en [tokens/](tokens/).

## 1. Costo fijo de las descriptions de las skills

Lo que Claude Code mete en el contexto de **cada** sesión: `name` +
`description` de cada skill que el modelo ve. Las skills con
`disable-model-invocation: true` no ocupan la lista (verificado en
`code.claude.com/docs/en/skills`). Mismo método que
`docs/vendor/emilkowalski-skills.md` (caracteres / 4).

Comando:
`python .claude/skills/optimizador-tokens/scripts/medir_tokens.py --descriptions .claude/skills --excluir optimizador-tokens`
→ [tokens/medicion-descriptions.json](tokens/medicion-descriptions.json)

| Conjunto (las 19 skills previas a M6) | Skills | En contexto | Caracteres en contexto | Tokens en contexto |
|---|---:|---:|---:|---:|
| **Total** | 19 | 16 | 6.038 | **1.504** |
| Propias del harness | 8 | 8 | 2.573 | 640 |
| Emil Kowalski | 10 | 7 | 3.244 | 809 |
| `frontend-design` (vendorizada de Anthropic) | 1 | 1 | 221 | 55 |

Las 3 de Emil fuera de la lista (`pick-ui-library`, `prototype`,
`review-animations`) suman 707 caracteres que no se cargan. Con
`optimizador-tokens` (335 caracteres, 83 tokens) el total queda en
**1.587 tokens** por sesión (20 skills, 17 visibles). Cifra coherente con la
de `docs/vendor/emilkowalski-skills.md` (807 tokens de Emil): la diferencia
de 2 tokens es el separador `": "` entre nombre y descripción que este script
agrega por skill.

Las más caras siguen siendo de Emil: `mobile-native` (188), `animate-expo`
(134), `animate` (120), `improve-animations` (116), `animation-vocabulary`
(111). La propia más cara es `verificador-datos` (106).

## 2. Prueba de retención sobre T2 de `panel-tareas-demo`

### Material

| Archivo | Qué es |
|---|---|
| [tokens/contexto-completo.md](tokens/contexto-completo.md) | Contexto crudo que el orquestador tenía para T2 en la wave 2: spec de T2, `schema/tareas.md` (resultado de T1), manifest completo, decisiones de la wave 1. |
| [tokens/capsula-suave.md](tokens/capsula-suave.md) | El mismo contexto en cápsula `suave`, escrita siguiendo la skill. |
| [tokens/prompt-completo.md](tokens/prompt-completo.md) | Prompt del sub-agente (PLANTILLA-SUBAGENTE adaptada a corrida aislada) con el contexto crudo en `[CONTEXTO]`. |
| [tokens/prompt-capsula.md](tokens/prompt-capsula.md) | Prompt idéntico salvo `[CONTEXTO]`, que lleva la cápsula. `<DIRECTORIO_TRABAJO>` se reemplazó al lanzar por un directorio temporal fuera del repo. |
| [tokens/verificar_t2.py](tokens/verificar_t2.py) | Checks reproducibles: C1–C4 = criterios de aceptación de la spec de T2; F1–F9 = detalles de fidelidad que una compresión mala perdería (UUID v4, máx. 200 caracteres, enum exacto, estado inicial, fuera de alcance, JSON válido). |
| [tokens/resultados/](tokens/resultados/) | Los dos contratos producidos y la salida de `verificar_t2.py`. |

### Entidades protegidas

`verificar_entidades.py contexto-completo.md capsula-suave.md` → código 0,
40 entidades revisadas (10 rutas, 8 IDs de tarea, 3 UUID, 19 literales),
0 faltantes, sin credenciales →
[tokens/entidades-capsula.json](tokens/entidades-capsula.json).

### Ahorro medido

| Comparación | Tokens original | Tokens final | Ahorro |
|---|---:|---:|---:|
| Contexto crudo → cápsula `suave` ([json](tokens/medicion-capsula.json)) | 2.210 | 1.024 | **54%** |
| Prompt completo → prompt con cápsula ([json](tokens/medicion-prompts.json)) | 2.735 | 1.549 | **43%** |

El contexto crudo (2.210) quedó apenas por encima del umbral vigente durante
la prueba (~2.000), así que en ese momento la regla mandaba comprimir. Con el
umbral nuevo (~4.000, ver abajo) este contexto ya no se comprimiría.

### Corridas

Dos sub-agentes `general-purpose`, mismo modelo (heredado, sin override),
lanzados en paralelo una sola vez, cada uno en un directorio temporal fuera
del repo, sin acceso a las fuentes (el prompt se lo prohibía) y sin commits.

| Corrida | Estado | Tokens totales del sub-agente (reporte del tool `Agent`) | Tool uses | Contrato producido (tokens, script) |
|---|---|---:|---:|---:|
| Contexto completo | COMPLETADA, sin `DECISION_NEEDED` | 48.127 | 3 | 1.815 |
| Cápsula `suave` | COMPLETADA, sin `DECISION_NEEDED` | 45.594 | 3 | 1.565 |

La diferencia total entre corridas fue de 2.533 tokens (~5% del total del
sub-agente): la mayor parte del gasto de un sub-agente es su contexto fijo
(system prompt, herramientas, lista de skills) y su propia salida, no el
bloque `[CONTEXTO]`.

### Resultado de los checks

`python milestones/mejora-skills/pruebas/tokens/verificar_t2.py resultados/contrato-completo.md resultados/contrato-capsula.md`
→ [tokens/resultados/verificacion-t2.txt](tokens/resultados/verificacion-t2.txt)

| Check | Completo | Cápsula |
|---|:---:|:---:|
| C1 `POST /tareas` con request y response JSON (201, objeto completo) | OK | OK |
| C2 `GET /tareas` con response JSON array (200) | OK | OK |
| C3 error 400 con payload JSON que identifica `titulo` | OK | OK |
| C4 explícito que `id`, `estado`, `fecha_creacion` los asigna el servidor | OK | OK |
| F1–F9 fidelidad (JSON válido, 4 campos exactos, UUID v4, `pendiente` inicial, ISO 8601 Z, enum, máx. 200, fuera de alcance) | 9/9 | 9/9 |
| **Total** | **13/13** | **13/13** |

Controles: el contrato original de T2 (`api/contrato-tareas.md`, commit
`b6c7e47`) también da 13/13, y una copia del contrato de la cápsula con tres
defectos plantados (límite 250 en vez de 200, un UUID v1, `"Pendiente"` con
mayúscula) da 8/13 y sale con código 1, así que los checks discriminan.

Diferencias cualitativas (fuera de los criterios): las dos corridas tomaron
los mismos supuestos de fondo (definir la forma del error 400, ignorar en
silencio `id`/`estado`/`fecha_creacion` si el cliente los manda, 400 también
para títulos de más de 200 caracteres). La corrida completa agregó una
cabecera `Location: /tareas/{id}` (aclarando que `GET /tareas/{id}` queda
fuera de alcance); la de cápsula agregó una tabla de qué usa cada tarea de UI
(T3, T4, T5). Ninguna de las dos contradice la spec.

### Veredicto

**Retención aprobada para el nivel `suave`**: con 54% menos tokens de
contexto, el sub-agente produjo un contrato que cumple los mismos 4
criterios de aceptación y los mismos 9 checks de fidelidad que el de
contexto completo. Alcance del veredicto: una tarea (`docs`/contrato) y una
corrida por variante; no habilita `medio` ni `agresivo` para prompts de
sub-agentes.

### Umbral de compresión (§7.4): se sube a ~4.000 tokens

Decisión del usuario en el gate de la wave 2: el umbral pasa de ~2.000 a
**~4.000 tokens estimados**; por debajo no se comprime.

Por qué: con T2 (contexto de 2.210 tokens, apenas sobre el umbral anterior)
el ahorro total del sub-agente fue de 2.533 tokens, ~5% de su gasto (48.127
→ 45.594). Casi todo lo que gasta un sub-agente es su contexto fijo y su
propia salida, no el bloque `[CONTEXTO]`. Del otro lado, escribir la cápsula
costó 1.024 tokens de salida (más caros que los de entrada) para ahorrar
1.186 tokens de entrada por request. Con contextos de ese tamaño el ahorro
neto es poco frente a ese costo. Compactar empieza a pagar con contextos
más grandes o cuando varios sub-agentes reciben la misma cápsula.

El veredicto de retención no cambia: la cápsula `suave` no perdió calidad.
Lo que se ajusta es cuándo vale la pena hacerla.

## 3. Pruebas de los scripts

`python -m unittest discover -s .claude/skills/optimizador-tokens/scripts -v`
→ 21 pruebas, todas OK (Python 3.11.9, solo biblioteca estándar). Cubren,
entre otras cosas:

- `verificar_entidades.py` **sale con código 1** si falta un puerto, un ID de
  tarea o si cambia un literal (`pendiente` → `Pendiente`); código 3 si la
  cápsula trae algo con forma de credencial; código 2 ante archivo
  inexistente o regex inválida; no exige credenciales del original; normaliza
  `../../../schema/tareas.md` → `schema/tareas.md`; no toma "filtro/orden"
  como ruta.
- `medir_tokens.py`: estimación = caracteres // 4; `--comparar` calcula el
  ahorro; `--api` sin clave cae a `estimado` y avisa; con una clave falsa
  contra un puerto local cerrado cae a `estimado` sin imprimir la clave;
  `--descriptions` parsea `description` en una línea, entre comillas y en
  bloque `>`, excluye las skills con `disable-model-invocation: true`,
  clasifica el origen y respeta `--excluir`.
