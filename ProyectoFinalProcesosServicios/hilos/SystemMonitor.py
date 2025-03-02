import psutil
import threading
import tkinter as tk

class SystemMonitor:
    def __init__(self, parent, stop_event):
        self.parent = parent
        self.stop_event = stop_event

        # Crear labels para cada métrica
        self.cpu_label = tk.Label(parent, text="CPU: 0%", bg="lightgreen", font=("Helvetica", 12), relief="groove")
        self.ram_label = tk.Label(parent, text="RAM: 0%", bg="lightcoral", font=("Helvetica", 12), relief="groove")
        self.battery_label = tk.Label(parent, text="Battery: N/A", bg="lightblue", font=("Helvetica", 12), relief="groove")
        self.network_label = tk.Label(parent, text="Net: N/A", bg="lightpink", font=("Helvetica", 12), relief="groove")

        # Posicionar los labels
        self.cpu_label.pack(side="left", fill="both", expand=True)
        self.ram_label.pack(side="left", fill="both", expand=True)
        self.battery_label.pack(side="left", fill="both", expand=True)
        self.network_label.pack(side="left", fill="both", expand=True)

        # Iniciar hilos
        threading.Thread(target=self.update_cpu, daemon=True).start()
        threading.Thread(target=self.update_ram, daemon=True).start()
        threading.Thread(target=self.update_battery, daemon=True).start()
        threading.Thread(target=self.update_network, daemon=True).start()

    def update_cpu(self):
        """Actualizar el uso de CPU."""
        while not self.stop_event.is_set():
            cpu_usage = psutil.cpu_percent()
            self.cpu_label.config(text=f"CPU: {cpu_usage}%")
            self.cpu_label.after(1000, lambda: None)  # Evitar bloqueo
            self.stop_event.wait(1)

    def update_ram(self):
        """Actualizar el uso de RAM."""
        while not self.stop_event.is_set():
            ram_usage = psutil.virtual_memory().percent
            self.ram_label.config(text=f"RAM: {ram_usage}%")
            self.ram_label.after(1000, lambda: None)  # Evitar bloqueo
            self.stop_event.wait(1)

    def update_battery(self):
        """Actualizar el estado de la batería."""
        while not self.stop_event.is_set():
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                time_left = battery.secsleft // 3600 if battery.secsleft > 0 else "N/A"
                self.battery_label.config(text=f"Battery: {percent}%, ({time_left}h left)")
            else:
                self.battery_label.config(text="Battery: N/A")
            self.battery_label.after(1000, lambda: None)  # Evitar bloqueo
            self.stop_event.wait(5)

    def update_network(self):
        """Actualizar el uso de red."""
        old_sent = psutil.net_io_counters().bytes_sent
        old_recv = psutil.net_io_counters().bytes_recv
        while not self.stop_event.is_set():
            new_sent = psutil.net_io_counters().bytes_sent
            new_recv = psutil.net_io_counters().bytes_recv
            sent_mb = (new_sent - old_sent) / (1024 * 1024)
            recv_mb = (new_recv - old_recv) / (1024 * 1024)
            self.network_label.config(text=f"Net: {sent_mb:.2f} MB sent, {recv_mb:.2f} MB recv")
            old_sent, old_recv = new_sent, new_recv
            self.network_label.after(1000, lambda: None)  # Evitar bloqueo
            self.stop_event.wait(1)
