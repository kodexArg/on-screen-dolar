import os
import json
from typing import Tuple
from loguru import logger
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logger.add("logs/bot.log", rotation="500 MB")

# Strings used. Change as you wish.
dialog = {
    "change": "Cambiar",  #  This is the text of the command that preceed the currency to change (startswitch)
    "hello": "Hola!",
    "received": "Mensaje recibido de",
    "bye": "Adios!",
    "changing_prices": "Cambiando tablero de precios",
    "price_updated": "Valor actualizado",
    "currency_not_found": "La moneda no se encuentra en la lista",
    "format_err": "Formato de mensaje incorrecto o la moneda no existe. Se espera: 'Cambiar <moneda> <precio>'",
    "unknown_err": "Error inesperado. No se realizó ningún cambio",
}


class ExchangePriceBoard:
    # TODO: docstring here

    def __init__(self):
        self.prices = {}
        self.load_prices()

    def load_prices(self):
        with open(os.path.join("src", "prices.json"), "r") as file:
            self.prices = eval(file.read())
            logger.info("Prices loaded")
            return self.prices

    def get_prices(self):
        return " ".join(f"{key}:{value}" for key, value in self.prices.items())

    def set_price(self, currency: str, price: str) -> Tuple[bool, str]:
        """Returns a tuple with the result of the operation and a message to send"""
        currency = currency.upper()

        # check if currency is in the list
        if currency not in self.prices.keys():
            return False, f"{currency} {dialog['currency_not_found']}"

        # check if price can be converted to float
        try:
            _ = float(price)
        except ValueError:
            return False, f"{price} {dialog['format_err']}"

        # update price
        self.prices[currency] = f"{price} ARS"

        # overwrite json file
        with open(os.path.join("src", "prices.json"), "w") as file:
            file.write(json.dumps(self.prices))
            logger.info("Prices updated")

        # return the new price
        return True, f"<{currency}> {dialog['price_updated']}: {price} ARS"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(dialog["hello"])


def is_authorized_user(userid: int) -> bool:
    authorized_users = []
    with open("authorized_users.txt", "r") as file:
        authorized_users = file.readlines()
        authorized_users = [int(user.strip()) for user in authorized_users]
        if userid in authorized_users:
            return True
        else:
            return False


async def listener(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO: add docstring here

    user = update.message.from_user
    split_msg = update.message.text.split(" ")

    async def incorrect_format():
        """Common function to handle format issues in the text message"""
        logger.warning(
            f"{dialog['received']} {user.first_name} {user.last_name} ({user.id}): {update.message}"
        )
        await update.message.reply_text(f"{dialog['format_err']} \n {split_msg}")

    # Authorization check
    if not is_authorized_user(user.id):
        return

    # Format check (starts with "Cambiar" and has 3 words)
    if not update.message.text.startswith(dialog["change"]) or len(split_msg) != 3:
        await incorrect_format()
        return

    # Do the change
    epb = ExchangePriceBoard()
    currency = split_msg[1]
    price = split_msg[2]

    # old price
    await update.message.reply_text(
        f"{dialog['changing_prices']} \n {epb.get_prices()}"
    )

    # change price
    set_price_success, message = epb.set_price(currency, price)
    if not set_price_success:
        logger.error(f"Error: {message}")
        await update.message.reply_text(f"Error\n{message}")
        return

    # new price
    await update.message.reply_text(f"{message} \n\n {epb.get_prices()}")


def main() -> None:
    app = (
        ApplicationBuilder()
        .token("6077052079:AAHk1NPF-yyDfrm5fM44VA_LFq-ijI2luLg")
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, listener))
    app.run_polling()


if __name__ == "__main__":
    main()
