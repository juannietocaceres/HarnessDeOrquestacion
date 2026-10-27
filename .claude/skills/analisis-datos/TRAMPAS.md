# Trampas de análisis

Se corre antes de dar un hallazgo por bueno (fases 3–4 de `SKILL.md`).
Cada trampa trae la pregunta que la detecta y qué hacer.

## 1. Granularidad y joins

- **Promediar promedios.** El promedio de los promedios por tienda no es el
  promedio por venta si las tiendas tienen distinto volumen. → Recalcula
  desde las filas, o pondera.
- **Join que multiplica filas.** Tras un `merge`, ¿el número de filas es el
  esperado? → `assert len(despues) == len(antes)` en joins que no deberían
  duplicar; `validate="many_to_one"` en pandas.
- **Contar lo que no es.** ¿`count` de pedidos o `nunique` de clientes?
  → Escribe en el encargo qué es una fila.

## 2. Composición y agregación

- **Paradoja de Simpson.** Una tendencia que se invierte al separar por
  grupos (el tratamiento A gana en total pero pierde en cada hospital).
  → Antes de concluir sobre el total, mira la misma comparación dentro de
  los 2–3 segmentos más grandes.
- **Efecto mezcla.** El promedio subió porque cambió la proporción de
  grupos, no porque cada grupo mejorara. → Descompón en efecto volumen,
  efecto mezcla y efecto tasa.
- **Denominador oculto.** "Bogotá tiene más quejas" — y más clientes.
  → Tasas por cada 1.000, no conteos, cuando los grupos tienen tamaños
  distintos.

## 3. Causalidad

- **Correlación no es causa.** Pregunta: ¿hay una tercera variable que
  mueva las dos? (la temperatura mueve helados y ahogamientos). ¿La flecha
  podría ir al revés?
- **Sesgo de selección.** ¿Quién está en los datos y quién no? Los que
  contestaron la encuesta, los clientes que siguen activos, los pacientes
  que llegaron al hospital.
- **Supervivencia.** Analizar solo lo que sobrevivió (empresas activas,
  estudiantes que terminaron) exagera lo que "funciona".
- → Con datos observacionales el lenguaje es "se asocia con". Para
  afirmar causa hace falta un experimento (A/B) o un diseño que lo
  justifique (diferencias en diferencias, discontinuidad), y se dice cuál.

## 4. Inferencia

- **Comparaciones múltiples.** Con 20 pruebas al 5 %, se espera una
  "significativa" por azar. → Declara cuántas comparaciones hiciste; usa
  Bonferroni (α / n) o trata los hallazgos sueltos como exploratorios.
- **Significativo no es importante.** Con muestras grandes una diferencia
  de 0,1 % sale significativa. → Reporta tamaño del efecto y si importa
  para la decisión.
- **Muestras chicas.** Un 80 % de 5 casos es 4 personas. → Muestra el `n`
  junto a cada porcentaje; con n < 30 por grupo, IC y prudencia.
- **Regresión a la media.** Los peores del mes pasado "mejoran" este mes
  sin hacer nada. → Compara contra un grupo que no recibió la acción.
- **Buscar hasta encontrar (p-hacking).** Cambiar filtros, periodos o
  exclusiones hasta que salga el resultado. → Las hipótesis del encargo se
  fijan antes; lo encontrado después se etiqueta como exploratorio.

## 5. Tiempo

- **Estacionalidad.** Diciembre contra noviembre no dice nada en retail.
  → Compara contra el mismo periodo del año anterior.
- **Periodo incompleto.** El último mes con 10 días de datos parece una
  caída. → Excluye o anualiza, y dilo.
- **Cambios de definición.** Un salto que coincide con un cambio de
  sistema, de formulario o de regla de negocio. → Pregunta antes de
  explicarlo.
- **Elegir el punto de inicio.** Un crecimiento "desde el mínimo" exagera.
  → Usa una base justificada y muéstrala.

## 6. Modelos (si hay predicción)

- **Fuga de información (leakage).** Una variable que solo se conoce
  después del resultado (fecha de cancelación para predecir cancelación).
  → Pregunta para cada variable: ¿la tendría en el momento de predecir?
- **Evaluar en los mismos datos.** → Separa entrenamiento y prueba; en
  series de tiempo, por fecha, nunca al azar.
- **Sin línea base.** Un 90 % de exactitud con 90 % de una clase no vale
  nada. → Compara siempre contra la predicción ingenua.

## 7. Comprobación de robustez (para confianza alta)

Antes de marcar una conclusión con confianza alta, que se sostenga:

- con y sin outliers;
- con y sin filas imputadas;
- en al menos dos subperiodos o dos segmentos grandes;
- con otra métrica razonable (mediana además de media).

Si cambia, la confianza baja a media y el informe dice de qué depende.
