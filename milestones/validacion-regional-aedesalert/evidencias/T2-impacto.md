# T2 · Criterio 2: Impacto social o técnico

- **Milestone:** `validacion-regional-aedesalert` · **Tarea:** T2
- **Pregunta del docente:** "¿Qué problema específico o cuello de botella resuelve en la región con sustento cuantitativo o técnico?"
- **Fecha de investigación y de consulta de todas las fuentes:** 2 de octubre de 2026 (salvo que se indique otra).
- **Informe de verificación de la v1:** `verificaciones/T2.md`

---

## ⚠️ Hallazgo crítico (cambia el argumento de la v1)

**Cali ya tiene un sistema de IA que anticipa brotes de dengue: DengueIA.** Lo desarrolló la Universidad Icesi con la Secretaría de Salud Pública de Cali, con apoyo de la Fundación Rockefeller y participación de la Universidad del Valle. Integra clima, casos de dengue, entomología, datos sociodemográficos y territoriales. Predice con 1 a 3 semanas de anticipación en 174 cuadrantes de 1 km² (unos 2,2 millones de habitantes), muestra el riesgo en rojo, amarillo y verde, y la Secretaría de Salud lo opera desde mayo de 2026 (memorando de entendimiento del 4 de mayo de 2026). Fuentes: hallazgos E1 a E5.

Consecuencias para este criterio:

1. La frase de la v1 *"la vigilancia del dengue en Cali es reactiva"* y la de que la propuesta *"integra dos fuentes que hoy se analizan por separado"* **ya no son ciertas para Cali en octubre de 2026**. Si el docente conoce DengueIA (salió en El País, El Tiempo y la Alcaldía), la v1 pierde credibilidad.
2. El *problema* sigue siendo real y está bien cuantificado (secciones A a D). Además, DengueIA **valida técnicamente el enfoque**: la propia ciudad adoptó un modelo de clima más casos para anticipar.
3. El *cuello de botella que resuelve AedesAlert* se **reformula** (ver §3). **Decisión del gate wave 1: opción A** ("complemento abierto"): misma idea, presentada como una versión abierta y replicable de DengueIA (datos abiertos y código libre) para los otros municipios del Valle en riesgo muy alto. DengueIA se cita como prueba de que el enfoque funciona. Criterio 2: 4/5.

---

## 1. Respuesta corta a la pregunta del criterio

Los códigos entre corchetes ([B3], [D1]…) remiten a los hallazgos de §2, donde cada cifra tiene su URL. Lo mismo vale para §3, §4 y §5.

> El dengue es endémico en el Valle del Cauca, con brotes cada 2 a 4 años, y el Plan Territorial de Salud clasifica a Cali y a otros 8 municipios en riesgo **muy alto** [B5, B6]. En 2024 Cali tuvo una incidencia de **1.520 casos por 100.000 habitantes**, frente a 937 en el país [B3, A1]. Declaró emergencia sanitaria el 11 de junio de 2024 [B1] y registró 21 muertes ese año [B4]. En Colombia, el dengue cuesta cerca de **USD 159,6 millones directos y USD 92,8 millones indirectos** (dólares de 2020) [D1, D2]. La evidencia académica muestra que en Cali el clima de **2 a 5 semanas antes** mejora la predicción por barrio [F1], que en el Valle la temperatura es la señal climática más robusta [F2], y que en Colombia un Random Forest con casos y clima rezagados supera a ARIMA [F3]. La experiencia de DengueIA demuestra que anticipar con 1 a 3 semanas es viable en Cali [E4]. **El cuello de botella que queda** es que esa capacidad no se conoce como abierta ni replicable: es un sistema institucional de Cali (ninguna fuente indica que sus datos, código o mapa sean públicos), trabaja en cuadrantes de 1 km² y no por comuna, [E2, E6], y no se conoce un sistema equivalente en los otros 8 municipios del Valle en riesgo muy alto ni para actores como IPS, EPS y laboratorios. AedesAlert lo ataca con un modelo **abierto, de bajo costo y replicable**, construido solo con datos abiertos (SIVIGILA y NASA POWER) y agregado por comuna.

---

## 2. Hallazgos (cifra + fuente + URL + fecha de consulta)

Todas las URL se consultaron el 2 de octubre de 2026. Cuando la página oficial no se pudo abrir (cali.gov.co devuelve 403 a la herramienta), se usó una réplica de prensa especializada y se indica.

### A. Carga del dengue en Colombia

| # | Dato | Cifra | Fuente | URL |
|---|---|---|---|---|
| A1 | Casos de dengue en Colombia en 2024 | 312.643 casos; 37,2 % con signos de alarma; 1,3 % grave; 284 muertes confirmadas; incidencia 937,4 por 100.000 hab. | INS, Informe de evento dengue 2024 (pp. 4 y 7) | https://www.ins.gov.co/buscador-eventos/Informesdeevento/DENGUE%20INFORME%20DE%20EVENTO%202024.pdf |
| A2 | Concentración regional 2024 | La región Pacífica aportó el 33,1 % de los casos del país (103.471); el Valle del Cauca y Cali concentraron el 85,0 % de ellos (87.914) | INS, Informe de evento dengue 2024 (pp. 8-9) | https://www.ins.gov.co/buscador-eventos/Informesdeevento/DENGUE%20INFORME%20DE%20EVENTO%202024.pdf |
| A3 | Colombia en 2025 (corte al 27-dic-2025) | 123.756 casos; 45.708 hospitalizaciones; 118 muertes confirmadas; 37,12 % con signos de alarma | Portafolio con datos del INS (8-ene-2026) | https://www.portafolio.co/economia/regiones/colombia-cerro-2025-con-123-756-casos-de-dengue-y-45-708-hospitalizaciones-485917 |
| A4 | Colombia en 2026, último boletín INS sobre dengue (semana 33, con corte en el periodo VIII = 32 semanas) | 70.350 casos; 38,6 % con signos de alarma; 1,0 % grave; 41 muertes confirmadas; incidencia 210,8 por 100.000; 27,0 % menos que en el mismo periodo de 2025 | INS, Boletín Epidemiológico Semanal, semana 33 de 2026 | https://www.ins.gov.co/BibliotecaDigital/2026-boletin-epidemiologico-semana-33.pdf |
| A5 | Situación nacional de brote en 2026 | El país se clasifica en situación de brote; 68.370 casos a la semana 31 | La FM (21-ago-2026) | https://www.lafm.com.co/sociedad/dengue-piocaduras-zancudos-mosquitos-colombia-muertes-afectados-408539 |
| A6 | Aumentos en Cali y el Valle en 2026 | A la semana 20 (43.868 casos en el país), **Cali** y el **Valle del Cauca** figuran entre las entidades con aumento superior al 30 % en la notificación | La FM, D. Cabrera (2-jun-2026) | https://www.lafm.com.co/sociedad/dengue-en-colombia-casos-aumentan-regiones-vigilancia-401129 |

### B. Cali y el Valle del Cauca

| # | Dato | Cifra | Fuente | URL |
|---|---|---|---|---|
| B1 | Emergencia sanitaria en Cali | Declarada el **11 de junio de 2024**. Más de 20.000 casos reportados a la fecha; a la semana 21: 12.452 sin signos de alarma (63,7 %), **6.918 con signos de alarma (35,4 %)** y **175 graves (0,9 %)**, es decir, 19.545 casos clasificados; 4 muertes | Consultor Salud (12-jun-2024) | https://consultorsalud.com/cali-emergencia-sanitaria-casos-de-dengue/ |
| B2 | Casos en Cali en 2024 (a la semana 39) | 34.463 casos; 21.917 sin signos de alarma | Consultor Salud (17-oct-2024), con datos de la Secretaría de Salud de Cali | https://consultorsalud.com/reduccion-dengue-cali-estrategias-efectivas/ |
| B3 | Incidencia de Cali en 2024 | **1.520 casos por 100.000 hab.**, frente a 937 en el promedio nacional | Fundación Rockefeller (5-may-2026); El País (5-may-2026) | https://www.rockefellerfoundation.org/news/dengueai-model-anticipates-outbreaks-93-effectiveness-three-weeks-advance-notice/ · https://www.elpais.com.co/cali/cali-usara-inteligencia-artificial-para-anticipar-brotes-de-dengue-asi-funcionara-dengueia-0537.html |
| B4 | Muertes por dengue en Cali en 2024 | 21 muertes confirmadas (entre las entidades territoriales con más muertes) | INS, Informe de evento dengue 2024 (p. 11) | https://www.ins.gov.co/buscador-eventos/Informesdeevento/DENGUE%20INFORME%20DE%20EVENTO%202024.pdf |
| B5 | Clasificación de riesgo | Cali en **"muy alto riesgo"** de transmisión, junto con Buga, Candelaria, Yumbo, Palmira, Tuluá, Cartago, Florida y Jamundí (9 municipios) | Gobernación del Valle, Plan Territorial de Salud 2024-2027 (p. 22) | https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=73263 |
| B6 | Patrón epidémico | "El dengue, en el Valle del Cauca, es una enfermedad endémica con ciclos epidémicos (brotes) cada dos a cuatro años" | PTS 2024-2027 (p. 22) | https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=73263 |
| B7 | Valle del Cauca en 2023 | 24.747 casos notificados (incluidos los distritos); incidencia de 594 por 100.000 hab.; letalidad acumulada 2020-2023 del 0,08 % | PTS 2024-2027 | https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=73263 |
| B8 | Valle del Cauca en 2025 | Más de 7.800 casos y 0 muertes. *Supuesto: probablemente sin los distritos de Cali y Buenaventura, como en los informes departamentales (ver B9); la nota no lo aclara* | Gobernación del Valle (8-ene-2026) | https://www.valledelcauca.gov.co/publicaciones/88162/el-valle-del-cauca-no-registro-muertes-por-dengue-durante-2025/ |
| B9 | Valle en el 1.er trimestre de 2024 (sin Cali ni Buenaventura) | 17.342 casos; incidencia de 1.031 por 100.000; brote desde la semana 25 de 2023 | Gobernación del Valle, informe de eventos de interés en salud, trimestre I de 2024 | https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=73499 |
| B10 | Comunas de Cali | 22 comunas (las acciones de control de 2024 cubrieron "las 22 comunas") | Consultor Salud (17-oct-2024) | https://consultorsalud.com/reduccion-dengue-cali-estrategias-efectivas/ |
| B11 | Vacunación en 2026 | El Ministerio de Salud amplía la vacunación contra el dengue en Cali para niñas y niños de 9 años o de cuarto grado (jornada del 14 al 19 de septiembre de 2026) | El País (15-sep-2026) | https://www.elpais.com.co/colombia/ministerio-de-salud-intensifica-vacunacion-en-colombia-y-amplia-cobertura-contra-el-dengue-en-cali-1549.html |

**No encontrado:** una cifra oficial de casos de dengue **de Cali en 2026** (acumulado por semana). El boletín INS de la semana 33 no desagrega a Cali, y las publicaciones de cali.gov.co no se pudieron abrir (403). Solo se sabe que Cali tuvo un aumento superior al 30 % en la notificación a la semana 20 (A6). Para 2025 en Cali solo se encontró el dato de mayo (C1).

### C. Evidencia de que la focalización funciona

| # | Dato | Cifra | Fuente | URL |
|---|---|---|---|---|
| C1 | Cali, mayo de 2025 | "Más de 50 barrios con cero o un caso de dengue"; 2.055 casos en 2025 a esa fecha (1.437 sin signos de alarma; 20 graves); 101 casos nuevos en la semana 19. La Alcaldía lo atribuye a la fumigación focalizada (hasta 4 jornadas intensivas en barrios como Morichal, El Guabal y Alirio Mora Beltrán, y más de 5 en la comuna 17) y a la participación comunitaria | Consultor Salud (27-may-2025), réplica del boletín de la Alcaldía de Cali (26-may-2025, no se pudo abrir: 403) | https://consultorsalud.com/fumigacion-dengue-cali-2025-control-vectorial/ · https://www.cali.gov.co/boletines/publicaciones/186981/fumigacion-oportuna-permite-a-cali-registrar-mas-de-50-barrios-sin-casos-de-dengue-en-2025/ |
| C2 | Escala del control vectorial en 2024 | 633.750 sumideros revisados; 20.229 viviendas fumigadas con motomochila; 602.716 predios con máquina pesada; 13.113 manzanas fumigadas | Consultor Salud (17-oct-2024) | https://consultorsalud.com/reduccion-dengue-cali-estrategias-efectivas/ |
| C3 | Intervención focalizada en el Valle | En Vijes, una película repelente en tanques y lavaderos redujo la tasa de dengue en un 92 % (piloto) | Gobernación del Valle (8-ene-2026) | https://www.valledelcauca.gov.co/publicaciones/88162/el-valle-del-cauca-no-registro-muertes-por-dengue-durante-2025/ |

**Matiz:** C1 y C3 son comunicados institucionales, no evaluaciones con grupo de comparación. 2025 fue un año de baja transmisión en todo el país (A3 frente a A1), así que no se puede atribuir toda la caída a la fumigación. Sirven como indicio de que focalizar ayuda, no como prueba causal. C2 muestra la magnitud del esfuerzo, que es justo lo que una buena priorización permite dirigir mejor.

### D. Costo del dengue

| # | Dato | Cifra | Fuente | URL |
|---|---|---|---|---|
| D1 | Costo directo agregado anual en Colombia | Cerca de **USD 159,6 millones** (atención ambulatoria USD 90,1 M y casos fatales USD 30,7 M = 75 % del total) | Rodríguez-Morales et al. (2024), *PLOS NTD* | https://doi.org/10.1371/journal.pntd.0012718 |
| D2 | Costo indirecto agregado (ingreso perdido por enfermedad o por cuidar a un enfermo) | **USD 92,8 millones** | Rodríguez-Morales et al. (2024) | https://doi.org/10.1371/journal.pntd.0012718 |
| D3 | Costo médico directo por hospitalización | USD 823 a 1.754 por episodio | Rodríguez-Morales et al. (2024) | https://doi.org/10.1371/journal.pntd.0012718 |

**Matiz:** es una revisión sistemática de 14 estudios del periodo 2010-2020, con valores en dólares de 2020. La suma de D1 y D2 (≈ USD 252 millones) es válida como orden de magnitud. El artículo no da la conversión a pesos, así que la cifra de "más de $1 billón de pesos" del documento de contexto no tiene respaldo en esta fuente.

### E. Estado del arte en Cali: DengueIA

| # | Dato | Cifra | Fuente | URL |
|---|---|---|---|---|
| E1 | Qué es y quién lo hace | Sistema de IA de la Universidad Icesi con la Secretaría de Salud Pública de Cali, apoyado por la Fundación Rockefeller y con participación de la Universidad del Valle | El País (5-may-2026); Fundación Rockefeller (5-may-2026) | https://www.elpais.com.co/cali/cali-usara-inteligencia-artificial-para-anticipar-brotes-de-dengue-asi-funcionara-dengueia-0537.html · https://www.rockefellerfoundation.org/news/dengueai-model-anticipates-outbreaks-93-effectiveness-three-weeks-advance-notice/ |
| E2 | Unidad espacial y cobertura | 174 cuadrantes de 1 km², con unos 2,2 millones de habitantes | El País (18-may-2026) | https://www.elpais.com.co/cali/asi-funciona-dengueia-la-herramienta-que-predice-casos-de-dengue-semanas-antes-en-cali-1857.html |
| E3 | Variables | Densidad poblacional, lluvia, temperatura, humedad, vegetación, sumideros, recolección de residuos y agua estancada; además, entomología y sociodemografía | El País (18-may-2026); Universidad Icesi (30-jul-2025) | https://www.elpais.com.co/cali/asi-funciona-dengueia-la-herramienta-que-predice-casos-de-dengue-semanas-antes-en-cali-1857.html · https://www.icesi.edu.co/blogs/dengue-ia-cali/2025/07/30/primera-rueda-de-prensa-de-dengue-ia-ver-antes-actuar-a-tiempo/ |
| E4 | Desempeño | Alertas a 1, 2 y 3 semanas; "93 % de efectividad"; identificó incrementos de riesgo en más del 90 % de los casos evaluados en 91 zonas priorizadas durante 3 meses de validación | Fundación Rockefeller (5-may-2026); El País (18-may-2026) | https://www.rockefellerfoundation.org/news/dengueai-model-anticipates-outbreaks-93-effectiveness-three-weeks-advance-notice/ |
| E5 | Estado de uso | La Secretaría de Salud lo usa desde la firma de un memorando de entendimiento el 4 de mayo de 2026; asignó 3 personas para alimentarlo y presentar sus resultados en los comités de análisis epidemiológico. Tiene un componente prescriptivo (recomienda fumigación, visitas y limpieza de sumideros). Mapa en rojo, amarillo y verde | Fundación Rockefeller; El País (18-may-2026); Universidad Icesi (30-jul-2025) | https://www.elpais.com.co/cali/asi-funciona-dengueia-la-herramienta-que-predice-casos-de-dengue-semanas-antes-en-cali-1857.html |
| E6 | Apertura | Ninguna de las fuentes dice que los datos, el código o el mapa sean públicos | El País; Icesi (sin mención) | https://www.icesi.edu.co/blogs/dengue-ia-cali/2025/07/30/primera-rueda-de-prensa-de-dengue-ia-ver-antes-actuar-a-tiempo/ |

Hay un boletín de la Alcaldía con el título *"DengueIA: nuevo modelo que pronostica casos de dengue con un 93% de efectividad y tres semanas de antelación"* (https://www.cali.gov.co/boletines/publicaciones/192444/), pero no se pudo abrir (403). Su contenido se verificó con la Fundación Rockefeller y El País.

### F. Sustento técnico: por qué el clima rezagado más los casos permite anticipar

| # | Estudio | Hallazgo cuantitativo | DOI |
|---|---|---|---|
| F1 | Desjardins et al. (2020). Cali, 340 barrios, 2015-2016, modelo autorregresivo condicional espacio-temporal | Siete variables meteorológicas (temperatura media, rango térmico, rango de humedad, lluvia total, días de lluvia, días frescos y días cálidos) con **rezagos óptimos de 2 a 5 semanas** mejoraron el ajuste del modelo. Hay fuerte dependencia espacial entre barrios (ρ = 0,98) | https://doi.org/10.4269/ajtmh.20-0080 |
| F2 | Ortega-Lenis et al. (2024). Valle del Cauca, 2001-2019, modelo bayesiano espacio-temporal (INLA) con modelos no lineales de rezago distribuido | Riesgo relativo máximo de **1,40 (IC 95 %: 1,17-1,67) a 26 °C con 0 a 2 meses de rezago**. Para lluvia (RR 1,22 con 2 a 3 meses de rezago) y humedad (RR 1,35) los intervalos de confianza incluyen 1, es decir, no son significativos. Años epidémicos: 2002, 2010, 2013, 2015 y 2016 | https://doi.org/10.1371/journal.pone.0311607 |
| F3 | Zhao et al. (2020). Colombia, nivel nacional y departamental, Random Forest y redes neuronales frente a ARIMA | Con casos de las 11 semanas previas y clima (lluvia, temperatura de superficie, índice de vegetación) con rezagos de 0 a 11 semanas, el **Random Forest superó a ARIMA**. El error aumenta con el horizonte (MAE de 9,32 a 1 semana y de 24,56 a 12 semanas). El clima pesa más en el corto plazo | https://doi.org/10.1371/journal.pntd.0008056 |

**Lectura técnica:** el mosquito *Aedes aegypti* tarda varias semanas entre la lluvia y la temperatura favorables, la cría, la infección y los síntomas. Por eso el clima de **2 a 5 semanas antes** (F1) y la temperatura de los 0 a 2 meses previos (F2) predicen los casos, y los casos recientes aportan la inercia de la transmisión (F3). El diseño de AedesAlert (clima rezagado más casos rezagados, con RF/XGBoost comparado con un SARIMA de línea base) coincide con lo que la literatura respalda y con lo que DengueIA ya demostró en Cali (E4). **Cautela:** en el Valle, la asociación es más robusta con la temperatura que con la lluvia o la humedad (F2).

---

## 3. Cuello de botella reformulado (decisión del gate wave 1: opción A)

| v1 (ya no se sostiene) | v2 propuesta |
|---|---|
| "La vigilancia es reactiva; casos y clima se analizan por separado." | "Cali ya demostró con DengueIA que anticipar el dengue con clima y casos funciona (93 % de efectividad, 1 a 3 semanas). El cuello de botella que queda es que **esa capacidad no es abierta ni replicable**: es un sistema institucional de Cali (con apoyo de una fundación internacional y dos universidades) que no se publica por comuna y no llega a los **otros 8 municipios del Valle en riesgo muy alto**." |
| "El modelo permite anticipar dónde focalizar." | "AedesAlert ofrece una versión **abierta y de bajo costo**: solo con datos abiertos (SIVIGILA y NASA POWER), código libre y agregación por **comuna**, que es la unidad con la que planean la Alcaldía y los actores privados (IPS, EPS, laboratorios). Sirve como herramienta complementaria, como referencia de comparación y como base replicable para Palmira, Tuluá, Buga, Cartago, Jamundí, Yumbo, Candelaria y Florida." |

**Nota sobre la evidencia:** no se encontró evidencia de que los otros 8 municipios en riesgo muy alto tengan un sistema predictivo, pero tampoco se buscó municipio por municipio. La v2 debería decir "no se conoce un sistema equivalente", no "no existe".

---

## 4. Puntaje propuesto: **4 / 5** (la v1 tenía 5)

**Justificación:**

- **A favor (sustento cuantitativo muy sólido, propio de un 5):** el problema está documentado con fuentes oficiales y revisadas por pares: incidencia en Cali de 1.520 por 100.000 en 2024 (1,6 veces la nacional), emergencia sanitaria, 21 muertes, riesgo muy alto en el PTS, brotes cada 2 a 4 años y costo de unos USD 252 millones anuales. El sustento técnico también es sólido: tres estudios con DOI, dos de ellos de Cali y el Valle, respaldan el uso de clima rezagado, y DengueIA demuestra que el enfoque funciona en la ciudad.
- **En contra (resta 1 punto):** el cuello de botella "anticipar dónde focalizar" **ya lo resolvió parcialmente DengueIA en Cali desde mayo de 2026**, con más variables y más resolución espacial (1 km² frente a comuna). El aporte de AedesAlert pasa a ser incremental: apertura, replicabilidad regional y unidad comuna. Ese aporte es real, pero no está probado que sea una necesidad sentida de la Secretaría ni de los otros municipios. Además, la evidencia de que "focalizar funciona" es de comunicados institucionales, sin evaluación causal.
- **Si se mantuviera el texto de la v1** (sin mencionar DengueIA), el puntaje honesto sería **3**, porque la afirmación central sobre el problema contradice la situación actual de Cali.

---

## 5. Texto sugerido para la fila de la matriz (insumo para T5)

> **Cuello de botella:** anticipar dónde focalizar el control del dengue de forma abierta y replicable. Cali tuvo 1.520 casos por 100.000 hab. en 2024 (937 en el país) [B3, A1] y declaró emergencia sanitaria [B1]. El PTS del Valle clasifica a Cali y a otros 8 municipios en riesgo muy alto y describe brotes cada 2 a 4 años en el departamento [B5, B6], y el dengue cuesta a Colombia cerca de USD 252 millones al año, en dólares de 2020 [D1, D2]. Cali ya valida el enfoque con DengueIA (93 % de efectividad reportada, hasta 3 semanas) [E4]. AedesAlert lo vuelve abierto y replicable: predicción semanal por comuna con datos abiertos (SIVIGILA + NASA POWER) y clima rezagado de 2 a 5 semanas (Desjardins et al., 2020), con Random Forest/XGBoost frente a SARIMA. **Puntaje: 4.**

**Frase corta de diferenciación (para la matriz):**

> DengueIA demostró en Cali que anticipar el dengue funciona. AedesAlert lleva ese enfoque a una versión abierta (datos abiertos y código libre) y replicable en los otros 8 municipios del Valle en riesgo muy alto [E4, E6, B5].

---

## 6. Supuestos

- **Decisión del gate wave 1: opción A** ("complemento abierto"). Se mantiene la idea (pedido "misma idea" del triage) y se presenta como una versión abierta y replicable de DengueIA para los otros municipios del Valle en riesgo muy alto. DengueIA se cita como prueba de que el enfoque funciona. Puntaje del criterio 2: 4/5.
- **S2.** Para el dato nacional de 2025 se usa la cifra de Portafolio (123.756 casos, con corte INS al 27-dic-2025) en lugar de la de El País del documento de contexto (123.745). La diferencia es menor y se explica por la fecha de corte.
- **S3.** El último boletín INS con un capítulo de dengue es el de la semana 33 de 2026. El de la semana 37 existe, pero trata otros eventos.
- **S4.** Las páginas de cali.gov.co no se pudieron abrir (403). Sus datos se tomaron de réplicas (Consultor Salud, El País, Fundación Rockefeller) y las URL originales se dejan como referencia.

---

## 7. Referencias (APA 7)

Alcaldía de Santiago de Cali. (2025, 26 de mayo). *Fumigación oportuna permite a Cali registrar más de 50 barrios sin casos de dengue en 2025*. https://www.cali.gov.co/boletines/publicaciones/186981/fumigacion-oportuna-permite-a-cali-registrar-mas-de-50-barrios-sin-casos-de-dengue-en-2025/

Cabrera, D. (2026, 2 de junio). Colombia supera los 43.000 casos de dengue en 2026. *La FM*. https://www.lafm.com.co/sociedad/dengue-en-colombia-casos-aumentan-regiones-vigilancia-401129

Consultor Salud. (2024a, 12 de junio). *Cali declaró emergencia sanitaria por incremento de casos de dengue*. https://consultorsalud.com/cali-emergencia-sanitaria-casos-de-dengue/

Consultor Salud. (2024b, 17 de octubre). *Reducción en los casos de dengue en Cali: estrategias demuestran efectividad*. https://consultorsalud.com/reduccion-dengue-cali-estrategias-efectivas/

Consultor Salud. (2025, 27 de mayo). *Fumigación oportuna permite a Cali registrar más de 50 barrios sin casos de dengue en 2025*. https://consultorsalud.com/fumigacion-dengue-cali-2025-control-vectorial/

Desjardins, M. R., Eastin, M. D., Paul, R., Casas, I., & Delmelle, E. M. (2020). Space–time conditional autoregressive modeling to estimate neighborhood-level risks for dengue fever in Cali, Colombia. *The American Journal of Tropical Medicine and Hygiene, 103*(5), 2040–2053. https://doi.org/10.4269/ajtmh.20-0080

El País. (2026a, 18 de mayo). Así funciona DengueIA, la herramienta que predice casos de dengue semanas antes en Cali; así fue su construcción. *El País*. https://www.elpais.com.co/cali/asi-funciona-dengueia-la-herramienta-que-predice-casos-de-dengue-semanas-antes-en-cali-1857.html

El País. (2026b, 24 de julio). Icesi ayuda a rastrear el dengue en Cali con el uso de la IA. *El País*. https://www.elpais.com.co/500-empresas/icesi-ayuda-a-rastrear-el-dengue-en-cali-con-el-uso-de-la-ia-2500.html

El País. (2026c, 15 de septiembre). Ministerio de Salud intensifica vacunación en Colombia y amplía cobertura contra el dengue en Cali. *El País*. https://www.elpais.com.co/colombia/ministerio-de-salud-intensifica-vacunacion-en-colombia-y-amplia-cobertura-contra-el-dengue-en-cali-1549.html

Erazo Córdoba, J. W. (2026, 5 de mayo). Cali usará inteligencia artificial para anticipar brotes de dengue: así funcionará DengueIA. *El País*. https://www.elpais.com.co/cali/cali-usara-inteligencia-artificial-para-anticipar-brotes-de-dengue-asi-funcionara-dengueia-0537.html

Gobernación del Valle del Cauca. (2024a). *Informe del comportamiento de los eventos de interés en salud pública, trimestre I de 2024*. https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=73499

Gobernación del Valle del Cauca. (2024b). *Plan Territorial de Salud 2024-2027*. https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=73263

Gobernación del Valle del Cauca. (2026, 8 de enero). *El Valle del Cauca no registró muertes por dengue durante 2025*. https://www.valledelcauca.gov.co/publicaciones/88162/el-valle-del-cauca-no-registro-muertes-por-dengue-durante-2025/

Instituto Nacional de Salud. (2025). *Informe de evento: dengue, 2024* (códigos 210, 220, 580). https://www.ins.gov.co/buscador-eventos/Informesdeevento/DENGUE%20INFORME%20DE%20EVENTO%202024.pdf

Instituto Nacional de Salud. (2026). *Boletín epidemiológico semanal: semana epidemiológica 33 de 2026*. https://www.ins.gov.co/BibliotecaDigital/2026-boletin-epidemiologico-semana-33.pdf

La FM. (2026, 21 de agosto). Dengue en Colombia entra en situación de brote: más de 68.000 casos y 41 muertes confirmadas en 2026. *La FM*. https://www.lafm.com.co/sociedad/dengue-piocaduras-zancudos-mosquitos-colombia-muertes-afectados-408539

Ortega-Lenis, D., Arango-Londoño, D., Hernández, F., & Moraga, P. (2024). Effects of climate variability on the spatio-temporal distribution of dengue in Valle del Cauca, Colombia, from 2001 to 2019. *PLOS ONE, 19*(10), e0311607. https://doi.org/10.1371/journal.pone.0311607

Rodríguez, D. K. (2026, 8 de enero). Casos de dengue en Colombia 2025 llegaron a 123.756 y dejaron 118 muertes: INS. *Portafolio*. https://www.portafolio.co/economia/regiones/colombia-cerro-2025-con-123-756-casos-de-dengue-y-45-708-hospitalizaciones-485917

Rodríguez-Morales, A. J., López-Medina, E., Arboleda, I., Cardona-Ospina, J. A., Castellanos, J., Faccini-Martínez, Á. A., Gallagher, E., Hanley, R., López, P., Mattar, S., Pérez, C. E., Kastner, R., Reynales, H., Rosso, F., Shen, J., Villamil-Gómez, W. E., & Fuquen, M. (2024). Cost of dengue in Colombia: A systematic review. *PLOS Neglected Tropical Diseases, 18*(12), e0012718. https://doi.org/10.1371/journal.pntd.0012718

The Rockefeller Foundation. (2026, 5 de mayo). *DengueAI: New model that anticipates outbreaks with 93% effectiveness and three weeks' advance notice*. https://www.rockefellerfoundation.org/news/dengueai-model-anticipates-outbreaks-93-effectiveness-three-weeks-advance-notice/

Universidad Icesi. (2025, 30 de julio). *Primera rueda de prensa de Dengue.IA: ver antes, actuar a tiempo*. Bitácora de Dengue.IA. https://www.icesi.edu.co/blogs/dengue-ia-cali/2025/07/30/primera-rueda-de-prensa-de-dengue-ia-ver-antes-actuar-a-tiempo/

Zhao, N., Charland, K., Carabali, M., Nsoesie, E. O., Maheu-Giroux, M., Rees, E., Yuan, M., Garcia Balaguera, C., Jaramillo Ramirez, G., & Zinszer, K. (2020). Machine learning and dengue forecasting: Comparing random forests and artificial neural networks for predicting dengue burden at national and sub-national scales in Colombia. *PLOS Neglected Tropical Diseases, 14*(9), e0008056. https://doi.org/10.1371/journal.pntd.0008056
