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

        handshake_msg: str = "250 Hello " + domain + " pleased to meet you"
        connection_socket.send(handshake_msg.encode())

        return True
    except (WhitespaceException,
            HelloException
            ) as e:
        # Print single line error message.
        print(str(UnrecognizedCommandException()))
        return False

    except (ElementException,
            CRLFException,) as e:
        # Print single line error message.
        print(str(SyntaxException()))
        return False

def parse_message(msg: str) -> list[str]:
    """
    parses decoded TCP messages and breaks them up 
    into separate messages according to newlines

    Args:
        msg: A string message recieved from the TCP socket.

    Returns:
        list[str]: The part of the received message up to the first
             newline.
    """
    # Split message into array of str's.
    split_msg = msg.split("\n")

    final_msg: list[str] = []

    # Add '\n' to each individual message.
    index: int = 0
    while (index < len(split_msg)):
        message = split_msg[index]
        if (message == "" and index == (len(split_msg) - 1)):
            break;
        message = message + "\n"
        final_msg.append(message)
        index += 1

    # Reeturn list of commands.
    return final_msg
        
def main():
    """
    The starting point for execution of the SMTP server.
    """
    engine: ServerEngine = ServerEngine()
    connection_exists: bool = False

    try:
        server_port: int = 9954
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(("", server_port))
        server_socket.listen(1)

        while (True):
            # Accept socket.
            connection_socket, address = server_socket.accept()
            connection_exists = True

            # Greet and terminate program if error occurs.
            if (not greet(connection_socket=connection_socket)):
                raise GreetingException()

            # Process SMTP messages.
            while (True):
                # Decode command and check for quit.
                command = connection_socket.recv(1024).decode()
                if (command[:4] == "QUIT"):
                    break

                # Split command into list of str's.
                split_command: list[str] = parse_message(command) 
                for cmd in split_command:
                    # Parse command and send a response.
                    command_response = engine.parse(cmd)

                    if (command_response):
                        connection_socket.send(command_response.encode())

            # Send closing socket message.
            closing_msg: str = "221 comp431sp24.cs.unc.edu closing connection"
            connection_socket.send(closing_msg.encode())

            # Close socket.
            connection_socket.close()
            connectin_exists = False

    except (GreetingException,
            KeyboardInterrupt):
        pass
    finally:
        if (connection_exists):
            connection_socket.close()
        server_socket.close()

if __name__ == "__main__":
    main()
