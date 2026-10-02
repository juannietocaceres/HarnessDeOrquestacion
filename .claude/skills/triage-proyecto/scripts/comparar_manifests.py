#!/usr/bin/env python3
"""Compara la estructura de dos milestone.yaml: ids, tipos, dependencias y waves.

Uso:
    python comparar_manifests.py <generado.yaml> <referencia.yaml>

Sirve para comprobar que un manifest re-generado por triage-proyecto es
equivalente a uno de referencia (p. ej. la prueba de regresión contra
milestones/panel-tareas-demo/milestone.yaml). No compara textos (titulo,
descripcion, criterios): solo la forma del grafo, que es lo que decide las
waves. `cap_concurrencia` se informa pero no cuenta como diferencia
estructural.

Código de salida: 0 = equivalentes, 1 = hay diferencias, 2 = error de lectura.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import preflight_manifest as pm  # noqa: E402


def resumen(manifest: dict) -> dict:
    tareas = {str(t["id"]): t for t in manifest["tareas"]}
    deps = {i: sorted(str(d) for d in (t.get("depende_de") or [])) for i, t in tareas.items()}
    internas = {i: [d for d in ds if d in tareas] for i, ds in deps.items()}
    waves, _ = pm.calcular_waves(internas)
    return {
        "ids": list(tareas),
        "tipos": {i: t.get("tipo") for i, t in tareas.items()},
        "deps": deps,
        "waves": [sorted(w) for w in waves],
        "sin_criterios": sorted(i for i, t in tareas.items() if not t.get("criterios_aceptacion")),
        "cap": manifest.get("cap_concurrencia", 3),
    }


def comparar(a: dict, b: dict) -> list[str]:
    ra, rb = resumen(a), resumen(b)
    difs = []
    if set(ra["ids"]) != set(rb["ids"]):
        difs.append(f"ids distintos: {sorted(ra['ids'])} vs {sorted(rb['ids'])}")
    for i in sorted(set(ra["ids"]) & set(rb["ids"])):
        if ra["tipos"][i] != rb["tipos"][i]:
            difs.append(f"{i}: tipo {ra['tipos'][i]} vs {rb['tipos'][i]}")
        if ra["deps"][i] != rb["deps"][i]:
            difs.append(f"{i}: depende_de {ra['deps'][i]} vs {rb['deps'][i]}")
    if ra["waves"] != rb["waves"]:
        difs.append(f"waves {ra['waves']} vs {rb['waves']}")
    if ra["sin_criterios"] != rb["sin_criterios"]:
        difs.append(f"tareas sin criterios {ra['sin_criterios']} vs {rb['sin_criterios']}")
    return difs


def main(argv: list[str]) -> int:
    pm.configurar_salida()
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        a, b = (pm.cargar_yaml(Path(p)) for p in argv)
    except (OSError, ValueError) as e:
        print(f"ERROR: {e}")
        return 2
    for etiqueta, m, ruta in (("generado", a, argv[0]), ("referencia", b, argv[1])):
        r = resumen(m)
        print(f"{etiqueta} ({Path(ruta).as_posix()}):")
        print(f"  deps: " + "; ".join(f"{i}<-{r['deps'][i] or '[]'}" for i in r["ids"]))
        print(f"  waves: {r['waves']}  sin criterios: {r['sin_criterios']}  cap: {r['cap']}")
    difs = comparar(a, b)
    for d in difs:
        print(f"  DIFERENCIA: {d}")
    if resumen(a)["cap"] != resumen(b)["cap"]:
        print("  nota: cap_concurrencia distinto (no estructural)")
    print("RESULTADO: " + ("EQUIVALENTES" if not difs else f"DISTINTOS ({len(difs)} diferencia/s)"))
    return 0 if not difs else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
