# Import necessary modules.
import os
import json
from secpar.lib.Commands.AbstractCommand import AbstractCommand

# Define a class called 'InitCommand' that inherits from 'AbstractCommand'.
class InitCommand(AbstractCommand):
    def __init__(self):
        # Define the path to the 'UserData.json' file.
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Resources", "User", "UserData.json")

        # If the file exists, remove it to start fresh.
        if os.path.exists(self.path):
            os.remove(self.path)

    def execute(self):
        # Prompt the user for GitHub-related information.
        github_name = input("Enter your GitHub username: ")
        github_repo_name = input("Enter the name of your GitHub repository: ")
        access_token_github = input("Enter your GitHub access token: ")

        # Create a dictionary containing user data.
        user_data = {
            "repo_owner": github_name,
            "repo_name": github_repo_name,
            "access_token": access_token_github,
        }

        try:
            # Write the user data to the 'UserData.json' file.
            with open(self.path, 'w') as json_file:
                json.dump(user_data, json_file, indent=4)
        except Exception as e:
            # Handle any exceptions that may occur during file writing.
            print(f"Error writing to 'UserData.json': {e}")

# End of the 'InitCommand' class definition.
