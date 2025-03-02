import tkinter as tk
from tkinter import scrolledtext
import socket
import threading


class ChatWidget:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg="lightgreen", width=200, height=300)  # Ajustar tamaño del frame
        self.frame.pack(fill="x", expand=False, padx=10, pady=10)

        # Label superior
        self.label = tk.Label(self.frame, text="Chat", font=("Arial", 14, "bold"), fg="red", bg="lightgreen")
        self.label.pack(pady=5)

        # Caja de texto para los mensajes
        self.chat_display = scrolledtext.ScrolledText(
            self.frame, wrap=tk.WORD, state="disabled", width=40, height=10  # Reducir dimensiones
        )
        self.chat_display.pack(pady=5)

        # Campo de entrada para escribir mensajes
        self.message_entry = tk.Entry(self.frame, width=35)  # Reducir ancho
        self.message_entry.pack(pady=5)
        self.message_entry.bind("<Return>", self.send_message)

        # Botón para enviar mensajes
        self.send_button = tk.Button(self.frame, text="Enviar", command=self.send_message, width=10)  # Reducir tamaño
        self.send_button.pack(pady=5)

        # Configuración del cliente socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ("127.0.0.1", 3333)  # Cambiar a la IP del servidor si es necesario

        try:
            self.client_socket.connect(self.server_address)
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.display_message(f"[ERROR] No se pudo conectar al servidor: {e}")

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            try:
                self.client_socket.send(message.encode("utf-8"))
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.display_message(f"[ERROR] No se pudo enviar el mensaje: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                if message:
                    self.display_message(message)
                else:
                    break
            except:
                self.display_message("[DESCONECTADO] Conexión perdida con el servidor.")
                break

    def display_message(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def close_connection(self):
        try:
            self.client_socket.close()
        except:
            pass