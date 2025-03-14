#!/usr/bin/env python

import socket
import sys
from time import gmtime, strftime

HOST = '0.0.0.0'
PORT = 2908
MAX_PACKET_LENGTH = 20

def recvall(sock, msgLen):
    msg = b""  # Use bytes instead of string for Python 3
    bytesRcvd = 0

    while bytesRcvd < msgLen:
        chunk = sock.recv(msgLen - bytesRcvd)
        if not chunk:
            break
        bytesRcvd += len(chunk)
        msg += chunk

    return msg

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print(f"Bind failed. Error Code: {msg.errno} Message: {msg.strerror}")
    sys.exit()

s.listen(1000)

print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] TCP ECHO Server is waiting for incoming connections ...")

while True:
    connection, client_address = s.accept()

    try:
        print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Client {client_address} connected ...")

        while True:
            try:
                data = recvall(connection, MAX_PACKET_LENGTH)
                print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Client {client_address} sent '{data.decode('utf-8')}'")

                if data:
                    print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Sending back to client {client_address} ...")
                    connection.sendall(data)
                else:
                    print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Client {client_address} disconnected ...")
                    break
            except socket.error as e:
                print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Something happened, but I do not want to bother you ... {e}")

    finally:
        connection.close()