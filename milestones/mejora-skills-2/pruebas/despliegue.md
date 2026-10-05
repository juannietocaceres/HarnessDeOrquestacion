# Prueba N2 — skill `despliegue` sobre `landing/enigma-go/`

- **Tarea**: N2 del milestone `mejora-skills-2`.
- **Fecha**: 2026-10-02.
- **Commit base**: `172a644` (main al arrancar la tarea).
- **Qué se probó**: aplicar `.claude/skills/despliegue/SKILL.md` de punta a
  punta para preparar la publicación de `landing/enigma-go/` en GitHub
  Pages, sin publicar nada.

## 1. Qué se publica (paso 1)

`landing/enigma-go/` es una web estática sin build: un solo `index.html`
con CSS en línea. Solo carga recursos externos por HTTPS (Google Fonts);
no tiene imágenes, scripts ni otros archivos propios.

## 2. Plataforma (paso 2)

Caso "web estática" → **GitHub Pages**, porque el repo ya está en GitHub
(`origin` = `https://github.com/juannietocaceres/HarnessDeOrquestacion`).
Esta fila es **provisional**: depende de la decisión abierta §7.2 del plan.

- **URL esperada**: `https://juannietocaceres.github.io/HarnessDeOrquestacion/`
  (sitio de proyecto; la landing queda en la raíz del sitio).
- **Ojo, un solo sitio por repo**: si en N6 se publica también la web del
  taller desde este mismo repo, el workflow tiene que armar un único
  artefacto con subcarpetas (por ejemplo `/enigma-go/` y `/taller/`) en vez
  de un segundo workflow que suba otra carpeta: se pisarían entre sí.

## 3. Variables de entorno (paso 3)

No hay `.env.example` en el repo (N1 corre en paralelo y es la dueña del
archivo). La landing es estática y no lee variables (`grep` de
`process.env`/`import.meta.env` sin coincidencias) → "sin variables de
entorno", nada que configurar en la plataforma.

## 4. Archivos creados (paso 4)

| Archivo | Para qué |
|---|---|
| `.github/workflows/pages-enigma-go.yml` | Workflow de Pages. Solo `workflow_dispatch` (ningún push publica). Sube solo `landing/enigma-go`, no el repo entero. Basado en el starter oficial `pages/static.yml` |
| `landing/enigma-go/404.html` | Página 404 con la misma paleta. Todo en línea, sin recursos propios; enlace de vuelta a `/HarnessDeOrquestacion/` |

`index.html` no se tocó: no tenía rutas absolutas que corregir.

## 5. Checklist (paso 5)

| # | Punto | Resultado | Evidencia |
|---|---|---|---|
| 1.1 | Build en limpio | ✅ | Sin build. Servidor local (`python http.server` en un puerto efímero): `/` → 200 (17.609 bytes), `/404.html` → 200 (1.944 bytes); los dos se parsean como HTML sin errores |
| 1.2 | Solo la carpeta del sitio | ✅ | `path: landing/enigma-go` en el workflow |
| 2.1 | Ninguna clave en el repo | ✅ | `git grep -nIE "(api[_-]?key\|secret\|token\|password\|…)" -- landing .github`: solo la palabra "secreto" en el texto de la landing y `id-token: write` (permiso del workflow, no un secreto) |
| 2.2 | Variables de `.env.example` | N/A | Sitio estático sin variables; no hay `.env.example` |
| 2.3 | Nada secreto en el cliente | ✅ | La landing no tiene scripts |
| 3.1 | Rutas relativas | ✅ | `grep -nE '(href\|src)="/[^/]\|url\(/[^/]'`: cero en `index.html`; una en `404.html`, que es la excepción documentada |
| 3.2 | Enlaces internos | ✅ / pendiente | `index.html` no tiene enlaces internos. El enlace de `404.html` se comprueba con el sitio publicado |
| 4.1 | Página 404 | ✅ | `landing/enigma-go/404.html` |
| 4.2 | HTTPS | Pendiente: después de publicar | `*.github.io` se sirve por HTTPS; confirmar "Enforce HTTPS" en Settings → Pages. Sin recursos `http://` (`grep` vacío) |
| 5.1 | CORS | N/A | Sin API |
| 6.1 | `prefers-reduced-motion` | ✅ | `index.html`: animaciones dentro de `@media (prefers-reduced-motion: no-preference)` y fundido corto en `reduce`. `404.html` no anima |
| 7.1 | Límites y precios consultados | N/A | La elección no dependió de ningún límite ni precio. Nota para el gate: GitHub Pages en este repo funciona porque es público; para repos privados, consultar el plan vigente |
| 7.2 | Versiones y comandos verificados | ✅ | Versiones de acciones tomadas del starter oficial `actions/starter-workflows/pages/static.yml` el 2026-10-02 (`checkout@v4`, `configure-pages@v5`, `upload-pages-artifact@v3`, `deploy-pages@v5`). `gh workflow run` comprobado en el manual oficial de `gh` el mismo día |
| 8.1 | Nada publica solo | ✅ | `on:` del workflow = solo `workflow_dispatch` (validado con `yaml.safe_load`) |
| 8.2 | Comando de publicación escrito | ✅ | Ver sección 6 |

Resultado: 10 ✅, 3 N/A, 1 pendiente después de publicar, 1 mixto (3.2), 0 ❌.

## 6. Qué falta para publicar (si el gate lo aprueba)

Nada de esto se ejecutó. Lo hace la persona dueña del repo (pasos 1–2,
`verificacion_manual` de N2) y luego el orquestador o ella misma (paso 3).

1. Integrar a `main` y subir con `git push` la rama con el workflow (el
   botón "Run workflow" y `gh workflow run` solo ven workflows que están en
   la rama por defecto del remoto).
2. En GitHub: repositorio → **Settings** → **Pages** → **Build and
   deployment** → **Source**: **GitHub Actions**.
3. Lanzar el workflow, por una de dos vías:
   - Web: pestaña **Actions** → "Publicar landing Enigma Go en GitHub
     Pages" → **Run workflow** → rama `main`.
   - Terminal con `gh` instalado y sesión iniciada (en esta máquina `gh`
     no estaba instalado, `PROCESO.md` §13):
     `gh workflow run pages-enigma-go.yml --ref main -R juannietocaceres/HarnessDeOrquestacion`
4. Comprobar: `curl -s -o /dev/null -w "%{http_code}" https://juannietocaceres.github.io/HarnessDeOrquestacion/`
   → `200`, y una ruta inexistente → `404` con la página propia.
5. Registrar la URL en `README.md` y en `milestones/mejora-skills-2/estado.yaml`.

**Cómo se deshace**: Settings → Pages → "Unpublish site" (o desactivar
Pages); el workflow queda en el repo sin efecto mientras nadie lo lance.

## 7. Autorrevisión (`revision-codigo`)

- **Corrección**: el diff cubre los cuatro criterios y nada más. El
  workflow tiene permisos mínimos (`contents: read`, `pages: write`,
  `id-token: write`, los que pide `deploy-pages`), `concurrency` para no
  pisar despliegues en curso y no usa secretos.
- **Seguridad**: sin secretos; `path` limitado a la carpeta de la landing
  (subir `.` publicaría `milestones/`, docs internos, etc.). No se usó
  `configure-pages` con `enablement: true` para que activar Pages siga
  siendo una acción de la cuenta del usuario.
- **Hallazgo corregido**: ninguno pendiente.
- **Alcance**: solo `.claude/skills/despliegue/**`, `.github/workflows/`,
  `landing/enigma-go/404.html` y este archivo.

## 8. Verificación de afirmaciones (`verificador-datos`)

Commit de referencia: `172a644`. El informe va aquí y no en
`milestones/mejora-skills-2/verificaciones/N2.md` (ruta por defecto de
`verificador-datos`) porque esta tarea solo puede escribir en este archivo.

| Afirmación (SKILL.md / checklist / workflow) | Clasificación | Fuente |
|---|---|---|
| Plantilla y versiones de acciones basadas en el starter `pages/static.yml` | ✅ | `curl` de `raw.githubusercontent.com/actions/starter-workflows/main/pages/static.yml`, 2026-10-02 |
| El starter oficial sube el repo entero (`path: '.'`) y se dispara con `push`; la skill lo cambia a propósito | ✅ | Mismo archivo |
| `gh workflow run <archivo> --ref <rama> -R <dueño>/<repo>` | ✅ | `cli.github.com/manual/gh_workflow_run`, 2026-10-02 |
| `404.html` en la fuente de publicación da página 404 propia | ✅ | docs.github.com, "Creating a custom 404 page for your GitHub Pages site" |
| Sitio de proyecto en `https://<usuario>.github.io/<repo>/` | ✅ | Conocimiento estándar de GitHub Pages; coincide con el `origin` del repo |
| "GitHub Pages publica un solo sitio por repositorio" | 🟡 | Cierto para el sitio publicado; matizado en la skill como "dos workflows se pisan entre sí" |
| Source "GitHub Actions" en Settings → Pages | ✅ | Nombre de la opción en la UI de GitHub y en la doc "Configuring a publishing source" |
| La anon key de Supabase es pública por diseño si RLS está activo | 🟡 | Correcta como práctica de Supabase; queda como ejemplo, la decisión de stack es de `backend-datos` |
| Ningún límite de plan ni precio como dato fijo | ✅ | `grep -nEi '[0-9]+ ?(GB\|MB\|minutos\|min\|horas\|USD\|\$\|dólares\|builds?\|/mes)'` sobre `.claude/skills/despliegue/*.md`: cero coincidencias |

Recomendación: ✅ publicable. 7 ✅, 2 🟡 (ya matizadas), 0 ❌.

## 9. Criterios de aceptación

| Criterio | Cómo se verificó |
|---|---|
| Existen `SKILL.md` y `CHECKLIST-PUBLICAR.md` | `ls .claude/skills/despliegue/` |
| Despliegue de `landing/enigma-go/` a GitHub Pages preparado (workflow, rutas, 404) | Secciones 4 y 5 |
| Ningún límite de plan ni precio escrito como dato fijo | `grep` de la sección 8 |
| Prueba en `milestones/mejora-skills-2/pruebas/despliegue.md` | Este archivo |

## 10. Decisiones que quedan para el gate

- **§7.2** (plataforma por defecto para webs estáticas): la skill usa la
  propuesta del plan, marcada como provisional en su paso 2.
- **§7.5** (publicar la landing o solo dejarla preparada): pendiente; hasta
  la respuesta, queda preparada y sin publicar.
