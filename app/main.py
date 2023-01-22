# Uncomment this to pass the first stage
import socket
from _thread import *
import re


def threaded_client(connection):

    while True:
        data = connection.recv(1024).decode()
        dataArray = data.split("\r\n")
        print(dataArray)

        if not data:
            break

        if len(dataArray) > 0:
            numberOfArgs = dataArray[0].replace("*", "")
            print(numberOfArgs)
            if numberOfArgs and numberOfArgs.isdigit() and int(numberOfArgs) > 1:
                response = ""
                firstCommand = dataArray[2]
                if firstCommand and (firstCommand.lower() == "echo"):
                    wordPointer = 4
                    wordLengthPointer = 3
                    while (wordLengthPointer < len(dataArray)) and (wordPointer < len(dataArray)) and dataArray[wordLengthPointer] != '':
                        word = f"{dataArray[wordPointer]}"
                        if word:
                            response += f"+{word}"
                        wordPointer += 2
                        wordLengthPointer += 2
                    connection.sendall(response.encode())
                else:
                    response = "+PONG\r\n"
                    connection.sendall(response.encode())
            else:
                response = "+PONG\r\n"
                connection.sendall(response.encode())
        else:
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
