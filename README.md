# MultiThreadApp

https://youtu.be/D2Q1FAYFCPc

![Descripción de la imagen](img/Captura%20de%20pantalla%202025-02-20%20211717.png)
Este programa es una ventana de escritorio con múltiples funcionalidades, incluyendo monitoreo del clima, gestión de aplicaciones, descarga de música, chat, estadísticas y un reproductor multimedia. Se ha diseñado con una interfaz gráfica que organiza diferentes módulos en secciones.


📌 Funcionalidad: Descargar Música MP3
Esta sección de la aplicación permite a los usuarios descargar archivos MP3 desde YouTube ingresando una URL válida.

🛠 ¿Cómo funciona?
Ingresar URL de YouTube

El usuario introduce un enlace de un video de YouTube en el campo de texto.
Presionar el botón "Descargar MP3"

El sistema procesa la URL y extrae el audio en formato MP3.
Se muestra una barra de progreso (si está implementada).
Ubicación del archivo descargado

Tras la conversión, el archivo MP3 queda disponible en la carpeta de descargas o en una ruta definida por el usuario.

📌 Análisis de la Relación entre la Economía Mundial y el Precio de Bitcoin
Esta sección del proyecto presenta dos gráficos de líneas que muestran la evolución de dos indicadores clave:

Índice Económico Mundial (Gráfico superior, en azul).
Precio del Bitcoin en USD (Gráfico inferior, en verde).

📊 Descripción de los gráficos
Gráfico superior: Economía Mundial

Representa la variación de un índice económico global a lo largo del tiempo.
En el eje X se observan los días, y en el eje Y, el índice económico.
Se aprecia volatilidad con caídas y subidas significativas.
Gráfico inferior: Precio del Bitcoin

Muestra la evolución del precio de Bitcoin en USD en el mismo periodo de tiempo.
En el eje X se representan los días, y en el eje Y, el valor del Bitcoin.
Se observa alta volatilidad con tendencias alcistas y bajistas.

🎮 Tic Tac Toe (Tres en Raya)
Esta sección del proyecto implementa un juego de Tic Tac Toe (Tres en Raya) con una interfaz gráfica sencilla.

📌 Características
Modo de juego:

Soporta Jugador vs Jugador, como se indica en la imagen.
Posible opción para Jugador vs IA en versiones futuras.
Interfaz gráfica:

Tablero de 3x3 con casillas interactivas.
Texto indicando de quién es el turno (en este caso, X).
Lógica del juego:

Los jugadores alternan turnos colocando X y O.
El juego detecta automáticamente si hay un ganador o empate.

🛠 Interfaz de Cliente SQL
Esta sección del proyecto implementa un cliente SQL que permite a los usuarios conectarse a una base de datos y ejecutar consultas SQL directamente desde la interfaz gráfica.

📌 Características
Conexión a la Base de Datos

Campos para ingresar host, usuario, contraseña y nombre de la base de datos.
Botón "Conectar" para establecer la conexión con el servidor SQL.
Ejecución de Consultas SQL

Área de texto donde los usuarios pueden escribir consultas SQL.
Botón "Ejecutar" para enviar la consulta a la base de datos.
Área de resultados donde se mostrarán los datos devueltos por la consulta.
Compatibilidad con Motores SQL

Compatible con MySQL, PostgreSQL o SQLite, dependiendo de la configuración de conexión.

🌐 Interfaz de Web Scraping y Almacenamiento en Base de Datos
Esta sección del proyecto permite realizar Web Scraping de una página web y almacenar los datos extraídos en una base de datos.

📌 Características
Conexión a la Base de Datos

Campos para ingresar host, usuario, contraseña y nombre de la base de datos.
Botón "Crear Base de Datos" para inicializar la base de datos donde se almacenarán los datos extraídos.
Web Scraping

Permite ingresar una URL objetivo (Ejemplo: https://quotes.toscrape.com/).
Campo para definir el Selector HTML (h1, p, div, span, etc.) para extraer datos específicos.
Botones de control:
Iniciar Scraping: Comienza el proceso de extracción de datos.
Parar Scraping: Detiene el proceso en curso.
Resetear Scraping: Limpia los datos extraídos y reinicia el proceso.
Estado del Scraping

Muestra un estado dinámico (Activo o Inactivo) en la interfaz para indicar si el proceso está en ejecución.
Resultados

Los datos extraídos se muestran en un área de texto en la parte inferior de la interfaz.

📧 Interfaz de Envío de Correos Electrónicos
Esta sección del proyecto permite a los usuarios enviar correos electrónicos a través de una interfaz gráfica sencilla.

📌 Características
Campos de entrada

Correo electrónico: Dirección del remitente.
Contraseña: Clave del correo (puede requerir autenticación de aplicaciones).
Destinatario: Dirección de correo a la que se enviará el mensaje.
Asunto: Título o tema del correo.
Mensaje: Cuerpo del correo a enviar.
Botón de envío

Una vez completados los campos, el usuario presiona "Enviar" para procesar el correo.
Compatibilidad

Funciona con SMTP para enviar correos desde proveedores como Gmail, Outlook, Yahoo, etc.

📩 Interfaz de Bandeja de Entrada de Correos
Esta sección del proyecto permite a los usuarios cargar y gestionar correos electrónicos desde su bandeja de entrada.

📌 Características
Inicio de Sesión

Correo electrónico: Campo para ingresar la dirección de email del usuario.
Contraseña: Clave del correo (puede requerir autenticación de aplicaciones si el proveedor lo exige).
Carga de Correos

Botón "Cargar Correos" para recuperar los mensajes desde el servidor de correo (IMAP o POP3).
Se listan los correos recuperados en la interfaz.
Gestión de Correos

Posibilidad de eliminar correos seleccionados mediante el botón "Eliminar Correo".
Compatibilidad

Funciona con IMAP o POP3, lo que permite acceder a bandejas de entrada de proveedores como Gmail, Outlook y Yahoo.
