# Informe Personal 
## Airelys Collazo Pérez C312
 
#### 1- Preparación del servidor, y creación del proyecto de Github 
Me correspondió ir preparando las condiciones para el sistema computacional que desarrollásemos.
Como primer paso se crea un proyecto de *Github* necesario para el trabajo en equipo y se unen a los miembros del equipo.
Además conocía que seguramente necesitaría de un servidor para albergar el sistema y poderlo usar en la fase de pruebas con un público que necesitaría acceder al mismo. Como requisito principal conozco que debe tener acceso a internet por el que debe ser accedido, y que se necesita que mantenga persistencia de datos. Se pensó en una base de datos, pero al ser sumamente  complejo el acceso a *Mongo Atlas* como primera expectativa(esto es dado que somos un país bloqueado), además realmente como teníamos casi completa seguridad que lo que hacía falta era simplemente guardar encuestas, sin muchos datos ni complejidad optamos por usar un json. Ahora volviendo al servidor, primero pensé en usar *Heroku*, pero este no mantiene persistencia, por lo tanto en busca de otro servidor gratuito encontré *pyhtonanywhere* el que reúne condiciones suficientes para usarlo para este trabajo.

#### 2- Conformación del diccionario de datos
Conociendo que sería conveniente usar un json por su simplicidad y flexibilidad me dispuse a conformar su diseño de forma que fuese fácilmente accedido por el programa y modificando, manteniendo una estructura correcta para evitar errores de integridad o datos duplicados sin necesidad

Primeramente en el json tendríamos un diccionario con 4 ítems principales:
- *Grupos* dado que necesitamos guardar los resultados de las encuestas por grupos
- *Analisis_Para_Administradores* que nos permite guardar el acceso del administrador a un grupo
- *Preguntas* para guardar las preguntas de las encuestas
- *Resultados* para guardar los resultados de los análisis correspondientes a las encuestas

Para *Grupos* debo guardar como llave algún identificador del grupo(podría ser el nombre?) y de valor otro diccionario que tenga por ítems los administradores del bot en el grupo dado que necesitamos almacenar los usuarios con el rol de administrador que tenga privilegios(como el de aplicar una encuesta y pedir los resultados), los integrantes con sus respuestas en las preguntas, el nombre del grupo y otros campos complementarios que se necesiten más adelante 
Para administradores guardamos el identificador del grupo
Para las preguntas guardé una lista de preguntas asignándole un número de identificador a cada una guardando además las categorías y subcategorías asignadas a cada una
Para los resultados los dejé en un diccionario en blanco esperando por los análisis y cuál sería la naturaleza de sus resultados. 

#### 3- Creando administradores
Una vez creado el bot, y Alejandro trabajando en las encuestas, a mime toca crear el sistema de roles, el que esta integrado por solo dos: usuario común que solo responde preguntas, administrador que pone encuestas y pide los resultados de la misma. El último es especialmente interesante dado que es quién va a tener acceso a todas las funcionalidades importantes. Primero vamos a tener un administrador principal que es el usuario final, el resto de administradores somos nosotros dado que necesitamos testear el bot y probarlo por lo tanto al inicializar cada grupo guardamos como administradores a estas personas recogiendo previamente el id del perfil de *Telegram* de cada uno como identificador. Luego creé un mecanismo para añadir nuevos administradores, eliminar y verificar los mismos a través de comandos, aquí no hay mucho más que explicar se añaden los comandos, y cada método accede al json, en el grupo en que se ejecuta el comando y la llave "Administradores" nos da acceso a estos datos para consultar, modificar o eliminar.
Adicionalmente cada comando o botón que necesite prioridad de administrador debe comprobar primero que el usuario que le usa sea parte de la lista de administradores del grupo.
Por último afuera guardamos un análisis para administradores, lo que nos permitiría que un usuario pida un análisis en un grupo y conocer luego qué análisis hacerle llegar

#### 4- Integración de los análisis con el bot
Se me asignó la tarea de con la ayuda de Henri y Alejandro integre estas dos soluciones parciales del problema que se complementan para completar la solución computacional al problema.
Para ello el comando de habilitar de encuestas que permite al administrador pedir por el chat privado del bot los análisis, ese comando no hace mucho más que guardar en el json, la sección de análisis para administradores el valor del identificador del grupo al administrador, y así conocer a que grupo dicho administrador quiere pedir el análisis.
Luego se crea el comando mostrar análisis que nos devuelve 3 botones con las opciones de mostrar análisis para el grupo, el personal, y la descripción general, estos datos son calculados por un algoritmo previamente implementado por Henri, y lo que hago es guardar dichos resultado en la sección de resultados. A estos resultados debo acceder en cada una de las opciones, en la de mostrar resultados para el grupo y personal es sencillo dado que pandas nos permite crear una hoja de cálculo *csv* la que luego se la puedo mandar al usuario, para devolver la descripción de los datos, se debe iterar por la misma e irla guardando en una variable la que es posteriormente enviada en un mensaje.

#### 5- Montar y correr el bot en pythonanywhere
Una vez terminada la implementación del bot, ya podía poner en un servidor para ejecutar las pruebas en los grupos y mostrarle su funcionamiento al profesor.
Para ello fue necesario crear una cuenta, y luego cogiendo la versión gratuita tengo acceso a 500mb de capacidad para poner el bot en este servidor que por defecto tiene instalado *pyhton* y a varios servicios aunque solo me bastaba la línea de comandos a través de la que primeramente instalé *pyhton-telegram-bot*, luego *pandas* y *numpy* usando el gestor de paquetes "pip". Luego se clona el proyecto desde *Github*, y se pone a correr con el comando
*python main.py*
Ejecutando este comando ya está corriendo el bot y completamente funcional.
Es de tener en cuenta que la versión gratuita de este servidor nos reinicia los procesos por lo que es necesario volver a correr el bot cada cierto tiempo

Con esto termina mi trabajo en el bot
