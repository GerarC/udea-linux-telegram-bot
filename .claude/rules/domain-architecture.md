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
