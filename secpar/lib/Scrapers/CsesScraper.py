import requests
from datetime import datetime
from bs4 import BeautifulSoup
from secpar.lib.Scrapers.AbstractScraper import AbstractScraper

def get_accepted_submissions_count(account):

    try:
        response = requests.get(account)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.findAll('table', class_='narrow')[1]
        return int(table.find('a').text)
    except:
        raise EnvironmentError("Failed to log in wrong username or password")

def get_problem_name(submission):
    return submission.find('td', string='Task:').next_sibling.text


def get_problem_tags(submission):
    return submission.find('div', class_='nav sidebar').find('h4').text


def get_problem_link(submission):
    return 'https://cses.fi' + submission.find('td', string='Task:').find_next('a').get('href')


def get_submission_id(problem):
    return problem.find('a').text.strip()


def get_submission_language(submission):
    return submission.find('td', string='Language:').next_sibling.text


def get_submission_date(submission):
    timestamp_str = submission.find('td', string='Submission time:').next_sibling.text
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S %z")
    return timestamp.strftime("%Y-%m-%d %H:%M")


def get_submission_code(submission):
    return submission.find('pre', class_='prettyprint').text


def check_problem_solved(problem):
    return problem.find('span', class_='task-score icon full')


def fix_cascaded_html(topic):
    cascaded_problems = topic.find_all('li')
    corrected_soup = BeautifulSoup("<ul></ul>", "html.parser")

    for cascaded_problem in cascaded_problems:
        corrected_soup.ul.append(cascaded_problem)

    return corrected_soup.prettify()


class CsesScraper(AbstractScraper):

    def __init__(self, username, password, repo_owner, repo_name, access_token):
        self.platform = 'Cses'
        self.platform_header = '''## CSES
| # | Problem | Solution | Tags | Submitted |
| - |  -----  | -------- | ---- | --------- |\n'''
        super().__init__(self.platform, username, password, repo_owner, repo_name, access_token, self.platform_header)

        self.session = requests.session()
        self.credits = {
            'csrf_token': '',
            'nick': self.username,
            'pass': self.password
        }

    def login(self):
        login_url = 'https://cses.fi/login'
        response = self.session.get(login_url, verify=False, headers=self.headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.credits['csrf_token'] = soup.find('input', {'name': 'csrf_token'})['value']
        response = self.session.post(login_url, self.credits)
        return response.url != login_url

    def get_submissions(self):
        user_submissions_url = 'https://cses.fi/problemset'
        response = self.session.get(user_submissions_url, verify=False, headers=self.headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = soup.find_all('ul', class_='task-list')
        account = 'https://cses.fi' + soup.find('a', class_='account').get('href')

        submissions_per_update = 100
        progress_count = 0
        end = get_accepted_submissions_count(account)

        for topic in topics:
            topic = fix_cascaded_html(topic)
            soup = BeautifulSoup(topic, 'html.parser')
            problems = soup.find_all('li', class_='task')

            for problem in problems:
                if check_problem_solved(problem):
                    progress_count += 1
                    self.print_progress_bar(progress_count, end)
                    if self.check_already_added(get_submission_id(problem)):
                        continue
                    submission = self.get_submission_html(problem)
                    self.push_code(submission)
                    self.update_already_added(submission)
                    if progress_count % submissions_per_update == 0:
                        self.update_submission_json()

    def push_code(self, submission):
        name = get_problem_name(submission)
        code = get_submission_code(submission)

        if code is not None:
            directory = self.generate_directory_link(submission)
            try:
                self.repo.create_file(directory, f"Add problem {name}", code)
            except:
                pass

    def update_already_added(self, submission):
        name = get_problem_name(submission)
        problem_link = get_problem_link(submission)
        directory_link = self.repo.html_url + '/blob/main/' + self.generate_directory_link(submission)
        language = get_submission_language(submission)
        tags = get_problem_tags(submission)
        date = get_submission_date(submission)

        self.current_submissions[str(name)] = {'id': str(name), 'name': name, 'problem_link': problem_link,
                                               'language': language, 'directory_link': directory_link,
                                               'tags': f'{tags}', 'date': date}

    def get_submission_html(self, problem):
        response = self.session.get('https://cses.fi' + problem.find('a').get('href'), verify=False, headers=self.headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        submission_link = soup.find('h4', string='Your submissions').find_next_sibling('a')
        while not submission_link.find('span', class_='task-score icon full'):
            submission_link = submission_link.find_next_sibling('a')
        else:
            submission_link = submission_link.find('span', class_='task-score icon full').parent.get('href')

        response = self.session.get('https://cses.fi' + submission_link, verify=False, headers=self.headers, timeout=20)
        return BeautifulSoup(response.text, 'html.parser')

    def generate_directory_link(self, submission):
        name = get_problem_name(submission)
        topic = get_problem_tags(submission)
        language = get_submission_language(submission)
        return f'{self.platform.upper()}/{topic}/{name}.{self.extensions[language]}'.replace(' ', '_')