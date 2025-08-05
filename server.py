import socket
import os

UDP_PORT = 50000
TCP_PORT = 50001
DISCOVERY_MSG = "DISCOVER_SERVER"
RESPONSE_MSG = "SERVER_HERE"
FILE_PATH = "sample.txt"  # ← Change this to any file you want to send

def udp_discovery_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", UDP_PORT))
    print(f"[UDP] Discovery server listening on port {UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode() == DISCOVERY_MSG:
            print(f"[UDP] Discovery request from {addr}")
            sock.sendto(RESPONSE_MSG.encode(), addr)
            break
    sock.close()

def tcp_file_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("", TCP_PORT))
    server_sock.listen(1)
    print(f"[TCP] Listening on port {TCP_PORT}, sending {FILE_PATH}")

    conn, addr = server_sock.accept()
    print(f"[TCP] Connection from {addr}")

    filename = os.path.basename(FILE_PATH)
    file_size = os.path.getsize(FILE_PATH)

    # Send filename and size separated by a delimiter (e.g., "::")
    conn.sendall(f"{filename}::{file_size}".encode())
    
    ack = conn.recv(1024)  # Wait for ACK from client
    if ack.decode() != "READY":
        print("[TCP] Client not ready. Aborting.")
        conn.close()
        server_sock.close()
        return

    with open(FILE_PATH, "rb") as f:
        while chunk := f.read(4096):
            conn.sendall(chunk)

    print("[TCP] File sent successfully!")
    conn.close()
    server_sock.close()

if __name__ == "__main__":
    udp_discovery_server()
    tcp_file_server()
