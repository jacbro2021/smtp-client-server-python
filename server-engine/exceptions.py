# Jacob Brown
# I pledge the Comp 431 honor code.

class MailFromCmdException(Exception):
    """Exception to handle improper formatting for mail-from-cmd non-terminal"""
    def __init__(self):
        super().__init__("ERROR -- mail-from-cmd")

class RcptToCmdException(Exception):
    """Exception to handle improper formatting for the reciept-to-cmd non-terminal"""
    def __init__(self):
        super().__init__("ERROR -- rcpt-to-cmd")

class DataCmdException(Exception):
    """Exception to handle improper formatting for the data non-terminal"""
    def __init__(self):
        super().__init__("Error -- data-cmd")

class WhitespaceException(Exception):
    """Exception to handle missing whitespace."""
    def __init__(self):
        super().__init__("ERROR -- whitespace")

class PathException(Exception):
    """Exception to handle improper path formatting."""
    def __init__(self):
        super().__init__("ERROR -- path")

class MailboxException(Exception):
    """Exception to handle improper mailbox formatting."""
    def __init__(self):
        super().__init__("ERROR -- mailbox")

class StringException(Exception):
    """Exception to handle improper string formatting."""
    def __init__(self):
        super().__init__("ERROR -- string")

class ElementException(Exception):
    """Exception to handle improper element formatting."""
    def __init__(self):
        super().__init__("ERROR -- element")

class CRLFException(Exception):
    """Exception to handle a missing newline at the end of the command."""
    def __init__(self):
        super().__init__("ERROR -- CRLF")

class UnrecognizedCommandException(Exception):
    """Exception handle the input of an unrecognized command."""
    def __init__(self):
        super().__init__("500 Syntax error: command unrecognized")

class SyntaxException(Exception):
    """Exception to handle syntax errors in command arguments."""
    def __init__(self):
        super().__init__("501 Syntax error in parameters or arguments")

class BadCmdSequenceException(Exception):
    """Exception to handle commands being input in the wrong sequence."""
    def __init__(self):
        super().__init__("503 Bad sequence of commands")


