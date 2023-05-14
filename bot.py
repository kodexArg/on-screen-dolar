from loguru import logger

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# This dictionary contains the strings this bot uses, so that it can be easily changed for other languages.
common_dialog = {
    "hello": "Hola!",
    "received": "Mensaje recibido de ",
    "bye": "Adios!",
    "changing_prices": "Cambiando tablero de precios"
}

# this dictionary contains the commands to actually change the Exchange Board prices
ebp_commands = ["USD", "USDB", "EUR", "CPL"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(common_dialog["hello"])


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(
        f"{common_dialog['received']} {update.effective_user.first_name}: {update.message.text}"
    )
    user = update.message.from_user
    first_name = user.first_name
    last_name = user.last_name
    message = update.message.text
    id = user.id

    # Check if the user is in the list of authorized users. The list of ids is in the file "authorized_users.txt"
    authorized_users = []
    with open("authorized_users.txt", "r") as file:
        authorized_users = file.readlines()
        authorized_users = [int(user.strip()) for user in authorized_users]
        if id not in authorized_users:
            await update.message.reply_text("No tienes permiso para usar este bot")
            return

app = (
    ApplicationBuilder().token("6077052079:AAHk1NPF-yyDfrm5fM44VA_LFq-ijI2luLg").build()
)
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
app.run_polling()