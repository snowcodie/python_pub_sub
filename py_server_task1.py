import socket
import sys

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    print(f"Server listening on port {port}...")

    try:
        conn, addr = server_socket.accept()
        print(f"Connected to client: {addr}")

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received from client: {data}")

    except KeyboardInterrupt:
        print("Server terminated by the user.")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
