---
paths:
  - "src/user_info/**"
  - "src/activity/**"
  - "src/common/domain/spi/**"
  - "src/*/domain/usecase/*_provider.py"
---

# Fan-out entre features: `/usuario_info` y `/stats_grupo`

Dos comandos transversales agregan datos que aportan varias features. Ambos
siguen el mismo patrón: el CONTRATO (puerto) vive en `common/domain/` porque
todas las features lo implementan/consumen, pero la AGREGACIÓN en sí no vive
en `common` — `common` es solo para lo transversal, no para dueños de features.

## `/usuario_info` (agrega, no reemplaza — feature propia `user_info/`)

- `common/domain/spi/user_info_provider_port.py` define `UserInfoProviderPort`
  (`get_section(chat_id, user_id, username) -> UserInfoSection | None`, `None`
  si la feature no tiene nada que mostrar para ese usuario) y
  `common/domain/model/user_info_section.py` define `UserInfoSection` — son
  los únicos dos archivos de `/usuario_info` que están en `common`, porque son
  el contrato que otras features importan.
- `user_info/domain/usecase/user_info_usecase.py` (`UserInfoUsecase`) recibe
  una `list[UserInfoProviderPort]` en el constructor y llama a todos en
  paralelo (`asyncio.gather`); si un provider individual lanza excepción, esa
  sección se omite (se loguea) en vez de tumbar toda la respuesta — mismo
  criterio de "degradar en vez de fallar todo" que usa `RssFeedAdapter` con
  feeds individuales. `user_info/domain/api/user_info_service.py` y
  `user_info/infrastructure/input/tg/msg_handler.py` completan la feature;
  no tiene `infrastructure/output/` propio porque no persiste nada, solo
  agrega lo que otras features ya calcularon.
- Cada feature que tiene datos por usuario implementa su propio provider en
  su **propio** `domain/usecase/` (ej.
  `points/domain/usecase/points_user_info_provider.py`), envolviendo su
  propio `<Feature>Service` — no accede a otra feature ni a Postgres
  directamente, así que sigue siendo domain puro (ver `domain-architecture.md`).
  No termina en `_usecase` porque no es el caso de uso principal de la
  feature, sino un adapter de un puerto ajeno (`common.domain.spi`).
- El container de cada feature expone `user_info_provider =
  providers.Factory(<Feature>UserInfoProvider, ...)`. El `ApplicationContainer`
  raíz los agrega con `providers.List(points.user_info_provider,
  activity.user_info_provider, ...)` y se lo inyecta a `UserInfoContainer`
  como `providers.Container(UserInfoContainer, info_providers=user_info_providers)`
  — el mismo patrón que usa `pool` para inyectarse a cada feature, solo que
  aquí lo que se inyecta es la lista de providers en vez del pool.
- **Al agregar una feature nueva con datos por usuario**: si tiene sentido
  mostrarla en `/usuario_info`, agregar su provider a `user_info_providers` en
  el `ApplicationContainer`.

## `/stats_grupo` (mismo patrón, pero a nivel de chat — sigue siendo dueño de `activity`)

A diferencia de `/usuario_info`, `/stats_grupo` sigue siendo dueño de una sola
feature (`activity`, que ya calcula sus propios números) — otras features
solo le APORTAN una línea extra, no lo reemplazan:

- `common/domain/spi/group_stats_provider_port.py` define
  `GroupStatsProviderPort` (`get_group_stat_line(chat_id) -> str | None`).
  Es el único archivo de este mecanismo que vive en `common` — el contrato.
- Cualquier feature que quiera aportar una línea (ej. `polls`) implementa este
  puerto en su propio `domain/usecase/` (`polls_group_stats_provider.py`),
  envolviendo su propio `<Feature>Service` — igual regla que en `user_info`:
  domain puro, sin acceder a otra feature.
- `ActivityUsecase` recibe `group_stats_providers: list[GroupStatsProviderPort]`
  (default `[]` si no se inyecta ninguno) y hace `asyncio.gather` sobre ellos
  igual que `UserInfoUsecase`, agregando las líneas no-`None` a
  `GroupStats.extra_lines`. Que `activity` dependa de este puerto de `common`
  no rompe la regla de pureza de dominio (es la misma excepción del shared kernel).
- El `ApplicationContainer` raíz arma `group_stats_providers =
  providers.List(polls.group_stats_provider, ...)` **antes** de construir
  `activity` (`activity = providers.Container(ActivityContainer, pool=db_pool,
  group_stats_providers=group_stats_providers)`) — el container que agrega la
  lista siempre debe declararse después de todos los que contribuyen a ella.
  `ActivityContainer` expone `group_stats_providers = providers.Dependency(default=[])`
  para que siga funcionando sola si nadie más aporta nada.
- **Al agregar una feature nueva que quiera sumar una línea a `/stats_grupo`**:
  implementar `GroupStatsProviderPort`, exponer `group_stats_provider` en su
  container, y agregarlo a la lista en el `ApplicationContainer`.
