# Informe técnico

### Integrantes:
- Airelys Collazo Pérez C312
- Alejandro Escobar Giraudy C312
- Henri Daniel Peña Dequero C311

## *Pollster Z Bot*
### Universidad de La Habana, MATCOM

#### Requerimientos técnicos 
Se va a ejecutar en un servidor con acceso a internet todo el tiempo, con persistencia de datos y una capacidad de al menos 100mb como por ejemplo puede ser *pythonanywhere*, necesario para el despliegue del bot y los usuarios finales pueden darle uso en Telegram por lo que solo necesitan un dispositivo que soporte la aplicación. 

#### Requerimientos de software  
Es necesario tener instalado *python* 3.7 o superior, además de las librerías *python-telegram-bot*, *pandas* y *numpy* en el servidor, para el usuario final basta tener instalado la aplicación Telegram.

#### Objetivo general:
- Diseñar un bot de Telegram capaz de hacer encuestas en los grupos y hacer un análisis descriptivo sobre los resultados para medir el sentido del humor.

#### Objetivos específicos:
- Aplicar encuestas capaces de medir el nivel de humor de los miembros de un grupo.
- Diseñar un bot capaz de aplicar encuestas en un grupo, almacenar y enviar resultados de los análisis.
- Gestionar administradores con privilegios para usar el bot.
- Ejecutar un análisis de los datos para devolver al usuario una descripción de las respuestas en las encuestas.
- Tener el bot listo para ser desplegado en un servidor para que funcione en todo momento.


#### Resumen
El ***Pollster Z Bot*** fue diseñado sobre la base de ser una aplicación que corra perpetuamente en internet, brindando los servicios de encuestas y análisis de datos de las mismas a partir de los integrantes de un grupo de Telegram. Para ello fue utilizado el Lenguaje Python con la biblioteca *python-telegran-bot*, *pandas* y *numpy*, así como *git* para la gestión de versiones y desarrollo de la aplicación, además desplegada en *pythonanywhere*.

#### Diseño de la aplicación
El proyecto en general está conformado por 4 archivos *.py*, donde se almacena el código, 1 archivo json, donde se guardan todos los datos acerca de las preguntas de las encuestas y de los datos que se recogen de los diferentes grupos,  una carpeta que contiene los CSV que serán enviados, otra que contiene los notebooks y CSV que explican el funcionamiento del análisis de datos, y por último algunos *txt* útiles para la instalación y despliegue en otras plataformas donde estará corriendo el código como puede ser *heroku*, o *pythonanywhere*.

#### Diccionario de datos 
Comencemos explicando cómo se guardan los datos en el json.
El archivo json tiene la estructura siguiente:
```json
{
    "Grupos" : {},
    "Analisis_Para_Administradores" : {},
    "Resultados" : {},
    "Preguntas" : []
}
```
En "Grupos" es un diccionario cuyas llaves son los id de los grupos donde el bot haya sido iniciado, y a partir de estas llaves guarda la información relativa al grupo.
La estructura de Grupos es:
```json
{
    "Integrantes": {}, 
    "Nombre del grupo": string, 
    "Pregunta Actual": int,
    "Administradores" : [], 
    "Usuarios": {}, 
    "Nuevo Administrador": string, 
    "Analisis" : int,
    "Reiniciar Encuesta" : int
}
```
Donde "Integrantes" es un diccionario, cuyas llaves son los id de los usuarios que hayan respondido preguntas del bot, y de estos estudiantes guarda en un diccionario, su username de Telegram (mediante la llave "Usuario"), y dado un número como llave, la respuesta que ha dado en las encuestas a la pregunta que coincide con ese número.
"Nombre del Grupo" representa el nombre del grupo de telegram correspondiente al id, "Pregunta Actual" es un entero que representa la pregunta que debemos enviar a continuación, Administradores es un lista que contiene los id de todos los administradores del bot en este grupo, Usuarios es un diccionario que, dado un username, devuelve el id de ese usuario, "Nuevo Administrador" es un string que ayuda al bot a agregar un nuevo administrador a ese grupo usando el id, "Analisis" y "Reiniciar Encuesta" son contadores que sirven para algunas de las funcionalidades del bot.
Regresando a la estructura principal del json, tenemos "Analisis_Para_Administradores", que dado un id de un administrador de un grupo en el que el bot esté activo, devuelve el id que identifica el grupo al que él puede acceder a sus datos a partir de los CSV.
"Resultados", que es un diccionario que tiene por llaves los id de los grupos y valor otro diccionario que contiene los resultados del último análisis ejecutado, hay 3 resultados: "descripcion" que tiene nombre, sumatoria por categoría, porcentaje por categoría, media por categoría para cada persona que respondió al menos una encuesta; "resultado" que tiene de forma general para todo el grupo en que promedio de sumatoria, porcentaje, media por categoría y sumatoria por subcategoría; moda contiene por categoría el valor que más se repite y en que porcentaje. Tenga en consideración que las respuestas de las encuestas se traducen a valores enteros entre 1 y 4.
Y por último "Preguntas", que es una lista de diccionarios que representan cada una de las preguntas, todos estos tienen por llaves "Pregunta", que es el enunciado de la pregunta, "NumeroPregunta", que es el índice de la pregunta, "IndiceSubcategoria", que representa el índice subcategoría a la que pertenece la pregunta, "Subcategoria", la subcategoría a la que pertenece la pregunta, y "Categoria", que es la categoría a la que pertenece la pregunta, para cada categoría se tiene varias subcategorías y por cada subcategoría se tiene varias preguntas, pero en general con 20 preguntas por categoría.

#### Esquema de las clases definidas 
Una vez explicado la estructura del json, comenzamos por cada uno de los .py.
Main.py contiene la estructura del bot en sí, los botones, comandos y etc. Es el archivo principal que debe ser cargado para que funcione el lenguaje.
En este se encuentra (al final) el *dispatcher* que nos permite agregar los comandos y botones, y a continuación el cuerpo de los mismos, que se agregan mediante *add_handler* (que pertenece a *python-telegram-bot*), siendo esta lista siguiente los comandos:
- *iniciar_bot*
- *start*
- *reiniciar_preguntas*
- *mostrar_analisis*
- *habilitar_analisis*
- *agregar_administrador*
- *eliminar_administrador*
- *mostrar_administradores*
- *ayuda*

Los botones tienen otras características y son demasiados puesto que, además de los principales, existen 240 solo para las encuestas.
Ahora explicaremos las funciones que podemos encontrar en todos los *.py*.
Estas contienen dos características similares, siempre que responda a un comando o botón la entrada serán dos parámetros *update* y *context*, que contienen toda la información que nos proporciona Telegram acerca de los usuarios que interactúan con el bot y el grupo en el que se encuentra (en caso de que se esté interactuando con el bot en un grupo claro está), y que se hace al inicio de cada método una serie de revisiones.
Estas revisiones suelen ser del tipo, si el usuario está interactuando con el bot por el privado o a partir de un grupo, si el grupo ya ha sido iniciado (o lo que es lo mismo, si el id del bot se encuentra en la sección "Grupos" del json), si dado el *username* del usuario ya fue recogido su id, y si la persona que interactúa con el bot es un administrador del mismo en ese grupo.
Aunque hay variaciones en algunos métodos, siempre se tiende a tener la estructura de preguntas anteriormente descrita, así que será común encontrarse ese código al inicio de cada función siempre, extrayendo y guardando en variables algunos datos de interés como el id del usuario y el id del grupo.
En **main.py** tenemos las funciones:
- *start*, que despliega los botones que se utilizan para lanzar preguntas al grupo, apoyándose en el método *Show_Pull_Buttons*
- *Show_Analisis_Buttons*, que muestra los botones utilizados para devolver los CSV con el análisis de datos
- *SendHelp*, que muestra la lista de comandos del ***Pollster Z Bot***

Una vez analizado main procedamos al resto de *.py*
**Assign_administrator.py** es el encargado de las funciones que tengan que ver con la decisión sobre quién es administrador de cierto grupo. Si bien todos los presentes en el grupo pueden participar en las encuestas, solo los que sean designados como administradores del grupo pueden utilizar los comandos del mismo, así como los botones que no tenga que ver con las encuestas.
Aquí podemos encontrar los métodos:
- *inicialization*, que responde a un comando que solo se puede utilizar una vez, y es el primero que debemos utilizar al agregar el bot a un grupo. Este comando agrega el grupo con su información pertinente al json, y designa a la persona que lo use como administrador del bot en el grupo inmediatamente. Ningún otro comando funciona hasta que no hayamos activado este.
- *add_administrator* y *enter_administrator*, son dos funciones que permiten agregar un administrador del bot en un grupo, por la dinámica de los comandos, al seleccionar el comando correspondiente, se habilita el bot para guardar información de quién se quiere agregar, *add_administrator* informa al json de este estado y *enter_administrador* agrega a la persona a partir de que el bot lea lo que escribe.
- *Remove_Administrator* y *Erase_Administrator*, que elimina un administrador del bot en un grupo siguiendo la lógica anterior.
- *Show_Administrators*, que básicamente manda un mensaje con una lista de los *usernames* de los administradores en el grupo actual.

**Send_pull.py** es el que contiene las funciones relacionadas con las encuestas.
En este podemos encontrar:
- *Restart_Pull*, que permite reiniciar las preguntas para que comience a mandarse desde la primera de nuevo
- *Pulls_Buttons*, es una función que responde a los 240 botones de las distintas opciones de las 60 preguntas, recibe en el *update* cuál es el botón que fue tocado y a qué pregunta pertenece, para guardar dicha información en el json.
- *Add_Pull_Callback_Query_Handler*, añade de forma dinámica el código de los 240 botones de las preguntas, para luego ser cargado por el *dispatcher* del *main*
- *Send_Pull*, que permite lanzar n preguntas con sus 4 opciones respectivas, esta viene a continuación de *Send_Pull_1, 3, 5 y 7*, que le informan del número de preguntas correspondientes a lanzar.

Por último tenemos **data_analisis.py** en donde están los métodos que calculan el análisis:
Consta de los métodos:
- *enable_analisis* se ejecuta al lanzar el comando *habilitar_analisis* permitiendo al usuario acceder al análisis por el chat privado del bot en donde se envía un mensaje de *feedback* para que el usuario sepa que fue ejecutado con éxito.
- *analisis* método que se ejecuta al lanzar el comando *mostrar_analisis*, en el mismo se toma los datos del grupo en que se habilitó el análisis y se procesan para guardar en el json "Resultados" los resultados. Para realizar el análisis se crean dos *DataFrames*(utilizando *pandas*), *df* que contiene de columnas *Nombre* y las preguntas teniendo por fila las respuestas de cada usuario y *sub* que tiene por columnas *Pregunta, NumeroPregunta, IndiceSubcategoria, Subcategoria, Categoria* siendo así cada fila una pregunta de esta manera conocemos por cada pregunta cuál es su categoría y subcategoría, teniendo esto se procede al análisis descriptivo de los datos, se crea un *DataFrame* *preproc* auxiliar en el que guardaremos los resultados, luego se agrupa preguntas por categoría guardando el resultado en categoría, iterando por las categorías procedemos a extraer la sumatoria, porcentaje y media filtrando en la categoría por persona y guardando dichas series(columnas en los DataFrames) en *preproc*, usando la misma lógica agrupamos y calculamos la sumatoria por subcategoría guardando el resultado también en categoría, luego se guarda en una variable llamada resultado la sumatoria de las categorías de todas las personas guardada en *preproc*, a continuación crea el diccionario de modas por categoría asignando como valor por defecto "-" y antes de llenarlo se verifica si existen preguntas respondidas en la categoría, una vez terminado y tenemos todos los datos descriptivos por lo tanto *preproc*, resultado, moda se guardan en **data.json** en *data["Resultados"][group_id]* teniendo como llaves "descripcion", "resultado", "moda" respectivamente.
- *Show_Data_Analisis_All_Member* lee de **data.json** en *data["Resultados"][group_id]["descripcion"]* y se toma las columnas desde "Nombre" hasta "Media Seriedad" y se guarda en *"CSV/Resultados en el grupo.csv"* para posteriormente enviarlo el mismo al usuario
- *Show_Data_Analisis_One_Member* envía al usuario un mensaje para indicarle como debe pedir el nombre de la persona de quien va a obtener los datos
- *Show_Data_Analisis_One_Member_Enter* lee el nombre que le envían al bot y lee de **data.json** en *data["Resultados"][group_id]["descripcion"]* devolviendo la fila que tiene por nombre el que el usuario necesita, se guarda en "*CSV/Resultados en la persona.csv"* y envía al usuario.
- *Data_Description* lee de **data.json** en *data["Resultados"][group_id]["resultado"]* y *data["Resultados"][group_id]["moda"]* para luego guardar los datos en una variable para luego enviarlo como un mensaje al usuario
  
De esta forma queda conformado el proyecto, concluimos el actual informe. Gracias por leer.
