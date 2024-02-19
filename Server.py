"""SMTP Server that recieves, validates, and stores SMTP messages."""
# Jacob Brown
# I pledge the Comp 431 honor code.

from socket import *
from server_engine.greeting_parser import parse as clean_greeting

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

            # Handshaking process.
            greeting_msg: str = "220 comp431sp24.cs.unc.edu"
            connection_socket.send(greeting_msg.encode())

            initial_response: str = connection_socket.recv(1024).decode()
            domain: str = clean_greeting(initial_response)

            handshake_msg: str = "250 Hello " + domain + "pleased to meet you"
            connection_socket.send(handshake_msg.encode())

            # Process SMTP messages.


            # Close socket.
            connection_socket.close()

    except KeyboardInterrupt:
        pass

    finally:
        server_socket.close()
        print("Socket closed")

if __name__ == "__main__":
    main()

"""
# Get request from client step 2
# Read request from connectionSocket
sentence = connection_socket.recv(1024).decode()
capitalized_sentence = sentence.upper()

# Step 4 
# Give response to client step 3
# Write reply to connection socket
connection_socket.send(capitalized_sentence.encode())
"""

