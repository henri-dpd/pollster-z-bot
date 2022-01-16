from typing import Text
import json
from os import path
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

INICIALIZATION = 0
ADD_ADMINISTRATOR = 0
REMOVE_ADMINISTRATOR = 0
SHOW_ADMINISTRATOR = 0

def inicialization(update, context):

    if(update.message.chat["type"] == "group" or update.message.chat["type"] == "supergroup"):
        with open('data.json', 'r+') as file:
            data = json.load(file)

            group_id = str(update.message.chat["id"])

            if(data["Grupos"].get(group_id, False) == False):
                group_name = update.message.chat["title"]
                user_id = str(update.message.from_user.id)
                username = str(update.message.from_user.username)

                with open('data.json', 'r+') as file:
                    data = json.load(file)

                    data["Grupos"][group_id] = {"Integrantes": {}, "Nombre del grupo": group_name, "Pregunta Actual": -1,
                                                "Administradores" : ["707317272", "1067047315", "837165115"], 
                                                "Usuarios": {}, "Nuevo Administrador": 0, "Analisis" : 0,
                                                "Reiniciar Encuesta" : 0}

                    admins = data["Grupos"][group_id]["Administradores"]
                    if not(user_id in admins):
                        data["Grupos"][group_id]["Administradores"].append(user_id)
                        data["Grupos"][group_id]["Usuarios"][username] = user_id

                    update.message.reply_text("El bot ha sido iniciado :) \n" + 
                                              "Tenga cuidado al utilizarlo, nadie sabe " +
                                              "qué secretos esconda...")

                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()


def add_administrator(update, context):

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
                    
                    data["Grupos"][group_id]["Nuevo Administrador"] = user_id
                    update.message.reply_text("Escriba el username del nuevo administrador que desea agregar (con / antes del nombre y sin  @)")            
                    
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    return ADD_ADMINISTRATOR
                else:
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
        
            



def enter_administrator(update, context):

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

                if(user_id == data["Grupos"][group_id]["Nuevo Administrador"]):
                    data["Grupos"][group_id]["Nuevo Administrador"] = 0

                    new_administrator_username = update.message.text

                    if(new_administrator_username[0] != "/"):
                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()
                        return ConversationHandler.END

                    new_administrator_username = new_administrator_username[1:len(new_administrator_username)]

                    if(not(new_administrator_username in data["Grupos"][group_id]["Usuarios"].keys())):
                        data["Grupos"][group_id]["Usuarios"][new_administrator_username] = -1

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

                return ConversationHandler.END            

def Remove_administrator(update, context):

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
                    
                    data["Grupos"][group_id]["Nuevo Administrador"] = user_id
                    update.message.reply_text("Escriba el username del administrador que desea borrar (con / antes del nombre y sin  @)")            
                    
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    return ADD_ADMINISTRATOR
                else:
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
            
            



def Erase_administrator(update, context):

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

                if(user_id == data["Grupos"][group_id]["Nuevo Administrador"]):
                    data["Grupos"][group_id]["Nuevo Administrador"] = 0

                    administrator_username = update.message.text

                    if(administrator_username[0] != "/"):
                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()
                        return ConversationHandler.END

                    administrator_username = administrator_username[1:len(administrator_username)]

                    if(administrator_username in data["Grupos"][group_id]["Usuarios"].keys()):
                        administrator_id = data["Grupos"][group_id]["Usuarios"][administrator_username]
                        if(administrator_username != -1):
                            data["Grupos"][group_id]["Usuarios"]["Administradores"].remove(administrator_username)
                        del(data["Grupos"][group_id]["Usuarios"][administrator_username])

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

                return ConversationHandler.END            

def Show_Administrators(update, context):
    
    if(update.message.chat["type"] == "group" or 
       update.message.chat["type"] == "supergroup"):
        
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
                    
                    administrators = data["Grupos"][group_id]["Usuarios"].keys()
                    text = ""
                    for i in administrators:
                        text = str(i) + "\n"
                    if(text == ""):
                        update.message.reply_text("Solo los dioses son administradores de este grupo")
                    else:
                        update.message.reply_text("Los administratores del bot en este grupo son: \n" + text)
                
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
