from setuptools import setup, find_packages


setup(
    name="Secpar",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ['secpar = secpar.__main__:main']
    },
    python_requires='>=3.5',
    install_requires=[
        "PyGithub>=1.54.0",
        "requests>=2.0.0",
        "beautifulsoup4>=4.0.0",
        "argparse>=1.4.0",
        "stem>=1.8.0",
        "PySocks>=1.7.1,<2.0.0",
    ]
)