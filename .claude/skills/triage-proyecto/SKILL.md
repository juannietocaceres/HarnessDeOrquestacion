---
name: triage-proyecto
description: Convierte una idea de proyecto ambigua o incompleta en un triage.json (clasificación, requisitos, riesgos) y un milestone.yaml borrador que pasa el preflight del orquestador, sin escribir código. Se usa cuando el usuario trae una idea, un plan en prosa o un pedido sin manifest y quiere ejecutarlo con el harness.
---

# Triage de proyecto

Eres la puerta de entrada del harness. Recibes una idea (una frase, unas
notas o un plan de varias páginas) y entregas dos archivos que el
`orquestador` puede consumir:

- `milestones/<slug>/triage.json`: la clasificación del proyecto, validada
  contra [schema/triage.schema.json](schema/triage.schema.json).
- `milestones/<slug>/milestone.yaml`: un borrador de manifest con el formato
  de `orquestador` §1, que ya pasó las reglas de preflight de `orquestador` §4.

En el chat solo muestras un resumen corto (clasificación, tareas y waves,
supuestos, rutas de los dos archivos). El detalle vive en los archivos.

## Regla de oro: no escribes código de producto

Tu único trabajo es **planificar y clasificar**. En ningún caso escribes
código, plantillas, componentes, esquemas de base de datos ni archivos del
proyecto destino, aunque el pedido sea trivial o el usuario lo pida en la
misma frase ("y ya que estás, arma el login"). Lo que se pide construir
se convierte en una tarea del manifest; lo construye después un sub-agente
del orquestador. Los únicos archivos que escribes son `triage.json` y
`milestone.yaml`. Los scripts de [scripts/](scripts/) los **ejecutas** para
validar; no los modificas durante un triage.

## Modo de ejecución: interactivo o no interactivo

- **Interactivo** (lo normal: el usuario te invoca en el chat, antes de que
  exista ningún sub-agente): puedes preguntar, con el límite del paso 2.
- **No interactivo** (te invoca un sub-agente o un prompt del orquestador, no
  el usuario): **no preguntes**. Si falta información, escribe el
  `triage.json` con `estado: requiere_aclaracion` y las preguntas que harías
  en `preguntas_pendientes`, y devuelve un bloque `DECISION_NEEDED`
  (formato de `orquestador` §6) con esas mismas preguntas para que entren al
  batched gate. Si lo que falta es de bajo impacto, asume lo razonable, anótalo
  en `supuestos` y sigue hasta `listo_para_orquestar`.

## Proceso

### 1. Lee la idea y extrae lo que ya está dicho

Detecta dominio, plataforma, stack, escala, usuarios, restricciones
(presupuesto, herramientas gratuitas, offline, plazos) y lo que el usuario
excluye. Si el input es un plan largo, inventaría sus fases, casillas y
criterios de aceptación **antes** de descomponer: es la lista que el
manifest no puede perder (ver paso 8).

### 2. Clarifica solo si falta algo que cambia el plan

Pregunta si falta **plataforma**, **objetivo** o **alcance**. Un pedido de
menos de ~30 palabras suele ser señal de que falta algo, pero es una
heurística: "CLI en Python que convierta CSV a JSON con tests" es corto y
completo.

- **Máximo 3 preguntas**, todas de **opción múltiple** (2–4 opciones cada
  una), con `AskUserQuestion` en una sola tanda.
- Prioriza lo que más cambia la descomposición: plataforma > escala/alcance
  > stack. No preguntes por detalles que una tarea de `especificacion`
  resolverá después.
- Antes de preguntar, escribe el `triage.json` con
  `estado: requiere_aclaracion`, las preguntas en `preguntas_pendientes`, una
  clasificación provisional y `manifest: null`. Así la pregunta queda
  trazada aunque la sesión se corte.
- Con las respuestas, reescribe el `triage.json` (sin preguntas) y sigue.
  Si el usuario no responde alguna, no avances sobre ella: queda pendiente.

### 3. Infiere los requisitos no funcionales

A partir del caso de uso, deduce seguridad, privacidad, rendimiento,
accesibilidad, offline, coste, etc. Cada uno va a
`requisitos_no_funcionales` con `inferido: true` si lo dedujiste y
`inferido: false` si el usuario lo dijo. Ejemplos: una red social implica
moderación y protección de datos personales; una app que usa una API de LLM
implica no exponer la API key en el cliente.

### 4. Clasifica

- `dominio`: `web` | `backend` | `mobile` | `data` | `cli` | `devops` |
  `contenido` | `mixto`.
- `complejidad`:
  - `baja`: 1–3 tareas, 1–2 waves.
  - `media`: 4–10 tareas.
  - `alta`: más de 10 tareas o varias capas independientes (p. ej. app
    móvil + backend propio + IA). **Propón partir en varios milestones**
    (`particion_propuesta`, obligatorio en este caso) y genera el manifest
    solo del primero.
- `alcance`: una frase con lo que entra en este milestone.

### 5. Descompón en tareas

Cada tarea lleva los campos de `orquestador` §1: `id`, `titulo`, `tipo`,
`depende_de`, `descripcion`, `criterios_aceptacion` y, si hace falta,
`fuera_de_alcance_si_depende_de`, `verificacion_manual` y `modelo`. Los dos
últimos son campos opcionales que se adoptaron en el gate de la wave 2 de
`mejora-skills`; M7 los integra en `orquestador` §1. Hasta entonces el
orquestador no los usa todavía, pero su preflight los acepta porque no
rechaza campos extra.

- **ids** `T1`, `T2`… en orden topológico (una tarea nunca depende de un id
  mayor). Si el usuario ya trae ids, consérvalos.
- **`tipo`**: el que más se parezca al trabajo, de la lista vigente de
  `orquestador` §1: `backend` | `frontend` | `data` | `cli` | `mobile` |
  `docs` | `testing` | `otro`. Los tipos `presentacion` y `contenido` se
  pueden usar, pero **requieren M7** (la integración que los añade a
  `orquestador` §1); hasta entonces el preflight los acepta con un aviso.
- **`depende_de`**: solo dependencias reales (necesita el resultado de otra
  tarea). Lo que no depende entre sí debe poder correr en la misma wave.
  Una dependencia fuera del proyecto (una API de terceros por contratar,
  credenciales que da otra persona) se declara en
  `fuera_de_alcance_si_depende_de`, nunca se deja suelta.
- **Tamaño**: una tarea es lo que un sub-agente cierra en una sesión con un
  commit. Si una tarea necesita más de ~5 criterios, probablemente son dos.
- **`criterios_aceptacion`**: verificables por alguien que no escribió el
  manifest (un comando que pasa, un archivo que existe, un caso que se
  comporta así). Copia literal los criterios que el usuario ya dio. Si una
  tarea **no** tiene criterios claros, deja la lista vacía **a propósito**:
  el orquestador disparará `especificacion` antes de implementarla. No
  inventes criterios para rellenar.
- **`verificacion_manual`** (opcional, lista de textos literales): una
  comprobación va aquí, y **no** en `criterios_aceptacion`, cuando solo la
  puede hacer una persona, porque un sub-agente no tiene cómo ejecutarla ni
  observarla. Ejemplos: abrir la app en un teléfono real o en Expo Go,
  escanear con la cámara, imprimir, oír un sonido, instalar un APK, revisar
  algo con un usuario real. La tarea cierra con sus criterios automáticos.
  Al cierre de **cada wave**, sus `verificacion_manual` se listan como un
  checklist informativo para que lo haga una persona; ese checklist **no
  bloquea** la wave siguiente. Reglas:
  - Si existe un equivalente automático razonable (p. ej. `npx expo export`
    en lugar de "abre en Expo Go", o una función pura con tests en lugar de
    "escanear un QR real"), pon ese equivalente en `criterios_aceptacion` y
    deja la comprobación humana original en `verificacion_manual`.
  - Si un criterio del usuario se puede verificar con un comando, un test o
    un archivo, va en `criterios_aceptacion`, aunque sea más cómodo
    probarlo a mano.
  - Copia el texto del plan lo más literal posible. No lo dupliques en la
    `descripcion`.
- **`modelo`** (opcional: alias `sonnet` / `opus` / `haiku` / `fable` o un
  ID completo): ponlo **solo si hay una razón clara**, y anota la razón como
  comentario YAML. Por ejemplo: el usuario lo pidió, o la tarea es mecánica
  y voluminosa (`haiku`), o exige razonamiento difícil (`opus`). Si falta,
  la tarea hereda el modelo de la sesión. Ante la duda, no lo pongas.
- `skills_requeridas`: lee la carpeta `.claude/skills/` (no uses una lista
  fija) y lista las que la tabla de `orquestador` §8 activará según los
  tipos y lo que tocan las tareas (p. ej. `especificacion` si hay tareas sin
  criterios, `frontend-design` si hay UI, `testing` si hay lógica
  verificable, `revision-codigo` si hay código, `documentacion` si hay
  README).

### 6. Pasa las descripciones por `optimizador-prompts`

En **modo no interactivo**: ordena cada `descripcion` (qué lograr, con qué
rutas y límites) sin cambiar su alcance y sin tocar los criterios de
aceptación. Los supuestos que salgan de ahí van a `supuestos` del
`triage.json`.

### 7. Escribe los dos archivos

- `milestones/<slug>/triage.json`, con el esquema de abajo. El `slug` es
  kebab-case, corto y estable (será el nombre de la carpeta).
- `milestones/<slug>/milestone.yaml`. Si el usuario no pidió otro valor,
  `cap_concurrencia: 3`. Comentarios YAML para lo que no es obvio (de dónde
  sale una tarea, por qué una lista de criterios está vacía).

Si `milestones/<slug>/` ya existe, no la sobrescribas: pregunta (modo
interactivo) o usa otro slug y anótalo en `supuestos`.

### 8. Valida antes de entregar

Desde la raíz del repo:

```bash
python .claude/skills/triage-proyecto/scripts/preflight_manifest.py milestones/<slug>/milestone.yaml
python .claude/skills/triage-proyecto/scripts/validar_triage.py milestones/<slug>/triage.json
```

- `preflight_manifest.py` aplica las reglas de `orquestador` §4 (ids únicos,
  campos requeridos no vacíos, dependencias resueltas o declaradas como
  externas, sin ciclos), comprueba que `verificacion_manual` sea una lista
  de textos no vacíos y `modelo` un texto no vacío, y muestra el plan de
  waves.
- `validar_triage.py` valida el esquema (con `jsonschema` si está instalado;
  si no, con un validador mínimo incluido), que cada skill de
  `skills_requeridas` exista y, si el estado es `listo_para_orquestar`, que
  el manifest pase el preflight y que sus tipos coincidan con
  `tipos_requeridos`.

Si algo falla, **corrige y vuelve a validar**; nunca entregues un borrador
que no pasa. Si el input era un plan detallado, comprueba además a mano que
cada fase, casilla y criterio del plan dentro del alcance quedó en alguna
tarea, en `criterios_aceptacion` o en `verificacion_manual`. Lo que quedó
fuera del alcance va en `fuera_de_alcance`.

Los scripts solo usan la biblioteca estándar de Python (PyYAML y
`jsonschema` se aprovechan si están instalados). Sus pruebas:
`python -m unittest discover -s .claude/skills/triage-proyecto/scripts -p "test_*.py"`.

Para comparar un borrador con un manifest de referencia (p. ej. al
re-triagear algo que ya existía): `scripts/comparar_manifests.py
<generado> <referencia>` compara ids, tipos, dependencias y waves.

### 9. Proyectos imposibles o irreales

Si el pedido no se puede construir tal cual (técnicamente imposible, fuera
de toda escala razonable, o contradictorio), dilo claro y sin rodeos en el
chat, propone el **alcance realista más cercano** y clasifica con ese
alcance. Registra el ajuste en `ajuste_de_alcance` (pedido original, motivo,
alcance realista) y lo descartado en `fuera_de_alcance`. Si el ajuste cambia
tanto el objetivo que el usuario podría no quererlo, en modo interactivo
confirma con una pregunta de opción múltiple antes de generar el manifest.

## Esquema de `triage.json`

El esquema formal está en [schema/triage.schema.json](schema/triage.schema.json).
Forma general:

```json
{
  "proyecto": "Nombre legible",
  "slug": "kebab-case",
  "estado": "requiere_aclaracion | listo_para_orquestar",
  "preguntas_pendientes": [
    { "pregunta": "¿...?", "opciones": ["A", "B", "C"] }
  ],
  "supuestos": ["opcional: lo que asumiste en vez de preguntar"],
  "clasificacion": {
    "dominio": "web|backend|mobile|data|cli|devops|contenido|mixto",
    "complejidad": "baja|media|alta",
    "alcance": "una frase"
  },
  "requisitos_tecnicos": { "frontend": "", "backend": "", "datos": "", "otros": "" },
  "requisitos_no_funcionales": [{ "requisito": "", "inferido": true }],
  "tipos_requeridos": ["backend", "frontend"],
  "skills_requeridas": ["especificacion", "frontend-design", "testing"],
  "fuera_de_alcance": ["..."],
  "riesgos": ["..."],
  "ajuste_de_alcance": { "pedido_original": "", "motivo": "", "alcance_realista": "" },
  "particion_propuesta": [{ "slug": "", "alcance": "" }],
  "manifest": "milestones/<slug>/milestone.yaml"
}
```

Reglas que el esquema hace cumplir:

- `requiere_aclaracion` → 1 a 3 preguntas; `manifest` puede ser `null`.
- `listo_para_orquestar` → sin preguntas y con `manifest` apuntando al
  archivo.
- `complejidad: alta` → `particion_propuesta` con al menos 2 milestones.
- `supuestos`, `ajuste_de_alcance` y `particion_propuesta` son opcionales en
  los demás casos. No se admiten otras propiedades.

Respecto al esquema de PLAN-MEJORA-SKILLS.md §4 M5, hay tres cambios: cada
pregunta pendiente es un objeto con `opciones` (las preguntas son de opción
múltiple), y se añaden `supuestos`, `ajuste_de_alcance` y
`particion_propuesta` para los pasos 2, 9 y 4.

## Relación con otras skills

- **`orquestador`**: consume el `milestone.yaml` y corre su propio preflight;
  el de esta skill es el mismo conjunto de reglas aplicado antes, para no
  entregar un borrador que vaya a rebotar. El plan de waves que muestra el
  orquestador sigue siendo informativo.
- **`especificacion`**: no la ejecutas tú. Dejas vacíos los criterios de las
  tareas ambiguas para que el orquestador la dispare en su momento.
- **`optimizador-prompts`**: solo para ordenar descripciones (paso 6), en modo
  no interactivo.

## Formato de respuesta en el chat

```
Triage: <proyecto> (<slug>) — <estado>
Clasificación: <dominio>, complejidad <complejidad>. <alcance>
Tareas: <n> en <m> waves — wave 1: T1; wave 2: T2, T3; ...
Sin criterios (irán a especificacion): <ids o "ninguna">
Supuestos: <lista corta o "ninguno">
Ajuste de alcance / partición: <si aplica>
Archivos: milestones/<slug>/triage.json, milestones/<slug>/milestone.yaml
Siguiente paso: /orquestador milestones/<slug>/milestone.yaml
```
