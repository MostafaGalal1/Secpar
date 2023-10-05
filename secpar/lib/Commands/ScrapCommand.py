import os
import json
import getpass

from .AbstractCommand import *
from ..Scrapers.ScraperFactory import ScraperFactory

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

        print(self.data)
        scraper = ScraperFactory(self.scraper_name, self.data).create()
        return scraper.scrape()
