# Inscripción a talleres (web estática)

HTML, CSS y JS sin build. Habla con Supabase usando `supabase-js` (cargado desde jsDelivr, versión fijada `2.117.2` con SRI) según `docs/contrato-api.md`. Pensada para el celular.

## Estructura

- `index.html`, `styles.css`, `app.js` (UI), `logic.js` (lógica pura, probada con node).
- `config.example.js`: plantilla de configuración. `config.js` (real) está en `.gitignore`.
- `scripts/generar-config.js`: genera `config.js` desde `.env`.
- `supabase/`: migración y seed (T1). `docs/`: modelo, contrato, pruebas RLS y pruebas de UI.

## Configurar las claves

Las claves públicas (`SUPABASE_URL`, `SUPABASE_ANON_KEY`) salen de `.env.example`:

```
cp .env.example .env        # completa los dos valores (panel de Supabase > Project Settings > API)
node scripts/generar-config.js
```

Esto crea `config.js`. Alternativa manual: copia `config.example.js` a `config.js` y completa los valores. Sin `config.js` válido, la página muestra el aviso "Falta la configuración" y no llama al backend. Nunca uses la clave `service_role` aquí.

## Probar en local

```
python -m http.server 8080    # desde esta carpeta; abre http://localhost:8080
node --test tests/logic.test.js   # pruebas de la lógica pura
```

Prueba en el celular real (misma red, `http://<IP-del-PC>:8080`): el emulador no reproduce teclado, zonas seguras ni toques.

## Publicar bajo un subpath (GitHub Pages)

Todas las rutas son relativas, así que funciona en `https://usuario.github.io/repo/`. `config.js` no se commitea: en el despliegue debe generarse en el paso de publicación (ver tarea de despliegue). La clave anon es pública por diseño; la protegen las políticas RLS de `supabase/`.

## Pruebas

Casos de UI y de lógica: `docs/pruebas-ui.md`. Casos de acceso a datos: `docs/pruebas-rls.md`.
