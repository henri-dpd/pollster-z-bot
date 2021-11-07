
import json
from os import path
from typing import Text
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from telegram.utils.helpers import DEFAULT_FALSE

TAKEPULLTEXT = 0
ENDCREATEPULL = 1
BUTTONS = 0

button_entry_points = []

def Pulls_Buttons(update, context):

    path = update.callback_query["data"].split("_")
    # 0: user, 1: "pulls", 2: actual pull, 3: actual option
    actual_user = path[0]
    actual_pull = path[2]
    actual_option = path[3]

    with open('data.json', 'r+') as file:
        data = json.load(file)
        users = data["users"]
        actual_vote = users[actual_user]["pulls"][path[2]]["options"][int(actual_option) - 1]["votes"]
        users[actual_user]["pulls"][path[2]]["options"][int(actual_option) - 1]["votes"] = actual_vote + 1
        
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    return BUTTONS

        


def CreatePull(update, context):
    update.callback_query.message.reply_text("Creemos un Pull, primero enviame el enunciado, luego empieza a enviar opciones y para terminar el comando /finish")
    with open('data.json', 'r+') as file:
        data = json.load(file)

        if data.get("users", False) == False:
            data["users"] = {}

        users = data["users"]
        if not(update.callback_query.message.chat["first_name"] in users) or not("pulls" in users[update.callback_query.message.chat["first_name"]]):
            users[update.callback_query.message.chat["first_name"]] = {"pulls": {"max" : 0}}
            
        max = users[update.callback_query.message.chat["first_name"]]["pulls"]["max"] + 1
        users[update.callback_query.message.chat["first_name"]]["pulls"]["max"] = max

        users[update.callback_query.message.chat["first_name"]]["pulls"][str(max)] = {"text": "", "options" : []}

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    return TAKEPULLTEXT


def TakePullText(update, context):
    if(update.message.text == "/finish"):
        update.message.reply_text("Pull terminada")
        SendPull(update, context)
        return TAKEPULLTEXT

    with open('data.json', 'r+') as file:
            data = json.load(file)
            users = data["users"]
            all_user_pulls = users[update.message.chat["first_name"]]["pulls"]
            max = all_user_pulls["max"]
            actual_pull = all_user_pulls[str(max)]

            if actual_pull["text"] == "":
                update.message.reply_text("Ahora por favor escriba las opciones en mensajes diferentes. Toque /finish para terminar")
                actual_pull["text"] = update.message.text
            else:
                actual_pull["options"].append({"option_text":update.message.text, "votes":0})
            
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    return TAKEPULLTEXT




def SendPull(update, context):
    with open('data.json', 'r+') as file:
        data = json.load(file)
        users = data["users"]
        all_user_pulls = users[update.message.chat["first_name"]]["pulls"]
        max = all_user_pulls["max"]
        actual_pull = all_user_pulls[str(max)]

        complete_text = actual_pull["text"]
        complete_text = complete_text + "\n\n"

        callback_path = update.message.chat["first_name"] + "_"
        callback_path = callback_path + "pulls" + "_"
        callback_path = callback_path + str(max) + "_"

        buttons = []
        i = 0
        for options in actual_pull["options"]:
            i = i + 1
            complete_text = complete_text + "Opción # " + str(i) + ":\n" + options["option_text"] + "\n\n\n"
            buttons.append([InlineKeyboardButton(
                text = "Opción # " + str(i),
                callback_data = (callback_path + str(i))
            )])

            button_entry_points.append(CallbackQueryHandler(pattern = callback_path + str(i), callback=Pulls_Buttons))
        
        update.message.reply_text(
            text = complete_text,
            reply_markup = InlineKeyboardMarkup(buttons)
        )
 
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    return ENDCREATEPULL