import logging
import re
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Expresiones regulares para detectar mensajes
expresion_regular = re.compile(r"\bhola\b", re.IGNORECASE)
expresion_menu = re.compile(r"\bmenu\b", re.IGNORECASE)
expresion_si = re.compile(r"\bsi\b", re.IGNORECASE)
expresion_no = re.compile(r"\bno\b", re.IGNORECASE)
expresion_deli = re.compile(r"\bdeli\b", re.IGNORECASE)  # Corregido aquí
expresion_gracias = re.compile(r"\bgracias\b", re.IGNORECASE)
expresion_adios = re.compile(r"\badios\b", re.IGNORECASE)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and respond accordingly."""
    message_text = update.message.text
    response = "No entendí tu mensaje."

    if expresion_regular.search(message_text):
        response = "¡Hola! Bienvenido a tu restaurante favorito. ¿En qué te puedo ayudar?"
    elif expresion_menu.search(message_text):
        response = "Hoy únicamente contamos con el menú especial. ¿Le gustaría ordenar?"
    elif expresion_si.search(message_text):
        response = "Proporcione su dirección completa para que nuestro repartidor llegue a su casa."
    elif expresion_no.search(message_text):
        response = "Una lástima, usted se lo pierde."
    elif expresion_deli.search(message_text):
        response = "Excelente, ¡disfruta tu comida!"
    elif expresion_gracias.search(message_text):
        response = "¡Estamos para servirte!"
    elif expresion_adios.search(message_text):
        response = "¡Adiós! Esperamos verte pronto."

    await update.message.reply_text(response)
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"¡Hola {user.mention_html()}! Bienvenido a tu restaurante favorito. Usa /help para obtener ayuda.",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "Comandos disponibles:\n"
        "/start - Iniciar conversación\n"
        "/help - Mostrar esta ayuda\n"
        "También puedes escribir:\n"
        "- 'Hola' para un saludo\n"
        "- 'Menu' para conocer el menú del día\n"
        "- 'Si' para confirmar una acción\n"
        "- 'No' para rechazar una acción\n"
        "- 'deli' para disfrutar tu comida\n"
        "- 'Gracias' para agradecer\n"
        "- 'Adios' para despedirte"
    )
    await update.message.reply_text(help_text)

def main() -> None:
    """Start the bot."""
    application = Application.builder().token("6633774921:AAG8rWcnQopD5IQe4U11HYNIUrlkliiqcis").build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
