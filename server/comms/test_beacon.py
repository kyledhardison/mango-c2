from .template import beacon


class test_beacon(beacon):
    def __init__(self, params):
        self.params = params
        TEST_VAR = "ABC"

    def send(self, message):
        print("Beacon sent!")
        return 0

    def receive(self):
        return "Message received 2"
