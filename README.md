# Scraping Engine for Competitive Programming Accelerated Retriever (Secpar)
[![PyPI](https://img.shields.io/pypi/v/Secpar.svg)](https://pypi.python.org/pypi/Secpar)
[![Downloads](https://pepy.tech/badge/Secpar)](https://pepy.tech/project/Secpar)
[![PyPI](https://img.shields.io/pypi/l/Secpar.svg)](https://github.com/MostafaGalal1/Secpar/blob/main/LICENSE)


## Overview

Secpar is a Python command-line tool designed to scrape code submissions from various online programming platforms and store them in a GitHub repository. It supports platforms such as Codeforces, CSES (University of Helsinki), and Vjudge. This documentation provides a detailed overview of the Scraper's functionalities and how to use them.

#### Demo Repo: [CP-Submissions](https://github.com/MostafaGalal1/CP-Submissions)

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
    - [Initialization](#initialization)
    - [Scraping](#scraping)
4. [Command-Line Interface](#command-line-interface)
5. [Scraper Configuration](#scraper-configuration)
6. [Customization](#customization)
7. [Data Storage](#data-storage)
8. [FAQs](#faqs)
9. [Contributing](#contributing)
10. [License](#license)
11. [Upcoming Features](#upcoming-features) 

## 1. Features <a name="features"></a>

- **Supported Platforms**: Secpar supports the following programming platforms:
  - Codeforces
  - CSES (University of Helsinki)
  - Vjudge

- **GitHub Integration**: Code submissions are stored in a GitHub repository, making it easy to manage and share your solutions.

- **Automatic README Generation**: Secpar automatically generates a README file for your GitHub repository, listing all your code submissions with problem details, links, and tags.

- **Incremental Scraping**: Secpar keeps track of previously scraped submissions, ensuring that only new submissions are added to your repository.
  
- **Multi-accounts Scraping**: Scrape the same platform more than once in case of having multiple accounts on that platform without worry of redundancy.

- **Authentication**: Securely authenticate with the supported platforms to access your submissions.

- **Customization**: Customize the formatting of your README and configure other scraper options.

## 2. Installation <a name="installation"></a>

To use Secpar, follow these installation steps:

**Install Secpar**: Install Secpar package on your local machine:

```shell
pip install Secpar
```

## 3. Usage <a name="usage"></a>

Secpar has two primary modes of operation: initialization and scraping.

### Initialization <a name="initialization"></a>

Initialization is the first step to configure your scraper for a GitHub repository.

1. Run the initialization command:

    ```shell
    python secpar -c init
    ```

2. Follow the prompts to enter your GitHub username, repository name, and access token.

### Scraping <a name="scraping"></a>

Scraping allows you to retrieve code submissions from supported platforms and store them in your GitHub repository.

1. To scrape submissions, use the following command:

    ```shell
    secpar -s PLATFORM_NAME
    ```

    Replace `PLATFORM_NAME` with one of the supported platforms: `codeforces`, `cses`, or `vjudge`.

2. Depending on the platform, you may need to provide additional information such as your platform password.

3. Secpar will fetch new submissions and update your GitHub repository.

### Note:
To upload submissions codes for codeforces you need to have `Tor` installed and inside your torrc file place these two line:

```shell
SocksPort 9050
ControlPort 9051
```

Open tor tab and make sure you can browse using it and keep it open till you scrape using the terminal.

## 4. Command-Line Interface <a name="command-line-interface"></a>

Secpar provides a command-line interface with the following options:

- `-c`, `--command`: Specify the command (`init` for initialization or `update` for scraping).

- `-s`, `--scrape`: Specify the platform to scrape data from (`codeforces`, `cses`, or `vjudge`).

- `-h`, `--help`: Display usage instructions and available options.

Example usage:

```shell
python secpar -c init
python secpar -s codeforces
```

## 5. Scraper Configuration <a name="scraper-configuration"></a>

Secpar can be configured in several ways:

- **GitHub Configuration**: Set up your GitHub repository details and access token during initialization.

- **Platform Authentication**: Authenticate with your platform credentials (e.g., Codeforces username and password) for scraping.

- **Customization**: Customize the formatting of your README and configure scraper options in the code (e.g., maximum requests, submission per update).

## 6. Customization <a name="customization"></a>

You can customize Secpar's behavior by modifying the source code. Here are some customization options:

- **Formatting**: Customize the formatting of the generated README for each platform. You can modify the formatting in the corresponding `Formatter` class.

- **Configuration**: Adjust Secpar's settings, such as maximum requests, submissions per update, or other platform-specific parameters.

## 7. Data Storage <a name="data-storage"></a>

Secpar stores code submissions and related information in your GitHub repository. Each submission is listed in the README with details such as problem name, language, solution link, tags, and submission date.

## 8. FAQs <a name="faqs"></a>

- **What platforms does Secpar support?**
  - Secpar currently supports Codeforces, CSES (University of Helsinki), and Vjudge.

- **Is it safe to store my GitHub access token?**
  - Access tokens should be stored securely. Secpar stores them in a configuration file, and it's essential to protect this file.

- **How can I customize the README format?**
  - You can customize the README format by modifying the corresponding `Formatter` class for each platform.

## 9. Contributing <a name="contributing"></a>

Contributions to Secpar are welcome! Feel free to fork the repository, make improvements, and create pull requests.

## 10. License <a name="license"></a>

Secpar is released under the MIT License. See the [LICENSE](https://github.com/MostafaGalal1/Secpar/blob/main/LICENSE) file for details.

## 11. Upcoming Features <a name="upcoming-features">
- More platforms: platforms such as Atcoder and CodeChef are currently being worked on.

---

*Note: This documentation provides an overview of Secpar's functionality and usage. For detailed code explanations, refer to the source code and comments in Secpar's repository.*
