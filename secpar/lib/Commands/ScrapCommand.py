import os
import json
import getpass

from .AbstractCommand import *
from ..Scrapers.ScraperFactory import ScraperFactory
from ..Formatters.ReadMeBuilder import ReadMeBuilder


class ScrapCommand(AbstractCommand):
    def __init__(self, scraper_name):
        self.scraper_name = scraper_name.lower()
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Resources", "User", "UserData.json")
        try:
            with open(self.path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            raise ValueError("You need to initialize your data first")

    def execute(self):
        if self.scraper_name == "cses" or self.scraper_name == "vjudge":
            self.data["user_name"] = input(f"Enter your {self.scraper_name} username: ")
            self.data["password"] = getpass.getpass("Enter your password: ")
        elif self.scraper_name == "codeforces":
            self.data["user_name"] = input("Enter your Codeforces handle: ")

        self.data["platforms"][self.scraper_name] = ""

        ScraperFactory(self.scraper_name, self.data).create().scrape()
        readme_builder = ReadMeBuilder(self.data)
        readme_content = readme_builder.build()
        readme_builder.update_readme(readme_content)

        try:
            with open(self.path, 'w') as json_file:
                json.dump(self.data, json_file, indent=4)
        except Exception as e:
            print(f"Error writing to 'userdata.json': {e}")
