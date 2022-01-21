# Pollster Z Bot Manual de Usuario

### Autores:
Alejandro Escobar Giraudy C312
Airelys Collazo Perez C312
Henri Daniel Peña Dequero C311

#### Objetivo general:
- Diseñar un bot de *Telegram* capaz de hacer encuestas en los grupos y hacer un análisis descriptivo sobre los resultados para medir el sentido del humor.

#### Objetivos específicos:
- Aplicar encuestas capaces de medir el nivel de humor de los miembros de un grupo.
- Diseñar un bot capaz de aplicar encuestas en un grupo, almacenar y enviar resultados de los análisis.
- Gestionar administradores con privilegios para usar el bot.
- Ejecutar un análisis de los datos para devolver al usuario una descripción de las respuestas en las encuestas.
- Tener el bot listo para ser desplegado en un servidor para que funcione en todo momento.

#### Requerimientos Técnicos y de Software:
El bot solo puede ser usado por cualquier persona con un teléfono móvil que pueda soportar *apks*, y tener instalado la aplicación *Telegram* en cuyos los grupos es donde puede ser puesto a funcionar, interactuando además por el chat privado con el bot. Además es necesario desplegarlo o ponerlo a funcionar en un servidor con internet 100% del tiempo, persistencia de datos y almacenamiento de al menos 100mb y tener instalado en el mismo *python* 3.7 y las librerías *python-telegram-bot*, *pandas* y *numpy*.
#### Forma de acceder:
En *Telegram* debe dirigirse a algún grupo, y si este grupo se lo permite (dependiendo de las opciones de privilegios del grupo), accede a la opción de añadir usuarios, escribe el nombre del ***Pollster Z Bot*** y finalmente se encuentra en el grupo para su uso. Nota: Al *pollster bot* se le puede escribir al privado, pero el funcionamiento del mismo en este caso lo explicaremos a continuación.
Para desplegarlo en un servidor debe extraer el código de github: https://github.com:henri-dpd/pollster-z-bot.git
#### Funcionamiento:
Una vez el bot ha sido añadido a un grupo, verá que puede acceder a todos sus comandos mediante el carácter /, como cualquier otro bot. Los comandos que se le van a mostrar son:
- *iniciar_bot*, este comando es el único que se puede activar una vez el bot es añadido a un grupo, solo puede ser presionado una vez y la persona que lo presionó pasa a ser administrador del grupo y se permite el uso del resto de comandos.
- *start*, que te devuelve un mensaje con varios botones para lanzar diferentes cantidades de preguntas al grupo. Solo lanzará 60 preguntas en total
- *reiniciar_preguntas*, como solo hay 60 preguntas en las encuestas, mediante este botón podemos reiniciarlas para que comiencen de nuevo a enviarse desde la primera. En caso de que no hayan sido lanzadas todavía las 60 preguntas el bot mandará una alerta sobre eso, y si se toca un segunda vez el comando sí serán reiniciadas
- *mostrar_analisis*, este comando no funciona en los grupos, sino en el privado del bot si eres un administrador del bot en un grupo y haz activado el comando *habilitar_analisis*. Te envía los botones correspondientes a los análisis de los datos que ha recogido el bot en el grupo designado
- *habilitar_analisis*, habilita el comando anterior, debe activarse en un grupo y los datos que se pueden recoger solo son los de ese grupo
- *agregar_administrador*, te habilita para que escribas / y el *username* de un integrante del grupo, para que este pase a ser administrador del bot en el grupo
- *eliminar_administrador*, lo mismo que en el anterior, pero para borrar el usuario
- mostrar_administradores, muestra una lista con todos los *usernames* de los administradores del bot en este grupo
- *ayuda*, manda un mensaje con una lista de estos comandos.

Cuando se selecciona *start*, se lanzan los botones:
- "Mostrar 1 Pregunta"
- "Mostrar 3 Preguntas"
- "Mostrar 5 Preguntas"
- "Mostrar 7 Preguntas"


Cada uno de estos botones permite lanzar el número en cuestión de preguntas de las encuestas, hasta un límite de 60 antes de reiniciar, cada pregunta de la encuesta está conformada por un mensaje que es la pregunta en sí y 4 opciones a elegir a modo de botones, que son:
- "Completamente en Desacuerdo"
- "Moderadamente en Desacuerdo"
- "Moderadamente de Acuerdo"
- "Completamente de Acuerdo"

Para que uno dé su opinión sobre la pregunta.

#### Salidas del bot
Ahora, una vez que se ha usado *habilitar_analisis*, en un grupo, como ya dijimos se habilita la opción de usar *mostrar_analisis* en el privado del bot, esta lanza tres botones:
- "Mostrar Análisis", que devuelve un *CSV* con las estadísticas del análisis de datos de las encuestas
- "Mostrar Análisis de un Miembro", una vez presionado se coloca / y el *username* de unos de los integrantes del grupo, y se devuelve un *CSV* solo con las estadísticas del análisis de datos de ese integrante.
- "Descripción de los Datos", devuelve un mensaje con un promedio de las estadísticas del grupo en general.

