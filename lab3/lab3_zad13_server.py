#!/usr/bin/env python

import socket
import sys
from time import gmtime, strftime


def check_msg_syntax(txt):
    s = len(txt.split(";"))
    if s != 7:
        return "BAD_SYNTAX"
    else:
        tmp = txt.split(";")
        if tmp[0] == "zad13odp" and tmp[1] == "src" and tmp[3] == "dst" and tmp[5] == "data":
            try:
                src_port = int(tmp[2])
                dst_port = int(tmp[4])
                data = tmp[6]
            except:
                return "BAD_SYNTAX"
            if src_port == 2900 and dst_port == 35211 and data == "hello :)":
                return "TAK"
            else:
                return "NIE"
        else:
            return "BAD_SYNTAX"


HOST = '127.0.0.1'
PORT = 2910

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.bind((HOST, PORT))
except socket.error as msg:
    print(f"Bind failed. Error Code: {msg.errno} Message: {msg.strerror}")
    sys.exit()

print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] UDP ECHO Server is waiting for incoming connections ...")

try:
    while True:
        data, address = sock.recvfrom(1024)
        print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Received {len(data)} bytes from client {address}. Data: {data.decode('utf-8')}")

        if data:
            answer = check_msg_syntax(data.decode('utf-8'))
            sent = sock.sendto(answer.encode('utf-8'), address)
            print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] Sent {sent} bytes back to client {address}.")
finally:
    sock.close()