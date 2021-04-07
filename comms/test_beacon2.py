from .template import beacon

class test_beacon2(beacon):
    def __init__(self):
        TEST_VAR = "ABC"

    def send(self, message):
        print("Beacon sent!")
        return 0
    
    def receive(self):
        return "Message received 2"