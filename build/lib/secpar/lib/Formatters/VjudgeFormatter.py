# Import the base class 'AbstractFormatter'.
from secpar.lib.Formatters.AbstractFormatter import AbstractFormatter

# Define a concrete formatter class 'VjudgeFormatter' that inherits from 'AbstractFormatter'.
class VjudgeFormatter(AbstractFormatter):

    def format(self):
        # Check if there is no data; return an empty string.
        if self.data is None:
            return ""

        # Initialize the readme content with the header.
        readme_content = self.get_header()

        # Initialize a count for numbering submissions.
        count = len(self.data.get("Submissions"))

        # Iterate over each submission in the data.
        for submission in self.data.get("Submissions"):
            name = submission.get("name")
            problem_link = submission.get("problem_link")
            language = submission.get("language")
            solution_link = submission.get("directory_link")
            date = submission.get("date")

            # Append formatted submission information to the readme content.
            readme_content += f'{count} | [{name}]({problem_link}) | [{language}]({solution_link}) | {date} |\n'
            count -= 1  # Decrement the count.

        readme_content += '\n'  # Add a newline at the end.
        return readme_content  # Return the formatted readme content.

# End of the 'VjudgeFormatter' class definition.
