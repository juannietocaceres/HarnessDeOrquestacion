"""Pruebas de perfilar.py, verificar_cifras.py y estilo_graficos.py.

verificar_cifras.py solo usa la biblioteca estándar; perfilar.py necesita
pandas y estilo_graficos.py matplotlib (sus pruebas se saltan si faltan).

Uso:
    python -m unittest discover -s .claude/skills/analisis-datos/scripts -v
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PERFILAR = AQUI / "perfilar.py"
VERIFICAR = AQUI / "verificar_cifras.py"
HAY_PANDAS = importlib.util.find_spec("pandas") is not None
HAY_MPL = importlib.util.find_spec("matplotlib") is not None

CSV_SUCIO = """id,ciudad,fecha,precio,email,constante,edad
1,Bogotá,03/02/2026,"$ 1.200",ana@x.com,a,34
2,bogota ,04/02/2026,"$ 950",luis@x.com,a,29
3,Medellín,05/02/2026,NA,eva@x.com,a,-3
4,Medellin,06/02/2026,"$ 1.100",tom@x.com,a,41
5,Cali,07/02/2026,"$ 98.000",ivo@x.com,a,38
2,bogota ,04/02/2026,"$ 950",luis@x.com,a,29
6,Cali,08/02/2026,"$ 1.050",sol@x.com,a,
"""

INFORME = """# Las ventas cayeron 18 % en el T3

En 2026 se analizaron 10.138 pedidos (3 hallazgos). El Norte explica el 70 %
de la caída (IC 95 %: 16,0 a 21,0 puntos; p < 0,05). El ticket medio fue 3,2 millones.

![gráfico](graficos/caida-q3-2025.png) `codigo 12345`

1. Primer punto sin cifras.
- Un dato inventado: 42 % de los clientes.
"""

CIFRAS = {
    "cifras": {
        "caida_pct": {"valor": -18.4, "ic95": [-21.0, -16.0]},
        "pedidos": 10138,
        "aporte_norte": 0.7012,
        "ticket_medio": {"valor": 3_215_000, "unidad": "COP"},
    }
}


def correr(script, *args):
    p = subprocess.run([sys.executable, str(script), *map(str, args)],
                       capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout, p.stderr


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def escribir(self, nombre, texto):
        ruta = self.dir / nombre
        ruta.write_text(texto, encoding="utf-8")
        return ruta


class TestVerificarCifras(Base):
    def test_detecta_inventada_y_acepta_formas(self):
        inf = self.escribir("informe.md", INFORME)
        cif = self.escribir("cifras.json", json.dumps(CIFRAS))
        codigo, out, _ = correr(VERIFICAR, inf, cif)
        r = json.loads(out)
        self.assertEqual(codigo, 1)
        self.assertEqual([f["numero"] for f in r["faltan"]], ["42 %"])
        # 18 % (abs de -18.4), 10.138, 70 % (x100), 16,0 y 21,0 (IC), 3,2 millones
        self.assertEqual(r["respaldados"], 6)

    def test_ignorar_y_ok(self):
        inf = self.escribir("informe.md", INFORME.replace("42 %", "70 %"))
        cif = self.escribir("cifras.json", json.dumps(CIFRAS))
        codigo, out, _ = correr(VERIFICAR, inf, cif)
        self.assertEqual(codigo, 0, out)

    def test_formato_plano_e_ignorar(self):
        inf = self.escribir("i.md", "Margen 2,54 cm y tasa 12.5 %.\n")
        cif = self.escribir("c.json", json.dumps({"tasa": 0.125, "ignorar": ["2,54"]}))
        codigo, out, _ = correr(VERIFICAR, inf, cif)
        self.assertEqual(codigo, 0, out)

    def test_estricto_exige_enteros_chicos(self):
        inf = self.escribir("i.md", "Hay 3 hallazgos.\n")
        cif = self.escribir("c.json", json.dumps({"x": 1}))
        self.assertEqual(correr(VERIFICAR, inf, cif)[0], 0)
        self.assertEqual(correr(VERIFICAR, inf, cif, "--estricto")[0], 1)

    def test_error_de_uso(self):
        self.assertEqual(correr(VERIFICAR, self.dir / "no.md", self.dir / "no.json")[0], 2)


@unittest.skipUnless(HAY_PANDAS, "requiere pandas")
class TestPerfilar(Base):
    def setUp(self):
        super().setUp()
        self.csv = self.escribir("ventas.csv", CSV_SUCIO)
        codigo, out, err = correr(PERFILAR, self.csv, "--salida", self.dir / "perfil")
        self.assertEqual(codigo, 0, err)
        self.p = json.loads((self.dir / "perfil.json").read_text(encoding="utf-8"))
        self.col = {c["columna"]: c for c in self.p["detalle"]}

    def test_dataset(self):
        self.assertEqual(self.p["filas"], 7)
        self.assertEqual(self.p["duplicados_exactos"], 1)
        self.assertEqual(self.p["llaves_candidatas"], [])  # id está repetido
        self.assertTrue((self.dir / "perfil.md").is_file())

    def test_numero_como_texto(self):
        precio = self.col["precio"]
        self.assertEqual(precio["tipo_sugerido"], "numero")
        self.assertEqual(precio["nulos"], 1)
        self.assertEqual(precio["estadisticos"]["max"], 98000)
        self.assertTrue(any("texto" in a for a in precio["alertas"]))
        self.assertGreaterEqual(precio["outliers_iqr"], 1)

    def test_fecha_y_variantes(self):
        self.assertEqual(self.col["fecha"]["tipo_sugerido"], "fecha")
        self.assertEqual(self.col["ciudad"]["tipo_sugerido"], "categoria")
        self.assertEqual(len(self.col["ciudad"]["variantes"]), 2)  # Bogotá, Medellín

    def test_pii_oculto_y_otras_alertas(self):
        self.assertIn("email", self.p["columnas_pii"])
        self.assertIsInstance(self.col["email"]["frecuentes"], str)
        self.assertNotIn("ana@x.com", (self.dir / "perfil.md").read_text(encoding="utf-8"))
        self.assertTrue(any("constante" in a for a in self.col["constante"]["alertas"]))
        self.assertTrue(any("negativos" in a for a in self.col["edad"]["alertas"]))


@unittest.skipUnless(HAY_MPL and HAY_PANDAS, "requiere matplotlib y pandas")
class TestEstilo(Base):
    def test_guarda_png_y_svg(self):
        sys.path.insert(0, str(AQUI))
        import pandas as pd
        from estilo_graficos import aplicar_estilo, barras_destacadas, guardar, linea_destacada, titular
        aplicar_estilo()
        fig, _ = barras_destacadas(["Norte", "Sur", "Centro"], [-12, -4, -2], destacar=["Norte"])
        titular(fig, "El Norte explica la caída", "Variación, millones")
        rutas = guardar(fig, self.dir / "g" / "barras", fuente="Fuente: prueba")
        fig2, _ = linea_destacada(pd.DataFrame({"A": [1, 2, 3], "B": [3, 2, 1]}), destacar=["B"])
        rutas += guardar(fig2, self.dir / "g" / "lineas")
        for r in rutas:
            self.assertGreater(Path(r).stat().st_size, 1000, r)


if __name__ == "__main__":
    unittest.main()
