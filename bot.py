from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import json

STARTED = 0
READING = 0
NOREADING = 1

def start(update, context):
    update.message.reply_text("Hola soy un bot en desarrollo.")
    SendHelp(update, context)
    return STARTED

def SendHelp(update, context):
    update.message.reply_text("Ayuda de PollsterZBot \n\n Comandos disponibles: \n /help \n /read \n /write")

def Read(update, context):
    update.message.reply_text("Estoy leyendo")
    return READING

def inputText(update, context):
    if(update.message.text == '/stop_read'):
        update.message.reply_text("Dejo de leer")
        return NOREADING
    else:
        with open('data.json', 'r+') as file:
            data = json.load(file)
            users = data["users"]
            if not(update.message.chat["first_name"] in users):
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
        if not(update.message.chat["first_name"] in users):
            users[update.message.chat["first_name"]] = {"messages":[]}
        myUser = users[update.message.chat["first_name"]]
        messages = ''.join(map(str,myUser["messages"]))
        update.message.reply_text("He leido: " + messages)
        users[update.message.chat["first_name"]]["messages"] = [] 
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()



if __name__ == '__main__':
    updater = Updater(token='2082442589:AAGlx-gPI-aCKMyJR-tkNjAQtwGOtc4e8So', use_context=True)

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
            CommandHandler('read', Read)
        ],
        states={
            READING: [MessageHandler(Filters.text, inputText)],
            NOREADING: [MessageHandler(Filters.text, Waiting)]
        },
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()