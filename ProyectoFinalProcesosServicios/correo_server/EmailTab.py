import tkinter as tk
from tkinter import ttk, messagebox
import threading

class MailTab:
    def __init__(self, parent, mail_client):
        self.mail_client = mail_client

        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Correo")

        # Campos para ingresar credenciales del usuario
        ttk.Label(self.frame, text="Correo electrónico:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_email = ttk.Entry(self.frame, width=40)
        self.entry_email.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Contraseña:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_password = ttk.Entry(self.frame, show="*", width=40)
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        # Campo para ingresar destinatario
        ttk.Label(self.frame, text="Destinatario:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_recipient = ttk.Entry(self.frame, width=40)
        self.entry_recipient.grid(row=2, column=1, padx=5, pady=5)

        # Campo para ingresar asunto
        ttk.Label(self.frame, text="Asunto:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.entry_subject = ttk.Entry(self.frame, width=40)
        self.entry_subject.grid(row=3, column=1, padx=5, pady=5)

        # Campo para escribir el mensaje
        ttk.Label(self.frame, text="Mensaje:").grid(row=4, column=0, sticky="ne", padx=5, pady=5)
        self.text_body = tk.Text(self.frame, width=50, height=10)
        self.text_body.grid(row=4, column=1, padx=5, pady=5)

        # Botón para enviar el correo
        self.send_button = ttk.Button(self.frame, text="Enviar", command=self.send_email_thread)
        self.send_button.grid(row=5, column=1, padx=5, pady=5, sticky="e")

    def send_email_thread(self):
        """Ejecuta el envío de correo en un hilo separado para no congelar la interfaz."""
        threading.Thread(target=self.send_email).start()

    def send_email(self):
        """Envía el correo utilizando el cliente de correo."""
        sender_email = self.entry_email.get()
        sender_password = self.entry_password.get()
        recipient = self.entry_recipient.get()
        subject = self.entry_subject.get()
        body = self.text_body.get("1.0", tk.END).strip()

        if not sender_email or not sender_password or not recipient or not subject or not body:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        result = self.mail_client.send_email(sender_email, sender_password, recipient, subject, body)
        messagebox.showinfo("Resultado", result)