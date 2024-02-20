# Jacob Brown
# I pledge the Comp 431 honor code.

import sys
from server_engine.exceptions import (DataCmdException,
                        CRLFException,
                        UnrecognizedCommandException,
                        SyntaxException,
                        )

# Global variable to hold the current line being input.
command: str = ""
# Global variable to hold the char that is currently being processed.
curr_char: str = ""

def advance_curr_char() -> None:
    """
    Advances the curr_char global variable to the next char in the command global variable.
    """
    global command, curr_char

    if (len(command) > 1):
        curr_char = command[0]
        command = command[1:]
    else:
        curr_char = command
        command = ""

def data_cmd(expected_char: str, second_a: bool = False):
    """
    Parse the data command.

    Args:
        expected_char: String of length one representing the char that is expected for the current iteration.
        second_a: Boolean showing that the second A in DATA is being processed when set to true.
    """

    if (expected_char == curr_char):
        advance_curr_char()
        match expected_char:
            case "D":
                data_cmd("A")
                return
            case "A":
                if (second_a):
                    return
                else:
                    data_cmd("T")
                    return
            case "T":
                data_cmd("A", True)
    else:
        raise DataCmdException()

def space() -> bool:
    """
    Determines if curr_char is a space or not.

    Returns:
        bool: True if curr_char is a space, false otherwise.
    """
    if (curr_char.isspace() and curr_char != "\n"):
        return True
    return False

def nullspace() -> None:
    """
    Parses the nullspace non-terminal.
    """
    while(space()):
        advance_curr_char()

def newline() -> None:
    """
    Checks to see if the current char is a newline (CRLF) character.

    Raises:
        CRLFException: if curr_char is not a newline character.
    """
    if (curr_char != "\n"):
        raise CRLFException()

def parse(line: str) -> None:
    """
    Parse the data command.

    Args:
        line: The command input by the user.
    """
    global command
    command = line
    
    # Populate first char from command
    advance_curr_char()
   
    try:
        # Check that the data command is properly formatted.
        data_cmd("D")
        # Skip through any null space.
        nullspace()
        # Check for a newline.
        newline()
        return
    except DataCmdException:
        raise UnrecognizedCommandException()
    except CRLFException:
        raise SyntaxException()

def parse_data_terminator(line: str) -> bool:
    """
    Parses the line at the end of the data in an SMTP message containing only a ".".

    Args:
        line: The line to check for the SMTP terminator.

    Returns:
        bool: True if the line is the SMTP Terminator, False otherwise.
    """
    global command
    command = line
    
    # Populate first char from command.
    advance_curr_char()

    # Check that the first char of the line is the ".".
    if (curr_char != "."):
        return False

    # Move curr char past the .
    advance_curr_char()

    # Check for a newline.
    try:
        newline()
        return True
    except CRLFException:
        return False

