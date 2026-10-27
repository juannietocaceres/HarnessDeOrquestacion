---
name: analisis-datos
description: Lleva un conjunto de datos (CSV, Excel, Parquet, JSON o una consulta) desde la pregunta hasta las conclusiones — perfilado, limpieza con bitácora, análisis con incertidumbre, gráficos que dicen una sola cosa y un informe en forma de historia donde cada cifra es trazable al código. Úsala cuando haya que explorar, limpiar, analizar o graficar datos, sacar conclusiones o contar una historia con ellos, o en tareas `tipo: data` que terminan en un informe.
---

# Análisis de datos

Conviertes datos en una **respuesta defendible a una pregunta concreta**:
una conclusión con su evidencia, su nivel de confianza y lo que no se pudo
saber, contada para quien tiene que decidir.

Este archivo es el mapa. El detalle de cada fase está en
[FASES.md](FASES.md) (léelo por secciones, `§<n>` = fase n), y el resto en
el material de apoyo que indica la tabla de fases.

## Tres reglas duras

1. **Nunca leas el dataset crudo en el contexto.** Ni `cat`, ni `head` de
   miles de filas, ni pegarlo en el chat. Corres `perfilar.py` y lees su
   resumen; para mirar filas concretas, imprime una muestra filtrada (≤ 20
   filas, solo las columnas que importan). Es la diferencia entre gastar
   2.000 tokens y gastar 200.000.
2. **Ningún número entra al informe si no lo produjo el código.** Cada cifra
   que se afirma (un total, un porcentaje, una diferencia, un intervalo) la
   escribe el script de análisis en `cifras.json` con un nombre, y
   `verificar_cifras.py` comprueba el informe contra ese archivo. Una cifra
   calculada "a ojo" o recordada es lo mismo que una referencia inventada.
3. **Los datos crudos no se tocan.** Viven en `datos/crudos/` y solo se
   leen. Toda transformación es código versionado que escribe en
   `datos/limpios/`; así cualquier resultado se puede reconstruir desde cero.

## Modo de trabajo: interactivo o dentro de un sub-agente

- **Sesión con el usuario**: si falta la pregunta, la audiencia o la
  definición de la métrica principal, pregúntalo antes de analizar (una sola
  tanda, máximo 3 preguntas). Lo no crítico lo asumes y lo listas.
- **Dentro de un sub-agente del orquestador**: no preguntes nunca. Asume lo
  razonable y lista los supuestos en tu reporte. Termina con un
  `DECISION_NEEDED` (formato de `orquestador/SKILL.md` §6) cuando:
  - la métrica principal admite dos definiciones que cambian la conclusión
    (p. ej. "cliente activo" por compra o por inicio de sesión);
  - la limpieza eliminaría más del 5 % de las filas, o imputaría más del
    20 % de una columna que sostiene una conclusión;
  - el perfil detecta datos personales (columnas `pii` o alerta de
    cuasi-identificadores) y el encargo no dice qué se puede mostrar;
  - piden una conclusión causal ("X causa Y") y los datos son
    observacionales (ver [TRAMPAS.md](TRAMPAS.md) §3).
- **Datos de salud o personales en Colombia**: aplica la Ley 1581 de 2012
  (protección de datos personales; los de salud son datos sensibles). En
  informes, gráficos, `cifras.json` y anexos van **solo agregados y
  anonimizados**: nada de filas individuales, nombres, documentos ni
  ubicaciones finas, y ningún grupo tan pequeño que permita reconocer a
  alguien.

## Dos profundidades

| Modo | Cuándo | Qué se entrega |
|---|---|---|
| **Exprés** | "Échale un ojo", una pregunta puntual, datos para decidir si vale la pena seguir | Fases 0–1, una limpieza mínima y 3 hallazgos con un gráfico cada uno, en `hallazgos.md` (una página). Sin informe completo. |
| **Completo** | Informe, entrega de clase, decisión de negocio, tarea `tipo: data` con informe | Las 7 fases y la salida de FASES.md §9. |

Si no te lo dicen, empieza en exprés y propone el completo solo si los
hallazgos lo justifican: muchos encargos se resuelven con tres gráficos
buenos.

## Flujo de fases

| Fase | Qué haces | Qué lees |
|---|---|---|
| 0. Encargo | `encargo.md` de 5 líneas antes de abrir los datos: pregunta, decisión, audiencia, métrica, alcance, más 2–3 hipótesis previas | FASES.md §0 |
| 1. Perfilado | `python .claude/skills/analisis-datos/scripts/perfilar.py datos/crudos/<archivo> --salida perfil` y lees `perfil.md`; fijas qué es una fila y cuál es la llave | FASES.md §1 |
| 2. Limpieza | `src/01_limpieza.py` + `bitacora-limpieza.md` (filas antes → después por paso), `assert` al final, perfil del limpio | FASES.md §2 |
| 3. Exploración | `src/02_analisis.py`: métrica principal, dimensiones, tiempo, descomposición, contraste con las hipótesis | FASES.md §3 |
| 4. Análisis | Método según la pregunta, tamaño del efecto e intervalo (bootstrap; **por bloques si la serie está ordenada en el tiempo**), cifras a `cifras.json` | FASES.md §4, [TRAMPAS.md](TRAMPAS.md); si es "¿qué va a pasar?", [PRONOSTICO.md](PRONOSTICO.md) |
| 5. Gráficos | `src/03_graficos.py`, un mensaje por gráfico, título = conclusión, PNG + SVG, mirar cada uno | FASES.md §5, [GRAFICOS.md](GRAFICOS.md) |
| 6. Historia | Idea central en una frase; informe en pirámide, títulos que afirman, 3 hallazgos | FASES.md §6, [PLANTILLA-INFORME.md](PLANTILLA-INFORME.md) |
| 7. Conclusiones | Cada una con evidencia, confianza y limitación; `verificar_cifras.py` en 0; pipeline reproducible; `verificador-datos` para lo externo | FASES.md §7 |
| — | Dependencias y datos grandes; estructura de `analisis/<slug>/` y qué se muestra en el chat | FASES.md §8 y §9 |

Scripts en `scripts/`: `perfilar.py` (perfil sin leer el dataset),
`estadistica.py` (bootstrap simple y por bloques, solo `numpy`),
`estilo_graficos.py` (estilo de matplotlib) y `verificar_cifras.py`
(números del informe contra `cifras.json`).
