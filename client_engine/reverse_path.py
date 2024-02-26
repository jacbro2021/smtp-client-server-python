"""Script to validate and return reverse_paths"""
# Jacob Brown
# I pledge the Comp 431 honor code.

import sys
from client_engine.exceptions import (MailFromCmdException,
                        WhitespaceException,
                        PathException,
                        MailboxException,
                        StringException,
                        ElementException,
                        CRLFException,
                        UnrecognizedCommandException,
                        SyntaxException,
                        )

# The command input by the user.
command: str = ""
# The character that is currently being processed from the command.
curr_char: str = ""

def space() -> bool:
    """
    Checks if curr_char is a space.
    """
    if (curr_char.isspace()):
        return True
    return False

def reverse_path() -> None:
    """
    Parses the reverse path non-terminal.
    """
    path()

def path() -> None:
    """
    Parses the path non-terminal.

    Raises:
        PathException: If the path is improperly formatted.
    """
    mailbox()

def mailbox() -> None:
    """
    Parses the mailbox non-terminal.

    Raises:
        MailboxException: If the mailbox is improperly formatted.
    """
    local_part()
    
    if (curr_char != "@"):
        raise MailboxException()
    
    advance_curr_char()
    domain()

def local_part() -> None:
    """
    Parses the local-part non-terminal.
    """
    string()

def string() -> None:
    """
    Parses the string non-terminal.
    """
    if (char()):
        while (char()):
            advance_curr_char()
    else:
        raise StringException()

def char() -> bool:
    """
    Parses the char non-terminal.

    Returns:
        bool: True if curr_char is a valid char, false otherwise.
    """
    if (space() or special()):
        return False
    return True

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

def newline() -> None:
    """
    Checks to see if the current char is a newline (CRLF) character.

    Raises:
        CRLFException: if curr_char is not a newline character.
    """
    if (curr_char != "\n"):
        raise CRLFException()

def special() -> bool:
    """
    Checks to see if the current char is a special character.

    Returns:
        bool: True if curr_char is a special character, false otherwise.
    """
    special_chars: list[str] = ["<", ">", "(", ")", "[", "]", "\\", ".", ",", ";", ":", "@", "\""]
    if curr_char in special_chars:
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

def parse(line: str) -> str:
    """
    Parses the SMTP command input from the command line.

    Args:
        line: The command input from the command line.

    Returns:
        str: the validated reverse path or None if the reverse path was invalid.
    """
    global command

    command = line
    advance_curr_char()

    try:
        # Parse the reverse path.
        reverse_path()

        # Make sure the command is empty.
        if (command != ""):
            raise ElementException()

        # Return the valid reverse path.
        return line.strip()
    except (MailFromCmdException,
            WhitespaceException,
            ) as e:
        raise UnrecognizedCommandException()
    except (PathException,
                MailboxException,
                StringException,
                ElementException,
                CRLFException) as e:
        sys.stdout.write(f"{str(e)}\n")
        return None

if __name__ == "__main__":
    for line in sys.stdin:
        parse(line)
