"""File to hold all possible exceptions for HW3."""
# Jacob Brown
# I pledge the Comp 431 honor code.

class InvalidResponseCodeException(Exception):
    """Exception to handle improper formatting for mail-from-cmd non-terminal"""
    def __init__(self):
        super().__init__("Invalid response code.")


