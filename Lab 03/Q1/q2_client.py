import socket
import threading

HOST = 'localhost'
PORT = 9998

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Connected to chat server")

# Receive messages from server
def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            client.close()
            break

# Send messages to server
def send():
    while True:
        message = input()
        client.send(message.encode())

# Threads for sending and receiving
receive_thread = threading.Thread(target=receive)
send_thread = threading.Thread(target=send)

receive_thread.start()
send_thread.start()
