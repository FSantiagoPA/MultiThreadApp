import tkinter as tk
from tkinter import ttk, messagebox
import threading
import mysql.connector
from mysql.connector import Error


class SQLQueryExecutor:
    def __init__(self, parent):
        """
        Clase para ejecutar consultas SQL en una base de datos MySQL.

        Args:
            parent (tk.Frame): Frame donde se colocarán los widgets.
        """
        self.parent = parent

        # Campos para ingresar información de conexión
        self.db_info_frame = tk.Frame(self.parent)
        self.db_info_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(self.db_info_frame, text="Host:").grid(row=0, column=0, sticky="w")
        self.host_entry = tk.Entry(self.db_info_frame)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1)

        tk.Label(self.db_info_frame, text="Usuario:").grid(row=1, column=0, sticky="w")
        self.user_entry = tk.Entry(self.db_info_frame)
        self.user_entry.insert(0, "root")
        self.user_entry.grid(row=1, column=1)

        tk.Label(self.db_info_frame, text="Contraseña:").grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(self.db_info_frame, show="*")
        self.password_entry.grid(row=2, column=1)

        tk.Label(self.db_info_frame, text="Base de datos:").grid(row=3, column=0, sticky="w")
        self.database_entry = tk.Entry(self.db_info_frame)
        self.database_entry.grid(row=3, column=1)

        # Botón para conectar a la base de datos
        self.connect_button = tk.Button(self.db_info_frame, text="Conectar", command=self.connect_to_database)
        self.connect_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Área para ingresar consultas SQL
        self.query_frame = tk.Frame(self.parent)
        self.query_frame.pack(pady=10, padx=10, fill="both", expand=True)

        tk.Label(self.query_frame, text="Consulta SQL:").pack(anchor="w")
        self.query_text = tk.Text(self.query_frame, height=10)
        self.query_text.pack(fill="both", expand=True)

        # Botón para ejecutar consultas
        self.execute_button = tk.Button(self.query_frame, text="Ejecutar", command=self.execute_query)
        self.execute_button.pack(pady=5)

        # Área para mostrar resultados
        self.result_frame = tk.Frame(self.parent)
        self.result_frame.pack(pady=10, padx=10, fill="both", expand=True)

        tk.Label(self.result_frame, text="Resultados:").pack(anchor="w")
        self.result_text = tk.Text(self.result_frame, height=10, state="disabled")
        self.result_text.pack(fill="both", expand=True)

    def connect_to_database(self):
        """Conecta a la base de datos utilizando los datos proporcionados."""
        self.host = self.host_entry.get()
        self.user = self.user_entry.get()
        self.password = self.password_entry.get()
        self.database = self.database_entry.get()

        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                messagebox.showinfo("Conexión Exitosa", "Conectado a la base de datos")
        except Error as e:
            messagebox.showerror("Error de Conexión", str(e))

    def execute_query(self):
        """Ejecuta la consulta SQL en un hilo separado."""
        query = self.query_text.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Consulta Vacía", "Por favor, ingrese una consulta SQL.")
            return

        threading.Thread(target=self.run_query, args=(query,), daemon=True).start()

    def run_query(self, query):
        """Ejecuta la consulta y muestra los resultados."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]

                # Mostrar los resultados
                self.result_text.config(state="normal")
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, "\t".join(column_names) + "\n")
                for row in rows:
                    self.result_text.insert(tk.END, "\t".join(map(str, row)) + "\n")
                self.result_text.config(state="disabled")
            else:
                self.connection.commit()
                messagebox.showinfo("Éxito", "Consulta ejecutada correctamente.")
        except Error as e:
            messagebox.showerror("Error de Consulta", str(e))
