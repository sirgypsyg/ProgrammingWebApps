import socket

HOST = '127.0.0.1'
PORT = 2525  

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

conn, addr = server_socket.accept()

#Powitanie SMTP
conn.send(b"welcome to SMTP server\r\n")

while True:
    data = conn.recv(1024).decode().strip()
    if not data:
        break

    print(f"< {data}")

    cmd = data.upper()

    if cmd.startswith("EHLO") or cmd.startswith("HELO"):
        conn.send(b"250 Hello localhost\r\n")

    elif cmd.startswith("MAIL FROM"):
        conn.send(b"250 OK\r\n")

    elif cmd.startswith("RCPT TO"):
        conn.send(b"250 OK\r\n")

    elif cmd == "DATA":
        conn.send(b"354 End with <CR><LF>.<CR><LF>\r\n")
        # Odbieramy dane wiadomości do momentu linii z kropką
        message_lines = []
        while True:
            line = conn.recv(1024).decode().strip()
            if line == ".":
                break
            message_lines.append(line)
        print("Wiadomość została zasymulowana.")
        conn.send(b"250 Message accepted for delivery\r\n")

    elif cmd == "QUIT":
        conn.send(b"221 Bye\r\n")
        break

    else:
        conn.send(b"502 Command not implemented\r\n")

conn.close()
server_socket.close()
print("Serwer zakończył działanie.")