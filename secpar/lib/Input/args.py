import argparse

def parse_args():
    # Create an ArgumentParser instance with a description and an epilog for usage examples.
    parser = argparse.ArgumentParser(
        description="Creates a repository of all the submissions from a given platform",
        epilog="Example usage: `secpar -c init`"
    )

    # Create argument groups for commands and platforms.
    command_group = parser.add_argument_group('Commands', 'Commands to initialize')
    platform_group = parser.add_argument_group('Platforms', 'Platforms to scrape data from')

    # Add arguments for the "command" option (-c or --command).
    command_group.add_argument(
        "-c",
        "--command",
        choices=["init"],  # Specify valid choices for the "command" argument.
        type=str,
        help="Choose a command: init"
    )

    # Add arguments for the "scrap" option (-s or --scrap).
    platform_group.add_argument(
        "-s",
        "--scrap",
        choices=["codeforces", "cses", "vjudge"],  # Specify valid choices for the "scrap" argument.
        type=str,
        help="Specify the platform name (codeforces, cses, or vjudge)"
    )

    # Parse the command-line arguments.
    args = parser.parse_args()

    # Check if both "scrap" and "command" options are provided, which is invalid.
    if args.scrap and args.command:
        parser.error("The --scrap option should be used alone, without specifying --command.")

    return args  # Return the parsed arguments.

# End of the 'parse_args' function.
