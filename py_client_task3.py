import socket
import sys

def start_client(server_ip, port, client_type, topic):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
        print(f"Connected to server at {server_ip}:{port}")

        client_socket.sendall(client_type.encode())
        client_socket.sendall(topic.encode())

        if client_type == "PUBLISHER":
            print("You are in Publisher mode.")
            print(f"Your messages will be relayed to all connected Subscribers on topic '{topic}'.")

            while True:
                message = input("Type your message ('terminate' to exit): ")
                client_socket.sendall(message.encode())

                if message.lower() == "terminate":
                    break
        else:
            try:
                while True:
                    message = client_socket.recv(1024).decode()
                    print("Received: " + message)
            except (ConnectionResetError, KeyboardInterrupt):
                pass

    except KeyboardInterrupt:
        print("Client terminated by the user.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python py_client_task3.py <SERVER_IP> <PORT> <PUBLISHER|SUBSCRIBER> <TOPIC>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    client_type = sys.argv[3].upper()
    topic = sys.argv[4].upper()

    if client_type not in ["PUBLISHER", "SUBSCRIBER"]:
        print("Invalid client type. Use 'PUBLISHER' or 'SUBSCRIBER'.")
        sys.exit(1)

    start_client(server_ip, port, client_type, topic)
