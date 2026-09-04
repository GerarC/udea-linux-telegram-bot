from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

HELP_TEXT = """\
🤖 <b>¿Qué puede hacer este bot?</b>

📰 <b>Noticias de tecnología</b> — <i>cualquiera</i>
Menciona en el chat algo como "noticias de tech", "inteligencia artificial", \
"devops", "kubernetes", "linux", etc. y el bot responde con una noticia. \
Tiene un cooldown por chat entre respuestas.

🧠 <b>/autispuntos +N</b> (o -N) — <i>solo admins del grupo</i>
Responde (reply) al mensaje de la persona a quien le quieres dar o quitar \
Autispuntos. Ej: responder con <code>/autispuntos +3</code>.

🏆 <b>/autisranking</b> — <i>cualquiera</i>
Muestra el ranking de Autispuntos del grupo.

🔍 <b>/ver_autispuntos</b> — <i>cualquiera</i>
Muestra cuántos Autispuntos tienes. Si respondes (reply) al mensaje de otra \
persona, muestra los de ella en vez de los tuyos.

❓ <b>/help</b> — <i>cualquiera</i>
Muestra este mensaje.\
"""


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(HELP_TEXT, parse_mode=ParseMode.HTML)
