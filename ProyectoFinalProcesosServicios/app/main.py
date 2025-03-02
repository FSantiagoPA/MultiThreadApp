import tkinter as tk
import threading
import time
import datetime
from tkinter import Menu # Importar el widget Menu
from tkinter import ttk # Importar el widget ttk
from correo_server.EmailTab import MailTab
from correo_server.InboxTab import InboxTab
from correo_server.MailClient import MailClient
from hilos.ChatWidget import ChatWidget
from hilos.MusicPlayer import MusicPlayer
from hilos.WeatherWidget import WeatherWidget
from hilos.SystemMonitor import SystemMonitor
from hilos.ApplicationLauncher import ApplicationLauncher
from hilos.LanguageChart import LanguageChart
from solapas.MusicDownloader import MusicDownloader
from solapas.EconomyBitcoinChart import EconomyBitcoinChart
from solapas.SQLQueryExecutor import SQLQueryExecutor
from solapas.TicTacToe import TicTacToe
from solapas.WebScraperToDB import WebScraperToDB


# Crear instancia del cliente de correo con configuración de puertos
email_client = MailClient()

# Clave de API de OpenWeatherMap
API_KEY = "1fa8fd05b650773bbc3f2130657e808a"

def update_time(status_bar):
    """Función que actualiza la hora y el día de la semana en un label"""
    while True:
        # Obtener la fecha y hora actual
        now = datetime.datetime.now()
        day_of_week = now.strftime("%A")  # Día de la semana
        time_str = now.strftime("%H:%M:%S")  # Hora en formato HH:MM:SS
        date_str = now.strftime("%Y-%m-%d")  # Fecha en formato YYYY-MM-DD
        label_text = f"{day_of_week}, {date_str} - {time_str}"

        # Actualizar el label (debemos usar `after` para asegurarnos que se actualice en el hilo principal de Tkinter)
        label_fecha_hora.after(1000, status_bar.config, {"text": label_text})

        # Espera 1 segundo antes de actualizar de nuevo
        time.sleep(1)

# Crear la ventana principal
root = tk.Tk()
root.title("Ventana Responsive")
root.geometry("1000x700")  # Tamaño inicial

# Configurar la ventana principal para que sea responsive
root.columnconfigure(0, weight=0)  # Columna izquierda, tamaño fijo
root.columnconfigure(1, weight=1)  # Columna central, tamaño variable
root.columnconfigure(2, weight=0)  # Columna derecha, tamaño fijo
root.rowconfigure(0, weight=1)  # Fila principal, tamaño variable
root.rowconfigure(1, weight=0)  # Barra de estado, tamaño fijo

# Crear el menú superior
menu_bar = Menu(root)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nuevo")
file_menu.add_command(label="Abrir")
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Copiar")
edit_menu.add_command(label="Pegar")

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Acerca de")

menu_bar.add_cascade(label="Archivo", menu=file_menu)
menu_bar.add_cascade(label="Editar", menu=edit_menu)
menu_bar.add_cascade(label="Ayuda", menu=help_menu)

root.config(menu=menu_bar)

# Crear los frames laterales y el central
frame_izquierdo = tk.Frame(root, bg="lightblue", width=150)
frame_central = tk.Frame(root, bg="white")
frame_derecho = tk.Frame(root, bg="lightgreen", width=150)

# Colocar los frames laterales y el central
frame_izquierdo.grid(row=0, column=0, sticky="ns")
frame_central.grid(row=0, column=1, sticky="nsew")
frame_derecho.grid(row=0, column=2, sticky="ns")

# Configurar los tamaños fijos de los frames laterales
frame_izquierdo.grid_propagate(False)
frame_derecho.grid_propagate(False)

# Integrar el widget del clima en el panel izquierdo
weather_widget = WeatherWidget(frame_izquierdo, API_KEY)

# Añadir el lanzador de aplicaciones al panel izquierdo
app_launcher = ApplicationLauncher(frame_izquierdo)

# Añadir gráfico de lenguajes al panel izquierdo
language_chart = LanguageChart(frame_izquierdo)

# Crear el widget de Chat en el panel derecho con más espacio
chat_widget = ChatWidget(frame_derecho)

# Agregar el reproductor de música al panel derecho, en la parte inferior
music_player = MusicPlayer(frame_derecho)

# Dividir el frame central en dos partes (superior variable e inferior fija)
frame_central.rowconfigure(0, weight=1)  # Parte superior, tamaño variable
frame_central.rowconfigure(1, weight=0)  # Parte inferior, tamaño fijo
frame_central.columnconfigure(0, weight=1)  # Ocupa toda la anchura

# Crear subframes dentro del frame central
frame_superior = tk.Frame(frame_central, bg="lightyellow")
frame_inferior = tk.Frame(frame_central, bg="lightgray", height=100)

# Colocar los subframes dentro del frame central
frame_superior.grid(row=0, column=0, sticky="nsew")
frame_inferior.grid(row=1, column=0, sticky="ew")

# Fijar el tamaño de la parte inferior
frame_inferior.grid_propagate(False)

# Crear un evento de parada
stop_event = threading.Event()

# Definir el manejador para el cierre de la ventana
def on_closing():
    """Cerrar correctamente la aplicación."""
    stop_event.set()  # Detener los hilos
    root.destroy()    # Destruir la ventana principal

# Configurar el manejador de cierre
root.protocol("WM_DELETE_WINDOW", on_closing)

# Crear la barra de estado
barra_estado = tk.Label(root, text="Barra de estado", bg="lightgray", anchor="w")
barra_estado.grid(row=1, column=0, columnspan=3, sticky="ew")

# Inicializar el monitor del sistema
system_monitor = SystemMonitor(barra_estado, stop_event)

# Notebook para las pestañas
style = ttk.Style()
style.configure("CustomNotebook.TNotebook.Tab", font=("Arial", 12, "bold"))
notebook = ttk.Notebook(frame_superior, style="CustomNotebook.TNotebook")
notebook.pack(fill="both", expand=True)

# Crear la Solapa 1 y añadir el downloader
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Downloader", padding=4)

# Añadir el downloader a la Solapa 1
music_downloader = MusicDownloader(tab1)

# Crear la Solapa 2 y añadir los gráficos
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Graphics", padding=4)

# Añadir los gráficos de economía mundial y Bitcoin a la Solapa 2
economy_bitcoin_chart = EconomyBitcoinChart(tab2)

# Crear la Solapa 3 y añadir el Tic Tac Toe
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Tic Tac Toe", padding=4)

# Añadir el juego de Tic Tac Toe a la Solapa 3
tic_tac_toe = TicTacToe(tab3)

# Crear la Solapa 4 y añadir el SQL Query Executor
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="SQL Querys", padding=4)

# Añadir el ejecutor de consultas SQL a la Solapa 4
sql_query_executor = SQLQueryExecutor(tab4)

# Crear la Solapa 5 y añadir el Web Scraper
tab5 = ttk.Frame(notebook)
notebook.add(tab5, text="Web Scraper", padding=4)

# Añadir el widget de Web Scraper a la Solapa 5
web_scraper = WebScraperToDB(tab5)

# Crear pestañas de correo
MailTab(notebook, email_client)
InboxTab(notebook, email_client)

# Barra de estado
# Dividir la barra de estado en 4 labels
# Usar pack para alinear los labels horizontalmente
label_fecha_hora = tk.Label(barra_estado, text="Hilo fecha-hora", font=("Helvetica", 14), bd=1, fg="blue", relief="sunken", anchor="w", width=20, padx=10)

label_fecha_hora.pack(side="right", fill="x", expand=True)
# barra_estado.grid(row=1, column=0, columnspan=3, sticky="ew")


update_thread = threading.Thread(target=update_time, args=(label_fecha_hora,))
update_thread.daemon = True  # Hacemos el hilo un demonio para que termine con la app
update_thread.start()

# Ejecución de la aplicación
root.mainloop()