"""Pruebas de medir_tokens.py y verificar_entidades.py (solo biblioteca estándar).

Uso:
    python -m unittest discover -s .claude/skills/optimizador-tokens/scripts -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MEDIR = AQUI / "medir_tokens.py"
VERIFICAR = AQUI / "verificar_entidades.py"

ORIGINAL = """Tarea T2 depende de T1. Edita `api/contrato-tareas.md` y lee schema/tareas.md.
Ver https://code.claude.com/docs/en/skills y el commit b6c7e47.
Servidor en localhost:5173, Python 3.11, id 550e8400-e29b-41d4-a716-446655440000.
El estado inicial es `pendiente`; responde `201 Created` en POST /tareas.
Prosa de relleno: filtro/orden y HTML/CSS/JS no son rutas.
"""

CAPSULA_OK = """T2<-T1|editar:`api/contrato-tareas.md`|leer:schema/tareas.md
ref:https://code.claude.com/docs/en/skills|commit:b6c7e47
srv:localhost:5173|Python 3.11|id:550e8400-e29b-41d4-a716-446655440000
estado_ini:`pendiente`|POST /tareas->`201 Created`
"""


def correr(script, *args, env=None):
    p = subprocess.run([sys.executable, str(script), *map(str, args)],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout, p.stderr


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def archivo(self, nombre, texto):
        p = self.dir / nombre
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(texto, encoding="utf-8")
        return p


class TestVerificarEntidades(Base):
    def test_capsula_completa_pasa(self):
        o, c = self.archivo("o.md", ORIGINAL), self.archivo("c.md", CAPSULA_OK)
        code, out, _ = correr(VERIFICAR, o, c)
        d = json.loads(out)
        self.assertEqual(code, 0, d["faltantes"])
        self.assertTrue(d["entidades_preservadas"])
        for cat in ("url", "ruta", "id_tarea", "version", "puerto", "uuid", "hash", "literal"):
            self.assertIn(cat, d["por_categoria"], cat)

    def test_falla_si_falta_una_entidad(self):
        o = self.archivo("o.md", ORIGINAL)
        c = self.archivo("c.md", CAPSULA_OK.replace("localhost:5173", "localhost"))
        code, out, _ = correr(VERIFICAR, o, c)
        d = json.loads(out)
        self.assertEqual(code, 1)
        self.assertFalse(d["entidades_preservadas"])
        self.assertIn("puerto", d["faltantes"])

    def test_falla_si_cambia_un_literal(self):
        o = self.archivo("o.md", ORIGINAL)
        c = self.archivo("c.md", CAPSULA_OK.replace("`pendiente`", "`Pendiente`"))
        code, out, _ = correr(VERIFICAR, o, c)
        self.assertEqual(code, 1)
        self.assertIn("pendiente", json.loads(out)["faltantes"]["literal"])

    def test_falla_si_falta_un_id_de_tarea(self):
        o = self.archivo("o.md", ORIGINAL)
        c = self.archivo("c.md", CAPSULA_OK.replace("T2<-T1", "T2<-"))
        code, out, _ = correr(VERIFICAR, o, c)
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)["faltantes"]["id_tarea"], ["T1"])

    def test_prosa_con_barra_no_es_ruta(self):
        o = self.archivo("o.md", ORIGINAL)
        code, out, _ = correr(VERIFICAR, o, self.archivo("c.md", CAPSULA_OK))
        self.assertEqual(code, 0)
        texto = json.dumps(json.loads(out), ensure_ascii=False)
        self.assertNotIn("filtro/orden", texto)

    def test_rutas_relativas_se_normalizan(self):
        o = self.archivo("o.md", "Ver [x](../../../schema/tareas.md).")
        c = self.archivo("c.md", "x: schema/tareas.md")
        self.assertEqual(correr(VERIFICAR, o, c)[0], 0)

    def test_ignorar_hace_explicita_la_omision(self):
        o = self.archivo("o.md", ORIGINAL)
        c = self.archivo("c.md", CAPSULA_OK.replace("Python 3.11", "Python"))
        code, out, _ = correr(VERIFICAR, o, c, "--ignorar", "3.11")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["ignoradas"], ["3.11"])

    def test_credencial_en_capsula_sale_con_3(self):
        o = self.archivo("o.md", ORIGINAL)
        c = self.archivo("c.md", CAPSULA_OK + "\nkey: sk-ant-api03-abcdefghijklmnop\n")
        code, out, _ = correr(VERIFICAR, o, c)
        self.assertEqual(code, 3)
        self.assertTrue(json.loads(out)["credencial_en_capsula"])

    def test_credencial_del_original_no_se_exige(self):
        o = self.archivo("o.md", "T1 usa api_key=sk-ant-api03-abcdefghijklmnop")
        c = self.archivo("c.md", "T1 (credencial omitida)")
        self.assertEqual(correr(VERIFICAR, o, c)[0], 0)

    def test_archivo_inexistente_sale_con_2(self):
        o = self.archivo("o.md", ORIGINAL)
        self.assertEqual(correr(VERIFICAR, o, self.dir / "no.md")[0], 2)

    def test_regex_extra_invalida_sale_con_2(self):
        o, c = self.archivo("o.md", ORIGINAL), self.archivo("c.md", CAPSULA_OK)
        self.assertEqual(correr(VERIFICAR, o, c, "--extra", "(")[0], 2)

    def test_extra_agrega_categoria(self):
        o = self.archivo("o.md", "codigo 404 y 201")
        c = self.archivo("c.md", "codigo 201")
        code, out, _ = correr(VERIFICAR, o, c, "--extra", r"\b[1-5]\d\d\b")
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)["faltantes"]["extra_1"], ["404"])


class TestMedirTokens(Base):
    def env_sin_clave(self):
        env = dict(os.environ)
        env.pop("ANTHROPIC_API_KEY", None)
        return env

    def test_estimacion_es_caracteres_entre_4(self):
        a = self.archivo("a.md", "x" * 403)
        code, out, _ = correr(MEDIR, a, env=self.env_sin_clave())
        d = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(d["archivos"][0]["caracteres"], 403)
        self.assertEqual(d["archivos"][0]["tokens"], 100)
        self.assertEqual(d["metodo"], "estimado")

    def test_comparar_calcula_ahorro(self):
        o, f = self.archivo("o.md", "a" * 4000), self.archivo("f.md", "b" * 1000)
        code, out, _ = correr(MEDIR, "--comparar", o, f, env=self.env_sin_clave())
        m = json.loads(out)["metricas"]
        self.assertEqual((m["tokens_original"], m["tokens_final"], m["ahorro"]), (1000, 250, "75%"))

    def test_api_sin_clave_cae_a_estimado_y_avisa(self):
        a = self.archivo("a.md", "hola")
        code, out, _ = correr(MEDIR, "--api", a, env=self.env_sin_clave())
        d = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(d["metodo"], "estimado")
        self.assertIn("ANTHROPIC_API_KEY", d["aviso"])

    def test_descriptions_cuenta_solo_las_visibles(self):
        self.archivo("skills/a/SKILL.md", "---\nname: a\ndescription: Hace algo util.\n---\ncuerpo largo " * 1)
        self.archivo("skills/b/SKILL.md", "---\nname: b\ndescription: >\n  Linea uno\n  linea dos.\ndisable-model-invocation: true\n---\n")
        self.archivo("skills/c/SKILL.md", "---\nname: c\ndescription: \"Con comillas\"\n---\n")
        self.archivo("skills/c/LICENSE.txt", "MIT (c) Emil Kowalski")
        code, out, _ = correr(MEDIR, "--descriptions", self.dir / "skills", env=self.env_sin_clave())
        d = json.loads(out)
        self.assertEqual(code, 0)
        por = {s["skill"]: s for s in d["skills"]}
        self.assertEqual(por["a"]["caracteres"], len("a: Hace algo util."))
        self.assertEqual(por["b"]["caracteres"], len("b: Linea uno linea dos."))
        self.assertFalse(por["b"]["en_contexto"])
        self.assertEqual(por["c"]["origen"], "emil")
        self.assertEqual(por["c"]["caracteres"], len("c: Con comillas"))
        self.assertEqual(d["resumen"]["total"]["en_contexto"], 2)
        self.assertEqual(d["resumen"]["total"]["tokens_en_contexto"], por["a"]["tokens"] + por["c"]["tokens"])

    def test_descriptions_excluir(self):
        self.archivo("skills/a/SKILL.md", "---\nname: a\ndescription: x\n---\n")
        self.archivo("skills/b/SKILL.md", "---\nname: b\ndescription: y\n---\n")
        _, out, _ = correr(MEDIR, "--descriptions", self.dir / "skills", "--excluir", "b", env=self.env_sin_clave())
        self.assertEqual([s["skill"] for s in json.loads(out)["skills"]], ["a"])

    def test_frontmatter_ausente_sale_con_2(self):
        self.archivo("skills/a/SKILL.md", "sin frontmatter")
        self.assertEqual(correr(MEDIR, "--descriptions", self.dir / "skills")[0], 2)

    def test_dos_modos_a_la_vez_sale_con_2(self):
        a = self.archivo("a.md", "x")
        self.assertEqual(correr(MEDIR, a, "--comparar", a, a)[0], 2)

    def test_archivo_inexistente_sale_con_2(self):
        self.assertEqual(correr(MEDIR, self.dir / "no.md")[0], 2)

    def test_la_clave_nunca_aparece_en_la_salida(self):
        # Clave falsa contra un puerto local cerrado: la llamada falla sin salir
        # de la máquina y el script cae a estimado sin imprimir la clave.
        env = self.env_sin_clave()
        env["ANTHROPIC_API_KEY"] = "sk-ant-falsa-para-prueba-000000"
        env["OPTIMIZADOR_TOKENS_URL_PRUEBA"] = "http://127.0.0.1:9/v1/messages/count_tokens"
        a = self.archivo("a.md", "hola mundo")
        code, out, err = correr(MEDIR, "--api", a, env=env)
        self.assertEqual(code, 0)
        self.assertNotIn("sk-ant-falsa", out + err)
        self.assertEqual(json.loads(out)["metodo"], "estimado")


if __name__ == "__main__":
    unittest.main()
