from .lib.Input.args import *
from .lib.Commands.CommandFactory import *

if __name__ == "__main__":
    print("""
         __  __                              __
        / / / /___ _______      _____  _____/ /_
       / /_/ / __ `/ ___/ | /| / / _ \/ ___/ __/
      / __  / /_/ / /   | |/ |/ /  __(__  ) /_
     /_/ /_/\__,_/_/    |__/|__/\___/____/\__/

     ==========================================
     """)
    input_data = parse_args()
    command = CommandFactory(input_data).create()
    command.execute()