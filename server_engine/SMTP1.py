# Jacob Brown
# I pledge the Comp 431 honor code.

import sys
from pathlib import Path
from enum import (Enum,
                  auto,
                  )
from server_engine.mail_from import parse as mail_from
from server_engine.rcpt_to import parse as rcpt_to
from server_engine.data_cmd import (parse as data_cmd, 
                      parse_data_terminator as terminator,
                      )
    
from server_engine.exceptions import (UnrecognizedCommandException,
                        SyntaxException,
                        BadCmdSequenceException,
                        )

class Cmd(Enum):
    """
    Enum to describe which type of command has been input to the command
    line.
    """
    MAIL = auto()
    RCPT = auto()
    DATA = auto()

class ServerEngine:

    # Var to hold the state of the program. The state is used to 
    #   indicate which command is expected to be recieved next.
    state: int = 0
    # Var to hold the sender that is parsed from the MAIL TO 
    #   command.
    sender: str = ""
    # Var to hold all of the recipients of a given message.
    recipients: list[str]  = []
    # Var to hold the data sent in the message (the actual text).
    message: str = ""
    # Flag to track if the data command has been terminated.
    data_terminated: bool = True


    def is_mail(line: str) -> bool:
        """
        Checks to see if the provided line is a mail_from_command.

        Args:
            line: The command to check.

        Returns: 
            bool: True if the line is a mail_from_command, false otherwise.
        """
        try:
            mail_from(line)
            return True
        except UnrecognizedCommandException as e:
            return False
        except SyntaxException as e:
            return True

    def is_rcpt(line: str) -> bool:
        """
        Checks to see if the provided line is a rcpt_to_command.

        Args:
            line: The command to check.

        Returns:
            bool: True if the line is a rcpt_to_command, false otherwise.
        """
        try:
            rcpt_to(line)
            return True
        except UnrecognizedCommandException as e:
            return False
        except SyntaxException as e:
            return True

    def is_data(line: str) -> bool:
        """
        Checks to see if the provided line is a Data command.

        Args:
            line: The command to check.

        Returns:
            bool: True if the line is a data command, false otherwise.
        """
        try:
            data_cmd(line)
            return True
        except UnrecognizedCommandException as e:
            return False
        except SyntaxException as e:
            return True

    def get_cmd_type(line: str) -> Cmd:
        """
        Finds the command type of a given line, if one exists.

        Args:
            line: The line to find the command type of. More specifically
                  The non-terminal that the line maps to.

        Returns:
            Cmd: either one of the three options from the Cmd enum defined above or None.
        """
        if (is_mail(line)):
            return Cmd.MAIL
        elif (is_rcpt(line)):
            return Cmd.RCPT
        elif (is_data(line)):
            return Cmd.DATA
        else:
            return None

    def retrieve_reverse_path(line: str) -> str:
        """
        Takes in a mail from command and parses out the reverse path.

        Args:
            line: A valid mail from command.
        """
        # Grab first character and remove it from the input
        current_char: str = line[0]
        line = line[1:]

        # Remove all text prefixing the reverse path.
        while (current_char != "<"):
            line = line[1:]
            current_char = line[0]

        # Skip through the reverse path
        ind: int = 0
        while (line[ind].isspace() == False):
            ind += 1

        # Remove any trailing whitespace or newlines.
        line = line[:ind]

        return line

    def store_mail_from(line: str) -> None:
        """
        Reformat the mail from command and store it in the sender global var.

        Args:
            line: The valid mail from cmd to be reformatted and saved in
                  memory.
        """
        global sender
        sender = f"From: {retrieve_reverse_path(line)}"

    def store_rcpt_to(line: str) -> None:
        """
        Reformat the rcpt to command and add it to the recipients list.

        Args: 
            line: The valid rcpt to command to be reformatted and saved in
                  memory.
        """
        global recipients
        recipients.append(f"To: {retrieve_reverse_path(line)}")

    def store_data(line: str) -> None:
        """
        Append the line retrieved as input to the message.

        Args:
            line: Saves the arbitrary text of the SMTP message in memory.
        """
        global message
        message += line

    def get_filepath(r_path: str) -> Path:
        """
        Returns the filepath for a given reverse path parsed from a rcpt to
        command.

        Args:
            r_path: The reverse path parsed from the rcpt to command.
        """
        # Remove opening <.
        ind: int = 0
        while (r_path[ind] != "<"):
            ind += 1
        ind += 1
        r_path = r_path[ind:]
        
        # Remove closing >.
        ind = 0
        while (r_path[ind] != ">"):
            ind += 1
        r_path = r_path[:ind]

        return Path(f"forward/{r_path}")

    def save_message() -> None:
        """
        Saves the various parts of a valid SMTP message held in memory to
        a file. If this file does not already exist, then this func will 
        make the file. The message could be saved to multiple files or 
        just one, depending on how many RCPT TO: (recievers) the message
        is intended for.
        """
        global sender, recipients, message

        # Create the smtp_message using the data stored in memory
        smtp_message: str = f"{sender}\n"
        for recipient in recipients:
            smtp_message += f"{recipient}\n"
        smtp_message += message
        
        # Save message to appropriate file.
        for recipient in recipients:
            path: Path = get_filepath(recipient)

            if (path.exists()):
                with path.open("a") as file:
                    file.write(smtp_message)
            else:
                with path.open("w") as file:
                    file.write(smtp_message)

    def reset_state() -> None:
        """
        Erase any stored data in the sender, recipients, or message global
        variables. Designed to be used when an exception is raised at any 
        point in the input process.
        """
        global state, sender, recipients, message

        sender = ""
        recipients.clear()
        message = ""
        state = 0

    def validate_mail_state(cmd_type: Cmd, line: str) -> None:
        """
        Validates input when a mail from command is expected and outputs
        the appropriate message.

        Args:
            cmd_type: Cmd indicating the type of command that was input.
            line: The input command.
        """
        global state

        try:
            if ((cmd_type is None) or (cmd_type == Cmd.MAIL)):
                # Call mail_from to handle the case where cmd_type is None. 
                mail_from(line)
                # Store the reverse path
                store_mail_from(line)
                # Indicate that the message was properly recieved and increment state
                sys.stdout.write("250 OK\n")
                state += 1

            elif ((cmd_type == Cmd.RCPT) or (cmd_type == Cmd.DATA)):
                    raise BadCmdSequenceException

        except (UnrecognizedCommandException,
                SyntaxException,
                BadCmdSequenceException,
                ) as e:
            # Reset the state of the program and output the proper error.
            reset_state()
            sys.stdout.write(f"{str(e)}\n")

    def validate_rcpt_state(cmd_type: Cmd, line: str) -> None:
        """
        Validates input when the first rcpt to command is expected and 
        outputs the proper message. Saves the line in memory if properly formatted.

        Args:
            cmd_type: The type of command input.
            line: The input that is currently being analyzed.
        """
        global state

        try:
            if ((cmd_type is None) or (cmd_type == Cmd.RCPT)):
                # Call rcpt_to to throw proper error if cmd_type is None.
                rcpt_to(line)
                # Store the reverse path.
                store_rcpt_to(line)
                # Output the proper message and increment state.
                sys.stdout.write("250 OK\n")
                state += 1

            elif ((cmd_type == Cmd.MAIL) or (cmd_type == Cmd.DATA)):
                raise BadCmdSequenceException()

        except (UnrecognizedCommandException,
                SyntaxException,
                BadCmdSequenceException,
                ) as e:
            # Reset state to beginning and output the proper error.
            reset_state()
            sys.stdout.write(f"{str(e)}\n")


    def validate_data_or_rcpt_state(cmd_type: Cmd, line: str) -> None:
        """
        Validate input when either a data command or rcpt to command are expected.
        outputs the proper message and saves the input in memory if necessary.

        Args:
            cmd_type: Cmd indicating what type of command the line is.
            line: the line recieved as input.
        """
        global state, data_terminated

        try:
            if ((cmd_type == Cmd.RCPT) or (cmd_type is None)):
                # Validate that cmd_type is not None.
                rcpt_to(line)
                # Store the input in memory and output the proper message.
                store_rcpt_to(line)
                sys.stdout.write("250 OK\n")

            elif (cmd_type == Cmd.DATA):
                # Output proper message and change state to accept incoming data.
                sys.stdout.write("354 Start mail input; end with <CRLF>.<CRLF>\n")
                data_terminated = False
                state += 1

            else:
                raise BadCmdSequenceException()

        except (UnrecognizedCommandException,
                SyntaxException,
                BadCmdSequenceException,
                ) as e:
            reset_state()
            sys.stdout.write(f"{str(e)}\n")


    def validate_data_or_terminate_state(cmd_type: Cmd, line: str) -> None:
        """
        Validates input when either arbitrary text or the "." termination
        line are expected. Outputs any necessary messages and saves data
        in memory. Once the "." termination line is recieved, calls the 
        save_message function to properly save the data.

        Args:
            cmd_type: Cmd indicating what type of command the line is.
            line: the line recieved as input.
        """
        global state, data_terminated

        if (terminator(line)):
            # Output proper message and flip data terminated flag to True.
            sys.stdout.write("250 OK\n")
            data_terminated = True
            # Save the message to the file system.
            save_message()
            # Clear out data from memory.
            reset_state()

        else:
            # Store data in memory.        
            store_data(line)

    def parse(line: str) -> None:
        """
        Parses input and processes SMTP messages.

        Args: 
            line: The most recent line of input.
        """
        global state
        cmd_type: Cmd = get_cmd_type(line)

        match state:
            case 0:
                validate_mail_state(cmd_type, line)
            case 1: 
                validate_rcpt_state(cmd_type, line)    
            case 2:
                validate_data_or_rcpt_state(cmd_type, line)
            case 3:
                validate_data_or_terminate_state(cmd_type, line)

if __name__ == "__main__":
    for line in sys.stdin:
        # Print the line to the terminal.
        sys.stdout.write(line)
        # Parse the line.
        parse(line)

    if (data_terminated == False):
        # Print proper error for not terminating data cmd.
        sys.stdout.write("501 Syntax error in parameters or arguments\n")
