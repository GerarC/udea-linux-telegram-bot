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
  un detalle de infraestructura (URLs de feeds, TTL de caché) va en
  `infrastructure/utils`.
