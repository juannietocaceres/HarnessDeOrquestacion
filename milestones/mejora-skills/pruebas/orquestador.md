# Pruebas — M7 (integración en `orquestador/SKILL.md`)

Fecha: 2026-10-01. Comandos corridos desde la raíz del worktree de M7, después
de `git merge --ff-only main` (46fa018 → e6de756).

## Criterio 1 — "Manifests existentes siguen pasando preflight"

Script: `.claude/skills/triage-proyecto/scripts/preflight_manifest.py` (aplica
las reglas de `orquestador` §4). Ningún manifest existente se modificó.

```text
$ python .claude/skills/triage-proyecto/scripts/preflight_manifest.py milestones/panel-tareas-demo/milestone.yaml
Preflight de milestones/panel-tareas-demo/milestone.yaml
  aviso: tarea T2: sin criterios de aceptación -> el orquestador disparará `especificacion`
  wave 1: T1
  wave 2: T2
  wave 3: T3, T4, T5
RESULTADO: PASA (5 tareas, 3 waves)
exit=0

$ python .claude/skills/triage-proyecto/scripts/preflight_manifest.py milestones/enigma-go/milestone.yaml
Preflight de milestones/enigma-go/milestone.yaml
  wave 1: T1
  wave 2: T2, T3
  wave 3: T4
  wave 4: T5
  wave 5: T6
  wave 6: T7
RESULTADO: PASA (7 tareas, 6 waves)
exit=0

$ python .claude/skills/triage-proyecto/scripts/preflight_manifest.py milestones/mejora-skills/milestone.yaml
Preflight de milestones/mejora-skills/milestone.yaml
  wave 1: M1, M2, M3, M4
  wave 2: M5, M6
  wave 3: M7
  wave 4: M8
  wave 5: M9
RESULTADO: PASA (9 tareas, 5 waves)
exit=0
```

Tests del script:

```text
$ python .claude/skills/triage-proyecto/scripts/test_scripts.py
.......................
----------------------------------------------------------------------
Ran 23 tests in 0.058s

OK
```

Prueba adicional: un manifest de prueba (fuera del repo, en el scratchpad)
con `tipo: presentacion`, `tipo: contenido`, `modelo: sonnet`,
`modelo: claude-haiku-4-5` y `verificacion_manual` pasa el preflight:

```text
  aviso: tarea T1: tipo `presentacion` requiere M7 (aún no está en orquestador §1)
  aviso: tarea T2: tipo `contenido` requiere M7 (aún no está en orquestador §1)
  wave 1: T1
  wave 2: T2
RESULTADO: PASA (2 tareas, 2 waves)
exit=0
```

Los dos avisos ya no son ciertos tras M7 (los tipos están en §1). El script
es de `triage-proyecto` y queda fuera del alcance de M7: pasa como hallazgo
para M8/M9 (mover `presentacion`/`contenido` a `TIPOS_VIGENTES` en
`preflight_manifest.py` y actualizar la nota "requieren M7" de
`triage-proyecto/SKILL.md`).

**Veredicto: PASA.**

## Criterio 2 — "La tabla §8 solo nombra skills existentes"

Script (Python estándar, en el scratchpad de la sesión): extrae la sección
`## 8.` de `orquestador/SKILL.md`, toma la tercera columna de cada fila de la
tabla, saca los nombres entre comillas invertidas (descarta los modos
`capsula`/`empaquetar` de `optimizador-tokens`) y comprueba que cada uno es
una carpeta con `SKILL.md` en `.claude/skills/`. Además busca en toda la §8
las tres skills excluidas por el gate.

```python
sec = re.search(r'^## 8\..*?(?=^## 9\.)', txt, re.S | re.M).group(0)
filas = [l for l in sec.splitlines()
         if l.startswith('|') and not l.startswith('|---') and 'Momento' not in l]
col = [c.strip() for c in l.strip('|').split('|')][2]
nombres += [n for n in re.findall(r'`([^`]+)`', col) if n not in MODOS]
skills = {p.name for p in Path('.claude/skills').iterdir()
          if p.is_dir() and (p / 'SKILL.md').exists()}
```

```text
Filas de la tabla §8: 16
  OK    animate
  OK    animate-expo
  OK    documentacion
  OK    emil-design-eng
  OK    especificacion
  OK    frontend-design
  OK    mobile-native
  OK    optimizador-prompts
  OK    optimizador-tokens
  OK    presentaciones-visuales
  OK    review-animations
  OK    revision-codigo
  OK    testing
  OK    triage-proyecto
  OK    verificador-datos
Skills excluidas por el gate mencionadas en §8: ninguna
Otros identificadores entre comillas invertidas en §8 (fuera de la tabla):
  animation-vocabulary  (skill existente)
  contenido  (no es nombre de skill)
  descripcion  (no es nombre de skill)
  find-animation-opportunities  (skill existente)
  improve-animations  (skill existente)
  mejora-skills  (no es nombre de skill)
  pick-ui-library  (skill existente)
  presentacion  (no es nombre de skill)
  prototype  (skill existente)
  tipo  (no es nombre de skill)
RESULTADO: PASA
exit=0
```

Las 15 skills de la tabla existen; las 5 de Emil sin fila fija que se
nombran en el texto de §8 también existen; `apple-design`, `ask-sonner` y
`write-swift` no aparecen.

**Veredicto: PASA.**

## Registro (decisión del gate, wave 1)

Búsqueda de formas de voseo en `orquestador/SKILL.md` y
`optimizador-prompts/*.md` (`validás`, `agrupás`, `lanzás`, `implementás`,
`coordinás`, `construí`, `usá`, `indicá`, `partilas`, `acá`, `recién`,
`vos`): sin coincidencias.
