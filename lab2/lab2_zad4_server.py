#!/usr/bin/env python

import socket
import sys
from time import gmtime, strftime

HOST = '127.0.0.1'
PORT = 2902

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.bind((HOST, PORT))
except socket.error as msg:
    print(f"Bind failed. Error Code: {msg.errno} Message: {msg.strerror}")
    sys.exit()

print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] UDP ECHO Server is waiting for incoming connections ...")

try:
    while True:
        data, address = sock.recvfrom(4096)
        
        print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Received {len(data)} bytes from client {address}. Data: {data.decode('utf-8')}")

        if data:
            sent = sock.sendto(data, address)
            print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Sent {sent} bytes back to client {address}.")
finally:
    sock.close()