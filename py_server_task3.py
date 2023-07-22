import socket
import sys
import threading

# Dictionary to store all connected clients and their topics/subjects
clients = {}

def relay_message_to_subscribers(message, topic, publisher_addr):
    for addr, (client_type, client_topic) in clients.items():
        if addr != publisher_addr and client_type == "SUBSCRIBER" and client_topic == topic:
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

            client_type, topic = clients[addr]

            # Check if the client is a Publisher and relay the message to Subscribers with the same topic
            if client_type == "PUBLISHER":
                print(f"Received from Publisher {addr} on topic {topic}: {data}")
                relay_message_to_subscribers(data, topic, addr)

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
            topic = client_socket.recv(1024).decode().upper()

            clients[client_addr] = (client_type, topic)

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
