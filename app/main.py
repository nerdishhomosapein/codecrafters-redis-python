# Uncomment this to pass the first stage
import socket
from _thread import *


def threaded_client(connection):

    while True:
        data = connection.recv(1024).decode()
        if not data:
            break
        response = "+PONG\r\n"
        connection.sendall(response.encode())
    connection.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        connection, _ = server_socket.accept()  # wait for client
        start_new_thread(threaded_client, (connection,))
    server_socket.close()

if __name__ == "__main__":
    main()
