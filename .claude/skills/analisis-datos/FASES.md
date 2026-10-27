# Fases del análisis en detalle

Se lee por secciones desde `SKILL.md`, cuando la fase lo pide. Los
números de sección son los de la fase.

## 0. Encargo: la pregunta antes que los datos

Antes de abrir el archivo, escribe `encargo.md` (5 líneas, no más):

```
Pregunta:   ¿<una pregunta que se pueda responder con sí/no, cuánto o cuál>?
Decisión:   <qué va a hacer alguien distinto según la respuesta>
Audiencia:  <quién lo lee y qué sabe de datos: directivo, docente, técnico>
Métrica:    <la métrica principal, definida de forma operativa>
Alcance:    <periodo, población, qué queda fuera>
```

- "Analizar las ventas" no es una pregunta. "¿Qué región explica la caída
  de ventas del tercer trimestre?" sí lo es.
- Si no hay decisión detrás, pregunta para qué es: cambia qué se profundiza
  y cómo se cuenta.
- Escribe aquí también **las hipótesis previas** (2 o 3): lo que esperas
  encontrar. Sirven para buscar, y para no confundir "lo que encontré" con
  "lo que quería encontrar".

## 1. Ingesta y perfilado

```
python .claude/skills/analisis-datos/scripts/perfilar.py datos/crudos/<archivo> --salida perfil
```

Produce `perfil.md` (lo lees tú) y `perfil.json` (lo leen otros scripts):
dimensiones, tipo y tipo sugerido por columna, nulos, únicos, duplicados,
outliers por IQR, categorías con variantes de escritura (`"Bogotá"`,
`"bogota "`), números guardados como texto, fechas como texto, columnas
constantes, columnas con posibles datos personales (también de salud:
fecha de nacimiento, historia clínica, `num_ide`/`tip_ide`, barrio; de
esas no muestra valores ni mínimos y máximos) y un aviso de
cuasi-identificadores si el archivo junta edad o fecha de nacimiento,
sexo y ubicación fina aunque no haya nombres. Con `--hoja` lee una
hoja de Excel; con `--sep` fija el separador si la detección falla.

Del perfil sale una lista corta: **qué columnas responden la pregunta** y
**qué problemas de calidad las afectan**. Los problemas de columnas que no
se usan no se limpian (no es trabajo útil).

Antes de seguir, entiende **qué es una fila** (un pedido, un cliente, un
cliente-mes) y **qué identifica una fila** (la llave). La mitad de los
errores de análisis son errores de granularidad: promediar promedios,
contar pedidos creyendo contar clientes, un join que multiplica filas.

## 2. Limpieza con bitácora

El código va en `src/01_limpieza.py` y cada paso queda en
`bitacora-limpieza.md` con una fila:

| # | Problema | Decisión | Filas antes → después | Columnas | Por qué |
|---|---|---|---|---|---|
| 1 | 312 duplicados exactos | Eliminar | 10.450 → 10.138 | todas | Exportación repetida del 3 de marzo |

Reglas:

- **Orden**: tipos (fechas, números con separador de miles o `$`) →
  normalizar texto (espacios, mayúsculas, tildes, variantes) → duplicados
  → valores imposibles (edad −3, fecha futura) → faltantes → outliers.
- **Nunca elimines en silencio.** Cada filtro reporta cuántas filas quitó.
  Un `dropna()` sin mirar qué quita es un sesgo que nadie va a ver.
- **Faltantes: primero por qué faltan.** Si faltan al azar, imputar o
  descartar da casi igual; si faltan por algo (los que no responden el
  ingreso son los de ingreso alto), cualquier imputación sesga. Prefiere
  marcar (`es_imputado`) y analizar con y sin imputados a "rellenar con la
  media".
- **Outliers: un valor extremo no es un error.** Se corrige si es imposible
  o claramente de captura (un precio con tres ceros de más); se mantiene si
  es real, y se reporta si cambia la conclusión.
- **Al final del script, valida con `assert`**: llave única, sin nulos en
  columnas obligatorias, rangos válidos, conteo de filas dentro de lo
  esperado. Un pipeline que no se valida a sí mismo se rompe sin avisar
  cuando lleguen datos nuevos.
- Guarda en `datos/limpios/` (Parquet si hay `pyarrow`, si no CSV) y vuelve
  a correr `perfilar.py` sobre el limpio: ese segundo perfil es la evidencia
  de que la limpieza hizo lo que dice la bitácora.

## 3. Exploración guiada por la pregunta

En `src/02_analisis.py`. No es "graficar todo contra todo": es responder
la pregunta por capas.

1. **Univariado** de la métrica principal: distribución (no solo la
   media), forma, colas. Si es asimétrica, la mediana describe mejor.
2. **La métrica contra cada dimensión candidata** (región, segmento,
   tiempo, canal). Ordena las dimensiones por cuánto explican, no por el
   orden de las columnas.
3. **Tiempo**, si lo hay: tendencia, estacionalidad, quiebres. Compara
   contra el mismo periodo anterior, no contra el mes de al lado.
4. **Descomposición**: si un total cambió, ¿cambió el volumen, el precio o
   la mezcla? ¿Qué segmento aporta cuánto del cambio?
5. Contrasta contra las hipótesis del encargo: confirmada, refutada o sin
   evidencia suficiente.

Imprime tablas agregadas, nunca el DataFrame entero.

## 4. Análisis: método según la pregunta

| Pregunta | Método razonable | Lo que se reporta |
|---|---|---|
| ¿Cuánto / cómo es? (descriptiva) | Mediana, percentiles, proporciones | Valor + intervalo de confianza (bootstrap) |
| ¿A es distinto de B? (comparativa) | Diferencia de medias o proporciones; bootstrap; t de Welch o prueba de proporciones si hay `scipy` | **Tamaño del efecto** + IC del 95 %; el p-valor solo acompaña |
| ¿X se relaciona con Y? | Spearman (robusto) o Pearson; dispersión con tendencia | Coeficiente + IC + gráfico; nunca la palabra "causa" |
| ¿Cómo evoluciona? | Serie temporal agregada; media móvil; variación interanual | Cambio absoluto y relativo contra una base explícita |
| ¿Qué grupos hay? | Segmentación por reglas antes que clustering; k-means solo con variables escaladas y justificadas | Perfil de cada segmento y su tamaño |
| ¿Qué va a pasar? | Línea base ingenua primero; modelo solo si le gana a la línea base en datos que no vio. Todo el detalle en [PRONOSTICO.md](PRONOSTICO.md) | Error en validación contra la línea base |

- **Siempre incertidumbre.** Un 12 % sin intervalo no dice si es 12 ± 1 o
  12 ± 15. El bootstrap con `numpy` (remuestrear 2.000 veces y tomar los
  percentiles 2,5 y 97,5) sirve casi para todo y no necesita `scipy`:
  `bootstrap(valores, estadistico)` de `scripts/estadistica.py`.
- **Datos ordenados en el tiempo: bootstrap por bloques.** Si las filas son
  semanas o meses seguidos, cada valor se parece al anterior
  (autocorrelación) y el bootstrap simple, que los baraja como si fueran
  independientes, da intervalos **demasiado estrechos**. Usa bloques
  móviles: `bootstrap_bloques(serie, estadistico, largo_bloque)` de
  `scripts/estadistica.py`. Largo del bloque ≈ raíz cúbica de n
  (`largo_bloque_sugerido(n)`), o el periodo estacional si lo hay (12 en
  meses, 52 en semanas, siempre que n lo permita). **Di en el informe el
  largo de bloque usado.**
- **Tamaño del efecto antes que significancia.** Con 100.000 filas todo es
  "significativo"; la pregunta es si la diferencia importa para la decisión.
- **Una sola prueba por hipótesis del encargo.** Si pruebas 20 cosas, una
  sale significativa por azar (TRAMPAS.md §4): decláralo o corrige.
- **Lo más simple que responda.** Una tabla dinámica bien hecha le gana a
  un modelo que nadie entiende.
- Corre la lista de [TRAMPAS.md](TRAMPAS.md) antes de dar un hallazgo por
  bueno. Es corta y atrapa los errores que más conclusiones tumban.

**Cada cifra que vas a afirmar se guarda en `cifras.json`** desde el
script, con nombre, valor y unidad:

```python
cifras["caida_ventas_q3_pct"] = {"valor": -18.4, "unidad": "%", "ic95": [-21.0, -15.9],
                                  "fuente": "src/02_analisis.py: comparacion_q3"}
json.dump(cifras, open("cifras.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
```

Convierte a `float()` / `int()` los valores de numpy antes de guardarlos
(`json` no serializa `np.float64` dentro de listas).

## 5. Gráficos

En `src/03_graficos.py`, con el estilo de `scripts/estilo_graficos.py`.
Reglas completas y selector de gráfico en [GRAFICOS.md](GRAFICOS.md). Lo
esencial:

- **Un gráfico, un mensaje.** El título es la conclusión ("El Norte explica
  el 70 % de la caída"), no la descripción ("Ventas por región").
- **Gris para el contexto, un color para lo que importa.** Si todo tiene
  color, nada destaca.
- **Etiquetas directas** sobre las líneas y barras en vez de leyenda;
  menos ejes, menos rejilla, sin bordes.
- **Barras desde cero, siempre.** Sin 3D, sin doble eje, sin tortas de más
  de 3 porciones.
- Exporta a `graficos/` en PNG (200 dpi) y SVG. Nombre del archivo = el
  mensaje en corto (`caida-q3-por-region.png`).
- **Mira cada gráfico** (léelo como imagen) antes de darlo por bueno:
  etiquetas encimadas, ejes cortados y colores que no se distinguen solo
  se ven mirando.

Si el entorno tiene la skill `dataviz` (no es del harness), puedes usarla
para paleta y gráficos interactivos; las reglas de mensaje de esta sección
mandan igual.

## 6. Historia

Antes de escribir el informe, escribe **la idea central** en una frase
completa, con sujeto, verbo y consecuencia:

> La caída del 18 % en ventas del T3 se concentra en la región Norte, donde
> el cierre de dos distribuidores explica 7 de cada 10 pesos perdidos;
> recuperar esos canales es más rentable que la campaña nacional prevista.

Si no puedes escribirla, todavía no tienes historia: vuelve al análisis.

Luego arma el informe con [PLANTILLA-INFORME.md](PLANTILLA-INFORME.md):

- **La respuesta primero** (pirámide): conclusión y recomendación en el
  primer párrafo; la evidencia después; el método al final o en anexo.
- **Situación → complicación → resolución** para el arco: qué se sabía,
  qué cambió o qué problema hay, qué se propone.
- **Cada título de sección es una afirmación**, no un tema. Leyendo solo
  los títulos se entiende la historia.
- **Tres hallazgos, no quince.** Lo que no sostiene la idea central va a
  un anexo. Ser exhaustivo no es ser útil.
- **Escribe para la audiencia del encargo.** Un directivo quiere la
  decisión y el riesgo; un docente quiere ver el método; un técnico, el
  código y los supuestos.
- **Lenguaje según la evidencia**: "se asocia con" para correlación,
  "causó" solo con experimento o diseño causal; "aproximadamente" cuando
  hay incertidumbre que el lector debe sentir.

Si además hace falta exponerlo, la historia pasa a
`presentaciones-visuales` (`tipo: presentacion`): un hallazgo por slide, el
título de la slide es el hallazgo y el gráfico es la evidencia.

## 7. Conclusiones y verificación

Cada conclusión del informe lleva cuatro cosas:

| Conclusión | Evidencia | Confianza | Limitación |
|---|---|---|---|
| El Norte explica ~70 % de la caída | `aporte_norte_pct` (gráfico 2) | Alta: diferencia grande, IC estrecho, consistente en los 3 meses | Datos de un solo año |

- **Confianza alta**: efecto grande, IC estrecho, se sostiene al cambiar
  supuestos (con y sin outliers, con y sin imputados). **Media**: efecto
  claro pero datos limitados o un supuesto pesa. **Baja**: indicio; se
  presenta como hipótesis para confirmar, no como conclusión.
- **Recomendaciones accionables**: quién, qué y cómo se sabrá si funcionó.
- **Qué no se puede concluir** con estos datos, explícito. Es lo que más
  credibilidad le da al resto.

Antes de entregar:

1. `python .claude/skills/analisis-datos/scripts/verificar_cifras.py informe.md cifras.json`
   → código 0. Un número del informe que no está en `cifras.json` se
   corrige o se saca. Los números que no son resultados (años, "3
   hallazgos", "Tabla 2") van en la lista `ignorar` de `cifras.json` o el
   script ya los descarta.
2. Correr de cero `src/01` → `02` → `03` y comprobar que `cifras.json` sale
   igual: si no se reproduce, no está terminado.
3. `verificador-datos` sobre las afirmaciones que **no** salen de los datos
   (contexto del sector, cifras externas, explicaciones de causa). Lo que
   sale de los datos ya lo cubre el paso 1.
4. `revision-codigo` sobre `src/` si es una tarea del harness.

## 8. Entorno y dependencias

- **Base**: Python 3.10+ con `pandas` y `numpy`. Para gráficos,
  `matplotlib`. Opcionales: `pyarrow` (Parquet), `openpyxl` (Excel),
  `scipy` (pruebas clásicas), `seaborn`.
- Si falta algo, comprueba con `python -c "import <paquete>"` antes de
  escribir código que lo use, y deja el comando de instalación
  (`pip install matplotlib`) en el reporte o en `requirements.txt` del
  análisis. No instales paquetes en el entorno del usuario sin decirlo.
- Datos grandes (> ~1 GB o > 10 millones de filas): lee solo las columnas
  necesarias (`usecols`), con tipos fijados (`dtype`), o usa `duckdb` /
  `polars` si están; agrega antes de traer a memoria.
- Notebook o scripts: **scripts** por defecto (se versionan, se revisan y
  se re-ejecutan limpio). Un `.ipynb` solo si el encargo lo pide, y se
  entrega ejecutado de arriba a abajo sin errores.

## 9. Salida

En `analisis/<slug>/` (o la carpeta que fije la tarea):

| Archivo | Contenido |
|---|---|
| `encargo.md` | Pregunta, decisión, audiencia, métrica, alcance e hipótesis |
| `datos/crudos/` | Datos originales, solo lectura (en `.gitignore` si pesan o tienen datos personales) |
| `datos/limpios/` | Salida de la limpieza |
| `perfil.md` / `perfil.json` | Perfil del crudo (y `perfil-limpio.*` del limpio) |
| `bitacora-limpieza.md` | Una fila por transformación, con filas antes → después |
| `src/01_limpieza.py`, `02_analisis.py`, `03_graficos.py` | El pipeline reproducible |
| `cifras.json` | Toda cifra que se afirma, con valor, unidad, IC y fuente |
| `graficos/` | PNG + SVG, un mensaje por archivo |
| `informe.md` | La historia con conclusiones (modo completo) |
| `hallazgos.md` | Una página con 3 hallazgos (modo exprés) |

En el chat muestra solo: la idea central, los 3 hallazgos con su nivel de
confianza, la ruta del informe, el resultado de `verificar_cifras.py` y los
supuestos y limitaciones. Dentro del harness, decisiones de limpieza de
alto impacto y conclusiones de confianza baja van como
`verificacion_manual` de la tarea.
