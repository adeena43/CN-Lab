import socket
import threading
import os

HOST = 'localhost'
PORT = 9999

# Allowed file extensions
ALLOWED_EXTENSIONS = ['.txt', '.jpg', '.pdf']

# Banned words
BANNED_WORDS = ['bad', 'hate', 'stupid']

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Chat server started...")
print("Waiting for clients...")

clients = []

# Send message to all clients except sender
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)

# Handle each client
def handle_client(client):
    while True:
        try:
            msg = client.recv(1024).decode()

            if not msg:
                break

            # ---------- FILE HANDLING ----------
            if msg.startswith("FILE:"):
                filename = msg.split(":", 1)[1]
                ext = os.path.splitext(filename)[1]

                # ❌ Reject file type
                if ext not in ALLOWED_EXTENSIONS:
                    client.send("Server: File type not allowed".encode())
                    continue

                # ✅ Accept file
                filesize = int(client.recv(1024).decode())

                with open(filename, "wb") as f:
                    received = 0
                    while received < filesize:
                        data = client.recv(1024)
                        f.write(data)
                        received += len(data)

                # Feedback
                client.send("Server: File accepted".encode())
                broadcast(f"Server: File received ({filename})".encode(), client)
                continue

            # ---------- MESSAGE VALIDATION ----------
            if any(word in msg.lower() for word in BANNED_WORDS):
                client.send("Server: Message contains banned words".encode())
                continue

            # Normal message
            broadcast(msg.encode(), client)

        except:
            if client in clients:
                clients.remove(client)
            client.close()
            break

# Accept clients
def receive_connections():
    while True:
        client, addr = server.accept()
        print("Connected with", addr)
        clients.append(client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
