"""Comprueba que cada número de un informe salga de cifras.json.

Es la regla "ningún número entra al informe si no lo produjo el código"
convertida en un criterio verificable. Extrae los números del informe
(Markdown) y busca para cada uno una cifra de cifras.json que, redondeada a
los decimales con que se escribió, dé ese número.

Para cada cifra se aceptan sus formas habituales de escritura:
    el valor, su valor absoluto ("caída del 18 %" para -18.4),
    ×100 (0.184 escrito como 18 %), y ÷ mil / millón / mil millones
    cuando el número va seguido de "mil", "millones", "k", "M", "MM".
Cada número se lee en formato español (10.138 ; 18,4) y en inglés
(10,138 ; 18.4); vale si alguna de las dos lecturas coincide.

Se ignoran: bloques y spans de código, URLs y destinos de enlaces e
imágenes, números pegados a letras (T3, Q4, H2O, 3D), marcadores de lista
numerada, niveles de confianza y significancia ("IC 95 %", "95 % de
confianza", "p < 0,05", "α = 0,05"), años entre 1900 y 2100 escritos
sin decimales, enteros de 0 a 10 sin % (conteos de prosa: "3 hallazgos"; --estricto los exige) y lo que
liste "ignorar" en cifras.json.

Formato de cifras.json (cualquiera de los dos):
    {"cifras": {"nombre": {"valor": -18.4, "ic95": [-21, -15.9]}, ...},
     "ignorar": ["2,54"]}
    {"nombre": -18.4, "otro": {"valor": 3}}
Cuentan "valor", "ic95" y cualquier número dentro de la entrada.

Uso:
    python verificar_cifras.py INFORME.md CIFRAS.json [--estricto]

Salida: JSON por stdout. Códigos de salida:
    0  todos los números del informe están respaldados
    1  hay al menos un número sin respaldo
    2  error de uso (archivo inexistente, JSON inválido)
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

ESCALAS = {"mil": 1e3, "k": 1e3, "millones": 1e6, "millón": 1e6, "millon": 1e6,
           "m": 1e6, "mm": 1e9, "mil millones": 1e9, "billones": 1e12}
NUM = re.compile(
    r"(?<![\w.,/#-])(?P<signo>[-−+]?)(?P<num>\d{1,3}(?:[.,]\d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)?)"
    r"(?![\w])(?P<cola>\s*(?:%|mil millones|millones|mill[oó]n|mil|MM|M|k)\b|\s*%)?")


def limpiar(texto):
    texto = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), texto, flags=re.S)
    texto = re.sub(r"`[^`\n]*`", " ", texto)
    texto = re.sub(r"\]\([^)]*\)", "] ", texto)        # destinos de enlaces e imágenes
    texto = re.sub(r"https?://\S+", " ", texto)
    texto = re.sub(r"<!--.*?-->", " ", texto, flags=re.S)
    texto = re.sub(r"^\s*\d+[.)]\s", " ", texto, flags=re.M)  # listas numeradas
    # niveles de confianza y significancia: parámetros del método, no resultados
    texto = re.sub(r"\b(IC|CI|intervalo de confianza|confianza)( del| de)?\s*\d{2}(?:[.,]\d)?\s*%", " ", texto, flags=re.I)
    texto = re.sub(r"\d{2}(?:[.,]\d)?\s*%\s*de\s*confianza", " ", texto, flags=re.I)
    texto = re.sub(r"\b(p|α|alfa|alpha)\s*[<=>≤]\s*[\d.,]+", " ", texto, flags=re.I)
    return texto


def lecturas(num):
    """Interpretaciones posibles de '10.138' / '18,4' / '1,234.5' -> [(valor, decimales)]."""
    salida = set()
    for dec, mil in ((",", "."), (".", ",")):
        t = num
        if dec in t and t.count(dec) > 1:
            continue
        partes_mil = t.split(dec)[0]
        if mil in partes_mil and not re.fullmatch(r"\d{1,3}(\%s\d{3})+" % mil, partes_mil):
            continue
        t = t.replace(mil, "").replace(dec, ".")
        try:
            v = float(t)
        except ValueError:
            continue
        salida.add((v, len(t.split(".")[1]) if "." in t else 0))
    return sorted(salida)


def numeros_de(entrada):
    if isinstance(entrada, bool):
        return []
    if isinstance(entrada, (int, float)):
        return [float(entrada)]
    if isinstance(entrada, dict):
        return [x for v in entrada.values() for x in numeros_de(v)]
    if isinstance(entrada, (list, tuple)):
        return [x for v in entrada for x in numeros_de(v)]
    return []


def formas(v, escala):
    base = [v, abs(v), v * 100, abs(v) * 100]
    return [b / escala for b in base]


def respaldado(valor, decimales, cifras, escala):
    tol = 0.5 * 10 ** (-decimales) + 1e-9
    for nombre, vals in cifras.items():
        for v in vals:
            for f in formas(v, escala):
                if math.isfinite(f) and abs(f - valor) <= tol:
                    return nombre
    return None


def cargar_cifras(ruta):
    data = json.loads(Path(ruta).read_text(encoding="utf-8"))
    ignorar = set(map(str, data.get("ignorar", []))) if isinstance(data, dict) else set()
    bloque = data.get("cifras", data) if isinstance(data, dict) else {}
    cifras = {k: numeros_de(v) for k, v in bloque.items() if k != "ignorar"}
    return {k: v for k, v in cifras.items() if v}, ignorar


def verificar(texto, cifras, ignorar, estricto=False):
    ok, faltan, omitidos = [], [], 0
    for n_linea, linea in enumerate(limpiar(texto).splitlines(), 1):
        for m in NUM.finditer(linea):
            num, cola = m.group("num"), (m.group("cola") or "").strip()
            crudo = (m.group("signo") + num + (" " + cola if cola else "")).strip()
            if num in ignorar or crudo in ignorar:
                omitidos += 1
                continue
            opciones = lecturas(num)
            if not opciones:
                continue
            v0, d0 = opciones[0]
            if d0 == 0 and 1900 <= v0 <= 2100 and not cola:
                omitidos += 1
                continue
            if not estricto and d0 == 0 and 0 <= v0 <= 10 and not cola:
                omitidos += 1
                continue
            escala = ESCALAS.get(cola.lower(), 1) if cola and cola != "%" else 1
            signo = -1 if m.group("signo") in ("-", "−") else 1
            encontrado = None
            for v, d in opciones:
                encontrado = respaldado(signo * v, d, cifras, escala)
                if encontrado:
                    break
            registro = {"linea": n_linea, "numero": crudo,
                        "contexto": linea.strip()[max(0, m.start() - 40): m.end() + 40]}
            if encontrado:
                ok.append({**registro, "cifra": encontrado})
            else:
                faltan.append(registro)
    return ok, faltan, omitidos


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("informe")
    ap.add_argument("cifras")
    ap.add_argument("--estricto", action="store_true", help="exigir también enteros de 0 a 10")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    for r in (a.informe, a.cifras):
        if not Path(r).is_file():
            sys.stderr.write(f"No existe: {r}\n")
            return 2
    try:
        cifras, ignorar = cargar_cifras(a.cifras)
    except (json.JSONDecodeError, AttributeError) as e:
        sys.stderr.write(f"cifras.json inválido: {e}\n")
        return 2
    texto = Path(a.informe).read_text(encoding="utf-8")
    ok, faltan, omitidos = verificar(texto, cifras, ignorar, a.estricto)
    usadas = {r["cifra"] for r in ok}
    print(json.dumps({
        "respaldados": len(ok), "sin_respaldo": len(faltan), "omitidos": omitidos,
        "cifras_sin_usar": sorted(set(cifras) - usadas), "faltan": faltan,
    }, ensure_ascii=False, indent=2))
    return 1 if faltan else 0


if __name__ == "__main__":
    sys.exit(main())
