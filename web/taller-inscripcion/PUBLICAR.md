# Publicar el taller de inscripción en GitHub Pages

Skill `despliegue`. Nada de esto se ejecuta solo: el workflow es solo `workflow_dispatch` y la publicación requiere aprobación en el gate del milestone `e2e-skills-2`.

- Workflow: `.github/workflows/pages-taller-inscripcion.yml` (publica solo `web/taller-inscripcion/`).
- URL esperada: `https://juannietocaceres.github.io/HarnessDeOrquestacion/`.

## Aviso: un repo, un solo sitio de Pages

GitHub Pages da un único sitio por repositorio. Este workflow y `pages-enigma-go.yml` (landing Enigma Go) publican al mismo sitio y comparten `concurrency: pages`: **el último que corre reemplaza al otro**. Publicar el taller deja la landing fuera de línea hasta volver a correr su workflow, y viceversa. Para tener ambos a la vez hay que separar repositorios o unir las dos carpetas en un solo artefacto (decisión pendiente; no se tocó el workflow de enigma-go).

## Cómo se genera `config.js`

`config.js` está en `.gitignore`. En el build, el job lee las variables de repositorio `SUPABASE_URL` y `SUPABASE_ANON_KEY`, escribe un `.env` temporal en `$RUNNER_TEMP` y llama a `scripts/generar-config.js <ruta>`; luego borra el `.env`. Los valores no se imprimen en logs (solo se verifica que no estén vacíos). La anon key es pública por diseño (RLS la protege), pero va como variable del repo, no en el código. Nunca usar `service_role`.

El sitio publicado contiene solo: `index.html`, `404.html`, `styles.css`, `logic.js`, `app.js`, `config.js`. Quedan fuera `docs/`, `informe/`, `supabase/`, `tests/`, `scripts/`, `.env.example`.

## Prerrequisitos manuales (una vez)

1. Settings > Pages > Source: **GitHub Actions**; activar "Enforce HTTPS".
2. Cargar las variables (placeholders; los valores salen de Supabase > Project Settings > API):
   ```
   gh variable set SUPABASE_URL --repo juannietocaceres/HarnessDeOrquestacion --body "<project-url>"
   gh variable set SUPABASE_ANON_KEY --repo juannietocaceres/HarnessDeOrquestacion --body "<anon-public-key>"
   ```
3. Si se prefiere secreto: `gh secret set NOMBRE` y cambiar `vars.` por `secrets.` en el workflow.

## Publicar (solo tras aprobación)

```
git push origin main
gh workflow run pages-taller-inscripcion.yml --repo juannietocaceres/HarnessDeOrquestacion --ref main
gh run watch --repo juannietocaceres/HarnessDeOrquestacion
```

Deshacer: Settings > Pages > Unpublish site (o volver a correr `pages-enigma-go.yml` para restaurar la landing).

## Checklist de despliegue

| # | Punto | Resultado | Evidencia |
|---|---|---|---|
| 1.1 | Build en limpio | pendiente: después de publicar | el paso de armado copia 6 archivos; se verifica en el run |
| 1.2 | Solo la carpeta del sitio | OK | el artefacto se arma desde `web/taller-inscripcion` con 6 archivos |
| 2.1 | Ninguna clave en el repo | OK | `config.js` ignorado; el repo solo tiene `config.example.js` |
| 2.2 | Variables de `.env.example` | pendiente: manual | `SUPABASE_URL`, `SUPABASE_ANON_KEY` como variables del repo |
| 2.3 | Nada secreto en el cliente | OK | solo URL y anon key (RLS) |
| 3.1 | Rutas relativas | OK | recursos propios sin `/` inicial en `index.html` |
| 3.2 | Enlaces internos | pendiente: después de publicar | |
| 4.1 | Página 404 | OK | `404.html` en línea; enlace absoluto `/HarnessDeOrquestacion/` (uno relativo se rompe en rutas profundas) |
| 4.2 | HTTPS | pendiente: después de publicar | activar "Enforce HTTPS" |
| 5.1 | CORS | N/A | la API es Supabase; sin API propia |
| 6.1 | `prefers-reduced-motion` | styles.css tiene la regla |
| 7.1 | Límites y precios | N/A | no se afirma ninguno |
| 7.2 | Versiones de acciones | OK | `checkout@v4`, `configure-pages@v5`, `upload-pages-artifact@v3`, `deploy-pages@v5`, como en enigma-go (consultadas 2026-10-02); no re-verificadas en línea |
| 8.1 | Nada publica solo | OK | solo `workflow_dispatch` |
| 8.2 | Comando escrito | OK | sección "Publicar" |

## Registro de publicación

Pendiente de aprobación en el gate.
