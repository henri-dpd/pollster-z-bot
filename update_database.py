#Insertar el documento data a la colleccion 
def insert_document(collection, data):
    collection.insert_one(data)

#Para filtrar documentos de una coleccion, si filtramos por mas de un elemento 
#tenemos que pasar multiple en True
def find_document(collection, elements, multiple = False):
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)

#Actualizamos el documento de una coleccion
#query_elements es la query que queremos actualizar y new values seria el nuevo 
#valor para esa query
def update_document(collection, query_elements, new_values):
    collection.update_one(query_elements, {'$set' : new_values})

#Eliminamos un documento de la coleccion pasando una query del documento a eliminar
def delete_document(collection,query):
    collection.delete_one(query)
