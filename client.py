import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(7632).decode()
            if message:
                print("\n" + message)
                print("Ketik pesan (format: 'to:<target_id> <message>' atau 'broadcast <message>') atau 'exit' untuk keluar: ", end="")
            else:
                break
        except Exception as e:
            print(f"Terjadi kesalahan dalam menerima pesan: {e}")
            break
    print("Koneksi ke server terputus.")
    sock.close()

def send_messages(sock):
    while True:
        try:
            message = input("Ketik pesan (format: 'to:<target_id> <message>' atau 'broadcast <message>') atau 'exit' untuk keluar: ")
            if message.lower() == 'exit':
                break
            sock.send(message.encode())
        except Exception as e:
            print(f"Terjadi kesalahan dalam mengirim pesan: {e}")
            break
    sock.close()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 7632))

client_name = input("Masukkan nama Anda: ")
client.send(client_name.encode())

receive_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
send_thread = threading.Thread(target=send_messages, args=(client,))

receive_thread.start()
send_thread.start()

send_thread.join()
client.close()
