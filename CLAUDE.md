# Arquitectura del proyecto

Bot de Telegram en Python (`python-telegram-bot` + `dependency-injector`), organizado
en **arquitectura hexagonal por feature**. Cada feature es una carpeta independiente
bajo `src/` con la misma forma interna; `common/` es lo único transversal a todas.

```
src/
├── main.py                      # composition root: carga settings, arma el container raíz, arranca el bot
├── common/                      # transversal a todas las features
│   ├── application/bootstrap/container.py   # ApplicationContainer: agrega los containers de cada feature
│   ├── domain/                                # "shared kernel": el único domain que otras features pueden importar
│   │   ├── error/domain_error.py                # excepción base compartida (con user_message opcional)
│   │   ├── api/user_info_service.py              # puerto de entrada de /info_usuario
│   │   ├── model/{user_info,user_info_section}.py  # entidades de /info_usuario
│   │   ├── spi/user_info_provider_port.py        # puerto que implementa cada feature para aportar a /info_usuario
│   │   └── usecase/user_info_usecase.py           # hace fan-out a todos los providers registrados
│   └── infrastructure/
│       ├── configuration/settings.py          # env vars globales (token, DB, log level)
│       ├── configuration/logging_config.py     # JSON logging (un log = una línea JSON, para Grafana/Loki)
│       ├── input/tg/{bot,help_handler}.py       # arma la Application de Telegram, registra handlers y el menú "/"
│       ├── input/tg/error_handler.py            # handler global (app.add_error_handler) para excepciones no atrapadas
│       ├── input/tg/user_info_handler.py        # comando /info_usuario
│       └── output/postgres/
│           ├── pool.py                            # pool de asyncpg ÚNICO, compartido por todas las features
│           ├── schema.py                           # crea group_members (identidad compartida chat_id+user_id)
│           └── members.py                          # upsert_member(conn, chat_id, user_id, username)
└── <feature>/
    ├── application/bootstrap/container.py   # DI: arma adapters + usecase de ESTA feature
    ├── domain/
    │   ├── api/<algo>_service.py              # puerto de entrada (Protocol) — lo que expone el dominio
    │   ├── model/<algo>.py                    # entidades (dataclasses)
    │   ├── spi/<algo>_port.py                  # puertos de salida (Protocol) — lo que el dominio necesita
    │   ├── usecase/<feature>_usecase.py         # implementación del caso de uso
    │   └── utils/constants.py                    # constantes de NEGOCIO hardcodeadas (regex, umbrales, etc.)
    └── infrastructure/
        ├── configuration/settings.py           # SOLO valores que vienen de variables de entorno
        ├── input/<tecnología>/...                # adaptadores driving, agrupados por tecnología (tg/, http/, etc.)
        ├── output/<tecnología>/...                # adaptadores driven, agrupados por tecnología (postgres/, rss/, etc.)
        └── utils/constants.py                       # constantes hardcodeadas propias de infraestructura (URLs, TTLs)
```

## Reglas duras (no negociables)

1. **`domain/` no importa NUNCA una librería de terceros.** Ni `telegram`, ni
   `feedparser`, ni `asyncpg`, ni `dependency_injector`. Solo stdlib (`re`, `random`,
   `dataclasses`, `typing.Protocol`, etc.), otros módulos del propio `domain/` de esa
   feature, y `common/domain/*` (ver excepción abajo). Si una regla de negocio
   necesita algo externo (DB, HTTP, Telegram), se define como un puerto en
   `domain/spi/` y se implementa en `infrastructure/output/`.
   - **Excepción**: `common/domain/` es el único domain que una feature SÍ puede
     importar — es el "shared kernel" transversal (`DomainError`, y los contratos
     de `/info_usuario`: `UserInfoProviderPort`, `UserInfoSection`). Sigue siendo solo
     domain puro (sin librerías de terceros), así que no rompe la regla de pureza.
     Ninguna feature importa el `domain/` de OTRA feature directamente — solo
     `common/domain/`.

2. **`api`, `model`, `spi`, `usecase`, `error`/`exception` son CARPETAS, no archivos.**
   Cada archivo dentro tiene un nombre descriptivo del concepto que contiene
   (`news_service.py`, `news_item.py`, `news_feed_port.py`), nunca `api.py`/`model.py`
   a secas. La clase que implementa el caso de uso termina en `_usecase`
   (`NewsUsecase`, `PointsUsecase`), no `_service_impl`.

3. **`infrastructure/input` consume `domain/api` directamente.** No hay capa
   `application/handler` ni `dto`/`mapper` intermedios — es un paso innecesario. La
   capa `application` de cada feature es solo el **wiring de DI**
   (`application/bootstrap/container.py`), nada más.

4. **`input/` y `output/` se organizan por tecnología**, no por archivo suelto:
   `output/postgres/`, `output/rss/`, `input/tg/`. Así si mañana cambias de RSS a
   otra fuente, o agregas un segundo canal de entrada, no hay ambigüedad de dónde va.

5. **Separación configuración vs. constantes**:
   - `infrastructure/configuration/settings.py` → SOLO cosas que vienen de env vars
     (con un `load_*_settings()` que valida lo requerido y lanza `SystemExit` si
     falta algo). Nunca hardcodear un valor ahí.
   - `<capa>/utils/constants.py` → valores hardcodeados. Si es una regla de negocio
     (umbrales, regex de trigger, cooldown por defecto) va en `domain/utils`; si es
     un detalle de infraestructura (URLs de feeds, TTL de caché) va en
     `infrastructure/utils`.

6. **DI con `dependency-injector`**: cada feature tiene su propio
   `<Feature>Container(DeclarativeContainer)` en `application/bootstrap/container.py`.
   `common/application/bootstrap/container.py` tiene el `ApplicationContainer` raíz
   que los agrega con `providers.Container(...)`. Un recurso compartido entre
   features (como el pool de Postgres) se crea **una sola vez** en el container raíz
   y se inyecta a cada feature como `pool = providers.Dependency()` — nunca cada
   feature abre su propia conexión/pool a la misma base de datos.
   - Si un provider de un container hijo depende del container padre, el `Provide[...]`
     en el punto de inyección debe referenciar el **path completo desde el container
     que efectivamente se wirea** (ej. `Provide[ApplicationContainer.news.usecase]`,
     no `Provide[NewsContainer.usecase]`), o el wiring no resuelve nada en runtime.
   - Si una feature usa una base de datos, la creación de sus tablas va en un
     `providers.Resource` propio (`schema_ready`) dentro de su container — así queda
     garantizado que corre en `container.init_resources()` al arrancar, sin que nada
     tenga que depender explícitamente de él.
   - `container.init_resources()` / `shutdown_resources()` se llaman desde los hooks
     `post_init`/`post_shutdown` de `python-telegram-bot` en `main.py`, porque
     `main()` es síncrono pero esos recursos (pool async) necesitan un loop corriendo.

7. **Credenciales de Postgres como campos separados** (`DB_HOST`, `DB_PORT`,
   `DB_NAME`, `DB_USER`, `DB_PASSWORD`), nunca una sola `DATABASE_URL` armada a mano
   — un password con caracteres especiales (`#`, `&`, `!`) rompe el parseo de URL.
   Y siempre `statement_cache_size=0` en `asyncpg` porque se usa el pooler de
   Supabase (PgBouncer en modo transacción, que no soporta prepared statements).
   - Un `SUM(...)` (u otro agregado) en una query devuelve `Decimal` vía asyncpg,
     no `int` — si el modelo de dominio espera `int`, castear explícito en el SQL
     (`SUM(...)::bigint`), no confiar en que herede el tipo de la columna base.
   - `LIMIT $n` con el parámetro en `NULL` equivale a "sin límite" en Postgres —
     útil para traer un ranking completo (no solo el top N) cuando se necesita
     calcular la posición de cualquier fila, no solo mostrar las primeras (ver
     `activity/infrastructure/output/postgres/repository_adapter.py`).

8. **Identidad de usuario compartida (`group_members`)**: si una feature necesita
   guardar "algo por usuario en un grupo" (puntos, badges, warnings, xp, lo que
   sea), su tabla es angosta — `(chat_id, user_id, <su propio dato>)` — con
   `FOREIGN KEY (chat_id, user_id) REFERENCES group_members (chat_id, user_id)`.
   El username **nunca** se duplica en la tabla de la feature: vive una sola vez
   en `group_members` (`common/infrastructure/output/postgres/schema.py`).
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

9. **Idioma**: todo el código (identificadores, comentarios, docstrings) en inglés.
   Única excepción intencional: texto de cara al usuario en español (mensajes del
   bot, palabras del regex de trigger, etiquetas de nivel) porque el bot atiende
   un grupo hispanohablante — eso se queda en español y se documenta con un
   comentario `NOTE:` explicando por qué.

10. **Errores de dominio con mensaje de usuario**: `DomainError`
    (`common/domain/error/domain_error.py`) acepta un `user_message: str | None`
    opcional en el constructor. Hay un `error_handler` global
    (`common/infrastructure/input/tg/error_handler.py`, registrado con
    `app.add_error_handler(...)` en `bot.py`) que captura cualquier excepción no
    atrapada de cualquier handler de Telegram: si es un `DomainError` con
    `user_message`, responde ese texto y loguea en `warning` (falla esperada); si
    no, responde un mensaje genérico y loguea en `error` con el traceback (falla
    inesperada).
    - Una excepción de dominio de una feature (ej. `FetchingNewsError` en
      `news/domain/error/`) define su propio `user_message` al construirse.
      `common` nunca importa excepciones específicas de una feature — solo conoce
      la base `DomainError`, así se mantiene desacoplado.
    - No hace falta un `try/except` en cada handler de Telegram para los fallos
      esperados de una feature: basta con lanzar la excepción de dominio y dejar
      que el handler global la traduzca a un mensaje de usuario. Un `try/except`
      puntual en el handler solo se justifica cuando el mensaje de error depende
      de contexto que el handler tiene y la excepción no (ver
      `points/infrastructure/input/tg/msg_handler.py`, el catch de
      `TelegramError` al verificar si el usuario es admin).

11. **Varios handlers sobre el mismo tipo de update (PTB)**: `python-telegram-bot`
    solo ejecuta el primer handler que matchea dentro de un mismo `group` (default
    `group=0`); no sigue probando los demás handlers de ese grupo. Si dos features
    necesitan reaccionar al mismo tipo de update (ej. `news.on_message` responde a
    triggers de texto, `activity.track_message` cuenta todos los mensajes de
    texto), hay que registrarlas en `group`s distintos en
    `common/infrastructure/input/tg/bot.py` (`app.add_handler(handler, group=1)`),
    documentando el porqué con un `NOTE:` — si no, el segundo handler nunca corre.

12. **`/info_usuario` (fan-out a providers)**: es el comando transversal que agrega
    info por-usuario de todas las features (Autispuntos, actividad, y lo que se
    agregue). Vive en `common` porque nadie más puede ser dueño de "el resumen de
    todas las features":
    - `common/domain/spi/user_info_provider_port.py` define `UserInfoProviderPort`
      (`get_section(chat_id, user_id, username) -> UserInfoSection | None`, `None`
      si la feature no tiene nada que mostrar para ese usuario).
    - `common/domain/usecase/user_info_usecase.py` (`UserInfoUsecase`) recibe una
      `list[UserInfoProviderPort]` en el constructor y llama a todos en paralelo
      (`asyncio.gather`); si un provider individual lanza excepción, esa sección
      se omite (se loguea) en vez de tumbar toda la respuesta — mismo criterio de
      "degradar en vez de fallar todo" que usa `RssFeedAdapter` con feeds
      individuales.
    - Cada feature que tiene datos por usuario implementa su propio provider en
      su **propio** `domain/usecase/` (ej.
      `points/domain/usecase/points_user_info_provider.py`), envolviendo su
      propio `<Feature>Service` — no accede a otra feature ni a Postgres
      directamente, así que sigue siendo domain puro (ver excepción de la regla 1).
      No termina en `_usecase` porque no es el caso de uso principal de la
      feature, sino un adapter de un puerto ajeno (`common.domain.spi`).
    - El container de cada feature expone `user_info_provider =
      providers.Factory(<Feature>UserInfoProvider, ...)`. El `ApplicationContainer`
      raíz los agrega con `providers.List(points.user_info_provider,
      activity.user_info_provider, ...)` y arma `user_info_usecase =
      providers.Factory(UserInfoUsecase, providers=user_info_providers)`.
    - **Al agregar una feature nueva con datos por usuario**: si tiene sentido
      mostrarla en `/info_usuario`, agregar su provider a esa lista — es el único paso
      extra sobre el checklist normal de abajo.

## Checklist para agregar una feature nueva

1. Crear `src/<feature>/{application/bootstrap,domain/{api,model,spi,usecase,utils},infrastructure/{input,output,configuration,utils}}`.
2. Escribir el dominio primero (`model` → `spi` → `api` → `usecase`), sin ningún
   import externo. Si necesita persistencia, el puerto en `spi` se define ahí
   aunque el adapter real se escriba después.
3. Implementar los adapters en `infrastructure/output/<tecnología>/`, y el/los
   entry point(s) en `infrastructure/input/<tecnología>/`.
4. Armar `<Feature>Container` en `application/bootstrap/container.py`. Si necesita
   el pool de Postgres compartido, declarar `pool = providers.Dependency()`.
5. Registrar el container nuevo en `common/application/bootstrap/container.py`
   (`providers.Container(FeatureContainer, pool=db_pool)` si aplica).
6. Registrar los handlers de Telegram en `common/infrastructure/input/tg/bot.py`,
   y agregar los comandos nuevos a `BOT_COMMANDS` para que aparezcan en el menú "/".
7. Si agrega comandos o triggers nuevos, actualizar `common/infrastructure/input/tg/help_handler.py`.
8. Actualizar `container.wire(modules=[...])` en `main.py` con el nuevo módulo de
   `infrastructure/input` si usa `@inject`/`Provide`.
9. Si la feature guarda algo por usuario-en-grupo, su tabla lleva FK a
   `group_members` (ver regla 8 arriba) — nunca una columna `username` propia.

## Verificación obligatoria antes de dar algo por terminado

- `python -m compileall src` sin errores.
- Una prueba funcional real (no solo que compile): instanciar el container, resolver
  el usecase, y ejercitarlo — contra la base de datos real cuando la feature la usa,
  no solo con mocks. Limpiar cualquier fila de prueba insertada al terminar.
  - Si el provider que se resuelve depende (directa o indirectamente) de un
    `providers.Resource` async como el pool (`db_pool`), hay que **awaitearlo**
    al resolverlo manualmente fuera del bot (`usecase = await
    container.<feature>.usecase()`), no solo llamarlo — si no, se obtiene un
    `Future`/`Task` en vez de la instancia real y falla con un `AttributeError`
    confuso al primer método que se le llame.
- Antes de cualquier operación destructiva sobre datos reales (DROP TABLE, DELETE
  sin filtrar bien, etc.), **inspeccionar el contenido primero**, no solo contar
  filas — ya hubo un incidente en este proyecto por confiar en un `count(*)` y
  borrar una tabla que tenía datos reales de uso del bot.
- Si un cambio toca contenido sensible o inusual (por ejemplo el regex de trigger,
  o cualquier texto que no sea obviamente parte de la feature pedida), señalarlo
  explícitamente al usuario en vez de aplicarlo o ignorarlo en silencio.

## Despliegue (Render)

El filesystem de Render es efímero — nada de estado en archivos locales (nada de
SQLite sin disco persistente). Todo el estado que deba sobrevivir un redeploy vive
en Postgres (Supabase). Variables de entorno se configuran en el panel de Render,
nunca se commitea `.env` (ya está en `.gitignore`).
