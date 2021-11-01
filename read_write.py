import json

READING = 0
NOTREADING = 1
WRITE = 0

def Read(update, context):
    update.callback_query.answer(text="Estoy leyendo, para detenerme escriba stop_read")
    return READING

def inputText(update, context):
    if(update.message.text == '/stop_read'):
        update.message.reply_text("Dejo de leer")
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
        if not(update.callback_query.message.chat["first_name"] in users) or not("messages" in users[update.callback_query.message.chat["first_name"]]):
            users[update.callback_query.message.chat["first_name"]] = {"messages":[]}
        myUser = users[update.callback_query.message.chat["first_name"]]
        messages = ''.join(map(str,myUser["messages"]))
        update.callback_query.message.reply_text("He leido: " + messages)
        users[update.callback_query.message.chat["first_name"]]["messages"] = [] 
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
