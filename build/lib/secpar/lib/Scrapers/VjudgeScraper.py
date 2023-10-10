import requests
from datetime import datetime
from secpar.lib.Scrapers.AbstractScraper import AbstractScraper

# Function to get the problem number from a submission
def get_problem_number(submission):
    return submission.get('probNum')

# Function to get the problem hashkey from a submission
def get_problem_hashkey(submission):
    return submission.get('oj') + submission.get('probNum')


# Function to get the name of the online judge (OJ) from a submission
def get_oj_name(submission):
    return submission.get('oj')

# Function to generate a link to the problem on vjudge
def get_problem_link(submission):
    oj = get_oj_name(submission)
    problem_name = get_problem_number(submission)
    return f'https://vjudge.net/problem/{oj}-{problem_name}'

# Function to get the submission ID from a submission
def get_submission_id(submission):
    return submission.get('runId')

# Function to generate a link to the submission on vjudge
def get_submission_url(submission):
    submission_id = get_submission_id(submission)
    return f'https://vjudge.net/solution/data/{submission_id}'

# Function to get the programming language used in a submission
def get_submission_language(submission):
    return submission.get('language')

# Function to get the submission date and time
def get_submission_date(submission):
    timestamp = datetime.fromtimestamp(submission.get('time') / 1000)
    return timestamp.strftime("%Y:%m:%d %H:%M")

# Function to get the code of a submission
def get_submission_code(submission):
    return submission.get('code')

# VjudgeScraper class
class VjudgeScraper(AbstractScraper):

    def __init__(self, username, password, repo_owner, repo_name, access_token):
        self.platform = 'Vjudge'
        self.platform_header = '''## Vjudge<a name="vjudge"></a>
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

    # Function to get the count of accepted submissions from multiple platforms
    def get_accepted_submissions_count(self, submissions):
        count = 0
        for platform in submissions:
            for submission in submissions.get(platform):
                if not self.check_already_added(platform + submission):
                    count += 1
        return count

    # Function to retrieve new submissions from vjudge
    def get_new_submissions(self):
        submissions_per_page = 20
        page_count = 0
        new_submissions = []
        submissions_hash = {}

        while True:
            page_submissions = self.get_page_submissions(page_count, submissions_per_page)
            if len(page_submissions) == 0:
                break
            for submission in page_submissions:
                problem_key = get_problem_hashkey(submission)
                if problem_key not in submissions_hash and not self.check_already_added(problem_key):
                    new_submissions.append(submission)
                    submissions_hash[problem_key] = True
            page_count += 1

        return new_submissions

    # Function to retrieve submissions from a specific page
    def get_submissions(self):
        submissions_per_update = 100
        progress_count = 0
        new_submissions = self.get_new_submissions()
        end = len(new_submissions)

        for submission in new_submissions:
            progress_count += 1
            self.print_progress_bar(progress_count, end)
            self.push_code(submission)
            self.update_already_added(submission)

            if progress_count % submissions_per_update == 0:
                self.update_submission_json()
        self.print_progress_bar(1, 1)
        print("")

    def get_problem_name(self, submission):
        problem_number = get_problem_number(submission)
        response = self.session.get(
            f'https://vjudge.net/problem/data?draw=0&start=0&length=20&OJId=All&probNum={problem_number}&source=&category=all',
            verify=False, timeout=20)
        return response.json().get("data")[0].get('title')

    def get_page_submissions(self, page, submissions_per_page):
        response = self.session.get(f'https://vjudge.net/status/data?draw={page}&start={page * submissions_per_page}'
                                    f'&length=20&un={self.username}&OJId=All&res=1&orderBy=run_id', verify=False, headers=self.headers, timeout=20)
        return response.json().get("data")

    # Function to push code to the repository
    def push_code(self, submission):
        submission_html = self.get_submission_html(submission)
        name = self.get_problem_name(submission_html)
        code = get_submission_code(submission_html)

        if code is not None:
            directory = self.generate_directory_link(submission)
            try:
                self.repo.create_file(directory, f"Add problem `{name}`", code, 'main')
            except:
                pass

    # Function to update the record of already added submissions
    def update_already_added(self, submission):
        problem_key = get_problem_hashkey(submission)
        name = self.get_problem_name(submission)
        problem_link = get_problem_link(submission)
        directory_link = self.repo.html_url + '/blob/main/' + self.generate_directory_link(submission)
        language = get_submission_language(submission)
        date = get_submission_date(submission)

        self.current_submissions[problem_key] = {'id': problem_key, 'name': name,
                                                        'problem_link': problem_link, 'language': language,
                                                        'directory_link': directory_link, 'date': date}

    # Function to retrieve the HTML of a submission
    def get_submission_html(self, submission):
        submission_url = get_submission_url(submission)
        response = self.session.get(submission_url, verify=False, headers=self.headers, timeout=20)
        return response.json()

    # Function to generate the directory link for a submission
    def generate_directory_link(self, submission):
        problem_number = get_problem_number(submission)
        oj = get_oj_name(submission)
        return f'{self.platform}/{oj}/{problem_number}.cpp'
