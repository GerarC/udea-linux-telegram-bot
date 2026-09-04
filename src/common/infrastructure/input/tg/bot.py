from telegram import BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from common.infrastructure.input.tg.help_handler import help_command
from news.infrastructure.input.tg.msg_handler import on_message
from points.infrastructure.input.tg.msg_handler import grant_points_command, my_points_command, ranking_command

BOT_COMMANDS = [
    BotCommand("help", "Muestra qué puede hacer el bot"),
    BotCommand("autispuntos", "Da o quita Autispuntos (reply, solo admins)"),
    BotCommand("autisranking", "Muestra el ranking de Autispuntos"),
    BotCommand("ver_autispuntos", "Muestra tus Autispuntos (o los de alguien, con reply)"),
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
    app.add_handler(CommandHandler("autispuntos", grant_points_command))
    app.add_handler(CommandHandler("autisranking", ranking_command))
    app.add_handler(CommandHandler("ver_autispuntos", my_points_command))
    app.add_handler(CommandHandler("help", help_command))
    return app
