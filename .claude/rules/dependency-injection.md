---
paths:
  - "**/application/bootstrap/container.py"
  - "src/main.py"
---

# DI con dependency-injector

Cada feature tiene su propio `<Feature>Container(DeclarativeContainer)` en
`application/bootstrap/container.py`. `common/application/bootstrap/container.py`
tiene el `ApplicationContainer` raíz que los agrega con `providers.Container(...)`.
Un recurso compartido entre features (como el pool de Postgres) se crea **una sola
vez** en el container raíz y se inyecta a cada feature como
`pool = providers.Dependency()` — nunca cada feature abre su propia conexión/pool
a la misma base de datos.

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
- Un container puede recibir una **lista** de providers de otras features en vez
  de (o además de) el pool — ver `cross-feature-fanout.md` para el patrón completo
  (`user_info` y `/stats_grupo`). Se declara como
  `providers.Dependency(default=[])` si la feature debe seguir funcionando sola
  cuando nadie más aporta nada, y el container que agrega la lista (`ApplicationContainer`)
  debe declararse **después** de todos los containers que contribuyen a ella.
- Al probar un container manualmente (fuera del bot), si el provider que se
  resuelve depende de un `providers.Resource` async (como el pool), hay que
  **awaitearlo** (`usecase = await container.<feature>.usecase()`), no solo
  llamarlo — si no, se obtiene un `Future`/`Task` en vez de la instancia real y
  falla con un `AttributeError` confuso al primer método que se le llame.
