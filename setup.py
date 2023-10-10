from setuptools import setup, find_packages
import codecs
import os

# Get the current directory
here = os.path.abspath(os.path.dirname(__file__))

# Read the README file as long description
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '1.1.0'
DESCRIPTION = 'Scrape problems submissions from different platforms'

# Define the authors
author_name_1 = 'Mostafa Galal'
author_email_1 = 'mostafam.galal82@gmail.com'
author_name_2 = 'Mahmoud Goda'
author_email_2 = 'mahmoden17@gmail.com'

# Combine author information
authors = f"{author_name_1} <{author_email_1}>, {author_name_2} <{author_email_2}>"

# Setting up
setup(
    name="Secpar",
    version=VERSION,
    author=authors,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    package_data={'secpar': ['*.json', '*.py']},
    include_package_data=True,
    license="MIT",
    entry_points={
        "console_scripts": ['secpar = secpar.__main__:main']
    },
    url="https://github.com/MostafaGalal1/Secpar",
    python_requires='>=3.5',
    install_requires=[
        "PyGithub>=1.54.0",
        "requests>=2.0.0",
        "beautifulsoup4>=4.0.0",
        "stem>=1.8.0",
        "PySocks>=1.7.1,<2.0.0",
        "argparse>=1.4.0",
    ],
    keywords=['CP', 'scraper', 'secpar', 'problem solving', 'python', 'tools'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
