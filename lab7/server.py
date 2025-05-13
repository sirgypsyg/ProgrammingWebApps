import socket
import threading

HOST = "0.0.0.0"
PORT_TCP = 5001
PORT_UDP = 5002
BUFFER_SIZE = 1024

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_TCP))
        s.listen(1)
        print("[TCP] Czekam na połączenie...")
        conn, addr = s.accept()
        with conn:
            print(f"[TCP] Połączono z {addr}")
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break

def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT_UDP))
        print("[UDP] Odbieranie pakietów...")
        while True:
            data, addr = s.recvfrom(BUFFER_SIZE)
            if not data:
                break

# Uruchamiamy oba serwery równolegle
threading.Thread(target=tcp_server, daemon=True).start()
threading.Thread(target=udp_server, daemon=True).start()

# Serwer działa cały czas
input("Serwer działa... naciśnij Enter, by zakończyć\n")