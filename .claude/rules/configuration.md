---
paths:
  - "src/*/infrastructure/configuration/**"
  - "src/*/domain/utils/**"
  - "src/*/infrastructure/utils/**"
---

# Separación configuración vs. constantes

- `infrastructure/configuration/settings.py` → SOLO cosas que vienen de env vars
  (con un `load_*_settings()` que valida lo requerido y lanza `SystemExit` si
  falta algo). Nunca hardcodear un valor ahí.
- `<capa>/utils/constants.py` → valores hardcodeados. Si es una regla de negocio
  (umbrales, regex de trigger, cooldown por defecto) va en `domain/utils`; si es
  un detalle de infraestructura (URLs de API, TTL de caché, queries SQL) va en
  `infrastructure/utils`.
- **Dentro de `infrastructure/`, las constantes van anidadas junto a la
  tecnología que las usa**, no en un `infrastructure/utils/constants.py` plano
  a nivel de feature: `infrastructure/output/postgres/utils/constants.py` para
  las queries SQL (ver `postgres.md`), `infrastructure/output/http/utils/constants.py`
  para URLs/timeouts de un adapter HTTP, `infrastructure/output/rss/utils/constants.py`
  si hiciera falta, etc. El `infrastructure/utils/constants.py` plano (sin
  `output/<tech>/` ni `input/<tech>/` en el medio) se reserva para el caso
  poco común de una constante que de verdad usan **varias** tecnologías de la
  misma feature a la vez — ver `news/infrastructure/utils/constants.py`
  (`FEEDS`, `FEED_TTL_SECONDS`), que lo importan tanto
  `infrastructure/configuration/settings.py` (como default) como
  `application/bootstrap/container.py`. Si una constante solo la usa un
  adapter, va junto a ESE adapter, no un nivel más arriba "por si acaso".
