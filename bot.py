import os
import json
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


STARTED = 0
READING = 0
NOTREADING = 1
TAKEPULLTEXT = 0
TAKEOPTIONS = 0 
ENDCREATEPULL = 0

def start(update, context):
    update.message.reply_text("Hola soy un bot en desarrollo.")
    SendHelp(update, context)
    return STARTED

def SendHelp(update, context):
    update.message.reply_text("Ayuda de PollsterZBot \n\n Comandos disponibles: \n /help \n /read \n /stop_read \n /write \n /create_pull")

def CreatePull(update, context):    
    update.message.reply_text("Creemos Pull, primero enviame el enunciado")
    with open('data.json', 'r+') as file:
            data = json.load(file)
            users = data["users"]
            if not(update.message.chat["first_name"] in users) or not("pulls" in users[update.message.chat["first_name"]]):
                users[update.message.chat["first_name"]] = {"pulls":[]}
            users[update.message.chat["first_name"]]["pulls"][0].append({"text":"", "options":[]})
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    return TAKEPULLTEXT

def TakePullText(update, context):    
    update.message.reply_text("Texto de la pull: " + update.message.text)
    with open('data.json', 'r+') as file:
            data = json.load(file)
            users = data["users"]
            users[update.message.chat["first_name"]]["pulls"][0]["text"] = update.message.text
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    return TAKEOPTIONS

def TakeOptions(update, context):    
    if(update.message.text == "/finish")
        update.message.reply_text("Pull terminada")
        SendPull(update, context)
        return ENDCREATEPULL
    update.message.reply_text("Creemos Pull, primero enviame el enunciado")
    with open('data.json', 'r+') as file:
            data = json.load(file)
            users = data["users"]
            users[update.message.chat["first_name"]]["pulls"][0]["options"].append({"text":update.message.text, "votes":0})
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    return TAKEOPTIONS


def SendPull(update, context):   
    with open('data.json', 'r+') as file:
        data = json.load(file)
        users = data["users"]
        myUser = users[update.message.chat["first_name"]]
        myPull = myUser["pulls"][0]
        
        buttons = []
        for options in myPull["options"]:
            buttons.append([InlineKeyboardButton(
                text = options["text"]
                url = "google.es"
            )])
        
        update.message.reply_text(
            text = myPull["text"],
            reply_markup = InlineKeyboardMarkup(buttons)
        )        
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    return ENDCREATEPULL

def Read(update, context):
    update.message.reply_text("Estoy leyendo")
    return READING

def inputText(update, context):
    if(update.message.text == '/stop_read'):
        update.message.reply_text("Dejo de leer")
        return NOTREADING
    if(update.message.text == '/create_pull'):
        CreatePull(update, context)
        return NOTREADING
    else:
        with open('data.json', 'r+') as file:
            data = json.load(file)
            users = data["users"]
            if not(update.message.chat["first_name"] in users) or not("messages" in users[update.message.chat["first_name"]]):
                users[update.message.chat["first_name"]] = {"messages":[]}
            users[update.message.chat["first_name"]]["messages"].append(update.message.text)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    return READING

def Waiting(update, context):    
    if(update.message.text == '/read'):
        update.message.reply_text("Comienzo a leer")
        return READING

def Write(update, context):
    with open('data.json', 'r+') as file:
        data = json.load(file)
        users = data["users"]
        if not(update.message.chat["first_name"] in users) or not("messages" in users[update.message.chat["first_name"]]):
            users[update.message.chat["first_name"]] = {"messages":[]}
        myUser = users[update.message.chat["first_name"]]
        messages = ''.join(map(str,myUser["messages"]))
        update.message.reply_text("He leido: " + messages)
        users[update.message.chat["first_name"]]["messages"] = [] 
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()



if __name__ == '__main__':
    updater = Updater(token=os.environ['ZTOKEN'], use_context=True)

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
    dp.add_handler(CommandHandler('help', SendHelp))
    dp.add_handler(CommandHandler('write', Write))

    dp.add_handler(ConversationHandler(
        entry_points=[         
            CommandHandler('create_pull', CreatePull) ],
        states={
            TAKEPULLTEXT: [MessageHandler(Filters.text, TakePullText)],
            TAKEOPTIONS: [MessageHandler(Filters.text, TakeOptions)],
            ENDCREATEPULL:[]
        },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[         
            CommandHandler('read', Read)
        ],
        states={
            READING: [MessageHandler(Filters.text, inputText)],
            NOTREADING: [MessageHandler(Filters.text, Waiting)]
        },
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()