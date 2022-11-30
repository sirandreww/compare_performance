"""
***************************************************************************************************
import
***************************************************************************************************
"""

import src.helperFunctions as helperFunctions

"""
***************************************************************************************************
main
***************************************************************************************************
"""


def main():
    output_directory = helperFunctions.get_path_to_output_directory()
    print(f"output_directory = {output_directory}")
    out_files_1 = helperFunctions.get_all_file_paths_in_dir_recursively(
        f"{output_directory}/program_1"
    )
    out_files_2 = helperFunctions.get_all_file_paths_in_dir_recursively(
        f"{output_directory}/program_2"
    )
    assert len(out_files_1) == len(out_files_2)
    out_files_1.sort()
    out_files_2.sort()
    for f1, f2 in zip(out_files_1, out_files_2):
        f1_text = helperFunctions.read_file(f1)
        f2_text = helperFunctions.read_file(f2)
        is_f1_safe = f1_text.count("safe") == 1
        is_f2_safe = f2_text.count("safe") == 1





"""
***************************************************************************************************
call main
***************************************************************************************************
"""

# this is better than simply defining main here because this avoids global variables
if __name__ == "__main__":
    main()
