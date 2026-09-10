# udea-linux-telegram-bot

Bot de Telegram para un grupo de la comunidad Linux/Arch — mitad utilidades
reales (paquetes, recordatorios, estadísticas), mitad tono irreverente
(Autispuntos, insultos con cariño, horóscopo). Escrito en Python con
`python-telegram-bot` y `dependency-injector`.

## Comandos

| Comando | Qué hace |
|---|---|
| `/help` | Lista todos los comandos disponibles. |
| `/autispuntos +N` (o `-N`) | Da o quita Autispuntos a quien respondas (reply). Solo admins. |
| `/autisranking` | Ranking de Autispuntos del grupo. |
| `/ver_autispuntos` | Tus Autispuntos, o los de alguien si respondes su mensaje. |
| `/insultar @usuario` | Insulto random (con cariño). Acepta reply o mención; el reply tiene prioridad. |
| `/cumplido @usuario` | Cumplido random. Acepta reply o mención; el reply tiene prioridad. |
| `/paquete nombre` | Busca un paquete en los repositorios de Arch Linux y muestra su descripción. |
| `/recordar mensaje en N min\|horas\|días` | Programa un recordatorio; sobrevive un reinicio del bot. |
| `/mas_desocupados [mes\|total]` | Top 5 de quienes más mensajes envían. |
| `/usuario_info` | Tu información acumulada en el bot (o la de alguien, con reply). |
| `/stats_grupo` | Estadísticas del grupo: mensajes, hora pico, día más activo. |
| `/encuesta pregunta \| opción1 \| opción2` | Crea una encuesta nativa de Telegram. |
| `/horoscopo signo` | Horóscopo del día para un signo (determinístico, no aleatorio). |
| *(pasivo)* | Detecta menciones de noticias de tecnología ("linux", "kubernetes", etc.) y responde con una noticia real (RSS). |

## Arquitectura

Arquitectura hexagonal por feature: cada carpeta bajo `src/<feature>/` tiene
su propio `domain/` (puro, sin dependencias de terceros) e
`infrastructure/` (adapters de Telegram, Postgres, HTTP, etc.), conectados
por inyección de dependencias (`dependency-injector`). El detalle completo —
estructura de carpetas, convenciones de cada capa, y por qué está organizado
así — vive en [`.claude/CLAUDE.md`](.claude/CLAUDE.md) y las reglas en
[`.claude/rules/`](.claude/rules/).

**Stack:**
- [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) (con `JobQueue` para recordatorios)
- [`dependency-injector`](https://python-dependency-injector.ets-labs.org/) para DI
- [`asyncpg`](https://github.com/MagicStack/asyncpg) contra Postgres (Supabase)
- [`httpx`](https://www.python-httpx.org/) para integraciones HTTP externas (ej. la API de paquetes de Arch)
- Logging en JSON (una línea por evento) pensado para Grafana/Loki

## Correrlo localmente

Requiere Python 3.14 y una base de datos Postgres accesible (ej. un proyecto
de Supabase).

```bash
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
```

Crear un `.env` en la raíz (nunca se commitea) con:

```
TELEGRAM_BOT_TOKEN=...
DB_HOST=...
DB_PORT=5432
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
LOG_LEVEL=INFO
```

Y correr:

```bash
python src/main.py
```

El bot crea automáticamente las tablas que necesita en Postgres al arrancar
(no hace falta correr migraciones a mano).

## Despliegue

Se despliega como contenedor Docker en [Fly.io](https://fly.io/)
(`fly.toml`, app `udea-linux-telegram-bot`, región `gru`). El filesystem del
contenedor es efímero — todo el estado que debe sobrevivir un redeploy vive
en Postgres, nunca en disco local. Los secretos (`TELEGRAM_BOT_TOKEN`,
`DB_*`) se configuran con `fly secrets set`; las variables no sensibles
(ej. `LOG_LEVEL`) van en `fly.toml`.
