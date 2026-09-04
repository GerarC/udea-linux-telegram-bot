---
paths:
  - "src/**/infrastructure/output/postgres/**"
---

# Postgres / asyncpg

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
  `activity/infrastructure/output/postgres/repository_adapter.py`). Para calcular
  solo la posición de UN usuario es más eficiente usar `RANK() OVER (...)` en SQL
  en vez de traer el ranking completo (ver `get_position`/`get_monthly_stats` en
  `points`/`activity`).

## Identidad de usuario compartida (`group_members`)

Si una feature necesita guardar "algo por usuario en un grupo" (puntos, badges,
warnings, xp, lo que sea), su tabla es angosta — `(chat_id, user_id, <su propio
dato>)` — con `FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id,
user_id)`. El username **nunca** se duplica en la tabla de la feature: vive una
sola vez en `group_members` (`common/infrastructure/output/postgres/schema.py`).

- Antes de insertar/actualizar su propia fila, la feature llama
  `upsert_member(conn, chat_id, user_id, username)` (de
  `common/infrastructure/output/postgres/members.py`) **dentro de la misma
  transacción**, para garantizar que la fila en `group_members` exista antes
  de que la FK la necesite.
- `group_members` se crea dentro de `init_pool` (`common/.../pool.py`), antes
  de que se resuelva el pool para cualquier feature — así ninguna feature
  puede crear su tabla con la FK antes de que `group_members` exista.
- Para leer el nombre del usuario, la feature hace `JOIN` contra
  `group_members` en sus queries (ver `points/infrastructure/output/postgres/repository_adapter.py`
  como referencia) — nunca vuelve a guardar el username en su propia tabla.
- Si una tabla de una feature ya existente tenía `username` duplicado antes de
  adoptar este patrón, la migración (backfill → drop column → add FK) se hace
  dentro de su propio `ensure_schema()`, de forma idempotente y sin perder las
  filas existentes (ver `points/infrastructure/output/postgres/schema.py` como
  ejemplo real de esta migración).
- Esta FK solo aplica a datos **por usuario**. Un dato agregado a nivel de
  chat (ej. `chat_activity_timeline`: mensajes por hora/día de la semana del
  grupo entero) NO lleva FK a `group_members` ni pasa por `upsert_member` —
  no tiene `user_id` que referenciar (ver
  `activity/infrastructure/output/postgres/schema.py`, tabla `chat_activity_timeline`).
