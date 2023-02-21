from abc import ABC, abstractmethod


class HandlerStrategy(ABC):
    @abstractmethod
    def send_message(self, message, exchange, routing):
        pass

    @abstractmethod
    def get_message(self):
        pass

    @abstractmethod
    def optimize(self):
        pass
