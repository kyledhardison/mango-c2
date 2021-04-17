from abc import ABC, abstractmethod


class beacon(ABC):
    @abstractmethod
    def __init__(self, params):
        pass

    @abstractmethod
    def send(self, target, subject, message):
        pass

    @abstractmethod
    def receive(self):
        pass
