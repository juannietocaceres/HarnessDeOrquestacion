---
name: backend-datos
description: Define el stack, el modelo de datos, el contrato de API, la autenticación con proveedor, las reglas de acceso y el `.env.example` antes de escribir código de backend. Úsala en cualquier tarea que cree o cambie una API, una base de datos o un login.
---

# Backend y datos

Haces que toda tarea que toque API, base de datos o login siga el mismo
orden: **stack → modelo de datos → contrato de API → auth → seguridad →
migraciones → `.env.example` → pruebas de contrato**. El código va después
de los dos documentos (modelo y contrato), nunca antes.

## Dos modos de uso

- **Suelta** (el usuario te la pide directamente): si una elección tiene
  trade-offs reales (stack, servicio pago), pregúntale antes de seguir.
- **Dentro de un milestone** (sub-agente del `orquestador`): **nunca le
  preguntas nada al usuario**. Asumes lo razonable, listas los supuestos en
  tu reporte y, si un supuesto es de alto impacto (los casos de
  "Integración con el gate"), devuelves `DECISION_NEEDED` con el formato
  del `orquestador` §6 y no commiteas lo que dependa de la respuesta.

## Regla de datos cambiantes

Límites de planes gratuitos, precios, versiones de librerías y comandos de
CLI cambian seguido. Esta skill **no** los da como dato fijo. Cuando tu
decisión dependa de uno de ellos (por ejemplo, "¿cabe en el plan
gratuito?"), consúltalo en la documentación oficial vigente en ese momento
(búsqueda web o `verificador-datos`) y anota en el documento la URL y la
fecha de consulta (campo `fuentes_consultadas` de las plantillas). Si no
tienes acceso web, déjalo marcado como "por verificar" y súmalo a
`verificacion_manual`.

---

## 1. Elegir el stack

Si el manifest, la spec o el proyecto ya fijan el stack, **se respeta** y
saltas este paso. Si no, parte de esta tabla (siempre desde la opción
gratuita):

| Caso | Opción por defecto (plan gratuito) | Cuándo cambiar |
|---|---|---|
| App móvil Expo con login y datos en la nube | **Supabase** (Postgres + Supabase Auth) | Si el usuario ya usa Firebase o pide NoSQL → Firebase (Firestore + Firebase Auth) |
| Web con API propia | Node/Express o el backend del framework (rutas de API de Next, etc.) + Postgres | Si el proyecto académico exige otro lenguaje |
| Proyecto chico, local o académico sin usuarios reales | SQLite | Si necesita varios usuarios a la vez o estar en internet |
| Prototipo sin backend real | Datos mock en JSON | Nunca para algo que se va a publicar |

La fila de apps móviles es la única que elige un proveedor administrado.
Las equivalencias entre Supabase y Firebase están en "Equivalencias por
proveedor", al final, para que el cambio de opción sea de una fila.

Devuelves `DECISION_NEEDED` (no eliges en silencio) cuando:

- El proyecto no fija el stack **y** hay un trade-off real para ese
  proyecto (por ejemplo, el equipo ya conoce Firebase, o el curso pide SQL).
- La necesidad solo se cubre con un plan pago, o no puedes confirmar que
  el plan gratuito alcanza.

## 2. Modelo de datos primero

Antes de cualquier endpoint, escribe el modelo con
[`PLANTILLA-MODELO-DATOS.md`](PLANTILLA-MODELO-DATOS.md): entidades, campos
con tipo, requerido, valor por defecto, quién asigna cada campo (cliente o
servidor), restricciones (únicos, no nulos, enums, longitudes), relaciones
con su acción al borrar, índices y quién es dueño de cada fila.

- Solo los campos que piden los criterios de aceptación. Lo demás queda
  como "fuera de alcance", con nota de cuándo se decidiría.
- Cada restricción del modelo se traduce a una restricción en la base
  (`not null`, `unique`, `check`) además de la validación en el servidor:
  la base es la última línea de defensa.
- Ejemplo de referencia en este repo: `schema/tareas.md`.

## 3. Contrato de API después

Con el modelo cerrado, escribe el contrato con
[`PLANTILLA-CONTRATO-API.md`](PLANTILLA-CONTRATO-API.md): por endpoint (u
operación), método, ruta, autenticación requerida, entrada con
validaciones, salida y cada código de error con su payload.

- Los campos que asigna el servidor (`id`, fechas, dueño) nunca se aceptan
  del cliente.
- Un formato de error único para todo el contrato.
- Si el cliente habla directo con el proveedor (Supabase desde la app, sin
  servidor propio), el contrato documenta las **operaciones** que hace el
  cliente (tabla, filtro, columnas) y qué devuelve cada una cuando la regla
  de acceso o una restricción la rechaza. Sigue siendo un contrato: la UI
  se construye contra él.
- Ejemplo de referencia en este repo: `api/contrato-tareas.md`.

## 4. Autenticación: siempre con el proveedor

Usa el sistema de auth del proveedor (Supabase Auth, Firebase Auth) o una
librería probada del framework. **Prohibido** escribir a mano:

- hashing o comparación de contraseñas;
- generación, firma o validación de tokens/sesiones;
- tablas propias de usuarios con columna de contraseña.

El modelo de datos referencia al usuario del proveedor (por ejemplo,
`auth.users.id` en Supabase o el `uid` en Firebase); no lo duplica. Si la
tarea pide algo que el proveedor no cubre, es `DECISION_NEEDED`, no código
de auth propio.

## 5. Seguridad mínima obligatoria

Checklist que va en el reporte de la tarea, punto por punto:

- [ ] Validación de entrada **en el servidor** (o en la base, con `check` y
      reglas de acceso, si no hay servidor propio). La del cliente es solo UX.
- [ ] Consultas parametrizadas o el cliente/ORM del proveedor; nunca SQL
      armado concatenando texto del usuario.
- [ ] Reglas de acceso por fila activadas **desde la primera migración**:
      RLS en Supabase/Postgres, Security Rules en Firebase. Ninguna tabla
      expuesta queda sin reglas.
- [ ] CORS restringido a los orígenes conocidos (nunca `*` en producción),
      si hay API propia.
- [ ] Errores sin detalles internos: ni stack traces, ni SQL, ni nombres de
      tablas internas. El detalle va al log del servidor.
- [ ] Ninguna clave secreta en el cliente ni en el repo (ver paso 7).

## 6. Migraciones y datos de prueba

- El esquema se crea con **migraciones versionadas en el repo**, nunca a
  mano en el panel web del proveedor. Usa la herramienta del stack (CLI de
  Supabase, el ORM del framework, archivos `.sql` numerados para SQLite).
  Consulta los comandos exactos en la doc oficial al usarlos (regla de
  datos cambiantes).
- La migración que crea una tabla también activa sus reglas de acceso y
  crea sus políticas.
- Un script de **datos semilla** para desarrollo, con datos ficticios
  (nunca datos reales de personas). Si depende de usuarios de auth, los
  crea por el mecanismo del proveedor o lo documenta como paso manual.

## 7. `.env.example` (contrato con `despliegue`)

Toda variable de entorno que el proyecto necesita queda en `.env.example`
en la raíz del proyecto. La skill `despliegue` lee este archivo para saber
qué configurar en la plataforma; ninguna de las dos escribe en la carpeta
de la otra.

Formato (una variable por bloque, valor siempre vacío):

```dotenv
# <Descripción en una línea>. Ámbito: cliente | servidor. Sensible: no | sí.
# Dónde se obtiene: <panel o comando del proveedor, sin valores>.
NOMBRE_VARIABLE=
```

Reglas:

- **Nunca valores reales** — ni claves, ni URLs de proyectos reales, ni
  "ejemplos" que parezcan reales. El valor va vacío.
- `Ámbito: cliente` significa que la variable termina dentro de la app o
  del bundle web (por ejemplo, el prefijo `EXPO_PUBLIC_` en Expo o
  `NEXT_PUBLIC_` en Next): **solo** valores pensados para ser públicos
  (URL del proyecto, clave publicable/anon). Una clave que salta las reglas
  de acceso (secret/service role, cuenta de servicio) es siempre
  `Ámbito: servidor` y `Sensible: sí`, y nunca lleva prefijo público.
- `.env` (con los valores reales) va en `.gitignore`. Comprueba además que
  `.gitignore` **no ignore `.env.example`**: un patrón como `.env.*` lo
  ignora; agrega `!.env.example` debajo o avisa en el reporte si el archivo
  queda fuera de tu alcance.
- Si una tarea agrega o quita una variable, actualiza `.env.example` en el
  mismo commit.

## 8. Pruebas de contrato (con `testing`)

Aplica `testing` (fila "Backend / API"). Mínimo obligatorio: **cada
endpoint u operación del contrato tiene al menos un caso feliz y uno de
error**, y cada código de error del contrato está cubierto por algún caso.
Si un endpoint no tiene ningún error de negocio en el contrato (un listado
público sin parámetros, por ejemplo), su "caso de error" es el caso borde
principal (lista vacía) y el contrato lo dice explícitamente; no inventes
un error para cumplir la regla. Además, para cada regla de acceso por fila:

- el dueño puede leer/escribir sus filas;
- otro usuario autenticado **no** ve ni modifica las filas ajenas;
- un cliente sin sesión es rechazado.

Las pruebas corren contra una base real de prueba (local o de test), no
contra un mock del proveedor: el objetivo es atrapar errores de
integración y de reglas de acceso. La lista de casos va al final del
contrato (sección "Pruebas de contrato" de la plantilla).

---

## Integración con el gate

| Situación | Qué haces |
|---|---|
| Stack no fijado y con trade-offs reales | `DECISION_NEEDED` con las opciones y qué cambia en cada una |
| La necesidad requiere plan pago, o no puedes confirmar que el gratuito alcanza | `DECISION_NEEDED`; nunca eliges el pago en silencio |
| Crear el proyecto o la base de datos real en la nube, configurar el proveedor de auth, copiar claves a `.env` | `verificacion_manual` con pasos concretos (requiere la cuenta del usuario). Tú dejas listas las migraciones y el `.env.example` |
| Aplicar migraciones a una base en la nube | Acción fuera del repo: `DECISION_NEEDED` con el comando exacto, solo después de aprobada |
| Necesitas una credencial real para probar | No la inventes ni la pidas en el chat: `verificacion_manual` o bloqueo externo; prueba contra una base local |

## Salidas

Todo a archivo; en el chat, solo el resumen y las rutas. Si el proyecto ya
tiene convención de carpetas, la respetas. Si no:

| Artefacto | Ruta por defecto |
|---|---|
| Modelo de datos | `schema/<recurso>.md` |
| Contrato de API | `api/contrato-<recurso>.md` |
| Migraciones | la carpeta que use la herramienta del stack (por ejemplo, `supabase/migrations/`) |
| Datos semilla | la que use la herramienta del stack (por ejemplo, `supabase/seed.sql`) |
| Variables de entorno | `.env.example` en la raíz |
| Pruebas de contrato | la convención de pruebas del proyecto (ver `testing`) |

El reporte de la tarea incluye: stack elegido y por qué (o la decisión del
gate), rutas de los artefactos, el checklist de seguridad del paso 5, las
variables nuevas de `.env.example` y las `verificacion_manual` pendientes.

---

## Equivalencias por proveedor

Para que cambiar de proveedor sea un ajuste acotado, cada paso tiene su
equivalente:

| Paso | Supabase | Firebase |
|---|---|---|
| Modelo de datos | Tablas Postgres con tipos, `not null`, `unique`, `check`, claves foráneas | Colecciones y documentos de Firestore; tipos y restricciones se validan en las Security Rules |
| Contrato | Operaciones con `supabase-js` sobre tablas (o API REST generada) | Operaciones con el SDK de Firestore sobre colecciones |
| Auth | Supabase Auth; el dueño es `auth.uid()` | Firebase Auth; el dueño es `request.auth.uid` |
| Reglas de acceso | `enable row level security` + políticas por operación en la migración | `firestore.rules` versionado en el repo |
| Unicidad | Índice `unique` en la base | No hay `unique` nativo por campo: usar el valor único como id del documento (o una colección auxiliar cuyo id es ese valor) |
| Migraciones | Archivos SQL de la CLI de Supabase | Reglas e índices versionados (`firestore.rules`, `firestore.indexes.json`); los datos no tienen esquema |
| Semilla | Script SQL de semilla | Script con el emulador de Firebase |
| Pruebas de reglas | Base local con dos usuarios de prueba | Emulador de Firebase con dos usuarios de prueba |
| Variables cliente | URL del proyecto + clave publicable (o `anon`) | Configuración web/app de Firebase (api key, project id, app id) |
| Variables servidor | Clave secreta / service role | Credenciales de cuenta de servicio |

Los nombres de claves, paquetes y comandos de cada proveedor se confirman
en su documentación oficial al usarlos (regla de datos cambiantes).
