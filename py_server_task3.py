import socket
import sys
import threading

# Dictionary to store all connected clients and their topics/subjects
clients = {}

def relay_message_to_subscribers(message, topic, publisher_addr):
    for addr, client_info in clients.items():
        client_type = client_info["type"]
        client_topic = client_info["topic"]

        if addr != publisher_addr and client_type == "SUBSCRIBER" and client_topic == topic:
            try:
                client_socket = client_info["socket"]  # Get the subscriber's socket
                client_socket.sendall(message.encode('utf-8'))
            except (ConnectionResetError, KeyError):
                pass


def handle_client(client_socket, addr):
    try:
        client_type = client_socket.recv(1024).decode('utf-8').upper()
        topic = client_socket.recv(1024).decode('utf-8').upper()
        clients[addr] = {"type": client_type, "topic": topic, "socket": client_socket}

        print(f"Connected to {client_type} {addr} on topic {topic}.")

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

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
