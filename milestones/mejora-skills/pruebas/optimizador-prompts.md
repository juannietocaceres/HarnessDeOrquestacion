# Prueba — optimizador-prompts (M2)

Objetivo: comprobar que, al armar el prompt de sub-agente con
`.claude/skills/optimizador-prompts/PLANTILLA-SUBAGENTE.md`, los criterios de
aceptación del manifest aparecen **literales**.

## Input

Tarea elegida: **T4** de `milestones/enigma-go/milestone.yaml` (la que tiene
más criterios y referencias cruzadas al plan: §7, §8; buen caso para
detectar parafraseo).

```yaml
  - id: T4
    titulo: "Generador de casos + validador de solución"
    tipo: mobile
    depende_de: [T2, T3]
    descripcion: >
      Implementar src/engine/generator.ts (generateCase(config): elige
      escenario, crea sospechosos según scaling, elige culpable, construye
      pistas no falsas que eliminan a todos los inocentes y al menos una que
      apunta al culpable, agrega red herrings, rellena marcadores; en
      asesinato_roles asigna un sospechoso por jugador con secretBrief; en
      modo exterior/mixto rellena qrPayload "enigmago:{caseId}:{clueId}" y
      hidingHint) y src/engine/validator.ts con las 6 reglas de §8.
      El generador reintenta con otra semilla derivada hasta 10 veces y si
      falla lanza un error claro. Casos deterministas por semilla (caseId
      y createdAt incluidos: createdAt inyectable para tests).
    criterios_aceptacion:
      - "validator.ts implementa las 6 reglas de §8 con un test negativo por regla."
      - "Test que genera 500 casos con configuraciones aleatorias válidas: el 100% pasa validator y el esquema Zod de Case."
      - "La misma semilla + config produce el mismo caso (test)."
      - "En modo exterior/mixto cada pista que se escanea tiene qrPayload con el formato de §7 y hidingHint."
      - "npm test y npm run typecheck en verde."
```

Modo: no interactivo (simula al orquestador armando el prompt). Supuestos
tomados: el código vive en `enigma-go/` (comentario del manifest); T2 y T3
ya están integradas en `main`; tipo `mobile` con lógica verificable activa
`testing`; no toca UI, así que no aplica `frontend-design`.

## Output (prompt generado)

```text
Sos un sub-agente del harness de orquestación (estás en tu propio git worktree, en una rama propia). No ves la conversación del orquestador: este prompt es todo tu contexto.

[TAREA] T4 — "Generador de casos + validador de solución" — tipo: mobile (milestone `enigma-go`)

[OBJETIVO]
Implementar dos módulos del motor en enigma-go/:
1. src/engine/generator.ts con generateCase(config), que:
   - elige escenario, crea sospechosos según scaling y elige culpable;
   - construye pistas no falsas que eliminan a todos los inocentes y al menos una que apunta al culpable;
   - agrega red herrings y rellena marcadores;
   - en asesinato_roles asigna un sospechoso por jugador con secretBrief;
   - en modo exterior/mixto rellena qrPayload "enigmago:{caseId}:{clueId}" y hidingHint;
   - reintenta con otra semilla derivada hasta 10 veces y, si falla, lanza un error claro;
   - es determinista por semilla (caseId y createdAt incluidos; createdAt inyectable para tests).
2. src/engine/validator.ts con las 6 reglas de §8.

[CRITERIOS DE ACEPTACIÓN] (literales del manifest)
- "validator.ts implementa las 6 reglas de §8 con un test negativo por regla."
- "Test que genera 500 casos con configuraciones aleatorias válidas: el 100% pasa validator y el esquema Zod de Case."
- "La misma semilla + config produce el mismo caso (test)."
- "En modo exterior/mixto cada pista que se escanea tiene qrPayload con el formato de §7 y hidingHint."
- "npm test y npm run typecheck en verde."

[CONTEXTO]
- Plan fuente: milestones/enigma-go/plan.md (§5 tipos de juego, §6 escalado, §7 modelo de datos, §8 validador de solución).
- Archivos relevantes (de T2): enigma-go/src/engine/types.ts, enigma-go/src/lib/rng.ts, enigma-go/src/engine/scaling.ts.
- Archivos relevantes (de T3): enigma-go/src/engine/templates/ (JSON + index.ts con plantillas tipadas).
- Dependencias: T2 y T3 ya están integradas en main y visibles en tu worktree.

[SKILLS A APLICAR]
- testing: durante la implementación, la tarea introduce lógica verificable (lee .claude/skills/testing/SKILL.md).
- revision-codigo: autorrevisión antes de reportar (lee .claude/skills/revision-codigo/SKILL.md).

[RESTRICCIONES]
- Trabajás solo en tu worktree. Toca solo: enigma-go/src/engine/generator.ts, enigma-go/src/engine/validator.ts y sus tests en enigma-go/__tests__/. Nada más.
- No modifiques otros worktrees ni el checkout principal.
- No cambies types.ts, rng.ts, scaling.ts ni las plantillas; si necesitás un cambio ahí, es una decisión (ver protocolo).

[PROTOCOLO DE DECISIÓN]
Nunca le preguntes al usuario. Si encontrás una ambigüedad real de alto impacto que no podés resolver con lo que tenés, detenete y terminá tu turno devolviendo exactamente:
DECISION_NEEDED
tarea: T4
pregunta: "..."
opciones: ["A", "B"]
contexto: "..."
No commitees trabajo a medias que dependa de la respuesta; quedás pausado y se te reanuda con la respuesta. Para todo lo demás, asumí lo razonable y listá los supuestos en tu reporte.

[ENTREGA]
- Un solo commit en tu rama, mensaje en español que empiece por "T4: ...".
- Antes de commitear: `git status` para confirmar que solo tocaste las rutas permitidas.
- Reporte final (corto): estado (COMPLETADA o DECISION_NEEDED), nombre de rama, hash del commit, archivos creados/modificados, cada criterio de aceptación con cómo lo verificaste, supuestos tomados.
```

## Verificación (automática, no a ojo)

Se cargan los `criterios_aceptacion` de T4 directamente desde el YAML (con
PyYAML, así se resuelven las comillas igual que el orquestador) y se busca
cada uno, como línea exacta `- "<criterio>"`, dentro del bloque
`[CRITERIOS DE ACEPTACIÓN]` del prompt de arriba. Además se compara el bloque
completo contra la lista generada desde el YAML (mismo orden, nada de más).

Comando:

```bash
python - <<'EOF'
import re, yaml
m = yaml.safe_load(open("milestones/enigma-go/milestone.yaml", encoding="utf-8"))
crit = next(t for t in m["tareas"] if t["id"] == "T4")["criterios_aceptacion"]
doc = open("milestones/mejora-skills/pruebas/optimizador-prompts.md", encoding="utf-8").read()
prompt = doc.split("## Output (prompt generado)")[1].split("```text\n")[1].split("```")[0]
bloque = prompt.split("[CRITERIOS DE ACEPTACIÓN] (literales del manifest)\n")[1].split("\n\n")[0]
lineas = bloque.splitlines()
for c in crit:
    print("OK   " if f'- "{c}"' in lineas else "FALTA", c)
esperado = [f'- "{c}"' for c in crit]
print("BLOQUE IDENTICO" if lineas == esperado else "BLOQUE DISTINTO")
EOF
```

Salida:

```
OK    validator.ts implementa las 6 reglas de §8 con un test negativo por regla.
OK    Test que genera 500 casos con configuraciones aleatorias válidas: el 100% pasa validator y el esquema Zod de Case.
OK    La misma semilla + config produce el mismo caso (test).
OK    En modo exterior/mixto cada pista que se escanea tiene qrPayload con el formato de §7 y hidingHint.
OK    npm test y npm run typecheck en verde.
BLOQUE IDENTICO
```

## Veredicto

**Aprobada.** Los 5 criterios de aceptación de T4 aparecen literales en el
bloque `[CRITERIOS DE ACEPTACIÓN]` del prompt generado, en el mismo orden y
sin líneas de más (`BLOQUE IDENTICO`).

Control negativo: se repitió el mismo chequeo reemplazando, solo dentro del
prompt, el tercer criterio por una paráfrasis ("Misma semilla y config dan el
mismo caso (test).") y el script devolvió `FALTA` para ese criterio y
`BLOQUE DISTINTO`. O sea, la comprobación detecta un parafraseo y no es
trivialmente verdadera.

La claridad que agrega la skill quedó en `[OBJETIVO]` (la `descripcion` de un
solo párrafo pasada a lista, sin agregar ni quitar alcance), `[CONTEXTO]`
(secciones del plan y rutas concretas de T2/T3) y `[RESTRICCIONES]` (rutas
permitidas); los criterios no se tocaron.
