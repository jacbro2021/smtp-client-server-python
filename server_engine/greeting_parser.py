"""Engine for parsing the HELO greeting message sent by the client to the SMTP server"""
# Jacob Brown
# I pledge the Comp 431 honor code.

import sys
from server_engine.exceptions import (MailFromCmdException,
                        WhitespaceException,
                        PathException,
                        MailboxException,
                        StringException,
                        ElementException,
                        CRLFException,
                        UnrecognizedCommandException,
                        SyntaxException,
                        HelloException
                        )

                       
# The command input by the user.
command: str = ""
# The character that is currently being processed from the command.
curr_char: str = ""

def helo(expected_char: str) -> None:
    """
    Determines if the HELO portion of the command is properly formatted.
    """

    if expected_char != "":
        if curr_char == expected_char:
            advance_curr_char()

            match expected_char:
                case "H":
                    helo("E")
                    return
                case "E":
                    helo("L")
                    return
                case "L":
                    helo("O")
                    return
                case "O":
                    return
        else:
            raise HelloException()

def whitespace() -> None:
    """
    Parses the whitespace non-terminal.

    Raises:
        WhitespaceException: If there is no whitespace where whitespace is required within the command.
    """
    if (space()):
        while (space()):
            advance_curr_char()
        return
    raise WhitespaceException()


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

def domain() -> None:
    """
    Parses the domain non-terminal.
    """
    element()
    if (curr_char == "."):
        while (curr_char == "."):
            advance_curr_char()
            element()

def element() -> None:
    """
    Parses the element non-terminal.

    Raises:
        ElementException: If the element is improperly formatted.
    """
    if (letter()):
        advance_curr_char()
        name()
    else:
        raise ElementException()

def name() -> None:
    """
    Parse the name non-terminal.
    """
    let_dig_str()

def let_dig_str() -> None:
    """
    Parses the let-dig-str non-terminal.
    """
    if (let_dig()):
        while (let_dig()):
            advance_curr_char()

def let_dig() -> bool:
    """
    Checks if a character is a valid letter or digit.

    Args:
        char: The string of length one to check.

    Returns:
        bool: True if the characters is a valid letter or digit, false
              otherwise.
    """
    return letter() or digit()

def letter() -> bool:
    """
    Checks if the given char is a letter.

    Returns:
        bool: True if the char is a letter, false otherwise.
    """
    ascii_val: int = ord(curr_char)
    if ((ascii_val >= 65 and ascii_val <= 90) or (ascii_val >= 97 and ascii_val <= 122)):
        return True
    return False

def digit() -> bool:
    """
    Checks if the given char is a digit.

    Returns:
        bool: True if the char is a digit, false otherwise.
    """        
    ascii_val: int = ord(curr_char)
    if (ascii_val >= 48 and ascii_val <= 57):
        return True
    return False

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

def stripped_domain(line: str) -> str:
    """
    Takes in a pre-validated greeting command and returns the domain.

    Args:
        line: The line received from the SMTP client

    Returns:
        str: The domain from the line arg.
    """
    return line[5:].strip()

def parse(line: str) -> str:
    """
    Parses the HELO greeting command from the SMTP client.

    Args:
        line: The command sent by the client.

    Returns:
        The parsed and stripped domain from the line argument.
    """
    global command
    
    command = line
    advance_curr_char()
    try:
        # Parse the 'HELO' portion of greeting.
        helo("H")
        # Parse for whitespace.
        whitespace()
        # Parse the domain.
        domain()
        # Jump through any nullspace.
        nullspace()
        # Check for newline.
        newline()

        return stripped_domain(line)
    except (HelloException,
            WhitespaceException,
            ) as e:
        raise UnrecognizedCommandException()
    except (PathException,
                MailboxException,
                StringException,
                ElementException,
                CRLFException) as e:
        raise SyntaxException()


if __name__ == "__main__":
    line: str = input() + "\n"
    parse(line=line)










