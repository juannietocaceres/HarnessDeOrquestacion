#!/usr/bin/env python3
"""Valida un triage.json contra schema/triage.schema.json y contra el repo.

Uso:
    python validar_triage.py <ruta/triage.json> [--raiz DIR] [--sin-jsonschema]

  --raiz DIR         carpeta desde la que se resuelven `manifest` y
                     `.claude/skills/` (por defecto, el directorio actual).
  --sin-jsonschema   usa el validador mínimo aunque jsonschema esté instalado.

Comprueba:
  1. El esquema (con `jsonschema` si está instalado; si no, con un validador
     mínimo que cubre las palabras clave que usa triage.schema.json).
  2. Que cada skill de `skills_requeridas` exista en <raiz>/.claude/skills/.
  3. Si `estado` es `listo_para_orquestar`: que el archivo `manifest` exista,
     pase el preflight (preflight_manifest.py) y que todo `tipo` del manifest
     esté en `tipos_requeridos`.
Avisos (no fallan): tipos de `tipos_requeridos` sin ninguna tarea, tipos que
requieren M7.

Código de salida: 0 = válido, 1 = inválido, 2 = no se pudo leer.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DIR_SCRIPTS = Path(__file__).resolve().parent
RUTA_ESQUEMA = DIR_SCRIPTS.parent / "schema" / "triage.schema.json"
sys.path.insert(0, str(DIR_SCRIPTS))

import preflight_manifest as pm  # noqa: E402


# --------------------------------------------------------------------------
# Validador mínimo de JSON Schema (subconjunto usado por triage.schema.json)
# --------------------------------------------------------------------------

_TIPOS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "null": lambda v: v is None,
}


def validar_minimo(valor, esquema: dict, ruta: str = "$") -> list[str]:
    errores: list[str] = []
    if "type" in esquema:
        tipos = esquema["type"] if isinstance(esquema["type"], list) else [esquema["type"]]
        if not any(_TIPOS[t](valor) for t in tipos):
            return [f"{ruta}: se esperaba tipo {'/'.join(tipos)}"]
    if "const" in esquema and valor != esquema["const"]:
        errores.append(f"{ruta}: debe valer {esquema['const']!r}")
    if "enum" in esquema and valor not in esquema["enum"]:
        errores.append(f"{ruta}: {valor!r} no está en {esquema['enum']}")
    if isinstance(valor, str):
        if len(valor) < esquema.get("minLength", 0):
            errores.append(f"{ruta}: texto vacío o demasiado corto")
        if "pattern" in esquema and not re.search(esquema["pattern"], valor):
            errores.append(f"{ruta}: {valor!r} no cumple el patrón {esquema['pattern']}")
    if isinstance(valor, list):
        if len(valor) < esquema.get("minItems", 0):
            errores.append(f"{ruta}: mínimo {esquema['minItems']} elemento/s")
        if "maxItems" in esquema and len(valor) > esquema["maxItems"]:
            errores.append(f"{ruta}: máximo {esquema['maxItems']} elemento/s (tiene {len(valor)})")
        if esquema.get("uniqueItems"):
            vistos = [json.dumps(v, sort_keys=True) for v in valor]
            if len(set(vistos)) != len(vistos):
                errores.append(f"{ruta}: elementos repetidos")
        if "items" in esquema:
            for i, v in enumerate(valor):
                errores += validar_minimo(v, esquema["items"], f"{ruta}[{i}]")
    if isinstance(valor, dict):
        for req in esquema.get("required", []):
            if req not in valor:
                errores.append(f"{ruta}: falta la propiedad requerida '{req}'")
        props = esquema.get("properties", {})
        for k, v in valor.items():
            if k in props:
                errores += validar_minimo(v, props[k], f"{ruta}.{k}")
            elif esquema.get("additionalProperties") is False:
                errores.append(f"{ruta}: propiedad no permitida '{k}'")
    for sub in esquema.get("allOf", []):
        errores += validar_minimo(valor, sub, ruta)
    if "if" in esquema:
        if not validar_minimo(valor, esquema["if"], ruta):
            errores += validar_minimo(valor, esquema.get("then", {}), ruta)
        elif "else" in esquema:
            errores += validar_minimo(valor, esquema["else"], ruta)
    return errores


def validar_esquema(datos, esquema: dict, forzar_minimo: bool = False) -> tuple[list[str], str]:
    if not forzar_minimo:
        try:
            import jsonschema  # type: ignore
        except ImportError:
            pass
        else:
            clase = jsonschema.validators.validator_for(esquema)
            errs = sorted(clase(esquema).iter_errors(datos), key=lambda e: list(e.path))
            return [f"$.{'.'.join(map(str, e.path))}: {e.message}" for e in errs], "jsonschema"
    return validar_minimo(datos, esquema), "validador mínimo"


# --------------------------------------------------------------------------
# Comprobaciones contra el repo
# --------------------------------------------------------------------------

def validar_triage(datos, raiz: Path, forzar_minimo: bool = False) -> dict:
    esquema = json.loads(RUTA_ESQUEMA.read_text(encoding="utf-8"))
    errores, motor = validar_esquema(datos, esquema, forzar_minimo)
    avisos: list[str] = []
    res = {"errores": errores, "avisos": avisos, "motor": motor, "preflight": None}
    if errores or not isinstance(datos, dict):
        return res

    dir_skills = raiz / ".claude" / "skills"
    for s in datos["skills_requeridas"]:
        if not (dir_skills / s / "SKILL.md").is_file():
            errores.append(f"skills_requeridas: '{s}' no existe en {dir_skills.as_posix()}")
    for t in datos["tipos_requeridos"]:
        if t in pm.TIPOS_M7:
            avisos.append(f"tipos_requeridos: '{t}' requiere M7 (aún no está en orquestador §1)")

    if datos["estado"] == "listo_para_orquestar":
        ruta_manifest = raiz / datos["manifest"]
        if not ruta_manifest.is_file():
            errores.append(f"manifest: no existe {datos['manifest']}")
            return res
        try:
            manifest = pm.cargar_yaml(ruta_manifest)
        except (OSError, ValueError) as e:
            errores.append(f"manifest: no se pudo leer {datos['manifest']}: {e}")
            return res
        pf = pm.preflight(manifest)
        res["preflight"] = pf
        errores += [f"preflight del manifest: {e}" for e in pf["errores"]]
        if not pf["errores"]:
            tipos_manifest = {t.get("tipo") for t in manifest["tareas"]}
            for t in sorted(tipos_manifest - set(datos["tipos_requeridos"])):
                errores.append(f"tipos_requeridos: falta '{t}', que usa el manifest")
            for t in sorted(set(datos["tipos_requeridos"]) - tipos_manifest):
                avisos.append(f"tipos_requeridos: '{t}' no lo usa ninguna tarea del manifest")
    return res


def main(argv: list[str]) -> int:
    pm.configurar_salida()
    args = [a for a in argv if not a.startswith("--")]
    raiz = Path(".")
    if "--raiz" in argv:
        i = argv.index("--raiz")
        if i + 1 >= len(argv):
            print(__doc__)
            return 2
        raiz = Path(argv[i + 1])
        args.remove(argv[i + 1])
    if len(args) != 1:
        print(__doc__)
        return 2
    ruta = Path(args[0])
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"ERROR: no se pudo leer {ruta}: {e}")
        return 2
    r = validar_triage(datos, raiz, forzar_minimo="--sin-jsonschema" in argv)
    print(f"Validación de {ruta.as_posix()} (esquema con {r['motor']})")
    for e in r["errores"]:
        print(f"  ERROR: {e}")
    for a in r["avisos"]:
        print(f"  aviso: {a}")
    if r["preflight"] and not r["preflight"]["errores"]:
        print(f"  preflight del manifest: PASA ({len(r['preflight']['waves'])} waves)")
    if r["errores"]:
        print(f"RESULTADO: INVÁLIDO ({len(r['errores'])} error/es)")
        return 1
    print(f"RESULTADO: VÁLIDO (estado: {datos['estado']})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
