---
paths:
  - "src/**/infrastructure/output/postgres/**"
---

# Postgres / asyncpg

## Estructura de carpetas de `infrastructure/output/postgres/`

Cada feature organiza su carpeta `postgres/` en subcarpetas por rol, nunca
archivos sueltos al nivel de `postgres/`:

- `adapter/<adapter_name>.py` — la(s) clase(s) que implementan el/los SPI de
  la feature (`repository_adapter.py`, `history_adapter.py`). Solo la clase y
  sus métodos, sin constantes SQL sueltas ni funciones ajenas a esa clase.
- `schema/<tabla>.py` — un archivo por tabla, cada uno con su propio
  `async def ensure_schema(pool)` (nombre de función igual en todos, el
  archivo ya lo identifica). `schema/__init__.py` re-exporta un
  `ensure_schema(pool)` que orquesta (llama) el de cada tabla — así el import
  externo (`from <feature>.infrastructure.output.postgres.schema import
  ensure_schema`) no cambia aunque `schema` pase de módulo a paquete.
- `utils/constants.py` — TODAS las strings SQL de la feature (tanto las que
  usa `adapter/` como las de `schema/`), como constantes `_SQL` a secas. Ni
  `adapter/` ni `schema/` definen SQL inline, todo se importa desde acá.
- `utils/helpers.py` — funciones que no pertenecen a un adapter específico
  (ver `common/infrastructure/output/postgres/utils/helpers.py`,
  `upsert_member` — la usan varios adapters de varias features, no es
  método de ninguno).

Ejemplo real: `activity/infrastructure/output/postgres/` tiene
`schema/user_message_stats.py` + `schema/chat_activity_timeline.py` (dos
tablas, dos archivos), `utils/constants.py` con las ~10 queries de ambos
(schema + adapter), y `adapter/repository_adapter.py` con la clase
`PostgresActivityRepository`.

## Gotchas de asyncpg / Supabase

- **Credenciales como campos separados** (`DB_HOST`, `DB_PORT`, `DB_NAME`,
  `DB_USER`, `DB_PASSWORD`), nunca una sola `DATABASE_URL` armada a mano — un
  password con caracteres especiales (`#`, `&`, `!`) rompe el parseo de URL.
- Siempre `statement_cache_size=0` en `asyncpg` porque se usa el pooler de
  Supabase (PgBouncer en modo transacción, que no soporta prepared statements).
- Un `SUM(...)` (u otro agregado) en una query devuelve `Decimal` vía asyncpg,
  no `int` — si el modelo de dominio espera `int`, castear explícito en el SQL
  (`SUM(...)::bigint`), no confiar en que herede el tipo de la columna base.
- `LIMIT $n` con el parámetro en `NULL` equivale a "sin límite" en Postgres —
  útil para traer un ranking completo (no solo el top N) cuando se necesita
  calcular la posición de cualquier fila, no solo mostrar las primeras (ver
  `GET_MONTHLY_RANKING_SQL` en `activity/infrastructure/output/postgres/utils/constants.py`).
  Para calcular solo la posición de UN usuario es más eficiente usar
  `RANK() OVER (...)` en SQL en vez de traer el ranking completo (ver
  `get_position`/`get_monthly_stats` en `points`/`activity`).
- **Nunca hacer check-then-act en dos llamadas separadas** (ej. `SELECT` para ver
  si algo aplica y luego `INSERT/UPDATE` para marcarlo). El bot corre con
  `concurrent_updates=True` (`common/infrastructure/input/tg/bot.py`), así que dos
  updates concurrentes del mismo chat pueden pasar el check antes de que
  cualquiera marque el estado. Hay que fusionarlo en un solo `UPSERT` atómico con
  la condición en el `WHERE` del `DO UPDATE` y `RETURNING` para saber si "ganó":
  `ON CONFLICT (...) DO UPDATE SET ... WHERE <condición> RETURNING ...` — el
  `ON CONFLICT` bloquea la fila antes de evaluar el `WHERE`, así que una segunda
  llamada concurrente ve el valor recién commiteado por la primera y falla la
  condición correctamente en vez de ambas pasar (ver
  `news/infrastructure/output/postgres/adapter/history_adapter.py`, `try_fire`,
  que reemplazó un `is_cooldown_active` + `mark_fired` de dos pasos por
  exactamente este patrón — la constante `TRY_FIRE_SQL` vive en
  `news/infrastructure/output/postgres/utils/constants.py`).

## Identidad de usuario compartida (`group_members`)

Si una feature necesita guardar "algo por usuario en un grupo" (puntos, badges,
warnings, xp, lo que sea), su tabla es angosta — `(chat_id, user_id, <su propio
dato>)` — con `FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id,
user_id)`. El username **nunca** se duplica en la tabla de la feature: vive una
sola vez en `group_members`
(`common/infrastructure/output/postgres/schema/group_members.py`).

- Antes de insertar/actualizar su propia fila, la feature llama
  `upsert_member(conn, chat_id, user_id, username)` (de
  `common/infrastructure/output/postgres/utils/helpers.py`) **dentro de la
  misma transacción**, para garantizar que la fila en `group_members` exista
  antes de que la FK la necesite.
- `group_members` se crea dentro de `init_pool` (`common/.../pool.py`), antes
  de que se resuelva el pool para cualquier feature — así ninguna feature
  puede crear su tabla con la FK antes de que `group_members` exista.
- Para leer el nombre del usuario, la feature hace `JOIN` contra
  `group_members` en sus queries (ver
  `points/infrastructure/output/postgres/adapter/repository_adapter.py` como
  referencia) — nunca vuelve a guardar el username en su propia tabla.
- Si una tabla de una feature ya existente tenía `username` duplicado antes de
  adoptar este patrón, la migración (backfill → drop column → add FK) se hace
  dentro de su propio `schema/<tabla>.py::ensure_schema()`, de forma idempotente
  y sin perder las filas existentes (ver
  `points/infrastructure/output/postgres/schema/autispuntos.py` como ejemplo
  real de esta migración).
- Esta FK solo aplica a datos **por usuario**. Un dato agregado a nivel de
  chat (ej. `chat_activity_timeline`: mensajes por hora/día de la semana del
  grupo entero) NO lleva FK a `group_members` ni pasa por `upsert_member` —
  no tiene `user_id` que referenciar (ver
  `activity/infrastructure/output/postgres/schema/chat_activity_timeline.py`).
