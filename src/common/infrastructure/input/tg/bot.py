from telegram.ext import Application, MessageHandler, filters

from news.infrastructure.input.tg.msg_handler import on_message


def build_application(token: str) -> Application:
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    return app
