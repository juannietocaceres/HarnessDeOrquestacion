# Checklist antes de publicar

Obligatorio antes de pedir la publicación (skill `despliegue`, paso 5).
Cada punto se marca ✅ (cumple), ❌ (no cumple: bloquea) o N/A (no aplica,
con el motivo). La tabla de resultado del final va en el reporte de la
tarea.

## 1. Build

- [ ] **El build de producción pasa en limpio.** Corre el comando de build
  del proyecto desde cero (sin caché ni carpeta de salida previa) y sin
  errores. Si es estático sin build, comprueba que la carpeta publicada
  tiene `index.html` y que se abre en el navegador sin errores en consola.
- [ ] **La carpeta publicada es solo la del sitio.** El workflow o la
  configuración apunta a la carpeta de salida, no a la raíz del repo.

## 2. Secretos y variables

- [ ] **Ninguna clave en el repo.** Busca en lo que se publica y en el diff:
  `git grep -nIE "(api[_-]?key|secret|token|password|passwd|BEGIN [A-Z ]*PRIVATE KEY)"`
  y revisa cada coincidencia. `.env` está en `.gitignore`.
- [ ] **Variables de `.env.example` configuradas en la plataforma.** Lista
  cada variable y dónde va (secreto del repo/entorno, variable del
  proyecto). Configurarlas es `verificacion_manual`. Sin `.env.example` en
  un proyecto estático: N/A con el motivo.
- [ ] **Nada de secretos en el cliente.** En un sitio estático, todo lo que
  se publica es público: ninguna variable que el navegador lea puede ser
  secreta (solo claves públicas por diseño, como la anon key de Supabase con
  RLS activo).

## 3. Rutas

- [ ] **Rutas relativas correctas para el subdominio.** En GitHub Pages
  (sitio de proyecto en `/<repo>/`): ningún recurso propio con ruta absoluta
  (`href="/..."`, `src="/..."`, `url(/...)`). Comprueba con
  `grep -nE '(href|src)="/[^/]|url\(/[^/]' <carpeta>/*.html`.
  En frameworks: ruta base configurada.
- [ ] **Enlaces internos funcionan** desde la URL publicada (anclas,
  páginas internas, descargas).

## 4. 404 y HTTPS

- [ ] **Hay página 404 propia** (`404.html` en la carpeta publicada para
  GitHub Pages; equivalente de la plataforma en las demás). Su enlace de
  vuelta usa la ruta absoluta del sitio y no carga recursos propios.
- [ ] **HTTPS.** La URL publicada se sirve por HTTPS (en GitHub Pages,
  "Enforce HTTPS" activo en Settings → Pages; con dominio propio, revisar
  que el certificado esté emitido). No hay recursos cargados por `http://`
  (contenido mixto).

## 5. API

- [ ] **CORS permite solo el dominio publicado** (y `localhost` solo en
  desarrollo). Nada de `*` en una API con datos de usuarios. Sin API: N/A.

## 6. Accesibilidad del movimiento

- [ ] **Las animaciones respetan `prefers-reduced-motion`.** Hay una regla
  `@media (prefers-reduced-motion: reduce)` (o la animación vive dentro de
  `no-preference`), o el equivalente en la librería de animación. Sin
  animaciones: N/A.

## 7. Datos que cambian

- [ ] **Límites y precios consultados al momento.** Si un límite del plan
  gratuito o un precio influyó en la elección, quedó anotado con la fuente
  y la fecha de consulta. Ningún archivo del proyecto lo afirma como dato
  fijo.
- [ ] **Versiones de acciones y comandos verificados** contra la fuente
  oficial, con fecha.

## 8. Publicación controlada

- [ ] **Nada publica solo.** El workflow se dispara solo con
  `workflow_dispatch` (o la plataforma no tiene despliegue automático
  activo) hasta que el gate decida otra cosa.
- [ ] **Comando o acción exacta de publicación escrita**, junto con la URL
  esperada y cómo se deshace.

---

## Tabla de resultado (copiar al reporte)

| # | Punto | Resultado | Evidencia |
|---|---|---|---|
| 1.1 | Build en limpio | | |
| 1.2 | Solo la carpeta del sitio | | |
| 2.1 | Ninguna clave en el repo | | |
| 2.2 | Variables de `.env.example` | | |
| 2.3 | Nada secreto en el cliente | | |
| 3.1 | Rutas relativas | | |
| 3.2 | Enlaces internos | | |
| 4.1 | Página 404 | | |
| 4.2 | HTTPS | | |
| 5.1 | CORS | | |
| 6.1 | `prefers-reduced-motion` | | |
| 7.1 | Límites y precios consultados | | |
| 7.2 | Versiones y comandos verificados | | |
| 8.1 | Nada publica solo | | |
| 8.2 | Comando de publicación escrito | | |

Los puntos que solo se pueden comprobar con el sitio ya publicado (3.2
desde la URL real, 4.2, el código 200 del paso 8 de la skill) se marcan
"pendiente: después de publicar" y se cierran en ese momento.
