# T2. Insumos del modelo de negocio (Business Model Canvas) — AedesAlert Cali

**Fecha de consulta de todas las fuentes web:** 2 de octubre de 2026 (salvo que se indique otra).
**Idea:** modelo de IA que predice cada semana el riesgo de dengue por comuna con datos abiertos (casos SIVIGILA + clima NASA POWER; Random Forest/XGBoost frente a SARIMA) y lo muestra en un mapa semáforo, con código libre. Se presenta como **complemento abierto y replicable de DengueIA** para los otros 8 municipios del Valle en riesgo muy alto. Autor: Juan Diego Nieto (UCC Cali), trabaja solo; es su proyecto de grado.
**Reutilizado sin repetir:** ecosistema de apoyo (NIDO, Tecnoparque, Fondo Emprender, Valle INN+, Minciencias, Clúster de Excelencia Clínica, UCC) en `milestones/validacion-regional-aedesalert/evidencias/T4-ecosistema.md` (abajo, "PREV-T4"); clasificación de riesgo de los municipios en `.../evidencias/T2-impacto.md` (fila B5, "PREV-T2").

**Convención:** cada dato lleva su fuente con URL. Lo que no tiene fuente se marca **[supuesto]**; las conclusiones propias se marcan **[inferencia]**. Las fuentes se consultaron con WebFetch, que devuelve un resumen del contenido: las citas textuales vienen de ese resumen.

---

## 0. Resumen para el Canvas (lo más útil)

1. **Quién decide y paga** es la **secretaría de salud municipal** (y la Secretaría Departamental de Salud para la vigilancia en el departamento), con recursos públicos de salud pública. El dinero del **Plan de Intervenciones Colectivas (PIC)** es grande (Palmira: $2.300 millones para 2026; Tuluá: $1.160 millones para el 2.º semestre de 2026), pero **se contrata casi siempre con la ESE (hospital público) del municipio** mediante convenio interadministrativo, así que AedesAlert **no** entraría como ejecutor del PIC. [inferencia, ver §4]
2. Las secretarías sí contratan **directamente** a profesionales para analizar datos de vectores y apoyar la vigilancia (p. ej., Cali, 2023: $12,9 y $16,7 millones por contrato) y a **universidades** para fortalecer la vigilancia epidemiológica (Cali–Fundación Univalle, 2020: $400 millones). Ese es el patrón de compra que encaja con "código libre + servicios". [§4]
3. Para financiar el desarrollo hay un **precedente directo en el Valle**: el **Programa AEDES** contra dengue, chikunguña y zika, financiado con el **Fondo de CTeI del SGR** ($14.770 millones en total; $2.010 millones para el Valle; incluyó Cali y Buga). Hoy la asignación CTeI funciona por **convocatorias de Minciencias** para **alianzas del SNCTI** (una IES con experiencia como proponente), no para un estudiante solo. [§4, §8]
4. El costo técnico del prototipo puede ser **$0**: Streamlit Community Cloud, GitHub Free y NASA POWER son gratuitos; el costo real es **el tiempo de una persona** (referencia: $2,2 millones/mes ingeniero de sistemas en Cali según Indeed; salario mínimo 2026: $1.750.905). [§9]
5. **Diferenciación con DengueIA:** DengueIA es un sistema institucional de Cali (cuadrículas de 1 km², financiado por la Fundación Rockefeller, modelo predictivo + prescriptivo); la fuente no menciona código abierto ni otros municipios. AedesAlert: **abierto, por comuna, replicable y de bajo costo para los otros 8 municipios**. Hay un precedente internacional de financiador que exige **software abierto** para herramientas clima–enfermedad (Wellcome, 2023, incluido Mosqlimate/InfoDengue en Brasil). [§10]

---

## 1. Segmentos de clientes (Bloque 7)

### 1.1 Mapa de segmentos

| Segmento | Por qué le sirve AedesAlert | Rol que le asigna la norma (dengue) | Quién paga / con qué | Fuente |
|---|---|---|---|---|
| **Secretarías de salud municipales de los 8 municipios en riesgo muy alto** (Buga, Candelaria, Cartago, Florida, Jamundí, Palmira, Tuluá, Yumbo) — **segmento principal (cliente que paga)** | Necesitan focalizar control vectorial y planear acciones; no se conoce un sistema predictivo equivalente al de Cali en esos municipios (PREV-T2: "no se conoce", no "no existe") | Las secretarías municipales participan en investigaciones epidemiológicas de dengue grave, en los COVE y en unidades de análisis de muertes (INS, 2024) | Presupuesto de salud pública (SGP: PIC + gestión de la salud pública) y recursos propios (Res. 518 de 2015, art. 20) | PTS Valle 2024-2027, p. 22 (PREV-T2, B5): https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=73263 · INS (2024): https://www.ins.gov.co/buscador-eventos/Lineamientos/Pro_Dengue.pdf |
| **Gobernación del Valle – Secretaría Departamental de Salud** (incluye el Laboratorio de Salud Pública) — **cliente y aliado** | Vista departamental de los 9 municipios en riesgo muy alto en un solo mapa | Las secretarías departamentales deben "realizar monitoreo de comportamientos inusuales", "garantizar la vigilancia virológica y entomológica" y analizar indicadores periódicamente (INS, 2024) | Proyectos departamentales de dengue: p. ej. el proyecto "Contribución al mejoramiento de las condiciones y situaciones endemoepidémicas de enfermedades transmisibles – dengue en el Valle del Cauca" contrató servicios profesionales por contratación directa ($40.500.000, ene-2022, contrato CO1.PCCNTR.3248437) | SECOP II (datos.gov.co): https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=dengue&departamento=Valle%20del%20Cauca&$limit=40 |
| **Secretaría de Salud Pública de Cali** — **usuario de referencia, no cliente principal** | Ya tiene DengueIA; AedesAlert serviría como referencia abierta de comparación por comuna | Igual que municipales (Cali es distrito) | — | dengueia-fase1.md; Icesi (2026) |
| **EPS (EAPB)** — **segmento secundario (hipótesis)** | Anticipar demanda de servicios y de muestras en su población afiliada por zona | Deben "analizar y usar la información epidemiológica para la toma de decisiones" y garantizar la toma de muestra en casos probables (INS, 2024) | Recursos propios de la EPS [supuesto: **no se encontró evidencia** de que EPS compren tableros predictivos de dengue] | INS (2024) |
| **IPS (clínicas, hospitales; UPGD)** — **segmento secundario (hipótesis)** | Preparar urgencias, camas e insumos ante picos | Notifican casos, toman muestras, capacitan al talento humano y analizan muertes por dengue (INS, 2024) | Recursos propios [supuesto: sin evidencia de compra] | INS (2024) |
| **Laboratorios clínicos y aseguradoras** — **segmento exploratorio** | Planear reactivos (laboratorios) o riesgo (aseguradoras) | — | [supuesto: no se encontró evidencia de demanda; mantener como hipótesis a validar con entrevistas] | — |
| **Academia y comunidad técnica** (universidades, semilleros, desarrolladores) — **usuarios del código, no pagan** | Reutilizar el código y los datos para otros municipios o enfermedades | — | — | [inferencia] |

### 1.2 Notas para el Canvas
- Un bien público con código libre tiene **usuarios** (cualquiera usa el mapa) y **clientes** (quien paga implementación, soporte o capacitación). Conviene separarlos en el lienzo. [inferencia]
- Las 8 secretarías municipales y la departamental son el segmento con **evidencia de compra** (§4). IPS, EPS, laboratorios y aseguradoras quedan como **hipótesis**: el protocolo del INS les asigna funciones de análisis, pero no se encontró que compren este tipo de herramienta.

---

## 2. Canales (Bloque 6)

| Canal | Evidencia | Fuente |
|---|---|---|
| **SECOP II** (contratación pública electrónica) | "Plataforma transaccional para gestionar en línea todos los Procesos de Contratación", con cuentas para entidades y proveedores. Todas las contrataciones de §4 están publicadas allí. | Colombia Compra Eficiente (s. f.-a): https://www.colombiacompra.gov.co/secop |
| **Contratación directa** (servicios profesionales; actividades científicas y tecnológicas; contratos interadministrativos) | Ley 1150 de 2007, art. 2, num. 4, literales c), e) y h) (§4.2) | Ley 1150 de 2007: http://www.secretariasenado.gov.co/senado/basedoc/ley_1150_2007.html |
| **Universidad como puente** (proyecto de grado → convenio UCC–secretaría o alianza SNCTI) | Precedentes: Cali contrató a la Fundación Universidad del Valle ($400 M, 2020) para la vigilancia epidemiológica; el Programa AEDES (SGR) tuvo una universidad aliada (UIS) | SECOP II (§4.3); Gobernación del Valle del Cauca (s. f.) |
| **Comités de vigilancia (COVE) departamentales** | Las secretarías municipales deben participar en los COVE departamentales (INS, 2024): es el espacio donde coinciden los 9 municipios y la Gobernación | INS (2024) |
| **Ecosistema** (NIDO, Tecnoparque, Clúster de Excelencia Clínica / Qualinn) | Ver PREV-T4 (no se repite) | PREV-T4 |
| **Repositorio público (GitHub) + mapa web público (Streamlit)** | Canal de entrega del bien público; ambos gratuitos (§9) | GitHub Docs (s. f.); Streamlit (s. f.-a) |
| **Compra Pública para la Innovación (CPI)** | Colombia Compra Eficiente tiene instrumentos para que "las Entidades Estatales logren satisfacer sus necesidades por medio de soluciones innovadoras". [a matizar: no se verificó su uso por secretarías de salud del Valle] | Colombia Compra Eficiente (s. f.-b): https://www.colombiacompra.gov.co/compra-publica-para-la-innovacion/compra-publica-innovadora-introduccion |

---

## 3. Relación con clientes (Bloque 5)

| Tipo de relación | Base | Fuente |
|---|---|---|
| **Co-creación con la secretaría** (validación del mapa con los técnicos de ETV/salud ambiental) | DengueIA trabajó así: la Secretaría de Salud Pública de Cali aportó datos y validación | Icesi (2026); dengueia-fase1.md |
| **Acompañamiento semanal** (boletín o reunión corta con el reporte de riesgo) | El dato se actualiza por semana epidemiológica, como la notificación de SIVIGILA [supuesto sobre la periodicidad de uso] | — |
| **Capacitación y transferencia** para que la secretaría opere el modelo sin depender del autor | Coherente con código libre; las IPS tienen la obligación de capacitar a su talento humano según protocolos (INS, 2024) | INS (2024) |
| **Comunidad abierta** (issues, documentación, réplica en otros municipios) | [inferencia] | — |
| **Contrato por vigencia** | Las contrataciones de salud pública se hacen por vigencia anual o semestral (p. ej., PIC 2025, PIC 2.º semestre 2026; §4.1); la contratación del PIC se hace "a más tardar el 31 de marzo de cada vigencia" (Res. 295 de 2023) → la relación comercial se renueva cada año [inferencia] | MinSalud (2023); SECOP II |

---

## 4. Fuentes de ingresos (Bloque 9): cómo compra el sector público

### 4.1 El Plan de Intervenciones Colectivas (PIC) y la línea de ETV

- **Qué es:** el PIC es "un plan complementario al Plan Obligatorio de Salud" "dirigido a impactar positivamente los determinantes sociales" (Res. 518 de 2015, art. 8). Lo formulan y ejecutan los departamentos, distritos y municipios según su análisis de situación de salud (arts. 12-13). Su anexo técnico incluye **"Prevención y Control de Vectores"** (control químico y biológico). Fuente: MinSalud (2015), https://www.minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/DE/DIJ/resolucion-0518-de-2015.pdf
- **Cómo se financia:** con recursos de la **Subcuenta de Salud Pública Colectiva del Sistema General de Participaciones (SGP)**, que se reparten entre el PIC y las **acciones de gestión de la salud pública** (Res. 518 de 2015, art. 20). La **vigilancia en salud pública** es uno de los procesos de la gestión de la salud pública (art. 5). [a matizar: el resumen del fetch da un reparto "30-70 %" que no se pudo confirmar textualmente; no se usa la cifra]
- **Con quién se contrata (Res. 295 de 2023, que modifica la 518):** en orden, (1) "las Empresas Sociales del Estado e IPS indígenas ubicadas en el territorio siempre y cuando tengan la capacidad técnica y operativa"; (2) ESE de municipios vecinos; (3) "universidades, organizaciones no gubernamentales (ONG), instituciones prestadoras de servicios de salud de naturaleza privada y otras entidades privadas". El ejecutor no podrá subcontratar las acciones PIC, "sin embargo, podrá contratar las actividades de apoyo que permitan la ejecución". Plazo: la contratación del PIC se realiza "a más tardar el 31 de marzo de cada vigencia" (arts. 14 y 16 modificados). Fuentes: MinSalud (2023), https://www.minsalud.gov.co/Normatividad_Nuevo/Resoluci%C3%B3n%20No.%20295%20de%202023.pdf · resumen secundario: ConsultorSalud (2023), https://consultorsalud.com/resolucion-295-2023-intervenciones-colectivas/
- **Evidencia en SECOP II (municipios objetivo):**

| Municipio | Objeto (resumido) | Valor (COP) | Contratista | Modalidad | Fecha | ID contrato |
|---|---|---|---|---|---|---|
| Palmira | Acciones del PIC, vigencia 2026 | 2.300.000.000 | Hospital Raúl Orejuela Bueno (ESE) | Contratación directa (con ofertas) | 07-nov-2025 | CO1.PCCNTR.8562123 |
| Palmira | Acciones del PIC, vigencia 2025 | 2.636.632.438 | Hospital Raúl Orejuela Bueno | Contratación directa (con ofertas) | 28-mar-2025 | CO1.PCCNTR.7714305 |
| Tuluá | Convenio interadministrativo PIC, 2.º semestre 2026 | 1.160.000.000 | ESE Hospital Rubén Cruz Vélez | Contratación directa | 10-jul-2026 | CO1.PCCNTR.9644184 |
| Tuluá | Convenio interadministrativo PIC, vigencia 2025 | 2.948.999.888 | ESE Hospital Rubén Cruz Vélez | Contratación directa | 28-mar-2025 | CO1.PCCNTR.7715530 |

Fuentes: SECOP II – Contratos electrónicos (datos.gov.co): https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=intervenciones%20colectivas&ciudad=Palmira&$order=fecha_de_firma%20DESC&$limit=15 · https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=intervenciones%20colectivas&ciudad=Tulu%C3%A1&$order=fecha_de_firma%20DESC&$limit=15

**Lectura [inferencia]:** el PIC es una bolsa grande y anual, pero va a la ESE local por convenio interadministrativo; un emprendimiento o un estudiante no es ejecutor natural del PIC. La puerta realista es la **gestión de la salud pública / vigilancia** (contratos de apoyo profesional o con universidades), o ser **proveedor de apoyo** de la ESE, si la secretaría lo pide.

### 4.2 Modalidades de contratación pública aplicables

| Modalidad | Qué dice la norma | Encaje con AedesAlert | Fuente |
|---|---|---|---|
| **Contrato interadministrativo** (Ley 1150/2007, art. 2, num. 4, lit. c) | Contratación directa "siempre que las obligaciones derivadas del mismo tengan relación directa con el objeto de la entidad ejecutora"; la Ley 1474 de 2011 excluye ciertos contratos (obra, suministro, etc.) cuando el ejecutor es, entre otros, una IES pública | Aplica entre entidades públicas (secretaría–ESE, secretaría–universidad pública). **La UCC no es pública** [a matizar: dato de conocimiento general, no verificado en esta tarea], así que no usaría esta vía | Ley 1150 de 2007 |
| **Actividades científicas y tecnológicas** (lit. e) | "Los contratos para el desarrollo de actividades científicas y tecnológicas" se celebran por contratación directa | Vía natural para un modelo predictivo desarrollado con una universidad o grupo de investigación [inferencia] | Ley 1150 de 2007 |
| **Servicios profesionales y de apoyo a la gestión** (lit. h) | Contratación directa "para la prestación de servicios profesionales y de apoyo a la gestión" | Vía para que el autor, como persona natural, preste el servicio de implementación, análisis y capacitación | Ley 1150 de 2007 |
| **Contratos con ESAL de reconocida idoneidad / convenios de asociación** (Decreto 092 de 2017) | Regula la contratación con entidades sin ánimo de lucro para programas de interés público alineados con los planes de desarrollo, sin contraprestación directa, con proceso competitivo si hay varias ESAL idóneas | Posible vía para una ESAL o universidad privada sin ánimo de lucro [a matizar: requisitos detallados no verificados en fuente primaria] | Acosta Suárez y Guarnizo Rojas (2020) |
| **Mínima cuantía** | Usada por municipios del Valle para compras pequeñas de campañas de dengue (Roldanillo, 2024: $4.980.000 en material impreso) | Para licencias o servicios de bajo valor [inferencia] | SECOP II (consulta "dengue", Valle) |

### 4.3 Evidencia de cómo las secretarías compran servicios de dengue, vigilancia y datos (SECOP II)

| Entidad | Objeto (resumido) | Valor (COP) | Modalidad | Fecha | ID contrato |
|---|---|---|---|---|---|
| Secretaría de Salud de Cali | Servicios profesionales: "interpretar la información de las actividades de monitoreo y control de *Aedes aegypti*" | 12.864.000 | Contratación directa | 18-oct-2023 | CO1.PCCNTR.5468788 |
| Secretaría de Salud de Cali | Servicios especializados: "análisis integrado de las intervenciones operativas del control de vectores" y apoyo a la vigilancia epidemiológica | 16.725.000 | Contratación directa | 17-oct-2023 | CO1.PCCNTR.5460200 |
| Secretaría de Salud de Cali | La Fundación Universidad del Valle "a diseñar una estrategia integral que fortalezca el sistema de vigilancia epidemiológica" (COVID-19) | 400.000.000 | Contratación directa | 30-jul-2020 | CO1.PCCNTR.1736909 |
| Gobernación del Valle – Secretaría de Salud | Servicios profesionales en el proyecto "Contribución al mejoramiento de las condiciones y situaciones endemoepidémicas de enfermedades transmisibles – dengue en el Valle del Cauca" | 40.500.000 | Contratación directa | 17-ene-2022 | CO1.PCCNTR.3248437 |
| DAGMA (Cali) | Actividades silviculturales en comunas "para disminuir los factores de riesgo del dengue" | 987.846.550 | Contratación directa | 04-oct-2023 | CO1.PCCNTR.5424422 |

Fuentes: https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=dengue&departamento=Valle%20del%20Cauca&$limit=40 · https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=universidad%20vigilancia%20salud%20publica&departamento=Valle%20del%20Cauca&$order=fecha_de_firma%20DESC&$limit=20
Nota: la búsqueda "software salud publica epidemiologica" en SECOP II no devolvió contratos; **no se encontró** un contrato de compra de software predictivo de dengue por una secretaría del Valle.

### 4.4 Modelos de ingreso propuestos (para un bien público)

| Modelo | Quién paga | Evidencia / referencia | Estado |
|---|---|---|---|
| **Código abierto + servicios** (implementación por municipio, capacitación, soporte por vigencia) | Secretarías municipales y departamental | Contratación directa de servicios profesionales y de apoyo (lit. h) ya usada para análisis de vectores; referencia de valor por contrato: $12,9-16,7 M (Cali, 2023) | **Principal**. Precio por municipio: **[supuesto]**, a validar |
| **Convenio universidad–entidad** (UCC o grupo de investigación como ejecutor) | Secretaría o Gobernación | Cali–Fundación Univalle ($400 M, 2020); lit. e (actividades científicas y tecnológicas) | Complementario |
| **Financiación por proyectos** (SGR-CTeI, cooperación internacional) | Fondos públicos o internacionales | Programa AEDES (SGR); Wellcome (software abierto); DengueIA (Rockefeller) — ver §8 | Para desarrollo y escalamiento, no para operación recurrente |
| **Suscripción al tablero para IPS/EPS** (funciones extra: alertas por sede, informes) | IPS, EPS | Sin evidencia de compra encontrada | **Hipótesis** a validar |
| **Capital semilla** (Fondo Emprender) | SENA | Requisitos y estado en PREV-T4 (convocatorias 2026 cerradas) | Próximo ciclo |

---

## 5. Recursos clave (Bloque 3)

| Recurso | Tipo | Disponibilidad / costo | Fuente |
|---|---|---|---|
| Casos de dengue (SIVIGILA, INS) | Datos | Público [supuesto: el portal del INS publica microdatos por municipio; **el detalle por comuna requiere datos de la secretaría** — riesgo a confirmar] | — |
| Clima diario (NASA POWER) | Datos | "Access POWER's free, low-latency, high-accuracy, community-specific datasets" | NASA (s. f.): https://power.larc.nasa.gov/ |
| Modelos (Random Forest/XGBoost, SARIMA) y código | Intelectual | Código libre en GitHub; repos públicos ilimitados en GitHub Free | GitHub Docs (s. f.) |
| Despliegue del mapa | Tecnológico | Streamlit Community Cloud: "Totally free"; solo apps públicas; hasta 2,7 GB de memoria; las apps sin tráfico "go to sleep" a las 12 horas | Streamlit (s. f.-a, s. f.-b) |
| Créditos de nube (opcional) | Tecnológico | Azure for Students: "$100 credit ... within 12 months", sin tarjeta de crédito, con correo institucional | Microsoft (s. f.) |
| El autor (ingeniería de datos, ML, despliegue) | Humano | 1 persona; tiempo del proyecto de grado | — |
| Acompañamiento académico (director de proyecto UCC) y técnico (Tecnoparque) | Humano / alianza | PREV-T4 | PREV-T4 |
| Relación con técnicos de ETV de cada secretaría | Relacional | Indispensable para datos por comuna y validación [inferencia] | — |

---

## 6. Actividades clave (Bloque 2)

1. **Ingesta y limpieza semanal** de casos (SIVIGILA/secretaría) y clima (NASA POWER), agregados por comuna y semana epidemiológica.
2. **Entrenamiento y comparación de modelos** (Random Forest/XGBoost frente a SARIMA), con clima rezagado (la evidencia de 2 a 5 semanas está en PREV-T2, Desjardins et al., 2020).
3. **Publicación del mapa semáforo** y del reporte semanal.
4. **Validación con la secretaría** (como hizo DengueIA con la Secretaría de Cali; Icesi, 2026).
5. **Réplica** a otro municipio (parametrizar comunas/corregimientos).
6. **Documentación y capacitación** para que la entidad lo opere.
7. **Gestión comercial pública:** registro como proveedor en SECOP II, propuestas de servicios por vigencia y presentación en el COVE departamental.
8. **Gobernanza de datos** (anonimización, agregación por comuna; el marco de Habeas Data está en T1).

(Actividades derivadas de la idea; no requieren fuente salvo las indicadas.)

---

## 7. Socios clave (Bloque 1)

| Socio | Qué aporta | Fuente |
|---|---|---|
| Secretarías de salud (municipales y departamental) | Datos por comuna, validación, contratación | INS (2024); SECOP II |
| Laboratorio de Salud Pública Departamental | Vigilancia virológica y entomológica (función de la secretaría departamental) | INS (2024) |
| UCC (director de proyecto, grupo de investigación) | Respaldo académico; ejecutor en alianzas tipo SGR o Minciencias | PREV-T4 §2.7 |
| SENA–Tecnoparque, NIDO, Clúster de Excelencia Clínica | Prototipo, incubación, conexión con IPS/EPS | PREV-T4 |
| NASA POWER, INS (proveedores de datos abiertos) | Datos | NASA (s. f.) |
| GitHub, Streamlit (infraestructura gratuita) | Alojamiento de código y mapa | GitHub Docs (s. f.); Streamlit (s. f.-a) |
| ESE municipales (ejecutoras del PIC) | Ejecutan las acciones colectivas de control vectorial que el mapa ayudaría a focalizar | SECOP II (§4.1) |
| Equipo de DengueIA (Icesi, Univalle) | Posible intercambio metodológico y comparación [inferencia: no hay contacto ni acuerdo] | Icesi (2026) |
| Financiadores (Minciencias/SGR, Fondo Emprender, cooperación internacional) | Recursos para desarrollo y escalamiento | §8 |

---

## 8. Fuentes de financiación (insumo para Ingresos y Socios)

| Fuente | Qué es / cómo funciona | Estado a oct-2026 | Fuente |
|---|---|---|---|
| **SGR – Asignación para la CTeI** | La Constitución (Acto Legislativo 05 de 2019) destina el **10 %** de las regalías a CTeI "a través de convocatorias públicas, abiertas, y competitivas". Plan de convocatorias 2025-2026: **$2.792.875.424.526** (general: $2.042.892.994.235; ambiental: $749.982.430.291). Las convocatorias se dirigen a "alianzas entre entidades del SNCTI"; en la convocatoria 48, por ejemplo, el proponente debía ser un actor reconocido por Minciencias o una IES con experiencia en mínimo dos proyectos de CTeI (los requisitos varían por convocatoria). | Hay plan vigente; **no se verificó una convocatoria abierta en salud** para el Valle (la convocatoria 44 forma talento en maestría/doctorado con el reto de seguridad sanitaria) | Minciencias (2025): https://minciencias.gov.co/sites/default/files/upload/paginas/plan_de_convocatorias_actei_2025-2026_0.pdf · Minciencias (s. f.): https://minciencias.gov.co/sites/default/files/upload/convocatoria/terminos_de_referencia_convocatoria_48.pdf |
| **Precedente SGR en dengue: Programa AEDES** | Investigación aplicada para un modelo de intervención contra dengue, chikunguña y zika en Valle, Santander y Casanare, financiada por el "Fondo de Ciencia, Tecnología e Innovación del Sistema General de Regalías": CTeI $10.804.759.883 + cofinanciación $3.965.179.780 = **$14.769.939.663**; **$2.010.086.631** del Fondo CTeI para el Valle; municipios incluyen **Cali y Buga**; aprobado en agosto de 2013, inició el 15-ene-2014 (57 meses); ejecutor Santander con la UIS como aliada | Histórico (precedente) | Gobernación del Valle del Cauca (s. f.): https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=26030 |
| **Fondo Emprender, NIDO, Tecnoparque, Valle INN+, Minciencias ColombIA Inteligente, UCC** | Ver PREV-T4 (no se repite) | Fondo Emprender 2026 cerrado; NIDO y Tecnoparque apalancan sin dinero; ColombIA Inteligente terminada | PREV-T4 |
| **Cooperación internacional – Fundación Rockefeller** | Financiador principal de la fase 1 de DengueIA (monto no publicado) | Precedente en Cali | Icesi (2026): https://www.icesi.edu.co/dengue-ia-cali-cierra-su-primera-fase/ |
| **Cooperación internacional – Wellcome** | 3-feb-2023: **£22,7 millones** para **24 equipos en 12 países** que desarrollan herramientas digitales para enfermedades infecciosas sensibles al clima; "The software will be open source"; incluyó **Mosqlimate** (Brasil, mejora del sistema de alerta InfoDengue con datos climáticos) | No se verificó una ronda abierta en 2026 | Wellcome (2023): https://wellcome.org/insights/articles/new-digital-tools-use-climate-data-better-predict-and-prepare-infectious-diseases-outbreaks |

---

## 9. Estructura de costos (Bloque 8)

### 9.1 Tabla de costos de referencia (COP)

TRM usada para convertir dólares: **$3.312,84 por USD** (TRM del 1-oct-2026; Infobae, 2026).

| # | Concepto | Valor de referencia (COP) | Periodicidad | Fuente o marca |
|---|---|---|---|---|
| 1 | Datos climáticos NASA POWER | $0 | — | NASA (s. f.): "free" |
| 2 | Datos de casos SIVIGILA / secretaría | $0 | — | **[supuesto]** (datos públicos o entregados por convenio) |
| 3 | Repositorio de código (GitHub Free: repos ilimitados, 2.000 min/mes de Actions) | $0 | Mensual | GitHub Docs (s. f.) |
| 4 | Mapa web (Streamlit Community Cloud, app pública) | $0 | Mensual | Streamlit (s. f.-a) |
| 5 | Crédito de nube opcional (Azure for Students, USD 100) | $0 de costo; equivale a ≈ $331.284 en crédito (USD 100 × 3.312,84) | 12 meses | Microsoft (s. f.); Infobae (2026) |
| 6 | Dominio .com.co (registro / renovación, IVA incluido) | $114.990 / $149.990 | Anual | MI.COM.CO (2026) |
| 7 | Dominio .co (registro / renovación, IVA incluido) | $149.990 / $229.990 | Anual | MI.COM.CO (2026) |
| 8 | Salario mínimo mensual 2026 (piso legal) | $1.750.905 | Mensual | Decreto 159 de 2026 (transitorio, por orden judicial, hasta la sentencia de nulidad) |
| 9 | Ingeniero/a en sistemas en **Cali** (promedio) | $2.200.927 | Mensual | Indeed (2026a): 7 salarios, act. 14-abr-2026 — **muestra pequeña** |
| 10 | Ingeniero/a en sistemas en **Colombia** (promedio) | $2.583.055 | Mensual | Indeed (2026b): 132 salarios, act. 17-sep-2026 |
| 11 | Científico/a de datos en **Colombia** (promedio, todas las experiencias) | $6.909.154 | Mensual | Indeed (2026c): 24 salarios, act. 25-sep-2026 — no es junior ni Cali |
| 12 | Referencia de contrato público por servicios de análisis de vectores (Cali) | $12.864.000 a $16.725.000 por contrato | Por contrato (plazo no verificado) | SECOP II (§4.3) |
| 13 | Carga prestacional si se contrata por nómina (salud, pensión, primas, etc.) | **[supuesto]**: no calculada; se recomienda modelar al autor como contratista por prestación de servicios | — | — |
| 14 | Equipo de cómputo del autor | $0 adicional | — | **[supuesto]**: ya lo tiene |
| 15 | Desplazamientos a municipios (capacitación, validación) | **[supuesto]**: sin valor de referencia | Por visita | — |
| 16 | Registro como proveedor en SECOP II | $0 | — | **[supuesto]**: la página oficial no indica costo |

### 9.2 Escenarios ilustrativos [supuesto: cálculos propios con las cifras de la tabla]
- **Fase prototipo (proyecto de grado):** costo monetario ≈ **$0-$150.000/año** (solo el dominio .com.co si se quiere un nombre propio); el costo real es el tiempo del autor.
- **Fase piloto en 1 municipio (6 meses, 1 persona a tiempo completo):** 6 × $2.200.927 ≈ **$13,2 millones** (referencia Indeed Cali, sin carga prestacional) + dominio + desplazamientos [supuesto].
- **Estructura:** dominada por **costos fijos de personal**; infraestructura casi nula mientras el mapa sea público. Si se requiere un tablero privado para IPS/EPS, Streamlit Community Cloud no sirve como está ("public apps only", con listas de acceso por app) y aparecería un costo de nube **[supuesto]**.

---

## 10. Diferenciación frente a DengueIA (insumo para la Propuesta de valor)

| Aspecto | DengueIA (fase 1) | AedesAlert Cali | Fuente |
|---|---|---|---|
| Alcance territorial | Cali: 174 zonas de 1 km², ~2,2 millones de habitantes; fase 2 busca "escalar el sistema a más territorios de Cali" | Los otros 8 municipios del Valle en riesgo muy alto (+ Cali como referencia) | Icesi (2026); PREV-T2 B5 |
| Unidad de análisis | Celdas de 1 km² | Comuna (unidad administrativa) | Icesi (2026) |
| Componentes | Modelo predictivo ("93 % de efectividad"), prescriptivo (84 % de pertinencia, 87 % de viabilidad operativa) y tablero | Solo predictivo + mapa semáforo (alcance de proyecto de grado) | Icesi (2026) |
| Apertura | El artículo **no menciona** código ni datos abiertos | Código libre y solo datos abiertos | Icesi (2026) |
| Financiación | Fundación Rockefeller (principal) + alianza institucional (Icesi, Univalle, Secretarías, DATIC, DAGMA, Cubo Social) | Costo de infraestructura ≈ $0; proyecto individual | Icesi (2026); §9 |
| Modelo de sostenibilidad | Fase 2: apropiación institucional; no menciona comercialización | Servicios de implementación/capacitación por contrato con secretarías | Icesi (2026); §4.4 |

**Mensaje sugerido [inferencia]:** "DengueIA probó en Cali que anticipar el dengue funciona; AedesAlert lo vuelve abierto, barato y replicable para los municipios que no tienen ni la financiación internacional ni la alianza de Cali." No afirmar que AedesAlert es más preciso que DengueIA (no hay comparación).

---

## 11. Supuestos y vacíos

1. Precio por municipio de los servicios: **no hay referencia directa**; se propone usar como ancla los contratos de servicios profesionales de análisis de vectores (§4.3).
2. Demanda de IPS, EPS, laboratorios y aseguradoras: **hipótesis sin evidencia de compra**.
3. Disponibilidad de casos por **comuna**: no verificada; probablemente requiere convenio de datos con cada secretaría.
4. No se encontró en SECOP II un contrato de software predictivo de dengue en el Valle.
5. El reparto porcentual PIC / gestión de la salud pública (art. 20, Res. 518) no se pudo confirmar textualmente.
6. La naturaleza privada de la UCC y los requisitos detallados del Decreto 092 de 2017 se toman de conocimiento general y de una fuente secundaria académica.
7. Salario de Cali con muestra pequeña (7 salarios); se reporta junto al promedio nacional.
8. Decreto 159 de 2026 es transitorio: el valor del salario mínimo puede cambiar si el Consejo de Estado falla la nulidad.

---

## 12. Referencias (APA 7)

Acosta Suárez, N., & Guarnizo Rojas, M. L. (2020). Los convenios de asociación con entidades sin ánimo de lucro y su inclusión como modalidad en el estatuto general de la contratación estatal. *Revista IUSTA, 52*, 123-146. https://www.redalyc.org/journal/5603/560365773006/html/

Colombia Compra Eficiente. (s. f.-a). *SECOP*. Recuperado el 2 de octubre de 2026, de https://www.colombiacompra.gov.co/secop

Colombia Compra Eficiente. (s. f.-b). *Compra pública innovadora: introducción*. Recuperado el 2 de octubre de 2026, de https://www.colombiacompra.gov.co/compra-publica-para-la-innovacion/compra-publica-innovadora-introduccion

Colombia Compra Eficiente. (2026). *SECOP II – Contratos electrónicos* [Conjunto de datos]. Datos Abiertos Colombia. Recuperado el 2 de octubre de 2026, de https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=dengue&departamento=Valle%20del%20Cauca&$limit=40

ConsultorSalud. (2023). *Res. 295 de 2023: cambios para las intervenciones colectivas*. https://consultorsalud.com/resolucion-295-2023-intervenciones-colectivas/

Congreso de la República de Colombia. (2007). *Ley 1150 de 2007, por medio de la cual se introducen medidas para la eficiencia y la transparencia en la Ley 80 de 1993*. http://www.secretariasenado.gov.co/senado/basedoc/ley_1150_2007.html

GitHub. (s. f.). *GitHub's plans*. GitHub Docs. Recuperado el 2 de octubre de 2026, de https://docs.github.com/en/get-started/learning-about-github/githubs-plans

Gobernación del Valle del Cauca. (s. f.). *Proyecto No. 7 Programa AEDES* [Ficha de proyecto financiado con el Fondo de CTeI del SGR]. https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=26030

Gobernación del Valle del Cauca. (2024). *Plan Territorial de Salud 2024-2027*. https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=73263

Indeed. (2026a). *Sueldo de ingeniero/a en sistemas en Cali, Valle del Cauca*. Recuperado el 2 de octubre de 2026, de https://co.indeed.com/career/ingeniero-en-sistemas/salaries/Cali--Valle-del-Cauca

Indeed. (2026b). *Sueldo de ingeniero/a en sistemas en Colombia*. Recuperado el 2 de octubre de 2026, de https://co.indeed.com/career/ingeniero-en-sistemas/salaries

Indeed. (2026c). *Sueldo de científico/a de datos en Colombia*. Recuperado el 2 de octubre de 2026, de https://co.indeed.com/career/cient%C3%ADfico-de-datos/salaries

Infobae. (2026, 1 de octubre). *Precio del dólar hoy en Colombia: se cotiza a la baja, la divisa está en $3.288,39 tras la decisión de subir la tasa de interés por parte del Banco de la República*. https://www.infobae.com/colombia/2026/10/01/precio-del-dolar-hoy-en-colombia-se-cotiza-en-3298-tras-la-decision-de-subir-la-tasa-de-interes-por-parte-del-banco-de-la-republica/

Instituto Nacional de Salud [INS]. (2024). *Protocolo de vigilancia en salud pública: dengue* (versión 07, 15 de julio de 2024). https://www.ins.gov.co/buscador-eventos/Lineamientos/Pro_Dengue.pdf

MI.COM.CO. (2026). *Precios de dominios*. Recuperado el 2 de octubre de 2026, de https://mi.com.co/precios

Microsoft. (s. f.). *Azure for Students*. Recuperado el 2 de octubre de 2026, de https://azure.microsoft.com/en-us/free/students

Ministerio de Ciencia, Tecnología e Innovación [Minciencias]. (s. f.). *Términos de referencia: Convocatoria 48 del SGR*. https://minciencias.gov.co/sites/default/files/upload/convocatoria/terminos_de_referencia_convocatoria_48.pdf

Ministerio de Ciencia, Tecnología e Innovación [Minciencias]. (2025). *Plan de convocatorias públicas, abiertas y competitivas de la Asignación para la Ciencia, Tecnología e Innovación del SGR 2025-2026*. https://minciencias.gov.co/sites/default/files/upload/paginas/plan_de_convocatorias_actei_2025-2026_0.pdf

Ministerio de Salud y Protección Social. (2015). *Resolución 518 de 2015*. https://www.minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/DE/DIJ/resolucion-0518-de-2015.pdf

Ministerio de Salud y Protección Social. (2023). *Resolución 295 de 2023*. https://www.minsalud.gov.co/Normatividad_Nuevo/Resoluci%C3%B3n%20No.%20295%20de%202023.pdf

Presidencia de la República de Colombia. (2026, 19 de febrero). *Decreto 159 de 2026* [salario mínimo mensual legal 2026]. Régimen Legal de Bogotá. https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=192181&dt=S

NASA Langley Research Center. (s. f.). *NASA POWER: Prediction of Worldwide Energy Resources*. Recuperado el 2 de octubre de 2026, de https://power.larc.nasa.gov/

Streamlit. (s. f.-a). *Streamlit Community Cloud*. Recuperado el 2 de octubre de 2026, de https://streamlit.io/cloud

Streamlit. (s. f.-b). *Manage your app*. Streamlit Docs. Recuperado el 2 de octubre de 2026, de https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app

Universidad Icesi. (2026, 21 de septiembre). *Dengue.IA.Cali cierra su primera fase*. https://www.icesi.edu.co/dengue-ia-cali-cierra-su-primera-fase/

Wellcome. (2023, 3 de febrero). *New digital tools use climate data to better predict and prepare for infectious diseases outbreaks*. https://wellcome.org/insights/articles/new-digital-tools-use-climate-data-better-predict-and-prepare-infectious-diseases-outbreaks
