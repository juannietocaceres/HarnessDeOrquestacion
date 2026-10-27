"""Estilo de matplotlib para gráficos de un solo mensaje (ver GRAFICOS.md).

    from estilo_graficos import aplicar_estilo, barras_destacadas, linea_destacada, titular, guardar

- aplicar_estilo(): sin bordes superior/derecho, rejilla mínima, texto gris
  oscuro, tamaños legibles en slide.
- barras_destacadas(etiquetas, valores, destacar=[...]): barras horizontales
  ordenadas, gris salvo las destacadas, valor escrito al final de cada barra.
- linea_destacada(df_ancho, destacar=[...]): una línea por columna, gris
  salvo las destacadas, etiqueta directa al final (sin leyenda).
- titular(fig, titulo, subtitulo): título = conclusión; subtítulo = medida.
- guardar(fig, ruta_sin_extension, fuente=...): PNG 200 dpi + SVG.

Los números se escriben con coma decimal y punto de miles (decimal=",");
decimal="." para la convención en inglés.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

GRIS = "#B0B0B0"
GRIS_TEXTO = "#4A4A4A"
ACENTO = "#C2410C"
# Variante de Okabe–Ito (apta para daltonismo), sin amarillo claro.
PALETA_CATEGORICA = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#000000"]


def aplicar_estilo():
    plt.rcParams.update({
        "figure.figsize": (8, 4.5), "figure.dpi": 100, "savefig.dpi": 200,
        "font.size": 11, "axes.titlesize": 14, "axes.labelsize": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": GRIS, "axes.labelcolor": GRIS_TEXTO,
        "xtick.color": GRIS_TEXTO, "ytick.color": GRIS_TEXTO,
        "text.color": GRIS_TEXTO, "axes.grid": False,
        "axes.prop_cycle": plt.cycler(color=PALETA_CATEGORICA),
        "legend.frameon": False, "svg.fonttype": "none",
    })


def numero(v, formato="{:,.0f}", decimal=","):
    """Formatea v y, si decimal=",", intercambia separadores: 1,234.5 -> 1.234,5."""
    texto = formato.format(v)
    return texto.translate(str.maketrans(",.", ".,")) if decimal == "," else texto


def _colores(etiquetas, destacar, color):
    destacar = set(map(str, destacar or []))
    return [color if str(e) in destacar else GRIS for e in etiquetas]


def barras_destacadas(etiquetas, valores, destacar=None, formato="{:,.0f}", color=ACENTO, ax=None,
                      decimal=","):
    pares = sorted(zip(map(str, etiquetas), map(float, valores)), key=lambda p: p[1])
    etq, val = [p[0] for p in pares], [p[1] for p in pares]
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, max(3, 0.45 * len(etq) + 1.5)))
    else:
        fig = ax.figure
    barras = ax.barh(etq, val, color=_colores(etq, destacar, color), height=0.7)
    ax.set_xlim(min(0, min(val)) * 1.15, max(0, max(val)) * 1.15 or 1)
    ax.axvline(0, color=GRIS, linewidth=0.8)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(left=False, bottom=False, labelbottom=False)
    rango = (max(val) - min(0, min(val))) or 1
    for b, v in zip(barras, val):
        x = b.get_width()
        ax.text(x + (0.01 if v >= 0 else -0.01) * rango, b.get_y() + b.get_height() / 2,
                numero(v, formato, decimal), va="center",
                ha="left" if v >= 0 else "right", fontsize=10)
    return fig, ax


def linea_destacada(df_ancho, destacar=None, color=ACENTO, formato="{:,.0f}", ax=None, decimal=","):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    destacar = set(map(str, destacar or []))
    orden = [c for c in df_ancho.columns if str(c) not in destacar] + \
            [c for c in df_ancho.columns if str(c) in destacar]
    for col in orden:
        serie = df_ancho[col].dropna()
        es = str(col) in destacar
        ax.plot(serie.index, serie.values, color=color if es else GRIS,
                linewidth=2.4 if es else 1.4, zorder=3 if es else 2)
        if len(serie):
            ax.annotate(f"{col}  " + numero(serie.iloc[-1], formato, decimal),
                        (serie.index[-1], serie.iloc[-1]), xytext=(6, 0),
                        textcoords="offset points", va="center",
                        color=color if es else GRIS_TEXTO, fontweight="bold" if es else "normal")
    ax.grid(axis="y", color="#EAEAEA", linewidth=0.8)
    return fig, ax


def titular(fig, titulo, subtitulo=None):
    # Posiciones en pulgadas convertidas a fracción: no se encima con figuras de otra altura.
    alto = fig.get_figheight()
    fig.suptitle(titulo, x=0.01, y=1 - 0.12 / alto, ha="left", va="top",
                 fontsize=14, fontweight="bold", color="#1F1F1F")
    if subtitulo:
        fig.text(0.01, 1 - 0.47 / alto, subtitulo, ha="left", va="top", fontsize=10.5, color=GRIS_TEXTO)
    fig.tight_layout(rect=(0, 0.35 / alto, 1, 1 - (0.8 if subtitulo else 0.5) / alto))


def guardar(fig, ruta, fuente=None):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if fuente:
        fig.text(0.01, 0.01, fuente, ha="left", va="bottom", fontsize=8.5, color="#808080")
    for ext in (".png", ".svg"):
        fig.savefig(ruta.with_suffix(ext), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return [str(ruta.with_suffix(".png")), str(ruta.with_suffix(".svg"))]
