import socket
import sys
import threading

# Dictionary to store all connected clients and their types
clients = {}

def relay_message_to_subscribers(message, publisher_addr):
    for addr, client_type in clients.items():
        # print(addr)
        # print(client_type)
        if addr != publisher_addr and client_type != "PUBLISHER":
            try:
                client_socket = clients[addr]  # Get the subscriber's socket
                client_socket.sendall(message.encode())
            except (ConnectionResetError, KeyError):
                pass

def handle_client(client_socket, addr):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Check if the client is a Publisher and relay the message to Subscribers
            if clients[addr] == "PUBLISHER":
                print(f"Received from Publisher {addr}: {data}")
                relay_message_to_subscribers(data, addr)
            else:
                print(f"Received from Subscriber {addr}: {data}")

    except (ConnectionResetError, KeyError):
        pass
    finally:
        print(f"Client {addr} disconnected.")
        client_socket.close()
        # Remove the client from the dictionary upon disconnection
        del clients[addr]


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}...")

    try:
        while True:
            client_socket, client_addr = server_socket.accept()
            print(f"Connected to client: {client_addr}")

            client_type = client_socket.recv(1024).decode().upper()
            clients[client_addr] = client_type

            # Store the socket object for Subscribers separately
            if client_type == "SUBSCRIBER":
                clients[client_addr] = client_socket

            threading.Thread(target=handle_client, args=(client_socket, client_addr)).start()

    except KeyboardInterrupt:
        print("Server terminated by the user.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python my_server_app.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
