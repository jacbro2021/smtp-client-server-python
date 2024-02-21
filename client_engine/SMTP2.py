"""Engine for SMTP client."""
# Jacob Brown
# I pledge the Comp 431 honor code.

from reverse_path import parse 

class ClientEngine:
    """Engine to hold state for the SMTP client."""
    # State for the client
    state: int = 0

    def process_input(self, line: str):


