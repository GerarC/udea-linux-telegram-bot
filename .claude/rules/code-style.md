---
paths:
  - "src/**/*.py"
---

# Idioma y estilo de código

Todo el código (identificadores, comentarios, docstrings) en inglés. Única
excepción intencional: texto de cara al usuario en español (mensajes del bot,
palabras del regex de trigger, etiquetas de nivel) porque el bot atiende un
grupo hispanohablante — eso se queda en español y se documenta con un
comentario `NOTE:` explicando por qué.

- Si una regla de negocio necesita hora/fecha en **hora local del grupo**
  (ej. "hora pico de actividad"), usar `zoneinfo.ZoneInfo("America/Bogota")`
  (stdlib, sigue siendo domain puro) en vez de UTC — pero `zoneinfo` depende
  de una base de datos de zonas horarias que Windows NO trae, y algunas
  imágenes Docker mínimas (`slim`, Alpine) tampoco. Hay que declarar
  `tzdata` en `requirements.txt` como dependencia (no se importa directo en
  el código, `zoneinfo` la descubre sola) para que funcione en cualquier
  entorno. La zona horaria en sí es una constante de negocio
  (`domain/utils/constants.py`), configurable por env var igual que
  cualquier otro límite (ver `activity/infrastructure/configuration/settings.py`).
