from time import sleep

from stem import Signal
from stem.control import Controller
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from secpar.lib.Scrapers.AbstractScraper import AbstractScraper

CONTROL_PORT = 9051
SOCKS_PORT = 9050
MAX_REQUESTS = 8


def get_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://localhost:{}'.format(SOCKS_PORT),
        'https': 'socks5h://localhost:{}'.format(SOCKS_PORT)
    }
    return session


def renew_connection():
    with Controller.from_port(port=CONTROL_PORT) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


def get_accepted_submissions_count(submissions):
    x = {}
    try:
        count = 0
        for submission in submissions:
            if get_submission_verdict(submission) and not is_gym_submission(submission) and get_problem_hashkey(submission) not in x:
                count += 1
                x[get_problem_hashkey(submission)] = ""
        return count
    except:
        raise EnvironmentError("Please enter valid handle")

def get_contest_id(submission):
    return submission.get('contestId')


def get_problem_name(submission):
    return submission.get('problem').get('name')

def get_problem_hashkey(submission):
    return str(submission.get('problem').get('contestId'))+submission.get('problem').get('index')


def get_problem_tags(submission):
    return submission.get('problem').get('tags')


def get_problem_index(submission):
    return submission.get("problem").get("index")


def get_problem_rating(submission):
    return submission.get('problem').get('rating')


def get_problem_link(submission):
    contest_id = get_contest_id(submission)
    problem_index = get_problem_index(submission)
    return f'https://codeforces.com/contest/{contest_id}/problem/{problem_index}'


def get_submission_verdict(submission):
    return submission.get('verdict') == "OK"


def get_submission_id(submission):
    return submission.get('id')


def get_submission_language(submission):
    return submission.get('programmingLanguage')


def get_submission_date(submission):
    submission_creation_date = datetime.utcfromtimestamp(submission.get('creationTimeSeconds'))
    return submission_creation_date.strftime('%Y-%m-%d %H:%M')


def get_submission_link(submission):
    contest_id = get_contest_id(submission)
    submission_id = get_submission_id(submission)
    return f'https://codeforces.com/contest/{contest_id}/submission/{submission_id}'


def get_submission_code(submission):
    return submission.find('pre').text


def is_gym_submission(submission):
    contest_id = get_contest_id(submission)
    return not contest_id or contest_id >= 100000  # check that the submission isn't in a gym


class CodeforcesScraper(AbstractScraper):

    def __init__(self, user_name, repo_owner, repo_name, access_token, use_tor=True):
        self.platform = 'Codeforces'
        self.platform_header = '''## Codeforces
| # | Problem | Solution | Tags | Submitted |
| - |  -----  | -------- | ---- | --------- |\n'''
        super().__init__(self.platform, user_name, '', repo_owner, repo_name, access_token, self.platform_header)

        self.session = get_tor_session() if use_tor else requests.session()
        self.use_tor = use_tor
        self.request_count = 0

    def login(self):
        pass

    def get_submissions(self):
        user_submissions_url = f'https://codeforces.com/api/user.status?handle={self.username}'
        response = self.session.get(user_submissions_url, verify=False, headers=self.headers)
        submissions = response.json().get("result")

        end = problems_count = get_accepted_submissions_count(submissions)

        for submission in submissions:
            problem_key = get_problem_hashkey(submission)
            if not get_submission_verdict(submission) or is_gym_submission(submission) or self.check_already_added(problem_key):
                continue
            if self.use_tor: self.push_code(submission)
            self.update_already_added(submission, problems_count)
            self.print_progress_bar(end-problems_count+1,end)
            sleep(0.05)
            problems_count -= 1

    def push_code(self, submission):
        submission_html = self.get_submission_html(submission)
        name = get_problem_name(submission)
        code = get_submission_code(submission_html)

        if code is not None:
            directory = self.generate_directory_link(submission)
            try:
                self.repo.create_file(directory, f"Add problem `{name}`", code)
            except:
                pass

    def update_already_added(self, submission, problems_count):
        problem_key = get_problem_hashkey(submission)
        name = get_problem_name(submission)
        problem_link = get_problem_link(submission)
        directory_link = self.repo.html_url + '/blob/main/' + self.generate_directory_link(submission) if self.use_tor else get_submission_link(submission)
        language = get_submission_language(submission)
        tags = get_problem_tags(submission)
        rating = get_problem_rating(submission)
        date = get_submission_date(submission)
        tags = " ".join([f"`{tag}`" for tag in tags])

        self.current_submissions[problem_key] = {'id': problem_key, 'count': problems_count, 'name': name,
                                                        'problem_link': problem_link, 'language': language,
                                                        'directory_link': directory_link, 'tags': f'{tags} `{rating}`',
                                                        'date': date}

    def get_submission_html(self, submission):
        submission_url = get_submission_link(submission)

        while True:
            self.request_count += 1
            if self.request_count == MAX_REQUESTS:
                self.session = get_tor_session()
                renew_connection()
                self.request_count = 0
            try:
                response = self.session.get(submission_url, verify=False, headers=self.headers)
                if response.status_code == 200:
                    return BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(e)

    def generate_directory_link(self, submission):
        contest_id = get_contest_id(submission)
        submission_id = get_submission_id(submission)
        language = get_submission_language(submission)
        return f'{self.platform}/{contest_id}/{submission_id}.{self.extensions[language]}'
