import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Creates a repository of all the submissions from a given platform",
        epilog="Example usage: `CP_Scraper -c init`"
    )

    command_group = parser.add_argument_group('Commands', 'Commands to initialize or update the repository')
    command_group.add_argument(
        "-c",
        "--command",
        choices=["init", "update"],
        type=str,
        help="Choose a command: init or update"
    )

    platform_group = parser.add_argument_group('Platforms', 'Platforms to scrape data from')
    platform_group.add_argument(
        "-s",
        "--scrap",
        choices=["codeforces", "cses"],
        type=str,
        help="Specify the platform name (codeforces or cses)"
    )

    args = parser.parse_args()

    # If both --platform and --command are provided, it's invalid
    if args.scrap and args.command:
        parser.error("The --scrap should be used alone, without specifying --command.")

    return args