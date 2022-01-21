# Reporte

### Integrantes:
- Airelys Collazo Pérez C-312
- Alejandro Escobar Giraudy C-312
- Henri Daniel Peña Dequero C-311

## *Pollster Z Bot*
### Universidad de La Habana, MATCOM

#### 1. Introducción
Pollster Z Bot es un software que corre perpetuamente en un servidor con acceso a internet, comunicándose con telegram para ser usado en la aplicación con mismo nombre. Este es concebido como solución a la problemática de medir el sentido del humor en un grupo de personas.
¿Cómo es posible calcular el sentido del humor? Este es un concepto muy abstracto, al consultar con la opinión de psicólogos, articulos y demás se puede llegar a la conclusión de que directamente es muy complejo evaluarlo dado que el sentido del humor puede ser tan diverso como lo que se defina por sentido del humor(pues que puede ser interpretado de varias maneras), o con respecto a que medidas, o el cambio de acuerdo al grupo social en que se evalue, etc. Consecuencia de estas problemáticas se puede llegar a la solución de que no es necesario evaluar directamente el sentido del humor, sino que se puede evaluar otras escalas relacionadas al mismo, como la alegría, seriedad, etc lo que nos lleva a buscar solución en una escala multidimensional, como lo es **STCI**.
En la modalidad de autoreporte Willibald Ruch en 1994, (Ruch, 1996) desarrolla un instrumento llamado **STCI-60** (State Trait Cheerfulness Inventory), el cual contiene tres constructos. Dos sobre estados emocionales (alegría y mal humor) y uno sobre encuadre de la mente (seriedad). Cada uno de ellos puede manifestarse como estado o como rasgo dependiendo si se expresa como una disposición actual hacia el humor o si  se refiere a una disposición permanente (rasgo). La escala desarrollada por Ruch evalúa el humor como rasgo o disposición permanente. 
Siendo este el elegido para intentar medir el sentido del humor de una persona, llevado a un grupo se ha de tener en cuenta de que es necesario aplicar individualmente las encuestas y de estos resultados sacar conclusiones para el grupo en general.
Teniendo la herramienta para evaluar el sentido del humor, ¿Cómo la aplicamos? Teniendo en cuenta que los grupos de la facultad se han hecho en Telegram y que el mismo brinda la opción de crear bots que puedan leer  mensajes, poner botones, guardar datos y demás funcionalidades útiles, pues sería muy conveniente desarrollar la aplicación como un bot capaz de aplicar la encuestas a los grupos teniendo en cuenta que estos deben tener por integrantes a los estudiantes a los que se le quiere evaluar el sentido del humor. 
Si, perfecto, un bot de telegram... ¿Y ahora? Pues ya conociendo esto es necesario buscar la forma de implementarlo y desplegarlo para su uso, para implementarlo hemos elegido la librería python-telegram-bot en la que podemos crear el bot y agregarle todas las funionalidades necesarias como crear botones útiles para las encuestas, ejecución de comandos, enviar mensajes, etc. También es necesario tener persistencia de datos para guardar los resultados de las encuestas, así como administradores, incluso las mismas preguntas a aplicar con sus respectivas categorías y subcategorías, para ello es conveniente que sea flexible, además lo suficientemente rápido para acceder y modificar los datos en tiempo real, para ello se usa json. Luego el bot es puesto y corrido en un servidor que tenga instalado python y permita persistencia de datos, pythonanywhere nos proporciona los requisitos necesarios. Por último es bueno pensar en que usar para hacer los análisis descriptivos de los datos recogidos en las encuestas, para ello es muy cómodo usar las librerías de python pandas y numpy, las que tienen implementadas muchas herramientas útiles para este proceso.
EN este punto se ha reunido las condiciones necesarias para la implementación correcta del sistema computacional que de solución al problema en cuestión. De esta forma se concibe el proyecto

##### 1.1 Objetivo general:
- Diseñar un bot de telegram capaz de hacer encuestas en los grupos y hacer un análisis descriptivo sobre los resultados para medir el sentido del humor.

##### 1.2 Objetivos específicos:
- Aplicar encuestas capaces de medir el nivel de humor de los miembros de un grupo.
- Diseñar un bot capaz de aplicar encuestas en un grupo, almacenar y enviar resultados de los análisis.
- Gestionar administradores con privilegios para usar el bot.
- Ejecutar un análisis de los datos para devolver al usuario una descripción de las respuestas en las encuestas.
- Tener el bot listo para ser desplegado en un servidor para que funcione en todo momento.

#### 2. Análisis de requerimientos 
EL bot está implementado en *python*, usando principalmente las librerías *python-telgram-bot*, *pandas* y *numpy*, por lo tanto, es necesario desplegarlo en un servidor capaz de instalar estas dependencias, que además tenga acceso a internet 100% del tiempo, persistencia de datos y un almacenamiento de al menos 100mb. Adicionalmente el usuario final necesita un dispositivo con acceso a internet capaz de soportar la aplicación Telegram en donde se le dará uso.

##### 2.1 Solución Propuesta 
EL problema planteado es el de calcular el sentido del humor en un grupo de alumnos. Como ya mencionamos Willibald Ruch plantea que ante la dificultad de definir el sentido del humor es necesario conocer más bien los rasgos del comportamiento involucrados en la posibilidad de vivir el humor. Desarrolla para esto el concepto de regocijo o *exhilaration*, emoción que puede evaluarse empíricamente para lo que se desarrolla un instrumento que en realidad más que evaluar "sentido del humor" evalúa tres constructos o rasgos (alegría, seriedad y mal humor),  que posibilitan la emoción de regocijo. La escala STCI-T-60 es entonces el instrumento que contiene estos tres constructos.
Estos constructos determinan las características de la emoción de regocijo (*exhilaration*), en términos del umbral para alcanzar el estado, el nivel alcanzado y su estabilidad en el tiempo. La emoción de regocijo se crea ante estímulos tales como humor, cosquillas y gas hilarante, y se constituye en un conjunto de conductas (risas, posturas, gestos), experiencias (regocijo, percepciones entretenidas) y variables fisiológicas (respiración, vocalización, actividad cardíaca y endocrina). La emoción de regocijo también esta influenciada por variables contextuales como la influencia social, drogas psicoactivas y alcohol.
Esta consta de 60 preguntas(20 por categoría) a responder en 4 posibles opciones: Completamente de acuerdo, moderadamente de acuerdo, moderadamente en desacuerdo y completamente en desacuerdo, asignándole a cada uno de números enteros del 4 al 1 respectivamente, con lo que se procede a calcular. Estas categorías tienen a su vez varias subcategorías asignadas por preguntas.

Teniendo esto en cuenta procedemos a buscar como se puede aplicar de forma simple y eficiente dado que las encuestas a menudo son complejas de aplicar sin pérdida de interés por parte del sujeto a evaluar. conociendo que los grupos de la facultad se crean en Telegram, y que la aplicación de mismo nombre permite que se puedan implementar y usar bots, pues es una muy buena vía para aplicar los cuestionarios. Por lo tanto la solución pasa por implementar en *python* un bot de *Telegram* que sea capaz de aplicar los cuestionarios, analizar los resultados y devolverlos, adicionalmente para su correcto funcionamiento es necesario que tenga rol de administrador con los privilegios para enviar encuestas y pedir los resultados.

El bot está implementado con la librería *python-telegram-bot*, que se encarga de gestionar la comunicación con *Telegram* y te brinda los objetos ya implementados. El proyecto queda conformado por 4 archivos:
* **main.py** en el que esta creado el método principal del bot, en el mismo esta implementado adicionalmente los principales comandos de inicio, ayuda, enviar encuestas(así como los botones de elección de cantidad de preguntas a enviar), mostrar resultados de los análisis y el resto tomados de otros archivos del proyecto. 
* **assing_administrator.py** donde se implementa los comandos de asignar administradores, eliminar y mostrarlos, para ello es necesario apoyarse en un archivo json que va a guardar estos datos
* **send_pull.py** se encuentra la implementación de enviar las encuestas, así como el comando de reiniciar las encuestas para que las envíe desde el principio. Aquí se ha tenido que optimizar bien el código por un tema de que la librería *python-telegram-bot* mantiene un límite de tiempo por operaciones, este es fácilmente sobrepasado si enviamos muchas encuestas al mismo tiempo, además normalmente cada botón de una encuesta debería ser programado estáticamente, pero el para las 60 encuestas tendríamos 240 botones con código muy similar, por lo tanto lo mejor para este caso es crear cada encuesta de forma dinámica arriesgando que el mismo pueda ser destruido después de ejecutar el comando de enviar encuestas(el que se ejecuta para tener las opciones de enviar 1, 3, 5, 7 encuestas)
* **data_analisis.py** implementa todos los análisis descriptivos sobre los resultados en las encuestas, así como los comandos de *habilitar_analisis* y mostrar análisis, el último devolviendo 3 opciones: análisis en el grupo, análisis de una persona, descripción. El primero devuelve una hoja de cálculo con los resultados por categorías para todas las personas que respondieron al menos una encuesta, el segundo devuelve  una hoja de cálculo con los mismos datos que el primero añadiendo las subcategorías para una persona, y el tercero devuelve un mensaje con una descripción general de los resultados obtenidos en el grupo. Para ello se hace uso de las librerías *pandas* y *numpy* que suponen una eficiente herramienta para hacer un análisis descriptivo correcto de los datos haciendo uso de *DataFrames* y *Series* y sus respectivas operaciones.

La persistencia de datos se mantiene en un archivo json llamado **data.json**, en el que se guarda las preguntas, sus categorías y subcategorías, se guarda los administradores, y los grupos en los que se inicia el bot con los integrantes que han respondido encuestas y sus respuestas. Este modelo fue elegido a raíz de que es conveniente su flexibilidad y simplicidad manteniendo además una buena velocidad de acceso y modificación y su facilidad para usar.

El bot es necesario ejecutarlo en un servidor con acceso a internet que mantenga persistencia de datos y brinde una capacidad de al menos 100mb, en el que además pueda ser instalado *python* y librerías del lenguaje. Esto es necesario dado que el programa debe disponer de acceso a internet para la comunicación con *Telegram* además necesita de capacidad para guardar los datos de los grupos en los que es usado y que persistan en el tiempo(se menciona dado que hay servidores como *heroku* que en su versión gratuita reinicia cada cierto tiempo el despliegue perdiendo así los datos que se habían guardado hasta el momento), además esta implementado con pyhton haciendo uso de *pyhton-telegram-bot*, *pandas* y *numpy*. Un servidor que cumple estos requisitos es *pythonanywhere*

El proyecto contiene además otros archivos para su despliegue y uso en servidores como lo es **requirements.txt** que tiene las dependencias necesarias, **runtime** que tiene la versión de *python* en la que funciona, y **Procfile** guarda el comando a ejecutar para correr el bot. Por último se incluye una carpeta CSV que contiene la hoja de cálculo a enviar al usuario

También se incluye una carpeta de Notebooks en la que se ha implementado un generador de una población que responde en su totalidad las encuestas y un análisis de la misma hecho antes de implementarlo en el bot, en el mismo explica cómo se hace cada paso del mismo


#### 3. Prueba y resultados obtenidos 
Se ha hecho una prueba real del bot, para la que el bot ha sido montado en el servidor *pyhtonanywhere* auxiliándonos de *Github* para llevar el código al mismo justo después de instalar *pyhton-telegram-bot* usando gestor de paquetes *pip*, luego de correrlo con el comando *python main.py*, los cuestionarios son aplicados en un grupo de Telegram "offtopic" de 3ero CC en el que se ha añadido sin problemas le bot e iniciado, enviado 7 preguntas por la mañana y 7 por la tarde todos los días hasta que se  acabaron. Esta acción se cumplió satisfactoriamente durante el período del 10 al 15 de enero del 2022 con el objetivo de acumular la primera experiencia de uso real del bot creado. El grupo lo integran 60 estudiantes y es usado para hablar de cualquier temática de interés, además el período de aplicación de las encuestas corresponde al tramo final del semestre en el que el grupo es menos visitado de lo normal.

Luego aplicar las preguntas se extraen del bot lo análisis generales del grupo, el personal de dos miembros del grupo(a conveniencia los que más participaron), y a continuación se expone los resultados obtenidos.

##### 3.1 Análisis del grupo
Al comprobar los análisis obtenidos para el grupo podemos observar que a penas 10 personas respondieron al menos una pregunta de la encuesta, siendo a pruebas 2 o 3 los que ha respondido regularmente las preguntas. 
Analizando los datos se puede observar claramente  que en general los datos de las categorías no son ni muy elevados ni muy bajos, la alegría media se mantiene cercano a 3, el mal humor solo una persona supera el valor de 3, y la seriedad generalmente es alta(3 y 4) teniendo solo uno con el mínimo y alrededor de 2.7 los que más encuestas respondieron a excepción de uno que alcanza los 3.3 de media en esta categoría.

##### 3.2 Análisis de la persona
Se extrajo el personal de las dos personas que mayor número de preguntas respondieron a conveniencia. 

El primero a analizar es el usuario *hnadie*, este usuario mantiene una alegría con una media de 2.91 de 4, malhumor en 3.08 y seriedad en 2.7, teniendo además en el resto de subcategorías medias relativamente altas con un valor mínimo de 2, siendo "tristeza en situaciones alegres" el único que alcanza el máximo.

El segundo es el usuario *Sangre_Roja*, este usuario mantiene una alegría con una media de 2.42 de 4, malhumor en 2.92 y seriedad en 2.76, teniendo además en el resto de subcategorías medias oscilado entre 3 y 2 generalmente con solo uno por encima de 3(3.5 "estilo de interacción alegre")

##### 3.3 Descripción de los datos
Esta opción nos da por respuesta:
Medias: 
Alegria: 10.27
Porcentaje Alegria: 12.84
Media Alegria: 2.42
Mal humor: 10.18
Porcentaje Mal humor: 12.73
Media Mal humor: 2.47
Seriedad: 11.45
Porcentaje Seriedad: 14.32
Media Seriedad: 2.38
Amplio rango de desencadenadores de alegria, risa y sonrisa: 2.05
Bajo umbral para la risa y sonrisa.: 0.59
Estilo de comunicacion sobrio.: 0.98
Estilo de interaccion alegre: 0.64
Irritabilidad en situaciones alegres.: 0.0
Percepcion de que los eventos de la vida diaria son serios e importantes.: 1.86
Preferir actividades concretas y racionales: 0.59
Prevalencia de animo alegre.: 0.88
Prevalencia de estados serios.: 1.98
Prevalencia de mal humor: 1.27
Prevalencia de tristeza: 1.22
Sentimientos de irritabilidad.: 1.77
Tristeza en situaciones alegres.: 0.55
Vision positiva de las circunstancias adversas de la vida.: 2.33
Vivir en torno a metas.: 0.48
Modas: 
Alegria: 
valor: 3.0
porcentaje: 50.0
Seriedad: 
valor: 3.0
porcentaje: 66.67
Mal humor: 
valor: 3.0
porcentaje: 60.0

Claramente condicionado por la falta de participación en las encuestas aunque se puede ver como la moda de respuestas a las encuestas para todas las categorías es "moderadamente de acuerdo"

#### 4. Conclusiones y Recomendaciones
De esta forma queda concluido nuestra solución al problema en cuestión quedando desarrollada un bot que aplica las encuestas, guarda los resultados, analiza y devuelve los resultados de forma sencilla. ***Pollster Z Bot*** está listo para ser usado para un efectivo análisis del sentido del humor en el grupo y puede ser extendido para ampliar sus funcionalidades, se recomienda continuar trabajando en el tema donde hay una amplia gama de funcionalidades a incorporar por ejemplo: Permitir la aplicación de encuestas adicionales creadas por el usuario final con el objetivo de medir la aceptación de determinado tema en el grupo, leer mensajes y filtrar por temas de interés en el grupo, durante el análisis hacer un clústering agrupando por personas con sentido del humor o temas de interés parecidos, etc.

#### 5. Bibliografía y referencias
- Documentación  *python-telegram-bot*, *pandas*, *pyhtonanywhere*
- Series Investigación Clínica en Terapia de Pareja N°2 OTOÑO 2009 La Evaluación del Sentido del Humor AUTORES: Dr. Luis Tapia Villanueva, Ps. Gianella Poulsen
- Köhler G.,  Ruch W., (1996). Source of variance in current sense of humor inventories: How much substance, how much method variance? Humor. International Journal of Humor Research 9(3/4), 363-397.
- Estudio exploratorio sobre la utilización del humor en el proceso de enseñanza aprendizaje universitario Exploratory study on the use of humor at the university teaching‐learning process -Dr. C. Emilio Alberto Ortiz Torres eortiz@uho.edu.cu - Universidad de Holguín, Cuba.
- SENSE OF HUMOR AND DIMENSION OF PERSONALITY - JAMES A. THORSON AND F. C.POWELL - University of Nebraska at Omaha (799-809) 

