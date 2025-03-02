import tkinter as tk
import threading
import time
import mysql.connector
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox

class WebScraperToDB:
    def __init__(self, parent):
        """
        Inicializa el widget de scraping con integración a base de datos.
        """
        self.parent = parent
        self.scraping_thread = None
        self.stop_event = threading.Event()

        # Crear campos de conexión para la base de datos
        db_frame = tk.Frame(self.parent)
        db_frame.pack(pady=5)

        tk.Label(db_frame, text="Host:").grid(row=0, column=0)
        self.host_entry = tk.Entry(db_frame)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1)

        tk.Label(db_frame, text="Usuario:").grid(row=1, column=0)
        self.user_entry = tk.Entry(db_frame)
        self.user_entry.insert(0, "root")
        self.user_entry.grid(row=1, column=1)

        tk.Label(db_frame, text="Contraseña:").grid(row=2, column=0)
        self.password_entry = tk.Entry(db_frame, show="*")
        self.password_entry.grid(row=2, column=1)

        tk.Label(db_frame, text="Nombre BD:").grid(row=3, column=0)
        self.database_entry = tk.Entry(db_frame)
        self.database_entry.insert(0, "scraping_db")
        self.database_entry.grid(row=3, column=1)

        tk.Button(db_frame, text="Crear Base de Datos", command=self.create_database).grid(row=4, column=0, columnspan=2, pady=5)

        # Área para URL y botones de control
        control_frame = tk.Frame(self.parent)
        control_frame.pack(pady=5)

        tk.Label(control_frame, text="URL para Scraping:").grid(row=0, column=0)
        self.url_entry = tk.Entry(control_frame, width=50)
        self.url_entry.insert(0, "https://quotes.toscrape.com/")
        self.url_entry.grid(row=0, column=1)

        # Campo para Selector HTML
        tk.Label(control_frame, text="Selector HTML:").grid(row=2, column=0)
        self.selector_entry = tk.Entry(control_frame, width=50)
        self.selector_entry.insert(0, "h1")  # Valor predeterminado
        self.selector_entry.grid(row=2, column=1)

        self.start_button = tk.Button(control_frame, text="Iniciar Scraping", command=self.start_scraping)
        self.start_button.grid(row=1, column=0, pady=5)

        self.stop_button = tk.Button(control_frame, text="Parar Scraping", command=self.stop_scraping, state="disabled")
        self.stop_button.grid(row=1, column=1, pady=5)

        self.reset_button = tk.Button(control_frame, text="Resetear Scraping", command=self.reset_database)
        self.reset_button.grid(row=1, column=2, pady=5)

        # Área para mostrar el estado
        self.status_label = tk.Label(self.parent, text="Estado: Inactivo", fg="red")
        self.status_label.pack(pady=5)

        # Área para mostrar los datos scrapeados
        self.scraped_data_frame = tk.Frame(self.parent)
        self.scraped_data_frame.pack(pady=5, fill="both", expand=True)

        tk.Label(self.scraped_data_frame, text="Datos Scrapeados:").pack(anchor="w")

        self.scraped_data_text = tk.Text(self.scraped_data_frame, height=10, state="disabled")
        self.scraped_data_text.pack(fill="both", expand=True)

    def create_database(self):
        """Crea la base de datos y la tabla para almacenar datos de scraping."""
        try:
            connection = mysql.connector.connect(
                host=self.host_entry.get(),
                user=self.user_entry.get(),
                password=self.password_entry.get()
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_entry.get()}")
            connection.database = self.database_entry.get()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scraped_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.close()
            messagebox.showinfo("Éxito", "Base de datos y tabla creadas correctamente.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", str(e))

    def start_scraping(self):
        """Inicia el scraping en un hilo separado."""
        if self.scraping_thread and self.scraping_thread.is_alive():
            messagebox.showwarning("Aviso", "El scraping ya está en ejecución.")
            return
        self.stop_event.clear()
        self.scraping_thread = threading.Thread(target=self.scrape_data, daemon=True)
        self.scraping_thread.start()
        self.status_label.config(text="Estado: Ejecutando...", fg="green")
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def scrape_data(self):
        """Realiza el scraping de manera continua y guarda los datos en la base de datos."""
        url = self.url_entry.get()
        selector = self.selector_entry.get()

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            connection = mysql.connector.connect(
                host=self.host_entry.get(),
                user=self.user_entry.get(),
                password=self.password_entry.get(),
                database=self.database_entry.get()
            )
            cursor = connection.cursor()

            while not self.stop_event.is_set():
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")

                # Busca elementos según el selector ingresado por el usuario
                elements = soup.select(selector)
                if not elements:
                    self.status_label.config(text="Estado: Sin datos encontrados.", fg="orange")
                    time.sleep(5)  # Pausa antes de intentar de nuevo
                    continue

                for element in elements:
                    title_text = element.get_text(strip=True)
                    link = element.get("href", "Sin enlace")  # Asegúrate de que el selector apunte a elementos <a>

                    # Insertar en la base de datos
                    cursor.execute("INSERT INTO scraped_data (title, link) VALUES (%s, %s)", (title_text, link))
                    connection.commit()

                    # Mostrar en la interfaz
                    self.scraped_data_text.config(state="normal")
                    self.scraped_data_text.insert("end", f"{title_text} - {link}\n")
                    self.scraped_data_text.see("end")
                    self.scraped_data_text.config(state="disabled")

                    self.status_label.config(text=f"Estado: Scrapeando {title_text}...", fg="green")

                # Pausa entre iteraciones
                time.sleep(5)

            connection.close()
            self.status_label.config(text="Estado: Inactivo", fg="red")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_label.config(text="Estado: Error", fg="red")

    def stop_scraping(self):
        """Detiene el proceso de scraping."""
        self.stop_event.set()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def reset_database(self):
        """Elimina todos los datos de la tabla."""
        try:
            connection = mysql.connector.connect(
                host=self.host_entry.get(),
                user=self.user_entry.get(),
                password=self.password_entry.get(),
                database=self.database_entry.get()
            )
            cursor = connection.cursor()
            cursor.execute("TRUNCATE TABLE scraped_data")
            connection.commit()
            connection.close()
            messagebox.showinfo("Éxito", "Datos reseteados correctamente.")

            # Limpiar el cuadro de texto
            self.scraped_data_text.config(state="normal")
            self.scraped_data_text.delete("1.0", "end")
            self.scraped_data_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))