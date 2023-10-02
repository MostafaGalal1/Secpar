from CsesScraper import CsesScraper
from CodeforcesScraper import CodeforcesScraper


class ScraperFactory:
    def __init__(self, scraper_name, data):
        self.scraper_name = scraper_name
        self.data = data

    def create(self):
        if self.scraper_name == "cses":
            return CsesScraper(self.data["user_name"], self.data["password"], self.data["repo_owner"], self.data["repo_name"], self.data["access_token"])
        elif self.scraper_name == "codeforces":
            return CodeforcesScraper(self.data["user_name"], self.data["repo_owner"], self.data["repo_name"], self.data["access_token"])
        else:
            raise ValueError(f"Unsupported scraper name: {self.scraper_name}")
