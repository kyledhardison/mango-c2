from abc import ABC, abstractmethod

class beacon(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def receive(self):
        pass