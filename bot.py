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

# Strings this bot uses, so that it can be easily changed for other languages.
dialog = {
    "change": "Cambiar",  #  This is the text of the command that preceed the currency to change (startswitch)
    "hello": "Hola!",
    "received": "Mensaje recibido de ",
    "bye": "Adios!",
    "changing_prices": "Cambiando tablero de precios",
    "price_updated": "Valor actualizado",
    "not_found": "No se encontró el valor",
    "format_error": "Formato de mensaje incorrecto o la moneda no existe. Se espera: 'Cambiar <moneda> <precio>'",
    "error_nothing_changed": "Error inesperado. No se realizón ningán cambio",
}


class ExchangePriceBoard:
    """

    This is an example of the json/dictonary used:
    {
        "DOLAR": "382 ARS",
        "EURO": "293 ARS",
        "PESOS CHILENOS": "3.16 ARS",
        "DOLAR BLUE": "411 ARS"
    }
    """

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
        """
        This method is used to change the price of a currency.
        It returns a tuple with the status of the operation and a message to send to the user.
        """
        # check if currency is in the dictionary
        if currency.capitalize() not in self.prices.keys():
            return False, f"{currency} {dialog['not_found']}"

        # update price
        self.prices[currency] = f"{price} ARS"

        # return the new price
        return True, f"{currency} {dialog['price_updated']}: {price} ARS"


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

    async def incorrect_format():
        """Send a message and log when the format of the message is incorrect."""
        logger.info(
            f"{dialog['received']} {user.first_name} {user.last_name} ({user.id}): {update.message}"
        )
        await update.message.reply_text(
            f"{dialog['format_error']} \n {update.message.text.split(' ')}"
        )

    # Is authorized
    if not is_authorized_user(user.id) or message is None:
        return

    # Exit if message does not start with "Cambiar" or don't have 3 words
    split_msg = update.message.text.split(" ")
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
        await update.message.reply_text(dialog["error_nothing_changed"])
        return
    
    # new price
    await update.message.reply_text(f"{dialog['price_updated']} \n {epb.get_prices()}")


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
