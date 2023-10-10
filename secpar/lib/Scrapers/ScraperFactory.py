from .CsesScraper import CsesScraper
from .CodeforcesScraper import CodeforcesScraper
from .VjudgeScraper import VjudgeScraper

# Factory class to create scraper instances based on the provided scraper name
class ScraperFactory:
    def __init__(self, scraper_name, data):
        self.scraper_name = scraper_name  # The name of the scraper to create
        self.data = data  # Data required for scraper initialization

    # Method to create a scraper instance based on the provided scraper name
    def create(self):
        if self.scraper_name == "cses":
            # Create and return an instance of the CsesScraper
            return CsesScraper(self.data["user_name"], self.data["password"], self.data["repo_owner"], self.data["repo_name"], self.data["access_token"])
        elif self.scraper_name == "codeforces":
            # Create and return an instance of the CodeforcesScraper
            return CodeforcesScraper(self.data["user_name"], self.data["repo_owner"], self.data["repo_name"], self.data["access_token"], self.data["use_tor"])
        elif self.scraper_name == "vjudge":
            # Create and return an instance of the VjudgeScraper
            return VjudgeScraper(self.data["user_name"], self.data["password"], self.data["repo_owner"], self.data["repo_name"], self.data["access_token"])
        else:
            # Raise an error if the provided scraper name is unsupported
            raise ValueError(f"Unsupported scraper name: {self.scraper_name}")

