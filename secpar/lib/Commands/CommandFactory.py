from .InitCommand import *
from .ScrapCommand import *
from .AbstractCommand import *

class CommandFactory:
    def __init__(self, data):
        self.input_data = data

    def create(self):
        if self.input_data.command == "init" :
            return InitCommand()
        elif self.input_data.scrap is not None :
            return ScrapCommand(self.input_data.scrap)
        elif self.input_data.command is None :
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Resources", "User", "UserData.json")
            if os.path.exists(path):
                print("Please specify the platform to scrap, example: `CP_Scraper -s codeforces`")
                return AbstractCommand()
            else:
                return InitCommand()