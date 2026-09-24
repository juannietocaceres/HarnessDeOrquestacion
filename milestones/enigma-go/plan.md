# Plan de implementación: Enigma Go (MVP)

> Plan para un agente de código. Síguelo en orden por fases. Cada fase termina con criterios de aceptación verificables. No avances a la siguiente fase hasta cumplirlos.

## 1. Contexto

**Enigma Go** es una app móvil que genera juegos de misterio personalizados. El usuario indica:

- **Número de jugadores** (1–12)
- **Tiempo disponible** (15, 30, 45, 60 o 90 min)
- **Modo**: `app` (se juega dentro del celular), `exterior` (pistas físicas con QR en un lugar real) o `mixto`
- **Dificultad**: fácil / media / difícil

La app genera un caso único (historia, sospechosos, pistas, solución), guía la partida y al final revela al culpable y muestra un ranking.

**Restricción:** usar solo herramientas gratuitas o con plan gratis.

## 2. Stack

| Capa | Tecnología | Motivo |
|---|---|---|
| App | Expo (React Native) + TypeScript | Gratis, un solo código para Android/iOS, se prueba con Expo Go |
| Navegación | expo-router | Estándar en Expo |
| Estado | Zustand | Simple |
| Almacenamiento local | AsyncStorage | Partidas guardadas y offline |
| QR | `react-native-qrcode-svg` (generar) + `expo-camera` (escanear) | Modo exterior |
| Validación | Zod | Validar los casos generados |
| Backend (fase 4) | Supabase (plan gratis): Auth + Postgres + Edge Functions | Cuentas, historial y proxy seguro para la IA |
| IA (fase 4) | LLM vía Edge Function (proveedor configurable por variable de entorno) | La API key nunca va en la app |
| Tests | Jest + @testing-library/react-native | |

## 3. Alcance del MVP

**Incluido**

- 3 tipos de juego (sección 5)
- Generador de casos **sin IA** basado en plantillas (funciona offline y gratis)
- Flujo completo: configurar → jugar → acusar → revelar → ranking
- Modo exterior con QR imprimibles/compartibles
- Historial local de partidas

**Fuera del MVP**

- Multijugador en red (cada quien en su celular). En el MVP se juega **pasando un solo celular**.
- Pagos o historias premium
- GPS / geocercas (se deja como mejora futura)

## 4. Estructura del proyecto

```
enigma-go/
├─ app/                      # pantallas (expo-router)
│  ├─ index.tsx              # Inicio
│  ├─ setup.tsx              # Configurar partida
│  ├─ players.tsx            # Nombres de jugadores
│  ├─ game/[id]/briefing.tsx # Historia inicial + roles
│  ├─ game/[id]/play.tsx     # Pistas, interrogatorios, temporizador
│  ├─ game/[id]/scan.tsx     # Escáner QR (modo exterior)
│  ├─ game/[id]/accuse.tsx   # Acusación final
│  ├─ game/[id]/result.tsx   # ¡Caso resuelto! + ranking
│  ├─ print/[id].tsx         # Hoja de QR para imprimir/compartir
│  └─ history.tsx
├─ src/
│  ├─ engine/
│  │  ├─ types.ts            # tipos + esquemas Zod
│  │  ├─ scaling.ts          # reglas jugadores/tiempo → tamaño del caso
│  │  ├─ generator.ts        # genera un caso desde plantillas
│  │  ├─ validator.ts        # comprueba que el caso tenga solución
│  │  ├─ scoring.ts
│  │  └─ templates/          # JSON: escenarios, personajes, móviles, armas, pistas
│  ├─ store/gameStore.ts
│  ├─ components/
│  └─ lib/rng.ts             # RNG con semilla (casos reproducibles)
└─ __tests__/
```

## 5. Tipos de juego

| Tipo | Modo | Jugadores | Descripción |
|---|---|---|---|
| `detective` | app | 1–6 | El grupo investiga junto: lee pistas, interroga sospechosos (NPC) y acusa |
| `asesinato_roles` | app / mixto | 4–12 | Cada jugador recibe un personaje secreto y uno de ellos es el culpable. Rondas de pistas y votación |
| `busqueda` | exterior | 2–12 | El organizador esconde QR en un lugar. Cada QR revela una pista. El orden de las pistas lleva a la solución |

El tipo se sugiere automáticamente según jugadores y modo, y el usuario puede cambiarlo.

## 6. Reglas de escalado (`scaling.ts`)

Implementar como funciones puras con tests:

- **Pistas totales** = `clamp(round(tiempoMin / 6), 3, 15)`
- **Sospechosos**:
  - `detective`: `clamp(3 + floor(jugadores / 2), 3, 6)`
  - `asesinato_roles`: igual al número de jugadores (cada jugador es un sospechoso)
  - `busqueda`: `clamp(3 + floor(tiempoMin / 30), 3, 6)`
- **Pistas falsas (red herrings)**: fácil 0, media 1, difícil 2
- **Rondas** (`asesinato_roles`): `clamp(floor(tiempoMin / 15), 2, 5)`
- **Temporizador**: el tiempo elegido. Al llegar a 0 se fuerza la acusación.

## 7. Modelo de datos

```ts
type GameMode = 'app' | 'exterior' | 'mixto';
type GameType = 'detective' | 'asesinato_roles' | 'busqueda';

interface GameConfig {
  players: string[];          // nombres, length 1..12
  minutes: 15 | 30 | 45 | 60 | 90;
  mode: GameMode;
  type: GameType;
  difficulty: 'facil' | 'media' | 'dificil';
  seed: number;
}

interface Suspect {
  id: string;
  name: string;
  role: string;               // "jardinero", "chef"...
  motive: string;
  alibi: string;
  assignedPlayer?: string;    // solo en asesinato_roles
  secretBrief?: string;       // texto privado para ese jugador
}

interface Clue {
  id: string;
  order: number;
  text: string;
  eliminates: string[];       // ids de sospechosos que esta pista descarta
  pointsTo?: string;          // id del culpable si apunta a él
  isRedHerring: boolean;
  qrPayload?: string;         // modo exterior: "enigmago:{caseId}:{clueId}"
  hidingHint?: string;        // sugerencia de dónde esconder el QR
}

interface Case {
  id: string;
  title: string;
  setting: string;
  intro: string;
  victimOrObject: string;
  suspects: Suspect[];
  clues: Clue[];
  solution: { culpritId: string; explanation: string };
  config: GameConfig;
  createdAt: string;
}
```

Definir los esquemas con Zod en `types.ts` y exportar los tipos inferidos.

## 8. Validador de solución (clave)

`validator.ts` debe rechazar cualquier caso (de plantillas o de IA) que no cumpla:

1. Existe exactamente un `culpritId` y está en `suspects`.
2. La unión de `eliminates` de las pistas **no falsas** descarta a **todos** los inocentes y **nunca** al culpable.
3. Ninguna pista no falsa elimina al culpable.
4. Hay al menos una pista con `pointsTo === culpritId`.
5. El número de pistas y sospechosos coincide con `scaling.ts`.
6. En `asesinato_roles`, cada jugador tiene exactamente un sospechoso asignado.

Si falla, el generador reintenta con otra semilla (máximo 10 intentos) y, si sigue fallando, muestra un error.

## 9. Pantallas y flujo

1. **Inicio**: botón "Nueva partida" e "Historial".
2. **Configurar**: selector de jugadores (stepper 1–12), tiempo (chips), modo (App / Afuera / Mixto), dificultad y tipo sugerido.
3. **Jugadores**: ingresar nombres.
4. **Briefing**: intro del caso. En `asesinato_roles`, pantalla "pasa el celular a {jugador}" → toca para ver tu rol secreto → ocultar.
5. **Jugar**: temporizador visible, pistas desbloqueadas en orden (una cada `minutes / totalClues` min o manualmente), lista de sospechosos con notas. En `busqueda` las pistas se desbloquean **solo** al escanear su QR.
6. **Imprimir QR** (antes de jugar en modo exterior): cuadrícula de QR numerados con `hidingHint`. Se comparte como imagen/PDF con `expo-print` + `expo-sharing`.
7. **Acusar**: cada jugador (o el grupo) elige un sospechoso.
8. **Resultado**: "¡Caso resuelto!" o "El culpable escapó", explicación y ranking.

## 10. Puntuación (`scoring.ts`)

- Acierto: +100
- Bonus de tiempo: `+ floor(minutosRestantes * 2)`
- Penalización por pista extra pedida: −10
- En `asesinato_roles`: el culpable gana +150 si la mayoría no lo descubre.

## 11. Fases

### Fase 0: Proyecto base
- [ ] `npx create-expo-app@latest enigma-go -t expo-template-blank-typescript`
- [ ] Instalar dependencias:
  ```bash
  npx expo install expo-router expo-camera expo-print expo-sharing @react-native-async-storage/async-storage react-native-svg
  npm i zustand zod react-native-qrcode-svg
  npm i -D jest jest-expo @testing-library/react-native
  ```
- [ ] Configurar expo-router, ESLint y Jest.

**Aceptación:** `npx expo start` abre la app en Expo Go y `npm test` corre (aunque sea un test vacío).

### Fase 1: Motor sin IA
- [ ] `types.ts` con Zod
- [ ] `rng.ts` con semilla (mulberry32)
- [ ] `scaling.ts` + tests para todas las combinaciones de jugadores × tiempo
- [ ] Plantillas JSON: al menos **4 escenarios** (mansión, colegio, oficina, parque), **15 personajes**, **10 móviles** y **30 pistas parametrizables** con marcadores tipo `{suspect}` y `{object}`
- [ ] `generator.ts`: elige escenario, crea sospechosos, elige culpable, construye pistas que eliminan inocentes y agrega las pistas falsas
- [ ] `validator.ts` (sección 8)

**Aceptación:** un test que genera **500 casos** con configuraciones aleatorias, y el 100 % pasa el validador. La misma semilla produce el mismo caso.

### Fase 2: UI y flujo modo app
- [ ] Pantallas 1–5, 7 y 8 para `detective` y `asesinato_roles`
- [ ] Temporizador y desbloqueo de pistas
- [ ] Pantalla de "pasa el celular" para roles secretos
- [ ] Guardar partida en curso y en el historial (AsyncStorage)

**Aceptación:** se juega una partida completa de cada tipo con 1, 4 y 8 jugadores sin errores. Si se cierra la app a mitad de partida, se retoma al abrirla.

### Fase 3: Modo exterior
- [ ] Generar `qrPayload` por pista
- [ ] Pantalla de impresión con QR + sugerencias de escondite, y exportar a PDF
- [ ] Escáner: valida que el QR sea del caso actual, desbloquea la pista y avisa si está fuera de orden
- [ ] Modo `mixto`: algunas pistas en la app y otras por QR

**Aceptación:** se imprime una hoja de QR, se escanea con la cámara real y se desbloquean las pistas correctas. Un QR de otro caso es rechazado con un mensaje claro.

### Fase 4: IA generativa (opcional, detrás de un switch)
- [ ] Proyecto Supabase gratis y Edge Function `generate-case`
- [ ] La función recibe `GameConfig`, llama al LLM con el prompt de la sección 12 y devuelve JSON
- [ ] La app valida con Zod + `validator.ts`. Si falla, reintenta 2 veces y luego usa el generador de plantillas (fallback)
- [ ] API key solo como secreto de Supabase (`supabase secrets set LLM_API_KEY=...`)
- [ ] Límite simple: máximo N generaciones por dispositivo al día

**Aceptación:** con internet se generan casos por IA que pasan el validador. Sin internet o con error, la app usa plantillas sin que el usuario lo note.

### Fase 5: Pulido
- [ ] Estilo visual "noir" (blanco y negro, tipografía manuscrita para las pistas)
- [ ] Sonidos y vibración al desbloquear pistas
- [ ] Onboarding de 3 pantallas
- [ ] Build Android: `npx eas build -p android --profile preview` (APK gratis)

**Aceptación:** APK instalable en un Android real con el flujo completo funcionando.

## 12. Prompt para la IA (fase 4)

```
Eres un diseñador de juegos de misterio. Genera un caso en español en JSON
que cumpla EXACTAMENTE este esquema: {esquema Case sin config/createdAt}.

Parámetros:
- Tipo: {type}
- Jugadores: {players.length} ({players})
- Sospechosos: {nSuspects}
- Pistas: {nClues} (de ellas {nRedHerrings} falsas)
- Modo: {mode}
- Dificultad: {difficulty}
- Público: familiar, sin violencia gráfica

Reglas obligatorias:
1. Un solo culpable.
2. Las pistas no falsas, juntas, descartan a todos los inocentes mediante "eliminates".
3. Ninguna pista no falsa descarta al culpable.
4. Al menos una pista tiene "pointsTo" igual al culpable.
5. Si el modo es exterior o mixto, cada pista trae "hidingHint" realista para un parque o una casa.
6. Si el tipo es asesinato_roles, asigna un sospechoso por jugador con un "secretBrief" de máximo 60 palabras.

Responde SOLO con el JSON.
```

## 13. Definición de terminado

- Todas las casillas de las fases 0–3 marcadas (la 4 y la 5 son opcionales para la entrega).
- `npm test` en verde, con el test de 500 casos incluido.
- README con cómo correr la app, cómo jugar cada modo y capturas de pantalla.
- Sin API keys en el repositorio.
