import requests
from datetime import datetime
from secpar.lib.Scrapers.AbstractScraper import AbstractScraper


def get_problem_number(submission):
    return submission.get('probNum')

def get_problem_hashkey(submission):
    return submission.get('oj') + submission.get('probNum')

def get_problem_name(submission):
    problem_number = get_problem_number(submission)
    response = requests.get(f'https://vjudge.net/problem/data?draw=0&start=0&length=20&OJId=All&probNum={problem_number}&source=&category=all')
    return response.json().get("data")[0].get('title')


def get_oj_name(submission):
    return submission.get('oj')


def get_problem_link(submission):
    oj = get_oj_name(submission)
    problem_name = get_problem_number(submission)
    return f'https://vjudge.net/problem/{oj}-{problem_name}'


def get_submission_id(submission):
    return submission.get('runId')


def get_submission_url(submission):
    submission_id = get_submission_id(submission)
    return f'https://vjudge.net/solution/data/{submission_id}'


def get_submission_language(submission):
    return submission.get('language')


def get_submission_date(submission):
    timestamp = datetime.fromtimestamp(submission.get('time') / 1000)
    return timestamp.strftime("%Y:%m:%d %H:%M")


def get_submission_code(submission):
    return submission.get('code')


class VjudgeScraper(AbstractScraper):

    def __init__(self, username, password, repo_owner, repo_name, access_token):
        self.platform = 'Vjudge'
        self.platform_header = '''## vjudge
| # | Problem | Solution | Submitted |
| - |  -----  | -------- | --------- |\n'''
        super().__init__(self.platform, username, password, repo_owner, repo_name, access_token, self.platform_header)

        self.session = requests.session()
        self.credits = {
            'username': self.username,
            'password': self.password,
            'captcha': '',
        }

    def login(self):
        login_url = 'https://vjudge.net/user/login'
        response = self.session.post(login_url, self.credits)
        return response.text == 'success'

    def get_accepted_submissions_count(slef, submissions):
        count = 0
        for platform in submissions:
            for submission in submissions.get(platform):
                if not slef.check_already_added(platform+submission):
                    count += 1
        return count

    def get_submissions(self):
        try:
            user_submissions_url = f'https://vjudge.net/user/solveDetail/{self.username}'
            response = self.session.get(user_submissions_url, verify=False, headers=self.headers)
            submissions = response.json().get("acRecords")
        except:
            raise EnvironmentError("Failed to log in wrong username or password")

        end = self.get_accepted_submissions_count(submissions)
        progress_count = 0

        submissions_per_page = 20
        page_count = 0

        while True:
            page_submissions = self.get_page_submissions(page_count, submissions_per_page)
            if not page_submissions:
                break
            for submission in page_submissions:
                problem_key = get_problem_hashkey(submission)
                if self.check_already_added(problem_key):
                    continue
                self.print_progress_bar(progress_count + 1, end)
                progress_count += 1
                self.push_code(submission)
                self.update_already_added(submission)

                if progress_count % 100 == 0:
                    self.update_submission_json()

            page_count += 1

    def get_page_submissions(self, page, submissions_per_page):
        response = self.session.get(f'https://vjudge.net/status/data?draw={page}&start={page * submissions_per_page}'
                                    f'&length=20&un={self.username}&OJId=All&res=1&orderBy=run_id')
        return response.json().get("data")

    def push_code(self, submission):
        submission_html = self.get_submission_html(submission)
        name = get_problem_name(submission_html)
        code = get_submission_code(submission_html)

        if code is not None:
            directory = self.generate_directory_link(submission)
            try:
                self.repo.create_file(directory, f"Add problem `{name}`", code)
            except:
                pass

    def update_already_added(self, submission):
        problem_key = get_problem_hashkey(submission)
        name = get_problem_name(submission)
        problem_link = get_problem_link(submission)
        directory_link = self.repo.html_url + '/blob/main/' + self.generate_directory_link(submission)
        language = get_submission_language(submission)
        date = get_submission_date(submission)

        self.current_submissions[problem_key] = {'id': problem_key, 'name': name,
                                                        'problem_link': problem_link, 'language': language,
                                                        'directory_link': directory_link, 'date': date}

    def get_submission_html(self, submission):
        submission_url = get_submission_url(submission)
        response = self.session.get(submission_url)
        return response.json()

    def generate_directory_link(self, submission):
        problem_number = get_problem_number(submission)
        oj = get_oj_name(submission)
        return f'{self.platform}/{oj}/{problem_number}.cpp'
