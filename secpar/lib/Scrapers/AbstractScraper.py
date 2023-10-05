import json
import os

import requests
from abc import ABC, abstractmethod
from github import Github

requests.packages.urllib3.disable_warnings()


class AbstractScraper(ABC):
    def __init__(self, platform, username, password, repo_owner, repo_name, access_token, platform_header):
        git = Github(access_token)

        self.platform = platform
        self.username = username
        self.password = password
        self.headers = {"accept": "application/json, text/javascript, */*; q=0.01",
                        "accept-language": "en-GB,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-US;q=0.6",
                        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
                        "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "x-requested-with": "XMLHttpRequest",
                        "Referer": self.username, "Referrer-Policy": "strict-origin-when-cross-origin"}
        self.platform_header = platform_header
        self.current_submissions = {}
        self.extensions = {}
        self.repo = git.get_user(repo_owner).get_repo(repo_name)

    def scrape(self):
        self.load_extensions()
        self.load_already_added()
        self.login()
        self.get_submissions()
        self.update_submission_json()
        self.update_readme()

    def load_extensions(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Resources", "Extensions", f"{self.platform}Extensions.json")
        with open(path, 'r') as json_file:
            self.extensions = json.load(json_file)

    def load_already_added(self):
        submissions_path = f'submissions/{self.platform}Submissions.json'
        try:
            json_string = self.repo.get_contents(submissions_path).decoded_content.decode('utf-8')
            self.current_submissions = json.loads(json_string)['Submissions']
            self.current_submissions = {obj['id']: obj for obj in self.current_submissions}
        except:
            self.current_submissions = {}

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def get_submissions(self):
        pass

    @abstractmethod
    def get_submission_html(self, submission):
        pass

    def check_already_added(self, submission_id):
        if str(submission_id) in self.current_submissions:
            return True
        return False

    @abstractmethod
    def update_already_added(self, submission_id, problems_count):
        pass

    @abstractmethod
    def generate_directory_link(self, submission):
        pass

    def update_submission_json(self):
        self.current_submissions = list(self.current_submissions.values())
        self.current_submissions = sorted(self.current_submissions, key=lambda item: item['date'], reverse=True)
        print(self.current_submissions)

        try:
            self.repo.update_file(f'submissions/{self.platform}Submissions.json', f"Update {self.platform}Submissions.json", json.dumps({'Header': self.platform_header, 'Submissions': self.current_submissions}), self.repo.get_contents(f'submissions/{self.platform}Submissions.json').sha)
        except:
            self.repo.create_file(f'submissions/{self.platform}Submissions.json', f"Create {self.platform}Submissions.json", json.dumps({'Header': self.platform_header, 'Submissions': self.current_submissions}))

    # todo: this method is general and will apply three formatters on three platforms so i think about making a factory of formatters each contains a method for writing in readme for specific platform
    # note: submissions json files now should be already generatable and updatable
    def update_readme(self):
        pass
