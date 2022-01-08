
import json
from numpy.core.numeric import NaN
import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
from telegram import ChatAction
from telegram.ext.conversationhandler import ConversationHandler

DATA_ANALISIS_ALL_MEMBER = 0
DATA_DESCRIPTION = 0
DATA_ANALISIS_ONE_MEMBER = 0


def analisis(update, context):

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
            
                        group_analisis = data["Grupos"][group_id]["Integrantes"]

                        keys = group_analisis.keys()
                        
                        questions = data["Preguntas"]
                        
                        sub = {"Pregunta":[], "NumeroPregunta":[], "IndiceSubcategoria":[], "Subcategoria":[], "Categoria":[]}

                        for question in questions:
                            for column in question:
                                sub[column].append(question[column])

                        df = {"Nombre": []}

                        for q in sub["NumeroPregunta"]:
                            df[q] = []


                        for id in keys:
                            df["Nombre"].append(group_analisis[id]["Usuario"])
                            for i in range(60):
                                str_i = str(i)
                                if str_i in group_analisis[id].keys():
                                    df[i+1].append(group_analisis[id][str_i])
                                else:
                                    df[i+1].append(NaN)

                        df = pd.DataFrame(df)

                        sub = pd.DataFrame(sub)

                        preproc = pd.DataFrame()

                        preproc["Nombre"] = df["Nombre"]
                        categoria = sub.groupby(['Categoria'])

                        for i in categoria:
                            preproc[i[0]] = df.loc[:,list(categoria.get_group(i[0])["NumeroPregunta"])].sum(axis=1)
                            preproc["Porcentaje " + i[0]] =(df.loc[:,list(categoria.get_group(i[0])["NumeroPregunta"])].sum(axis=1))/80*100
                            preproc["Media " + i[0]] = df.loc[:,list(categoria.get_group(i[0])["NumeroPregunta"])].mean(axis=1)

                        subcategoria = sub.groupby(['Subcategoria'])

                        for i in subcategoria:
                            preproc[i[0]] = df.loc[:,list(subcategoria.get_group(i[0])["NumeroPregunta"])].mean(axis=1)

                        result = preproc.loc[:,"Alegria":].sum()/df["Nombre"].count()

                        moda = { 
                                "Alegria" : {
                                    "valor": preproc["Media Alegria"].round().mode()[0], 
                                    "porcentaje": preproc["Media Alegria"].round().value_counts(normalize=True).max()*100
                                },
                                "Seriedad" : {
                                    "valor": preproc["Media Seriedad"].round().mode()[0], 
                                    "porcentaje": preproc["Media Seriedad"].round().value_counts(normalize=True).max()*100
                                },
                                "Mal humor": {
                                    "valor": preproc["Media Mal humor"].round().mode()[0], 
                                    "porcentaje": preproc["Media Mal humor"].round().value_counts(normalize=True).max()*100
                                }
                            }
                        
                        #corr = preproc.iloc[:,[0,3,6,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]].corr()
                        
                        descr = {
                            "descripcion": preproc.to_json(),
                            "resultado": result.to_json(),
                            "moda": moda,
                        #    "correlacion por categoria y subcategoria": corr
                        }

                        data["Resultados"][group_id] = descr
                        
                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()


def Show_Data_Analisis_All_Member(update, context):
        
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
                        general = pd.DataFrame(json.loads(data["Resultados"][group_id]["descripcion"]))
                        general = general.loc[:, "Nombre": "Media Seriedad"]
                        general.to_csv("CSV/Resultados en el grupo.csv")

                        update.callback_query.message.chat.send_action(
                            action = ChatAction.UPLOAD_DOCUMENT,
                            timeout = None
                        )
                    
                        update.callback_query.message.chat.send_document(
                            document = open("CSV/Resultados en el grupo.csv", 'rb')
                        )

                        #os.unlink("CSV/Resultados en el grupo.csv")

                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()


def Show_Data_Analisis_One_Member(update, context):

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
                    
                    data["Grupos"][group_id]["Analisis"] = user_id
                    update.callback_query.message.reply_text("Escriba el username de la persona de la que desea ver sus datos (con / antes del nombre y sin  @)")            

                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    return DATA_ANALISIS_ONE_MEMBER
                else:
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()



def Show_Data_Analisis_One_Member_Enter(update, context):
        
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
                    
                if(user_id in data["Grupos"][group_id]["Administradores"]
                    and data["Grupos"][group_id]["Analisis"] == user_id):
                    
                    data["Grupos"][group_id]["Analisis"] = 0

                    name = update.message.text

                    if(name[0] != "/"):
                        file.seek(0)
                        json.dump(data, file, indent=4)
                        file.truncate()
                        return ConversationHandler.END

                    name = name[1:len(name)]

                    preproc = pd.DataFrame(json.loads(data["Resultados"][group_id]["descripcion"]))
                    personal = preproc[(preproc["Nombre"] == name)]

                    personal.to_csv("CSV/Resultados en la persona" + ".csv", sep=',')
                
                    update.message.reply_text("Resultados de la encuesta de: \n @" + name)


                    update.message.chat.send_action(
                    action = ChatAction.UPLOAD_DOCUMENT,
                    timeout = None
                    )
                
                    update.message.chat.send_document(
                    document = open("CSV/Resultados en la persona" + ".csv", 'rb')
                    )

                    #os.unlink("CSV/" + name + ". Resultados en la persona" + ".csv")


                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                return ConversationHandler.END

def Data_Description(update, context):
        
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
                        
                        result = json.loads(data["Resultados"][group_id]["resultado"])
                        moda = data["Resultados"][group_id]["moda"]
                        
                        message_text = "Medias: \n"
                        for d in result:
                            message_text += d +": "+ str(round(result[d],2)) + "\n"
                        message_text += "Modas: \n"
                        for d in moda:
                            message_text += d +": \n"
                            for m in moda[d]:
                                message_text += m + ": " + str(round(moda[d][m],2)) + "\n"

                        update.callback_query.message.reply_text(message_text)

                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()