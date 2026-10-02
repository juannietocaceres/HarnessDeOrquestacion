"""Checks reproducibles de un contrato de T2 (panel-tareas-demo) para la
prueba de retención de optimizador-tokens.

Uso:
    python verificar_t2.py ruta/a/contrato-tareas.md [otra ...]

Por cada archivo imprime cada check (OK/FALLA) y un resumen JSON. Los checks
C1–C4 son los criterios de aceptación de la spec de T2; F1–F9 son detalles de
fidelidad del contexto (los que una compresión mala perdería: UUID v4, máx.
200 caracteres, enum exacto, fuera de alcance, etc.). Sale con código 1 si
algún archivo falla algún check. Solo biblioteca estándar.
"""
import json
import re
import sys
from pathlib import Path

CAMPOS = {"id", "titulo", "estado", "fecha_creacion"}
ENUM = {"pendiente", "en_curso", "hecha"}
UUID4 = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", re.I)
ISO_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$")


def bloques_json(texto):
    """Devuelve [(posicion, objeto | None si no parsea)]."""
    out = []
    for m in re.finditer(r"```json[^\n]*\n(.*?)```", texto, re.S):
        try:
            out.append((m.start(), json.loads(m.group(1))))
        except json.JSONDecodeError:
            out.append((m.start(), None))
    return out


def es_tarea(o):
    return isinstance(o, dict) and set(o) == CAMPOS


def tarea_valida(o):
    return (es_tarea(o) and o["estado"] in ENUM and isinstance(o["titulo"], str)
            and o["titulo"].strip() and ISO_Z.match(str(o["fecha_creacion"])) is not None)


def seccion(texto, patron):
    """Texto desde el primer encabezado que matchea hasta el siguiente del mismo nivel o superior."""
    m = re.search(r"^(#+)[^\n]*" + patron + r"[^\n]*$", texto, re.M | re.I)
    if not m:
        return ""
    nivel = len(m.group(1))
    resto = texto[m.end():]
    fin = re.search(r"^#{1,%d}\s" % nivel, resto, re.M)
    return resto[: fin.start()] if fin else resto


def checks(texto):
    bl = bloques_json(texto)
    objs = [o for _, o in bl if o is not None]
    post = seccion(texto, r"POST\s+/tareas") or texto
    get = seccion(texto, r"GET\s+/tareas") or texto
    post_objs = [o for _, o in bloques_json(post) if o is not None]
    get_objs = [o for _, o in bloques_json(get) if o is not None]
    plano = re.sub(r"\s+", " ", texto)
    r = {}
    r["C1 POST con request y response JSON (201, objeto completo)"] = (
        any(isinstance(o, dict) and set(o) <= {"titulo"} and "titulo" in o for o in post_objs)
        and any(tarea_valida(o) for o in post_objs) and "201" in post)
    r["C2 GET con response JSON array (200)"] = (
        any(isinstance(o, list) and o and all(tarea_valida(t) for t in o) for o in get_objs)
        and "200" in get)
    r["C3 error 400 con payload JSON que identifica titulo"] = (
        "400" in texto and any(isinstance(o, dict) and not es_tarea(o) and "titulo" in json.dumps(o, ensure_ascii=False)
                               and o != {"titulo": o.get("titulo")} for o in objs))
    r["C4 explícito: id, estado, fecha_creacion los asigna el servidor, nunca el cliente"] = bool(
        re.search(r"servidor", plano, re.I) and re.search(r"nunca", plano, re.I)
        and all(f in texto for f in ("id", "estado", "fecha_creacion"))
        and re.search(r"(asigna|genera|calcula)[^.]{0,120}servidor|servidor[^.]{0,120}(asigna|genera|calcula)", plano, re.I))
    r["F1 todos los bloques json parsean"] = bool(bl) and all(o is not None for _, o in bl)
    tareas = [o for o in objs if es_tarea(o)] + [t for o in objs if isinstance(o, list) for t in o if isinstance(t, dict)]
    r["F2 toda tarea de ejemplo tiene exactamente los 4 campos de T1"] = bool(tareas) and all(es_tarea(t) for t in tareas)
    r["F3 ids de ejemplo son UUID v4"] = bool(tareas) and all(UUID4.match(str(t.get("id", ""))) for t in tareas)
    r["F4 estado inicial pendiente al crear"] = any(tarea_valida(o) and o["estado"] == "pendiente" for o in post_objs)
    r["F5 fechas ISO 8601 UTC con Z"] = bool(tareas) and all(ISO_Z.match(str(t.get("fecha_creacion", ""))) for t in tareas)
    r["F6 menciona UUID v4 e ISO 8601 / UTC"] = bool(re.search(r"UUID\s*v?4", texto, re.I) and re.search(r"ISO\s*8601", texto) and "UTC" in texto)
    r["F7 enum exacto pendiente/en_curso/hecha"] = all(v in texto for v in ENUM)
    r["F8 límite de 200 caracteres de titulo (de T1)"] = bool(re.search(r"\b200\b[^.\n]{0,40}caracter", texto, re.I))
    r["F9 fuera de alcance: PATCH/PUT/DELETE, autenticación, paginación"] = all(
        re.search(p, texto, re.I) for p in (r"PATCH|PUT", r"DELETE", r"autenticaci", r"paginaci"))
    return r


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if not argv:
        print(__doc__)
        return 2
    resumen, fallo = {}, False
    for ruta in argv:
        p = Path(ruta)
        if not p.is_file():
            print(f"error: no existe {ruta}", file=sys.stderr)
            return 2
        res = checks(p.read_text(encoding="utf-8"))
        print(f"== {ruta}")
        for k, v in res.items():
            print(f"  {'OK   ' if v else 'FALLA'} {k}")
        ok = sum(res.values())
        resumen[ruta] = {"ok": ok, "total": len(res), "fallas": [k for k, v in res.items() if not v]}
        fallo = fallo or ok < len(res)
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    return 1 if fallo else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
