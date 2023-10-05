from abc import ABC, abstractmethod


class AbstractFormatter(ABC):

    @abstractmethod
    def format(self):
        pass
