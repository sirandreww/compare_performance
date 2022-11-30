"""
***************************************************************************************************
File that has function that are used everywhere in the project
***************************************************************************************************
"""

import os
import src.globalDefinitions as globalDefinitions

"""
***************************************************************************************************
helper functions
***************************************************************************************************
"""


def _get_real_path_of_script() -> str:
    file_path = os.path.realpath(globalDefinitions.SCRIPT_NAME)
    return file_path


def _pop_path(path: str) -> str:
    split = path.split('/')
    split.pop()
    result = "/".join(split)
    return result


"""
***************************************************************************************************
API functions
***************************************************************************************************
"""


def get_path_to_saved_profile() -> str:
    main_py_path = _get_real_path_of_script()
    popped_path = _pop_path(main_py_path)
    pickle_file_path = f"{popped_path}/{globalDefinitions.CONFIG_FILE_NAME}"
    return pickle_file_path


def get_path_to_output_directory() -> str:
    main_py_path = _get_real_path_of_script()
    popped_path = _pop_path(main_py_path)
    pickle_file_path = f"{popped_path}/{globalDefinitions.OUTPUT_DIRECTORY_NAME}"
    return pickle_file_path


def get_all_file_paths_in_dir_recursively(rootdir: str):
    result = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            file_path = os.path.join(subdir, file)
            result += [file_path]
    return result


def change_directory(path: str):
    print(f"cd {path}")
    os.chdir(path)


def run_cmd(cmd: str):
    print(cmd)
    cmd_result = os.system(cmd)
    assert cmd_result == 0


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def read_file(path: str) -> str:
    with open(path) as f:
        lines = f.read()
        return lines
