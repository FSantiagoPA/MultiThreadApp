import os
import tkinter as tk
from tkinter import ttk
import threading
import yt_dlp

# Definir la carpeta donde se guardarán los archivos descargados
DOWNLOAD_FOLDER = "musicplayer"

class MusicDownloader:
    def __init__(self, parent):
        """
        Inicializa la interfaz para descargar música de YouTube en MP3.
        """
        self.parent = parent

        # Crear carpeta de descargas si no existe
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)

        # Etiqueta de título
        title = tk.Label(self.parent, text="Descargar Música MP3", font=("Helvetica", 14, "bold"))
        title.pack(pady=10)

        # Entrada para la URL
        self.url_label = tk.Label(self.parent, text="URL de YouTube:")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(self.parent, width=50)
        self.url_entry.pack(pady=5)

        # Botón para iniciar la descarga
        self.download_button = tk.Button(self.parent, text="Descargar MP3", command=self.start_download, bg="lightblue")
        self.download_button.pack(pady=10)

        # Barra de progreso
        self.progress = ttk.Progressbar(self.parent, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        # Etiqueta de estado
        self.status_label = tk.Label(self.parent, text="", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

    def start_download(self):
        """Inicia la descarga en un hilo separado."""
        url = self.url_entry.get()
        if not url:
            self.status_label.config(text="Por favor, ingrese una URL válida.", fg="red")
            return
        self.status_label.config(text="Iniciando descarga...", fg="blue")
        threading.Thread(target=self.download_music, args=(url,), daemon=True).start()

    def download_music(self, url):
        """Descarga el audio de YouTube en MP3 usando yt-dlp."""
        try:
            self.status_label.config(text="Descargando...", fg="blue")
            output_template = os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s")

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.status_label.config(text="¡Descarga completada!", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
    def update_progress(self, stream, chunk, bytes_remaining):
        """Actualiza la barra de progreso durante la descarga."""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress["value"] = percentage
