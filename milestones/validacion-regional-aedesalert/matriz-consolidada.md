# Matriz de selección consolidada · AedesAlert Cali (v2)

> Fuente única de verdad para T6 (Word), T7 (deck HTML) y T8 (guion). Toda cifra de este archivo está en `evidencias/` con su URL; la §8 dice en qué archivo y en qué hallazgo. Si un entregable necesita una cifra que no está aquí, primero se agrega aquí con su trazabilidad.

---

## 1. Ficha

| Campo | Contenido |
|---|---|
| Título | Evaluación de la idea de negocio AedesAlert Cali bajo cuatro criterios de validación regional. Matriz de selección para el contexto de Cali y el Valle del Cauca |
| Idea | **AedesAlert Cali**: modelo predictivo basado en inteligencia artificial para identificar zonas de riesgo de propagación del dengue, como complemento abierto y replicable de DengueIA |
| Autor | Juan Diego Nieto (trabajo individual) |
| Programa | Ingeniería de Sistemas, Universidad Cooperativa de Colombia, sede Cali |
| Curso | Ideación, Emprendimiento y Desarrollo Tecnológico |
| Docente | ______________________________ |
| Lugar y fecha | Santiago de Cali, 2 de octubre de 2026 |
| Escala de puntaje | 1 = no cumple · 2 = cumple de forma mínima · 3 = cumple parcialmente · 4 = cumple con evidencia, pero con una limitación relevante · 5 = cumple con evidencia verificable |

---

## 2. Descripción de la idea

AedesAlert Cali es una herramienta abierta de apoyo a la toma de decisiones en salud pública. Integra los casos de dengue notificados al SIVIGILA con variables climáticas de NASA POWER (lluvia, temperatura y humedad) para predecir cada semana el riesgo de propagación del dengue por comuna y mostrarlo en un mapa tipo semáforo; para ello compara modelos de aprendizaje automático (Random Forest y XGBoost) con un modelo SARIMA como línea base. Desde mayo de 2026, la Secretaría de Salud Pública de Cali usa DengueIA, un sistema desarrollado con la Universidad Icesi, con participación de la Universidad del Valle y apoyo de la Fundación Rockefeller, que anticipa el riesgo hasta con tres semanas y un 93 % de efectividad reportada (El País, 2026; The Rockefeller Foundation, 2026). AedesAlert no compite con DengueIA: lo toma como prueba de que el enfoque funciona y propone una versión complementaria, construida solo con datos abiertos y código libre, que se prototipa con las 22 comunas de Cali y está pensada para replicarse en los otros ocho municipios del Valle clasificados en riesgo muy alto: Buga, Candelaria, Cartago, Florida, Jamundí, Palmira, Tuluá y Yumbo (Gobernación del Valle del Cauca, 2024e). La herramienta predice y alerta; no previene por sí misma, pero permite que las acciones de prevención lleguen antes.

---

## 3. Matriz de selección

**Tabla 1.** Matriz de selección de la idea AedesAlert Cali

| CRITERIO DE EVALUACIÓN | DESCRIPCIÓN DEL CUMPLIMIENTO (CONTEXTO CALI / VALLE) | PUNTAJE (1-5) |
|---|---|---|
| **Caracterización Económica**<br>*¿A qué sector productivo del Valle del Cauca fortalece o transforma?* | Transforma el sector Salud, en su segmento HealthTech, con capacidades del sector TI. Aporta a la línea «Modelos de negocio HealthTech» del Clúster de Excelencia Clínica (528 empresas en 2023), priorizada en 2025, en una región cuyas instituciones de salud tienen madurez digital intermedia (2,42/5) (Cámara de Comercio de Cali, 2025a, 2025c). El empleo TIC del Valle creció en promedio 7,2 % frente a 4,9 % nacional en 2019-2023 (Cámara de Comercio de Cali, 2025b). El Valle es la 3.ª economía del país (≈9,8 % del PIB 2025pr; DANE, 2026). | **5** |
| **Impacto Social o Técnico**<br>*¿Qué problema específico o cuello de botella resuelve en la región con sustento cuantitativo o técnico?* | Cuello de botella: anticipar dónde focalizar, con una herramienta abierta y replicable. Cali tuvo 1.520 casos por 100.000 hab. en 2024 (937 en el país) y declaró emergencia sanitaria (Erazo Córdoba, 2026; Consultor Salud, 2024a). El PTS ubica a Cali y otros 8 municipios en riesgo muy alto (Gobernación del Valle del Cauca, 2024e). DengueIA ya valida el enfoque en Cali (93 % de efectividad reportada; The Rockefeller Foundation, 2026); AedesAlert lo replica por comuna con datos abiertos y clima rezagado de 2 a 5 semanas (Desjardins et al., 2020). | **4** |
| **Políticas de Fomento**<br>*¿Con qué plan de desarrollo (Alcaldía/Gobernación) o política de CTeI se alinea?* | Nacional: CONPES 4144 de 2025, Política Nacional de IA (ejes Datos e infraestructura y Uso y adopción de la IA; MinTIC, 2025), y Plan Decenal de Salud Pública 2022-2031. Departamental: Plan «Liderazgo que Transforma» 2024-2027, subprogramas «Valle innovador: distritos de innovación e inteligencia artificial» y «Prevención y promoción en salud»; el PTS propone IA y análisis de datos (Gobernación del Valle del Cauca, 2024d, 2024e). Distrital: Cali prioriza el dengue y las enfermedades transmitidas por vectores, y ya aplica IA con DengueIA. | **5** |
| **Apoyo del Ecosistema**<br>*¿Qué entidad o programa local (Cámara de Comercio - NIDO, Valle INN, SENA) podría apalancar o cofinanciar la propuesta?* | Apalancamiento gratuito desde ya: SENA-Tecnoparque (sublínea de IA y geotecnología) para el prototipo, y NIDO, que acompañó 220 startups en 2024-2025 (Cámara de Comercio de Cali, 2026) y abrió ValleyCare para HealthTech en 2024. Validación: la Secretaría de Salud y los grupos de Icesi y Univalle de DengueIA como referencia, y el Clúster de Excelencia Clínica para pilotos con IPS y EPS. Cofinanciación: Fondo Emprender, cuyas convocatorias 2026 cerraron en abril (Infobae, 2026). Hoy no hay convocatoria abierta. | **4** |
| **TOTAL** | Idea viable para Cali y el Valle del Cauca como complemento abierto y replicable de DengueIA. Riesgo principal: demanda no validada en los otros municipios y disponibilidad de datos históricos por comuna. | **18/20** |

*Nota.* Escala de 1 (no cumple) a 5 (cumple con evidencia verificable). Elaboración propia con base en las fuentes citadas.

**Frase de una línea por criterio** (para la diapositiva de la matriz y el guion):

| Criterio | Frase corta | Puntaje |
|---|---|---|
| Caracterización económica | Transforma el sector Salud (HealthTech) con capacidades TI | 5 |
| Impacto social o técnico | Problema grande y medido; DengueIA prueba el enfoque, AedesAlert lo abre y lo replica | 4 |
| Políticas de fomento | Alineada en los tres niveles; Cali ya usa IA contra el dengue | 5 |
| Apoyo del ecosistema | Tecnoparque y NIDO apalancan ya; la cofinanciación dependerá de un próximo ciclo | 4 |
| **Total** | | **18/20** |

**Puntajes.** Se mantienen los propuestos por T1-T4 (C1 = 5, C2 = 4, C3 = 5, C4 = 4). Al cruzar las cuatro evidencias no se encontró una incoherencia que obligue a cambiarlos: DengueIA resta novedad en el criterio 2 (de 5 a 4), mientras que la evidencia nueva, incluido DengueIA, refuerza la alineación del criterio 3 (de 4 a 5), y el criterio 4 conserva el 4 de la v1 por otra razón (no hay convocatoria de cofinanciación abierta). El total, 18/20, coincide con el de la v1, aunque con otra composición.

---

## 4. Análisis por criterio

### 4.1 Caracterización económica

El Valle del Cauca es la tercera economía del país: con cifras preliminares de 2025 aportó cerca del 9,8 % del PIB nacional, después de Bogotá y Antioquia (DANE, 2026). AedesAlert Cali no crea un sector nuevo: transforma el sector salud al llevar la analítica de datos y la inteligencia artificial a la vigilancia epidemiológica, y para hacerlo usa capacidades del sector TI. En salud, la referencia regional es el Clúster de Excelencia Clínica de la Cámara de Comercio de Cali, que agrupaba 528 empresas en 2023 y tiene entre sus cuatro líneas de trabajo los «Modelos de negocio HealthTech», definidos como transformación digital y uso de datos en salud (Cámara de Comercio de Cali, 2025a). En 2025 la Cámara priorizó esa línea y midió una madurez digital «intermedia» (2,42 sobre 5) en 25 instituciones de salud de la región (Cámara de Comercio de Cali, 2025c). En TI, el empleo del sector en el Valle creció en promedio 7,2 % entre 2019 y 2023, frente al 4,9 % nacional (Cámara de Comercio de Cali, 2025b). Hay un matiz: el clúster se orienta sobre todo a servicios clínicos privados, mientras que AedesAlert sirve primero a la salud pública, así que el vínculo pasa por la línea HealthTech y por usuarios como IPS, EPS y laboratorios. Se asigna un puntaje de 5.

### 4.2 Impacto social o técnico

El dengue es endémico en el Valle del Cauca, con brotes cada dos a cuatro años, y el Plan Territorial de Salud 2024-2027 clasifica a Cali y a otros ocho municipios en riesgo muy alto (Gobernación del Valle del Cauca, 2024e). En 2024 Cali registró 1.520 casos por 100.000 habitantes, frente a 937 en el país (Erazo Córdoba, 2026; Instituto Nacional de Salud, 2025), y el 11 de junio declaró emergencia sanitaria con más de 20.000 casos (Consultor Salud, 2024a). En Colombia, el dengue cuesta cerca de USD 159,6 millones directos y USD 92,8 millones indirectos al año, en dólares de 2020 (Rodríguez-Morales et al., 2024). Anticipar es viable: en Cali, el clima de dos a cinco semanas antes mejora la predicción por barrio (Desjardins et al., 2020), y en Colombia un Random Forest con casos y clima rezagados supera a ARIMA (Zhao et al., 2020). DengueIA lo confirma, con alertas hasta tres semanas antes y un 93 % de efectividad reportada (The Rockefeller Foundation, 2026). Por eso el cuello de botella ya no es anticipar en Cali, sino que esa capacidad no se conoce como abierta ni replicable. AedesAlert la ofrece con datos abiertos, código libre y agregación por comuna. Como ese aporte es incremental y su demanda aún no está validada, se asigna 4.

### 4.3 Políticas de fomento

La alineación cubre los tres niveles. En el nacional, con el CONPES 4144 de 2025, Política Nacional de Inteligencia Artificial (2025-2030), en sus ejes de datos e infraestructura y de uso y adopción de la IA, con la salud entre los sectores estratégicos (DNP, 2025; MinTIC, 2025), y con el Plan Decenal de Salud Pública 2022-2031, en sus ejes de cambio climático y de conocimiento en salud pública (Ministerio de Salud y Protección Social, 2024). En el departamental, con el Plan de Desarrollo «Liderazgo que Transforma» 2024-2027 (Ordenanza 655 de 2024): en la Línea I, «Valle innovador: distritos de innovación e inteligencia artificial», y en la Línea II, «Prevención y promoción en salud» (Gobernación del Valle del Cauca, 2024c, 2024d). El Plan Territorial de Salud propone usar inteligencia artificial y análisis de datos (Gobernación del Valle del Cauca, 2024e), y Minciencias se articula a NIDO con misiones como la soberanía sanitaria (Gobernación del Valle del Cauca, 2024b). En el distrital, la planeación en salud de Cali prioriza el dengue y las enfermedades transmitidas por vectores (Ministerio de Salud y Protección Social y Ministerio de Hacienda y Crédito Público, 2025), y la Alcaldía ya aplica IA a su predicción con DengueIA (Universidad Icesi, s. f.). Aunque no se verificó una meta literal del plan distrital, se asigna 5.

### 4.4 Apoyo del ecosistema

Las entidades no encajan por igual, así que se propone una ruta priorizada. Primero, SENA-Tecnoparque, con acompañamiento técnico gratuito y permanente para el prototipo y una sublínea de inteligencia artificial y geotecnología (Red Tecnoparque Colombia, s. f.). Segundo, NIDO, de la Cámara de Comercio de Cali, la Gobernación y la Alcaldía, con Comfandi como cogestor desde abril de 2026: acompañó a 220 startups en 2024-2025 y su oferta 2026 va desde la ideación hasta la internacionalización (Cámara de Comercio de Cali, 2026; Gobernación del Valle del Cauca, 2026b); en 2024 abrió ValleyCare para HealthTech (Gobernación del Valle del Cauca, 2024a). Tercero, aliados de validación: la Secretaría de Salud y los grupos de Icesi y Univalle que construyeron DengueIA, como referencia de comparación, y el Clúster de Excelencia Clínica, para pilotos con IPS y EPS. Para cofinanciar, Fondo Emprender abrió en 2026 doce convocatorias por más de $282.000 millones en capital semilla (Infobae, 2026), pero cerraron en abril; el autor podría aplicar en un próximo ciclo cuando curse los dos últimos semestres o tenga el 80 % de los créditos (Ámbito Jurídico, 2024). ColombIA Inteligente se terminó en agosto de 2026 (Minciencias, 2026), y Valle INN+ ya adjudicó su convocatoria y tiene encaje bajo (Gobernación del Valle del Cauca, 2026a). Como no hay convocatoria abierta, se asigna 4.

---

## 5. Conclusión

AedesAlert Cali obtiene 18 de 20 puntos en la matriz de selección. Es sólida en caracterización económica, porque transforma el sector salud con capacidades TI en una de las líneas que la Cámara de Comercio de Cali priorizó, y en políticas de fomento, porque se alinea con instrumentos nacionales, departamentales y distritales, y Cali ya usa IA contra el dengue. En impacto obtiene 4: el problema es grande y está medido, pero DengueIA ya resolvió en parte la anticipación en Cali, de modo que el aporte de AedesAlert es ser abierto, por comuna y replicable. En ecosistema obtiene 4: hay apoyos gratuitos para empezar, pero ninguna convocatoria de cofinanciación está abierta. El **riesgo principal** es que ese valor diferencial no se traduzca en uso: aún no se ha validado con las secretarías de salud de los otros municipios, y no está confirmado que existan datos históricos por comuna de varios años que incluyan el brote de 2024. El **siguiente paso** es confirmar qué años publica Datos Abiertos Cali (y pedir los faltantes a la Secretaría de Salud mediante un derecho de petición), presentar el prototipo a Tecnoparque y buscar la retroalimentación de una secretaría municipal en riesgo muy alto. Con base en esta evaluación, la idea es viable para el contexto de Cali y el Valle del Cauca.

---

## 6. Referencias (APA 7)

Solo las citadas en §2 a §5, en orden alfabético. Las letras (2024a, 2025b…) se asignaron por orden alfabético del título dentro de cada autor y año, y por eso pueden no coincidir con las de los archivos de evidencias (la equivalencia está en §8).

Ámbito Jurídico. (2024, 23 de mayo). *Modifican acuerdo relacionado con las condiciones para ser beneficiarios del Fondo Emprender*. https://www.ambitojuridico.com/noticias/general/educacion-y-cultura/modifican-acuerdo-relacionado-con-las-condiciones-para-ser

Cámara de Comercio de Cali. (2025a, 6 de noviembre). *Excelencia Clínica*. Plataforma Clúster. https://www.ccc.org.co/plataformacluster/excelencia-clinica/

Cámara de Comercio de Cali. (2025b, 18 de junio). *La innovación tecnológica como motor del desarrollo regional* (Ritmo Cluster, Informe n.º 46). https://www.ccc.org.co/wp-content/uploads/2025/06/20250618_La-innovacio%CC%81n-tecnolo%CC%81gica-como-motor-del-desarrollo-regional.pdf

Cámara de Comercio de Cali. (2025c, 22 de agosto). *Panorama de innovación y transformación digital en salud* (Ritmo Cluster, Informe n.º 47). https://www.ccc.org.co/wp-content/uploads/2025/08/20250822_InformeEC.pdf

Cámara de Comercio de Cali. (2026, 10 de abril). *NIDO amplía su alcance y fortalece la innovación en el Valle del Cauca*. https://www.ccc.org.co/nido-ampla-su-alcance-y-fortalece-la-innovacin-en-el-valle-del-cauca/

Consultor Salud. (2024a, 12 de junio). *Cali declaró emergencia sanitaria por incremento de casos de dengue*. https://consultorsalud.com/cali-emergencia-sanitaria-casos-de-dengue/

Departamento Administrativo Nacional de Estadística [DANE]. (2026, 3 de julio). *Boletín técnico: Producto interno bruto departamental 2025 preliminar*. https://www.dane.gov.co/files/operaciones/PIB/bol-PIBDep-2025pr.pdf

Departamento Nacional de Planeación [DNP]. (2025). *Documento CONPES 4144: Política Nacional de Inteligencia Artificial*. https://colaboracion.dnp.gov.co/CDT/Conpes/Econ%C3%B3micos/4144.pdf

Desjardins, M. R., Eastin, M. D., Paul, R., Casas, I., & Delmelle, E. M. (2020). Space–time conditional autoregressive modeling to estimate neighborhood-level risks for dengue fever in Cali, Colombia. *The American Journal of Tropical Medicine and Hygiene, 103*(5), 2040–2053. https://doi.org/10.4269/ajtmh.20-0080

El País. (2026, 18 de mayo). Así funciona DengueIA, la herramienta que predice casos de dengue semanas antes en Cali; así fue su construcción. *El País*. https://www.elpais.com.co/cali/asi-funciona-dengueia-la-herramienta-que-predice-casos-de-dengue-semanas-antes-en-cali-1857.html

Erazo Córdoba, J. W. (2026, 5 de mayo). Cali usará inteligencia artificial para anticipar brotes de dengue: así funcionará DengueIA. *El País*. https://www.elpais.com.co/cali/cali-usara-inteligencia-artificial-para-anticipar-brotes-de-dengue-asi-funcionara-dengueia-0537.html

Gobernación del Valle del Cauca. (2024a, 19 de septiembre). *Atentos emprendedores del sector salud, NIDO abre nueva convocatoria con ValleyCare*. https://www.valledelcauca.gov.co/publicaciones/83790/atentos-emprendedores-del-sector-salud-nido-abre-nueva-convocatoria-con-valleycare/

Gobernación del Valle del Cauca. (2024b, 14 de febrero). *Gobernadora logra que MinCiencias se articule al proyecto del Distrito de Innovación e Inteligencia Artificial*. https://www.valledelcauca.gov.co/publicaciones/81170/gobernadora-logra-que-minciencias-se-articule-al-proyecto-del-distrito-de-innovacion-e-inteligencia-artificial/

Gobernación del Valle del Cauca. (2024c, 31 de mayo). *Ordenanza 655 de 2024, por medio de la cual se adopta el Plan de Desarrollo Departamental del Valle del Cauca 2024-2027 «Liderazgo que Transforma»*. https://prosperidad.valledelcauca.gov.co/storage/Clientes/Gobernacion/prosperidad/imagenes/contenidos/ORDENANZA%20655%20DEL%2031%20DE%20MAYO%20DE%202024-%20%20PLAN%20DE%20DESARROLLO.pdf

Gobernación del Valle del Cauca. (2024d). *Plan de Desarrollo del Valle del Cauca 2024-2027 «Liderazgo que transforma»* [Versión resumida]. https://www.aerosantaana.gov.co/wp-content/uploads/2025/03/Plan-de-Desarrollo-del-Valle-del-Cauca-2024-2027-Liderazgo-que-transforma.pdf

Gobernación del Valle del Cauca. (2024e). *Plan Territorial de Salud 2024-2027*. https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=73263

Gobernación del Valle del Cauca. (2026a, 25 de febrero). *Cuatro mil emprendedores de 26 municipios fueron seleccionados para acceder al Fondo ValleINN+*. https://www.valledelcauca.gov.co/publicaciones/88621/cuatro-mil-emprendedores-de-26-municipios-fueron-seleccionados/

Gobernación del Valle del Cauca. (2026b, 10 de abril). *NIDO 2026: incubación y aceleración de startups y pymes innovadoras para impulsar la economía del Valle del Cauca*. https://www.valledelcauca.gov.co/publicaciones/88971/

Infobae. (2026, 17 de marzo). *«Más de $282.000 millones para emprendedores»: SENA abre 12 convocatorias en Colombia con capital semilla*. https://www.infobae.com/colombia/2026/03/17/mas-de-282000-millones-para-emprendedores-sena-abre-12-convocatorias-en-colombia-con-capital-semilla/

Instituto Nacional de Salud. (2025). *Informe de evento: dengue, 2024* (códigos 210, 220, 580). https://www.ins.gov.co/buscador-eventos/Informesdeevento/DENGUE%20INFORME%20DE%20EVENTO%202024.pdf

Ministerio de Ciencia, Tecnología e Innovación [Minciencias]. (2026). *Convocatoria ColombIA Inteligente 2026 (Convocatoria 976)*. https://minciencias.gov.co/convocatorias/convocatoria-colombia-inteligente-2026

Ministerio de Salud y Protección Social. (2024). *Del Plan Decenal de Salud Pública a la planeación territorial para la salud*. Organización Panamericana de la Salud. https://www.paho.org/sites/default/files/4.pdsp-pts_0.pdf

Ministerio de Salud y Protección Social y Ministerio de Hacienda y Crédito Público. (2025). *Informe de análisis Plan Financiero Territorial de Salud: Distrito de Santiago de Cali, cuatrienio 2024-2027*. https://www.minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/VP/FS/pfts-cali-2024-2027-publicacion.pdf

Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2025, 11 de marzo). *Ante la academia, el Gobierno Nacional presentó el Conpes de Inteligencia Artificial*. https://www.mintic.gov.co/portal/715/w3-article-400044.html

Red Tecnoparque Colombia. (s. f.). *Red Tecnoparque Colombia*. Servicio Nacional de Aprendizaje. https://redtecnoparque.com/

The Rockefeller Foundation. (2026, 5 de mayo). *DengueAI: New model that anticipates outbreaks with 93% effectiveness and three weeks' advance notice*. https://www.rockefellerfoundation.org/news/dengueai-model-anticipates-outbreaks-93-effectiveness-three-weeks-advance-notice/

Rodríguez-Morales, A. J., López-Medina, E., Arboleda, I., Cardona-Ospina, J. A., Castellanos, J., Faccini-Martínez, Á. A., Gallagher, E., Hanley, R., López, P., Mattar, S., Pérez, C. E., Kastner, R., Reynales, H., Rosso, F., Shen, J., Villamil-Gómez, W. E., & Fuquen, M. (2024). Cost of dengue in Colombia: A systematic review. *PLOS Neglected Tropical Diseases, 18*(12), e0012718. https://doi.org/10.1371/journal.pntd.0012718

Universidad Icesi. (s. f.). *Conoce Dengue.IA*. Citradi. https://www.icesi.edu.co/citradi/dengue-cali/conoce-dengueia/

Zhao, N., Charland, K., Carabali, M., Nsoesie, E. O., Maheu-Giroux, M., Rees, E., Yuan, M., Garcia Balaguera, C., Jaramillo Ramirez, G., & Zinszer, K. (2020). Machine learning and dengue forecasting: Comparing random forests and artificial neural networks for predicting dengue burden at national and sub-national scales in Colombia. *PLOS Neglected Tropical Diseases, 14*(9), e0008056. https://doi.org/10.1371/journal.pntd.0008056

**Notas para T6 sobre las referencias:**
- «The Rockefeller Foundation» se ordena por «Rockefeller» (APA 7 ordena los autores corporativos por la primera palabra significativa), por eso va antes de Rodríguez-Morales («Roc» < «Rod»).
- Todas las referencias de la lista están citadas al menos una vez en §2 a §5. Si T6 recorta algún párrafo, debe revisar que no queden referencias sin cita ni citas sin referencia.
- Faltan en `evidencias/` las referencias de los conjuntos de datos (SIVIGILA en Datos Abiertos Cali y NASA POWER). Por eso la descripción de la idea los nombra sin cita. Si T6 quiere citarlos, debe verificar antes la URL y la fecha (ver §10).

---

## 7. Escaleta de la exposición (5 minutos)

8 diapositivas expuestas + 1 de respaldo (R) que solo se muestra si hay preguntas. Ritmo de referencia para el guion (T8): unas 130 palabras por minuto.

| Diapositiva | Título | Mensaje (1 frase) | Cifras / elementos en pantalla | Tiempo (inicio–fin) | Duración |
|---|---|---|---|---|---|
| 1 | AedesAlert Cali: validación regional | Presento AedesAlert Cali y la evalúo con los cuatro criterios de validación regional del curso. | Título de la idea, nombre, curso, UCC Cali, octubre de 2026; los 4 criterios como índice | 0:00–0:15 | 0:15 |
| 2 | La idea: un complemento abierto de DengueIA | Cali ya demostró con DengueIA que anticipar el dengue funciona; AedesAlert lleva ese enfoque a una versión abierta y replicable para el Valle. | Flujo SIVIGILA + NASA POWER → Random Forest/XGBoost vs. SARIMA → mapa semáforo por comuna. DengueIA: 93 % de efectividad reportada, hasta 3 semanas, 174 zonas de 1 km². AedesAlert: 22 comunas, datos abiertos, código libre, otros 8 municipios en riesgo muy alto | 0:15–0:55 | 0:40 |
| 3 | Criterio 1 · Caracterización económica | Transforma el sector Salud, en su segmento HealthTech, con capacidades TI. | 3.ª economía del país, ≈9,8 % del PIB (2025pr); Clúster de Excelencia Clínica: 528 empresas (2023), línea HealthTech; madurez digital 2,42/5; empleo TIC +7,2 % vs. +4,9 % promedio (2019-2023). Puntaje **5** | 0:55–1:35 | 0:40 |
| 4 | Criterio 2 · Impacto social o técnico | El problema es grande y la anticipación funciona; lo que falta es que sea abierta y replicable en el Valle. | 1.520 vs. 937 casos por 100.000 hab. (2024); emergencia sanitaria 11-jun-2024 (>20.000 casos); 9 municipios en riesgo muy alto; brotes cada 2 a 4 años; ≈USD 252 millones/año (USD de 2020); clima rezagado 2 a 5 semanas. Puntaje **4** | 1:35–2:25 | 0:50 |
| 5 | Criterio 3 · Políticas de fomento | Está alineada en los tres niveles, y el Distrito ya usa IA contra el dengue. | Nacional: CONPES 4144 de 2025 (2025-2030), PDSP 2022-2031. Departamental: «Liderazgo que Transforma» 2024-2027 (Ordenanza 655), PTS 2024-2027, Minciencias articulado a NIDO con misión de soberanía sanitaria. Distrital: dengue y ETV prioritarios, DengueIA. Puntaje **5** | 2:25–3:05 | 0:40 |
| 6 | Criterio 4 · Apoyo del ecosistema | Hay apoyos gratuitos para empezar ya; la cofinanciación dependerá de un próximo ciclo. | Ruta: 1) Tecnoparque (IA y geotecnología); 2) NIDO (220 startups 2024-2025, ValleyCare); 3) Secretaría de Salud, Icesi y Univalle + Clúster de Excelencia Clínica. Fondo Emprender: 12 convocatorias, >$282.000 millones, cerradas en abril de 2026. ColombIA Inteligente: terminada (ago-2026). Valle INN+: encaje bajo. Puntaje **4** | 3:05–3:45 | 0:40 |
| 7 | Matriz de selección (resultado principal) | AedesAlert Cali obtiene 18 de 20: fuerte en sector y políticas, con impacto y ecosistema en 4. | Tabla 1 resumida: 4 criterios con su frase corta y puntaje (5 · 4 · 5 · 4), TOTAL **18/20** destacado | 3:45–4:30 | 0:45 |
| 8 | Conclusión: riesgo y siguiente paso | La idea pasa la validación regional como complemento abierto; el reto es validar la demanda y conseguir los datos. | Riesgo principal (demanda no validada + datos por comuna); siguientes pasos: Datos Abiertos Cali / derecho de petición, Tecnoparque, una secretaría municipal en riesgo muy alto. «Gracias» | 4:30–4:50 | 0:20 |
| R | Fuentes (respaldo, no cuenta) | Muestra de dónde sale cada cifra. | Lista corta de fuentes: DANE, CCC, INS, PTS del Valle, Rodríguez-Morales et al., Fundación Rockefeller, CONPES 4144, Infobae, Minciencias | — | — |

**Suma de la escaleta:** 15 + 40 + 40 + 50 + 40 + 40 + 45 + 20 = **290 s = 4:50** (dentro del rango 4:30–5:00). Diapositivas expuestas: **8**.

---

## 8. Trazabilidad de cifras

Archivos: **T1** = `evidencias/T1-caracterizacion-economica.md` · **T2** = `evidencias/T2-impacto.md` · **T3** = `evidencias/T3-politicas.md` · **T4** = `evidencias/T4-ecosistema.md`. El código es el del hallazgo (H#, A#…) o la fila/sección de la tabla donde está la URL.

| Cifra o dato usado | Dónde se usa | Archivo | Código / fila con URL | Cita en este archivo |
|---|---|---|---|---|
| 3.ª economía del país | §3, §4.1, diap. 3 | T1 | H3 | DANE (2026) |
| ≈9,8 % del PIB nacional (2025pr; cálculo con cifras del boletín) | §3, §4.1, diap. 3 | T1 | H4 | DANE (2026) |
| 528 empresas (2023) | §3, §4.1, diap. 3 | T1 | H9 | Cámara de Comercio de Cali (2025a) |
| 4 líneas del clúster; línea «Modelos de negocio HealthTech» | §3, §4.1 | T1 | H11 | Cámara de Comercio de Cali (2025a) |
| Línea HealthTech priorizada en 2025 | §3, §4.1 | T1 | H12 | Cámara de Comercio de Cali (2025c) |
| Madurez digital 2,42/5 en 25 instituciones | §3, §4.1, diap. 3 | T1 | H13 | Cámara de Comercio de Cali (2025c) |
| Empleo TIC 7,2 % vs. 4,9 % (2019-2023) | §3, §4.1, diap. 3 | T1 | H17 | Cámara de Comercio de Cali (2025b) |
| 1.520 casos por 100.000 hab. en Cali (2024) | §3, §4.2, diap. 4 | T2 | B3 | Erazo Córdoba (2026) |
| 937 por 100.000 en Colombia (2024; INS: 937,4) | §3, §4.2, diap. 4 | T2 | A1 (y B3) | Instituto Nacional de Salud (2025) |
| Emergencia sanitaria 11-jun-2024, >20.000 casos | §3, §4.2, diap. 4 | T2 | B1 | Consultor Salud (2024a) |
| Cali + otros 8 municipios en riesgo muy alto (9 en total) y sus nombres | §2, §3, §4.2, diap. 2 y 4 | T2 | B5 | Gobernación del Valle del Cauca (2024e) |
| Brotes cada 2 a 4 años (en el Valle) | §4.2, diap. 4 | T2 | B6 | Gobernación del Valle del Cauca (2024e) |
| USD 159,6 M directos + USD 92,8 M indirectos ≈ USD 252 M/año, USD de 2020 | §4.2, diap. 4 | T2 | D1, D2 (y matiz de §2.D) | Rodríguez-Morales et al. (2024) |
| Clima rezagado 2 a 5 semanas (Cali, por barrio) | §3, §4.2, diap. 4 | T2 | F1 | Desjardins et al. (2020) |
| Random Forest supera a ARIMA (Colombia) | §4.2 | T2 | F3 | Zhao et al. (2020) |
| DengueIA: 93 % de efectividad reportada; alertas a 1, 2 y 3 semanas | §2, §3, §4.2, diap. 2 | T2 | E4 | The Rockefeller Foundation (2026) |
| DengueIA: 174 zonas de 1 km² | diap. 2 | T2 / T3 | E2 / §2.3 fila DengueIA | El País (2026) |
| DengueIA en uso desde mayo de 2026; Icesi, Univalle, Fundación Rockefeller | §2 | T2 / T3 | E1, E5 / §2.3 fila DengueIA | El País (2026); Universidad Icesi (s. f.) |
| 22 comunas de Cali | §2, diap. 2 | T2 | B10 | (dato descriptivo, sin cita en el texto) |
| CONPES 4144 de 2025, horizonte 2025-2030, ejes Datos e infraestructura y Uso y adopción de la IA, salud como sector estratégico | §3, §4.3, diap. 5 | T3 | §2.1 fila CONPES 4144 | DNP (2025); MinTIC (2025) |
| Plan Decenal de Salud Pública 2022-2031, ejes 5 y 6 (soberanía sanitaria) | §3, §4.3, diap. 5 | T3 | §2.1 fila PDSP | Ministerio de Salud y Protección Social (2024) |
| Ordenanza 655 de 2024 (31-may-2024); Plan «Liderazgo que Transforma» 2024-2027; Línea I y II y subprogramas | §3, §4.3, diap. 5 | T3 | §2.2 filas del Plan de Desarrollo | Gobernación del Valle del Cauca (2024c, 2024d) |
| PTS 2024-2027 propone IA y análisis de datos | §3, §4.3, diap. 5 | T3 | §2.2 fila PTS | Gobernación del Valle del Cauca (2024e) |
| NIDO: misión de «soberanía sanitaria» (Minciencias) | §4.3, diap. 5 | T3 | §2.2 fila NIDO | Gobernación del Valle del Cauca (2024b) |
| Cali prioriza «dengue y enfermedades transmitidas por vector» | §3, §4.3, diap. 5 | T3 | §2.3 fila Plan Financiero Territorial de Salud | Ministerio de Salud y Protección Social y Ministerio de Hacienda y Crédito Público (2025) |
| NIDO: 220 startups (2024-2025) | §3, §4.4, diap. 6 | T4 | §2.1 «Cifras verificadas» | Cámara de Comercio de Cali (2026) |
| NIDO: Comfandi cogestor desde abril de 2026; oferta 2026 de ideación a internacionalización | §4.4 | T4 | §2.1 «Qué es» / «Qué ofrece» | Cámara de Comercio de Cali (2026); Gobernación del Valle del Cauca (2026b) |
| ValleyCare (septiembre de 2024) | §3, §4.4, diap. 6 | T4 | §2.1 «Antecedente en salud» | Gobernación del Valle del Cauca (2024a) |
| Tecnoparque gratuito, permanente, sublínea de IA y geotecnología | §3, §4.4, diap. 6 | T4 | §2.2 | Red Tecnoparque Colombia (s. f.) |
| Fondo Emprender: 12 convocatorias, >$282.000 millones, cerradas en abril de 2026 | §3, §4.4, diap. 6 | T4 | §2.3 «Qué ofrece» / «Estado» | Infobae (2026) |
| Elegibilidad: dos últimos semestres u 80 % de los créditos | §4.4 | T4 | §2.3 «Requisitos» | Ámbito Jurídico (2024) |
| ColombIA Inteligente terminada en agosto de 2026 (Res. 0736 de 2026) | §4.4, diap. 6 | T4 | §2.6 «Estado» | Minciencias (2026) |
| Valle INN+: convocatoria ya adjudicada (25-feb-2026), encaje bajo | §4.4, diap. 6 | T4 | §2.4 «Estado» | Gobernación del Valle del Cauca (2026a) |
| Puntajes 5 · 4 · 5 · 4 = 18/20 | §3, §5, diap. 7 | T1 §4 · T2 §4 · T3 §5 · T4 §4 | Puntaje propuesto de cada evidencia | — |

**Equivalencia de letras de referencias** (este archivo → evidencias):

| Aquí | En evidencias |
|---|---|
| Cámara de Comercio de Cali (2025a, 2025b, 2025c) | Iguales en T1; en T4, «Excelencia Clínica» figura como (s. f.-a) |
| Cámara de Comercio de Cali (2026) | T4: (2026b) |
| DANE (2026) | T1: (2026a) |
| El País (2026) | T2: El País (2026a) |
| Gobernación del Valle del Cauca (2024a) ValleyCare | T4: (2024) |
| Gobernación del Valle del Cauca (2024b) Minciencias/NIDO | T3: (2024b) |
| Gobernación del Valle del Cauca (2024c) Ordenanza 655 | T3: (2024d) |
| Gobernación del Valle del Cauca (2024d) versión resumida | T3: (2024e) |
| Gobernación del Valle del Cauca (2024e) PTS | T2: (2024b); T3: (2024c) |
| Gobernación del Valle del Cauca (2026a) Valle INN+ seleccionados | T4: (2026a) |
| Gobernación del Valle del Cauca (2026b) NIDO 2026 | T4: (2026b) |
| Minciencias (2026) página de la convocatoria | T4: (2026b) |
| Erazo Córdoba (2026) | T2: Erazo Córdoba (2026); T3: El País (2026, 5 de mayo) |

---

## 9. Cambios frente a la v1

1. **Enfoque de la idea:** AedesAlert pasa de «la vigilancia es reactiva» a **complemento abierto y replicable de DengueIA** para los otros 8 municipios del Valle en riesgo muy alto (decisión del gate de la wave 1).
2. **Criterio 1:** PIB 9,7 % (2024) → **≈9,8 % (2025pr)**; «528 empresas» → **528 empresas (2023)**; se quita «cerca de 1.200 empresas de software» y se usa **empleo TIC 7,2 % vs. 4,9 %**; se añade la madurez digital de **2,42/5** y la priorización de la línea HealthTech en 2025.
3. **Criterio 2 (5 → 4):** se elimina «la vigilancia es reactiva» y «dos fuentes que hoy se analizan por separado»; se añaden la incidencia **1.520 vs. 937**, DengueIA y el sustento técnico con DOI (Desjardins, Zhao); «brotes cada 2 a 4 años» se atribuye al Valle, no a Cali; el costo se presenta en **dólares de 2020**; «la focalización funciona» y los 50 barrios salen de la matriz (eran un indicio sin evaluación causal).
4. **Criterio 3 (4 → 5):** «seguridad sanitaria» → **soberanía sanitaria**; «eje Valle Competitivo e Innovador» → **Línea I y subprogramas con nombre propio**; se añaden el PDSP 2022-2031, el PTS (IA y análisis de datos), la prioridad del dengue en la planeación en salud de Cali y DengueIA.
5. **Criterio 4 (se mantiene en 4, con otra base):** NIDO «desde 2026 acompaña la ideación» → **oferta 2026 desde la ideación hasta la internacionalización**, con el antecedente ValleyCare; Fondo Emprender con **convocatorias cerradas en abril de 2026** y elegibilidad precisa; Minciencias pasa a opción **no disponible hoy**; Valle INN+ con la fuente de la edición que incluye a Cali; se suman como aliados de validación la Secretaría de Salud, Icesi y Univalle (DengueIA).
6. **Conclusión:** el riesgo principal pasa de «solo datos» a **demanda no validada en los otros municipios + datos por comuna**; se añade un siguiente paso concreto.
7. **Referencias:** se quitan las «s. f.» que sí tenían fecha (Cámara de Comercio de Cali, Bancolombia, El País), se quitan las que ya no se citan (El País s. f., DANE 2025, Gobernación 2025 de Valle INN+ de 5 municipios, Consultor Salud sin letra) y se agregan las nuevas fuentes con URL o DOI.
8. **Escaleta:** de 7 diapositivas en 4:45 a 8 diapositivas en 4:50; se separan la idea con DengueIA (diap. 2) y la conclusión (diap. 8) de la matriz (diap. 7), que queda como resultado principal.

---

## 10. Datos que faltan (no se afirman)

- **Referencias de los conjuntos de datos** (SIVIGILA en Datos Abiertos Cali y NASA POWER): no están en `evidencias/`. La descripción de la idea los nombra sin cita.
- **Casos de dengue de Cali en 2026:** no hay cifra oficial accesible (T2, «No encontrado»); solo se sabe que Cali y el Valle tuvieron aumentos de notificación superiores al 30 % a la semana 20 (T2, A6). No se usa en la matriz.
- **Meta literal del Plan de Desarrollo de Cali sobre dengue:** cali.gov.co devolvió 403 (T3, §4). El criterio 3 se sostiene sin ella; si el docente la exige, el 4 de la v1 también es defendible (T3, §5).
- **Requisitos de entrada de NIDO para una idea sin empresa constituida:** no publicados (T4, §2.1). Es un supuesto que hay que confirmar con NIDO.
- **Apertura de DengueIA:** ninguna fuente dice que sus datos, código o mapa sean públicos (T2, E6). Por eso se dice «no se conoce como abierta», no «es cerrada».
