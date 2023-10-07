from github import Github


from ..Formatters.CodeforcesFormatter import CodeforcesFormatter
from ..Formatters.CsesFormatter import CsesFormatter
from ..Formatters.VjudgeFormatter import VjudgeFormatter


class ReadMeBuilder():
    def __init__(self, data):
        self.platforms = data.get("platforms")
        git = Github(data.get("access_token"))
        self.repo = git.get_user(data.get("repo_owner")).get_repo(data.get("repo_name"))

    def get_formmater(self, name):
        if name == "cses":
            return CsesFormatter(self.repo)
        elif name == "codeforces":
            return CodeforcesFormatter(self.repo)
        elif name == "vjudge":
            return VjudgeFormatter(self.repo)

    def update_readme(self, readme_content):
        readme_path = 'README.md'
        try:
            # If the README exists, update it
            existing_readme = self.repo.get_contents(readme_path)
            self.repo.update_file(readme_path,"Update README.md",readme_content,existing_readme.sha)
            print("README.md updated.")
        except Exception as e:
            # If the README doesn't exist, create it
            self.repo.create_file(readme_path,"Create README.md",readme_content,)
            print("README.md created.")

    def build(self):
        readme_content = ""
        for platform in self.platforms:
            readme_content += self.get_formmater(platform).format()
        return readme_content
