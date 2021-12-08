from typing import Text
import json
from os import path
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from pathlib import Path
from sys import path

path.append(Path(__file__).parent.absolute())

from send_pull import BUTTONS, TAKEPULLTEXT, button_entry_points
from send_pull import Send_Pull_1, Send_Pull_3, Send_Pull_5, Send_Pull_7, Send_Pull_10
from data_analisis import analisis, DATA_ANALISIS, Show_Data_Analisis
from assign_administrator import INICIALIZATION, ADD_ADMINISTRATOR, ENTER_ADMINISTRATOR 
from assign_administrator import inicialization, add_administrator, enter_administrator
STARTED = 0
HELP = 0


def start(update, context):
    if(update.message.chat["type"] == "group"):
        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.message.chat["id"])
            user_id = str(update.message.from_user.id)

            if(data["Grupos"].get(group_id, False) != False and user_id in data["Grupos"][group_id]["Administradores"]):
                update.message.reply_text("Hola soy un bot capaz de medir el humor del grupo a partir de una serie de encuestas.")
                Show_Buttons(update, context)


def Show_Buttons(update, context):
    update.message.reply_text(text = "Botones Disponibles del PollsterZBot",
                              reply_markup = InlineKeyboardMarkup([
                                  [InlineKeyboardButton(text = "Mostrar 1 Pregunta", callback_data = "Send_Pull_1")],
                                  [InlineKeyboardButton(text = "Mostrar 3 Preguntas", callback_data = "Send_Pull_3")],
                                  [InlineKeyboardButton(text = "Mostrar 5 Preguntas", callback_data = "Send_Pull_5")],
                                  [InlineKeyboardButton(text = "Mostrar 7 Preguntas", callback_data = "Send_Pull_7")],
                                  [InlineKeyboardButton(text = "Mostrar 10 Preguntas", callback_data = "Send_Pull_10")],
                                  [InlineKeyboardButton(text = "Mostrar Análisis", callback_data = "Show_Data_Analisis")]
                                  ]))

def SendHelp(update, context):
    if(update.message.chat["type"] == "group"):
        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.message.chat["id"])
            user_id = str(update.message.from_user.id)

            if(data["Grupos"].get(group_id, False) != False and user_id in data["Grupos"][group_id]["Administradores"]):
                update.message.reply_text(text = "Hola, soy bot diseñado para realizar encuestas. \n" +
                                                 "Solo puedo ser usado por ciertos elegidos. \n\n" +
                                                 "Mis comandos son: \n" +
                                                 "/Start \n" +
                                                 "/Agregar_Administrador \n" +
                                                 "/Confirmar_Administrador \n"
                                                 
                                                 )



if __name__ == '__main__':
    updater = Updater(token='2082442589:AAH3MNzWrZVcqXWkHNBvq5Y0edK15AWWvRM', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('Iniciar_Bot', inicialization)
        ],
        states={
            INICIALIZATION: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('Start', start)
        ],
        states={
            STARTED: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('Agregar_Administrador', add_administrator)
        ],
        states={
            ADD_ADMINISTRATOR: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('Confirmar_Administrador', enter_administrator)
        ],
        states={
            ENTER_ADMINISTRATOR: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('Ayuda', SendHelp)
        ],
        states={
            HELP: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('Analisis', analisis)
        ],
        states={
            DATA_ANALISIS: []
        },
        fallbacks=[]
    ))


    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern = "Send_Pull_1", callback=Send_Pull_1)
        ],
        states={
            TAKEPULLTEXT: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern = "Send_Pull_3", callback=Send_Pull_3)
        ],
        states={
            TAKEPULLTEXT: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern = "Send_Pull_5", callback=Send_Pull_5)
        ],
        states={
            TAKEPULLTEXT: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern = "Send_Pull_7", callback=Send_Pull_7)
        ],
        states={
            TAKEPULLTEXT: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern = "Send_Pull_10", callback=Send_Pull_10)
        ],
        states={
            TAKEPULLTEXT: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern = "Show_Data_Analisis", callback=Show_Data_Analisis)
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