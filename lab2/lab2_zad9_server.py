#!/usr/bin/env python

import socket
import sys
from time import gmtime, strftime

HOST = '127.0.0.1'
PORT = 2906

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.bind((HOST, PORT))
except socket.error as msg:
    print(f"Bind failed. Error Code: {msg.errno} Message: {msg.strerror}")
    sys.exit()

print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] UDP ECHO Server is waiting for incoming connections on port {PORT} ...")

try:
    while True:
        data, address = sock.recvfrom(4096)
        print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Received {len(data)} bytes from client {address}. Data: {data.decode('utf-8')}")

        if data:
            try:
                # Perform reverse DNS lookup
                hostname = socket.gethostbyaddr(data.decode('utf-8'))
                sent = sock.sendto(hostname[0].encode('utf-8'), address)
                print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Sent {sent} bytes back to client {address}.")
            except socket.herror as e:
                error_message = "Sorry, an error occurred in gethostbyaddr"
                sent = sock.sendto(error_message.encode('utf-8'), address)
                print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Sent {sent} bytes back to client {address}.")
finally:
    sock.close()