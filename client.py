import socket
import threading
from des import *

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print("\n" + message)
            else:
                break
        except Exception as e:
            print(f"Terjadi kesalahan dalam menerima pesan: {e}")
            break
    print("Koneksi ke server terputus.")
    sock.close()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
thread.start()

client_id = client.recv(1024).decode()
print(client_id)

try:
    while True:
        print("Ketik pesan (format: 'to:<target_id> <message>' atau 'broadcast <message>') atau 'exit' untuk keluar: ")
        message = input()
        if message.lower() == 'exit':
            break
        client.send(message.encode())
except KeyboardInterrupt:
    print("Keluar dari aplikasi.")

client.close()
