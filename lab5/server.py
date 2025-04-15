import socket
import random
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345
LOG_FILE = "guess_server_log.txt"

def log_event(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def guess_number_server(host=HOST, port=PORT):
    number_to_guess = random.randint(1, 100)
    print(f"[INFO] Serwer wystartował na {host}:{port}")
    print(f"[INFO] Wylosowana liczba: {number_to_guess}")
    log_event(f"Server started on {host}:{port} | Number to guess: {number_to_guess}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"[INFO] Oczekiwanie na połączenie...")

        client_socket, client_address = server_socket.accept()
        log_event(f"New connection from {client_address[0]}:{client_address[1]}")
        with client_socket:
            print(f"[INFO] Połączono z {client_address}")
            client_socket.sendall(b"Witaj w grze 'Zgadnij liczbe'! Zgadnij liczbe od 1 do 100.\n")

            while True:
                data = client_socket.recv(1024).decode('utf-8').strip()
                if not data:
                    break

                log_event(f"Received from {client_address[0]}:{client_address[1]}: {data}")
                
                try:
                    guess = int(data)
                    if guess < number_to_guess:
                        response = "Za malo\n"
                    elif guess > number_to_guess:
                        response = "Za duzo\n"
                    else:
                        response = "Gratulacje! Zgadles liczbe!\n"
                        client_socket.sendall(response.encode('utf-8'))
                        log_event(f"Client guessed the number correctly: {guess}")
                        break
                except ValueError:
                    response = "Blad: Podaj poprawna liczbe calkowita.\n"

                client_socket.sendall(response.encode('utf-8'))

    print("[INFO] Zakonczono gre. Serwer wylosuje nowa liczbe przy ponownym uruchomieniu.")

if __name__ == "__main__":
    guess_number_server()