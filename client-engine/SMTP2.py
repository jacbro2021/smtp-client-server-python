"""SMTP client script. processes valid "forward" smpt files."""
# Jacob Brown
# I pledge the Comp 431 honor code.

import sys
from enum import Enum, auto
from exceptions import InvalidResponseCodeException

class CmdType(Enum):
    FROM = auto()
    TO = auto()
    DATA = auto()

# Global var to hold the state of the program.
state: int = 0
# Global var to indicate if this is the start of the body of the message.
consuming_data: bool = False

def parse_from(line: str) -> bool:
    """
    Parses the 'From:' command retrieved from the argument file.

    Args: 
        line: The line containing a potential 'From:' command.

    Returns:
        bool: True if the line is a 'From:' command, False otherwise.
    """
    command: str = line[0:5]

    if (command == "From:"):
        # Parse the email and write to stdout.
        email: str = line[5:].strip()
        output_cmd = "MAIL FROM: " + email
        sys.stdout.write(f"{output_cmd}\n")

        # Capture the status code and echo to standard error.
        status_code: str = input()
        sys.stderr.write(f"{status_code}\n")

        # Check that the response code is valid.
        if (status_code[0:3] != "250"):
            raise InvalidResponseCodeException()

        return True
    return False

def parse_to(line: str) -> bool:
    """
    Parses the 'To:' command retrieved from the argument file.

    Args:
        line: The line containing a potential 'To:' command.

    Returns:
        bool: True if the line is a 'To:' command, False otherwise.
    """
    command: str = line[0:3]

    if (command == "To:"):
        #Parse the email and write to stdout.
        email: str = line[3:].strip()
        output_cmd: str = "RCPT TO: " + email
        sys.stdout.write(f"{output_cmd}\n")

        # Capture the status code and echo to standard error.
        status_code: str = input()
        sys.stderr.write(f"{status_code}\n")

        # Check that the response code is valid.
        if (status_code[0:3] != "250"):
            raise InvalidResponseCodeException()

        return True
    return False

def output_data() -> None:
    """
    Outputs the data command to stdout and awaits the proper status
    code.
    """
    sys.stdout.write("DATA\n")

    status_code: str = input()
    sys.stderr.write(f"{status_code}\n")

    # Check that the response code is valid.
    if (status_code[0:3] != "354"):
        raise InvalidResponseCodeException()

def terminate_data() -> None:
    """
    Outputs the data command terminator to stdout and awaits the proper
    status code.
    """
    sys.stdout.write(".\n")

    status_code: str = input()
    sys.stderr.write(f"{status_code}\n")

    # Check that the response code is valid.
    if (status_code[0:3] != "250"):
        raise InvalidResponseCodeException()

def identify_cmd(line: str) -> CmdType:
    """
    Identify the type of command of each line read from the file passed as an argument.

    Arg:
        line: A line retrieved from the argument file.

    Returns:
        CmdType: Enum value indicating the type of the command.
    """
    if (line[0:3] == "To:"):
        return CmdType.TO
    elif (line[0:5] == "From:"):
        return CmdType.FROM
    else:
        return CmdType.DATA

def read_file(path: str) -> None:
    """
    Opens a file in read-only mode and reads its contents line by line.

    Args:
        path: The path to the file to be read.
    """
    global state, consuming_data

    try:
        with open(path, "r") as file:
            for line in file:
                if (state == 0):
                    # Parse the 'From:' command and increment state.
                    parse_from(line)
                    state += 1

                elif (state == 1):
                    # Parse the 'To:' command and increment state.
                    parse_to(line)
                    state += 1

                elif (state == 2):
                    cmd_type: CmdType = identify_cmd(line)

                    if (cmd_type == CmdType.FROM):
                        # Terminate the previous command and reset
                        # consuming data flag.
                        terminate_data()
                        consuming_data = False
                        
                        # Parse the 'From:' command and increment state.
                        parse_from(line)
                        state = 1

                    elif (cmd_type == CmdType.TO):
                        # Parse the 'To:' command and stay in the same 
                        # state.
                        parse_to(line)

                    elif (cmd_type == CmdType.DATA):
                        # If this is the first line of the body, then output the DATA terminal.
                        if (not consuming_data):
                            consuming_data = True
                            output_data()

                        # Echo each body line to stdout.
                        sys.stdout.write(line)
           
            # Add data terminator for last message processed.
            terminate_data()

            # Write 'QUIT' message to console.
            sys.stdout.write("QUIT\n")

    except (InvalidResponseCodeException) as e:
        sys.stdout.write("QUIT\n")
    except (Exception) as e:
        pass
        

if __name__ == "__main__":
    # Get the file path that was passed as an argument.
    path = sys.argv[1]
    # Parse through the file.
    read_file(path)


