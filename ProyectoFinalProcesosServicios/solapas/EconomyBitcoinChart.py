import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import random

class EconomyBitcoinChart:
    def __init__(self, parent):
        """
        Inicializa los gráficos de economía mundial y Bitcoin en disposición vertical.

        Args:
            parent (tk.Frame): Frame donde se colocarán los gráficos.
        """
        self.parent = parent

        # Crear la figura para los gráficos
        self.figure = Figure(figsize=(8, 6), dpi=100)

        # Subgráficos: Economía mundial y Bitcoin
        self.ax_economy = self.figure.add_subplot(211)  # Gráfico superior
        self.ax_bitcoin = self.figure.add_subplot(212)  # Gráfico inferior

        # Inicializar datos simulados
        self.economy_data = [random.randint(50, 100) for _ in range(10)]  # Economía en meses
        self.bitcoin_data = [random.randint(20000, 60000) for _ in range(10)]  # Bitcoin en días

        self.update_economy_chart()
        self.update_bitcoin_chart()

        # Embebiendo los gráficos en Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Iniciar hilos para actualizar los gráficos
        threading.Thread(target=self.update_charts, daemon=True).start()

    def update_economy_chart(self):
        """Actualiza el gráfico de economía mundial."""
        self.ax_economy.clear()
        self.ax_economy.plot(self.economy_data, marker="o", color="blue")
        self.ax_economy.set_title("Economía Mundial")
        self.ax_economy.set_ylabel("Índice económico")
        self.ax_economy.grid(True)

    def update_bitcoin_chart(self):
        """Actualiza el gráfico de Bitcoin."""
        self.ax_bitcoin.clear()
        self.ax_bitcoin.plot(self.bitcoin_data, marker="o", color="green")
        self.ax_bitcoin.set_title("Precio de Bitcoin")
        self.ax_bitcoin.set_ylabel("Precio en USD")
        self.ax_bitcoin.set_xlabel("Días")  # Etiqueta para los días
        self.ax_bitcoin.grid(True)

    def update_charts(self):
        """Actualiza ambos gráficos periódicamente."""
        while True:
            # Actualizar datos simulados
            self.economy_data = self.economy_data[1:] + [random.randint(50, 100)]  # Economía en meses
            self.bitcoin_data = self.bitcoin_data[1:] + [random.randint(20000, 60000)]  # Bitcoin en días

            # Actualizar gráficos
            self.update_economy_chart()
            self.update_bitcoin_chart()
            self.canvas.draw()

            # Esperar 5 segundos antes de la próxima actualización
            time.sleep(5)