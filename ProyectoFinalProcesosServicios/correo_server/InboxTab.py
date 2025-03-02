import tkinter as tk
from tkinter import ttk, messagebox
import threading

class InboxTab:
    def __init__(self, parent, email_client):
        self.email_client = email_client

        self.frame = ttk.Frame(parent)
        parent.add(self.frame, text="Bandeja de Entrada")

        ttk.Label(self.frame, text="Correo electrónico:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_email = ttk.Entry(self.frame, width=40)
        self.entry_email.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Contraseña:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_password = ttk.Entry(self.frame, show="*", width=40)
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        self.load_button = ttk.Button(self.frame, text="Cargar Correos", command=self.load_emails_thread)
        self.load_button.grid(row=2, column=1, sticky="e", padx=5, pady=5)

        self.email_listbox = tk.Listbox(self.frame, width=80, height=20)
        self.email_listbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.email_listbox.bind("<Double-Button-1>", self.show_email)

        self.delete_button = ttk.Button(self.frame, text="Eliminar Correo", command=self.delete_email_thread)
        self.delete_button.grid(row=4, column=1, sticky="e", padx=5, pady=5)

        self.emails = []

    def load_emails_thread(self):
        threading.Thread(target=self.load_emails).start()

    def delete_email_thread(self):
        threading.Thread(target=self.delete_email).start()

    def load_emails(self):
        email_address = self.entry_email.get()
        password = self.entry_password.get()

        if not email_address or not password:
            messagebox.showerror("Error", "Debe ingresar su correo y contraseña.")
            return

        self.emails = []
        self.email_listbox.delete(0, tk.END)

        emails = self.email_client.fetch_emails(email_address, password)

        if isinstance(emails, str):
            messagebox.showerror("Error", emails)
            return

        for email_id, subject, sender in emails:
            self.email_listbox.insert(tk.END, f"{subject} - {sender}")
            self.emails.append((email_id, subject, sender))

    def delete_email(self):
        selected_index = self.email_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Advertencia", "Seleccione un correo para eliminar.")
            return

        email_id, _, _ = self.emails[selected_index[0]]
        email_address = self.entry_email.get()
        password = self.entry_password.get()

        result = self.email_client.delete_email(email_address, password, email_id)

        if "eliminado" in result:
            self.email_listbox.delete(selected_index)
            messagebox.showinfo("Éxito", result)
        else:
            messagebox.showerror("Error", result)

    def show_email(self, event):
        selected_index = self.email_listbox.curselection()
        if selected_index:
            email_id, subject, sender = self.emails[selected_index[0]]
            messagebox.showinfo("Correo", f"Asunto: {subject}\nDe: {sender}")
