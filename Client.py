"""SMTP Client that takes input from the user and transmits an SMTP message to a server via TCP."""
# Jacob Brown
# I pledge the Comp 431 honor code.

from socket import *
import sys

def main():
    """
    Starting point of the SMTP client.
    """
    try:
        server_name: str = "comp431sp24.cs.unc.edu"
        server_port: int = 9954

        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_name, server_port))

        initial_msg: str = client_socket.recv(1024).decode()
        print(initial_msg)

        print("responding...")
        initial_res: str = "HELO comp431sp24b.cs.unc.edu\n"
        client_socket.send(initial_res.encode())

        greet_msg: str = client_socket.recv(1024).decode()
        print(greet_msg)

        for line in sys.stdin:
            command = line

            client_socket.send(command.encode())

            if (command == "QUIT\n"):
                break

            res: str = client_socket.recv(1024).decode()
            print(res)

            if (res[:3] == "354"):
                for line in sys.stdin:
                    client_socket.send(line.encode())

                    if (line == ".\n"):
                        print(client_socket.recv(1024).decode())
                        break
            

        closing_msg: str = client_socket.recv(1024).decode()
        print(closing_msg)
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
