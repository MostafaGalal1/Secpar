import json
from abc import ABC, abstractmethod

# Define an abstract base class called 'AbstractFormatter' that inherits from 'ABC' (Abstract Base Class).
class AbstractFormatter(ABC):
    def __init__(self, repo):
        # Initialize common attributes for formatters.
        self.platform = self.__class__.__name__.split("Formatter")[0]  # Get the platform name from the class name.
        self.repo = repo
        self.data = self.get_data()  # Load data from a specific file.

    @abstractmethod
    def format(self):
        pass  # Declare an abstract 'format' method that should be implemented in concrete formatter classes.

    def get_data(self):
        try:
            # Attempt to retrieve and parse data from a specific file in the repository.
            file_contents = self.repo.get_contents(f"submissions/{self.platform}Submissions.json")
            data = json.loads(file_contents.decoded_content.decode('utf-8'))
            return data
        except:
            pass  # Handle exceptions gracefully (e.g., if the file doesn't exist).

    def get_header(self):
        return self.data.get("Header")  # Get the "Header" information from the loaded data.

# End of the 'AbstractFormatter' class definition.
