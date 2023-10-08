from .AbstractFormatter import AbstractFormatter


class VjudgeFormatter(AbstractFormatter):

    def format(self):
        if self.data is None : return ""
        readme_content = self.get_header()
        count = len(self.data.get("Submissions"))
        for submission in self.data.get("Submissions"):
            name = submission.get("name")
            problem_link = submission.get("problem_link")
            language = submission.get("language")
            solution_link = submission.get("directory_link")
            date = submission.get("date")
            readme_content += f'{count} | [{name}]({problem_link}) | [{language}]({solution_link}) | {date} |\n'
            count -= 1
        readme_content += '\n'
        return readme_content