import socket
import threading

class Server:
    clients = {}

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        print("Server berjalan...")

    def listen(self):
        while True:
            client_socket, client_address = self.socket.accept()
            client_id = str(client_address[1])
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_id))
            client_thread.start()

    def handle_client(self, client_socket, client_id):
        try:
            client_name = client_socket.recv(7632).decode()
            Server.clients[client_id] = {'socket': client_socket, 'name': client_name}
            print(f"Client {client_id} ({client_name}) terhubung.")
            
            response_message = f"NOTENC:ID Anda adalah {client_id}. Gunakan format pesan 'to:<target_id> <message terenkripsi>' atau 'broadcast <message terenkripsi>' untuk mengirim pesan."
            client_socket.send(response_message.encode())

            while True:
                message = client_socket.recv(7632).decode()
                if message:
                    if message.startswith("to:"):
                        parts = message.split(" ", 2)
                        if len(parts) < 3:
                            continue
                        target_id = parts[1]
                        encrypted_message = parts[2]

                        if target_id in Server.clients:
                            target_socket = Server.clients[target_id]['socket']
                            sender_name = Server.clients[client_id]['name']
                            forward_message = f"Dari {sender_name} ({client_id}): {encrypted_message}"
                            target_socket.send(forward_message.encode())
                            print(f"Mengirim pesan dari {client_name} ke {Server.clients[target_id]['name']}: {encrypted_message}")
                        else:
                            client_socket.send(f"NOTENC:Client {target_id} tidak ditemukan.".encode())

                    elif message.startswith("broadcast"):
                        encrypted_message = message.split(" ", 1)[1]
                        broadcast_message = f"Broadcast dari {Server.clients[client_id]['name']} ({client_id}): {encrypted_message}"
                        print(f"Mengirim Broadcast dari {client_name}: {encrypted_message}")
                        for cid, client_info in Server.clients.items():
                            if cid != client_id:
                                client_info['socket'].send(broadcast_message.encode())
                else:
                    break
        except Exception as e:
            print(f"Kesalahan pada client {client_id}: {e}")
        
        client_socket.close()
        del Server.clients[client_id]
        print(f"Client {client_id} ({client_name}) terputus.")

if __name__ == '__main__':
    server = Server('127.0.0.1', 7632)
    server.listen()
