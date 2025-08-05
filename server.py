import socket
import os

UDP_PORT = 50000
TCP_PORT = 50001
DISCOVERY_MSG = "DISCOVER_SERVER"
RESPONSE_MSG = "SERVER_HERE"
FILE_PATH = "sample.txt"

# --- UDP Discovery Server ---
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

# --- TCP File Transfer Server ---
def tcp_file_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("", TCP_PORT))
    server_sock.listen(1)
    print(f"[TCP] Listening on port {TCP_PORT}, sending {FILE_PATH}")

    conn, addr = server_sock.accept()
    print(f"[TCP] Connection from {addr}")

    file_size = os.path.getsize(FILE_PATH)
    conn.sendall(str(file_size).encode())

    with open(FILE_PATH, "rb") as f:
        while chunk := f.read(4096):
            conn.sendall(chunk)

    print("[TCP] File sent successfully!")
    conn.close()
    server_sock.close()

if __name__ == "__main__":
    udp_discovery_server()
    tcp_file_server()
