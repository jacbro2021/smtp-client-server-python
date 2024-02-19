"""SMTP Server that recieves, validates, and stores SMTP messages."""
# Jacob Brown
# I pledge the Comp 431 honor code.

from socket import *

def main():
    """
    The starting point for execution of the SMTP server.
    """
    try:
        server_port: int = 9954
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(("", server_port))
        server_socket.listen(1)
        print("Server listening")

        while (True):
            pass

    finally:
        server_socket.close()
        print("Socket closed")

if __name__ == "__main__":
    main()

