"""Verifica que una cápsula conserve las entidades protegidas del original.

Extrae con regex del texto ORIGINAL las entidades que optimizador-tokens
nunca puede alterar y comprueba que cada una aparezca, carácter por
carácter, en la CÁPSULA. Convierte "sin pérdida" en un criterio verificable.

Categorías extraídas:
    url        http(s)://...
    ruta       rutas de archivo/carpeta y rutas de API (a/b.md, ui/, /tareas);
               se normalizan quitando prefijos ./ y ../ (la cápsula puede usar
               la ruta relativa a la raíz del repo)
    id_tarea   T1, M6, RF2, RNF1
    version    1.2, 3.10.4, v2.1.0
    puerto     localhost:5173, 127.0.0.1:8080, "puerto 3000", "port 8080"
    uuid       550e8400-e29b-41d4-a716-446655440000
    hash       hex de 7 a 64 caracteres con letras y dígitos (commits, sha256)
    literal    texto entre `comillas invertidas` (valores exactos: enums,
               campos, códigos de estado, comandos), hasta 80 caracteres

Además falla si la cápsula contiene algo con forma de credencial (las
credenciales nunca se copian ni se comprimen: se omiten y se avisa). Las
credenciales del original no se exigen en la cápsula.

Uso:
    python verificar_entidades.py ORIGINAL CAPSULA [--sin CATEGORIA ...]
                                  [--extra REGEX ...] [--ignorar TEXTO ...]

    --sin       desactiva una categoría (p. ej. --sin literal)
    --extra     agrega un patrón propio (se toma el grupo 0)
    --ignorar   entidad concreta que se acepta perder (queda listada en el JSON
                como "ignoradas", para que la omisión sea explícita)

Salida: JSON por stdout. Códigos de salida:
    0  todas las entidades protegidas están en la cápsula
    1  falta al menos una entidad protegida
    2  error de uso (archivo inexistente, regex inválida)
    3  la cápsula contiene algo con forma de credencial
"""
import argparse
import json
import re
import sys
from pathlib import Path

EXT = r"(?:md|py|ya?ml|json|html?|css|jsx?|tsx?|txt|sh|ps1|toml|ini|cfg|csv|sql|go|rs|java|kt|swift|rb|php|lock|env)"

PATRONES = {
    "url": r"https?://[^\s<>()\[\]`\"']+",
    # a/b, a/b/c.ext, carpeta/ , /ruta-api ; exige una letra en algún segmento
    "ruta": (
        r"(?<![\w/.:-])"
        r"(?:\.{1,2}/)*"
        r"(?:"
        r"[\w.-]+(?:/[\w.-]+)+/?"            # a/b, a/b/c.md
        r"|[\w-]+/(?=[\s`)\],;:]|$)"         # carpeta/
        r"|/[A-Za-z_][\w.-]*(?:/[\w{}:.-]+)*" # /tareas, /api/v1/x, /x.md
        r"|[\w-]+\." + EXT + r"\b"           # archivo.md
        r")"
    ),
    "id_tarea": r"\b(?:T|M|RF|RNF)\d+\b",
    "version": r"\bv?\d+\.\d+(?:\.\d+)*\b",
    "puerto": r"(?:\b(?:localhost|127\.0\.0\.1|0\.0\.0\.0)|\b(?:puerto|port))[:\s]\s*\d{2,5}\b",
    "uuid": r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b",
    "hash": r"\b(?=[0-9a-f]*[a-f])(?=[0-9a-f]*\d)[0-9a-f]{7,64}\b",
    "literal": r"`([^`\n]{1,80})`",
}

CREDENCIALES = [
    r"sk-ant-[\w-]{10,}",
    r"\bsk-[A-Za-z0-9]{20,}",
    r"\bgh[pousr]_[A-Za-z0-9]{20,}",
    r"\bAKIA[0-9A-Z]{16}\b",
    r"\bxox[abprs]-[\w-]{10,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"(?i)\b(?:api[_-]?key|secret|password|passwd|contraseña|token)\s*[:=]\s*['\"]?[^\s'\"`]{8,}",
]


def normalizar_ruta(r: str) -> str:
    r = re.sub(r"^(?:\.{1,2}/)+", "", r)
    return r.rstrip(".,;:")


def parece_ruta(ent: str) -> bool:
    """Filtra pares de prosa con barra ("filtro/orden", "HTML/CSS/JS",
    "vacío/faltante"): una ruta relativa sin extensión solo cuenta si termina
    en "/" o algún segmento tiene "-", "_" o "."."""
    if len(ent) < 3 or not re.search(r"[A-Za-z]", ent):
        return False
    if ent.startswith("/") or ent.endswith("/"):
        return True
    if re.search(r"\." + EXT + r"$", ent):
        return True
    return bool(re.search(r"[-_.]", ent)) and ent.isascii()


def es_credencial(texto: str) -> bool:
    return any(re.search(p, texto) for p in CREDENCIALES)


def extraer(texto: str, categorias: dict) -> dict:
    encontradas = {}
    sin_uuid = re.sub(PATRONES["uuid"], " ", texto)  # los trozos de un UUID no son hashes
    for cat, patron in categorias.items():
        vistos = []
        fuente = sin_uuid if cat == "hash" else texto
        for m in re.finditer(patron, fuente):
            ent = m.group(1) if cat == "literal" else m.group(0)
            if cat == "ruta":
                ent = normalizar_ruta(ent)
                if not parece_ruta(ent):
                    continue
            if cat == "url":
                ent = ent.rstrip(".,;:")
            ent = ent.strip()
            if ent and not es_credencial(ent) and ent not in vistos:
                vistos.append(ent)
        if vistos:
            encontradas[cat] = vistos
    return encontradas


def leer(ruta: str) -> str:
    p = Path(ruta)
    if not p.is_file():
        raise FileNotFoundError(ruta)
    return p.read_text(encoding="utf-8")


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Comprueba que la cápsula conserve las entidades protegidas.")
    ap.add_argument("original")
    ap.add_argument("capsula")
    ap.add_argument("--sin", nargs="*", default=[], choices=sorted(PATRONES), metavar="CATEGORIA")
    ap.add_argument("--extra", nargs="*", default=[], metavar="REGEX")
    ap.add_argument("--ignorar", nargs="*", default=[], metavar="TEXTO")
    args = ap.parse_args(argv)

    try:
        original, capsula = leer(args.original), leer(args.capsula)
        categorias = {c: p for c, p in PATRONES.items() if c not in args.sin}
        for i, p in enumerate(args.extra):
            re.compile(p)
            categorias[f"extra_{i + 1}"] = p
    except FileNotFoundError as e:
        print(f"error: no existe el archivo: {e}", file=sys.stderr)
        return 2
    except re.error as e:
        print(f"error: regex inválida en --extra: {e}", file=sys.stderr)
        return 2

    entidades = extraer(original, categorias)
    faltantes, ignoradas, total = {}, [], 0
    for cat, ents in entidades.items():
        for ent in ents:
            total += 1
            if ent in capsula:
                continue
            if ent in args.ignorar:
                ignoradas.append(ent)
                continue
            faltantes.setdefault(cat, []).append(ent)

    credencial = es_credencial(capsula)
    salida = {
        "original": args.original,
        "capsula": args.capsula,
        "entidades_revisadas": total,
        "por_categoria": {c: len(v) for c, v in entidades.items()},
        "faltantes": faltantes,
        "ignoradas": ignoradas,
        "credencial_en_capsula": credencial,
        "entidades_preservadas": not faltantes and not credencial,
    }
    json.dump(salida, sys.stdout, ensure_ascii=False, indent=2)
    print()
    if credencial:
        return 3
    return 1 if faltantes else 0


if __name__ == "__main__":
    sys.exit(main())
