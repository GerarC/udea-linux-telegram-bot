from telegram import BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from activity.infrastructure.input.tg.msg_handler import most_inactive_command, track_message
from banter.infrastructure.input.tg.msg_handler import cumplido_command, insultar_command
from common.infrastructure.input.tg.error_handler import error_handler
from common.infrastructure.input.tg.help_handler import help_command
from common.infrastructure.input.tg.user_info_handler import user_info_command
from news.infrastructure.input.tg.msg_handler import on_message
from points.infrastructure.input.tg.msg_handler import grant_points_command, my_points_command, ranking_command

BOT_COMMANDS = [
    BotCommand("help", "Muestra qué puede hacer el bot"),
    BotCommand("autispuntos", "Da o quita Autispuntos (reply, solo admins)"),
    BotCommand("autisranking", "Muestra el ranking de Autispuntos"),
    BotCommand("ver_autispuntos", "Muestra tus Autispuntos (o los de alguien, con reply)"),
    BotCommand("insultar", "Insulta (con cariño) a un usuario"),
    BotCommand("cumplido", "Le dice un cumplido a un usuario"),
    BotCommand("mas_desocupados", "Top 5 de quienes más mensajes envían"),
    BotCommand("usuario_info", "Muestra tu información acumulada en el bot (o la de alguien, con reply)"),
]


async def register_commands(app: Application) -> None:
    await app.bot.set_my_commands(BOT_COMMANDS)


def build_application(
    token: str,
    post_init=None,
    post_shutdown=None,
) -> Application:
    builder = Application.builder().token(token)
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
    app.add_handler(CommandHandler("usuario_info", user_info_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_error_handler(error_handler)
    return app
