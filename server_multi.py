import socket
from threading import Thread
from des import *


# while True:
#     key = input("Masukkan key anda: ")
#
#     if len(key) == 8:
#         break
#     else:
#         print("Key harus 8 karakter")
#
# key = str2hex(key)
# rkb,rk = generate_round_key(key)

# def handle_key(client):
#     if key == client:
#         return True
#
#     return False

class Server:
    Clients = []

    # Create a TCP socket over IPv4. Accept at max 5 connections.
    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        self.rk = []
        self.rkb = []
        print('Server waiting for connection....')

    def listen(self):
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Connection from {client_address}")

            client_key = client_socket.recv(1024).decode()

            print(client_key)

            self.rkb, self.rk = generate_round_key(client_key)

            # if not handle_key(client_key):
            #   print(f"Key from {client_address} is invalid")
            #   client_socket.close()
            #   continue

            client_name = client_socket.recv(1024).decode()
            client = {'client_name': client_name, 'client_socket': client_socket}

            message = f"Welcome, {client_name} has joined the chat!"
            message = pad(message)
            encrypted_text = encrypt(message, self.rkb, self.rk)

            self.broadcast_message(client_name, encrypted_text)

            Server.Clients.append(client)
            Thread(target=self.handle_new_client, args=(client,)).start()

    def handle_new_client(self, client):
        client_name = client['client_name']
        client_socket = client['client_socket']

        try:
            while True:
                try:
                    client_message = client_socket.recv(1024).decode()

                    # Check for exit message or empty message indicating disconnection
                    if client_message.strip() == client_name + ": exit" or not client_message.strip():
                        message = f"{client_name} has left the chat!"
                        message = pad(message)
                        encrypted_text = encrypt(message, self.rkb, self.rk)
                        self.broadcast_message(client_name, encrypted_text)

                        # Remove client from the list and close the socket
                        Server.Clients.remove(client)
                        client_socket.close()
                        break
                    else:
                        # Send the message to all other clients
                        self.broadcast_message(client_name, client_message)

                except ConnectionResetError:
                    # Handle unexpected client disconnection
                    print(f"{client_name} has unexpectedly disconnected.")
                    break

        finally:
            # Ensure cleanup if disconnection occurs
            if client in Server.Clients:
                Server.Clients.remove(client)
            client_socket.close()

    def broadcast_message(self, sender_name, message):
        for client in self.Clients:
            client_socket = client['client_socket']
            client_name = client['client_name']
            try:
                if client_name != sender_name:
                    client_socket.send(message.encode())
            except BrokenPipeError:
                print(f"Connection to {client_name} has been lost.")
                self.Clients.remove(client)


if __name__ == '__main__':
    server = Server('127.0.0.1', 7632)
    server.listen()
