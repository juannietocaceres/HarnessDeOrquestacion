# Guía para construir tu Canvas — AedesAlert Cali

> Milestone `canvas-aedesalert` · Tarea T4 · 2 de octubre de 2026.
> Para Diego: tú haces el lienzo; esta guía te dice qué poner en cada recuadro, con qué datos y qué evitar. Trae una **propuesta de referencia** por bloque (en español y en inglés) que puedes copiar tal cual o cambiar. Al final está la **escaleta de la presentación en inglés** (§11) y la **trazabilidad de cifras** (§12).
>
> Códigos de evidencia: **T1-Ix** = indicador Ix de `evidencias/T1-sector.md`; **T2 §x** = sección de `evidencias/T2-modelo-negocio.md`; **PREV-T2 Bx/Fx** = hallazgo de `milestones/validacion-regional-aedesalert/evidencias/T2-impacto.md`. Las URL de todas las cifras están en §12.
> Marcas: **[supuesto]** = no tiene fuente, se debe validar; **[hipótesis]** = segmento o ingreso sin evidencia de compra.

---

## 0. Cómo usar esta guía con tu plantilla

### 0.1 Mapa de tu plantilla (`insumos/modelo-canvas.png`)

Título de la plantilla: **#MODELO DE NEGOCIO: NOMBRE DE LA EMPRESA** → escribe **AedesAlert Cali**.
*Sugerencia (no obligatoria):* como el segmento que paga son los otros 8 municipios del Valle, podrías titularlo **AedesAlert** o **AedesAlert Valle**. Si lo cambias, cámbialo también en la portada del deck y en el guion; si no, deja **AedesAlert Cali**, que es el nombre usado en todo el trabajo anterior.

```
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ SOCIOS CLAVE │ ACTIVIDADES  │ PROPUESTA DE │ RELACIÓN CON │ SEGMENTOS DE │
│  (Bloque 1)  │ CLAVE (B. 2) │ VALOR (B. 4) │ EL CLIENTE   │ CLIENTES     │
│  alto        ├──────────────┼──────────────┤ (B. 5)       │  (Bloque 7)  │
│  izquierda   │ RECURSOS     │ [YOUR LOGO   ├──────────────┤  alto        │
│              │ CLAVE (B. 3) │  HERE]       │ CANALES (B.6)│  derecha     │
├──────────────┴──────────────┴──────┬───────┴──────────────┴──────────────┤
│ ESTRUCTURA DE COSTOS (Bloque 8)    │ FUENTES DE INGRESOS (Bloque 9)      │
│ franja inferior izquierda          │ franja inferior derecha             │
└────────────────────────────────────┴─────────────────────────────────────┘
```

| Orden de llenado (pauta) | Bloque | Dónde queda en tu plantilla | Tamaño | Máx. palabras versión corta |
|---|---|---|---|---|
| 1.° | Propuesta de valor (Bloque 4) | Centro, arriba (debajo queda el recuadro "YOUR LOGO HERE") | Mediano | 45 |
| 2.° | Segmentos de clientes (Bloque 7) | Columna derecha, de arriba abajo | Alto | 60 |
| 3.° | Canales (Bloque 6) | Cuarta columna, abajo | Mediano | 45 |
| 4.° | Relación con el cliente (Bloque 5) | Cuarta columna, arriba | Mediano | 45 |
| 5.° | Fuentes de ingresos (Bloque 9) | Franja inferior derecha | Ancho | 45 |
| 6.° | Recursos clave (Bloque 3) | Segunda columna, abajo | Mediano | 45 |
| 7.° | Actividades clave (Bloque 2) | Segunda columna, arriba | Mediano | 45 |
| 8.° | Socios clave (Bloque 1) | Columna izquierda, de arriba abajo | Alto | 60 |
| 9.° | Estructura de costos (Bloque 8) | Franja inferior izquierda | Ancho | 45 |

El recuadro "YOUR LOGO HERE" del centro y el de la esquina superior derecha son para el logo: pon uno sencillo (un mosquito o un semáforo) o bórralos.

### 0.2 Reglas para escribir en el lienzo

1. **Viñetas cortas, no párrafos.** Una idea por viñeta, de 3 a 10 palabras.
2. **Empieza por sustantivo o verbo:** "Mapa semanal…", "Validar con…", "Capacitación…".
3. **Sin cifras de relleno.** En el lienzo pon solo cifras que puedas defender (están en §12). Los precios sin fuente van con "(a validar)".
4. **Coherencia entre bloques:** cada segmento debe tener su propuesta, su canal, su relación y su ingreso. Si un segmento no paga (Cali, academia), dilo.
5. **Hipótesis visibles:** IPS y EPS van marcadas como hipótesis.
6. **Mismo lenguaje en lienzo, deck y guion.** Si cambias una viñeta, cámbiala en la diapositiva 6 (lienzo completo) y en la diapositiva del bloque.
7. **Lienzo en español o en inglés:** la pauta pide el lienzo para tu proyecto de grado; puedes entregar el lienzo en español y mostrar en el deck la versión en inglés (la bonificación es por *presentar* en inglés).

---

## 1. Propuesta de valor — Bloque 4 (1.° en la pauta)

**Qué pide el bloque.** El núcleo: qué problema resuelves, para quién, y por qué te elegirían a ti y no la alternativa (no hacer nada, hacerlo a mano o esperar algo como DengueIA).

**Preguntas guía**
- ¿Qué le duele hoy a la secretaría de salud de un municipio en riesgo muy alto cuando planea el control del mosquito?
- ¿Qué decisión toma mejor con un mapa semanal por comuna?
- ¿Qué gana con que el código sea libre (sin licencia, sin depender de un proveedor)?
- ¿Qué gana la Gobernación al ver los 9 municipios en un solo mapa?
- ¿En qué te diferencias de DengueIA **sin** decir que eres más preciso?

**Datos útiles (con fuente)**
- Cali tuvo **1.520 casos por 100.000 hab.** en 2024, frente a **937** del país [T1-I18].
- **9 municipios** del Valle en riesgo muy alto de transmisión: Cali, Buga, Candelaria, Yumbo, Palmira, Tuluá, Cartago, Florida y Jamundí [T1-I22].
- DengueIA (Cali) reportó **93 %** de efectividad y alertas **hasta 3 semanas** antes, en **174 zonas de 1 km²** con **~2,2 millones** de habitantes; la nota de Icesi **no menciona** código ni datos abiertos ni otros municipios [T2 §10; T1-I18].
- La evidencia para Cali muestra que el clima de **2 a 5 semanas antes** mejora la predicción por barrio [PREV-T2 F1].
- El costo de infraestructura del prototipo puede ser **$0** (NASA POWER, GitHub Free y Streamlit Community Cloud son gratuitos) [T2 §9.1].

**Errores comunes**
- Describir la tecnología en vez del beneficio ("usa XGBoost" no es una propuesta de valor).
- Prometer que "previene el dengue": la herramienta **predice y alerta**; la prevención la hace la secretaría.
- Decir que es "más preciso que DengueIA" o poner "93 %" como si fuera tu resultado: es el de DengueIA y tú aún no has entrenado tu modelo.
- Una sola frase genérica para todos los segmentos.

**Propuesta de referencia (ES)**
Alerta temprana de dengue, abierta y de bajo costo, para los municipios del Valle que no cuentan con un sistema como DengueIA. Cada semana, AedesAlert estima el riesgo por comuna con datos abiertos (casos del SIVIGILA y clima de NASA POWER) y lo muestra en un mapa semáforo, para que la secretaría de salud decida antes dónde focalizar el control del mosquito. El código es libre: la entidad no paga licencias, no queda atada a un proveedor y puede replicarlo en otro municipio. La Gobernación puede ver los 9 municipios en riesgo muy alto en un mismo mapa. AedesAlert complementa a DengueIA; no compite con él.

**Versión corta para la plantilla (ES, 37 palabras)**
- Mapa semanal de riesgo de dengue por comuna (semáforo)
- Anticipa dónde focalizar el control del mosquito
- Datos abiertos y código libre: sin licencias
- Replicable en los 8 municipios en riesgo muy alto
- Complemento de DengueIA, no competencia

**Reference proposal (EN)**
An open, low-cost dengue early-warning tool for the municipalities of Valle del Cauca that do not have a system like DengueIA. Every week, AedesAlert estimates dengue risk for each comuna (city district) using open data (SIVIGILA case reports and NASA POWER weather data) and shows it on a traffic-light map, so the local health secretariat can decide earlier where to focus mosquito control. The code is open source: no license fees, no vendor lock-in, and it can be replicated in another municipality. The departmental government can see all 9 very-high-risk municipalities on one map. AedesAlert complements DengueIA; it does not compete with it.

**Short version for the template (EN, 34 words)**
- Weekly dengue risk map by comuna (traffic light)
- Shows where to focus mosquito control first
- Open data and open-source code: no license fees
- Replicable in the 8 very-high-risk municipalities
- Complements DengueIA; does not compete

---

## 2. Segmentos de clientes — Bloque 7 (2.° en la pauta)

**Qué pide el bloque.** Para quién creas valor. En un bien público con código libre conviene separar **clientes** (quien paga implementación, capacitación o soporte) de **usuarios** (quien usa el mapa o el código sin pagar) [T2 §1.2].

**Preguntas guía**
- ¿Quién decide y quién paga? ¿Con qué presupuesto?
- ¿Qué segmento tiene evidencia de compra y cuál es solo una hipótesis?
- ¿Por qué Cali no es tu cliente principal si ya tiene DengueIA?
- ¿Es un mercado masivo o de nicho? (Es de nicho y del sector público: B2G.)

**Datos útiles (con fuente)**
- Segmento principal: secretarías de salud de **8 municipios** en riesgo muy alto (Buga, Candelaria, Cartago, Florida, Jamundí, Palmira, Tuluá y Yumbo) [T1-I22; T2 §1.1].
- Según el protocolo de dengue del INS (2024), las secretarías departamentales deben monitorear comportamientos inusuales y garantizar la vigilancia virológica y entomológica; las EPS deben "analizar y usar la información epidemiológica" [T2 §1.1].
- La Gobernación ya contrató servicios profesionales en un proyecto de dengue: **$40.500.000** (enero de 2022) [T2 §1.1, §4.3].
- Las IPS tienen poca capacidad de compra: la Secretaría de Salud del Valle reporta una cartera de **más de $6 billones** con la red pública y privada [T1 §3.1].
- **No se encontró evidencia** de que IPS, EPS, laboratorios o aseguradoras compren tableros predictivos de dengue [T2 §1.1, §11].

**Errores comunes**
- Poner "toda la población de Cali" como segmento: los ciudadanos no pagan ni operan el modelo.
- Poner IPS y EPS como clientes confirmados (son hipótesis).
- Poner a Cali como cliente principal: ya tiene DengueIA; es usuario de referencia.
- Olvidar a la Gobernación, que es cliente y aliado a la vez.

**Propuesta de referencia (ES)**
- **Clientes que pagan (principal):** secretarías de salud de Buga, Candelaria, Cartago, Florida, Jamundí, Palmira, Tuluá y Yumbo, los 8 municipios en riesgo muy alto fuera de Cali. Necesitan focalizar el control vectorial y no se conoce un sistema predictivo equivalente al de Cali en esos municipios.
- **Cliente y aliado:** Secretaría Departamental de Salud del Valle (incluye el Laboratorio de Salud Pública), que vigila a todos los municipios.
- **Usuario de referencia (no cliente principal):** Secretaría de Salud Pública de Cali, que ya usa DengueIA; AedesAlert le sirve como referencia abierta por comuna.
- **Segmentos secundarios [hipótesis]:** IPS (preparar urgencias e insumos) y EPS (anticipar demanda de su población afiliada). Validar con entrevistas.
- **Usuarios que no pagan:** universidades, semilleros y desarrolladores que reutilizan el código.

**Versión corta para la plantilla (ES, 45 palabras)**
- Pagan: secretarías de salud de Buga, Candelaria, Cartago, Florida, Jamundí, Palmira, Tuluá y Yumbo (riesgo muy alto)
- Cliente y aliado: Secretaría Departamental de Salud del Valle
- Usuario de referencia: Secretaría de Salud de Cali (usa DengueIA)
- Hipótesis: IPS y EPS
- Usuarios gratuitos: universidades y desarrolladores

**Reference proposal (EN)**
- **Paying customers (main segment):** the municipal health secretariats of Buga, Candelaria, Cartago, Florida, Jamundí, Palmira, Tuluá and Yumbo, the 8 very-high-risk municipalities outside Cali. They need to focus mosquito control, and no system like Cali's is known in these municipalities.
- **Customer and ally:** the Valle del Cauca departmental health secretariat (including its Public Health Laboratory), which oversees all municipalities.
- **Reference user (not the main customer):** Cali's Public Health Secretariat, which already uses DengueIA; AedesAlert gives it an open, comuna-level reference.
- **Secondary segments [hypothesis]:** clinics and hospitals (IPS), to prepare emergency rooms and supplies, and health insurers (EPS), to anticipate demand. To be validated with interviews.
- **Non-paying users:** universities, student research groups and developers who reuse the code.

**Short version for the template (EN, 41 words)**
- Paying: health secretariats of Buga, Candelaria, Cartago, Florida, Jamundí, Palmira, Tuluá and Yumbo (very high risk)
- Customer and ally: Valle del Cauca health secretariat
- Reference user: Cali health secretariat (uses DengueIA)
- Hypothesis: clinics and insurers (IPS/EPS)
- Free users: universities and developers

---

## 3. Canales — Bloque 6 (3.° en la pauta)

**Qué pide el bloque.** Cómo llegas al cliente en cada fase: cómo te conoce, cómo te evalúa, cómo te compra, cómo recibe el producto y qué pasa después de la compra.

**Preguntas guía**
- ¿Dónde se entera una secretaría de una herramienta así?
- ¿Cómo compra legalmente una entidad pública un servicio a una persona o a una universidad?
- ¿Por dónde entregas el producto (mapa, código, reporte)?
- ¿Qué canal usas para el piloto, antes de vender?

**Datos útiles (con fuente)**
- **SECOP II** es la plataforma transaccional de la contratación pública; todos los contratos de referencia de T2 están publicados allí [T2 §2].
- **Contratación directa** (Ley 1150 de 2007, art. 2, num. 4): lit. h) servicios profesionales y de apoyo a la gestión; lit. e) actividades científicas y tecnológicas [T2 §2, §4.2].
- **Universidad como puente:** Cali contrató a la Fundación Universidad del Valle por **$400 millones** (2020) para fortalecer la vigilancia epidemiológica [T2 §4.3].
- **COVE departamental:** las secretarías municipales deben participar en los comités de vigilancia del departamento (INS, 2024); allí coinciden los 9 municipios y la Gobernación [T2 §2].
- **Entrega gratuita:** repositorio público en GitHub y mapa web público en Streamlit [T2 §2, §9.1].

**Errores comunes**
- Poner "redes sociales" o "app en tiendas" como canal principal: el cliente es una entidad pública.
- Olvidar cómo se compra (SECOP II, contratación directa).
- Confundir canal (cómo llegas) con relación (cómo mantienes al cliente).

**Propuesta de referencia (ES)**
- **Conocer:** presentación en el COVE departamental y demo pública (mapa web + repositorio en GitHub); difusión por NIDO, Tecnoparque y el Clúster de Excelencia Clínica.
- **Evaluar:** piloto con una secretaría (prototipo con las 22 comunas de Cali y luego un municipio).
- **Comprar:** SECOP II por contratación directa (servicios profesionales o actividades científicas y tecnológicas), o convenio a través de la UCC.
- **Entregar:** mapa web semanal, reporte y código en GitHub.
- **Posventa:** capacitación y soporte durante la vigencia.

**Versión corta para la plantilla (ES, 30 palabras)**
- SECOP II y contratación directa
- Demo pública: mapa web + GitHub
- Presentación en el COVE departamental
- Convenio vía UCC
- NIDO, Tecnoparque y Clúster de Excelencia Clínica
- Piloto con una secretaría

**Reference proposal (EN)**
- **Awareness:** a pitch at the departmental surveillance committee (COVE) and a public demo (web map + GitHub repository); outreach through NIDO, Tecnoparque and the Clinical Excellence Cluster.
- **Evaluation:** a pilot with one health secretariat (prototype with Cali's 22 comunas, then one municipality).
- **Purchase:** SECOP II, through direct contracting (professional services or science and technology activities), or an agreement through UCC.
- **Delivery:** weekly web map, report and code on GitHub.
- **After sales:** training and support during the contract year.

**Short version for the template (EN, 32 words)**
- SECOP II and direct public contracting
- Public demo: web map + GitHub
- Pitch at the departmental surveillance committee (COVE)
- Agreements through UCC
- NIDO, Tecnoparque, Clinical Excellence Cluster
- Pilot with one health secretariat

---

## 4. Relación con el cliente — Bloque 5 (4.° en la pauta)

**Qué pide el bloque.** Qué tipo de relación tienes con cada segmento para conseguirlo, mantenerlo y que vuelva a contratar.

**Preguntas guía**
- ¿La relación es personal, automatizada o de comunidad?
- ¿Cómo validas el mapa con quienes hacen el control del mosquito?
- ¿Cómo logras que la secretaría opere el modelo sin depender de ti?
- ¿Cada cuánto se renueva la relación comercial?

**Datos útiles (con fuente)**
- DengueIA trabajó en co-creación: la Secretaría de Salud Pública de Cali aportó datos y validación [T2 §3].
- Los contratos de salud pública se hacen por vigencia anual o semestral; la contratación del PIC se hace "a más tardar el 31 de marzo de cada vigencia" (Res. 295 de 2023) [T2 §3, §4.1].
- La periodicidad semanal del reporte sigue a la semana epidemiológica de SIVIGILA [T2 §3, **supuesto** sobre el uso].

**Errores comunes**
- "Atención 24/7" o "chat con IA" sin un segmento que lo necesite.
- Una relación que crea dependencia del autor: contradice el código libre.
- Repetir los canales en este recuadro.

**Propuesta de referencia (ES)**
- **Co-creación:** validar el mapa con los técnicos de vectores (ETV) y salud ambiental de cada secretaría.
- **Acompañamiento semanal:** reporte o reunión corta con el riesgo de la semana.
- **Capacitación y transferencia:** para que el equipo de la secretaría opere el modelo por su cuenta.
- **Soporte por vigencia:** contrato anual que se renueva.
- **Comunidad abierta:** documentación, *issues* y réplicas en GitHub.

**Versión corta para la plantilla (ES, 28 palabras)**
- Co-creación: validar el mapa con técnicos de vectores
- Reporte semanal de riesgo
- Capacitación para operar sin depender del autor
- Soporte por contrato anual (vigencia)
- Comunidad abierta en GitHub

**Reference proposal (EN)**
- **Co-creation:** validate the map with each secretariat's vector-control and environmental health staff.
- **Weekly follow-up:** a short report or meeting with the week's risk.
- **Training and handover:** so the secretariat's team can run the model on its own.
- **Yearly support:** a contract renewed every fiscal year.
- **Open community:** documentation, issues and replications on GitHub.

**Short version for the template (EN, 28 words)**
- Co-creation: validate the map with vector-control staff
- Weekly risk report
- Training so the team runs it on its own
- Support through a yearly contract
- Open community on GitHub

---

## 5. Fuentes de ingresos — Bloque 9 (5.° en la pauta)

**Qué pide el bloque.** Cómo genera dinero el modelo: quién paga, por qué y cómo (pago por servicio, suscripción, convenio, financiación por proyecto).

**Preguntas guía**
- Si el código es gratis, ¿por qué te pagarían? (Por implementarlo, capacitar y dar soporte.)
- ¿Por qué el PIC no es tu puerta de entrada?
- ¿Qué ingresos son recurrentes y cuáles son de una sola vez (financiación de proyectos)?
- ¿Qué precio pondrías y en qué te basas? (Hoy es un supuesto.)

**Datos útiles (con fuente)**
- **Referencia de precio:** la Secretaría de Salud de Cali pagó **$12.864.000** y **$16.725.000** (oct-2023) por contratos de servicios profesionales de análisis de control de vectores [T2 §4.3].
- **El PIC va a la ESE local:** Palmira, **$2.300 millones** para 2026 con el Hospital Raúl Orejuela Bueno; Tuluá, **$1.160 millones** para el 2.° semestre de 2026 con la ESE Rubén Cruz Vélez. Por eso el PIC no es tu puerta de entrada [T2 §4.1].
- **Rubro de vigilancia de Cali:** **$3.412 millones** en 2026 ("Vigilancia en Salud Pública y fortalecimiento de los laboratorios") [T1-I8].
- **Convenio universidad–entidad:** Cali–Fundación Univalle, **$400 millones** (2020) [T2 §4.3].
- **Financiación por proyectos:** el SGR destina el **10 %** de las regalías a CTeI por convocatorias para alianzas del SNCTI; precedente: el **Programa AEDES** contra dengue, **$14.770 millones** en total y **$2.010 millones** para el Valle (incluyó Cali y Buga) [T2 §8]. Wellcome financió con **£22,7 millones** a **24 equipos en 12 países** herramientas clima–enfermedad con software abierto (2023) [T2 §8].
- **No se encontró** en SECOP II un contrato de software predictivo de dengue en el Valle [T2 §4.3].

**Errores comunes**
- "Venta de licencias": contradice el código libre.
- Poner el PIC como ingreso directo.
- Poner un precio como si fuera un dato: escríbelo "(a validar)".
- Mezclar financiación de proyectos (una vez) con ingresos recurrentes.
- Publicidad o venta de datos: los datos de salud son sensibles (Ley 1581 de 2012) [T1 §3.4].

**Propuesta de referencia (ES)**
- **Principal — servicios a secretarías (recurrente):** implementación por municipio, capacitación y soporte anual, contratados por contratación directa. Precio por municipio **[supuesto]**, a validar; referencia: contratos de servicios de análisis de vectores de $12,9 a $16,7 millones (Cali, 2023).
- **Complementario — convenio universidad–entidad:** la UCC o su grupo de investigación como ejecutor (actividades científicas y tecnológicas).
- **Financiación de desarrollo (no recurrente):** convocatorias SGR-CTeI en alianza con la UCC; cooperación internacional que exige software abierto.
- **[Hipótesis] Suscripción para IPS/EPS:** funciones extra (alertas por sede, informes).
- **Capital semilla:** Fondo Emprender en el próximo ciclo.
- El código y el mapa público siguen siendo gratuitos.

**Versión corta para la plantilla (ES, 30 palabras)**
- Servicios a secretarías: implementación por municipio, capacitación y soporte anual (precio a validar)
- Convenio universidad–entidad (UCC)
- Proyectos: SGR-CTeI, cooperación internacional
- Hipótesis: suscripción IPS/EPS
- Capital semilla: Fondo Emprender
- Código siempre gratuito

**Reference proposal (EN)**
- **Main — services for health secretariats (recurring):** setup per municipality, training and yearly support, hired through direct contracting. Price per municipality **[assumption]**, to be validated; benchmark: vector-control analysis contracts of COP 12.9 to 16.7 million (Cali, 2023).
- **Complementary — university–government agreements:** UCC or its research group as the contractor (science and technology activities).
- **Development funding (one-off):** royalties science fund calls (SGR-CTeI) in an alliance with UCC; international donors that require open-source software.
- **[Hypothesis] Subscription for clinics and insurers:** extra features (alerts by site, reports).
- **Seed capital:** Fondo Emprender in its next round.
- The code and the public map stay free.

**Short version for the template (EN, 32 words)**
- Services for health secretariats: setup per municipality, training, yearly support (price to be validated)
- University–government agreements (UCC)
- Project funding: SGR-CTeI, international cooperation
- Hypothesis: clinic/insurer subscription
- Seed capital: Fondo Emprender
- Code always free

---

## 6. Recursos clave — Bloque 3 (6.° en la pauta)

**Qué pide el bloque.** Los activos sin los cuales el modelo no funciona: físicos, intelectuales, humanos y financieros.

**Preguntas guía**
- ¿Qué datos necesitas y quién te los da?
- ¿Dónde vive el código y dónde se publica el mapa? ¿Cuánto cuesta?
- ¿Qué conocimiento tienes tú y qué te falta?
- ¿Qué relación necesitas para tener datos por comuna?

**Datos útiles (con fuente)**
- NASA POWER ofrece datos climáticos gratuitos [T2 §5].
- GitHub Free: repositorios públicos ilimitados y **2.000 minutos/mes** de Actions [T2 §9.1].
- Streamlit Community Cloud: gratis, solo apps públicas, hasta **2,7 GB** de memoria; la app "se duerme" tras **12 horas** sin tráfico [T2 §5].
- Azure for Students (opcional): **USD 100** de crédito por **12 meses**, sin tarjeta [T2 §5].
- Casos por comuna: probablemente requieren datos de la secretaría (convenio) **[supuesto, riesgo a confirmar]** [T2 §5, §11].
- Recurso humano: **1 persona** (el autor), con acompañamiento del director de proyecto de la UCC y de Tecnoparque [T2 §5].

**Errores comunes**
- Olvidar el recurso más crítico: los datos de casos por comuna.
- Poner "computador" y "internet" como recursos clave (no diferencian).
- Confundir recursos (lo que tienes) con actividades (lo que haces).

**Propuesta de referencia (ES)**
- **Datos:** casos de dengue (SIVIGILA o secretaría, agregados por comuna) y clima diario de NASA POWER.
- **Intelectuales:** modelos (Random Forest/XGBoost y SARIMA), código libre y documentación en GitHub.
- **Tecnológicos:** mapa en Streamlit Community Cloud (gratis); crédito opcional de Azure for Students.
- **Humanos:** el autor (datos, aprendizaje automático y despliegue); director de proyecto de la UCC; apoyo técnico de Tecnoparque.
- **Relacionales:** confianza con los técnicos de vectores de cada secretaría (datos por comuna y validación).

**Versión corta para la plantilla (ES, 32 palabras)**
- Datos: casos SIVIGILA + clima NASA POWER
- Modelos y código libre en GitHub
- Mapa en Streamlit (gratis)
- Autor: datos, IA y despliegue
- Director UCC y Tecnoparque
- Relación con técnicos de cada secretaría

**Reference proposal (EN)**
- **Data:** dengue cases (SIVIGILA or the secretariat, aggregated by comuna) and daily weather from NASA POWER.
- **Intellectual:** models (Random Forest/XGBoost and SARIMA), open-source code and documentation on GitHub.
- **Technology:** web map on Streamlit Community Cloud (free); optional Azure for Students credit.
- **People:** the author (data, machine learning and deployment); the UCC thesis advisor; technical support from Tecnoparque.
- **Relationships:** trust with each secretariat's vector-control staff (comuna-level data and validation).

**Short version for the template (EN, 32 words)**
- Data: SIVIGILA cases + NASA POWER weather
- Models and open-source code on GitHub
- Web map on Streamlit (free)
- Author: data, AI, deployment
- UCC advisor and Tecnoparque
- Trust with each secretariat's technical staff

---

## 7. Actividades clave — Bloque 2 (7.° en la pauta)

**Qué pide el bloque.** Lo que debes **hacer** bien para entregar la propuesta de valor: producir, resolver problemas, mantener la plataforma y vender.

**Preguntas guía**
- ¿Qué haces cada semana para que el mapa esté al día?
- ¿Cómo sabes que el modelo funciona antes de mostrarlo?
- ¿Qué haces para replicarlo en otro municipio?
- ¿Qué actividad comercial necesitas para venderle al Estado?
- ¿Qué haces para cuidar los datos de salud?

**Datos útiles (con fuente)**
- Clima rezagado de **2 a 5 semanas** mejora la predicción por barrio en Cali (Desjardins et al., 2020) [PREV-T2 F1].
- Los datos de salud son **datos sensibles** (Ley 1581 de 2012, art. 5) y su uso estadístico exige suprimir la identidad de los titulares (art. 6, lit. e) [T1 §3.4].
- DengueIA validó con la Secretaría de Cali [T2 §6].

**Errores comunes**
- Escribir solo actividades técnicas y olvidar la comercial y la de capacitación.
- Escribir recursos ("tener datos") en vez de actividades ("limpiar datos cada semana").
- Olvidar la gobernanza de datos.

**Propuesta de referencia (ES)**
1. Ingesta y limpieza semanal de casos y clima, agregados por comuna y semana epidemiológica.
2. Entrenamiento y comparación de modelos (Random Forest/XGBoost frente a SARIMA) con clima rezagado.
3. Publicación del mapa semáforo y del reporte semanal.
4. Validación con la secretaría.
5. Réplica a otro municipio (ajustar comunas y corregimientos).
6. Documentación y capacitación.
7. Gestión comercial pública: registro en SECOP II, propuestas por vigencia, presentación en el COVE.
8. Gobernanza de datos: solo datos agregados y anonimizados.

**Versión corta para la plantilla (ES, 34 palabras)**
- Limpiar datos cada semana
- Entrenar y comparar modelos (RF/XGBoost vs SARIMA)
- Publicar mapa y reporte semanal
- Validar con la secretaría
- Replicar por municipio
- Documentar y capacitar
- Vender por SECOP II
- Anonimizar y agregar datos

**Reference proposal (EN)**
1. Weekly collection and cleaning of case and weather data, aggregated by comuna and epidemiological week.
2. Training and comparing models (Random Forest/XGBoost versus SARIMA) with lagged weather.
3. Publishing the traffic-light map and the weekly report.
4. Validation with the health secretariat.
5. Replication in another municipality (adjusting comunas and rural areas).
6. Documentation and training.
7. Public-sector sales: SECOP II registration, yearly proposals, a pitch at the COVE.
8. Data governance: aggregated, anonymized data only.

**Short version for the template (EN, 34 words)**
- Clean data every week
- Train and compare models (RF/XGBoost vs SARIMA)
- Publish weekly map and report
- Validate with the secretariat
- Replicate per municipality
- Document and train
- Sell through SECOP II
- Anonymize and aggregate data

---

## 8. Socios clave — Bloque 1 (8.° en la pauta)

**Qué pide el bloque.** Quién te ayuda a operar, reducir riesgos o conseguir recursos que no tienes. Para cada socio: qué aporta.

**Preguntas guía**
- ¿Quién te da los datos que no son públicos?
- ¿Quién te da respaldo académico para entrar a convocatorias?
- ¿Quién te presta infraestructura gratis?
- ¿Quién ejecuta en terreno las acciones que el mapa ayuda a focalizar?
- ¿Con quién hay solo un posible intercambio y no un acuerdo?

**Datos útiles (con fuente)**
- NIDO acompañó **220 startups** en 2024-2025 (HealthTech, FoodTech, FinTech) [T1-I16].
- El Clúster de Excelencia Clínica agrupa **528 empresas** (2023) y tiene la línea "Modelos de negocio HealthTech" [T1-I9; T1 §1].
- Las convocatorias SGR-CTeI piden alianzas del SNCTI; en la convocatoria 48, el proponente debía ser un actor reconocido por Minciencias o una IES con experiencia en al menos dos proyectos de CTeI [T2 §8].
- El Programa AEDES tuvo una universidad aliada (UIS) [T2 §2, §8].
- Las ESE municipales ejecutan el PIC, que incluye el control de vectores [T2 §4.1, §7].

**Errores comunes**
- Repetir a los clientes como socios sin decir qué aportan (la secretaría es las dos cosas: cliente que paga y socio que da datos).
- Poner a DengueIA (Icesi, Univalle) como socio confirmado: no hay contacto ni acuerdo.
- Listar socios sin el aporte de cada uno.

**Propuesta de referencia (ES)**
- **Secretarías de salud (municipales y departamental):** datos por comuna, validación y contratación.
- **Laboratorio de Salud Pública Departamental:** vigilancia virológica y entomológica.
- **UCC (director de proyecto, grupo de investigación):** respaldo académico; ejecutor en alianzas SGR o Minciencias.
- **SENA-Tecnoparque, NIDO y Clúster de Excelencia Clínica:** prototipo, incubación y conexión con IPS/EPS.
- **INS y NASA POWER:** datos abiertos.
- **GitHub y Streamlit:** infraestructura gratuita.
- **ESE municipales:** ejecutan el control vectorial que el mapa ayuda a focalizar.
- **Equipo de DengueIA (Icesi, Univalle):** posible intercambio metodológico (sin acuerdo).
- **Financiadores:** Minciencias/SGR, Fondo Emprender y cooperación internacional.

**Versión corta para la plantilla (ES, 44 palabras)**
- Secretarías de salud: datos por comuna y validación
- Laboratorio de Salud Pública del Valle
- UCC: respaldo académico y alianzas SGR
- SENA-Tecnoparque, NIDO, Clúster de Excelencia Clínica
- INS y NASA POWER: datos abiertos
- GitHub y Streamlit: infraestructura
- ESE municipales: control vectorial
- Minciencias/SGR, Fondo Emprender, cooperación

**Reference proposal (EN)**
- **Health secretariats (municipal and departmental):** comuna-level data, validation and contracts.
- **Departmental Public Health Laboratory:** virological and entomological surveillance.
- **UCC (thesis advisor, research group):** academic backing; lead partner in SGR or Minciencias alliances.
- **SENA-Tecnoparque, NIDO and the Clinical Excellence Cluster:** prototyping, incubation and links to clinics and insurers.
- **INS and NASA POWER:** open data.
- **GitHub and Streamlit:** free infrastructure.
- **Municipal public hospitals (ESE):** they carry out the mosquito control that the map helps to target.
- **DengueIA team (Icesi, Univalle):** possible exchange of methods (no agreement yet).
- **Funders:** Minciencias/SGR, Fondo Emprender and international cooperation.

**Short version for the template (EN, 42 words)**
- Health secretariats: comuna data and validation
- Valle Public Health Laboratory
- UCC: academic backing and SGR alliances
- SENA-Tecnoparque, NIDO, Clinical Excellence Cluster
- INS and NASA POWER: open data
- GitHub and Streamlit: infrastructure
- Municipal public hospitals (ESE): mosquito control
- Minciencias/SGR, Fondo Emprender, international donors

---

## 9. Estructura de costos — Bloque 8 (9.° en la pauta)

**Qué pide el bloque.** Los costos más importantes de operar el modelo, si son fijos o variables, y si el modelo se guía por costo bajo o por valor.

**Preguntas guía**
- ¿Cuál es el costo dominante? (El tiempo de una persona.)
- ¿Qué cuesta la infraestructura mientras el mapa sea público?
- ¿Qué costos aparecen al pasar de prototipo a piloto?
- ¿Qué costo aparecería si una IPS o EPS pide un tablero privado?

**Datos útiles (con fuente)**
- Infraestructura: **$0** (NASA POWER, GitHub Free y Streamlit Community Cloud) [T2 §9.1].
- Dominio .com.co: **$114.990** el registro y **$149.990** la renovación (IVA incluido) [T2 §9.1].
- Ingeniero/a de sistemas en Cali: **$2.200.927/mes** (Indeed, **7 salarios**: muestra pequeña); en Colombia: **$2.583.055/mes** [T2 §9.1].
- Salario mínimo 2026: **$1.750.905** (Decreto 159 de 2026, transitorio) [T2 §9.1].
- Escenarios [supuesto, cálculo de T2]: prototipo ≈ **$0 a $150.000/año**; piloto de **6 meses** con 1 persona ≈ **$13,2 millones** (sin carga prestacional), más dominio y desplazamientos [T2 §9.2].
- Azure for Students (opcional): **USD 100**, equivalente a ≈ **$331.284** en crédito (TRM $3.312,84 del 1-oct-2026) [T2 §9.1].

**Errores comunes**
- Poner "costo $0": la infraestructura es gratis, pero tu tiempo no.
- Usar el salario de científico de datos de Colombia (**$6.909.154**) como si fuera el de un junior en Cali [T2 §9.1].
- Olvidar desplazamientos a los municipios y la capacitación.
- Meter aquí lo que te dan los financiadores (eso va en ingresos o socios).

**Propuesta de referencia (ES)**
- **Modelo guiado por costos bajos:** infraestructura gratuita mientras el mapa sea público.
- **Costo fijo dominante:** personal (1 persona). Referencia: $2,2 millones/mes de un ingeniero de sistemas en Cali (muestra pequeña) y $2,58 millones/mes en Colombia.
- **Costos variables:** desplazamientos a cada municipio para validar y capacitar **[supuesto, sin valor de referencia]**.
- **Costos menores:** dominio propio ($114.990 el registro .com.co).
- **Escenarios:** prototipo ≈ $0 a $150.000 al año; piloto de 6 meses en un municipio ≈ $13,2 millones más desplazamientos **[supuesto]**.
- **Riesgo de costo:** un tablero privado para IPS/EPS exigiría pagar nube **[supuesto]**.

**Versión corta para la plantilla (ES, 34 palabras)**
- Personal: 1 persona (ref. $2,2 M/mes, ingeniero en Cali)
- Infraestructura: $0 (NASA POWER, GitHub, Streamlit)
- Dominio .com.co: $114.990
- Desplazamientos a municipios (a estimar)
- Piloto 6 meses ≈ $13,2 M (estimado)
- Modelo de costos bajos

**Reference proposal (EN)**
- **Cost-driven model:** free infrastructure while the map stays public.
- **Main fixed cost:** people (1 person). Benchmark: COP 2.2 million/month for a systems engineer in Cali (small sample) and COP 2.58 million/month nationwide.
- **Variable costs:** travel to each municipality for validation and training **[assumption, no benchmark]**.
- **Minor costs:** own domain name (COP 114,990 to register a .com.co).
- **Scenarios:** prototype ≈ COP 0 to 150,000 per year; 6-month pilot in one municipality ≈ COP 13.2 million plus travel **[assumption]**.
- **Cost risk:** a private dashboard for clinics or insurers would require paid cloud hosting **[assumption]**.

**Short version for the template (EN, 34 words)**
- People: 1 person (benchmark COP 2.2M/month, engineer in Cali)
- Infrastructure: COP 0 (NASA POWER, GitHub, Streamlit)
- .com.co domain: COP 114,990
- Travel to municipalities (to be estimated)
- 6-month pilot ≈ COP 13.2M (estimate)
- Low-cost model

---

## 10. Chequeo de coherencia final (antes de entregar)

- [ ] El título de la plantilla dice **AedesAlert Cali** (o el nombre que elegiste) y es el mismo del deck y del guion.
- [ ] Los 9 recuadros están llenos, en viñetas, sin párrafos, dentro del límite de palabras (45; 60 en Socios y Segmentos).
- [ ] **Segmento principal → propuesta → canal → relación → ingreso:** secretarías de los 8 municipios → mapa semanal abierto → SECOP II/COVE/piloto → co-creación + soporte anual → servicios de implementación, capacitación y soporte.
- [ ] **Gobernación:** aparece en Segmentos (cliente y aliado), Socios (Laboratorio de Salud Pública) y Propuesta (los 9 municipios en un mapa).
- [ ] **Cali:** aparece como usuario de referencia, no como cliente principal.
- [ ] **IPS/EPS:** marcadas como hipótesis en Segmentos e Ingresos.
- [ ] **Código libre** en Propuesta, y ningún ingreso por licencias en Ingresos.
- [ ] **PIC:** no aparece como ingreso; la ESE aparece como socio que ejecuta el control.
- [ ] **Datos por comuna:** aparecen en Recursos y en Socios (secretarías) como dependencia.
- [ ] **Actividades** cubren lo técnico, la validación, la capacitación, la venta y la gobernanza de datos.
- [ ] **Costos** incluyen personal y desplazamientos, no solo "$0".
- [ ] Ninguna frase dice que AedesAlert es más preciso que DengueIA ni que "previene" el dengue.
- [ ] Toda cifra del lienzo está en §12 (y el precio por municipio dice "a validar").
- [ ] Si cambiaste algo, actualizaste las diapositivas 6 a 10 de la escaleta.

---

## 11. Escaleta de la presentación (EN) — 10 minutes

**Audience:** teacher and classmates (internal presentation). **Speaker:** Diego, alone. **Language:** English (+0.3 bonus).
**Exposed slides:** 12 + 1 backup (sources). **Total: 9:45** (15 seconds of margin).
**Rule:** every number on screen comes from §12. The Canvas slides use the reference proposal of §1–§9; if Diego changes his Canvas, he updates slides 6 to 10.

| Slide | Title (EN) | Key message (EN) | On screen (EN) | Time (start–end) |
|---|---|---|---|---|
| 1 | AedesAlert Cali | An open early-warning map for dengue in Valle del Cauca. | Project name; "Weekly dengue risk by comuna, with open data"; Juan Diego Nieto · Systems Engineering · UCC Cali · course name; traffic-light icon | 0:00–0:20 |
| 2 | Dengue hits Valle del Cauca hard | Dengue is a large, measured public health problem, and Cali is above the national average. | Cali 2024: **1,520** cases per 100,000 people vs **937** in Colombia · Colombia 2024: **312,643** cases · Cost to Colombia: **≈USD 252 million a year** (2020 dollars) · **9** municipalities of Valle at very high risk (map with names) | 0:20–1:05 |
| 3 | The sector: health, powered by IT | AedesAlert belongs to the health sector (HealthTech), and its first market is public health (GovTech). | Colombia spends **8.14%** of GDP on health (2024) · Health care activity grew **2.5%** in 2025 · Valle: 3rd largest economy, **≈9.8%** of GDP · Clinical Excellence Cluster: **528** firms (2023) · Two markets: clinical care (private) vs public health (secretariats) | 1:05–1:55 |
| 4 | Sector trends and rules | The sector is going digital, Valle has strong surveillance, and the law allows open, aggregated data. | HealthTech = **9%** of **2,295** Colombian startups · Valle = **11%** of startups · Digital maturity of regional health institutions: **2.42 / 5** · Valle ranks **1st** in public health surveillance (**98.68%**, Q1 2026) · Health data are sensitive (Law 1581 of 2012) → aggregated, anonymized data only · National AI policy (CONPES 4144 of 2025) | 1:55–2:40 |
| 5 | The idea, and DengueIA | DengueIA proved in Cali that forecasting dengue works; AedesAlert makes it open and replicable for the rest of the Valle. | Flow: SIVIGILA cases + NASA POWER weather → Random Forest/XGBoost vs SARIMA → weekly traffic-light map by comuna · Two columns: **DengueIA** (Cali, **174** zones of 1 km², ~**2.2 million** people, **93%** reported effectiveness, up to **3 weeks** ahead) / **AedesAlert** (comunas, open data, open-source code, prototype with Cali's **22** comunas, then the other **8** very-high-risk municipalities) · "A complement, not a competitor" | 2:40–3:35 |
| 6 | The Business Model Canvas | One view of the whole model; the next slides follow the order our teacher suggested. | Full reference Canvas (short EN versions of §1–§9) in the template layout; block numbers 1–9; small note: "Order: 4 → 7 → 6 → 5 → 9 → 3 → 2 → 1 → 8" | 3:35–4:15 |
| 7 | Value and customers (blocks 4 and 7) | Health secretariats of the 8 very-high-risk municipalities pay; Cali is a reference user; clinics and insurers are a hypothesis. | Value proposition (5 bullets) · Segments: paying (8 municipalities, named), customer and ally (Valle health secretariat), reference user (Cali), hypothesis (IPS/EPS), free users (academia) | 4:15–5:20 |
| 8 | Channels, relationships and revenue (blocks 6, 5 and 9) | The code is free; revenue comes from setup, training and yearly support, bought through public procurement. | Channels: COVE pitch, public demo, pilot, SECOP II, UCC agreement · Relationship: co-creation, weekly report, training, yearly support · Revenue: services (price to be validated; benchmark **COP 12.9–16.7 million** per contract, Cali 2023) · Why not the PIC: it goes to the local public hospital (Palmira 2026: **COP 2,300 million**) · Project funding: SGR-CTeI (precedent: AEDES program, **COP 14,770 million**) | 5:20–6:35 |
| 9 | Resources, activities and partners (blocks 3, 2 and 1) | Open data, free tools and one person, backed by the health secretariats, UCC and the local ecosystem. | Resources: SIVIGILA + NASA POWER, GitHub, Streamlit, author, UCC advisor · Activities: weekly data cleaning, model comparison, weekly map, validation, replication, training, SECOP II sales, data governance · Partners: secretariats, Public Health Lab, UCC, Tecnoparque, NIDO (**220** startups supported), Clinical Excellence Cluster, ESE, funders | 6:35–7:35 |
| 10 | Cost structure (block 8) | A low-cost model: infrastructure is free; the real cost is one person's time. | Infrastructure: **COP 0** · People: **COP 2.2 million/month** (systems engineer, Cali; small sample) · .com.co domain: **COP 114,990** · 6-month pilot ≈ **COP 13.2 million** + travel (estimate) · Fixed costs > variable costs | 7:35–8:20 |
| 11 | Risks and next steps | Demand and data are not validated yet; the next steps test both. | Risks: demand in the 8 municipalities not validated · comuna-level data may need a data agreement · no accuracy comparison with DengueIA · price is an assumption · Next steps: prototype with Cali's **22** comunas (thesis) → interviews and a pilot with one secretariat → SECOP II registration and COVE pitch → SGR-CTeI call through UCC | 8:20–9:15 |
| 12 | Closing | DengueIA showed it works in Cali; AedesAlert brings it, openly, to the rest of the Valle. | One sentence: "Open data. Open code. Earlier action." · Traffic-light map image · "Thank you — questions?" | 9:15–9:45 |
| 13 (backup) | Sources | All numbers come from public, cited sources. | Short APA list: DANE (2026), World Bank (2026), INS (2025, 2026), Rockefeller Foundation (2026), Universidad Icesi (2026), Gobernación del Valle (2024), Cámara de Comercio de Cali (2025, 2026), SECOP II (2026), Indeed (2026), MI.COM.CO (2026), BBVA Spark (2026), La República (2026), Rodríguez-Morales et al. (2024), Desjardins et al. (2020) | (not timed) |

**Time check:** 0:20 + 0:45 + 0:50 + 0:45 + 0:55 + 0:40 + 1:05 + 1:15 + 1:00 + 0:45 + 0:55 + 0:30 = **9:45** (585 seconds), within 9:30–10:00.

**Notes for the deck (T6) and the script (T7)**
- Say "reported effectiveness" for DengueIA's 93%: it is their number, not ours.
- Say "about 9.8%" for Valle's share of GDP (own calculation from DANE figures).
- Say "small sample" for the Cali salary (7 salaries on Indeed).
- Say "hypothesis" for clinics and insurers, and "to be validated" for the price.
- On slide 6, put the short EN versions exactly as in §1–§9.

---

## 12. Trazabilidad de cifras (cifra → archivo/hallazgo → URL)

Rutas: **T1** = `evidencias/T1-sector.md`; **T2** = `evidencias/T2-modelo-negocio.md`; **PREV-T2** = `milestones/validacion-regional-aedesalert/evidencias/T2-impacto.md`. Los números que solo organizan este documento (número de bloque, orden de la pauta, límites de palabras, número y tiempo de diapositivas) no son datos y no se listan.

| # | Cifra (como aparece) | Dónde se usa | Archivo / hallazgo | URL |
|---|---|---|---|---|
| C1 | Cali 2024: 1.520 casos por 100.000 hab. vs 937 nacional | §1, diap. 2 | T1-I18 (PREV-T2 B3) | https://www.rockefellerfoundation.org/news/dengueai-model-anticipates-outbreaks-93-effectiveness-three-weeks-advance-notice/ |
| C2 | 9 municipios del Valle en riesgo muy alto (Cali + 8, con nombres) | §0, §1, §2, diap. 2, 5, 7 | T1-I22; T2 §1.1 (PREV-T2 B5) | https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=73263 |
| C3 | DengueIA: 93 % de efectividad reportada, hasta 3 semanas, 174 zonas de 1 km², ~2,2 millones de habitantes | §1, diap. 5 | T2 §10; T1-I18 y §3.3 | https://www.icesi.edu.co/dengue-ia-cali-cierra-su-primera-fase/ · https://www.rockefellerfoundation.org/news/dengueai-model-anticipates-outbreaks-93-effectiveness-three-weeks-advance-notice/ |
| C4 | Clima rezagado de 2 a 5 semanas | §1, §7 | PREV-T2 F1 (Desjardins et al., 2020) | https://doi.org/10.4269/ajtmh.20-0080 |
| C5 | Infraestructura $0 (NASA POWER, GitHub Free, Streamlit Community Cloud) | §1, §9, diap. 10 | T2 §9.1 | https://power.larc.nasa.gov/ · https://docs.github.com/en/get-started/learning-about-github/githubs-plans · https://streamlit.io/cloud |
| C6 | Gobernación: $40.500.000, ene-2022 (proyecto de dengue) | §2 | T2 §1.1, §4.3 | https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=dengue&departamento=Valle%20del%20Cauca&$limit=40 |
| C7 | Cartera de más de $6 billones (Secretaría de Salud del Valle con la red) | §2 | T1 §3.1 (Consultor Salud, 2026a) | https://consultorsalud.com/gestion-en-salud-del-valle-del-cauca-destacada/ |
| C8 | Cali–Fundación Univalle: $400 millones (2020) | §3, §5 | T2 §4.3 | https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=universidad%20vigilancia%20salud%20publica&departamento=Valle%20del%20Cauca&$order=fecha_de_firma%20DESC&$limit=20 |
| C9 | 22 comunas de Cali | §3, diap. 5, 11 | PREV-T2 B10 | https://consultorsalud.com/reduccion-dengue-cali-estrategias-efectivas/ |
| C10 | Ley 1150 de 2007, art. 2, num. 4, lit. e) y h) | §3 | T2 §4.2 | http://www.secretariasenado.gov.co/senado/basedoc/ley_1150_2007.html |
| C11 | Contratación del PIC "a más tardar el 31 de marzo de cada vigencia" (Res. 295 de 2023) | §4 | T2 §4.1 | https://www.minsalud.gov.co/Normatividad_Nuevo/Resoluci%C3%B3n%20No.%20295%20de%202023.pdf |
| C12 | Contratos de Cali por análisis de vectores: $12.864.000 y $16.725.000 (oct-2023) → "$12,9 a $16,7 millones" | §5, diap. 8 | T2 §4.3 | https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=dengue&departamento=Valle%20del%20Cauca&$limit=40 |
| C13 | PIC Palmira 2026: $2.300 millones; PIC Tuluá 2.° semestre 2026: $1.160 millones | §5, diap. 8 | T2 §4.1 | https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=intervenciones%20colectivas&ciudad=Palmira&$order=fecha_de_firma%20DESC&$limit=15 · https://www.datos.gov.co/resource/jbjy-vk9h.json?$q=intervenciones%20colectivas&ciudad=Tulu%C3%A1&$order=fecha_de_firma%20DESC&$limit=15 |
| C14 | Rubro de vigilancia en salud pública de Cali 2026: $3.412 millones | §5 | T1-I8 | https://www.minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/VP/FS/pfts-cali-2024-2027-publicacion.pdf |
| C15 | SGR: 10 % de las regalías a CTeI; convocatoria 48 (IES con al menos dos proyectos de CTeI) | §5, §8 | T2 §8 | https://minciencias.gov.co/sites/default/files/upload/paginas/plan_de_convocatorias_actei_2025-2026_0.pdf · https://minciencias.gov.co/sites/default/files/upload/convocatoria/terminos_de_referencia_convocatoria_48.pdf |
| C16 | Programa AEDES: $14.770 millones en total ($14.769.939.663); $2.010 millones para el Valle | §5, diap. 8 | T2 §0, §8 | https://www.valledelcauca.gov.co/loader.php?lServicio=Tools2&lTipo=viewpdf&id=26030 |
| C17 | Wellcome (2023): £22,7 millones, 24 equipos, 12 países, software abierto | §5 | T2 §8 | https://wellcome.org/insights/articles/new-digital-tools-use-climate-data-better-predict-and-prepare-infectious-diseases-outbreaks |
| C18 | Ley 1581 de 2012 (art. 5 datos sensibles; art. 6, lit. e) | §5, §7, diap. 4 | T1 §3.4 | http://www.secretariasenado.gov.co/senado/basedoc/ley_1581_2012.html |
| C19 | GitHub Free: 2.000 minutos/mes de Actions | §6 | T2 §9.1 | https://docs.github.com/en/get-started/learning-about-github/githubs-plans |
| C20 | Streamlit Community Cloud: hasta 2,7 GB; se duerme tras 12 horas | §6 | T2 §5 | https://streamlit.io/cloud · https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app |
| C21 | Azure for Students: USD 100 por 12 meses ≈ $331.284 (TRM $3.312,84, 1-oct-2026) | §6, §9 | T2 §5, §9.1 | https://azure.microsoft.com/en-us/free/students · https://www.infobae.com/colombia/2026/10/01/precio-del-dolar-hoy-en-colombia-se-cotiza-en-3298-tras-la-decision-de-subir-la-tasa-de-interes-por-parte-del-banco-de-la-republica/ |
| C22 | 1 persona (el autor) | §6, §9, diap. 9-10 | T2 §5, §9.2 | (dato de la idea; sin URL: es el autor) |
| C23 | NIDO: 220 startups acompañadas (2024-2025) | §8, diap. 9 | T1-I16 | https://www.ccc.org.co/nido-ampla-su-alcance-y-fortalece-la-innovacin-en-el-valle-del-cauca/ |
| C24 | Clúster de Excelencia Clínica: 528 empresas (2023) | §8, diap. 3 | T1-I9 | https://www.ccc.org.co/plataformacluster/excelencia-clinica/ |
| C25 | Dominio .com.co: $114.990 registro / $149.990 renovación | §9, diap. 10 | T2 §9.1 | https://mi.com.co/precios |
| C26 | Ingeniero/a de sistemas: Cali $2.200.927/mes (7 salarios) → "$2,2 M"; Colombia $2.583.055/mes → "$2,58 M" | §9, diap. 10 | T2 §9.1 | https://co.indeed.com/career/ingeniero-en-sistemas/salaries/Cali--Valle-del-Cauca · https://co.indeed.com/career/ingeniero-en-sistemas/salaries |
| C27 | Científico/a de datos en Colombia: $6.909.154/mes | §9 | T2 §9.1 | https://co.indeed.com/career/cient%C3%ADfico-de-datos/salaries |
| C28 | Salario mínimo 2026: $1.750.905 (Decreto 159 de 2026) | §9 | T2 §9.1 | https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=192181&dt=S |
| C29 | Escenarios: prototipo ≈ $0 a $150.000/año; piloto 6 meses ≈ $13,2 millones (6 × $2.200.927) | §9, diap. 10 | T2 §9.2 [supuesto, cálculo con cifras de T2 §9.1] | https://co.indeed.com/career/ingeniero-en-sistemas/salaries/Cali--Valle-del-Cauca · https://mi.com.co/precios |
| C30 | Colombia 2024: 312.643 casos de dengue | diap. 2 | T1-I17 (PREV-T2 A1) | https://www.ins.gov.co/buscador-eventos/Informesdeevento/DENGUE%20INFORME%20DE%20EVENTO%202024.pdf |
| C31 | Costo del dengue en Colombia ≈ USD 252 millones al año (USD 2020) | diap. 2 | T1-I21 (PREV-T2 D1-D2) | https://doi.org/10.1371/journal.pntd.0012718 |
| C32 | Gasto corriente en salud: 8,14 % del PIB (2024) | diap. 3 | T1-I5 | https://api.worldbank.org/v2/country/CO/indicator/SH.XPD.CHEX.GD.ZS?format=json&mrv=5 |
| C33 | Atención de la salud: +2,5 % en 2025 | diap. 3 | T1-I3 | https://www.dane.gov.co/files/operaciones/PIB/bol-PIB-IVtrim2025.pdf |
| C34 | Valle: 3.ª economía, ≈9,8 % del PIB (2025pr) | diap. 3 | T1-I1 | https://www.dane.gov.co/files/operaciones/PIB/bol-PIBDep-2025pr.pdf |
| C35 | HealthTech = 9 % de 2.295 startups | diap. 4 | T1-I13 | https://www.bbvaspark.com/en/news/colombia-tech-report-2026-ecosystem-startups/ |
| C36 | Valle = 11 % de las startups del país | diap. 4 | T1-I15 | https://www.larepublica.co/empresas/ya-hay-mas-de-2-200-startups-en-colombia-sector-de-saas-lidera-por-encima-de-fintech-4396062 |
| C37 | Madurez digital de instituciones de salud de la región: 2,42 / 5 | diap. 4 | T1-I12 | https://www.ccc.org.co/wp-content/uploads/2025/08/20250822_InformeEC.pdf |
| C38 | Valle 1.° en vigilancia en salud pública: 98,68 % (I trim. 2026) | diap. 4 | T1-I23 | https://www.ins.gov.co/BibliotecaDigital/2026-boletin-epidemiologico-semana-21.pdf |
| C39 | CONPES 4144 de 2025 (Política Nacional de IA) | diap. 4 | T1 §3.3, §3.4 (PREV-T3 §2.1) | https://colaboracion.dnp.gov.co/CDT/Conpes/Econ%C3%B3micos/4144.pdf · https://www.mintic.gov.co/portal/715/w3-article-400044.html (PREV-T3: el PDF del DNP no abrió; ejes verificados en fuentes secundarias) |
