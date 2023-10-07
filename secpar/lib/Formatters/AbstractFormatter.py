import json
from abc import ABC, abstractmethod


class AbstractFormatter(ABC):
    def __init__(self, repo):
        self.platform = self.__class__.__name__.split("Formatter")[0]
        self.repo = repo
        self.data = self.get_data()

    @abstractmethod
    def format(self):
        pass
    def get_data(self):
        file_contents = self.repo.get_contents(f"submissions/{self.platform}Submissions.json")
        data = json.loads(file_contents.decoded_content.decode('utf-8'))
        return data
    def get_header(self):
        return self.data.get("Header")
