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
from data_analisis import DATA_ANALISIS,  DATA_ANALISIS_ALL_MEMBER, DATA_ANALISIS_ONE_MEMBER, DATA_DESCRIPTION 
from data_analisis import analisis, Show_Data_Analisis_All_Member, Data_Description
from data_analisis import Show_Data_Analisis_One_Member, Show_Data_Analisis_One_Member_Enter
from assign_administrator import INICIALIZATION, ADD_ADMINISTRATOR 
from assign_administrator import inicialization, add_administrator, enter_administrator
from assign_administrator import REMOVE_ADMINISTRATOR, Remove_administrator, Erase_administrator


STARTED = 0
HELP = 0
SHOW_ANALISIS = 0

def start(update, context):
    print(update)
    if(update.message.chat["type"] == "group"):
        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.message.chat["id"])
            user_id = str(update.message.from_user.id)
            username = str(update.message.from_user.username)

            verification = data["Grupos"][group_id]["Usuarios"].get(username, False)

            if(verification == -1):
                data["Grupos"][group_id]["Usuarios"][username] = user_id
                data["Grupos"][group_id]["Administradores"].append(user_id)


            if(data["Grupos"].get(group_id, False) != False and user_id in data["Grupos"][group_id]["Administradores"]):
                update.message.reply_text("Hola soy un bot capaz de medir el humor del grupo a partir de una serie de encuestas.")
                Show_Pull_Buttons(update, context)

def Show_Pull_Buttons(update, context):
    update.message.reply_text(text = "Botones Disponibles del PollsterZBot",
                              reply_markup = InlineKeyboardMarkup([
                                  [InlineKeyboardButton(text = "Mostrar 1 Pregunta", callback_data = "Send_Pull_1")],
                                  [InlineKeyboardButton(text = "Mostrar 3 Preguntas", callback_data = "Send_Pull_3")],
                                  [InlineKeyboardButton(text = "Mostrar 5 Preguntas", callback_data = "Send_Pull_5")],
                                  [InlineKeyboardButton(text = "Mostrar 7 Preguntas", callback_data = "Send_Pull_7")],
                                  [InlineKeyboardButton(text = "Mostrar 10 Preguntas", callback_data = "Send_Pull_10")]
                                  ]))

def Show_Analisis_Buttons(update, context):
    analisis(update, context)
    update.message.reply_text(text = "Botones Disponibles del PollsterZBot",
                              reply_markup = InlineKeyboardMarkup([
                                  [InlineKeyboardButton(text = "Mostrar Análisis", callback_data = "Show_Data_Analisis_All_Member")],
                                  [InlineKeyboardButton(text = "Mostrar Análisis de un Miembro", callback_data = "Show_Data_Analisis_One_Member")],
                                  [InlineKeyboardButton(text = "Descripción de los Datos", callback_data = "Data_Description")]
                                  ]))


def SendHelp(update, context):
    if(update.message.chat["type"] == "group"):
        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.message.chat["id"])
            user_id = str(update.message.from_user.id)
            username = str(update.message.from_user.username)

            verification = data["Grupos"][group_id]["Usuarios"].get(username, False)

            if(verification == -1):
                data["Grupos"][group_id]["Usuarios"][username] = user_id
                data["Grupos"][group_id]["Administradores"].append(user_id)

            if(data["Grupos"].get(group_id, False) != False and user_id in data["Grupos"][group_id]["Administradores"]):
                update.message.reply_text(text = "Hola, soy bot diseñado para realizar encuestas. \n" +
                                                 "Solo puedo ser usado por ciertos elegidos. \n\n" +
                                                 "Mis comandos son: \n" +
                                                 "/Start \n" +
                                                 "/Agregar_Administrador \n" +
                                                 "/Mostrar Análisis \n"
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
            CommandHandler('Mostrar_Analisis', Show_Analisis_Buttons)
        ],
        states={
            SHOW_ANALISIS: []
        },
        fallbacks=[]
    ))

    
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('Agregar_Administrador', add_administrator)
        ],
        states={
            ADD_ADMINISTRATOR: [MessageHandler(Filters.text, enter_administrator)]
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('Eliminar_Administrador', Remove_administrator)
        ],
        states={
            REMOVE_ADMINISTRATOR: [MessageHandler(Filters.text, Erase_administrator)]
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
            CallbackQueryHandler(pattern = "Show_Data_Analisis_All_Member", callback=Show_Data_Analisis_All_Member)
        ],
        states={
            DATA_ANALISIS_ALL_MEMBER: []
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern = "Show_Data_Analisis_One_Member", callback=Show_Data_Analisis_One_Member)
        ],
        states={
            DATA_ANALISIS_ONE_MEMBER: [MessageHandler(Filters.text, Show_Data_Analisis_One_Member_Enter)]
        },
        fallbacks=[]
    ))


    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern = "Data_Description", callback=Data_Description)
        ],
        states={
            DATA_DESCRIPTION: []
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