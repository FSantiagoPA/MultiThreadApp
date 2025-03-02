import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

class LanguageChart:
    def __init__(self, parent):
        """
        Inicializa el gráfico de los lenguajes de programación más usados.

        Args:
            parent (tk.Frame): Frame donde se colocará el gráfico.
        """
        self.parent = parent

        # Datos iniciales (puedes actualizar esto dinámicamente)
        self.languages = ["Python", "JavaScript", "Java", "C++", "C#"]
        self.usage = [30, 25, 20, 15, 10]  # Porcentajes de uso

        # Crear figura para el gráfico
        self.figure = Figure(figsize=(4, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.bar(self.languages, self.usage, color="skyblue")
        self.ax.set_title("Lenguajes más usados")
        self.ax.set_ylabel("Porcentaje de uso")

        # Embebiendo el gráfico en Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Iniciar hilo para actualizar el gráfico
        threading.Thread(target=self.update_chart, daemon=True).start()

    def fetch_data(self):
        """
        Simula la obtención de datos actualizados de lenguajes de programación.

        Returns:
            list: Lista de nuevos porcentajes de uso.
        """
        # Simulación: aquí puedes conectar a una API real
        self.usage = [value + 1 if value < 50 else value - 10 for value in self.usage]
        time.sleep(5)  # Simular retraso de actualización

    def update_chart(self):
        """
        Actualiza el gráfico periódicamente en un hilo.
        """
        while True:
            self.fetch_data()
            self.ax.clear()
            self.ax.bar(self.languages, self.usage, color="skyblue")
            self.ax.set_title("Lenguajes más usados")
            self.ax.set_ylabel("Porcentaje de uso")
            self.canvas.draw()
            time.sleep(5)  # Actualizar cada 5 segundos