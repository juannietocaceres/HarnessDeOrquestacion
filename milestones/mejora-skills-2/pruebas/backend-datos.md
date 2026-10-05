# Pruebas de N1 — skill `backend-datos`

Skill probada: `.claude/skills/backend-datos/` (SKILL.md y las dos plantillas).
Artefactos de prueba: [`backend-datos/`](backend-datos/).

## 1. Regresión: panel-tareas-demo (T1 y T2)

Se aplicó la skill a las descripciones de T1 y T2 de `panel-tareas-demo` y se
comparó con los originales.

- Generados: [`regresion/schema-tareas.md`](backend-datos/regresion/schema-tareas.md) y [`regresion/contrato-tareas.md`](backend-datos/regresion/contrato-tareas.md).
- Referencias: `schema/tareas.md` y `api/contrato-tareas.md`.

| Aspecto | Original | Generado | Resultado |
|---|---|---|---|
| Entidad | `tarea` (`id`, `titulo`, `estado`, `fecha_creacion`) | igual | Cubre lo mismo |
| Endpoints | `POST /tareas`, `GET /tareas` | igual | Cubre lo mismo |
| Códigos de error | `400` con `titulo_invalido`, campo `titulo` (vacío, solo espacios, más de 200 caracteres) | igual | Cubre lo mismo |
| Formato de error | `{error, campo, mensaje}` | igual | Cubre lo mismo |

Diferencias: el generado añade una tabla de pruebas de contrato (caso feliz y
de error por endpoint, más lista vacía) y una sección de supuestos, que exige
la skill (§8). Los campos que asigna el servidor y llegan del cliente se
ignoran (supuesto documentado). No hay diferencias de fondo.

## 2. Prueba nueva: app Expo con login y favoritos sincronizados

Carpeta: [`backend-datos/expo-favoritos/`](backend-datos/expo-favoritos/).

| Entregable | Archivo |
|---|---|
| Modelo de datos | [`schema-favoritos.md`](backend-datos/expo-favoritos/schema-favoritos.md) |
| Contrato de API | [`contrato-favoritos.md`](backend-datos/expo-favoritos/contrato-favoritos.md) |
| Migración con RLS | [`20261002000000_crear_favoritos.sql`](backend-datos/expo-favoritos/20261002000000_crear_favoritos.sql) |
| Datos semilla | [`seed.sql`](backend-datos/expo-favoritos/seed.sql) |
| Alternativa Firebase | [`firestore.rules`](backend-datos/expo-favoritos/firestore.rules) |
| Variables de entorno (contrato §3.3) | [`.env.example`](backend-datos/expo-favoritos/.env.example) |

Verificación de criterios:

- **RLS**: la migración ejecuta `enable row level security` y crea políticas de lectura, alta y borrado por `auth.uid()` en la misma migración que la tabla.
- **Sin auth a mano**: el contrato usa `supabase.auth.signUp`, `signInWithPassword`, `signOut` y `getSession`. Una búsqueda de `bcrypt`, `hash` y `password` en el SQL no encuentra tabla de usuarios ni hashing propio.
- **`.env.example`**: una variable por bloque, valor vacío, con ámbito y sensibilidad. Solo contiene las dos variables públicas (`EXPO_PUBLIC_*`); la clave de servicio no aparece.
- **Crear la base real en la nube**: queda como `verificacion_manual` (requiere la cuenta del usuario); no se ejecutó.
