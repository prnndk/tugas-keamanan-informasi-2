import socket
import threading

clients = {}

def handle_client(client_socket, client_id):
    try:
        client_name = client_socket.recv(7632).decode()
        clients[client_id] = {'socket': client_socket, 'name': client_name}
        print(f"Client {client_id} ({client_name}) terhubung.")
        
        client_socket.send(f"ID Anda adalah {client_id}. Gunakan format pesan 'to:<target_id> <message>' atau 'broadcast <message>' untuk mengirim pesan.".encode())

        while True:
            message = client_socket.recv(7632).decode()
            if message:
                print(f"Pesan dari {client_name} ({client_id}): {message}")

                if message.startswith("to:"):
                    target_id, actual_message = message[3:].split(" ", 1)
                    target_id = target_id.strip()

                    if target_id in clients:
                        target_socket = clients[target_id]['socket']
                        sender_name = clients[client_id]['name']
                        forward_message = f"Dari {sender_name} ({client_id}): {actual_message}"
                        target_socket.send(forward_message.encode())
                    else:
                        client_socket.send(f"Client {target_id} tidak ditemukan.".encode())

                elif message.startswith("broadcast"):
                    broadcast_message = f"[Broadcast dari {clients[client_id]['name']} ({client_id})]: {message[10:]}"
                    for cid, client_info in clients.items():
                        if cid != client_id:
                            client_info['socket'].send(broadcast_message.encode())
            else:
                break
    except Exception as e:
        print(f"Kesalahan pada client {client_id}: {e}")
    
    client_socket.close()
    del clients[client_id]
    print(f"Client {client_id} ({client_name}) terputus.")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 7632))
server.listen(5)
print("Server berjalan dan menunggu koneksi...")

while True:
    client_socket, client_address = server.accept()
    client_id = str(client_address[1])
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
    client_thread.start()
