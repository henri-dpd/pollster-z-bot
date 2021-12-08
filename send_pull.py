import json
from os import path
from typing import Text
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from telegram.utils.helpers import DEFAULT_FALSE

TAKEPULLTEXT = 0
BUTTONS = 0

button_entry_points = []

def Pulls_Buttons(update, context):

    group_id = str(update.callback_query.message.chat["id"])
    user_id = str(update.callback_query.from_user.id)
    user_name = update.callback_query.from_user.username
    path = update.callback_query["data"].split("_")
    #path[0] es la encuesta seleccionada, path[1] la opcion de esa encuesta

    pull = path[0]
    options_select = int(path[1])

    with open('data.json', 'r+') as file:
        data = json.load(file)

        if(data["Grupos"][group_id]["Integrantes"].get(user_id, False) == False):
            data["Grupos"][group_id]["Integrantes"][user_id] = {}
        data["Grupos"][group_id]["Integrantes"][user_id]["Usuario"] = user_name
        data["Grupos"][group_id]["Integrantes"][user_id][pull] = options_select
    
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def Add_Callback_Query_Handler(callback_query_handler):
    for i in range(len(button_entry_points)):
        if(button_entry_points[i].pattern == callback_query_handler.pattern):
            return
    button_entry_points.append(callback_query_handler)


def Send_Pull_1(update, context):
    Send_Pull(update, context, 1)

def Send_Pull_3(update, context):
    Send_Pull(update, context, 3)

def Send_Pull_5(update, context):
    Send_Pull(update, context, 5)

def Send_Pull_7(update, context):
    Send_Pull(update, context, 7)

def Send_Pull_10(update, context):
    Send_Pull(update, context, 10)

def Send_Pull(update, context, number_of_questions = 0):

    if(update.callback_query.message.chat["type"] == "group"):
        
        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.callback_query.message.chat["id"])
            user_id = str(update.callback_query.from_user.id)

            if(data["Grupos"].get(group_id, False) != False and user_id in data["Grupos"][group_id]["Administradores"]):

                actual_question = data["Grupos"][group_id]["Pregunta Actual"]

                questions = data["Preguntas"]

                for i in range(number_of_questions):

                    actual_question = actual_question + 1

                    if(actual_question == 59):
                        actual_question = 0
                    
                    Add_Callback_Query_Handler(CallbackQueryHandler(pattern = str(actual_question) + "_1", callback=Pulls_Buttons))
                    Add_Callback_Query_Handler(CallbackQueryHandler(pattern = str(actual_question) + "_2", callback=Pulls_Buttons))
                    Add_Callback_Query_Handler(CallbackQueryHandler(pattern = str(actual_question) + "_3", callback=Pulls_Buttons))
                    Add_Callback_Query_Handler(CallbackQueryHandler(pattern = str(actual_question) + "_4", callback=Pulls_Buttons))

                    pull_text = questions[actual_question]["Pregunta"] +"\n\n"
                    
                    buttons = [[InlineKeyboardButton(
                        text = "Completamente en Desacuerdo",
                        callback_data = (str(actual_question) + "_1"))],

                        [InlineKeyboardButton(
                        text = "Moderadamente en Desacuerdo",
                        callback_data = (str(actual_question) + "_2"))],

                        [InlineKeyboardButton(
                        text = "Moderadamente de Acuerdo",
                        callback_data = (str(actual_question) + "_3"))],

                        [InlineKeyboardButton(
                        text = "Completamente de Acuerdo",
                        callback_data = (str(actual_question) + "_4"))]
                        ]
                    update.callback_query.message.reply_text(
                        text = pull_text,
                        reply_markup = InlineKeyboardMarkup(buttons))

                data["Grupos"][group_id]["Pregunta Actual"] = actual_question

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()