import socket
from threading import Thread
import os
from des import *

class Client:

    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        while True:
            key = input("Masukkan key anda: ")

            if len(key) == 8:
                break
            else:
                print("Key harus 8 karakter")

        self.key = str2hex(key)
        self.rkb, self.rk = generate_round_key(self.key)
        self.socket.send(self.key.encode())

        self.name = input("Enter your name: ")

        self.talk_to_server()

    def talk_to_server(self):
        self.socket.send(self.name.encode())
        Thread(target=self.receive_message).start()
        self.send_message()

    def send_message(self):
        while True:
            try:
                client_input = input("")

                if client_input.lower() == 'exit':
                    self.socket.close()
                    os._exit(0)

                client_message = self.name + ": " + client_input

                client_message = pad(client_message)
                encrypted_text = encrypt(client_message,self.rkb,self.rk)
                self.socket.send(encrypted_text.encode())
            except Exception as e:
                print(f"Error sending message: {e}")
                break

    def receive_message(self):
        while True:
            server_message = self.socket.recv(1024).decode()
            if not server_message.strip():
                os._exit(0)

            try:
                if server_message:
                    server_message = decrypt(server_message,self.rkb,self.rk)
                    print("\033[1;31;40m" + server_message + "\033[0m")
            except Exception as e:
                print(f"Error receiving message: {e}")
                continue

if __name__ == '__main__':
    Client('127.0.0.1', 7632)