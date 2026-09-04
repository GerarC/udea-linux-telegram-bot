---
paths:
  - "src/**/infrastructure/input/**"
  - "src/**/domain/error/**"
---

# Errores de dominio y handlers de Telegram

## Errores de dominio con mensaje de usuario

`DomainError` (`common/domain/error/domain_error.py`) acepta un
`user_message: str | None` opcional en el constructor. Hay un `error_handler`
global (`common/infrastructure/input/tg/error_handler.py`, registrado con
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
  puntual en el handler solo se justifica en dos casos: (a) el mensaje de
  error depende de contexto que el handler tiene y la excepción no (ver
  `points/infrastructure/input/tg/msg_handler.py`, el catch de
  `TelegramError` al verificar si el usuario es admin), o (b) la acción es
  una limpieza *best-effort* que no debe tumbar el resto del comando si falla
  (ver `polls/infrastructure/input/tg/msg_handler.py`, el catch de
  `TelegramError` al borrar el mensaje de `/encuesta` — requiere que el bot
  sea admin del grupo con permiso de borrar mensajes; si no lo es, la
  encuesta ya se creó bien y el comando no debe fallar por eso).

## Varios handlers sobre el mismo tipo de update (PTB)

`python-telegram-bot` solo ejecuta el primer handler que matchea dentro de un
mismo `group` (default `group=0`); no sigue probando los demás handlers de ese
grupo. Si dos features necesitan reaccionar al mismo tipo de update (ej.
`news.on_message` responde a triggers de texto, `activity.track_message`
cuenta todos los mensajes de texto), hay que registrarlas en `group`s
distintos en `common/infrastructure/input/tg/bot.py`
(`app.add_handler(handler, group=1)`), documentando el porqué con un
`NOTE:` — si no, el segundo handler nunca corre.
