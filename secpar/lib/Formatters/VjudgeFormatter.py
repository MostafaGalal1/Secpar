from .AbstractFormatter import AbstractFormatter


class VjudgeFormatter(AbstractFormatter):

    def format(self):
        readme_content = self.get_header()
        for submission in self.data["Submissions"]:
            problem_count = submission.get("count")
            name = submission.get("name")
            problem_link = submission.get("problem_link")
            language = submission.get("language")
            solution_link = submission.get("directory_link")
            date = submission.get("date")
            readme_content += f'{problem_count} | [{name}]({problem_link}) | [{language}]({solution_link}) | {date} |\n'
        readme_content += '\n'
        return readme_content