# Jacob Brown
# I pledge the Comp 431 honor code.

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
    # Flag to track when data is being read from input.
    reading_data: bool = False


    def is_mail(self, line: str) -> bool:
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

    def is_rcpt(self, line: str) -> bool:
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

    def is_data(self, line: str) -> bool:
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

    def get_cmd_type(self, line: str) -> Cmd:
        """
        Finds the command type of a given line, if one exists.

        Args:
            line: The line to find the command type of. More specifically
                  The non-terminal that the line maps to.

        Returns:
            Cmd: either one of the three options from the Cmd enum defined above or None.
        """
        if (self.is_mail(line)):
            return Cmd.MAIL
        elif (self.is_rcpt(line)):
            return Cmd.RCPT
        elif (self.is_data(line)):
            return Cmd.DATA
        else:
            return None

    def retrieve_reverse_path(self, line: str) -> str:
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

        # Remove opening and closing <>.
        line = line[1:len(line) - 1]

        return line

    def store_mail_from(self, line: str) -> None:
        """
        Reformat the mail from command and store it in the sender global var.

        Args:
            line: The valid mail from cmd to be reformatted and saved in
                  memory.
        """
        self.sender = f"From: {self.retrieve_reverse_path(line)}"

    def parse_domain(self, reverse_path: str) -> str:
        """
        Parses the domain from a valid reverse_path

        Args:
            reverse_path: An already validate reverse_path
        """
        while (reverse_path[0] != "@"):
            reverse_path = reverse_path[1:]
        return reverse_path[1:]

    def store_rcpt_to(self, line: str) -> None:
        """
        Reformat the rcpt to command and add it to the recipients list.

        Args: 
            line: The valid rcpt to command to be reformatted and saved in
                  memory.
        """
        reverse_path: str = self.retrieve_reverse_path(line)
        domain: str = self.parse_domain(reverse_path)
        if domain not in self.recipients:
            self.recipients.append(domain)

    def store_data(self, line: str) -> None:
        """
        Append the line retrieved as input to the message.

        Args:
            line: Saves the arbitrary text of the SMTP message in memory.
        """
        self.message += line

    def save_message(self) -> None:
        """
        Saves the various parts of a valid SMTP message held in memory to
        a file. If this file does not already exist, then this func will 
        make the file. The message could be saved to multiple files or 
        just one, depending on how many RCPT TO: (recievers) the message
        is intended for.
        """
        # Save message to appropriate file.
        for recipient in self.recipients:
            path: Path = Path(f"forward/{recipient}")

            if (path.exists()):
                with path.open("a") as file:
                    file.write(self.message)
            else:
                with path.open("w") as file:
                    file.write(self.message)

    def reset_state(self) -> None:
        """
        Erase any stored data in the sender, recipients, or message global
        variables. Designed to be used when an exception is raised at any 
        point in the input process.
        """
        self.sender = ""
        self.recipients.clear()
        self.message = ""
        self.state = 0

    def validate_mail_state(self, cmd_type: Cmd, line: str) -> str:
        """
        Validates input when a mail from command is expected and outputs
        the appropriate message.

        Args:
            cmd_type: Cmd indicating the type of command that was input.
            line: The input command.

        Returns:
            str: The appropriate success or error message.
        """
        try:
            if ((cmd_type is None) or (cmd_type == Cmd.MAIL)):
                # Call mail_from to handle the case where cmd_type is None. 
                mail_from(line)
                # Store the reverse path
                self.store_mail_from(line)
                # Indicate that the message was properly recieved and increment state
                self.state += 1
                return "250 OK"

            elif ((cmd_type == Cmd.RCPT) or (cmd_type == Cmd.DATA)):
                    raise BadCmdSequenceException

        except (UnrecognizedCommandException,
                SyntaxException,
                BadCmdSequenceException,
                ) as e:
            # Reset the state of the program and output the proper error.
            self.reset_state()
            return str(e)

    def validate_rcpt_state(self, cmd_type: Cmd, line: str) -> str:
        """
        Validates input when the first rcpt to command is expected and 
        outputs the proper message. Saves the line in memory if properly formatted.

        Args:
            cmd_type: The type of command input.
            line: The input that is currently being analyzed.

        Returns:
            str: The appropriate success or error message.
        """
        try:
            if ((cmd_type is None) or (cmd_type == Cmd.RCPT)):
                # Call rcpt_to to throw proper error if cmd_type is None.
                rcpt_to(line)
                # Store the reverse path.
                self.store_rcpt_to(line)
                # Output the proper message and increment state.
                self.state += 1
                return "250 OK"

            elif ((cmd_type == Cmd.MAIL) or (cmd_type == Cmd.DATA)):
                raise BadCmdSequenceException()

        except (UnrecognizedCommandException,
                SyntaxException,
                BadCmdSequenceException,
                ) as e:
            # Reset state to beginning and output the proper error.
            self.reset_state()
            return str(e)


    def validate_data_or_rcpt_state(self, cmd_type: Cmd, line: str) -> str:
        """
        Validate input when either a data command or rcpt to command are expected.
        outputs the proper message and saves the input in memory if necessary.

        Args:
            cmd_type: Cmd indicating what type of command the line is.
            line: the line recieved as input.

        Returns:
            str: The appropriate success or error message.
        """
        try:
            if ((cmd_type == Cmd.RCPT) or (cmd_type is None)):
                # Validate that cmd_type is not None.
                rcpt_to(line)
                # Store the input in memory and output the proper message.
                self.store_rcpt_to(line)
                return "250 OK"

            elif (cmd_type == Cmd.DATA):
                # Output proper message and change state to accept incoming data.
                self.data_terminated = False
                self.state += 1

                return "354 Start mail input; end with <CRLF>.<CRLF>"

            else:
                raise BadCmdSequenceException()

        except (UnrecognizedCommandException,
                SyntaxException,
                BadCmdSequenceException,
                ) as e:
            self.reset_state()
            return str(e)

    def validate_data_or_terminate_state(self, cmd_type: Cmd, line: str) -> str:
        """
        Validates input when either arbitrary text or the "." termination
        line are expected. Outputs any necessary messages and saves data
        in memory. Once the "." termination line is recieved, calls the 
        save_message function to properly save the data.

        Args:
            cmd_type: Cmd indicating what type of command the line is.
            line: the line recieved as input.

        Returns:
            str: The appropriate success or error message.
        """
        if (terminator(line)):
            # Output proper message and flip data terminated flag to True.
            self.data_terminated = True
            # Save the message to the file system.
            self.save_message()
            # Clear out data from memory.
            self.reset_state()
            # Turn of reading data flag.
            self.reading_data = False

            return "250 OK"

        else:
            # Store data in memory.        
            self.reading_data = True
            self.store_data(line)
            return None

    def parse(self, line: str) -> str:
        """
        Parses input and processes SMTP messages.

        Args: 
            line: The most recent line of input.

        Returns:
            str: The string containing the error or success message.
        """
        cmd_type: Cmd = self.get_cmd_type(line)

        match self.state:
            case 0:
                return self.validate_mail_state(cmd_type, line)
            case 1: 
                return self.validate_rcpt_state(cmd_type, line)    
            case 2:
                return self.validate_data_or_rcpt_state(cmd_type, line)
            case 3:
                return self.validate_data_or_terminate_state(cmd_type, line)
