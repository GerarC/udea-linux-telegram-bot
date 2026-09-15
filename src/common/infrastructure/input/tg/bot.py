from telegram import BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from activity.infrastructure.input.tg.msg_handler import group_stats_command, most_inactive_command, track_message
from banter.infrastructure.input.tg.msg_handler import cumplido_command, insultar_command
from common.infrastructure.input.tg.error_handler import error_handler
from common.infrastructure.input.tg.help_handler import help_command
from confessions.infrastructure.input.tg.msg_handler import (
    borrar_confesion_command,
    confesar_command,
    confesiones_command,
)
from horoscope.infrastructure.input.tg.msg_handler import horoscopo_command
from news.infrastructure.input.tg.msg_handler import on_message
from package_info.infrastructure.input.tg.msg_handler import paquete_command
from points.infrastructure.input.tg.msg_handler import grant_points_command, my_points_command, ranking_command
from polls.infrastructure.input.tg.msg_handler import encuesta_command
from reminders.infrastructure.input.tg.msg_handler import recordar_command
from user_info.infrastructure.input.tg.msg_handler import gdb_command

BOT_COMMANDS = [
    BotCommand("help", "Muestra qué puede hacer el bot"),
    BotCommand("autispuntos", "Da o quita Autispuntos (reply, solo admins)"),
    BotCommand("autisranking", "Muestra el ranking de Autispuntos"),
    BotCommand("ver_autispuntos", "Muestra tus Autispuntos (o los de alguien, con reply)"),
    BotCommand("insultar", "Insulta (con cariño) a un usuario"),
    BotCommand("cumplido", "Le dice un cumplido a un usuario"),
    BotCommand("mas_desocupados", "Top 5 de quienes más mensajes envían"),
    BotCommand("gdb", "Debuguea tu existencia (o la de alguien, con reply o @usuario)"),
    BotCommand("stats_grupo", "Estadísticas del grupo: mensajes, hora pico, día más activo"),
    BotCommand("encuesta", "Crea una encuesta: /encuesta pregunta | opción1 | opción2"),
    BotCommand("horoscopo", "Muestra el horóscopo del día para un signo"),
    BotCommand("paquete", "Busca un paquete en los repositorios de Arch Linux"),
    BotCommand("recordar", "Programa un recordatorio: /recordar mensaje en N min"),
    BotCommand("confesar", "Publica una confesión anónima"),
    BotCommand("confesiones", "Muestra las últimas confesiones del grupo"),
    BotCommand("borrar_confesion", "Borra una confesión por id (solo admins)"),
]


async def register_commands(app: Application) -> None:
    await app.bot.set_my_commands(BOT_COMMANDS)


def build_application(
    token: str,
    post_init=None,
    post_shutdown=None,
) -> Application:
    # NOTE: concurrent_updates=True runs each update in its own asyncio task instead
    # of processing them one at a time - a slow command (e.g. news' RSS fetch) no
    # longer blocks every other message in the group. Safe here: the only shared
    # in-memory state (RssFeedAdapter's cache) already uses an asyncio.Lock, and
    # everything else goes through the asyncpg pool, which is built for concurrent
    # use (each task gets its own connection, capped by the pool's max_size).
    builder = Application.builder().token(token).concurrent_updates(True)
    if post_init is not None:
        builder = builder.post_init(post_init)
    if post_shutdown is not None:
        builder = builder.post_shutdown(post_shutdown)

    app = builder.build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    # NOTE: separate group so this runs alongside on_message instead of replacing it -
    # PTB only runs the first matching handler per group for a given update.
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_message), group=1)
    app.add_handler(CommandHandler("autispuntos", grant_points_command))
    app.add_handler(CommandHandler("autisranking", ranking_command))
    app.add_handler(CommandHandler("ver_autispuntos", my_points_command))
    app.add_handler(CommandHandler("insultar", insultar_command))
    app.add_handler(CommandHandler("cumplido", cumplido_command))
    app.add_handler(CommandHandler("mas_desocupados", most_inactive_command))
    app.add_handler(CommandHandler("gdb", gdb_command))
    app.add_handler(CommandHandler("stats_grupo", group_stats_command))
    app.add_handler(CommandHandler("encuesta", encuesta_command))
    app.add_handler(CommandHandler("horoscopo", horoscopo_command))
    app.add_handler(CommandHandler("paquete", paquete_command))
    app.add_handler(CommandHandler("recordar", recordar_command))
    app.add_handler(CommandHandler("confesar", confesar_command))
    app.add_handler(CommandHandler("confesiones", confesiones_command))
    app.add_handler(CommandHandler("borrar_confesion", borrar_confesion_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_error_handler(error_handler)
    return app
