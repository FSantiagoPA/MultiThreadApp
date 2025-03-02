import socket
import threading

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 3333
clients = []

# Manejo de cada cliente
def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"[{address}] {message}")
                broadcast(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            remove_client(client_socket)
            break

# Difusión de mensajes a todos los clientes conectados
def broadcast(message, sender_socket=None):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except Exception as e:
            remove_client(client)


# Eliminar cliente desconectado
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

# Configuración del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Servidor escuchando en {HOST}:{PORT}")

while True:
    client_socket, address = server.accept()
    print(f"Conexión establecida con {address}")
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, address)).start()
