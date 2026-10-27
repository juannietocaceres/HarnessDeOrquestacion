"""Perfil de calidad de un dataset, para leer el resumen y no el archivo.

Lee CSV/TSV/TXT, Excel, Parquet o JSON/JSONL y escribe:
    <salida>.md    resumen legible (lo lee el agente o la persona)
    <salida>.json  el mismo perfil, estructurado (lo leen otros scripts)

Por columna: tipo leído, tipo sugerido, nulos (incluye "", "NA", "N/A",
"null", "-", "?"), únicos, valores más frecuentes, estadísticos y outliers
por IQR si es numérica, números guardados como texto, fechas como texto,
espacios sobrantes, variantes de escritura de una misma categoría
("Bogotá" / "bogota "), columna constante y posibles datos personales.
De columnas con posibles datos personales (incluye salud: fecha de
nacimiento, historia clínica, num_ide/tip_ide, barrio, paciente) NO se
muestran valores.

Por dataset: filas, columnas, filas duplicadas exactas, llaves candidatas
y aviso de cuasi-identificadores (edad o fecha de nacimiento + sexo +
ubicación fina en el mismo archivo, aunque no haya nombres).

Uso:
    python perfilar.py ARCHIVO [--salida perfil] [--hoja NOMBRE]
                       [--sep ,] [--max-filas N] [--top 5]

Códigos de salida: 0 ok, 2 error de uso o de lectura.
"""
import argparse
import csv
import json
import re
import sys
import unicodedata
import warnings
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
except ImportError:  # pragma: no cover
    sys.stderr.write("Falta pandas/numpy: pip install pandas\n")
    sys.exit(2)

warnings.filterwarnings("ignore")

TOKENS_NULOS = {"", "na", "n/a", "nan", "null", "none", "-", "--", "?", "sin dato", "s/d", "nd", "n.d."}
PII_NOMBRE = re.compile(
    r"(e-?mail|correo|tel[eé]fono|celular|m[oó]vil|phone|c[eé]dula|documento|"
    r"\bdni\b|\bnit\b|\bcc\b|pasaporte|direcci[oó]n|address|nombre|apellido|"
    r"name|\bip\b|ssn|tarjeta|cuenta|"
    # salud y registros administrativos (SIVIGILA, RIPS, historias clínicas)
    r"fec_?nac|nacimiento|historia_?cl[ií]nica|\bhc\b|num_?ide|tip_?ide|"
    r"identificaci[oó]n|barrio|vereda|paciente)", re.I)
# Cuasi-identificadores: juntos permiten reconocer a alguien aunque no haya nombres.
CUASI_EDAD = re.compile(r"(?<![a-záéíóú])edad|\bage\b|fec_?nac|nacimiento|birth", re.I)
CUASI_SEXO = re.compile(r"sexo|g[eé]nero|\bsex\b|gender", re.I)
CUASI_LUGAR = re.compile(r"barrio|direcci[oó]n|address|vereda|manzana|corregimiento|"
                         r"latitud|longitud|\blat\b|\blon\b|coordenad", re.I)
PII_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
PII_TEL = re.compile(r"^\+?[\d\s().-]{7,}$")
FECHA_TXT = re.compile(r"\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}")
MONEDA = re.compile(r"[$€£%\s]|COP|USD|EUR", re.I)


def leer(ruta, hoja=None, sep=None, max_filas=None):
    ext = ruta.suffix.lower()
    if ext in (".xlsx", ".xlsm", ".xls"):
        return pd.read_excel(ruta, sheet_name=hoja or 0, dtype=object, nrows=max_filas)
    if ext == ".parquet":
        df = pd.read_parquet(ruta)
        return df.head(max_filas) if max_filas else df
    if ext in (".json", ".jsonl", ".ndjson"):
        return pd.read_json(ruta, lines=ext != ".json", dtype=False)
    for codif in ("utf-8-sig", "latin-1"):
        try:
            with open(ruta, encoding=codif, newline="") as f:
                muestra = f.read(65536)
            separador = sep
            if separador is None:
                try:
                    separador = csv.Sniffer().sniff(muestra, delimiters=",;\t|").delimiter
                except csv.Error:
                    separador = ","
            return pd.read_csv(ruta, sep=separador, dtype=str, keep_default_na=False,
                               encoding=codif, nrows=max_filas)
        except UnicodeDecodeError:
            continue
    raise ValueError("no se pudo decodificar el archivo (ni utf-8 ni latin-1)")


def normalizar_txt(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().lower()


def a_numero(s, miles_punto=False):
    """'$ 1.234,5' -> 1234.5 ; '1,234.5' -> 1234.5 ; None si no es número.

    '1.200' es ambiguo (1,2 o 1200): con miles_punto=True (la columna usa el
    punto como separador de miles, ver usa_miles_punto) se lee 1200.
    """
    t = MONEDA.sub("", str(s))
    if not t or not re.fullmatch(r"[-+]?[\d.,]+", t):
        return None
    if "," in t and "." in t:
        dec = "," if t.rfind(",") > t.rfind(".") else "."
        t = t.replace("." if dec == "," else ",", "").replace(",", ".")
    elif "," in t:
        t = t.replace(",", "") if re.fullmatch(r"[-+]?\d{1,3}(,\d{3})+", t) else t.replace(",", ".")
    elif re.fullmatch(r"[-+]?\d{1,3}(\.\d{3}){2,}", t) or (
            miles_punto and re.fullmatch(r"[-+]?\d{1,3}(\.\d{3})+", t)):
        t = t.replace(".", "")
    try:
        return float(t)
    except ValueError:
        return None


def usa_miles_punto(s):
    """True si todo valor con punto lo usa como miles (1.200, 98.000) y ninguno como decimal."""
    t = s.map(lambda x: MONEDA.sub("", str(x)))
    con_punto = t[t.str.contains(".", regex=False) & ~t.str.contains(",", regex=False)]
    return bool(len(con_punto)) and con_punto.str.fullmatch(r"[-+]?\d{1,3}(\.\d{3})+").all()


def es_texto(serie):
    return serie.dtype == object or pd.api.types.is_string_dtype(serie)


def recortar(v, n=40):
    v = str(v)
    return v if len(v) <= n else v[: n - 1] + "…"


def perfil_columna(nombre, serie, top):
    n = len(serie)
    col = {"columna": str(nombre), "tipo_leido": str(serie.dtype), "alertas": []}
    texto = es_texto(serie)
    if texto:
        crudo = serie.astype("string")
        es_nulo = crudo.isna() | crudo.str.strip().str.lower().isin(TOKENS_NULOS)
        tokens = int((~crudo.isna() & es_nulo).sum())
        if tokens:
            col["alertas"].append(f"{tokens} valores tipo nulo escritos como texto ('', 'NA', '-'...)")
    else:
        es_nulo = serie.isna()
    validos = serie[~es_nulo]
    col["nulos"] = int(es_nulo.sum())
    col["nulos_pct"] = round(100 * col["nulos"] / n, 1) if n else 0.0
    col["unicos"] = int(validos.astype(str).nunique())

    pii = bool(PII_NOMBRE.search(str(nombre)))
    if texto and len(validos):
        muestra = validos.astype(str).head(500)
        if muestra.str.match(PII_EMAIL).mean() > 0.5 or (
                muestra.str.match(PII_TEL).mean() > 0.8 and muestra.str.len().mean() >= 7
                and not muestra.map(lambda x: a_numero(x) is not None and "." in x).mean() > 0.5):
            pii = True
    col["pii"] = pii

    sugerido = "vacia" if not len(validos) else "texto"
    if len(validos) and col["unicos"] == 1:
        col["alertas"].append("columna constante: no aporta al análisis")

    if not texto and pd.api.types.is_numeric_dtype(serie) and not pd.api.types.is_bool_dtype(serie):
        sugerido = "numero"
        nums = pd.to_numeric(validos, errors="coerce").dropna()
    elif not texto and pd.api.types.is_datetime64_any_dtype(serie):
        sugerido, nums = "fecha", None
        col["rango"] = [str(validos.min()), str(validos.max())]
    elif texto and len(validos):
        s = validos.astype(str)
        miles = usa_miles_punto(s)
        convertidos = s.map(lambda x: a_numero(x, miles))
        frac_num = convertidos.notna().mean()
        if frac_num >= 0.9:
            sugerido = "numero"
            nums = convertidos.dropna().astype(float)
            if (s.str.strip() != s).any() or s.str.contains(r"[$€,%]|\.\d{3}\b").any():
                col["alertas"].append("número guardado como texto (símbolos, separadores o espacios): convertir")
            elif frac_num < 1:
                col["alertas"].append(f"{int((1 - frac_num) * len(s))} valores no numéricos en columna numérica")
            if frac_num < 1:
                malos = s[convertidos.isna()].unique()[:3]
                col["no_convertibles"] = [recortar(x) for x in malos]
        else:
            nums = None
            if s.str.contains(FECHA_TXT).mean() >= 0.9:
                fechas = pd.to_datetime(s, errors="coerce", format="mixed", dayfirst=True)
                if fechas.notna().mean() >= 0.9:
                    sugerido = "fecha"
                    col["rango"] = [str(fechas.min().date()), str(fechas.max().date())]
                    col["alertas"].append("fecha guardada como texto: convertir con formato explícito")
                    primeros = s.str.extract(r"^(\d{1,2})[-/.](\d{1,2})[-/.]").dropna().astype(int)
                    if len(primeros) and (primeros.max() <= 12).all():
                        col["alertas"].append("formato día/mes ambiguo: confirmar el orden antes de convertir")
                    if fechas.isna().any():
                        col["no_convertibles"] = [recortar(x) for x in s[fechas.isna()].unique()[:3]]
            if sugerido == "texto":
                if s.str.lower().isin({"si", "sí", "no", "true", "false", "0", "1", "s", "n", "y"}).all():
                    sugerido = "booleano"
                elif col["unicos"] <= max(20, 0.05 * len(s)):
                    sugerido = "categoria"
                elif col["unicos"] == len(s):
                    sugerido = "identificador"
            espacios = int((s != s.str.strip()).sum() + s.str.contains(r"\s{2,}").sum())
            if espacios:
                col["alertas"].append(f"{espacios} valores con espacios sobrantes")
            if sugerido in ("categoria", "texto") and not pii:
                grupos = s.groupby(s.map(normalizar_txt)).agg(lambda g: sorted(g.unique()))
                variantes = [v for v in grupos if len(v) > 1]
                if variantes:
                    col["variantes"] = [[recortar(x, 25) for x in v[:4]] for v in variantes[:5]]
                    col["alertas"].append(f"{len(variantes)} categorías escritas de varias formas: unificar")
    else:
        nums = None
    col["tipo_sugerido"] = sugerido

    if nums is not None and len(nums):
        q1, q3 = nums.quantile([0.25, 0.75])
        iqr = q3 - q1
        fuera = int(((nums < q1 - 1.5 * iqr) | (nums > q3 + 1.5 * iqr)).sum()) if iqr > 0 else 0
        col["estadisticos"] = {k: round(float(v), 4) for k, v in {
            "min": nums.min(), "p25": q1, "mediana": nums.median(), "p75": q3,
            "max": nums.max(), "media": nums.mean(), "desv": nums.std() if len(nums) > 1 else 0}.items()}
        col["outliers_iqr"] = fuera
        if fuera:
            col["alertas"].append(f"{fuera} outliers por IQR ({round(100 * fuera / len(nums), 1)} %): revisar si son reales")
        if (nums < 0).any() and re.search(r"edad|precio|cantidad|valor|monto|age|price|qty", str(nombre), re.I):
            col["alertas"].append(f"{int((nums < 0).sum())} valores negativos en una columna que suele ser positiva")
        if len(nums) > 2 and nums.median() and abs(nums.mean() - nums.median()) / abs(nums.median()) > 0.5:
            col["alertas"].append("distribución muy asimétrica: preferir mediana a media")

    if pii:
        col["alertas"].insert(0, "posible dato personal: no mostrar ni exportar sin autorización")
        col["frecuentes"] = "[oculto: posible dato personal]"
        # min/max de un documento o una fecha de nacimiento es el dato de una persona
        for clave in ("estadisticos", "rango", "no_convertibles", "variantes"):
            col.pop(clave, None)
    else:
        vc = validos.astype(str).value_counts().head(top)
        col["frecuentes"] = [[recortar(k), int(v)] for k, v in vc.items()]
    if col["nulos_pct"] >= 20:
        col["alertas"].append(f"{col['nulos_pct']} % nulos: entender por qué faltan antes de imputar")
    return col


def perfilar(df, top=5):
    columnas = [perfil_columna(c, df[c], top) for c in df.columns]
    dup = int(df.astype(str).duplicated().sum()) if len(df) else 0
    llaves = [c["columna"] for c in columnas
              if c["nulos"] == 0 and c["unicos"] == len(df) and len(df) > 1]
    alertas_ds = []
    if dup:
        alertas_ds.append(f"{dup} filas duplicadas exactas")
    if not llaves:
        alertas_ds.append("ninguna columna identifica cada fila: definir la llave (posible llave compuesta)")
    sin_nombre = [c for c in df.columns if str(c).startswith("Unnamed") or str(c).strip() == ""]
    if sin_nombre:
        alertas_ds.append(f"{len(sin_nombre)} columnas sin nombre (índice exportado o encabezado corrido)")
    nombres = [str(c) for c in df.columns]
    cuasi = {clave: [c for c in nombres if patron.search(c)]
             for clave, patron in (("edad", CUASI_EDAD), ("sexo", CUASI_SEXO), ("lugar", CUASI_LUGAR))}
    if all(cuasi.values()):
        alertas_ds.append(
            "cuasi-identificadores juntos (" + ", ".join(sum(cuasi.values(), [])) + "): edad o fecha de "
            "nacimiento + sexo + ubicación fina permiten reconocer personas aunque no haya nombres; "
            "en informes y gráficos solo agregados y anonimizados (Ley 1581 de 2012)")
    return {
        "filas": int(len(df)), "columnas": int(df.shape[1]), "duplicados_exactos": dup,
        "llaves_candidatas": llaves, "alertas": alertas_ds, "detalle": columnas,
        "columnas_pii": [c["columna"] for c in columnas if c["pii"]],
        "cuasi_identificadores": sum(cuasi.values(), []) if all(cuasi.values()) else [],
    }


def a_markdown(p, nombre_archivo):
    l = [f"# Perfil de `{nombre_archivo}`", "",
         f"- **Filas**: {p['filas']:,} · **Columnas**: {p['columnas']} · "
         f"**Duplicados exactos**: {p['duplicados_exactos']:,}".replace(",", "."),
         f"- **Llaves candidatas**: {', '.join(p['llaves_candidatas']) or 'ninguna'}"]
    if p["columnas_pii"]:
        l.append(f"- **Posibles datos personales**: {', '.join(p['columnas_pii'])}")
    for a in p["alertas"]:
        l.append(f"- ⚠ {a}")
    l += ["", "## Columnas", "", "| Columna | Leído → sugerido | Nulos | Únicos | Resumen |",
          "|---|---|---|---|---|"]
    for c in p["detalle"]:
        if "estadisticos" in c:
            e = c["estadisticos"]
            res = f"min {e['min']:g} · med {e['mediana']:g} · max {e['max']:g}"
        elif "rango" in c:
            res = f"{c['rango'][0]} → {c['rango'][1]}"
        elif isinstance(c["frecuentes"], str):
            res = c["frecuentes"]
        else:
            res = ", ".join(f"{k} ({v})" for k, v in c["frecuentes"][:3])
        res = res.replace("|", "\\|")
        l.append(f"| {c['columna']} | {c['tipo_leido']} → {c['tipo_sugerido']} | "
                 f"{c['nulos']} ({c['nulos_pct']} %) | {c['unicos']} | {res} |")
    con_alertas = [c for c in p["detalle"] if c["alertas"]]
    if con_alertas:
        l += ["", "## Problemas de calidad", ""]
        for c in con_alertas:
            l.append(f"**{c['columna']}**")
            l += [f"- {a}" for a in c["alertas"]]
            if c.get("variantes"):
                l.append("- variantes: " + "; ".join(" / ".join(f"`{x}`" for x in v) for v in c["variantes"]))
            if c.get("no_convertibles"):
                l.append("- no convertibles: " + ", ".join(f"`{x}`" for x in c["no_convertibles"]))
            l.append("")
    return "\n".join(l).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("archivo")
    ap.add_argument("--salida", default="perfil", help="ruta sin extensión (default: perfil)")
    ap.add_argument("--hoja", help="hoja de Excel")
    ap.add_argument("--sep", help="separador de CSV si la detección falla")
    ap.add_argument("--max-filas", type=int, help="leer solo las primeras N filas")
    ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    ruta = Path(a.archivo)
    if not ruta.is_file():
        sys.stderr.write(f"No existe: {ruta}\n")
        return 2
    try:
        df = leer(ruta, a.hoja, a.sep, a.max_filas)
    except Exception as e:  # lectura: cualquier fallo es error de uso
        sys.stderr.write(f"No se pudo leer {ruta}: {e}\n")
        return 2
    p = perfilar(df, a.top)
    p["archivo"] = str(ruta)
    salida = Path(a.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.with_suffix(".json").write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    salida.with_suffix(".md").write_text(a_markdown(p, ruta.name), encoding="utf-8")
    n_alertas = sum(len(c["alertas"]) for c in p["detalle"]) + len(p["alertas"])
    print(json.dumps({"filas": p["filas"], "columnas": p["columnas"], "alertas": n_alertas,
                      "pii": p["columnas_pii"], "md": str(salida.with_suffix(".md"))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
