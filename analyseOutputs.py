"""
***************************************************************************************************
import
***************************************************************************************************
"""

import src.helperFunctions as helperFunctions
import json

"""
***************************************************************************************************
main
***************************************************************************************************
"""


def main():
    output_directory = helperFunctions.get_path_to_output_directory()
    print(f"output_directory = {output_directory}")
    out_files_1 = helperFunctions.get_all_file_paths_in_dir_that_have_desired_ending(
        rootdir=f"{output_directory}/program_1",
        desired_ending=".out.txt"
    )
    out_files_2 = helperFunctions.get_all_file_paths_in_dir_that_have_desired_ending(
        rootdir=f"{output_directory}/program_2",
        desired_ending=".out.txt"
    )
    assert len(out_files_1) == len(out_files_2)
    out_files_1.sort()
    out_files_2.sort()
    results = {
        "total number of tests": len(out_files_1),
        "rfv number of files not run": 0,
        "rfv number of files that ran fully": 0,
        "abc number of files not run": 0,
        "abc number of files that ran fully": 0,
        "number of tests that ran for both": 0,
    }
    for f1, f2 in zip(out_files_1, out_files_2):
        assert f1.split("/")[-1] == f2.split("/")[-1]
        f1_text = helperFunctions.read_file(f1)
        f2_text = helperFunctions.read_file(f2)
        is_f1_empty = len(f1_text) == 0
        is_f2_empty = len(f2_text) == 0
        results["rfv number of files not run"] += (1 if is_f1_empty else 0)
        results["abc number of files not run"] += (1 if is_f2_empty else 0)
        if is_f1_empty or is_f2_empty:
            continue
        results["number of tests that ran for both"] += 1
        was_f1_canceled = f1_text.count("CANCELLED") > 0
        was_f2_canceled = f2_text.count("CANCELLED") > 0
        results["rfv number of files that ran fully"] += (0 if was_f1_canceled else 1)
        results["abc number of files that ran fully"] += (0 if was_f2_canceled else 1)
        if was_f1_canceled or was_f2_canceled:
            continue

        is_f1_safe = f1_text.count("Safe") > 0
        is_f2_safe = f2_text.count("successful") > 0
        assert is_f1_safe == is_f2_safe
    print(json.dumps(results, sort_keys=True, indent=4))


"""
***************************************************************************************************
call main
***************************************************************************************************
"""

# this is better than simply defining main here because this avoids global variables
if __name__ == "__main__":
    main()
