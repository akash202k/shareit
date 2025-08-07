import socket
import argparse

def enable_tcp_server(host, port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)
        print(f'[TCP] Listening on {host}:{port}')
        conn, addr = server.accept()
        print(f'[TCP] server connected to {addr}')
        conn.send(f"Hello {addr}".encode())
        
        while True:
            data = conn.recv(1024)
            print(f"[Client] : {data.decode()}")
            message = input("[Server] : ")
            if message.lower() == "exit":
                break
            conn.send(message.encode())
            
        conn.close()
        server.close()
    except Exception as e:
        print("[enable_tcp_server] Something went wrong !", e)


def enable_tcp_client(host, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        
        while True:
            data = client.recv(1024)
            print(f"[Server] : {data.decode()}")
            message = input("[Client] : ")
            if message.lower() == "exit":
                break
            client.send(message.encode())
            
            
        
        client.close()
    except Exception as e:
        print("[enable_tcp_client] something went wrong !", e)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="share-it")
    parser.add_argument("mode", choices=["send", "receive"] ,help="Operation mode")
    parser.add_argument("--file", help="file path to send")
    args = parser.parse_args()

    # if args.mode == "send" and not args.file:
    #     parser.error("--file is required when mode is 'send'")
    # if args.mode == "receive":
        
        
    if args.mode == "send":
        enable_tcp_server(host="0.0.0.0", port=50000)
    
    
    if args.mode == "receive":
        enable_tcp_client(host="127.0.0.1", port=50000)  
        
