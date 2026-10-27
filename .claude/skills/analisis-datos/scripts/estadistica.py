"""Intervalos por bootstrap, solo con numpy (ver FASES.md §4).

    from estadistica import bootstrap, bootstrap_bloques, largo_bloque_sugerido

- bootstrap(valores, estadistico): remuestreo simple, para filas
  independientes (clientes, pedidos).
- bootstrap_bloques(serie, estadistico, largo_bloque): bloques móviles,
  para datos ordenados en el tiempo (semanas, meses seguidos), donde el
  simple subestima la incertidumbre por la autocorrelación.
- largo_bloque_sugerido(n): round(n ** (1/3)), mínimo 1.

Ambas devuelven {"valor", "ic95": [inf, sup], ...} listo para cifras.json
(floats de Python, no de numpy).
"""
import numpy as np


def _resultado(datos, estadistico, replicas, nivel):
    alfa = (1 - nivel) / 2
    inf, sup = np.percentile(replicas, [100 * alfa, 100 * (1 - alfa)])
    return {"valor": float(estadistico(datos)), "ic95" if nivel == 0.95 else "ic": [float(inf), float(sup)]}


def bootstrap(valores, estadistico=np.mean, n=2000, nivel=0.95, semilla=0):
    datos = np.asarray(valores, dtype=float)
    if datos.size < 2:
        raise ValueError("hacen falta al menos 2 valores")
    rng = np.random.default_rng(semilla)
    replicas = [estadistico(datos[rng.integers(0, datos.size, datos.size)]) for _ in range(n)]
    return _resultado(datos, estadistico, replicas, nivel)


def largo_bloque_sugerido(n):
    return max(1, int(round(n ** (1 / 3))))


def bootstrap_bloques(serie, estadistico=np.mean, largo_bloque=None, n=2000, nivel=0.95, semilla=0):
    """Bootstrap de bloques móviles: concatena bloques contiguos al azar hasta el largo original."""
    datos = np.asarray(serie, dtype=float)
    total = datos.size
    largo = largo_bloque_sugerido(total) if largo_bloque is None else int(largo_bloque)
    if total < 2 or not 1 <= largo <= total:
        raise ValueError(f"largo de bloque {largo} inválido para una serie de {total} valores")
    rng = np.random.default_rng(semilla)
    n_bloques = -(-total // largo)
    inicios_posibles = total - largo + 1
    desplazamiento = np.arange(largo)
    replicas = []
    for _ in range(n):
        inicios = rng.integers(0, inicios_posibles, n_bloques)
        muestra = datos[(inicios[:, None] + desplazamiento).ravel()[:total]]
        replicas.append(estadistico(muestra))
    resultado = _resultado(datos, estadistico, replicas, nivel)
    resultado["largo_bloque"] = largo
    return resultado
