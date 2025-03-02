import os
import tkinter as tk
from tkinter import filedialog
import threading
import pygame

# Definir la carpeta donde se guardarán los archivos descargados
DOWNLOAD_FOLDER = "musicplayer"

class MusicPlayer:
    def __init__(self, parent):
        self.parent = parent
        self.is_playing = False

        # Inicializar el reproductor de música
        pygame.mixer.init()

        # Crear marco para el reproductor
        self.frame = tk.Frame(self.parent, bg="lightgreen", width=200, height=100)
        self.frame.pack(side="bottom", padx=10, pady=10, fill="both", expand=False)

        # Etiqueta de título
        self.title_label = tk.Label(
            self.frame, text="Reproductor de Música", font=("Arial", 12, "bold"), bg="lightgreen"
        )
        self.title_label.pack(pady=5)

        # Lista de canciones descargadas
        self.song_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.song_listbox.pack(pady=5)
        self.load_songs()

        # Crear un marco para los botones de control
        self.controls_frame = tk.Frame(self.frame, bg="lightgreen")
        self.controls_frame.pack(pady=10)

        # Botón para seleccionar un archivo manualmente
        self.select_button = tk.Button(
            self.frame, text="Seleccionar Archivo", command=self.select_file, width=20
        )
        self.select_button.pack(pady=5)

        # Botones de control
        self.play_button = tk.Button(
            self.controls_frame, text="▶ Reproducir", command=self.play_selected_music, width=12
        )
        self.play_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(
            self.controls_frame, text="■ Detener", command=self.stop_music, state="disabled", width=12
        )
        self.stop_button.grid(row=0, column=1, padx=5)

    def load_songs(self):
        """Carga la lista de canciones descargadas en la carpeta 'musicplayer/'."""
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)

        self.song_listbox.delete(0, tk.END)  # Limpiar lista antes de recargar

        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.endswith(".mp3"):
                self.song_listbox.insert(tk.END, file)

    def select_file(self):
        """Abrir el selector de archivos para elegir un archivo de música manualmente."""
        self.music_file = filedialog.askopenfilename(
            filetypes=[("Archivos de audio", "*.mp3 *.wav"), ("Todos los archivos", "*.*")]
        )
        if self.music_file:
            self.title_label.config(text=f"Archivo: {os.path.basename(self.music_file)}")

    def play_selected_music(self):
        """Reproducir la canción seleccionada desde la lista de descargas."""
        selected_index = self.song_listbox.curselection()
        if not selected_index:
            return

        selected_song = self.song_listbox.get(selected_index)
        self.music_file = os.path.join(DOWNLOAD_FOLDER, selected_song)

        self.is_playing = True
        self.play_button.config(state="disabled")
        self.stop_button.config(state="normal")

        threading.Thread(target=self._play_music_thread, daemon=True).start()

    def _play_music_thread(self):
        """Hilo que reproduce la música."""
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if not self.is_playing:
                pygame.mixer.music.stop()
                break

    def stop_music(self):
        """Detener la reproducción de música."""
        self.is_playing = False
        self.play_button.config(state="normal")
        self.stop_button.config(state="disabled")
        pygame.mixer.music.stop()
