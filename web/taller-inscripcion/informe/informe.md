---
title: "Aplicación web de inscripción a talleres con control de acceso por fila"
author: "[POR COMPLETAR: estudiante]"
date: "[POR COMPLETAR]"
lang: es
bibliography: referencias.bib
csl: apa.csl
---

> BORRADOR para revisión humana. Informe corto de clase, estructura genérica de la skill `trabajo-academico` (informe de taller). No hay lineamientos del docente: el formato institucional (portada, curso, docente) es un supuesto. Norma APA 7. El proyecto no se ha publicado, por lo que no hay datos de uso.

# Introducción

Este informe describe una aplicación web para que estudiantes de la universidad se inscriban a un taller. La aplicación es estática (HTML, CSS y JavaScript sin proceso de compilación), usa Supabase Auth para el inicio de sesión y guarda los datos en una base Postgres de Supabase protegida con políticas de seguridad por fila (RLS). El informe expone el problema, los objetivos, la solución (arquitectura, modelo de datos y seguridad), la metodología y las conclusiones. La interfaz se construyó en paralelo a la base de datos; aquí se describe solo a través del contrato de operaciones que consume (`docs/contrato-api.md`), sin detallar su aspecto. [POR COMPLETAR: curso y contexto del taller para el que se hace el informe.]

# Planteamiento del problema

Inscribir estudiantes a un taller con hojas de cálculo o mensajes sueltos expone dos riesgos: que se sobrepase el cupo y que unas personas vean o modifiquen los datos de otras. [CITA PENDIENTE: evidencia sobre problemas de inscripción manual en talleres universitarios; el proyecto no la recopiló.] El segundo riesgo corresponde a una categoría reconocida: el control de acceso defectuoso ocupa el primer lugar (A01) del OWASP Top 10 de 2021 [@owasp-a01]. Hace falta, entonces, un sistema de inscripción donde cada estudiante vea, cree y cancele solo su inscripción, y donde el cupo se respete aunque dos personas se inscriban al mismo tiempo.

# Objetivos

**Objetivo general.** Construir una aplicación web de inscripción a talleres en la que cada estudiante autenticado gestione únicamente su propia inscripción y el cupo de cada taller no se exceda.

**Objetivos específicos.**

1. Diseñar un modelo de datos con dos entidades (`talleres` e `inscripciones`), con sus relaciones, restricciones e índices, documentado en `docs/modelo-datos.md`.
2. Implementar en la base de datos cuatro políticas RLS que cubran la lectura de talleres y la lectura, creación y cancelación de inscripciones propias, mediante una migración SQL versionada.
3. Validar las políticas y el control de cupo con 14 casos de prueba (R1 a R14) definidos en `docs/pruebas-rls.md`; criterio de éxito: los 14 casos dan el resultado previsto. [POR COMPLETAR: resultado de la ejecución; todavía no se registra.]
4. Especificar el contrato de ocho operaciones del cliente (registro, inicio y cierre de sesión, listado de talleres, cupos disponibles, mis inscripciones, inscripción y cancelación) en `docs/contrato-api.md`.
5. Preparar la publicación en GitHub Pages con disparo manual, de modo que nada se publique sin aprobación.

| Objetivo | Actividad | Entregable |
|---|---|---|
| Específico 1 | Modelado de entidades y restricciones | `docs/modelo-datos.md` |
| Específico 2 | Escritura de la migración con RLS y permisos | `supabase/migrations/20261005000000_crear_talleres_inscripciones.sql` |
| Específico 3 | Diseño de casos de prueba con dos usuarios | `docs/pruebas-rls.md` |
| Específico 4 | Definición de operaciones del cliente | `docs/contrato-api.md` |
| Específico 5 | Configuración del flujo de publicación | [POR COMPLETAR: archivo del flujo de publicación] |

# Solución

## Arquitectura

El navegador carga una página estática y se comunica directamente con Supabase mediante su biblioteca cliente (`supabase-js`), con la clave pública (anon) y la sesión del usuario. No hay servidor propio: la autenticación y la autorización las resuelve Supabase. El registro y el inicio de sesión usan correo y contraseña de Supabase Auth, con las funciones `signUp()` y `signInWithPassword()` [@supabase-auth]. La aplicación no guarda contraseñas ni genera tokens propios. La publicación está preparada para GitHub Pages con un flujo personalizado de GitHub Actions, que la documentación de GitHub permite ejecutar manualmente desde la pestaña Actions [@github-pages]; así, solo se publica cuando alguien lo dispara.

## Modelo de datos

La tabla `talleres` guarda título, descripción, fecha de inicio (UTC), cupo (entre 1 y 1000) y fecha de creación; no tiene dueño y el cliente solo la lee. La tabla `inscripciones` guarda el taller elegido (`taller_id`), el nombre con que se inscribe (1 a 100 caracteres) y el dueño (`user_id`), que referencia a `auth.users`; el servidor asigna `id`, `user_id` y `creado_en`. Ambas claves foráneas borran en cascada. Una restricción única sobre `(user_id, taller_id)` impide inscribirse dos veces al mismo taller, y un índice sobre `taller_id` agiliza el conteo de cupo.

## Seguridad

La seguridad descansa en la base de datos y no en el cliente. Según la documentación de PostgreSQL, una tabla sin políticas deja todas sus filas disponibles a quien tenga privilegios sobre ella, y con la seguridad por fila habilitada y sin políticas rige una política de denegación por defecto [@postgres-rls]. Supabase indica habilitar RLS en toda tabla de un esquema expuesto y distingue los roles `anon` (sin sesión) y `authenticated` (con sesión), que las políticas pueden usar mediante `auth.uid()` [@supabase-rls]. Este principio coincide con la recomendación de OWASP de denegar por defecto, salvo para recursos públicos [@owasp-a01].

La migración aplica ese enfoque con cuatro políticas: los autenticados leen todos los talleres; cada estudiante lee, crea y cancela solo las inscripciones cuyo `user_id` es el suyo. No hay política de actualización, de modo que las inscripciones no se editan. Además, se revocan los permisos del rol anónimo, se retiran los de escritura sobre `talleres` y se concede a los autenticados solo la inserción de las columnas `taller_id` y `nombre`; por eso un intento de enviar `user_id`, `id` o `creado_en` falla con el código `42501`. La lista completa de inscritos no se expone en la web: el organizador la consulta en el panel de Supabase.

El cupo se valida con un disparador (*trigger*) previo a la inserción, definido con `SECURITY DEFINER` porque debe contar las inscripciones de todos los estudiantes, que RLS oculta al cliente. El disparador bloquea la fila del taller (`for update`) para evitar que dos inscripciones simultáneas superen el cupo, y rechaza la inscripción con el error `taller_lleno` si el taller está lleno. Una función `cupos_disponibles` permite mostrar las plazas libres sin revelar filas ajenas.

# Metodología

El trabajo siguió un enfoque de diseño primero: (a) se modeló el recurso y sus reglas de acceso en un documento; (b) se escribió la migración SQL que las implementa; (c) se definió el contrato de operaciones del cliente; y (d) se diseñaron pruebas de RLS con dos usuarios de prueba, A y B, contra una base local (`supabase start`) y con la clave anon, sin simulaciones. Los casos cubren lo permitido (por ejemplo, A crea y lista su inscripción), lo negado (B no ve ni borra la inscripción de A; nadie edita; no se duplica; no se supera el cupo) y el acceso sin sesión. [POR COMPLETAR: fecha y resultado de la primera ejecución de las pruebas.]

# Conclusiones

1. Objetivo 1: el modelo de dos entidades con restricciones de unicidad, claves foráneas y comprobaciones quedó documentado y se materializa en la migración.
2. Objetivo 2: las políticas RLS y los permisos por columna están escritos en la migración; que cumplan su propósito se confirma con la ejecución de las pruebas. [POR COMPLETAR]
3. Objetivo 3: se definieron los 14 casos de prueba; su ejecución y el conteo de aprobados quedan pendientes. [POR COMPLETAR]
4. Objetivo 4: el contrato describe las ocho operaciones y sus errores esperados, y sirve de referencia común para la interfaz y las pruebas.
5. Objetivo 5: la publicación está preparada con disparo manual; no se ha publicado y no hay datos de uso. [POR COMPLETAR: confirmar tras la aprobación de la publicación.]

Limitaciones: no hay edición de inscripciones, lista de espera ni confirmación por correo, y el organizador depende del panel de Supabase. Trabajo futuro: ejecutar las pruebas y documentar el resultado.

# Referencias

::: {#refs}
:::

# Exportación a Word

Con pandoc instalado (no lo estaba al generar este borrador):

```
pandoc informe.md --citeproc --bibliography referencias.bib --csl apa.csl -o informe.docx
```

Instalación en Windows: `winget install --source winget --exact --id JohnMacFarlane.Pandoc` (confirmar en https://pandoc.org/installing.html). El estilo se descarga con
`curl -o apa.csl https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl`.
