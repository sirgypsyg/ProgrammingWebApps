import socket

HOST = '127.0.0.1' 
PORT = 2900        
def validate_message(message):
    if message.startswith("zad15odpA;"):
        parts = message.split(";")
        print(f"Debug: parts = {parts}") 
        if len(parts) == 8 or message == "zad15odpA;ver;X;srcip;Y;dstip;Z;type;W": 
            if (
                parts[1] == "ver" and
                parts[3] == "srcip" and
                parts[5] == "dstip" and
                parts[7] == "type" 
            ):
                return "TAK"
            else:
                return "BAD SYNTAX"
        else:
            return "BAD SYNTAX"
    else:
        return "NIE"
    
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print(f"Server is listening on {HOST}:{PORT}...")
    
    while True:
        data, addr = server_socket.recvfrom(1024) 
        message = data.decode()
        print(f"Received message from {addr}: {message}")
        
        response = validate_message(message)
        print(f"Response to {addr}: {response}")
        
        server_socket.sendto(response.encode(), addr)