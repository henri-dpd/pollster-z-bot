
import json
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

TAKEPULLTEXT = 0
ENDCREATEPULL = 1

def CreatePull(update, context):
    update.callback_query.message.reply_text("Creemos Pull, primero enviame el enunciado, luego empieza a enviar opciones y para terminar el comando /finish")
    with open('data.json', 'r+') as file:
        data = json.load(file)
        users = data["users"]
        if not(update.callback_query.message.chat["first_name"] in users) or not("pulls" in users[update.callback_query.message.chat["first_name"]]):
            users[update.callback_query.message.chat["first_name"]] = {"pulls":[]}
        users[update.callback_query.message.chat["first_name"]]["pulls"].append({"text":"", "options":[]})
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    return TAKEPULLTEXT


def TakePullText(update, context):
    if(update.message.text == "/finish"):
        update.message.reply_text("Pull terminada")
        SendPull(update, context)
        return ENDCREATEPULL

    with open('data.json', 'r+') as file:
            data = json.load(file)
            users = data["users"]
            
            if users[update.message.chat["first_name"]]["pulls"][0]["text"] == "":
                update.message.reply_text("Texto de la pull: " + update.message.text)
                users[update.message.chat["first_name"]]["pulls"][0]["text"] = update.message.text
            else:
                users[update.message.chat["first_name"]]["pulls"][0]["options"].append({"text":update.message.text, "votes":0})
            
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    return TAKEPULLTEXT




def SendPull(update, context):   
    with open('data.json', 'r+') as file:
        data = json.load(file)
        users = data["users"]
        myUser = users[update.message.chat["first_name"]]
        myPull = myUser["pulls"][0]
        
        buttons = []
        i = 0
        for options in myPull["options"]:
            i = i + 1
            buttons.append([InlineKeyboardButton(
                text = options["text"] + " option:" + str(i),
                callback_data= ("Option " + str(i)) 
            )])
        
        update.message.reply_text(
            text = myPull["text"],
            reply_markup = InlineKeyboardMarkup(buttons)
        )

        users[update.message.chat["first_name"]]["pulls"] = [] 
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    return ENDCREATEPULL