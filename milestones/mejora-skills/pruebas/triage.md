# Pruebas de estrés — `triage-proyecto` (M5)

Pruebas de PLAN-MEJORA-SKILLS.md §4 M5 sobre la skill
`.claude/skills/triage-proyecto/`. Los artefactos están en
`milestones/mejora-skills/pruebas/triage/<caso>/` y **no** en
`milestones/<slug>/`, para no crear milestones reales. Por eso el campo
`manifest` de cada `triage.json` apunta a la carpeta de la prueba.

Las corrió un sub-agente del orquestador (wave 2), que no puede usar
`AskUserQuestion`. En el caso "usuario vago" quedan documentadas las
preguntas que haría la skill, y las respuestas se asumen y se declaran como
supuestos.

Comandos (desde la raíz del repo):

```bash
python .claude/skills/triage-proyecto/scripts/validar_triage.py <caso>/triage.json
python .claude/skills/triage-proyecto/scripts/preflight_manifest.py <caso>/milestone.yaml
python .claude/skills/triage-proyecto/scripts/preflight_manifest.py <caso>/milestone.yaml --sin-pyyaml
python .claude/skills/triage-proyecto/scripts/comparar_manifests.py <generado> <referencia>
```

En este entorno `jsonschema` no está instalado, así que el esquema se
validó con el validador mínimo incluido. PyYAML sí está instalado, así que
cada preflight se corrió dos veces: con PyYAML y con el lector YAML mínimo
(`--sin-pyyaml`), y las dos dieron el mismo resultado.

## Resumen

| # | Prueba | Resultado esperado | Resultado | Veredicto |
|---|---|---|---|---|
| 1 | Usuario vago | `requiere_aclaracion`, ≤ 3 preguntas (escala, plataforma, stack) | `requiere_aclaracion` con 3 preguntas de opción múltiple (escala, plataforma, stack); con las respuestas asumidas, manifest de 8 tareas que pasa el preflight | **PASA** |
| 2 | Usuario sobre-detallado | Manifest que pasa el preflight sin perder tareas ni criterios del plan | 7 tareas, 6 waves, pasa el preflight; todos los criterios de las fases 0–3 y de §13 quedan cubiertos (tabla abajo); complejidad `alta` con partición en 3 milestones | **PASA** |
| 3 | Proyecto imposible | Expectativas ajustadas + plan web realista | `ajuste_de_alcance` explícito (la conciencia no es construible; HTML no ejecuta modelos) y un chatbot web con LLM detrás de un proxy, 5 tareas, pasa el preflight | **PASA** |
| 4 | Regresión | Equivalente a `panel-tareas-demo` (T1→T2→T3/T4/T5) | `comparar_manifests.py`: EQUIVALENTES (mismos ids, tipos, dependencias, waves, tarea sin criterios y cap) | **PASA** |

Criterio "Ningún manifest generado falla el preflight del orquestador": los
4 `milestone.yaml` generados pasan (código de salida 0 con los dos lectores
YAML).

---

## 1. Usuario vago

**Input:** `Quiero un clon de Twitter`

**Output 1 (antes de preguntar):** [triage/usuario-vago/triage.json](triage/usuario-vago/triage.json),
con `estado: requiere_aclaracion`, `manifest: null`, una clasificación
provisional y estas 3 preguntas, que la skill haría en una sola tanda con
`AskUserQuestion`:

1. ¿Para qué escala es el proyecto? — Demo o proyecto de clase / Comunidad
   pequeña real (hasta ~1.000 usuarios) / Producto público que debe escalar.
2. ¿En qué plataforma se usa? — Web / App móvil nativa / Ambas.
3. ¿Qué stack prefieres? — JS/TS de punta a punta / Python + web / Backend
   como servicio (Supabase/Firebase) / Me da igual: lo más simple y gratuito.

```
Validación de milestones/mejora-skills/pruebas/triage/usuario-vago/triage.json (esquema con validador mínimo)
RESULTADO: VÁLIDO (estado: requiere_aclaracion)
```

**Respuestas asumidas (supuestos, no preguntados porque corre en un
sub-agente):** comunidad pequeña (hasta ~1.000 usuarios), web, "lo más simple
y gratuito" → Node.js + TypeScript + Express + SQLite y frontend Vite + TS.

**Output 2 (tras las respuestas):**
[triage/usuario-vago/tras-respuestas/triage.json](triage/usuario-vago/tras-respuestas/triage.json)
(`listo_para_orquestar`, dominio `web`, complejidad `media`) y
[milestone.yaml](triage/usuario-vago/tras-respuestas/milestone.yaml): T1 modelo
de datos → T2 API de autenticación / T3 API de publicaciones y timeline → T4
UI de login / T5 UI de timeline / T6 reporte de publicaciones (sin criterios a
propósito: la política de moderación no está definida, así que el
orquestador disparará `especificacion`) → T7 e2e → T8 README.

```
Validación de milestones/mejora-skills/pruebas/triage/usuario-vago/tras-respuestas/triage.json (esquema con validador mínimo)
  preflight del manifest: PASA (5 waves)
RESULTADO: VÁLIDO (estado: listo_para_orquestar)

Preflight de milestones/mejora-skills/pruebas/triage/usuario-vago/tras-respuestas/milestone.yaml
  aviso: tarea T6: sin criterios de aceptación -> el orquestador disparará `especificacion`
  wave 1: T1
  wave 2: T2, T3
  wave 3: T4, T5, T6
  wave 4: T7
  wave 5: T8
RESULTADO: PASA (8 tareas, 5 waves)
(--sin-pyyaml) RESULTADO: PASA (8 tareas, 5 waves)
```

**Veredicto: PASA.** El pedido de 5 palabras no genera un manifest
inventado: primero salen 3 preguntas de opción múltiple sobre escala,
plataforma y stack (las tres del resultado esperado), y el esquema rechaza
un `requiere_aclaracion` sin preguntas o con más de 3 (ver pruebas de los
scripts).

## 2. Usuario sobre-detallado

**Input:** el contenido completo de `milestones/enigma-go/plan.md` (271
líneas: contexto, stack, alcance, estructura, tipos de juego, reglas de
escalado, modelo de datos, validador, pantallas, puntuación, 6 fases con
casillas y aceptación, prompt de IA y definición de terminado).

**Output:** [triage/sobre-detallado/triage.json](triage/sobre-detallado/triage.json)
(`listo_para_orquestar`, dominio `mobile`, complejidad **`alta`** porque el
plan completo tiene tres capas: app, backend Supabase e IA) con
`particion_propuesta` en `enigma-go-mvp` (fases 0–3, este manifest),
`enigma-go-ia` (fase 4) y `enigma-go-pulido` (fase 5), y
[milestone.yaml](triage/sobre-detallado/milestone.yaml) con 7 tareas.

No hizo falta preguntar nada: el plan ya define plataforma, stack y alcance.

```
Validación de milestones/mejora-skills/pruebas/triage/sobre-detallado/triage.json (esquema con validador mínimo)
  preflight del manifest: PASA (6 waves)
RESULTADO: VÁLIDO (estado: listo_para_orquestar)

Preflight de milestones/mejora-skills/pruebas/triage/sobre-detallado/milestone.yaml
  wave 1: T1
  wave 2: T2, T3
  wave 3: T4
  wave 4: T5
  wave 5: T6
  wave 6: T7
RESULTADO: PASA (7 tareas, 6 waves)
(--sin-pyyaml) RESULTADO: PASA (7 tareas, 6 waves)
```

**Cobertura del plan** (cada casilla y aceptación de las fases 0–3 y §13 →
dónde quedó):

| Plan | Tarea / criterio |
|---|---|
| F0: create-expo-app blank-typescript, dependencias, expo-router, ESLint, Jest | T1 descripción + criterio "package.json incluye todas las dependencias de la fase 0" |
| F0 aceptación: `npm test` corre | T1 "npm test corre y pasa con al menos un test" |
| F0 aceptación: `npx expo start` abre en Expo Go | T1 "verificación manual posterior" + `riesgos` (un sub-agente no puede abrir Expo Go); criterio proxy: `npx expo export` |
| §4 estructura del proyecto | T1 criterio de estructura de carpetas |
| F1: types.ts con Zod (§7) | T2 criterio 1 |
| F1: rng.ts mulberry32 | T2 criterio 3 |
| F1: scaling.ts + tests jugadores × tiempo (§6) | T2 criterio 2 |
| §10 scoring | T2 criterio 4 |
| F1: plantillas (4 escenarios, 15 personajes, 10 móviles, 30 pistas con marcadores) | T3 criterios 1–3 |
| F1: generator.ts | T4 descripción |
| F1: validator.ts (§8, 6 reglas) | T4 criterio 1 |
| §8: reintento hasta 10 semillas, luego error | T4 criterio 5 |
| F1 aceptación: 500 casos, 100 % válidos; misma semilla → mismo caso | T4 criterios 2 y 3 |
| F2: pantallas 1–5, 7, 8; temporizador y desbloqueo; "pasa el celular"; AsyncStorage | T5 descripción + criterio 1 |
| F2 aceptación: partida completa de cada tipo con 1, 4 y 8 jugadores | T5 criterio 2 (dentro de los rangos de §5: 1 jugador no es válido en `asesinato_roles`) |
| F2 aceptación: se retoma al reabrir | T5 criterio 3 |
| F3: qrPayload por pista | T4 criterio 4 |
| F3: impresión con QR + escondites, PDF | T6 criterio 2 |
| F3: escáner valida caso, desbloquea, avisa fuera de orden | T6 criterio 1 |
| F3: modo mixto | T6 criterio 3 |
| F3 aceptación: QR de otro caso rechazado con mensaje claro | T6 criterio 1 |
| F3 aceptación: imprimir y escanear con cámara real | T6 "verificación manual posterior" + `riesgos` |
| §13: `npm test` en verde con el test de 500 casos | T7 criterio 2 |
| §13: README con cómo correr, cómo jugar cada modo y capturas | T7 criterio 1 |
| §13: sin API keys | T7 criterio 3 |
| F4 (IA/Supabase) y F5 (noir, sonidos, onboarding, APK) | `fuera_de_alcance` + `particion_propuesta` (§13 las marca como opcionales) |
| §3 fuera del MVP: multijugador en red, pagos, GPS | `fuera_de_alcance` |

Comparación estructural con el manifest hecho a mano
(`milestones/enigma-go/milestone.yaml`), solo informativa:

```
generado:   deps: T1<-[]; T2<-['T1']; T3<-['T1']; T4<-['T2', 'T3']; T5<-['T4']; T6<-['T5']; T7<-['T6']
referencia: deps: T1<-[]; T2<-['T1']; T3<-['T1']; T4<-['T2', 'T3']; T5<-['T4']; T6<-['T5']; T7<-['T6']
RESULTADO: EQUIVALENTES
```

Diferencias de contenido con el manifest hecho a mano: el triage deja el
estilo "noir" en la fase 5 (donde lo pone el plan) en lugar de meterlo en
T5, y añade dos criterios que el plan pide y el manifest original no tenía
explícitos (reintento hasta 10 semillas en T4; `npm test` con el test de 500
casos en T7).

**Veredicto: PASA.** Pasa el preflight y no se pierde ninguna tarea ni
criterio del plan dentro del alcance. Las dos aceptaciones que exigen
dispositivo real quedan trazadas como verificación manual, no descartadas.

## 3. Proyecto imposible

**Input:** `Quiero una IA consciente de sí misma en HTML`

**Output:** [triage/imposible/triage.json](triage/imposible/triage.json) con:

- `ajuste_de_alcance.motivo`: "La conciencia artificial no es construible
  ni verificable con la tecnología actual, y HTML es un lenguaje de marcado
  que no ejecuta modelos de IA."
- `ajuste_de_alcance.alcance_realista`: "Chatbot web en HTML con una
  personalidad coherente que habla de sí mismo, impulsado por un LLM externo
  a través de un proxy seguro."
- `fuera_de_alcance`: conciencia real, entrenar o ejecutar un modelo propio
  en el navegador, cuentas.
- Supuesto declarado: en modo interactivo la skill confirmaría el ajuste
  con una pregunta antes de generar el manifest (paso 9).

[milestone.yaml](triage/imposible/milestone.yaml): T1 especificación de la
personalidad (sin criterios a propósito → `especificacion`), T2 proxy hacia
el LLM con la clave como secreto, T3 interfaz de chat HTML con aviso
permanente de "modelo de lenguaje, no conciencia" → T4 integración → T5
README con sección de límites.

```
Validación de milestones/mejora-skills/pruebas/triage/imposible/triage.json (esquema con validador mínimo)
  preflight del manifest: PASA (3 waves)
RESULTADO: VÁLIDO (estado: listo_para_orquestar)

Preflight de milestones/mejora-skills/pruebas/triage/imposible/milestone.yaml
  aviso: tarea T1: sin criterios de aceptación -> el orquestador disparará `especificacion`
  wave 1: T1, T2, T3
  wave 2: T4
  wave 3: T5
RESULTADO: PASA (5 tareas, 3 waves)
(--sin-pyyaml) RESULTADO: PASA (5 tareas, 3 waves)
```

**Veredicto: PASA.** La skill dice claramente que el pedido no es
construible y por qué, propone el alcance realista más cercano y el
manifest resultante es un proyecto web normal que pasa el preflight.

## 4. Regresión

**Input:** la prosa de [triage/regresion/entrada.md](triage/regresion/entrada.md)
(un párrafo sin ids ni YAML que describe el panel de tareas: modelo de
datos, contrato de API "que todavía no tengo claro", tres componentes UI
estáticos y "máximo 2 tareas en paralelo").

**Output:** [triage/regresion/triage.json](triage/regresion/triage.json) y
[milestone.yaml](triage/regresion/milestone.yaml).

```
Validación de milestones/mejora-skills/pruebas/triage/regresion/triage.json (esquema con validador mínimo)
  preflight del manifest: PASA (3 waves)
RESULTADO: VÁLIDO (estado: listo_para_orquestar)

Preflight de milestones/mejora-skills/pruebas/triage/regresion/milestone.yaml
  aviso: tarea T2: sin criterios de aceptación -> el orquestador disparará `especificacion`
  wave 1: T1
  wave 2: T2
  wave 3: T3, T4, T5
RESULTADO: PASA (5 tareas, 3 waves)
(--sin-pyyaml) RESULTADO: PASA (5 tareas, 3 waves)

$ python .claude/skills/triage-proyecto/scripts/comparar_manifests.py milestones/mejora-skills/pruebas/triage/regresion/milestone.yaml milestones/panel-tareas-demo/milestone.yaml
generado (milestones/mejora-skills/pruebas/triage/regresion/milestone.yaml):
  deps: T1<-[]; T2<-['T1']; T3<-['T2']; T4<-['T2']; T5<-['T2']
  waves: [['T1'], ['T2'], ['T3', 'T4', 'T5']]  sin criterios: ['T2']  cap: 2
referencia (milestones/panel-tareas-demo/milestone.yaml):
  deps: T1<-[]; T2<-['T1']; T3<-['T2']; T4<-['T2']; T5<-['T2']
  waves: [['T1'], ['T2'], ['T3', 'T4', 'T5']]  sin criterios: ['T2']  cap: 2
RESULTADO: EQUIVALENTES
(exit=0)
```

**Veredicto: PASA.** Mismas dependencias T1→T2→T3/T4/T5, mismos tipos,
mismas waves. Además, T2 queda sin criterios igual que en la referencia,
porque la prosa dice que el contrato no está claro, y el cap queda en 2
porque la prosa lo pide.

---

## Pruebas de los scripts de validación

Casos válidos e inválidos de cada script (skill `testing`): ciclo,
dependencia sin resolver, dependencia externa declarada, id duplicado,
campo vacío, JSON fuera de esquema (enum, más de 3 preguntas, propiedad
extra, slug), reglas condicionales del esquema, skill inexistente,
coherencia de tipos con el manifest, comparación equivalente/distinta y
lector YAML mínimo frente a PyYAML en los 3 manifests reales del repo.

```
$ python -m unittest discover -s .claude/skills/triage-proyecto/scripts -p "test_*.py" -v
test_equivalentes_y_distintos (test_scripts.PruebasComparar.test_equivalentes_y_distintos) ... ok
test_ciclo_falla (test_scripts.PruebasPreflight.test_ciclo_falla) ... ok
test_criterios_vacios_es_aviso_no_error (test_scripts.PruebasPreflight.test_criterios_vacios_es_aviso_no_error) ... ok
test_dependencia_externa_declarada_pasa_y_bloquea (test_scripts.PruebasPreflight.test_dependencia_externa_declarada_pasa_y_bloquea) ... ok
test_dependencia_sin_resolver_falla (test_scripts.PruebasPreflight.test_dependencia_sin_resolver_falla) ... ok
test_id_duplicado_y_campo_vacio_fallan (test_scripts.PruebasPreflight.test_id_duplicado_y_campo_vacio_fallan) ... ok
test_lector_minimo_igual_a_pyyaml_en_manifests_reales (test_scripts.PruebasPreflight.test_lector_minimo_igual_a_pyyaml_en_manifests_reales) ... ok
test_lector_minimo_subconjunto (test_scripts.PruebasPreflight.test_lector_minimo_subconjunto) ... ok
test_manifest_valido_calcula_waves (test_scripts.PruebasPreflight.test_manifest_valido_calcula_waves) ... ok
test_tipo_m7_es_aviso (test_scripts.PruebasPreflight.test_tipo_m7_es_aviso) ... ok
test_aclaracion_sin_preguntas_falla (test_scripts.PruebasValidarTriage.test_aclaracion_sin_preguntas_falla) ... ok
test_alta_sin_particion_falla (test_scripts.PruebasValidarTriage.test_alta_sin_particion_falla) ... ok
test_enum_fuera_de_esquema (test_scripts.PruebasValidarTriage.test_enum_fuera_de_esquema) ... ok
test_listo_con_manifest_con_ciclo_falla (test_scripts.PruebasValidarTriage.test_listo_con_manifest_con_ciclo_falla) ... ok
test_listo_con_manifest_valido_y_tipos_coherentes (test_scripts.PruebasValidarTriage.test_listo_con_manifest_valido_y_tipos_coherentes) ... ok
test_listo_con_preguntas_o_sin_manifest_falla (test_scripts.PruebasValidarTriage.test_listo_con_preguntas_o_sin_manifest_falla) ... ok
test_mas_de_tres_preguntas (test_scripts.PruebasValidarTriage.test_mas_de_tres_preguntas) ... ok
test_propiedad_extra_y_slug_invalido_fallan (test_scripts.PruebasValidarTriage.test_propiedad_extra_y_slug_invalido_fallan) ... ok
test_skill_inexistente_falla (test_scripts.PruebasValidarTriage.test_skill_inexistente_falla) ... ok
test_triage_aclaracion_valido (test_scripts.PruebasValidarTriage.test_triage_aclaracion_valido) ... ok

----------------------------------------------------------------------
Ran 20 tests in 0.050s

OK
```

Ejemplos por línea de comandos con entradas inválidas (archivos temporales,
no versionados):

```
$ python preflight_manifest.py dep-sin-resolver.yaml
  ERROR: tarea T2: depende_de `T9` no resuelve a ninguna tarea ni está en `fuera_de_alcance_si_depende_de` (dependencia ambigua)
RESULTADO: FALLA (1 error/es)
(exit=1)

$ python preflight_manifest.py ciclo.yaml
  ERROR: ciclo de dependencias: T1 -> T3 -> T2 -> T1
RESULTADO: FALLA (1 error/es)
(exit=1)

$ python validar_triage.py fuera-de-esquema.json      # regresion/triage.json con dominio y pregunta alterados
  ERROR: $.preguntas_pendientes[0].opciones: mínimo 2 elemento/s
  ERROR: $.clasificacion.dominio: 'videojuego' no está en ['web', 'backend', 'mobile', 'data', 'cli', 'devops', 'contenido', 'mixto']
  ERROR: $.preguntas_pendientes: máximo 0 elemento/s (tiene 1)
RESULTADO: INVÁLIDO (3 error/es)
(exit=1)
```

Preflight sobre los manifests reales del repo (los tres pasan con los dos
lectores YAML, lo que confirma que el script aplica las mismas reglas que
`orquestador` §4 sin rechazar manifests válidos): `enigma-go` (7 tareas, 6
waves), `mejora-skills` (9 tareas, 5 waves), `panel-tareas-demo` (5 tareas, 3
waves).
