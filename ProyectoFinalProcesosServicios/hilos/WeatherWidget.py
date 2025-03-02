import tkinter as tk
import threading
import requests
import time


class WeatherWidget:
    def __init__(self, parent, api_key):
        """
        Inicializa el widget del clima con detalles adicionales.

        Args:
            parent (tk.Frame): Frame en el que se colocará el widget.
            api_key (str): Clave de la API de OpenWeatherMap.
        """
        self.parent = parent
        self.api_key = api_key

        # Crear un Frame para contener los datos
        self.frame = tk.Frame(self.parent, bg="white", bd=2, relief="groove")
        self.frame.pack(padx=10, pady=10, fill="x", anchor="n")

        # Encabezado del clima
        self.header_label = tk.Label(self.frame, text="Weather in ...", font=("Helvetica", 14, "bold"), bg="white")
        self.header_label.pack(pady=5)

        # Temperatura principal
        self.temp_label = tk.Label(self.frame, text="--°C", font=("Helvetica", 28, "bold"), bg="white")
        self.temp_label.pack()

        # Detalles adicionales
        self.details_label = tk.Label(self.frame, text="", font=("Helvetica", 12), bg="white", justify="left")
        self.details_label.pack(pady=5)

        # Iniciar el hilo para actualizar el clima
        self.start_weather_updates()

    def get_location(self):
        """
        Obtiene la ubicación actual (latitud y longitud) usando ip-api.
        """
        try:
            response = requests.get("http://ip-api.com/json/")
            response.raise_for_status()
            data = response.json()
            return data["lat"], data["lon"], data["city"]
        except Exception as e:
            return None, None, f"Error al obtener ubicación: {e}"

    def get_weather(self, lat, lon):
        """
        Obtiene el clima actual usando OpenWeatherMap.

        Args:
            lat (float): Latitud de la ubicación.
            lon (float): Longitud de la ubicación.
        """
        try:
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
            response = requests.get(weather_url)
            response.raise_for_status()
            data = response.json()

            # Información principal
            city = data["name"]
            temp = data["main"]["temp"]
            real_feel = data["main"]["feels_like"]
            wind_speed = data["wind"]["speed"]
            wind_gusts = data["wind"].get("gust", "N/A")
            weather = data["weather"][0]["description"].capitalize()

            # Obtener calidad del aire (Air Quality)
            air_quality = self.get_air_quality(lat, lon)

            # Formatear detalles adicionales
            details = (
                f"RealFeel: {real_feel}°\n"
                f"Wind: {wind_speed} km/h\n"
                f"Wind Gusts: {wind_gusts} km/h\n"
                f"Air Quality: {air_quality}"
            )

            return city, temp, details
        except Exception as e:
            return None, None, f"Error al obtener el clima: {e}"

    def get_air_quality(self, lat, lon):
        """
        Obtiene la calidad del aire usando OpenWeatherMap.

        Args:
            lat (float): Latitud.
            lon (float): Longitud.
        """
        try:
            aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}"
            response = requests.get(aqi_url)
            response.raise_for_status()
            data = response.json()
            aqi = data["list"][0]["main"]["aqi"]

            # Mapear AQI a descripciones
            aqi_mapping = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
            return aqi_mapping.get(aqi, "Unknown")
        except Exception as e:
            return f"Error: {e}"

    def update_weather(self):
        """
        Actualiza la información del clima periódicamente.
        """
        while True:
            lat, lon, location_info = self.get_location()
            if lat and lon:
                city, temp, details = self.get_weather(lat, lon)
                self.header_label.config(text=f"Weather in {city}")
                self.temp_label.config(text=f"{temp}°C")
                self.details_label.config(text=details)
            else:
                self.header_label.config(text=location_info)  # Error de ubicación

            time.sleep(60)  # Actualizar cada 60 segundos

    def start_weather_updates(self):
        """
        Inicia el hilo para actualizar el clima.
        """
        weather_thread = threading.Thread(target=self.update_weather, daemon=True)
        weather_thread.start()
