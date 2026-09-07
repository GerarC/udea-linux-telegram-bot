---
paths:
  - "src/*/domain/**"
  - "src/*/infrastructure/**"
  - "src/*/application/**"
---

# Arquitectura de dominio y estructura de carpetas

1. **`domain/` no importa NUNCA una librería de terceros.** Ni `telegram`, ni
   `feedparser`, ni `asyncpg`, ni `dependency_injector`. Solo stdlib (`re`, `random`,
   `dataclasses`, `typing.Protocol`, etc.), otros módulos del propio `domain/` de esa
   feature, y `common/domain/*` (ver excepción abajo). Si una regla de negocio
   necesita algo externo (DB, HTTP, Telegram), se define como un puerto en
   `domain/spi/` y se implementa en `infrastructure/output/`.
   - **Excepción**: `common/domain/` es el único domain que una feature SÍ puede
     importar — es el "shared kernel" transversal: `DomainError`, y los contratos
     que una feature implementa para aportar a `/usuario_info` o `/stats_grupo`
     (`UserInfoProviderPort`, `UserInfoSection`, `GroupStatsProviderPort` — ver
     `cross-feature-fanout.md`). Solo van a `common/domain/` los CONTRATOS que de
     verdad implementan/consumen varias features — no los usecases que los agregan,
     esos viven en su propia feature. Sigue siendo solo domain puro (sin librerías
     de terceros), así que no rompe la regla de pureza. Ninguna feature importa el
     `domain/` de OTRA feature directamente — solo `common/domain/`.

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

5. **Cada Protocol de `domain/api/` expone UNA sola operación (un método), y
   tiene su propio usecase que la implementa** — nada de agrupar varios
   métodos en un `<Feature>Service` grande, ni siquiera agrupando "por
   responsabilidad" (comando vs. consulta): cada operación es su propio
   Protocol + su propia clase `_usecase`. Ejemplos: `activity` tiene
   `ActivityService.register_message`, `MonthlyRankingService.get_monthly_ranking`,
   `AllTimeRankingService.get_all_time_ranking`, `MonthlyStatsService.get_monthly_stats`,
   `AllTimeStatsService.get_all_time_stats`, `GroupStatsService.get_group_stats` —
   seis Protocols, seis usecases (`ActivityUsecase`, `MonthlyRankingUsecase`,
   `AllTimeRankingUsecase`, `MonthlyStatsUsecase`, `AllTimeStatsUsecase`,
   `GroupStatsUsecase`). Mismo criterio en `points` (`PointsService`,
   `RankingService`, `UserPointsService`, `UserPositionService`), `polls`
   (`PollParserService`, `PollRecorderService`, `PollCountService`,
   `ChatPollCountService`) y `banter` (`InsultService`, `ComplimentService`).
   - **Motivo**: poder revisar el flujo de un handler leyendo una sola clase
     chica, sin código de otras operaciones que no le conciernen.
   - **Nunca un usecase que implemente varios Protocols a la vez** (nada de
     herencia múltiple tipo `class Foo(ServiceA, ServiceB)`). Si un usecase
     necesita el resultado de OTRA operación de la misma feature (ej.
     `PointsUsecase.grant_points` arma un `GrantResult` con el ranking
     actualizado), se le inyecta el usecase de esa otra operación como
     colaborador vía su Protocol (`ranking_service: RankingService` en el
     constructor) — composición, no herencia.
   - Varios usecases de una misma feature SÍ pueden compartir el mismo SPI
     (`ActivityRepositoryPort`, `PointsRepositoryPort`) y lógica utilitaria
     pura común vía funciones de `domain/utils/` (ej.
     `activity/domain/utils/clock.py` para mes actual/anterior,
     `points/domain/utils/leveling.py` para el nivel según puntos) — eso no
     rompe la regla, el problema es solo que UN usecase implemente MÚLTIPLES
     Protocols de entrada.
   - Un adapter que agrega datos de varias operaciones para otro puerto (ej.
     `ActivityUserInfoProvider` para `UserInfoProviderPort`, ver
     `cross-feature-fanout.md`) SÍ puede depender de varios Protocols a la
     vez en su constructor — esa es la forma correcta de combinar
     operaciones, no que un usecase implemente varios Protocols.
   - El container de la feature expone un provider de DI por usecase (ej.
     `monthly_ranking_usecase`, `all_time_ranking_usecase`, ...), todos
     compartiendo el mismo `repository_port`. Cada consumidor
     (`infrastructure/input`, u otro `domain/usecase`) importa y se inyecta
     solo el usecase concreto que necesita, nunca uno "de más" solo porque ya
     estaba ahí.
   - Al agregar una operación nueva a una feature existente: Protocol nuevo +
     usecase nuevo, nunca agregar un método a un Protocol/usecase existente.
