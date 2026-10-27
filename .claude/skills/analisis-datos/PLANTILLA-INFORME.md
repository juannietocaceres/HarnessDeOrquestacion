# Plantilla de informe

Se usa en la fase 6 de `SKILL.md`. Los textos entre `< >` se reemplazan;
los títulos de sección **se reescriben como afirmaciones**: los de abajo
son solo de ejemplo. Extensión objetivo: lo que se lee en 5 minutos
(≈ 2–4 páginas sin anexos).

---

```markdown
# <La idea central en una frase de máximo 15 palabras>

<Audiencia> · <fecha> · Datos: <fuente>, <periodo>, <n filas tras limpieza>

## En resumen

<3–4 líneas: la respuesta a la pregunta del encargo, la cifra principal con
su intervalo y la recomendación. Quien solo lea esto debe poder decidir.>

**Recomendación:** <qué hacer, quién, y cómo se sabrá si funcionó>.

## <Hallazgo 1 escrito como afirmación: "El Norte concentra la caída">

<2–4 líneas de contexto: qué se comparó y qué se ve.>

![<descripción del gráfico para quien no lo ve>](graficos/<archivo>.png)

<1–2 líneas: por qué importa para la decisión. Confianza: alta | media | baja.>

## <Hallazgo 2 como afirmación>

...

## <Hallazgo 3 como afirmación>

...

## Qué significa y qué hacer

| Conclusión | Evidencia | Confianza | Limitación |
|---|---|---|---|
| <...> | <cifra o gráfico> | <alta/media/baja + por qué> | <...> |

<Recomendaciones accionables, en orden de impacto.>

## Lo que estos datos no permiten afirmar

- <p. ej.: "No se puede atribuir la caída al cierre de distribuidores:
  coincide en el tiempo, pero no hay grupo de comparación.">

## Método (resumen)

- **Datos**: <origen, periodo, qué es una fila>.
- **Limpieza**: <n> pasos, <filas crudas> → <filas limpias>; detalle en
  `bitacora-limpieza.md`.
- **Análisis**: <métodos, cómo se calcularon los intervalos>.
- **Reproducir**: `python src/01_limpieza.py && python src/02_analisis.py && python src/03_graficos.py`.

## Anexos

<Tablas completas, hallazgos secundarios, gráficos de robustez.>
```

---

## Notas de redacción

- **Números**: separador de miles con punto y decimales con coma en
  documentos en español (`10.138`, `18,4 %`), o la convención del
  destino; una sola en todo el informe. `verificar_cifras.py` acepta ambas.
- **Redondeo**: el que el lector necesita (`18 %`, no `18,4372 %`); el
  valor exacto vive en `cifras.json`.
- **Un párrafo, una idea.** Frases cortas. Verbos en activo ("el Norte
  cayó"), no "se evidencia una disminución".
- **Sin jerga** si la audiencia no es técnica: "intervalo de confianza del
  95 %" se puede decir "entre 16 % y 21 %, con alta probabilidad".
- **Formato de entrega**: el Markdown es la fuente. Para Word, `pandoc
  informe.md -o informe.docx` (ver `trabajo-academico` §6 si lleva norma
  APA); para exponer, `presentaciones-visuales`.
