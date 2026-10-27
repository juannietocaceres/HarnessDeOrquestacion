# Gráficos: selector y reglas

Se lee en la fase 5 de `SKILL.md`. Un gráfico existe para que el lector vea
**una cosa** más rápido que leyendo una tabla. Si no hay una cosa que ver,
va una tabla (o nada).

## 1. Selector: qué quieres que vea el lector

| Mensaje | Gráfico | Evitar |
|---|---|---|
| Comparar categorías ("el Norte vende menos") | Barras **horizontales**, ordenadas de mayor a menor | Torta, barras verticales con etiquetas giradas |
| Cambio en el tiempo ("cae desde marzo") | Línea; barras si son pocos periodos discretos | Áreas apiladas con más de 3 series |
| Antes vs después, o dos momentos por categoría | Gráfico de pendiente (slope) o de pesas (dumbbell) | Dos barras agrupadas por categoría |
| Parte de un todo ("el 70 % viene de...") | Barra apilada al 100 % o una sola barra; torta solo con 2–3 porciones | Torta con muchas porciones, dona 3D |
| Distribución ("la mayoría paga menos de 50") | Histograma; boxplot o strip para comparar grupos | Solo la media en una barra |
| Relación entre dos variables | Dispersión, con línea de tendencia si ayuda | Doble eje Y |
| Composición de un cambio ("de 100 a 82: −12 Norte, −4 Sur...") | Cascada (waterfall) | Barras sueltas sin el total |
| Muchas categorías × tiempo | Small multiples (una mini-gráfica por categoría, mismos ejes) | Una línea por categoría en el mismo gráfico (espagueti) |
| Ranking con muchos elementos | Gráfico de puntos (dot plot) ordenado | Barras de 30 colores |
| Un solo número importante | El número grande, con su comparación ("−18 % vs T3 2025") | Un gráfico de una barra |

Para elegir entre dos: el que hace la comparación importante **más corta a
la vista** (cosas que se comparan, una al lado de la otra, sobre la misma
escala).

## 2. Reglas de estilo (las aplica `estilo_graficos.py`)

- **Título = la conclusión**, en una frase. Subtítulo = qué se mide y la
  unidad ("Ventas netas, millones de COP, ene–sep 2026").
- **Color con intención, según el mensaje:**
  - **Un solo mensaje** ("el Norte explica la caída"): gris (`#B0B0B0`)
    para el contexto y un color de acento (`#C2410C`) para lo que el
    título menciona. Un segundo color solo si hay un segundo actor en el
    mensaje.
  - **El mensaje es comparar varias series o modelos** (tres modelos de
    pronóstico contra lo observado, cuatro regiones que importan por
    igual): `PALETA_CATEGORICA` del script (variante de Okabe–Ito, apta
    para daltonismo), un color por serie, **con etiquetas directas** al
    final de cada línea en vez de leyenda. Más de 5–6 series → small
    multiples.
  - Nunca arcoíris por defecto, ni rojo/verde como única diferencia.
- **Etiquetas directas**: el nombre de la serie al final de su línea, el
  valor al final de la barra. La leyenda solo si no cabe nada de lo
  anterior.
- **Quitar lo que no informa**: bordes superior y derecho, rejilla densa,
  fondo de color, sombras, 3D, decimales que nadie necesita.
- **Barras empiezan en cero.** Las líneas pueden no empezar en cero si el
  eje lo dice claramente y la variación es lo importante.
- **Mismos ejes** en small multiples y en gráficos que se comparan entre sí.
- **Números legibles**: separador de miles, unidad en el subtítulo o el
  eje, porcentajes sin decimales salvo que importen.
- **Fuente y nota** abajo a la izquierda: de dónde salen los datos y el
  periodo; si hay imputados o exclusiones que afecten, se dice ahí.
- Texto a tamaño legible en una slide (≥ 11 pt al exportar a 8 × 4,5 in).

## 3. Uso de `estilo_graficos.py`

```python
import sys; sys.path.insert(0, ".claude/skills/analisis-datos/scripts")
from estilo_graficos import aplicar_estilo, barras_destacadas, linea_destacada, titular, guardar

aplicar_estilo()
fig, ax = barras_destacadas(df["region"], df["caida"], destacar=["Norte"], formato="{:.0f} %")
titular(fig, "El Norte explica el 70 % de la caída", "Aporte a la caída de ventas, T3 2026 vs T3 2025")
guardar(fig, "graficos/caida-q3-por-region", fuente="Fuente: ventas internas, ene–sep 2026")
```

- `barras_destacadas(etiquetas, valores, destacar=[...])`: barras
  horizontales ordenadas, gris salvo las destacadas, valor al final.
- `linea_destacada(df_ancho, destacar=[...])`: una línea por columna, gris
  salvo las destacadas, etiqueta al final de cada línea.
- `titular(fig, titulo, subtitulo)` y `guardar(fig, ruta_sin_extension,
  fuente=...)` (PNG 200 dpi + SVG).

Para lo que los helpers no cubren, `aplicar_estilo()` deja matplotlib con el
estilo base y se arma el gráfico a mano con `GRIS` y `ACENTO`.

## 4. Revisión de cada gráfico (antes de darlo por bueno)

- [ ] ¿Se entiende el mensaje en 5 segundos leyendo solo el título y
      mirando el color?
- [ ] ¿El color de acento está exactamente en lo que el título nombra?
- [ ] ¿Las barras arrancan en cero? ¿Los ejes comparables son iguales?
- [ ] ¿Hay etiquetas encimadas, cortadas o giradas? (míralo como imagen)
- [ ] ¿Se lee en gris (impresión, daltonismo)?
- [ ] ¿La cifra del título está en `cifras.json`?
