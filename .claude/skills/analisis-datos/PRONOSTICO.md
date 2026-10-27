# Pronóstico: "¿qué va a pasar?"

Se lee solo si la pregunta del encargo es de pronóstico (fila "¿Qué va a
pasar?" de FASES.md §4). Un pronóstico vale lo que vale su evaluación: casi
todo lo de aquí es sobre no engañarse al medir.

## 1. Línea base primero

Antes de cualquier modelo, calcula dos pronósticos ingenuos con la misma
evaluación que usarás para el modelo:

- **Ingenuo**: el próximo valor es la última observación.
- **Ingenuo estacional**: el próximo valor es el del mismo periodo de la
  temporada anterior (la misma semana del año pasado, el mismo mes).

Un modelo que no le gana a los dos, en datos que no vio, no se entrega. Se
reporta que la línea base es lo mejor disponible, que también es un
resultado.

## 2. Validación temporal de origen móvil

- **Nunca partición aleatoria.** Mezclar fechas deja que el modelo vea el
  futuro.
- **Origen móvil**: entrenas hasta el tiempo t, pronosticas t+1 … t+H,
  avanzas el origen y repites. Cada pronóstico se evalúa solo con datos
  posteriores a su origen. Reporta el error **por horizonte** (h = 1, 2,
  …): suele crecer con h y el promedio lo esconde.
- **Tres tramos en el tiempo**: entrenamiento → validación → prueba, en
  ese orden, sin solaparse.

## 3. Fuga de información en covariables

Para un horizonte h, una covariable solo puede entrar con **rezagos ≥ h**:
lo que se conocerá en el momento de pronosticar, no lo que pasó después.
Pregunta por cada variable: "el día que hago este pronóstico, ¿ya tengo
este dato?". Cuidado con las variables que se publican con retraso
(registros que se consolidan semanas después), las que se revisan
(cifras preliminares que cambian) y las agregadas sobre una ventana que
incluye el futuro (media móvil centrada).

## 4. Validación y prueba: la prueba se mira una vez

- Todas las decisiones (variables, hiperparámetros, transformaciones,
  qué modelo gana) se ajustan **solo con el periodo de validación**.
- El periodo de prueba se evalúa **una sola vez**, al final, con todo
  congelado.
- Si después de ver la prueba se cambia algo, el nuevo resultado **no
  reemplaza** al original: se reporta aparte como **análisis de
  sensibilidad**, diciendo qué se cambió y por qué.

## 5. Métricas

| Tipo de pronóstico | Métrica | Qué dice |
|---|---|---|
| Puntual | **MAE** y **RMSE** | Error típico en las unidades de la variable (RMSE castiga más los errores grandes) |
| Puntual | **Error relativo al ingenuo** (MAE del modelo / MAE del ingenuo, con el mismo origen móvil) | < 1 le gana a la línea base; es la cifra que más se entiende |
| Probabilístico (distribución) | **CRPS** | Calidad de toda la distribución pronosticada; en unidades de la variable; menor es mejor |
| Probabilístico (intervalos) | **Interval score (Winkler)** | Ancho del intervalo + penalización `2/α` por cuánto se sale el valor real |
| Intervalos | **Cobertura real** | % de valores reales que cayeron dentro del intervalo del 80 % o 95 %: debe quedar cerca de lo nominal, por horizonte |

Un intervalo del 95 % que cubre el 70 % de las veces está mal, aunque el
error puntual sea bueno. La cobertura se reporta siempre que se den
intervalos.

## 6. Comparar modelos: Diebold-Mariano

- Para decir que un modelo es mejor que otro (o que la línea base), no
  basta con que su error promedio sea menor: usa la prueba de
  **Diebold-Mariano** sobre la diferencia de pérdidas (p. ej. errores
  absolutos) de los dos modelos en los mismos puntos, con la corrección
  para muestras pequeñas de Harvey, Leybourne y Newbold y un error
  estándar que tenga en cuenta la autocorrelación hasta h − 1.
- **Varias series** (varios municipios, productos, sucursales): versión
  **agrupada (panel)**, que promedia las diferencias de pérdida entre
  series y usa un error estándar que tiene en cuenta que las series están
  correlacionadas entre sí. Probar serie por serie es caer en
  comparaciones múltiples (TRAMPAS.md §4).
- Se reporta la diferencia de error, su intervalo y el p-valor; con pocas
  ventanas de evaluación, la prueba tiene poca potencia y se dice.

## 7. Intervalos calibrados: predicción conforme por horizonte

Si los intervalos del modelo no cubren lo que prometen (§5), calíbralos
con **predicción conforme**, **por separado para cada horizonte h**:

1. En un tramo de calibración (dentro de validación, posterior al
   entrenamiento), guarda los errores absolutos |real − pronóstico| del
   horizonte h.
2. Toma su cuantil de nivel ⌈(n + 1)(1 − α)⌉ / n (n = cantidad de errores
   de calibración).
3. El intervalo del horizonte h es pronóstico ± ese cuantil.
4. Comprueba la cobertura en la prueba. Con series que cambian de nivel,
   recalibra con una ventana móvil de los errores más recientes.

## 8. Si el pronóstico dispara alertas (eventos)

Cuando el uso es avisar de un evento (brote, quiebre de stock, pico de
demanda), además de las métricas de §5 reporta, sobre periodos de prueba:

| Métrica | Qué dice |
|---|---|
| **Sensibilidad** | De los eventos reales, cuántos se alertaron |
| **Especificidad** | De los periodos sin evento, cuántos quedaron sin alerta |
| **MCC** (coeficiente de correlación de Matthews) | Resumen en un número que no se infla cuando los eventos son raros (a diferencia de la exactitud) |
| **Falsas alarmas por periodo** | Cuántas alertas sin evento hay por semana, mes o temporada: es lo que agota a quien las recibe |
| **Anticipación** | Cuántos periodos antes del evento llegó la primera alerta (mediana y rango); una alerta que llega tarde no sirve |

Define antes de evaluar qué cuenta como evento (umbral) y qué ventana de
anticipación cuenta como acierto, y no los ajustes mirando la prueba (§4).

## 9. Qué va a `cifras.json` y al informe

- Error del modelo y de las dos líneas base, por horizonte, con el
  esquema de validación (origen inicial, paso, H).
- Error relativo al ingenuo, resultado de Diebold-Mariano y cobertura
  real de los intervalos.
- Si hubo análisis de sensibilidad posterior a la prueba, aparte y
  rotulado.
- En el informe, lo que el pronóstico no puede anticipar (cambios de
  definición, eventos sin precedente en los datos) va en "lo que estos
  datos no permiten afirmar".
