#!/usr/bin/env python3
"""Preflight de un milestone.yaml con las mismas reglas que orquestador §4.

Uso:
    python preflight_manifest.py <ruta/milestone.yaml> [--sin-pyyaml]

Reglas (orquestador/SKILL.md §1 y §4):
  - `tareas` es una lista no vacía; `milestone` es un texto no vacío.
  - Todo `id` es único.
  - Toda tarea tiene `id`, `titulo`, `tipo` y `descripcion` no vacíos.
  - Todo `depende_de` resuelve a otro `id` del manifest o está listado en
    `fuera_de_alcance_si_depende_de` de esa tarea (dependencia externa).
  - El grafo de dependencias internas no tiene ciclos.
  - Campos opcionales por tarea: `verificacion_manual` (si está, lista de
    textos no vacíos), `modelo` (si está, texto no vacío: alias como
    sonnet/opus/haiku/fable o un ID completo) y `verificacion` (si está,
    `completa`, `ligera` o `ninguna`; perfil de costo de orquestador §1).
Avisos (no fallan): `tipo` fuera de la lista vigente (que ya incluye
`presentacion` y `contenido`), `criterios_aceptacion` vacío (disparará
`especificacion`), tareas bloqueadas por una dependencia externa.

Salida: errores, avisos y el plan de waves. Código 0 = pasa, 1 = falla,
2 = no se pudo leer el archivo.

Solo usa la biblioteca estándar. Si PyYAML está instalado lo usa para leer
el YAML; si no, usa un lector mínimo que cubre el subconjunto de YAML del
formato de manifest (mapas, listas, `>`/`|`, listas `[a, b]`, comentarios).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NIVELES_VERIFICACION = {"completa", "ligera", "ninguna"}
TIPOS_VIGENTES = {"backend", "frontend", "data", "cli", "mobile", "docs", "testing",
                  "presentacion", "contenido", "devops", "academico", "otro"}
NORMAS_CITACION = {"apa7", "icontec"}


# --------------------------------------------------------------------------
# Lector YAML mínimo (fallback sin PyYAML)
# --------------------------------------------------------------------------

class ErrorYaml(ValueError):
    pass


_CLAVE = re.compile(r"""^(?P<k>"[^"]*"|'[^']*'|[^\s:#'"\[\]{}-][^:#]*?|-[^\s:#][^:#]*?):(?:\s+(?P<v>.*))?$""")


def _quitar_comentario(texto: str) -> str:
    comilla = None
    for i, c in enumerate(texto):
        if comilla:
            if c == comilla:
                comilla = None
        elif c in "\"'":
            comilla = c
        elif c == "#" and (i == 0 or texto[i - 1] in " \t"):
            return texto[:i].rstrip()
    return texto.rstrip()


def _partir_flujo(texto: str) -> list[str]:
    partes, actual, comilla = [], "", None
    for c in texto:
        if comilla:
            actual += c
            if c == comilla:
                comilla = None
        elif c in "\"'":
            comilla = c
            actual += c
        elif c == ",":
            partes.append(actual.strip())
            actual = ""
        else:
            actual += c
    if actual.strip():
        partes.append(actual.strip())
    return partes


def _escalar(texto: str):
    t = texto.strip()
    if t.startswith("[") and t.endswith("]"):
        return [_escalar(p) for p in _partir_flujo(t[1:-1])]
    if t.startswith("{"):
        raise ErrorYaml("mapas en línea {...} no soportados por el lector mínimo")
    if t.startswith('"') and t.endswith('"') and len(t) >= 2:
        return json.loads(t)
    if t.startswith("'") and t.endswith("'") and len(t) >= 2:
        return t[1:-1].replace("''", "'")
    if t in ("", "~", "null", "Null", "NULL"):
        return None
    if t in ("true", "True", "TRUE"):
        return True
    if t in ("false", "False", "FALSE"):
        return False
    if re.fullmatch(r"[-+]?\d+", t):
        return int(t)
    if re.fullmatch(r"[-+]?\d+\.\d*", t):
        return float(t)
    return t


class _LectorYaml:
    def __init__(self, texto: str):
        self.lineas = texto.replace("\t", "    ").splitlines()
        self.i = 0

    def _siguiente(self):
        while self.i < len(self.lineas):
            linea = self.lineas[self.i]
            s = linea.strip()
            if not s or s.startswith("#") or s == "---":
                self.i += 1
                continue
            return len(linea) - len(linea.lstrip(" ")), s
        return None

    @staticmethod
    def _es_item(s: str) -> bool:
        return s == "-" or s.startswith("- ")

    def leer(self):
        sig = self._siguiente()
        if sig is None:
            return None
        valor = self._bloque(sig[0])
        if self._siguiente() is not None:
            raise ErrorYaml(f"línea {self.i + 1}: indentación inesperada")
        return valor

    def _bloque(self, sangria: int):
        _, s = self._siguiente()
        return self._lista(sangria) if self._es_item(s) else self._mapa(sangria)

    def _mapa(self, sangria: int) -> dict:
        res: dict = {}
        while True:
            sig = self._siguiente()
            if sig is None or sig[0] < sangria:
                break
            ind, s = sig
            if ind > sangria:
                raise ErrorYaml(f"línea {self.i + 1}: indentación inesperada")
            if self._es_item(s):
                break
            m = _CLAVE.match(_quitar_comentario(s))
            if not m:
                raise ErrorYaml(f"línea {self.i + 1}: se esperaba 'clave: valor'")
            clave = _escalar(m.group("k"))
            self.i += 1
            res[clave] = self._valor(m.group("v") or "", sangria)
        return res

    def _valor(self, resto: str, sangria: int):
        resto = _quitar_comentario(resto)
        if resto[:1] in (">", "|") and re.fullmatch(r"[>|][-+]?", resto):
            return self._bloque_literal(resto, sangria)
        if resto == "":
            sig = self._siguiente()
            if sig is None:
                return None
            ind, s = sig
            if ind > sangria or (ind == sangria and self._es_item(s)):
                return self._bloque(ind)
            return None
        return _escalar(resto)

    def _bloque_literal(self, indicador: str, sangria: int) -> str:
        crudas = []
        sangria_bloque = None
        while self.i < len(self.lineas):
            linea = self.lineas[self.i]
            if linea.strip() == "":
                crudas.append("")
                self.i += 1
                continue
            ind = len(linea) - len(linea.lstrip(" "))
            if ind <= sangria:
                break
            if sangria_bloque is None:
                sangria_bloque = ind
            crudas.append(linea[sangria_bloque:])
            self.i += 1
        while crudas and crudas[-1] == "":
            crudas.pop()
        if indicador[0] == "|":
            texto = "\n".join(crudas)
        else:
            texto, previa_vacia = "", True
            for c in crudas:
                if c == "":
                    texto += "\n"
                    previa_vacia = True
                else:
                    texto += ("" if previa_vacia else " ") + c
                    previa_vacia = False
        if indicador.endswith("-"):
            return texto
        return texto + "\n" if texto else texto

    def _lista(self, sangria: int) -> list:
        res = []
        while True:
            sig = self._siguiente()
            if sig is None or sig[0] < sangria:
                break
            ind, s = sig
            if ind > sangria:
                raise ErrorYaml(f"línea {self.i + 1}: indentación inesperada")
            if not self._es_item(s):
                break
            contenido = s[1:].lstrip(" ")
            self.i += 1
            if contenido == "":
                sig2 = self._siguiente()
                res.append(self._bloque(sig2[0]) if sig2 and sig2[0] > sangria else None)
                continue
            m = None if contenido.startswith(("\"", "'")) else _CLAVE.match(_quitar_comentario(contenido))
            if m:
                sangria_hijo = ind + (len(s) - len(contenido))
                elemento = {_escalar(m.group("k")): self._valor(m.group("v") or "", sangria_hijo)}
                elemento.update(self._mapa(sangria_hijo))
                res.append(elemento)
            else:
                res.append(_escalar(_quitar_comentario(contenido)))
        return res


def cargar_yaml(ruta: Path, forzar_fallback: bool = False):
    texto = ruta.read_text(encoding="utf-8")
    if not forzar_fallback:
        try:
            import yaml  # type: ignore
        except ImportError:
            pass
        else:
            return yaml.safe_load(texto)
    return _LectorYaml(texto).leer()


# --------------------------------------------------------------------------
# Preflight
# --------------------------------------------------------------------------

def _vacio(valor) -> bool:
    return valor is None or (isinstance(valor, str) and not valor.strip())


def _como_lista(valor):
    if valor is None:
        return []
    return valor if isinstance(valor, list) else None


def preflight(manifest) -> dict:
    """Devuelve {'errores': [...], 'avisos': [...], 'waves': [[ids]], 'bloqueadas': [ids]}."""
    errores: list[str] = []
    avisos: list[str] = []
    resultado = {"errores": errores, "avisos": avisos, "waves": [], "bloqueadas": []}

    if not isinstance(manifest, dict):
        errores.append("el manifest no es un mapa YAML")
        return resultado
    if _vacio(manifest.get("milestone")):
        errores.append("falta `milestone` (nombre del milestone)")
    cap = manifest.get("cap_concurrencia")
    if cap is not None and (not isinstance(cap, int) or isinstance(cap, bool) or cap < 1):
        errores.append(f"`cap_concurrencia` debe ser un entero >= 1 (vale {cap!r})")
    tareas = manifest.get("tareas")
    if not isinstance(tareas, list) or not tareas:
        errores.append("`tareas` debe ser una lista no vacía")
        return resultado

    ids: list[str] = []
    for n, t in enumerate(tareas, 1):
        if not isinstance(t, dict):
            errores.append(f"tarea #{n}: no es un mapa")
            continue
        etiqueta = t.get("id") or f"#{n}"
        for campo in ("id", "titulo", "tipo", "descripcion"):
            if _vacio(t.get(campo)):
                errores.append(f"tarea {etiqueta}: campo `{campo}` vacío o ausente")
        if not _vacio(t.get("id")):
            ids.append(str(t["id"]))
        tipo = t.get("tipo")
        if isinstance(tipo, str) and tipo:
            if tipo not in TIPOS_VIGENTES:
                avisos.append(f"tarea {etiqueta}: tipo `{tipo}` no está en la lista de orquestador §1")
        if "verificacion_manual" in t:
            vm = t["verificacion_manual"]
            if not isinstance(vm, list) or any(not isinstance(v, str) or not v.strip() for v in vm):
                errores.append(f"tarea {etiqueta}: `verificacion_manual` debe ser una lista de textos no vacíos")
        if "norma_citacion" in t and (not isinstance(t["norma_citacion"], str) or t["norma_citacion"] not in NORMAS_CITACION):
            errores.append(f"tarea {etiqueta}: `norma_citacion` debe ser uno de {sorted(NORMAS_CITACION)} (vale {t['norma_citacion']!r})")
        if "modelo" in t and (not isinstance(t["modelo"], str) or not t["modelo"].strip()):
            errores.append(f"tarea {etiqueta}: `modelo` debe ser un texto no vacío (alias o ID completo)")
        if "verificacion" in t and (not isinstance(t["verificacion"], str) or t["verificacion"] not in NIVELES_VERIFICACION):
            errores.append(f"tarea {etiqueta}: `verificacion` debe ser uno de {sorted(NIVELES_VERIFICACION)} (vale {t['verificacion']!r})")
        crit = t.get("criterios_aceptacion")
        if crit is not None and not isinstance(crit, list):
            errores.append(f"tarea {etiqueta}: `criterios_aceptacion` debe ser una lista")
        elif not crit:
            avisos.append(f"tarea {etiqueta}: sin criterios de aceptación -> el orquestador disparará `especificacion`")

    vistos = set()
    for i in ids:
        if i in vistos:
            errores.append(f"id duplicado: {i}")
        vistos.add(i)

    internas: dict[str, list[str]] = {}
    externas: dict[str, list[str]] = {}
    for t in tareas:
        if not isinstance(t, dict) or _vacio(t.get("id")):
            continue
        tid = str(t["id"])
        deps = _como_lista(t.get("depende_de"))
        decl = _como_lista(t.get("fuera_de_alcance_si_depende_de"))
        if deps is None:
            errores.append(f"tarea {tid}: `depende_de` debe ser una lista")
            deps = []
        if decl is None:
            errores.append(f"tarea {tid}: `fuera_de_alcance_si_depende_de` debe ser una lista")
            decl = []
        decl = [str(d) for d in decl]
        internas[tid], externas[tid] = [], []
        for d in deps:
            d = str(d)
            if d == tid:
                errores.append(f"tarea {tid}: depende de sí misma")
            elif d in vistos:
                internas[tid].append(d)
            elif d in decl:
                externas[tid].append(d)
            else:
                errores.append(
                    f"tarea {tid}: depende_de `{d}` no resuelve a ninguna tarea ni está en "
                    "`fuera_de_alcance_si_depende_de` (dependencia ambigua)"
                )

    ciclo = _buscar_ciclo(internas)
    if ciclo:
        errores.append("ciclo de dependencias: " + " -> ".join(ciclo))
    if errores:
        return resultado

    bloqueadas = {t for t, e in externas.items() if e}
    for t in sorted(bloqueadas):
        avisos.append(f"tarea {t}: BLOQUEADA_EXTERNA por {', '.join(externas[t])} (anotar en bloqueos-externos.md)")
    resultado["waves"], resultado["bloqueadas"] = calcular_waves(internas, bloqueadas)
    return resultado


def _buscar_ciclo(grafo: dict[str, list[str]]):
    estado: dict[str, int] = {}
    pila: list[str] = []

    def visitar(n):
        estado[n] = 1
        pila.append(n)
        for d in grafo.get(n, []):
            if estado.get(d) == 1:
                return pila[pila.index(d):] + [d]
            if d not in estado:
                r = visitar(d)
                if r:
                    return r
        pila.pop()
        estado[n] = 2
        return None

    for n in grafo:
        if n not in estado:
            r = visitar(n)
            if r:
                return r
    return None


def calcular_waves(internas: dict[str, list[str]], bloqueadas: set | None = None):
    """Waves según orquestador §3; las tareas bloqueadas (y lo que depende de ellas) quedan aparte."""
    bloqueadas = set(bloqueadas or ())
    cambio = True
    while cambio:
        cambio = False
        for t, deps in internas.items():
            if t not in bloqueadas and any(d in bloqueadas for d in deps):
                bloqueadas.add(t)
                cambio = True
    pendientes = [t for t in internas if t not in bloqueadas]
    hechas: set[str] = set()
    waves = []
    while pendientes:
        wave = [t for t in pendientes if all(d in hechas for d in internas[t])]
        if not wave:  # no debería pasar: los ciclos ya se rechazaron
            break
        waves.append(wave)
        hechas.update(wave)
        pendientes = [t for t in pendientes if t not in hechas]
    return waves, sorted(bloqueadas)


def configurar_salida() -> None:
    """Fuerza UTF-8 en la consola (en Windows la salida por defecto rompe los acentos)."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def main(argv: list[str]) -> int:
    configurar_salida()
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    ruta = Path(args[0])
    try:
        manifest = cargar_yaml(ruta, forzar_fallback="--sin-pyyaml" in argv)
    except (OSError, ValueError) as e:
        print(f"ERROR: no se pudo leer {ruta}: {e}")
        return 2
    r = preflight(manifest)
    print(f"Preflight de {ruta.as_posix()}")
    for e in r["errores"]:
        print(f"  ERROR: {e}")
    for a in r["avisos"]:
        print(f"  aviso: {a}")
    if r["errores"]:
        print(f"RESULTADO: FALLA ({len(r['errores'])} error/es)")
        return 1
    for n, w in enumerate(r["waves"], 1):
        print(f"  wave {n}: {', '.join(w)}")
    if r["bloqueadas"]:
        print(f"  fuera de waves (bloqueo externo): {', '.join(r['bloqueadas'])}")
    print(f"RESULTADO: PASA ({len(manifest['tareas'])} tareas, {len(r['waves'])} waves)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
