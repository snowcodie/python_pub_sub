import socket
import sys

def start_client(server_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")
        
        while True:
            message = input("Type your message ('terminate' to exit): ")
            client_socket.sendall(message.encode())

            if message.lower() == "terminate":
                break

    except KeyboardInterrupt:
        print("Client terminated by the user.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: py_client_task1.py <SERVER_IP> <PORT>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    start_client(server_ip, port)
