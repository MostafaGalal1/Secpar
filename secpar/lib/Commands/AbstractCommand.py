from abc import abstractmethod


class AbstractCommand:
    @abstractmethod
    def execute(self):
        pass
