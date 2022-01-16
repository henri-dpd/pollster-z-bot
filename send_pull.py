import json
from os import path
from typing import Text
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from telegram.utils.helpers import DEFAULT_FALSE

TAKEPULLTEXT = 0
BUTTONS = 0
RESTART_PULL = 0

button_entry_points = []

def Restart_Pull(update, context):

    if(update.message.chat["type"] == "group" or update.message.chat["type"] == "supergroup"):
        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.message.chat["id"])

            if(data["Grupos"].get(group_id, False) != False):

                user_id = str(update.message.from_user.id)
                username = str(update.message.from_user.username)

                verification = data["Grupos"][group_id]["Usuarios"].get(username, False)

                if(verification == -1):
                    data["Grupos"][group_id]["Usuarios"][username] = user_id
                    data["Grupos"][group_id]["Administradores"].append(user_id)

                if(user_id in data["Grupos"][group_id]["Administradores"]):
                    
                    actual_question = data["Grupos"][group_id]["Pregunta Actual"]

                    if(actual_question == 60):
                        data["Grupos"][group_id]["Pregunta Actual"] = 0
                        update.message.reply_text("Encuesta reiniciada :)")
                    else:
                        if(data["Grupos"][group_id]["Reiniciar Encuesta"] == 0):
                            data["Grupos"][group_id]["Reiniciar Encuesta"] = 1
                            update.message.reply_text("Todas las preguntas no han sido mostradas, \n" +
                            "Está seguro que quiere reiniciarlas?, de estarlo active el comando de nuevo.")
                        else:
                            data["Grupos"][group_id]["Pregunta Actual"] = 0
                            data["Grupos"][group_id]["Reiniciar Encuesta"] = 0
                            update.message.reply_text("Encuesta reiniciada :)")


                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()

def Pulls_Buttons(update, context):

    group_id = str(update.callback_query.message.chat["id"])
    user_id = str(update.callback_query.from_user.id)
    user_name = update.callback_query.from_user.username
    path = update.callback_query["data"].split("_")
    #path[0] es la encuesta seleccionada, path[1] la opción de esa encuesta

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


def Add_Pull_Callback_Query_Handler():
    for i in range(60):
        for j in range(4):
            button_entry_points.append(
                CallbackQueryHandler(pattern = str(i + 1) + "_" + str(j + 1), callback=Pulls_Buttons))


def Send_Pull_1(update, context):
    Send_Pull(update, context, 1)

def Send_Pull_3(update, context):
    Send_Pull(update, context, 3)

def Send_Pull_5(update, context):
    Send_Pull(update, context, 5)

def Send_Pull_7(update, context):
    Send_Pull(update, context, 7)


def Send_Pull(update, context, number_of_questions = 0):

    if(update.callback_query.message.chat["type"] == "group" or 
       update.callback_query.message.chat["type"] == "supergroup"):
        
        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.callback_query.message.chat["id"])

            if(data["Grupos"].get(group_id, False) != False):

                user_id = str(update.callback_query.from_user.id)
                username = str(update.callback_query.from_user.username)

                verification = data["Grupos"][group_id]["Usuarios"].get(username, False)

                if(verification == -1):
                    data["Grupos"][group_id]["Usuarios"][username] = user_id
                    data["Grupos"][group_id]["Administradores"].append(user_id)


                if(user_id in data["Grupos"][group_id]["Administradores"]):

                    if(len(button_entry_points) == 0):
                        Add_Pull_Callback_Query_Handler()

                    actual_question = data["Grupos"][group_id]["Pregunta Actual"]

                    questions = data["Preguntas"]

                    data["Grupos"][group_id]["Reiniciar Encuesta"] = 0

                    for i in range(number_of_questions):


                        if(actual_question < 60):
                            actual_question = actual_question + 1   
                        
                            pull_text = questions[actual_question]["Pregunta"] +"\n\n"
                        
                            buttons = [[InlineKeyboardButton(
                                text = "Completamente en Desacuerdo",
                                callback_data = (str(actual_question + 1) + "_1"))],

                                [InlineKeyboardButton(
                                text = "Moderadamente en Desacuerdo",
                                callback_data = (str(actual_question + 1) + "_2"))],

                                [InlineKeyboardButton(
                                text = "Moderadamente de Acuerdo",
                                callback_data = (str(actual_question + 1) + "_3"))],

                                [InlineKeyboardButton(
                                text = "Completamente de Acuerdo",
                                callback_data = (str(actual_question + 1) + "_4"))]
                                ]

                            update.callback_query.message.reply_text(
                            text = "Pregunta Número " + str(actual_question) + ":\n" + pull_text,
                            reply_markup = InlineKeyboardMarkup(buttons))

                    data["Grupos"][group_id]["Pregunta Actual"] = actual_question

                    if(actual_question == 60):
                        update.callback_query.message.reply_text("Ya han sido enviadas todas las preguntas :) \n" +
                        "Si desea reiniciarlas por favor toque /reiniciar_preguntas")

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()