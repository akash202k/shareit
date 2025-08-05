import socket

UDP_PORT = 50000
TCP_PORT = 50001
DISCOVERY_MSG = "DISCOVER_SERVER"
# 
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

    # Receive filename and file size
    header = client_sock.recv(1024).decode()
    filename, file_size = header.split("::")
    file_size = int(file_size)

    print(f"[TCP] Receiving {filename} ({file_size} bytes)")

    client_sock.sendall(b"READY")  # Send ACK

    received = 0
    with open(filename, "wb") as f:
        while received < file_size:
            data = client_sock.recv(4096)
            if not data:
                break
            f.write(data)
            received += len(data)

    print(f"[TCP] File {filename} received successfully!")
    client_sock.close()

if __name__ == "__main__":
    server_ip = udp_discovery_client()
    if server_ip:
        tcp_file_client(server_ip)
