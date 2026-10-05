---
title: "Modelo predictivo de inteligencia artificial para identificar zonas de riesgo de propagación del dengue por comuna en Santiago de Cali, con datos epidemiológicos y climáticos"
author: "[POR COMPLETAR: estudiante]"
date: "[POR COMPLETAR]"
lang: es
bibliography: referencias.bib

---

> BORRADOR de prueba de la skill `trabajo-academico`. Estructura según
> `ESTRUCTURAS.md` (anteproyecto), norma APA 7 (por defecto, decisión §7.3).
> No hay `docs/academico/lineamientos.md`: el formato institucional es un
> supuesto. Todo el contenido es borrador para revisión humana.

# Planteamiento del problema

El dengue es una infección viral transmitida por mosquitos; la OMS estima que cerca de la mitad de la población mundial está en riesgo y que ocurren entre 100 y 400 millones de infecciones al año [@oms2024dengue]. Un estudio de modelado estimó 390 millones de infecciones anuales [@bhatt2013]. [CITA PENDIENTE: cifras de casos de dengue en Cali por año; salen de SIVIGILA, @ins-sivigila, no se transcriben de memoria.]

En Cali, trabajos previos han relacionado el dengue con determinantes socioeconómicos y ambientales [@delmelle2016] y, con datos de 2018–2019, han explorado su relación con la temperatura superficial y las condiciones de insalubridad urbana [@bahos2025]. [POR COMPLETAR: vacío que atiende este trabajo; hipótesis a confirmar con revisión sistemática: falta un modelo predictivo que integre datos epidemiológicos y climáticos por comuna.]

# Pregunta de investigación

¿Con qué desempeño puede un modelo predictivo de aprendizaje automático, entrenado con datos epidemiológicos y climáticos, anticipar el nivel de riesgo de propagación del dengue en cada comuna de Santiago de Cali? [POR COMPLETAR: horizonte temporal y periodo de datos.]

# Justificación

[POR COMPLETAR: relevancia para la salud pública local (a quién sirve el resultado) y viabilidad (datos, tiempo, cómputo gratuito).] [CITA PENDIENTE: disponibilidad y licencia de los datos epidemiológicos por comuna y de los datos climáticos; confirmar con la fuente (verificacion_manual).]

# Objetivos

**Objetivo general.** Construir un modelo predictivo de riesgo de propagación del dengue por comuna en Santiago de Cali a partir de datos epidemiológicos y climáticos.

**Objetivos específicos.**

1. Compilar los datos epidemiológicos de dengue y los datos climáticos por comuna para el periodo de estudio.
2. Caracterizar la distribución espacial y temporal de los casos de dengue por comuna.
3. Comparar el desempeño de modelos predictivos candidatos (por ejemplo, bosques aleatorios [@breiman2001]).
4. Evaluar el modelo seleccionado con validación temporal sobre datos no vistos en el entrenamiento.
5. Clasificar las comunas por nivel de riesgo a partir de las predicciones del modelo.

| Objetivo | Actividad (metodología) | Entregable |
|---|---|---|
| 1 | Fase 1: adquisición y depuración de datos | Conjunto de datos integrado y diccionario de variables |
| 2 | Fase 2: análisis exploratorio | Mapas y series temporales por comuna |
| 3 | Fase 3: entrenamiento y comparación de modelos | Tabla comparativa de métricas |
| 4 | Fase 4: validación temporal | Informe de desempeño del modelo |
| 5 | Fase 5: zonificación del riesgo | Mapa de riesgo por comuna |

# Marco teórico y estado del arte

[POR COMPLETAR: conceptos (vigilancia epidemiológica, vectores *Aedes*, clima y transmisión, aprendizaje automático supervisado, validación temporal) y trabajos previos de predicción de dengue. Cada trabajo debe pasar la verificación de `SKILL.md` §5 antes de citarse.]

# Metodología

- **Tipo de estudio**: [POR COMPLETAR: cuantitativo, predictivo, con datos secundarios].
- **Datos**: casos de dengue notificados por comuna (SIVIGILA, @ins-sivigila) y variables climáticas (precipitación, temperatura, humedad) de [POR COMPLETAR: fuente climática, con URL y licencia verificadas]. Unidad de análisis: [POR COMPLETAR: comuna-semana epidemiológica].
- **Procedimiento**: fases 1 a 5 de la tabla de objetivos.
- **Validación**: partición temporal (entrenar con periodos anteriores, probar con posteriores) y métricas [POR COMPLETAR].
- **Consideraciones éticas**: [POR COMPLETAR: datos agregados por comuna, sin información personal; confirmarlo con la fuente].

# Cronograma

[POR COMPLETAR: actividades de las fases 1 a 5 en semanas o meses según el calendario del programa.]

# Presupuesto

[POR COMPLETAR: se parte de herramientas gratuitas (Python, bibliotecas abiertas, datos abiertos). Si algo requiere pago, se declara aquí.]

# Referencias

::: {#refs}
:::
