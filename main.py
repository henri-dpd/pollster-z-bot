from typing import Text
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from pathlib import Path
from sys import path

path.append(Path(__file__).parent.absolute())

from send_pull import BUTTONS, TAKEPULLTEXT, button_entry_points, SendPull

STARTED = 0
HELP = 0


def start(update, context):
    update.message.reply_text("Hola soy un bot en desarrollo.")
    Show_Buttons(update, context)
    return STARTED


def Show_Buttons(update, context):
    update.message.reply_text(text = "Botones Disponibles del PollsterZBot",
                              reply_markup = InlineKeyboardMarkup([
                                  [InlineKeyboardButton(text = "Mostrar Encuesta", callback_data = "Send Pull")]
                                  ]))

def SendHelp(update, context):
    update.message.reply_text(text = "Hola, este es un bot diseñado para realizar encuestas. Para comenzar presione \start")


if __name__ == '__main__':
    updater = Updater(token='2082442589:AAH3MNzWrZVcqXWkHNBvq5Y0edK15AWWvRM', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('start', start)
        ],
        states={
            STARTED: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('help', SendHelp)
        ],
        states={
            HELP: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern = "Send Pull", callback=SendPull)
        ],
        states={
            TAKEPULLTEXT: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=button_entry_points,
        states={
            BUTTONS: []
        },
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()