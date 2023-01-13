# Uncomment this to pass the first stage
import socket
import re


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    connection, _ = server_socket.accept()  # wait for client

    while True:
        data = connection.recv(1024).decode()

        print(f"{data=}")
        regex = re.compile(r"\bping\b")
        if re.findall(regex, data) and len(re.findall(regex, data)) > 0:
            response = "+PONG\r\n"
            connection.send(response.encode())

if __name__ == "__main__":
    main()
