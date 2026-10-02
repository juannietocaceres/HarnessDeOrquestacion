# Plan de Desarrollo: Skill de Optimización y Compresión de Tokens

## Visión General

Esta skill actuará como el "compactador de basura inteligente" de tu sistema. Su misión es interceptar el contexto antes de que llegue a agentes costosos, eliminando la redundancia, la prosa innecesaria y el formato expansivo, para entregar una cápsula de información hiperdensa. Esto reduce la latencia y recorta los costos de API sin sacrificar instrucciones críticas.

## Fase 1: Definición de las Reglas de Poda y Compresión

* **Minificación Estructural:** Todo JSON, HTML o código de configuración que pase por la skill es despojado de espacios, tabulaciones y saltos de línea innecesarios.
* **Conversión de Prosa a Clave-Valor:** Transforma narrativas conversacionales largas en variables directas. 
  * *Ejemplo:* De "El cliente mencionó que prefiere que el panel de control tenga un modo oscuro por defecto y que cargue rápido" a `UI_Prefs:[modo_oscuro,carga_rapida]`.
* **Poda de Historial (Context Pruning):** Detecta y elimina saludos, disculpas del sistema, confirmaciones pasadas ("Entendido, trabajaré en ello") y consolida múltiples turnos de chat en un único estado actual del proyecto.

## Fase 2: Diseño de la Lógica de Enrutamiento

* **Detección de Tipo de Contenido:** La skill debe saber qué está leyendo. Si es código fuente, aplica minificación estricta (no resume, para no romper la sintaxis). Si es lenguaje natural, aplica resumen extractivo.
* **Protección de Entidades Críticas:** Instrucciones estrictas para el LLM de nunca alterar IDs, rutas de archivos, credenciales, o requisitos técnicos específicos (versiones de librerías, IPs, puertos).

## Fase 3: Construcción de la Interfaz de la Skill (Input/Output)

* **Input:** Recibe el `raw_context` (historial, prompts largos, documentos anexos).
* **Output:** Genera un bloque comprimido estructurado, añadiendo un pequeño registro del ahorro para que el orquestador mida su eficiencia.

```json
{
  "compressed_payload": "UI_Prefs:[modo_oscuro,carga_rapida]|Tech:React,Node|Task:Build_Login",
  "metrics": {
    "original_tokens": 1450,
    "final_tokens": 120,
    "saved": "91%"
  }
}
```

## Fase 4: Pruebas de Retención de Contexto (Lossless Testing)

* **Auditoría de Ejecución:** Enviar el prompt original a un agente (Ej. *Backend_Developer*) y luego enviar solo el `compressed_payload` al mismo agente. El código generado en ambos casos debe cumplir exactamente los mismos requisitos.
* **Ajuste del Nivel de Agresividad:** Calibrar la skill para encontrar el punto óptimo donde la compresión no cause que los agentes empiecen a "alucinar" detalles por falta de contexto.

## Fase 5: Integración como Middleware

* **Inyección en el Pipeline:** Configurar esta skill para que se ejecute automáticamente como un paso intermedio. 
  * *Flujo:* `Usuario -> Project Triage -> TOKEN OPTIMIZER -> Agente de Desarrollo`.
* **Empaquetado de Sesión:** Utilizar la skill al final de cada ciclo de trabajo diario para comprimir todo lo que se hizo y guardarlo en la memoria del proyecto, listo para ser leído económicamente mañana.