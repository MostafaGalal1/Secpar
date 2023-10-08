from .AbstractFormatter import AbstractFormatter


class CsesFormatter(AbstractFormatter):

    def format(self):
        if self.data is None: return ""
        readme_content = self.get_header()
        count = len(self.data["Submissions"])
        for submission in self.data["Submissions"]:
            name = submission.get("name")
            problem_link = submission.get("problem_link")
            language = submission.get("language")
            solution_link = submission.get("directory_link")
            tags = submission.get("tags")
            date = submission.get("date")
            readme_content += f'{count} | [{name}]({problem_link}) | [{language}]({solution_link}) | {tags} | {date} |\n'
            count -= 1
        readme_content += '\n'
        return readme_content