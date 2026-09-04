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
│   │   ├── model/user_info_section.py            # contrato: la sección que cada feature aporta a /usuario_info
│   │   ├── spi/user_info_provider_port.py        # contrato: puerto que implementa cada feature para /usuario_info
│   │   └── spi/group_stats_provider_port.py      # contrato: puerto que implementa cada feature para /stats_grupo
│   └── infrastructure/
│       ├── configuration/settings.py          # env vars globales (token, DB, log level)
│       ├── configuration/logging_config.py     # JSON logging (un log = una línea JSON, para Grafana/Loki)
│       ├── input/tg/{bot,help_handler}.py       # arma la Application de Telegram, registra handlers y el menú "/"
│       ├── input/tg/error_handler.py            # handler global (app.add_error_handler) para excepciones no atrapadas
│       └── output/postgres/
│           ├── pool.py                            # pool de asyncpg ÚNICO, compartido por todas las features
│           ├── schema.py                           # crea group_members (identidad compartida chat_id+user_id)
│           └── members.py                          # upsert_member(conn, chat_id, user_id, username)
├── user_info/                    # feature normal que AGREGA lo que otras features exponen (sin persistencia propia)
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

Las reglas detalladas por tema viven en `.claude/rules/` y cargan solo cuando se
toca un archivo de esa área (no consumen contexto el resto del tiempo):

- `domain-architecture.md` — pureza de `domain/`, shared kernel de `common/`, nombres de carpetas/archivos.
- `configuration.md` — settings.py (env vars) vs. constants.py (hardcoded).
- `dependency-injection.md` — patrón de containers, `providers.Dependency()`, wiring.
- `postgres.md` — credenciales, gotchas de asyncpg, `group_members` (identidad compartida).
- `code-style.md` — idioma, zoneinfo/tzdata.
- `telegram-and-errors.md` — `DomainError`, error handler global, grupos de handlers en PTB.
- `cross-feature-fanout.md` — patrón de `/usuario_info` y `/stats_grupo` (fan-out a providers).

## Checklist para agregar una feature nueva

1. Crear `src/<feature>/{application/bootstrap,domain/{api,model,spi,usecase,utils},infrastructure/{input,output,configuration,utils}}`.
2. Escribir el dominio primero (`model` → `spi` → `api` → `usecase`), sin ningún
   import externo (ver `domain-architecture.md`).
3. Implementar los adapters en `infrastructure/output/<tecnología>/`, y el/los
   entry point(s) en `infrastructure/input/<tecnología>/`.
4. Armar `<Feature>Container` en `application/bootstrap/container.py` (ver
   `dependency-injection.md`). Si necesita el pool de Postgres, `pool = providers.Dependency()`.
5. Registrar el container nuevo en `common/application/bootstrap/container.py`.
6. Registrar los handlers de Telegram en `common/infrastructure/input/tg/bot.py`,
   y agregar los comandos nuevos a `BOT_COMMANDS`.
7. Si agrega comandos o triggers nuevos, actualizar `common/infrastructure/input/tg/help_handler.py`.
8. Actualizar `container.wire(modules=[...])` en `main.py` con el nuevo módulo de
   `infrastructure/input` si usa `@inject`/`Provide`.
9. Si la feature guarda algo por usuario-en-grupo, su tabla lleva FK a
   `group_members` (ver `postgres.md`) — nunca una columna `username` propia.
10. Si tiene sentido, sumar un provider a `/usuario_info` y/o `/stats_grupo`
    (ver `cross-feature-fanout.md`).

## Verificación obligatoria antes de dar algo por terminado

- `python -m compileall src` sin errores.
- Una prueba funcional real (no solo que compile): instanciar el container, resolver
  el usecase, y ejercitarlo — contra la base de datos real cuando la feature la usa,
  no solo con mocks. Limpiar cualquier fila de prueba insertada al terminar.
  - Si el provider depende (directa o indirectamente) de un `providers.Resource`
    async como el pool, hay que **awaitearlo** al resolverlo manualmente
    (`usecase = await container.<feature>.usecase()`), no solo llamarlo.
- Antes de cualquier operación destructiva sobre datos reales (DROP TABLE, DELETE
  sin filtrar bien, etc.), **inspeccionar el contenido primero**, no solo contar
  filas — ya hubo un incidente en este proyecto por confiar en un `count(*)` y
  borrar una tabla que tenía datos reales de uso del bot.
- Si un cambio toca contenido sensible o inusual (por ejemplo el regex de trigger,
  o cualquier texto que no sea obviamente parte de la feature pedida), señalarlo
  explícitamente al usuario en vez de aplicarlo o ignorarlo en silencio.

## Despliegue (Fly.io)

Se despliega como contenedor Docker (`Dockerfile`, imagen `python:3.14-slim`) en
Fly.io (`fly.toml`, app `udea-linux-telegram-bot`, región `gru`). El filesystem
es efímero — nada de estado en archivos locales (nada de SQLite sin disco
persistente). Todo el estado que deba sobrevivir un redeploy vive en Postgres
(Supabase), no en un volumen de Fly. Variables de entorno no sensibles van en
`fly.toml` (`[env]`, ej. `LOG_LEVEL`); secretos (`TELEGRAM_BOT_TOKEN`, `DB_*`)
se configuran con `fly secrets set` — nunca se commitea `.env` (ya está en
`.gitignore`). Como la imagen base es `slim`, aplica el gotcha de
`zoneinfo`/`tzdata` de `code-style.md` — ya está declarado en `requirements.txt`.
