from secpar.lib.Input.args import *
from secpar.lib.Commands.CommandFactory import *


def main():
    print("""
          _____                                
         / ___/ ___   _____ ____   ____ _ _____
         \__ \ / _ \ / ___// __ \ / __ `// ___/
        ___/ //  __// /__ / /_/ // /_/ // /    
       /____/ \___/ \___// .___/ \__,_//_/     
                        /_/    
      ==========================================        
        """)

    input_data = parse_args()
    command = CommandFactory(input_data).create()
    command.execute()

if __name__ == "__main__":
    main()