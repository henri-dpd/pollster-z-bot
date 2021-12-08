from typing import Text
import json
from os import path
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

INICIALIZATION = 0
ADD_ADMINISTRATOR = 0
ENTER_ADMINISTRATOR = 0

def inicialization(update, context):

    if(update.message.chat["type"] == "group"):

        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.message.chat["id"])

            if(data["Grupos"].get(group_id, False) == False):
                group_name = update.message.chat["title"]
                user_id = str(update.message.from_user.id)

                with open('data.json', 'r+') as file:
                    data = json.load(file)

                    data["Grupos"][group_id] = {"Integrantes": {}, "Nombre del grupo": group_name, "Pregunta Actual": 0,
                                                "Administradores" : ["707317272", "1067047315", "837165115"], "Nuevo Administrador": -1}
        
                    admins = data["Grupos"][group_id]["Administradores"]
                    if not(user_id in admins):
                        data["Grupos"][group_id]["Administradores"].append(user_id)

                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()


def add_administrator(update, context):

    if(update.message.chat["type"] == "group"):
        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.message.chat["id"])
            user_id = str(update.message.from_user.id)
            
            if(data["Grupos"].get(group_id, False) != False and user_id in data["Grupos"][group_id]["Administradores"]):
                data["Grupos"][group_id]["Nuevo Administrador"] = 1

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()



def enter_administrator(update, context):
    
    if(update.message.chat["type"] == "group"):
        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.message.chat["id"])
            user_id = str(update.message.from_user.id)
            
            if(data["Grupos"].get(group_id, False) != False and data["Grupos"][group_id]["Nuevo Administrador"] == 1):
                data["Grupos"][group_id]["Nuevo Administrador"] = 0
                if(not(user_id in data["Grupos"][group_id]["Administradores"])):
                    data["Grupos"][group_id]["Administradores"].append(user_id)

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()