import os
import json
import getpass

from secpar.lib.Commands.AbstractCommand import *
from secpar.lib.Scrapers.ScraperFactory import ScraperFactory
from secpar.lib.Formatters.ReadMeBuilder import ReadMeBuilder


class ScrapeCommand(AbstractCommand):
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
            use_tor_input = input("Do you want to use tor? (y/n): ").strip().lower()
            self.data["use_tor"] = True if use_tor_input =="y" else False

        ScraperFactory(self.scraper_name, self.data).create().scrape()
        readme_builder = ReadMeBuilder(self.data)
        readme_content = readme_builder.build()
        readme_builder.update_readme(readme_content)
