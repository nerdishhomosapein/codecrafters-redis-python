# Uncomment this to pass the first stage
import socket
from _thread import *
from datetime import datetime, timedelta
import time
import re


dictionary = {}


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
                    while (
                        (wordLengthPointer < len(dataArray))
                        and (wordPointer < len(dataArray))
                        and dataArray[wordLengthPointer] != ""
                    ):
                        word = f"{dataArray[wordPointer]}"
                        if word:
                            response += f"+{word}"
                        wordPointer += 2
                        wordLengthPointer += 2
                    connection.sendall(response.encode())
                elif firstCommand and (firstCommand.lower() == "set"):
                    expirationTime = None
                    if len(dataArray) > 10:
                        expirationTime = dataArray[10]
                        print(expirationTime)
                    key = dataArray[4]
                    value = dataArray[6]
                    if key and value:
                        if expirationTime and expirationTime.isdigit():
                            now = datetime.now()
                            key_expiry_time = now + timedelta(milliseconds = int(expirationTime))
                            key_expiry_time_stamp = key_expiry_time.timestamp()
                            dictionary[key] = (value, key_expiry_time_stamp)
                            response = "+OK\r\n"
                            connection.sendall(response.encode())
                        else:
                            dictionary[key] = (value, None)
                            response = "+OK\r\n"
                            connection.sendall(response.encode())

                elif firstCommand and (firstCommand.lower() == "get"):
                    key = dataArray[4]
                    if key:
                        if key in dictionary:
                            value, expiry_time = dictionary[key]
                            print("Expiry time: ", expiry_time)
                            print("Current time: ", time.time())
                            if expiry_time and expiry_time > time.time():
                                response = f"${len(value)}\r\n{value}\r\n"
                                connection.sendall(response.encode())
                            elif expiry_time and expiry_time <= time.time():
                                response = "$-1\r\n"
                                connection.sendall(response.encode())
                            else:
                                response = f"${len(value)}\r\n{value}\r\n"
                                connection.sendall(response.encode())
                        else:
                            response = "$-1\r\n"
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
