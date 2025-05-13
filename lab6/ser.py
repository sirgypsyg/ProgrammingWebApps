import socket

def handle_request(request):
    try:
        lines = request.split("\r\n")
        request_line = lines[0]
        method, path, _ = request_line.split()

        if method == "GET":
            if path == "/":
                return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Witaj na serwerze HTTP!</h1>"
            elif path == "/test":
                return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Testowy zasób!</h1>"
            else:
                return "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 - Zasób nie znaleziony</h1>"
        else:
            return "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n<h1>405 - Metoda niedozwolona</h1>"
    
    except Exception as e:
        return f"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n<h1>500 - Błąd serwera: {str(e)}</h1>"

def run_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Serwer działa na {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        
        try:
            request = client_socket.recv(1024).decode("utf-8")
            response = handle_request(request)
            client_socket.sendall(response.encode("utf-8"))
        except Exception as e:
            print(f"Błąd przetwarzania żądania: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    run_server("127.0.0.1", 8080)