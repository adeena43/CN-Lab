import socket
import threading
import os

HOST = 'localhost'
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to chat server")

# ---------------- RECEIVE THREAD ----------------
def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg:
                print(msg)
        except:
            client.close()
            break

# ---------------- SEND THREAD ----------------
def send():
    while True:
        msg = input()

        # -------- FILE SEND --------
        if msg.startswith("send "):
            filename = msg.split(" ", 1)[1]

            if not os.path.exists(filename):
                print("File not found")
                continue

            filesize = os.path.getsize(filename)

            # Send file header
            client.send(f"FILE:{filename}".encode())
            client.send(str(filesize).encode())

            # Send file data
            with open(filename, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client.send(data)

            # WAIT FOR SERVER FEEDBACK
            response = client.recv(1024).decode()
            print(response)
            continue

        # -------- NORMAL MESSAGE --------
        client.send(msg.encode())

# Start threads
receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

receive_thread.start()
send_thread.start()
