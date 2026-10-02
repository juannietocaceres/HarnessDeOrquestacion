# PLAN-MEJORA-SKILLS-2.md — Backend, despliegue y trabajo académico

> Segunda ampliación del harness. Continúa a `PLAN-MEJORA-SKILLS.md`
> (milestone `mejora-skills`, cerrado). Igual que el anterior, se ejecuta como
> un milestone del propio harness (Anexo A) con el prompt del Anexo B.

---

## 0. Por qué estas tres skills

Con 21 skills el harness está fuerte en frontend (11 skills entre
`frontend-design` y la suite de Emil) y débil en el resto. El objetivo del
harness es servir para **cualquier tipo de trabajo: apps, webs y proyectos
académicos**. Los huecos concretos son:

| Hueco | Qué pasa hoy | Skill nueva |
|---|---|---|
| API, base de datos, login | El sub-agente improvisa el stack y el modelo de datos en cada proyecto | `backend-datos` |
| Publicar lo construido | Un milestone termina con el código en `main`; nadie lo pone en internet | `despliegue` |
| Documentos de la universidad | No hay criterio para anteproyectos, informes, normas de citación ni referencias | `trabajo-academico` |

Con esto el harness queda en **24 skills**. No se agrega nada más en esta
ronda: otras áreas (seguridad avanzada, CI/CD, data science) se agregan solo
cuando un proyecto real las pida.

---

## 1. Estado de partida (lo que ya existe y hay que respetar)

- `orquestador` §0 (entrada desde una idea), §1 (manifest con `modelo:` y
  `verificacion_manual:` opcionales), §5 (paso 0: `git merge --ff-only main`
  en cada worktree), §8 (tabla de activación de skills).
- Tipos vigentes: `backend | frontend | data | cli | mobile | docs | testing | presentacion | contenido | otro`.
- `triage-proyecto` con `schema/triage.schema.json` y
  `scripts/preflight_manifest.py` (constante `TIPOS_VIGENTES`).
- `verificador-datos`, `optimizador-prompts` (`PLANTILLA-SUBAGENTE.md`),
  `optimizador-tokens` (umbral ~4.000), `especificacion`, `testing`,
  `revision-codigo`.
- Ejemplos reales en el repo que sirven de referencia:
  `schema/tareas.md` y `api/contrato-tareas.md` (salida de
  `panel-tareas-demo`), `landing/enigma-go/` y `presentaciones/` (salida de
  `e2e-skills`).
- El repo está publicado en GitHub (`PROCESO.md` §13). Todo lo que se
  escriba aquí es público.

**Antes de arrancar**: confirmar que los pendientes del milestone anterior
están cerrados (`.gitattributes` con LF para skills vendorizadas y
`milestones/enigma-go/estado.yaml` commiteado). Si no, cerrarlos primero
(ver Anexo B, paso 0).

---

## 2. Resumen de tareas

| # | Qué | Tipo de trabajo | Wave |
|---|---|---|---|
| N1 | Skill `backend-datos` | Skill nueva + plantillas | 1 |
| N2 | Skill `despliegue` | Skill nueva + checklist | 1 |
| N3 | Skill `trabajo-academico` | Skill nueva + plantillas + export a Word | 1 |
| N4 | Integración en `orquestador` y `triage-proyecto` | Cambios a skills existentes y scripts | 2 |
| N5 | Documentación del harness | `CLAUDE.md`, `RESUMEN-HARNESS.md`, `README.md`, `PROCESO.md` §15 | 3 |
| N6 | Validación de punta a punta | Corrida real con las 3 skills | 4 |

---

## 3. Reglas transversales

Se mantienen todas las de `PLAN-MEJORA-SKILLS.md` §3 (carpeta propia por
skill, `description` corta, español neutro con "tú", modo no interactivo
dentro de sub-agentes con `DECISION_NEEDED`, salidas a archivo, un commit
por tarea, decisiones de diseño en `PROCESO.md`). Además:

1. **Opciones gratis primero.** Toda recomendación de servicio (base de
   datos, hosting, auth) parte del plan gratuito. Si una necesidad solo se
   cubre pagando, eso es un `DECISION_NEEDED`, nunca una elección silenciosa.
2. **Datos que cambian se verifican, no se recuerdan.** Límites de planes
   gratuitos, precios, versiones y comandos de CLI cambian seguido. Las
   skills no los escriben como verdad fija: indican consultarlos en la
   documentación oficial vigente (con `verificador-datos` / búsqueda web) en
   el momento de usarlos, y anotar la fecha de consulta.
3. **Contrato entre N1 y N2 (corren en paralelo):** `backend-datos` deja la
   lista de variables de entorno del proyecto en **`.env.example`** (nombres
   y descripción, nunca valores reales). `despliegue` lee ese archivo para
   saber qué configurar en la plataforma. Ninguna de las dos escribe en la
   carpeta de la otra.
4. **Secretos.** Nunca se commitean claves, tokens ni contraseñas. `.env`
   va en `.gitignore` (ya está). Si un sub-agente necesita una credencial
   real, eso es `verificacion_manual` o bloqueo externo, no algo que se
   inventa ni se pide en el chat.
5. **Acciones con efecto fuera del repo** (publicar un sitio, crear una base
   de datos en la nube, enviar algo) requieren aprobación explícita en el
   batched gate. El sub-agente deja todo listo y devuelve `DECISION_NEEDED`
   con el comando exacto que se va a ejecutar.

---

## 4. Especificación por tarea

### N1 — `backend-datos`

**Objetivo**: que cualquier tarea que toque API, base de datos o login siga
un mismo criterio, en vez de improvisar.

**Contenido de la skill** (`.claude/skills/backend-datos/SKILL.md`):

1. **Elegir el stack** según el proyecto, con una tabla de decisión:

   | Caso | Opción por defecto (gratis) | Cuándo cambiar |
   |---|---|---|
   | App móvil Expo con login y datos en la nube | Supabase (Postgres + Auth) | Si el usuario ya usa Firebase o pide NoSQL |
   | Web con API propia | Node/Express o el backend del framework (rutas de API de Next, etc.) + Postgres | Si el proyecto académico exige otro lenguaje |
   | Proyecto chico, local o académico sin usuarios reales | SQLite | Si necesita varios usuarios a la vez o estar en internet |
   | Prototipo sin backend real | Datos mock en JSON | Nunca para algo que se va a publicar |

   Si el manifest ya fija el stack, se respeta. Si no lo fija y la elección
   tiene trade-offs reales para ese proyecto → `DECISION_NEEDED`.

2. **Modelo de datos primero**: entidades, campos con tipo, relaciones,
   restricciones (únicos, no nulos), índices necesarios. Plantilla en
   `PLANTILLA-MODELO-DATOS.md`. Ejemplo de referencia: `schema/tareas.md`.
3. **Contrato de API después**: endpoints, método, entrada, salida, códigos
   de error, autenticación requerida. Plantilla en
   `PLANTILLA-CONTRATO-API.md`. Ejemplo de referencia:
   `api/contrato-tareas.md`.
4. **Autenticación**: siempre con el proveedor (Supabase Auth, Firebase
   Auth, librería probada del framework). Prohibido escribir hashing de
   contraseñas o manejo de sesiones a mano.
5. **Seguridad mínima obligatoria**: validación de entrada en el servidor
   (nunca solo en el cliente), consultas parametrizadas, reglas de acceso
   por fila (RLS en Supabase / Security Rules en Firebase) activadas desde
   el primer día, CORS restringido, mensajes de error que no filtren
   detalles internos.
6. **Migraciones y datos de prueba**: el esquema se crea con migraciones
   versionadas en el repo (no a mano en un panel web), y hay un script de
   datos semilla para desarrollo.
7. **`.env.example`** con todas las variables (contrato con N2, §3.3).
8. **Pruebas**: se coordina con `testing` (tests de contrato de la API:
   cada endpoint del contrato tiene al menos un caso feliz y uno de error).

**Integración con el gate**: elegir stack con trade-offs, o cualquier
servicio que requiera plan pago → `DECISION_NEEDED`. Crear la base de datos
real en la nube → `verificacion_manual` (requiere la cuenta del usuario).

**Criterios de aceptación**:
- [ ] Skill + `PLANTILLA-MODELO-DATOS.md` + `PLANTILLA-CONTRATO-API.md` en `.claude/skills/backend-datos/`.
- [ ] Prueba de regresión: aplicando la skill a la descripción de T1 y T2 de `panel-tareas-demo`, el modelo y el contrato generados cubren lo mismo que `schema/tareas.md` y `api/contrato-tareas.md` (mismas entidades, endpoints y códigos de error, o diferencias justificadas).
- [ ] Prueba nueva: "app Expo con login y una lista de favoritos sincronizada" produce modelo, contrato, reglas RLS y `.env.example`, sin código de auth a mano.
- [ ] Pruebas documentadas en `milestones/mejora-skills-2/pruebas/backend-datos.md`.

---

### N2 — `despliegue`

**Objetivo**: que un milestone pueda terminar con el proyecto publicado,
usando opciones gratuitas, sin que el sub-agente toque cuentas del usuario
por su cuenta.

**Contenido de la skill** (`.claude/skills/despliegue/SKILL.md`):

1. **Elegir plataforma** con tabla de decisión (opciones gratis primero;
   límites vigentes se consultan al momento, §3.2):

   | Caso | Opción por defecto | Alternativa |
   |---|---|---|
   | Web estática (HTML/CSS/JS, landing, deck) | GitHub Pages (el repo ya está en GitHub) | Netlify |
   | Web con framework y funciones de servidor (Next, etc.) | Vercel | Netlify |
   | API propia | La que sugiera `backend-datos` para ese stack, con plan gratuito | — |
   | App Expo | Expo (Expo Go para pruebas; EAS para builds) | — |

2. **Checklist antes de publicar** (obligatorio, queda en el reporte):
   - El build de producción pasa en limpio.
   - Ninguna clave en el repo; todas las variables de `.env.example`
     configuradas en la plataforma.
   - URLs y rutas relativas correctas para el subdominio (problema típico
     de GitHub Pages con rutas absolutas).
   - Página 404 y HTTPS.
   - CORS de la API permite solo el dominio publicado.
   - Las animaciones respetan `prefers-reduced-motion` (si la tarea pasó
     por las skills de Emil, ya debería estar).
3. **Archivos de configuración en el repo**: workflow de GitHub Actions
   para Pages, `vercel.json`/`netlify.toml` si aplica, `app.json`/`eas.json`
   para Expo. Todo versionado.
4. **Publicar nunca es automático**: el sub-agente prepara todo y devuelve
   `DECISION_NEEDED` con la plataforma, la URL esperada y el comando o la
   acción exacta (§3.5). Solo después de la aprobación se ejecuta.
5. **Lo que requiere la cuenta del usuario** (login en Vercel, activar
   Pages en la configuración del repo, cuenta de Expo) va como
   `verificacion_manual` con instrucciones paso a paso, para que el usuario
   lo haga una vez.
6. **Después de publicar**: comprobar que la URL responde (código 200) y
   registrar la URL en el `README.md` del proyecto y en el `estado.yaml` del
   milestone.

**Criterios de aceptación**:
- [ ] Skill + `CHECKLIST-PUBLICAR.md` en `.claude/skills/despliegue/`.
- [ ] Prueba: preparar el despliegue de `landing/enigma-go/` en GitHub Pages (workflow, rutas, 404). La publicación real queda pendiente de aprobación en el gate.
- [ ] La skill no contiene límites de planes ni precios escritos como dato fijo.
- [ ] Prueba documentada en `milestones/mejora-skills-2/pruebas/despliegue.md`.

---

### N3 — `trabajo-academico`

**Objetivo**: que el harness sirva para proyectos de la universidad
(anteproyectos, informes, artículos, trabajo de grado) con estructura
correcta y **referencias reales**.

**Contenido de la skill** (`.claude/skills/trabajo-academico/SKILL.md`):

1. **Tipos de documento** con su estructura base (en
   `ESTRUCTURAS.md`):
   - Anteproyecto / propuesta: título, planteamiento del problema, pregunta
     de investigación, justificación, objetivos (general y específicos),
     marco teórico y estado del arte, metodología, cronograma, presupuesto,
     referencias.
   - Informe de taller o laboratorio: introducción, objetivos, marco
     teórico breve, procedimiento, resultados, análisis, conclusiones,
     referencias.
   - Artículo / paper: resumen y abstract con palabras clave, introducción,
     metodología, resultados, discusión, conclusiones, referencias.
   - Ensayo: tesis, argumentos, contraargumentos, conclusión.
   - Trabajo de grado: la estructura del anteproyecto ampliada con
     resultados, discusión y anexos.
2. **Lineamientos de la institución mandan.** Si existe
   `docs/academico/lineamientos.md` (guía del programa, modalidad de grado,
   formato exigido por el docente), tiene prioridad sobre todo lo de la
   skill. Si no existe y el documento es formal (anteproyecto, trabajo de
   grado), pedirlo como `DECISION_NEEDED` en vez de asumir.
3. **Norma de citación configurable**: APA 7 por defecto, ICONTEC
   (NTC 1486) como alternativa. La norma se fija por proyecto (campo en el
   manifest o en `lineamientos.md`), no se mezcla.
4. **Objetivos bien formulados**: un objetivo general y 3–5 específicos,
   cada uno con un verbo en infinitivo medible (taxonomía de Bloom), sin
   verbos vagos como "conocer" o "entender", y cada específico ligado a un
   entregable o actividad de la metodología.
5. **Referencias: regla dura contra inventarlas.**
   - Solo se incluyen fuentes que se pudieron verificar (DOI que resuelve,
     URL que existe, libro con ISBN). La verificación se hace con
     `verificador-datos` y búsqueda web.
   - Si no se encuentra fuente para una afirmación, se escribe
     `[CITA PENDIENTE: qué hace falta respaldar]` en el texto. Nunca una
     referencia aproximada o "probable".
   - Las referencias viven en `referencias.bib` (BibTeX) dentro de la
     carpeta del documento.
6. **Formato de trabajo y exportación**: se escribe en Markdown con citas
   tipo `[@clave]`. Export a Word con **pandoc** (gratis):
   `pandoc doc.md --citeproc --bibliography referencias.bib --csl apa.csl -o doc.docx`.
   El archivo `apa.csl` se toma del repositorio oficial de estilos CSL
   (citation-style-language/styles). Para ICONTEC, usar un CSL solo si se
   encuentra uno confiable; si no, checklist de formato manual.
   Si pandoc no está instalado, la skill da el comando de instalación y
   entrega el Markdown igual.
7. **Integridad académica**: la skill estructura, redacta borradores y
   verifica fuentes, pero el contenido final lo revisa y asume el
   estudiante. El reporte de la tarea lista qué secciones son borrador para
   revisión humana (`verificacion_manual`).
8. **Salida**: `academico/<slug>/documento.md`, `referencias.bib`,
   `documento.docx` si hay pandoc, y el informe de `verificador-datos` sobre
   las referencias.

**Criterios de aceptación**:
- [ ] Skill + `ESTRUCTURAS.md` + `CHECKLIST-APA7.md` en `.claude/skills/trabajo-academico/`.
- [ ] Prueba: esqueleto de anteproyecto para el tema "modelo predictivo de IA para identificar zonas de riesgo de propagación del dengue en Santiago de Cali por comuna, con datos epidemiológicos y climáticos" (tema del trabajo de grado; cambiarlo si no se quiere en el repo público). Debe incluir: planteamiento, pregunta, objetivos según el punto 4, estructura de metodología y **al menos 5 referencias verificadas** (con DOI o URL comprobada).
- [ ] `verificador-datos` sobre esas referencias: 0 incorrectas, 0 inventadas.
- [ ] Si hay pandoc en el equipo, se genera el `.docx`; si no, queda documentado el comando.
- [ ] Prueba documentada en `milestones/mejora-skills-2/pruebas/trabajo-academico.md`.

---

### N4 — Integración en `orquestador` y `triage-proyecto`

Depende de N1, N2 y N3.

1. **Tipos nuevos** en `orquestador` §1: `devops` (despliegue e
   infraestructura) y `academico` (documentos universitarios). Actualizar en
   el mismo commit:
   - `TIPOS_VIGENTES` en `triage-proyecto/scripts/preflight_manifest.py`.
   - Los `enum` de `tipos_requeridos` y `dominio` en
     `triage-proyecto/schema/triage.schema.json` (añadir `academico` como
     dominio).
   - La lista de tipos y dominios en `triage-proyecto/SKILL.md`.
   - Los tests de `triage-proyecto/scripts/test_scripts.py` (casos con los
     tipos nuevos).
2. **Campo opcional `norma_citacion:`** por tarea (`apa7 | icontec`), usado
   por `trabajo-academico`. Opcional: los manifests existentes siguen
   pasando.
3. **Filas nuevas en §8**:

   | Momento | Condición | Skill |
   |---|---|---|
   | Antes de implementar | La tarea crea o cambia API, base de datos o login | `backend-datos` (modelo y contrato antes del código) |
   | Durante la implementación | `tipo: backend`, o una tarea `mobile`/`frontend` que necesita datos persistentes | `backend-datos` |
   | Durante la implementación | `tipo: devops`, o el milestone pide publicar | `despliegue` |
   | Antes de ejecutar una publicación | Siempre | Batched gate (`DECISION_NEEDED` con comando exacto) |
   | Durante la implementación | `tipo: academico` | `trabajo-academico` |
   | Antes de reportarse COMPLETADA | `tipo: academico` | `verificador-datos` sobre todas las referencias |

4. **Triage**: cuando la idea es un trabajo de la universidad, clasificar
   con dominio `academico` y preguntar (dentro del máximo de 3) por la
   norma de citación y si hay lineamientos del docente o del programa.

**Criterios de aceptación**:
- [ ] Los 4 manifests existentes (`panel-tareas-demo`, `enigma-go`, `mejora-skills`, `e2e-skills`) siguen pasando `preflight_manifest.py`.
- [ ] `test_scripts.py` de `triage-proyecto` y de `optimizador-tokens` pasan.
- [ ] La tabla §8 solo nombra skills que existen.

---

### N5 — Documentación

- `CLAUDE.md` y `README.md`: conteo a 24 skills y filas nuevas en la tabla.
- `RESUMEN-HARNESS.md`: tabla de skills y diagrama con `despliegue` al
  final del flujo (publicación aprobada en el gate).
- `PROCESO.md` **§15 Backend, despliegue y académico**: por qué estas tres
  y no otras, el contrato `.env.example`, la regla de "publicar nunca es
  automático", la regla de referencias verificadas, decisiones del gate y
  resultados de las pruebas.
- Correr `verificador-datos` sobre los cuatro archivos al final.

---

### N6 — Validación de punta a punta

Corrida real, igual que `e2e-skills`, en la sesión principal (el triage
tiene que poder preguntar y el gate tiene que llegar al usuario):

1. Idea de entrada: *"Una web para que los estudiantes se inscriban a un
   taller de la universidad, con login, los inscritos guardados en una base
   de datos, publicada gratis, y un informe corto en APA que explique el
   proyecto."*
2. Esperado:
   - `triage-proyecto` clasifica como `mixto` y genera un manifest con
     tareas `backend`, `frontend`, `devops` y `academico`.
   - La tarea backend aplica `backend-datos` (modelo, contrato, RLS,
     `.env.example`).
   - La tarea devops aplica `despliegue` y **para en el gate** pidiendo
     autorización para publicar, con el comando exacto.
   - La tarea académica aplica `trabajo-academico` y pasa `verificador-datos`
     con 0 referencias inventadas.
   - Las acciones que requieren cuenta (crear proyecto en Supabase, activar
     Pages) aparecen en el checklist manual de la wave.
3. Resultado en `milestones/e2e-skills-2/` y resumen en `PROCESO.md` §15.

---

## 5. Orden de ejecución

| Wave | Tareas | Por qué |
|---|---|---|
| 1 | N1, N2, N3 | Independientes; cada una toca solo su carpeta. N1 y N2 se coordinan por el contrato `.env.example` (§3.3) |
| 2 | N4 | Necesita las tres skills para referenciarlas y para definir los tipos nuevos |
| 3 | N5 | Documenta lo ya integrado |
| 4 | N6 | Valida el sistema completo |

---

## 6. Riesgos

| Riesgo | Mitigación |
|---|---|
| Datos de planes gratuitos desactualizados | Regla §3.2: se consultan al usarse, con fecha |
| Referencias académicas inventadas | Regla dura de N3 punto 5 + `verificador-datos` obligatorio en `tipo: academico` |
| Publicar algo por error | Publicar requiere aprobación en el gate con el comando exacto (§3.5) |
| Secretos en el repo público | `.env.example` sin valores, `.env` ignorado, revisión en `revision-codigo` |
| N1 y N2 asumen cosas distintas en paralelo | Contrato `.env.example` fijado en este plan antes de arrancar |
| Romper los manifests existentes con los tipos nuevos | Criterio de N4: los 4 manifests pasan el preflight |

---

## 7. Decisiones abiertas (para el batched gate)

1. **Backend por defecto para apps**: ¿Supabase (Postgres, SQL, útil para
   aprender bases relacionales) o Firebase (NoSQL)? *Propuesta: Supabase.*
2. **Hosting por defecto para webs estáticas**: ¿GitHub Pages (el repo ya
   está en GitHub) o Vercel/Netlify? *Propuesta: GitHub Pages para
   estáticas, Vercel para frameworks con funciones de servidor.*
3. **Norma de citación por defecto**: ¿APA 7 o ICONTEC? Depende de lo que
   exija el programa en la UCC. *Propuesta: APA 7 por defecto, cambiable
   por proyecto.*
4. **Skills de documentos de Anthropic** (`docx`, `pdf` del repositorio
   `anthropics/skills`): ¿vale la pena vendorizarlas para entregables en
   Word? N3 revisa su licencia y reporta; no se copian si la licencia no lo
   permite. *Propuesta: decidir después de ver el reporte de N3; pandoc
   cubre lo básico gratis.*
5. **Publicación real en N2 y N6**: ¿se autoriza publicar la landing de
   Enigma Go y la web del taller en GitHub Pages, o solo se deja preparado?

---

## Anexo A — Manifest del milestone `mejora-skills-2`

Guardar como `milestones/mejora-skills-2/milestone.yaml`:

```yaml
milestone: "Backend, despliegue y trabajo académico"
cap_concurrencia: 3
tareas:
  - id: N1
    titulo: "Skill backend-datos"
    tipo: docs
    depende_de: []
    descripcion: >
      Crear .claude/skills/backend-datos/ con SKILL.md, PLANTILLA-MODELO-DATOS.md
      y PLANTILLA-CONTRATO-API.md según PLAN-MEJORA-SKILLS-2.md §4 N1. Respetar
      el contrato .env.example de §3.3.
    criterios_aceptacion:
      - "Existen SKILL.md y las dos plantillas con frontmatter válido"
      - "Regresión contra schema/tareas.md y api/contrato-tareas.md documentada"
      - "Prueba 'app Expo con login y favoritos' con modelo, contrato, RLS y .env.example, sin auth a mano"
      - "Pruebas en milestones/mejora-skills-2/pruebas/backend-datos.md"
  - id: N2
    titulo: "Skill despliegue"
    tipo: docs
    depende_de: []
    descripcion: >
      Crear .claude/skills/despliegue/ con SKILL.md y CHECKLIST-PUBLICAR.md según
      §4 N2. Lee .env.example (contrato §3.3). Publicar nunca es automático.
    criterios_aceptacion:
      - "Existen SKILL.md y CHECKLIST-PUBLICAR.md"
      - "Despliegue de landing/enigma-go/ a GitHub Pages preparado (workflow, rutas, 404)"
      - "Ningún límite de plan ni precio escrito como dato fijo"
      - "Prueba en milestones/mejora-skills-2/pruebas/despliegue.md"
    verificacion_manual:
      - "Activar GitHub Pages en la configuración del repositorio si la publicación se aprueba"
  - id: N3
    titulo: "Skill trabajo-academico"
    tipo: docs
    depende_de: []
    descripcion: >
      Crear .claude/skills/trabajo-academico/ con SKILL.md, ESTRUCTURAS.md y
      CHECKLIST-APA7.md según §4 N3. Revisar la licencia de las skills docx y pdf
      de anthropics/skills y reportarla para la decisión §7.4.
    criterios_aceptacion:
      - "Existen SKILL.md, ESTRUCTURAS.md y CHECKLIST-APA7.md"
      - "Esqueleto de anteproyecto de prueba con objetivos según §4 N3 punto 4"
      - "Al menos 5 referencias verificadas con DOI o URL comprobada"
      - "verificador-datos sobre las referencias: 0 incorrectas, 0 inventadas"
      - "Prueba en milestones/mejora-skills-2/pruebas/trabajo-academico.md"
    verificacion_manual:
      - "Revisar que el esqueleto del anteproyecto tenga sentido para el tema y el programa"
  - id: N4
    titulo: "Integrar en orquestador y triage-proyecto"
    tipo: docs
    depende_de: [N1, N2, N3]
    descripcion: >
      Aplicar §4 N4: tipos devops y academico, campo norma_citacion, filas nuevas
      en orquestador §8, actualización de preflight_manifest.py, triage.schema.json,
      triage-proyecto/SKILL.md y tests.
    criterios_aceptacion:
      - "Los 4 manifests existentes pasan preflight_manifest.py"
      - "test_scripts.py de triage-proyecto y optimizador-tokens pasan"
      - "La tabla §8 solo nombra skills existentes"
  - id: N5
    titulo: "Actualizar documentación"
    tipo: docs
    depende_de: [N4]
    modelo: sonnet
    descripcion: >
      Actualizar CLAUDE.md, README.md, RESUMEN-HARNESS.md y escribir PROCESO.md §15
      según §4 N5.
    criterios_aceptacion:
      - "Conteo de 24 skills correcto en los cuatro archivos"
      - "verificador-datos sobre los cuatro archivos sin afirmaciones incorrectas"
  - id: N6
    titulo: "Validación de punta a punta"
    tipo: testing
    depende_de: [N5]
    descripcion: >
      Correr el escenario de §4 N6 de forma real en la sesión principal y
      documentarlo en milestones/e2e-skills-2/.
    criterios_aceptacion:
      - "milestones/e2e-skills-2/ con triage, manifest, estado, decisiones y artefactos"
      - "backend-datos, despliegue y trabajo-academico usadas al menos una vez"
      - "La publicación pasó por el batched gate con el comando exacto"
    verificacion_manual:
      - "Abrir la web publicada (si se aprobó publicar) desde el celular y probar la inscripción"
```

---

## Anexo B — Prompt para pegar en Claude Code

```
Lee PLAN-MEJORA-SKILLS-2.md completo. Después lee CLAUDE.md,
.claude/skills/orquestador/SKILL.md y PROCESO.md §14.

0. Antes de nada, revisa que los pendientes del milestone mejora-skills
   estén cerrados: .gitattributes con LF para las skills vendorizadas y
   milestones/enigma-go/estado.yaml commiteado. Si falta alguno, ciérralo
   con su propio commit y no toques .claude/worktrees/.
1. Crea milestones/mejora-skills-2/milestone.yaml con el contenido del
   Anexo A.
2. Ejecútalo con /orquestador siguiendo sus reglas (preflight, waves,
   worktrees con paso 0, cap 3, batched gate por wave, campo modelo).
3. Cada sub-agente recibe como referencia la sección §4 de su tarea y las
   reglas de §3.
4. Las decisiones abiertas de §7 entran al batched gate de la wave donde
   aparezcan. No elijas por defecto. Nada se publica en internet sin mi
   aprobación explícita en el gate.
5. Al terminar, muéstrame: tareas completadas, decisiones tomadas,
   verificaciones manuales pendientes y cualquier contradicción encontrada
   entre skills.
```
