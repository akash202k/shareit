import os

files = {
    "server.py": """import socket
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
""",

    "client.py": """import socket

UDP_PORT = 50000
TCP_PORT = 50001
DISCOVERY_MSG = "DISCOVER_SERVER"

def udp_discovery_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(5)

    print("[UDP] Sending discovery broadcast...")
    sock.sendto(DISCOVERY_MSG.encode(), ("255.255.255.255", UDP_PORT))

    server_ip = None
    try:
        data, addr = sock.recvfrom(1024)
        if data.decode() == "SERVER_HERE":
            server_ip = addr[0]
            print(f"[UDP] Found server at {server_ip}")
    except socket.timeout:
        print("[UDP] No server found.")
    sock.close()
    return server_ip

def tcp_file_client(server_ip):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((server_ip, TCP_PORT))
    print(f"[TCP] Connected to {server_ip}:{TCP_PORT}")

    file_size = int(client_sock.recv(1024).decode())
    received = 0

    with open("received_file.txt", "wb") as f:
        while received < file_size:
            data = client_sock.recv(4096)
            if not data:
                break
            f.write(data)
            received += len(data)

    print("[TCP] File received successfully!")
    client_sock.close()

if __name__ == "__main__":
    server_ip = udp_discovery_client()
    if server_ip:
        tcp_file_client(server_ip)
""",

    "requirements.txt": """# No external dependencies needed
# Runs with Python 3.x standard library only
""",
}

# Create files
for filename, content in files.items():
    with open(filename, "w") as f:
        f.write(content)
    print(f"[+] Created {filename}")

# Create a sample file to send
with open("sample.txt", "w") as f:
    f.write("This is a sample file for testing P2P TCP file transfer over LAN.\n" * 5)
print("[+] Created sample.txt")

print("\n✅ Project setup complete! Run `python3 server.py` on one device and `python3 client.py` on another.")
