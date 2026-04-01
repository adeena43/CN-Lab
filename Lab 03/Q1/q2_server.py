import socket
import threading

# Server setup
HOST = 'localhost'
PORT = 9998

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Chat server started...")
print("Waiting for clients...")

clients = []

# Broadcast message to all clients
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

# Handle individual client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break

# Accept incoming clients
def receive_connections():
    while True:
        client, addr = server.accept()
        print("Connected with", addr)

        clients.append(client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
