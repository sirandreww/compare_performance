"""
***************************************************************************************************
File that has the object that actually performs the run
***************************************************************************************************
"""

import json
import src.helperFunctions as helperFunctions
import src.globalDefinitions as globalDefinitions

"""
***************************************************************************************************
import
***************************************************************************************************
"""


class ComparisonDetails:
    """
    ***********************************************************************************************
    class that manages the runs
    ***********************************************************************************************
    """

    """
    ***********************************************************************************************
    helper functions
    ***********************************************************************************************
    """

    def _load_parameters(self, config_file_path):
        with open(config_file_path, 'rb') as handle:
            self.configuration = json.load(handle)

    @staticmethod
    def _run_one_test_on_program_number(program_number, run_line, test_path, output_directory):
        current_run_line = run_line.replace(
            globalDefinitions.STRING_THAT_INDICATES_INPUT_FILE,
            test_path
        )
        output_file = test_path.split("/")[-1]
        name = f"program_{program_number}"
        command_to_send = f"{current_run_line} > \"{output_directory}/{name}/{output_file}.out.txt\""
        helperFunctions.run_cmd(command_to_send)

    def _run_tests_on_program_number(self, program_number, test_paths, output_directory):
        program = f"program {program_number}"
        source_path = self.configuration[program]["source path"]
        compilation_line = self.configuration[program]["compilation line"]
        run_line: str = self.configuration[program]["run line"]
        helperFunctions.change_directory(source_path)
        helperFunctions.run_cmd(compilation_line)
        for test_path in test_paths:
            self._run_one_test_on_program_number(
                program_number=program_number,
                run_line=run_line,
                test_path=test_path,
                output_directory=output_directory
            )

    @staticmethod
    def filter_list_of_string_by_ending(list_of_strings, desired_ending):
        filtered = []
        for f in list_of_strings:
            if f[-len(desired_ending):] == desired_ending:
                filtered += [f]
        return filtered

    """
    ***********************************************************************************************
    api functions
    ***********************************************************************************************
    """

    def __init__(self):
        self.configuration = {}

    def get_parameters(self, config_file_path):
        if helperFunctions.is_file(config_file_path):
            print(f"Loading profile because we found this file:\n{config_file_path}")
            self._load_parameters(config_file_path)
        else:
            raise Exception(f"No profile found at '{config_file_path}'")
        print("Done loading run information.")

    def run(self, output_directory):
        # get test parameters
        files_in_test_directory = helperFunctions.get_all_file_paths_in_dir_recursively(
            rootdir=self.configuration["test files path"]
        )
        ending_of_desired_files = self.configuration["ending of desired files"]
        filtered_inputs = self.filter_list_of_string_by_ending(
            list_of_strings=files_in_test_directory,
            desired_ending=ending_of_desired_files
        )

        # do each program alone
        for i in range(1, 3):
            self._run_tests_on_program_number(
                program_number=i,
                test_paths=filtered_inputs,
                output_directory=output_directory
            )