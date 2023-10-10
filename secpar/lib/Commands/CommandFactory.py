# Import necessary modules.
import os
from secpar.lib.Commands.InitCommand import InitCommand
from secpar.lib.Commands.ScrapeCommand import ScrapCommand
from secpar.lib.Commands.AbstractCommand import AbstractCommand

# Define a class called 'CommandFactory' responsible for creating command objects.
class CommandFactory:
    def __init__(self, data):
        self.input_data = data  # Initialize the factory with input data.

    def create(self):
        # Check the 'command' attribute in the input data to determine the type of command to create.
        if self.input_data.command == "init":
            return InitCommand()  # Return an 'InitCommand' object if the command is 'init'.
        elif self.input_data.scrap is not None:
            return ScrapCommand(self.input_data.scrap)  # Return a 'ScrapCommand' object if 'scrap' is not None.
        elif self.input_data.command is None:
            # If 'command' is None, check if a specific file exists and provide feedback to the user.
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Resources", "User", "UserData.json")
            if os.path.exists(path):
                print("Please specify the platform to scrap, example: `secpar -s codeforces`")
                return AbstractCommand()  # Return an 'AbstractCommand' object.
            else:
                return InitCommand()  # Return an 'InitCommand' object if the file does not exist.

# End of the 'CommandFactory' class definition.
