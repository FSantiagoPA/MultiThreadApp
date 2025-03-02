import tkinter as tk
import threading
import subprocess
import os


class ApplicationLauncher:
    def __init__(self, parent):
        """
        Inicializa los botones para lanzar aplicaciones con detección automática de rutas.

        Args:
            parent (tk.Frame): Frame donde se colocarán los botones.
        """
        self.parent = parent

        # Detectar rutas automáticamente
        self.vscode_path = self.detect_path(["C:\\Program Files\\Microsoft VS Code\\Code.exe",
                                             "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"])
        self.eclipse_path = self.detect_path(["C:\\eclipse\\eclipse.exe",
                                              "C:\\Program Files\\Eclipse Foundation\\eclipse.exe"])
        self.pycharm_path = self.detect_path(["C:\\Program Files\\JetBrains\\PyCharm\\bin\\pycharm64.exe",
                                              "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2023.1.4\\bin\\pycharm64.exe"])

        # Título para el grupo de botones
        title = tk.Label(self.parent, text="Aplicaciones", font=("Helvetica", 14, "bold"), bg="lightblue")
        title.pack(pady=10)

        # Botón para abrir Visual Studio Code
        self.vscode_button = tk.Button(self.parent, text="Visual Code", command=self.launch_vscode, bg="lightgreen",
                                       font=("Helvetica", 10))
        self.vscode_button.pack(fill="x", pady=2)

        # Botón para abrir Eclipse
        self.eclipse_button = tk.Button(self.parent, text="Eclipse", command=self.launch_eclipse, bg="lightgreen",
                                        font=("Helvetica", 10))
        self.eclipse_button.pack(fill="x", pady=2)

        # Botón para abrir PyCharm
        self.pycharm_button = tk.Button(self.parent, text="PyCharm", command=self.launch_pycharm, bg="lightgreen",
                                        font=("Helvetica", 10))
        self.pycharm_button.pack(fill="x", pady=2)

    def detect_path(self, paths):
        """
        Detecta automáticamente la primera ruta existente de una lista de posibles rutas.

        Args:
            paths (list): Lista de rutas posibles para un ejecutable.

        Returns:
            str: La primera ruta válida encontrada, o None si no se encuentra ninguna.
        """
        for path in paths:
            path = os.path.expandvars(path)  # Expande variables como %USERNAME%
            if os.path.exists(path):
                return path
        return None

    def launch_vscode(self):
        """Lanza Visual Studio Code si se encuentra la ruta."""
        self.launch_application(self.vscode_path, "Visual Studio Code")

    def launch_eclipse(self):
        """Lanza Eclipse si se encuentra la ruta."""
        self.launch_application(self.eclipse_path, "Eclipse")

    def launch_pycharm(self):
        """Lanza PyCharm si se encuentra la ruta."""
        self.launch_application(self.pycharm_path, "PyCharm")

    def launch_application(self, path, name):
        """
        Lanza una aplicación si la ruta es válida.

        Args:
            path (str): Ruta al ejecutable.
            name (str): Nombre de la aplicación (para mensajes de error).
        """
        if path:
            threading.Thread(target=self.run_command, args=([path],), daemon=True).start()
        else:
            print(f"No se encontró {name}. Por favor, instálalo o configura la ruta.")

    def run_command(self, command):
        """
        Ejecuta un comando del sistema operativo para abrir una aplicación.

        Args:
            command (list): Comando a ejecutar (lista de argumentos).
        """
        try:
            subprocess.run(command, check=True)
        except Exception as e:
            print(f"Error al intentar abrir la aplicación: {e}")
