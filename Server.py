"""SMTP Server that recieves, validates, and stores SMTP messages."""
# Jacob Brown
# I pledge the Comp 431 honor code.

from socket import *
from server_engine.exceptions import *
from server_engine.greeting_parser import parse as clean_greeting
from server_engine.SMTP1 import ServerEngine

def greet(connection_socket: socket) -> bool:
    """
    Handles the series of messages to establish connection between SMTP server and client.

    Args:
        connection_socket: The socket with a live connection to the client.

    Returns:
        bool: True if the connection was successful, false otherwise
    """
    greeting_msg: str = "220 comp431sp24.cs.unc.edu"
    connection_socket.send(greeting_msg.encode())

    # Parse and validate client greeting.
    initial_response: str = connection_socket.recv(1024).decode()
    try:
        domain: str = clean_greeting(initial_response)

        handshake_msg: str = "250 Hello " + domain + "pleased to meet you"
        connection_socket.send(handshake_msg.encode())

        return True
    except (WhitespaceException,
            HelloException
            ) as e:
        # Send client Unrecognized command exception.
        connection_socket.send(str(UnrecognizedCommandException()).encode())
        return False

    except (ElementException,
            CRLFException,) as e:
        # Send client syntax exception.
        connection_socket.send(str(SyntaxException()).encode())
        return False

def main():
    """
    The starting point for execution of the SMTP server.
    """
    try:
        server_port: int = 9954
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(("", server_port))
        server_socket.listen(1)
        print("Server listening on port 9954")

        while (True):
            connection_socket = server_socket.accept()
            print("connection opened")

            while (not greet(connection_socket=connection_socket)):
                # Continue calling greet.
                pass

            # Process SMTP messages.
            while (True):
                command = connection_socket.recv(1024).decode()
                print(command)

                if (command == "QUIT\n"):
                    break

            # Close socket.
            connection_socket.close()

    except KeyboardInterrupt:
        pass

    finally:
        server_socket.close()
        print("Socket closed")

if __name__ == "__main__":
    main()
