import time
import tkinter as tk
from tkinter import messagebox
import threading
import random


class TicTacToe:
    def __init__(self, parent):
        """
        Inicializa el juego de Tic Tac Toe.

        Args:
            parent (tk.Frame): Frame donde se colocará el juego.
        """
        self.parent = parent
        self.board = [""] * 9  # Tablero de 3x3 representado como una lista
        self.current_player = "X"  # Jugador inicial
        self.vs_computer = False  # Modo jugador vs máquina

        # Etiqueta para el título
        title = tk.Label(self.parent, text="Tic Tac Toe", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        # Botón para alternar entre modos
        self.mode_button = tk.Button(self.parent, text="Modo: Jugador vs Jugador", command=self.toggle_mode)
        self.mode_button.pack(pady=5)

        # Crear el tablero
        self.buttons = []
        self.board_frame = tk.Frame(self.parent)
        self.board_frame.pack()

        for i in range(9):
            button = tk.Button(
                self.board_frame,
                text="",
                font=("Helvetica", 20),
                width=5,
                height=2,
                command=self.create_button_command(i)  # Aquí usamos la función auxiliar
            )
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        # Etiqueta para el estado del juego
        self.status_label = tk.Label(self.parent, text="Turno: X", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

    def toggle_mode(self):
        """Alterna entre los modos Jugador vs Jugador y Jugador vs Máquina."""
        self.vs_computer = not self.vs_computer
        mode_text = "Modo: Jugador vs Máquina" if self.vs_computer else "Modo: Jugador vs Jugador"
        self.mode_button.config(text=mode_text)
        self.reset_game()

    def reset_game(self):
        """Reinicia el tablero y el estado del juego."""
        self.board = [""] * 9
        self.current_player = "X"
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)
        self.status_label.config(text="Turno: X")

    def make_move(self, index):
        """Realiza un movimiento en el tablero."""
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            # Verificar si hay un ganador
            winner = self.check_winner()
            if winner:
                self.end_game(f"¡Ganador: {winner}!")
                return
            elif "" not in self.board:
                self.end_game("¡Empate!")
                return

            # Cambiar de jugador
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Turno: {self.current_player}")

            # Si está en modo Jugador vs Máquina y es el turno de la máquina
            if self.vs_computer and self.current_player == "O":
                threading.Thread(target=self.computer_move).start()

    def computer_move(self):
        """Simula el movimiento de la máquina."""
        self.status_label.config(text="Turno: Máquina (O)")
        available_moves = [i for i, v in enumerate(self.board) if v == ""]
        move = random.choice(available_moves)

        def delayed_move():
            time.sleep(1)  # Simular el tiempo de "pensar"
            self.make_move(move)

        threading.Thread(target=delayed_move).start()

    def check_winner(self):
        """Verifica si hay un ganador."""
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Filas
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columnas
            (0, 4, 8), (2, 4, 6)  # Diagonales
        ]
        for a, b, c in winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != "":
                return self.board[a]
        return None

    def end_game(self, message):
        """Finaliza el juego mostrando un mensaje."""
        messagebox.showinfo("Fin del Juego", message)
        self.reset_game()

    def create_button_command(self, index):
            """Crea un comando para un botón con un índice específico."""

            def command():
                self.make_move(index)

            return command