#!/usr/bin/python3

import os
import time
import importlib

# Global definitions
SETTINGS_FILE = "settings.conf"
COMMS_DIR = "comms"


class core:
    def __init__(self):
        self.params = {}
        self.classes = []
        
        # Read settings into self.params
        f = open(SETTINGS_FILE, "r")
        file = f.read().split("\n")
        for line in file:
            if line.startswith("#") or line == '':
                pass
            else:
                new = line.split(" ")
                self.params[new[0]] = new[1]
        
        # Dynamically import comms modules
        beacon_files = os.listdir(COMMS_DIR)
        for b in beacon_files:
            if not (b == "__pycache__" or b == "__init__.py" or b == "template.py"):
                new_class = getattr(importlib.import_module(COMMS_DIR + "." + b[:-3]), b[:-3])
                self.classes.append(new_class)
        
        print(self.classes)

    def do_beacon(self):
        #TODO: Perform a beacon
        pass

    def run_core(self):
        mods = []
        for b in self.classes:
            mods.append(b())

        for m in mods:
            print(m.receive())


def main():
    test = core()
    test.run_core()

if __name__ == "__main__":
    main()
