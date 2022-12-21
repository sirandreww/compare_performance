"""
***************************************************************************************************
File that has the object that actually performs the run
***************************************************************************************************
"""

import json
import random
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
    def _run_one_test_on_program_number(test_number, program_number, run_line, test_path,
                                        output_directory):
        current_run_line = run_line.replace(
            globalDefinitions.STRING_THAT_INDICATES_INPUT_FILE,
            f"\"{test_path}\""
        )
        output_file = test_path.split("/")[-1]
        name = f"program_{program_number}"
        job_name = ("rfv" if program_number == 1 else "abc") + str(test_number)
        cpus_per_task = 1
        time_in_minutes = 1
        number_of_tasks_per_node = 24
        command_to_send = f"sbatch --cpus-per-task={cpus_per_task} --ntasks-per-node={number_of_tasks_per_node} --time={time_in_minutes} -J {job_name} --output=\"{output_directory}/{name}/{output_file}.out.txt\"  --wrap='time {current_run_line}' "
        helperFunctions.run_cmd(command_to_send)

    def _run_tests_on_program_number(self, program_number, test_paths, output_directory):
        program = f"program {program_number}"
        source_path = self.configuration[program]["source path"]
        compilation_line = self.configuration[program]["compilation line"]
        run_line: str = self.configuration[program]["run line"]
        helperFunctions.change_directory(source_path)
        helperFunctions.run_cmd(compilation_line)
        for test_number, test_path in enumerate(test_paths):
            self._run_one_test_on_program_number(
                test_number=test_number + 1,
                program_number=program_number,
                run_line=run_line,
                test_path=test_path,
                output_directory=output_directory
            )

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
        filtered_inputs = helperFunctions.get_all_file_paths_in_dir_that_have_desired_ending(
            rootdir=self.configuration["test files path"],
            desired_ending=self.configuration["ending of desired files"]
        )
        random.shuffle(filtered_inputs)

        # do each program alone
        for i in range(1, 3):
            self._run_tests_on_program_number(
                program_number=i,
                test_paths=filtered_inputs,
                output_directory=output_directory
            )
