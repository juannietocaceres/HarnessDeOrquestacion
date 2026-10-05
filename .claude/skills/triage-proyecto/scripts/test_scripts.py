#!/usr/bin/env python3
"""Pruebas de los scripts de triage-proyecto (solo biblioteca estándar).

Uso (desde la raíz del repo):
    python -m unittest discover -s .claude/skills/triage-proyecto/scripts -p "test_*.py" -v
"""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

DIR = Path(__file__).resolve().parent
RAIZ = DIR.parents[3]  # .claude/skills/triage-proyecto/scripts -> raíz del repo
sys.path.insert(0, str(DIR))

import comparar_manifests as cm  # noqa: E402
import preflight_manifest as pm  # noqa: E402
import validar_triage as vt  # noqa: E402


def tarea(tid, deps=(), **extra):
    t = {"id": tid, "titulo": f"Tarea {tid}", "tipo": "backend", "depende_de": list(deps),
         "descripcion": "algo", "criterios_aceptacion": ["se cumple"]}
    t.update(extra)
    return t


def manifest(*tareas):
    return {"milestone": "Prueba", "tareas": list(tareas)}


class PruebasPreflight(unittest.TestCase):
    def test_manifest_valido_calcula_waves(self):
        r = pm.preflight(manifest(tarea("T1"), tarea("T2", ["T1"]), tarea("T3", ["T1"]), tarea("T4", ["T2", "T3"])))
        self.assertEqual(r["errores"], [])
        self.assertEqual(r["waves"], [["T1"], ["T2", "T3"], ["T4"]])

    def test_ciclo_falla(self):
        r = pm.preflight(manifest(tarea("T1", ["T3"]), tarea("T2", ["T1"]), tarea("T3", ["T2"])))
        self.assertTrue(any("ciclo" in e for e in r["errores"]), r["errores"])

    def test_dependencia_sin_resolver_falla(self):
        r = pm.preflight(manifest(tarea("T1"), tarea("T2", ["T9"])))
        self.assertTrue(any("T9" in e and "no resuelve" in e for e in r["errores"]), r["errores"])

    def test_dependencia_externa_declarada_pasa_y_bloquea(self):
        r = pm.preflight(manifest(tarea("T1", ["API-X"], fuera_de_alcance_si_depende_de=["API-X"]),
                                  tarea("T2", ["T1"]), tarea("T3")))
        self.assertEqual(r["errores"], [])
        self.assertEqual(r["waves"], [["T3"]])
        self.assertEqual(r["bloqueadas"], ["T1", "T2"])

    def test_id_duplicado_y_campo_vacio_fallan(self):
        r = pm.preflight(manifest(tarea("T1"), tarea("T1"), tarea("T2", descripcion="  ")))
        self.assertTrue(any("duplicado" in e for e in r["errores"]))
        self.assertTrue(any("descripcion" in e for e in r["errores"]))

    def test_criterios_vacios_es_aviso_no_error(self):
        r = pm.preflight(manifest(tarea("T1", criterios_aceptacion=[])))
        self.assertEqual(r["errores"], [])
        self.assertTrue(any("especificacion" in a for a in r["avisos"]))

    def test_tipos_presentacion_y_contenido_son_vigentes(self):
        for tipo in ("presentacion", "contenido"):
            with self.subTest(tipo=tipo):
                r = pm.preflight(manifest(tarea("T1", tipo=tipo)))
                self.assertEqual(r["errores"], [])
                self.assertFalse(any("tipo" in a for a in r["avisos"]), r["avisos"])

    def test_tipo_desconocido_es_aviso(self):
        r = pm.preflight(manifest(tarea("T1", tipo="inventado")))
        self.assertEqual(r["errores"], [])
        self.assertTrue(any("inventado" in a for a in r["avisos"]))

    def test_verificacion_manual_y_modelo_validos(self):
        r = pm.preflight(manifest(tarea("T1", verificacion_manual=["Abrir en un teléfono real"], modelo="sonnet"),
                                  tarea("T2", ["T1"], modelo="claude-opus-5-5", verificacion_manual=[])))
        self.assertEqual(r["errores"], [])

    def test_verificacion_manual_invalida_falla(self):
        for valor in ("probar en el móvil", ["ok", ""], ["ok", 3], None):
            with self.subTest(valor=valor):
                r = pm.preflight(manifest(tarea("T1", verificacion_manual=valor)))
                self.assertTrue(any("verificacion_manual" in e for e in r["errores"]), r["errores"])

    def test_modelo_invalido_falla(self):
        for valor in ("", "  ", 5, None, ["sonnet"]):
            with self.subTest(valor=valor):
                r = pm.preflight(manifest(tarea("T1", modelo=valor)))
                self.assertTrue(any("modelo" in e for e in r["errores"]), r["errores"])

    def test_verificacion_valida(self):
        r = pm.preflight(manifest(tarea("T1", verificacion="ligera"), tarea("T2", verificacion="completa"),
                                  tarea("T3", verificacion="ninguna")))
        self.assertEqual(r["errores"], [])

    def test_verificacion_invalida_falla(self):
        for valor in ("", "total", False, None, ["ligera"]):
            with self.subTest(valor=valor):
                r = pm.preflight(manifest(tarea("T1", verificacion=valor)))
                self.assertTrue(any("verificacion" in e for e in r["errores"]), r["errores"])

    def test_lector_minimo_igual_a_pyyaml_en_manifests_reales(self):
        try:
            import yaml  # type: ignore
        except ImportError:
            self.skipTest("PyYAML no instalado")
        rutas = sorted(RAIZ.glob("milestones/*/milestone.yaml"))
        self.assertTrue(rutas)
        for ruta in rutas:
            with self.subTest(ruta=ruta.name):
                self.assertEqual(pm.cargar_yaml(ruta, forzar_fallback=True),
                                 yaml.safe_load(ruta.read_text(encoding="utf-8")))

    def test_lector_minimo_subconjunto(self):
        texto = (
            "milestone: \"Demo: con dos puntos\"  # comentario\n"
            "cap_concurrencia: 2\n"
            "tareas:\n"
            "- id: T1\n"
            "  depende_de: []   # vacío\n"
            "  descripcion: >\n"
            "    linea uno\n"
            "    linea dos\n"
            "  criterios_aceptacion:\n"
            "    - \"a: b\"\n"
            "    - 'c ''d'''\n"
            "- id: T2\n"
            "  depende_de: [T1, \"T3\"]\n"
        )
        m = pm._LectorYaml(texto).leer()
        self.assertEqual(m["milestone"], "Demo: con dos puntos")
        self.assertEqual(m["cap_concurrencia"], 2)
        self.assertEqual(m["tareas"][0]["descripcion"], "linea uno linea dos\n")
        self.assertEqual(m["tareas"][0]["criterios_aceptacion"], ["a: b", "c 'd'"])
        self.assertEqual(m["tareas"][1]["depende_de"], ["T1", "T3"])


TRIAGE_BASE = {
    "proyecto": "Demo",
    "slug": "demo",
    "estado": "requiere_aclaracion",
    "preguntas_pendientes": [{"pregunta": "¿Plataforma?", "opciones": ["Web", "Móvil"]}],
    "clasificacion": {"dominio": "web", "complejidad": "baja", "alcance": "provisional"},
    "requisitos_tecnicos": {"frontend": "", "backend": "", "datos": "", "otros": ""},
    "requisitos_no_funcionales": [{"requisito": "Accesible", "inferido": True}],
    "tipos_requeridos": [],
    "skills_requeridas": ["especificacion"],
    "fuera_de_alcance": [],
    "riesgos": [],
    "manifest": None,
}


class PruebasValidarTriage(unittest.TestCase):
    def setUp(self):
        self.esquema = json.loads(vt.RUTA_ESQUEMA.read_text(encoding="utf-8"))

    def errores(self, datos, raiz=RAIZ):
        return vt.validar_triage(datos, raiz, forzar_minimo=True)["errores"]

    def test_triage_aclaracion_valido(self):
        self.assertEqual(self.errores(copy.deepcopy(TRIAGE_BASE)), [])

    def test_enum_fuera_de_esquema(self):
        d = copy.deepcopy(TRIAGE_BASE)
        d["clasificacion"]["dominio"] = "videojuego"
        self.assertTrue(any("dominio" in e for e in self.errores(d)))

    def test_mas_de_tres_preguntas(self):
        d = copy.deepcopy(TRIAGE_BASE)
        d["preguntas_pendientes"] = [TRIAGE_BASE["preguntas_pendientes"][0]] * 4
        self.assertTrue(any("máximo 3" in e for e in self.errores(d)))

    def test_aclaracion_sin_preguntas_falla(self):
        d = copy.deepcopy(TRIAGE_BASE)
        d["preguntas_pendientes"] = []
        self.assertTrue(self.errores(d))

    def test_listo_con_preguntas_o_sin_manifest_falla(self):
        d = copy.deepcopy(TRIAGE_BASE)
        d["estado"] = "listo_para_orquestar"
        errs = self.errores(d)
        self.assertTrue(any("preguntas_pendientes" in e for e in errs), errs)
        self.assertTrue(any("manifest" in e for e in errs), errs)

    def test_alta_sin_particion_falla(self):
        d = copy.deepcopy(TRIAGE_BASE)
        d["clasificacion"]["complejidad"] = "alta"
        self.assertTrue(any("particion_propuesta" in e for e in self.errores(d)))

    def test_propiedad_extra_y_slug_invalido_fallan(self):
        d = copy.deepcopy(TRIAGE_BASE)
        d["slug"] = "Mi Slug"
        d["agentes"] = ["Frontend_Agent"]
        errs = self.errores(d)
        self.assertTrue(any("slug" in e for e in errs))
        self.assertTrue(any("agentes" in e for e in errs))

    def test_skill_inexistente_falla(self):
        d = copy.deepcopy(TRIAGE_BASE)
        d["skills_requeridas"] = ["skill-que-no-existe"]
        self.assertTrue(any("no existe" in e for e in self.errores(d)))

    def test_listo_con_manifest_valido_y_tipos_coherentes(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            (raiz / ".claude" / "skills" / "especificacion").mkdir(parents=True)
            (raiz / ".claude" / "skills" / "especificacion" / "SKILL.md").write_text("x", encoding="utf-8")
            (raiz / "m").mkdir()
            (raiz / "m" / "milestone.yaml").write_text(
                "milestone: X\ntareas:\n  - id: T1\n    titulo: t\n    tipo: backend\n"
                "    depende_de: []\n    descripcion: d\n    criterios_aceptacion: [\"c\"]\n",
                encoding="utf-8")
            d = copy.deepcopy(TRIAGE_BASE)
            d.update(estado="listo_para_orquestar", preguntas_pendientes=[], manifest="m/milestone.yaml",
                     tipos_requeridos=["backend"])
            self.assertEqual(self.errores(d, raiz), [])
            d["tipos_requeridos"] = ["frontend"]
            self.assertTrue(any("falta 'backend'" in e for e in self.errores(d, raiz)))

    def test_listo_con_manifest_con_ciclo_falla(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            (raiz / ".claude" / "skills" / "especificacion").mkdir(parents=True)
            (raiz / ".claude" / "skills" / "especificacion" / "SKILL.md").write_text("x", encoding="utf-8")
            d = copy.deepcopy(TRIAGE_BASE)
            d.update(estado="listo_para_orquestar", preguntas_pendientes=[], manifest="milestone.yaml")
            (raiz / "milestone.yaml").write_text(
                "milestone: X\ntareas:\n"
                "  - id: T1\n    titulo: t\n    tipo: backend\n    depende_de: [T2]\n    descripcion: d\n"
                "  - id: T2\n    titulo: t\n    tipo: backend\n    depende_de: [T1]\n    descripcion: d\n",
                encoding="utf-8")
            self.assertTrue(any("ciclo" in e for e in self.errores(d, raiz)))


class PruebasComparar(unittest.TestCase):
    def test_equivalentes_y_distintos(self):
        a = manifest(tarea("T1"), tarea("T2", ["T1"]))
        self.assertEqual(cm.comparar(a, copy.deepcopy(a)), [])
        b = manifest(tarea("T1"), tarea("T2"))
        self.assertTrue(cm.comparar(a, b))


if __name__ == "__main__":
    unittest.main()
