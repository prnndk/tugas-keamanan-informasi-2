import socket
from threading import Thread
from des import *

clients = {}

def handle_client(client_socket, client_id):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Pesan dari {client_id}: {message}")

                if message.startswith("to:"):
                    # Kirim ke client tertentu
                    target_id, actual_message = message[3:].split(" ", 1)
                    target_id = target_id.strip()

                    if target_id in clients:
                        target_socket = clients[target_id]
                        forward_message = f"Dari {client_id}: {actual_message}"
                        target_socket.send(forward_message.encode())
                    else:
                        client_socket.send(f"Client {target_id} tidak ditemukan.".encode())

                elif message.startswith("broadcast"):
                    broadcast_message = f"[Broadcast dari {client_id}]: {message[10:]}"
                    for cid, sock in clients.items():
                        if cid != client_id:  # Jangan kirim kembali ke pengirim
                            sock.send(broadcast_message.encode())

            else:
                break
        except:
            break

    client_socket.close()
    del clients[client_id]
    print(f"Client {client_id} terputus.")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen(5)
print("Server berjalan dan menunggu koneksi...")

while True:
    client_socket, client_address = server.accept()
    client_id = str(client_address[1])
    clients[client_id] = client_socket
    print(f"Client {client_id} terhubung dari {client_address}")

    client_socket.send(f"ID Anda adalah {client_id}. Gunakan format pesan 'to:<target_id> <message>' atau 'broadcast <message>' untuk mengirim pesan.".encode())
    client_thread = Thread(target=handle_client, args=(client_socket, client_id))
    client_thread.start()
