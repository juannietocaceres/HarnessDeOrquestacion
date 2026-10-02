"""Mide caracteres y tokens de textos para optimizador-tokens.

Solo usa la biblioteca estándar de Python. El conteo por defecto es una
estimación (caracteres // 4, "metodo": "estimado"). Con --api, y solo si
existe la variable de entorno ANTHROPIC_API_KEY, usa el endpoint oficial
POST /v1/messages/count_tokens ("metodo": "api"); si la variable no existe o
la llamada falla, vuelve a la estimación y lo dice en el JSON. La clave
nunca se imprime ni se escribe en ningún archivo.

Uso:
    # Contar uno o más archivos (o "-" para stdin)
    python medir_tokens.py archivo.md [otro.md ...]

    # Comparar original vs. comprimido: métricas del JSON de salida de la skill
    python medir_tokens.py --comparar original.md capsula.md

    # Costo de contexto de las descriptions de las skills de una carpeta
    python medir_tokens.py --descriptions .claude/skills [--excluir nombre ...]

Opciones comunes:
    --api            usa el conteo oficial si hay ANTHROPIC_API_KEY
    --modelo ID      modelo para el conteo oficial (por defecto claude-opus-5-5;
                     el tokenizador cambia según el modelo)

Salida: JSON por stdout. Código de salida 0 si midió, 2 si hubo un error de
uso (archivo inexistente, frontmatter ilegible, argumentos inválidos).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

URL_CONTEO = "https://api.anthropic.com/v1/messages/count_tokens"
# Solo para pruebas: permite apuntar a un servidor local. Cualquier otro host
# se ignora, para que la clave nunca se envíe fuera de api.anthropic.com.
_URL_PRUEBA = os.environ.get("OPTIMIZADOR_TOKENS_URL_PRUEBA", "")
if _URL_PRUEBA.startswith(("http://127.0.0.1:", "http://localhost:")):
    URL_CONTEO = _URL_PRUEBA
VERSION_API = "2023-06-01"
MODELO_POR_DEFECTO = "claude-opus-5-5"


class ErrorUso(Exception):
    pass


def leer(ruta: str) -> str:
    if ruta == "-":
        return sys.stdin.read()
    p = Path(ruta)
    if not p.is_file():
        raise ErrorUso(f"no existe el archivo: {ruta}")
    return p.read_text(encoding="utf-8")


def estimar(texto: str) -> int:
    """Estimación usada en todo el harness: caracteres // 4."""
    return len(texto) // 4


def contar_api(texto: str, modelo: str, clave: str) -> int:
    """Conteo oficial. Gratis pero con límite de requests por minuto."""
    cuerpo = json.dumps(
        {"model": modelo, "messages": [{"role": "user", "content": texto or " "}]}
    ).encode("utf-8")
    req = urllib.request.Request(
        URL_CONTEO,
        data=cuerpo,
        headers={
            "x-api-key": clave,
            "anthropic-version": VERSION_API,
            "content-type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return int(json.load(resp)["input_tokens"])


class Contador:
    """Decide el método una vez y lo aplica a todos los textos de la corrida."""

    def __init__(self, usar_api: bool, modelo: str):
        self.modelo = modelo
        self.clave = os.environ.get("ANTHROPIC_API_KEY") if usar_api else None
        self.metodo = "api" if self.clave else "estimado"
        self.aviso = None
        if usar_api and not self.clave:
            self.aviso = "ANTHROPIC_API_KEY no definida: se usó la estimación"

    def contar_todos(self, textos: list) -> list:
        """Cuenta todos los textos con un único método: si el conteo oficial
        falla en cualquiera, toda la corrida pasa a estimado (no se mezclan)."""
        if self.metodo == "api":
            try:
                return [contar_api(t, self.modelo, self.clave) for t in textos]
            except (urllib.error.URLError, KeyError, ValueError, OSError) as e:
                self.metodo = "estimado"
                self.aviso = f"falló el conteo oficial ({type(e).__name__}): se usó la estimación"
        return [estimar(t) for t in textos]

    def info(self) -> dict:
        d = {"metodo": self.metodo}
        if self.metodo == "api":
            d["modelo"] = self.modelo
        if self.aviso:
            d["aviso"] = self.aviso
        return d


def ahorro(original: int, final: int) -> str:
    if original <= 0:
        return "0%"
    return f"{round(100 * (original - final) / original)}%"


def leer_frontmatter(texto: str, ruta: str) -> dict:
    """Parser mínimo de frontmatter YAML: claves de primer nivel escalares,
    valores en una línea (con o sin comillas) o bloques > / | indentados."""
    lineas = texto.splitlines()
    if not lineas or lineas[0].strip() != "---":
        raise ErrorUso(f"sin frontmatter: {ruta}")
    try:
        fin = next(i for i in range(1, len(lineas)) if lineas[i].strip() == "---")
    except StopIteration:
        raise ErrorUso(f"frontmatter sin cerrar: {ruta}")
    datos, i = {}, 1
    while i < fin:
        linea = lineas[i]
        if not linea.strip() or linea.startswith((" ", "\t", "#")) or ":" not in linea:
            i += 1
            continue
        clave, valor = linea.split(":", 1)
        valor = valor.strip()
        if valor in (">", "|", ">-", "|-", ">+", "|+"):
            bloque = []
            i += 1
            while i < fin and (lineas[i].startswith((" ", "\t")) or not lineas[i].strip()):
                bloque.append(lineas[i].strip())
                i += 1
            sep = " " if valor.startswith(">") else "\n"
            datos[clave.strip()] = sep.join(b for b in bloque if b).strip()
            continue
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
            valor = valor[1:-1]
        datos[clave.strip()] = valor
        i += 1
    return datos


def origen_skill(carpeta: Path, fm: dict) -> str:
    lic = carpeta / "LICENSE.txt"
    if lic.is_file() and "Emil Kowalski" in lic.read_text(encoding="utf-8", errors="replace"):
        return "emil"
    if "license" in fm:
        return "vendorizada-otra"
    return "propia"


def medir_descriptions(dir_skills: str, excluir: list, contador: Contador) -> dict:
    base = Path(dir_skills)
    if not base.is_dir():
        raise ErrorUso(f"no existe la carpeta: {dir_skills}")
    skills = []
    for skill_md in sorted(base.glob("*/SKILL.md")):
        carpeta = skill_md.parent
        if carpeta.name in excluir:
            continue
        fm = leer_frontmatter(skill_md.read_text(encoding="utf-8"), str(skill_md))
        nombre = fm.get("name", carpeta.name)
        desc = fm.get("description", "")
        # Lo que entra en la lista de skills: nombre + descripción (+ when_to_use).
        listado = f"{nombre}: {desc}"
        if fm.get("when_to_use"):
            listado += " " + fm["when_to_use"]
        oculta = fm.get("disable-model-invocation", "").lower() == "true"
        skills.append({
            "skill": carpeta.name,
            "origen": origen_skill(carpeta, fm),
            "caracteres": len(listado),
            "_texto": listado,
            "disable_model_invocation": oculta,
            "en_contexto": not oculta,
            "caracteres_skill_md": len(skill_md.read_text(encoding="utf-8")),
        })
    for s, t in zip(skills, contador.contar_todos([s.pop("_texto") for s in skills])):
        s["tokens"] = t
    grupos = {}
    for s in skills:
        for g in ("total", s["origen"]):
            acc = grupos.setdefault(g, {"skills": 0, "en_contexto": 0, "caracteres_en_contexto": 0, "tokens_en_contexto": 0})
            acc["skills"] += 1
            if s["en_contexto"]:
                acc["en_contexto"] += 1
                acc["caracteres_en_contexto"] += s["caracteres"]
                acc["tokens_en_contexto"] += s["tokens"]
    return {"modo": "descriptions", "carpeta": dir_skills, "excluidas": excluir,
            "skills": skills, "resumen": grupos, **contador.info()}


def main(argv=None) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Mide caracteres y tokens (estimados u oficiales).")
    ap.add_argument("archivos", nargs="*", help="archivos a contar ('-' = stdin)")
    ap.add_argument("--comparar", nargs=2, metavar=("ORIGINAL", "FINAL"))
    ap.add_argument("--descriptions", metavar="DIR_SKILLS")
    ap.add_argument("--excluir", nargs="*", default=[], metavar="SKILL")
    ap.add_argument("--api", action="store_true")
    ap.add_argument("--modelo", default=MODELO_POR_DEFECTO)
    args = ap.parse_args(argv)

    modos = sum(bool(x) for x in (args.archivos, args.comparar, args.descriptions))
    if modos != 1:
        print("error: usa exactamente uno: archivos, --comparar o --descriptions", file=sys.stderr)
        return 2

    contador = Contador(args.api, args.modelo)
    try:
        if args.comparar:
            orig, fin = (leer(r) for r in args.comparar)
            t_o, t_f = contador.contar_todos([orig, fin])
            salida = {
                "original": args.comparar[0], "final": args.comparar[1],
                "caracteres_original": len(orig), "caracteres_final": len(fin),
                "metricas": {"tokens_original": t_o, "tokens_final": t_f,
                             "ahorro": ahorro(t_o, t_f), **contador.info()},
            }
        elif args.descriptions:
            salida = medir_descriptions(args.descriptions, args.excluir, contador)
        else:
            textos = [leer(r) for r in args.archivos]
            items = [{"archivo": r, "caracteres": len(t), "tokens": n}
                     for r, t, n in zip(args.archivos, textos, contador.contar_todos(textos))]
            salida = {"archivos": items, **contador.info()}
    except ErrorUso as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    json.dump(salida, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
