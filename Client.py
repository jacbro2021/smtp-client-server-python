"""SMTP Client that takes input from the user and transmits an SMTP message to a server via TCP."""
# Jacob Brown
# I pledge the Comp 431 honor code.

from socket import *
import sys
from client_engine.reverse_path import parse as parse_path
from client_engine.exceptions import SMTPException

# Default time to wait between sending TCP messages.
wait_time: int = 0.01

def parse_from() -> str:
    """
    Prompt the user to input the From: path and parse the path entered
    by the user.

    Returns:
        str: the valid path entered by the user.
    """
    cleaned_path: str = None
    if (not cleaned_path):
        while(not cleaned_path):
            print("From:")
            line: str = input() + "\n"
            cleaned_path = parse_path(line)
    return cleaned_path

def parse_to() -> list[str]:
    """
    Prompt the user to input the 'To:' path(s) and parse the entered path(s).

    Returns:
        list[str]: The list of validated paths.
    """
    cleaned_paths: list[str] = None
    if (not cleaned_paths):
        while(not cleaned_paths):
            print("To:")
            paths: list[str] = input().split(",")
            cleaned_paths = []
            
            for path in paths:
                # Strip off any whitespace.
                path = path.strip()
                # Validate the path.
                cleaned_path: str = parse_path(path + "\n")

                if (cleaned_path):
                    cleaned_paths.append(cleaned_path)
                else:
                    # Reprompt user.
                    cleaned_paths = None
                    break
    return cleaned_paths

def fetch_subject() -> str:
    """
    Prompts the user to input the subject of the email.

    Returns:
        str: the subject input by the user.
    """
    print("Subject:")
    return input()

def fetch_message() -> list[str]:
    """
    Prompts the user to input the content of the email.

    Returns:
        list[str]: a list containing each line of the email.
    """
    print("Message:")
    line: str = input()

    message: list[str] = []

    while (line != "."):
        message.append(line)
        line = input()

    return message
        

def main():
    """
    Starting point of the SMTP client.
    """
    from_path: str = parse_from() 
    to_path: list[str] = parse_to()
    subject: str = fetch_subject()
    message: list[str] = fetch_message()

    try:
        # Server name and port passed as command line arguments.
        server_name: str = sys.argv[1]
        server_port: str = sys.argv[2]

        # Configure socket.
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_name, int(server_port)))

        # Recieve greeting from server.
        greeting: str = client_socket.recv(1024).decode()
        if (greeting[:3] != "220"):
            raise SMTPException()

        # Send greeting to server.
        initial_res: str = "HELO cs.unc.edu\n"
        client_socket.send(initial_res.encode())

        # Receive server secondary greeting.
        confirm_greeting: str = client_socket.recv(1024).decode()
        if (confirm_greeting[:3] != "250"):
            raise SMTPException()

        # Send 'MAIL FROM' command.
        mail_from = f"MAIL FROM: <{from_path}>\n"
        client_socket.send(mail_from.encode())

        # Parse 'MAIL FROM' response.
        mail_from_res = client_socket.recv(1024).decode()
        if (mail_from_res[:3] != "250"):
            raise SMTPException("Error transmitting SMTP message!")

        # Send 'RCPT TO' commands.
        for path in to_path:
            rcpt_to = f"RCPT TO: <{path}>\n"
            client_socket.send(rcpt_to.encode())

            rcpt_to_res: str = client_socket.recv(1024).decode()
            if (rcpt_to_res[:3] != "250"):
                raise SMTPException("Error transmitting SMTP message!")

        # Send 'DATA' command.
        data = f"DATA\n"
        client_socket.send(data.encode())

        # Parse 'DATA' response.
        data_res: str = client_socket.recv(1024).decode()
        if (data_res[:3] != "354"):
            raise SMTPException("Error transmitting SMTP message!")

        # Send 'From' message.
        from_msg = f"From: <{from_path}>\n"
        client_socket.send(from_msg.encode())

        # Send 'To' message.
        to_msg: str = "To: "
        for recipient in to_path:
            to_msg += f"<{recipient}>, "
        to_msg = to_msg[:len(to_msg)-2] 
        to_msg = f"{to_msg}\n"
        client_socket.send(to_msg.encode())
        
        # Send subject line.
        subject_line: str = f"Subject: {subject}\n"
        client_socket.send(subject_line.encode())

        # Send a blank line.
        blank: str = "\n"
        client_socket.send(blank.encode())

        # Send message body.
        for line in message:
            line += "\n"
            client_socket.send(line.encode())

        # Send period to end message transmission.
        period: str = ".\n"
        client_socket.send(period.encode())

        # Check server response
        final_response: str = client_socket.recv(1024).decode()
        if (final_response[:3] != "250"):
            raise SMTPException("Error transmitting SMTP message!")

        # Send 'QUIT' command.
        quit_cmd: str = "QUIT\n"
        client_socket.send(quit_cmd.encode())

        # Parse 'QUIT' response.
        quit_res: str = client_socket.recv(1024).decode()
        if (quit_res[:3] != "221"):
            raise SMTPException("Failed to close connection to server.")

    except SMTPException as e:
        print(str(e))

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
