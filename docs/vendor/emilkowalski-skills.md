# Skills vendorizadas: suite de Emil Kowalski

Registro de la copia de skills de terceros hecha en la tarea M4 del
milestone `mejora-skills` (ver `PLAN-MEJORA-SKILLS.md` §4 M4). Mismo
estándar con el que se vendorizó `frontend-design` (`PROCESO.md` §5):
copia byte a byte, sin reescribir ni resumir, verificada con `diff`.

## Origen

| Campo | Valor |
|---|---|
| Repositorio | https://github.com/emilkowalski/skills |
| Commit usado | `d16ebe60d09a5ba2afcb7054ede9d0a10c9f6128` (`d16ebe6`, "Update README.md") |
| Fecha del commit | 2026-09-24 01:18:27 +0200 |
| Fecha de la copia | 2026-10-01 |
| Licencia | MIT, © 2026 Emil Kowalski. El `LICENSE` de la raíz del repo upstream se copió sin cambios como `LICENSE.txt` dentro de cada carpeta de skill. |

El commit usado coincide con el de referencia del plan: al clonar, `HEAD`
de `main` en upstream seguía siendo `d16ebe6`.

## Skills copiadas

Cada carpeta conserva su nombre original (varias skills se citan entre sí
por nombre) y su contenido completo, incluidos los archivos auxiliares.

| Skill | Archivos | Auto-invocable |
|---|---|---|
| `emil-design-eng` | `SKILL.md` | Sí |
| `animate` | `SKILL.md`, `RECIPES.md` | Sí |
| `animate-expo` | `SKILL.md`, `RECIPES.md` | Sí |
| `review-animations` | `SKILL.md`, `STANDARDS.md` | No (`disable-model-invocation: true`) |
| `improve-animations` | `SKILL.md`, `AUDIT.md`, `PLAN-TEMPLATE.md` | Sí |
| `find-animation-opportunities` | `SKILL.md` | Sí |
| `mobile-native` | `SKILL.md` | Sí |
| `pick-ui-library` | `SKILL.md` | No (`disable-model-invocation: true`) |
| `prototype` | `SKILL.md`, `PICKER.md` | No (`disable-model-invocation: true`) |
| `animation-vocabulary` | `SKILL.md` | Sí |

En total se copiaron 10 de las 13 skills de upstream. Las otras tres se
dejaron fuera por decisión del usuario en el gate de la wave 1 del
milestone `mejora-skills` (plan §7.1 y §7.2):

| Skill excluida | Decisión | Motivo |
|---|---|---|
| `write-swift` | Fuera (§7.1) | No hay proyectos Swift/iOS en el harness. Para React Native/Expo ya está `animate-expo`. |
| `ask-sonner` | Fuera (§7.2) | Uso raro. Costaba ~108 tokens por sesión y no se puede desactivar sin editar su frontmatter. |
| `apple-design` | Fuera (§7.2) | Uso raro. Costaba ~109 tokens por sesión y no se puede desactivar sin editar su frontmatter. |

`animation-vocabulary` se incluyó aunque también estaba en la lista de uso
raro (§7.2). Ninguna de las 10 skills copiadas cita a las tres excluidas,
así que dejarlas fuera no rompe ninguna referencia (ver "Verificación").
Para incorporarlas más adelante, sigue el procedimiento de "Cómo actualizar"
y registra la nueva decisión aquí.

Del repo upstream **no** se copiaron `README.md`, `performance-cheatsheet.md`
ni los archivos de configuración de la raíz (`.gitattributes`, `.gitignore`,
`.pl`): ninguna skill los referencia.

## Verificación

1. **Copia idéntica.** Para cada skill copiada, `diff -r` entre
   `skills/<s>` del clon upstream y `.claude/skills/<s>` del repo sale vacío
   salvo la línea `Only in ...: LICENSE.txt`; `cmp LICENSE <s>/LICENSE.txt`
   sale vacío.
2. **Referencias cruzadas.** Las skills se citan entre sí con el nombre
   entre comillas invertidas (`` `review-animations` ``). Búsqueda usada:

   ```bash
   grep -rnoE '`(emil-design-eng|animate-expo|animate|review-animations|improve-animations|find-animation-opportunities|animation-vocabulary|apple-design|mobile-native|pick-ui-library|prototype|ask-sonner|write-swift)\b' .claude/skills
   ```

   Nombres citados en upstream: `animate`, `animate-expo`,
   `review-animations`, `improve-animations`, `find-animation-opportunities`,
   `pick-ui-library`. Las seis existen como carpeta. En las 10 carpetas
   copiadas no aparece ninguna mención (ni con comillas invertidas ni en
   prosa) a las skills excluidas `write-swift`, `ask-sonner` y
   `apple-design`, ni tampoco a `animation-vocabulary`. Algunas
   coincidencias de `` `animate` `` son la prop `animate={...}` de Motion y
   no una referencia a la skill, pero la carpeta `animate` existe de todos
   modos.

### Finales de línea (Windows)

Todos los archivos upstream usan LF. Este repo se trabaja con
`core.autocrlf=true`, así que:

- La copia hecha con `cp` queda en LF en disco y se guarda en LF en los
  objetos de git: el contenido commiteado es byte a byte idéntico a upstream
  (`git ls-files --eol` muestra `i/lf`).
- Cuando git vuelva a escribir esos archivos en un checkout de Windows (por
  ejemplo, el checkout principal tras integrar la rama), los dejará en CRLF
  (`w/crlf`), igual que pasa hoy con `frontend-design`. Eso no es una
  modificación del contenido versionado, pero hace que un `diff -r` crudo
  contra un clon LF muestre todas las líneas como distintas.

Para verificar en un checkout de Windows, usar una de estas dos formas:

```bash
# a) ignorando el CR que agrega autocrlf
diff -r --strip-trailing-cr /ruta/al/clon/skills/<s> .claude/skills/<s>

# b) comparando contra lo commiteado (bytes exactos del objeto de git)
git -c core.autocrlf=false archive HEAD .claude/skills/<s> | tar -x -C /tmp/verif
diff -r /ruta/al/clon/skills/<s> /tmp/verif/.claude/skills/<s>
```

En Windows, `git archive` también aplica `core.autocrlf`: sin el
`-c core.autocrlf=false`, el archivo extraído sale en CRLF y el `diff`
falla. Así se verificó el commit de M4: el `diff -r` salió limpio (salvo
`LICENSE.txt`) y, además, se comparó cada blob de `git cat-file blob` con su
archivo upstream, sin diferencias.

No se agregó un `.gitattributes` para forzar LF porque la tarea M4 solo
puede tocar las carpetas de las skills y este documento; queda como
propuesta para una tarea posterior (`.claude/skills/** text eol=lf` o
`-text` en un `.gitattributes` de raíz).

## Cómo actualizar

1. Clonar upstream en un directorio temporal fuera del repo y anotar el
   hash: `git clone https://github.com/emilkowalski/skills <tmp> && git -C <tmp> rev-parse HEAD`.
2. Revisar qué cambió desde el commit registrado arriba:
   `git -C <tmp> diff d16ebe6 HEAD -- skills/ LICENSE`.
3. Para cada skill vendorizada: borrar la carpeta local, `cp -r <tmp>/skills/<s> .claude/skills/<s>`
   y `cp <tmp>/LICENSE .claude/skills/<s>/LICENSE.txt`.
4. Verificar con `diff -r` (ver arriba) y repetir la búsqueda de
   referencias cruzadas: si upstream agregó una skill nueva que las demás
   citan, decidir en el gate si se incorpora.
5. Volver a medir el costo de contexto (tabla de abajo) y actualizar este
   documento con el hash, la fecha y los cambios.

Alternativa descartada: `npx skills@latest add emilkowalski/skills`. Es más
rápida pero no deja claro qué versión quedó ni dónde se instala; la copia
manual con hash fijo es reproducible.

## Reglas de convivencia con el resto del harness

Tomadas del plan (§4 M4); el orquestador las incorpora en M7.

- `frontend-design` decide la **identidad visual**: paleta, tipografía,
  layout.
- `emil-design-eng`, `animate` y `animate-expo` deciden **movimiento,
  micro-interacciones y detalles de componentes**.
- Si chocan en algo concreto, gana el brief del usuario; después,
  `frontend-design` en lo estético y Emil en los valores de animación.
- **Entradas escalonadas (stagger): gana Emil, acotado** (decisión del
  usuario en el gate de la wave 1). El stagger de Emil (30–80 ms entre
  elementos, `ease-out`) se permite **solo dentro de un grupo de elementos
  relacionados**: los ítems de una lista, las celdas de una grilla o las
  tarjetas de un mismo bloque. **Nunca** se usa para una cascada decorativa
  de secciones enteras de la página (cada sección entrando con
  fade-and-slide-up al hacer scroll o al cargar). Ahí se aplica
  `frontend-design`: como máximo, un único momento orquestado. Las skills de
  Emil no se editan; esta regla la aplica quien las usa.
- Las skills con `disable-model-invocation: true` (`review-animations`,
  `pick-ui-library`, `prototype`) no se disparan solas. Para que un
  sub-agente las use, el orquestador le indica en el prompt *"lee y aplica
  `.claude/skills/review-animations/SKILL.md`"* (lectura directa del
  archivo, no invocación).

## Costo de contexto medido

Claude Code carga en el contexto de cada sesión el `name` + `description`
del frontmatter de cada skill auto-invocable; el cuerpo del `SKILL.md` solo
entra cuando la skill se usa. Las skills con `disable-model-invocation:
true` no ocupan esa lista. Medición con un script de Python estándar sobre
el clon upstream; tokens estimados como caracteres / 4.

| Skill | Caracteres `name`+`description` | Tokens ~ | `disable-model-invocation` | Tamaño de `SKILL.md` (caracteres) |
|---|---:|---:|---|---:|
| `emil-design-eng` | 170 | 42 | no | 27.029 |
| `animate` | 479 | 119 | no | 11.779 |
| `animate-expo` | 535 | 133 | no | 17.785 |
| `review-animations` | 176 | 44 | **sí** | 8.339 |
| `improve-animations` | 465 | 116 | no | 8.147 |
| `find-animation-opportunities` | 386 | 96 | no | 9.710 |
| `mobile-native` | 751 | 187 | no | 16.787 |
| `pick-ui-library` | 274 | 68 | **sí** | 4.760 |
| `prototype` | 251 | 62 | **sí** | 7.774 |
| `animation-vocabulary` | 444 | 111 | no | 13.181 |
| `apple-design` | 437 | 109 | no | 22.880 |
| `ask-sonner` | 433 | 108 | no | 7.147 |
| `write-swift` | 493 | 123 | no | 42.214 |

| Conjunto | Tokens ~ visibles al modelo en cada sesión |
|---|---:|
| Las 6 skills propias del harness (línea base, antes de M4) | ~405 |
| 9 skills base de Emil | ~696 |
| 9 base + `ask-sonner`, `apple-design`, `animation-vocabulary` (las 12 del plan) | ~1.025 |
| Las 13 (incluye `write-swift`) | ~1.148 |
| Solo las 3 de uso raro | ~328 |
| Solo `write-swift` | ~123 |

**Costo final con lo vendorizado (10 skills):** las 9 base más
`animation-vocabulary` suman 3.931 caracteres de `name`+`description`.
De ellos, 3.230 caracteres (unos **807 tokens**) son visibles para el modelo
en cada sesión, porque `review-animations`, `pick-ui-library` y `prototype`
no ocupan la lista. Con la línea base del harness (~405 tokens), la lista
de skills pasa de ~405 a ~1.212 tokens. Dejar fuera `write-swift`,
`ask-sonner` y `apple-design` ahorra ~340 tokens por sesión frente a
vendorizar las 13.

## Contradicciones encontradas en la lectura cruzada

Lectura cruzada de `frontend-design` contra `emil-design-eng` y `animate`.
Se registran aquí porque M4 no puede tocar `PROCESO.md`; la tarea que lo
actualice (M8) debería trasladarlas allí.

1. **Entradas escalonadas (stagger).** `frontend-design`: *"fade-and-slide-up
   entrances on each section and hover transitions on every card are the
   generic default and read as AI-generated"* y *"A single orchestrated
   moment ... lands better than scattered effects"*. Emil: en la tabla
   "Never Ship" de `animate`, *"Everything entering at once → 30–80ms
   stagger"*, y en `emil-design-eng` el checklist dice *"Elements all appear
   at once → Add stagger delay"*, con un ejemplo de `translateY(8px)` +
   fade. Choque real en entradas de página/secciones: una skill trata la
   entrada escalonada como señal de diseño genérico y la otra la exige por
   defecto. **Resuelta en el gate de la wave 1: gana Emil, acotado.** Ver
   la regla correspondiente en "Reglas de convivencia": se permite el
   stagger dentro de un grupo de elementos relacionados y nunca como
   cascada decorativa de secciones.
2. **Hover en tarjetas.** `frontend-design` desaconseja *"hover transitions
   on every card"*; los ejemplos de Emil usan
   `.element:hover { transform: scale(1.05); }` como patrón de
   gating táctil. No es una contradicción de fondo (Emil también dice que
   lo que se ve decenas de veces al día debe ser *"near-imperceptible only
   — fast and subtle, or nothing"*), pero el ejemplo puede leerse como
   recomendación de hover con escala. Se resuelve con la misma regla: el
   ejemplo ilustra el `@media`, no autoriza hover en cada tarjeta.
3. **Fricción con el harness (no con `frontend-design`).** Las 13 skills
   upstream abren con una sección "Initial Response": *"When this skill is
   first invoked without a specific question, respond only with: ... Do not
   provide any other information until the user asks a question."* Dentro
   de un sub-agente del orquestador eso no debe pasar: el prompt del
   sub-agente siempre trae la tarea concreta, que cuenta como "pregunta
   específica". Conviene que M7 lo diga explícitamente al delegar una skill
   de Emil. Del mismo modo, `emil-design-eng` exige tablas
   *Before/After/Why* al revisar código de UI; es compatible con
   `revision-codigo` si se usa como formato de los hallazgos de motion.

No se encontraron otras contradicciones: ambas partes coinciden en respetar
`prefers-reduced-motion`, en que el movimiento disparado por el usuario es
bienvenido cuando muestra qué cambió, y en reservar el movimiento
decorativo para momentos raros (el "delight budget" de Emil frente al
"single orchestrated moment" de `frontend-design`).
