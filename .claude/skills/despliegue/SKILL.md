---
name: despliegue
description: Prepara la publicación de un proyecto (web estática, web con framework, API o app Expo) en una plataforma gratuita, con la configuración versionada en el repo y el checklist de publicación. Úsala cuando un milestone o una tarea deba terminar con algo publicado; nunca publica sin aprobación explícita.
---

# Despliegue

Dejas un proyecto **listo para publicar**: eliges la plataforma, escribes la
configuración en el repo, pasas el checklist y entregas el comando exacto
que publica. Publicar es una acción con efecto fuera del repo: **nunca la
ejecutas tú sin una aprobación explícita** de la persona usuaria.

## Dos modos de uso

- **Suelto** (te lo piden directamente): preparas todo, muestras el
  checklist resuelto y preguntas si se publica, con la plataforma, la URL
  esperada y el comando exacto. No ejecutas nada hasta tener un "sí".
- **Dentro de un milestone** (corres como sub-agente del `orquestador`):
  **nunca le preguntas nada al usuario**. Preparas todo, dejas el checklist
  en el reporte y terminas tu turno con un `DECISION_NEEDED` de publicación
  (ver "Pedir la publicación"). Aunque te reanuden con un "sí", tampoco
  publicas tú: lo ejecuta el orquestador después del gate, salvo que la
  respuesta del gate diga explícitamente que lo hagas tú.

## Regla de datos que cambian

Límites de los planes gratuitos, precios, versiones de acciones o CLIs y
comandos cambian seguido. Esta skill **no los escribe como dato fijo** y tú
tampoco los escribes así en los archivos del proyecto:

- Cuando un límite o un precio importa para la decisión (ancho de banda,
  minutos de build, si el plan gratis permite repos privados, uso
  comercial), consúltalo en la documentación oficial vigente **en ese
  momento** (búsqueda web o `verificador-datos`) y anota en el reporte la
  fuente y la fecha de consulta.
- Si la necesidad solo se cubre con un plan pago, eso es un
  `DECISION_NEEDED`, nunca una elección silenciosa.
- Las versiones de las acciones de GitHub y los comandos de CLI que aparecen
  aquí son un punto de partida: compruébalos contra la fuente oficial antes
  de usarlos y deja la fecha de consulta en un comentario del archivo.

---

## Proceso

### 1. Qué se publica

Identifica la carpeta o el build que se publica y qué tipo de proyecto es
(web estática, web con framework y funciones de servidor, API, app Expo).
Si el proyecto tiene un paso de build, ubica el comando y la carpeta de
salida.

### 2. Elegir plataforma

> Decisión confirmada en el gate (§7.2 del plan): GitHub Pages para webs
> estáticas y Vercel para frameworks con funciones de servidor.

| Caso | Opción por defecto | Alternativa |
|---|---|---|
| Web estática (HTML/CSS/JS, landing, deck) | GitHub Pages (si el repo ya está en GitHub) | Netlify |
| Web con framework y funciones de servidor (Next, etc.) | Vercel | Netlify |
| API propia | La que sugiera `backend-datos` para ese stack, con plan gratuito | — |
| App Expo | Expo: Expo Go para probar; EAS para builds | — |

- Si el manifest o la persona usuaria ya fijaron la plataforma, se respeta.
- Si el caso no encaja en la tabla, o la opción por defecto no cubre la
  necesidad sin pagar → `DECISION_NEEDED` con las alternativas.
- **GitHub Pages publica un solo sitio por repositorio.** Si hay más de una
  cosa estática que publicar del mismo repo (por ejemplo una landing y un
  deck), el workflow arma un único artefacto con subcarpetas; dos workflows
  que suben carpetas distintas se pisan entre sí.

### 3. Variables de entorno (contrato con `backend-datos`)

`backend-datos` deja la lista de variables del proyecto en **`.env.example`**
en la raíz del proyecto: nombres y descripción, nunca valores reales.

- Lee `.env.example`. Cada variable tiene que quedar configurada en la
  plataforma (secretos del repositorio o del entorno en GitHub, variables
  del proyecto en Vercel/Netlify, secretos de EAS en Expo).
- Tú no configuras valores: listas en el checklist qué variable va dónde y
  eso pasa a `verificacion_manual` (requiere la cuenta del usuario).
- Si no hay `.env.example` y el proyecto es estático sin backend, anótalo
  ("sin variables de entorno") y sigue. Si no lo hay pero el código lee
  variables (`process.env`, `import.meta.env`, `Constants.expoConfig`),
  no lo inventes: es un hallazgo para `backend-datos` o un `DECISION_NEEDED`.
- No escribes en la carpeta de `backend-datos` ni en `.env.example`.

### 4. Configuración versionada en el repo

Todo lo que la plataforma necesita queda en archivos del repo, nunca solo
en un panel web:

| Plataforma | Archivos |
|---|---|
| GitHub Pages | `.github/workflows/<nombre>.yml` (ver plantilla abajo) y `404.html` en la carpeta publicada |
| Vercel | `vercel.json` si hace falta algo distinto del default del framework |
| Netlify | `netlify.toml` (comando de build, carpeta publicada, redirecciones) |
| Expo | `app.json` / `app.config.*` y `eas.json` |

#### Plantilla: workflow de GitHub Pages para una carpeta estática

Basada en el starter workflow oficial `pages/static.yml` de
`actions/starter-workflows`. Verifica las versiones de las acciones antes
de usarla.

```yaml
name: Publicar <proyecto> en GitHub Pages

# Solo manual: publicar requiere aprobación (skill despliegue).
# Agregar un trigger `push` es una decisión del gate, no un default.
on:
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: <carpeta-publicada>
      - id: deployment
        uses: actions/deploy-pages@v5
```

- `path` apunta **solo** a la carpeta que se publica, nunca a `.` (subir el
  repo entero publica todo, incluidos milestones y docs internos).
- Si hay build, agrega los pasos de instalación y build antes de subir el
  artefacto, y apunta `path` a la carpeta de salida.
- El trigger es solo `workflow_dispatch`: ningún push publica por accidente.

#### Rutas en GitHub Pages

Un sitio de proyecto se sirve en `https://<usuario>.github.io/<repo>/`, no
en la raíz del dominio. Por eso:

- Las rutas a recursos propios son **relativas** (`./estilos.css`,
  `img/logo.png`), nunca absolutas (`/estilos.css` apunta fuera del sitio).
- En frameworks, configura la ruta base (`base` en Vite, `basePath` en
  Next estático, etc.) con `/<repo>/`.
- **Excepción: `404.html`.** GitHub Pages lo sirve en cualquier ruta
  inexistente, a cualquier profundidad, así que ahí una ruta relativa no
  sabe dónde está la portada. El enlace de vuelta usa la ruta absoluta del
  sitio (`/<repo>/`) y la página no carga recursos propios (todo en
  línea).

### 5. Checklist antes de publicar

Recorre [CHECKLIST-PUBLICAR.md](CHECKLIST-PUBLICAR.md) completo. Es
obligatorio y su tabla de resultado va en el reporte de la tarea (o en el
archivo de prueba, si la tarea lo pide). Un punto en ❌ bloquea pedir la
publicación: corrígelo o, si la corrección tiene trade-offs, escálalo.

### 6. Pedir la publicación

Con el checklist en verde, terminas con un bloque como este (formato del
`orquestador` §6):

```
DECISION_NEEDED
tarea: <id>
pregunta: "¿Se publica <qué> en <plataforma>?"
opciones: ["Publicar ahora", "Dejar preparado sin publicar"]
contexto: "Plataforma: <plataforma>. URL esperada: <url>. Pasos: (1) <acción de cuenta, si falta>; (2) <comando exacto>. Checklist: <n>/<n> en verde. Se puede deshacer con: <cómo despublicar>."
```

- Incluye siempre: plataforma, URL esperada, comando o acción exacta, qué
  requiere la cuenta del usuario y cómo se deshace.
- "Dejar preparado" es una respuesta válida: la configuración queda
  versionada y la publicación se hace cuando se apruebe.

### 7. Lo que requiere la cuenta del usuario

Activar Pages en la configuración del repo, iniciar sesión en Vercel o
Netlify, crear la cuenta de Expo, cargar secretos: nada de eso lo haces tú
ni lo pides en el chat. Va como `verificacion_manual` en el manifest (o en
el reporte, si la tarea no la tenía) con pasos numerados, para que la
persona lo haga una vez. Nunca pidas que te peguen un token.

Ejemplo para GitHub Pages con workflow:

1. En GitHub: repositorio → **Settings** → **Pages**.
2. En **Build and deployment**, **Source**: elegir **GitHub Actions**.
3. Lanzar el workflow: pestaña **Actions** → el workflow → **Run workflow**
   sobre `main`, o desde una terminal con sesión iniciada en `gh`:
   `gh workflow run <archivo>.yml --ref main -R <usuario>/<repo>`.

### 8. Después de publicar

1. Comprueba que la URL responde con código 200
   (`curl -s -o /dev/null -w "%{http_code}" <url>`) y que una ruta
   inexistente devuelve la página 404 propia (código 404).
2. Registra la URL en el `README.md` del proyecto y en el `estado.yaml` del
   milestone (por ejemplo `publicado: {url: ..., fecha: ..., plataforma: ...}`
   en la tarea).
3. Si la URL no responde, no reintentes a ciegas: revisa el log de la
   corrida (pestaña Actions o el panel de la plataforma) y repórtalo.

---

## Qué nunca haces

- Publicar, activar un servicio, crear una cuenta o cambiar la
  configuración de un repo remoto sin aprobación explícita.
- Escribir claves, tokens o valores reales de variables en el repo, en el
  reporte o en el chat.
- Agregar un trigger que publique solo (`push`, `schedule`) sin que el gate
  lo haya decidido.
- Escribir límites de planes o precios como dato fijo.
- Elegir un plan pago en silencio.

## Skills relacionadas

- `backend-datos`: dueña de `.env.example` y de la elección de stack de la
  API (de ahí sale la plataforma para "API propia").
- `verificador-datos`: para límites, precios, versiones y comandos al
  momento de usarlos.
- `revision-codigo`: autorrevisión de los workflows y archivos de
  configuración (en especial secretos y permisos).
- Suite de Emil (`animate`, `review-animations`): si la UI pasó por ellas,
  el punto de `prefers-reduced-motion` del checklist ya debería estar
  cubierto; igual se comprueba.

## Fuentes (consultadas el 2026-10-05)

- Workflow oficial de Pages para sitios estáticos (acciones y permisos):
  https://github.com/actions/starter-workflows/blob/main/pages/static.yml
- Publicar con GitHub Actions y página 404 personalizada de Pages:
  https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
  y https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-custom-404-page-for-your-github-pages-site
