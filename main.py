"""
***************************************************************************************************
import
***************************************************************************************************
"""

import os
import json

"""
***************************************************************************************************
globals
***************************************************************************************************
"""

WELCOME_MSG: str = """
*************************************************
Thank you for using this tool.
The tool creates 2 executables and races them on
multiple tests to get an image of performance.
Author: Andrew Luka
*************************************************
"""
SCRIPT_NAME: str = __file__
CONFIG_FILE_NAME = "configuration.txt"


"""
***************************************************************************************************
Comparison details
***************************************************************************************************
"""


class ComparisonDetails:
    def __init__(self):
        self.configuration = {}

    def load_parameters(self):
        with open(get_path_to_saved_profile(), 'rb') as handle:
            self.configuration = json.load(handle)

    def get_parameters(self):
        config_file_path = get_path_to_saved_profile()
        if os.path.isfile(config_file_path):
            print(f"Loading profile because we found this file:\n{config_file_path}")
            self.load_parameters()
        else:
            raise Exception(f"No profile found at '{config_file_path}'")
        print("Done loading run information.")

    def run(self):
        print(self.configuration)


"""
***************************************************************************************************
helper functions
***************************************************************************************************
"""


def get_path_to_saved_profile() -> str:
    def get_real_path_of_script() -> str:
        file_path = os.path.realpath(SCRIPT_NAME)
        return file_path

    def pop_path(path: str) -> str:
        split = path.split('/')
        split.pop()
        result = "/".join(split)
        return result
    main_py_path = get_real_path_of_script()
    popped_path = pop_path(main_py_path)
    pickle_file_path = f"{popped_path}/{CONFIG_FILE_NAME}"
    return pickle_file_path


"""
***************************************************************************************************
main
***************************************************************************************************
"""


def main():
    print(WELCOME_MSG)
    details = ComparisonDetails()
    details.get_parameters()
    details.run()


"""
***************************************************************************************************
call main
***************************************************************************************************
"""

# this is better than simply defining main here because this avoids global variables
if __name__ == "__main__":
    main()
