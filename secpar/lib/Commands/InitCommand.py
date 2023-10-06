import os
import json

from .AbstractCommand import *

class InitCommand(AbstractCommand):
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Resources", "User", "UserData.json")
        if os.path.exists(self.path):
            os.remove(self.path)

    def execute(self):
        github_name = input("Enter your GitHub username: ")
        github_repo_name = input("Enter the name of your GitHub repository: ")
        access_token_github = input("Enter your GitHub access token: ")

        user_data = {
            "repo_owner": github_name,
            "repo_name": github_repo_name,
            "access_token": access_token_github,
            "platforms": {}
        }

        try:
            with open(self.path, 'w') as json_file:
                json.dump(user_data, json_file, indent=4)
        except Exception as e:
            print(f"Error writing to 'userdata.json': {e}")
