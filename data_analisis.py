
import json
import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering

DATA_ANALISIS = 0


def analisis(update, context):
    
    with open('data.json', 'r+') as file:
        data = json.load(file)

        group_id = update.chat["id"]

        group_analisis = data["Grupos"][group_id]

        df = { "name" : group_analisis.keys() }

        for row in group_analisis.values():
            for question in row:
                if df.get(question, True):
                    df[question] = []
                df[question].append(row[question])
        
        df = pd.DataFrame(df)

        questions = data["Preguntas"]

        sub = {"Pregunta":[], "NumeroPregunta":[], "IndiceSubcategoria":[], "Subcategoria":[], "Categoria":[]}

        for question in question:
            for column in question:
                sub[column].append(question[column])

        sub = pd.DataFrame(sub)

        preproc = pd.DataFrame()

        categoria = sub.groupby(['Categoria'])

        for i in categoria:
            preproc[i[0]] = df[list(categoria.get_group(i[0])["Pregunta"])].sum(axis=1)
            preproc["Porcentaje " + i[0]] =(df[list(categoria.get_group(i[0])["Pregunta"])].sum(axis=1)-20)/60*100
            preproc["Media " + i[0]] = df[list(categoria.get_group(i[0])["Pregunta"])].mean(axis=1)

        subcategoria = sub.groupby(['SubCategoria'])

        for i in subcategoria:
            preproc[i[0]] = df[list(subcategoria.get_group(i[0])["Pregunta"])].mean(axis=1)

        result = preproc.sum()/df["Nombre"].count()

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
        
        corr = preproc.iloc[:,[0,3,6,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]].corr()
        
        descr = {
            "descricion": preproc,
            "resultado": result,
            "moda": moda,
            "correlacion por categoria y subcategoria": corr
        }

        data["Resultados"][group_id] = descr

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def Show_Data_Analisis(update, context):
        
        if(update.callback_query.message.chat["type"] == "group"):
        
            with open('data.json', 'r+') as file:
                data = json.load(file)

                group_id = str(update.callback_query.message.chat["id"])
                user_id = str(update.callback_query.from_user.id)

                if(data["Grupos"].get(group_id, False) != False and user_id in data["Grupos"][group_id]["Administradores"]):
                    #Henri tu código va aquí
                    pass
                
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()