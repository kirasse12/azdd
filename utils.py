import os
import struct
from datetime import datetime

def receive_data(conn):
    try:
        length_bytes = conn.recv(4)
        if not length_bytes:
            return None
        length = struct.unpack('!I', length_bytes)[0]
        return conn.recv(length).decode()
    except Exception as e:
        print(f"[!] Erreur de réception des données : {e}")
        return None

def receive_file(conn, filesize, save_path):
    with open(save_path, 'wb') as f:
        received = 0
        while received < filesize:
            chunk = conn.recv(min(4096, filesize - received))
            if not chunk:
                break
            f.write(chunk)
            received += len(chunk)
        print(f"[✓] Fichier sauvegardé : {save_path}")

def save_file(conn, data_type, data_dir):
    filename = receive_data(conn)
    filesize_str = receive_data(conn)

    if not filename or not filesize_str:
        print(f"[-] Échec de réception des infos fichier {data_type}")
        return

    try:
        filesize = int(filesize_str)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = os.path.splitext(filename)[-1]
        folder = os.path.join(data_dir, data_type)
        os.makedirs(folder, exist_ok=True)
        save_path = os.path.join(folder, f"{timestamp}{file_ext}")
        receive_file(conn, filesize, save_path)
    except ValueError:
        print("[-] Taille de fichier invalide.")

def handle_client_command(conn, command):
    print(f"[!] Commande inconnue ou donnée non supportée : {command}")
