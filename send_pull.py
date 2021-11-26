import json
from os import path
from typing import Text
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from telegram.utils.helpers import DEFAULT_FALSE

TAKEPULLTEXT = 0
BUTTONS = 0


def Pulls_Buttons(update, context):

    group = update.callback_query.message.chat["id"]
    user_name = update.callback_query.message.reply_to_message.from_user.username
    path = update.callback_query["data"].split("_")
    #path[0] es la encuesta seleccionada, path[1] la opcion de esa encuesta

    pull = path[0]
    options_select = int(path[1])

    with open('data.json', 'r+') as file:
        data = json.load(file)

        data["Grupos"][group][user_name][pull] = options_select
        
    
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()
    return BUTTONS



button_entry_points = []

def SendPull(update, context):

    with open('data.json', 'r+') as file:
        data = json.load(file)

        questions = data["Preguntas"]

        new_button_entry_points = []

        for i in range(len(questions)):

            new_button_entry_points.append(CallbackQueryHandler(pattern = str(i) + "_1", callback=Pulls_Buttons))
            new_button_entry_points.append(CallbackQueryHandler(pattern = str(i) + "_2", callback=Pulls_Buttons))
            new_button_entry_points.append(CallbackQueryHandler(pattern = str(i) + "_3", callback=Pulls_Buttons))
            new_button_entry_points.append(CallbackQueryHandler(pattern = str(i) + "_4", callback=Pulls_Buttons))

            pull_text = questions[i]["Pregunta"] +"\n\n"
            
            buttons = [[InlineKeyboardButton(
                text = "Completamente en Desacuerdo",
                callback_data = (str(i) + "_1"))],

                [InlineKeyboardButton(
                text = "Moderadamente en Desacuerdo",
                callback_data = (str(i) + "_2"))],

                [InlineKeyboardButton(
                text = "Moderadamente de Acuerdo",
                callback_data = (str(i) + "_3"))],

                [InlineKeyboardButton(
                text = "Completamente de Acuerdo",
                callback_data = (str(i) + "_4"))]
                ]

            update.callback_query.message.reply_text(
                text = pull_text,
                reply_markup = InlineKeyboardMarkup(buttons))
                

        button_entry_points = new_button_entry_points

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    return TAKEPULLTEXT

