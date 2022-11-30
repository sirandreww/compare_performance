"""
***************************************************************************************************
import
***************************************************************************************************
"""

import src.helperFunctions as helperFunctions
import json
import csv


"""
***************************************************************************************************
helper functions
***************************************************************************************************
"""


def get_file_paths():
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
    return out_files_1, out_files_2


def get_results_and_table(number_of_files):
    results = {
        "total number of tests": number_of_files,
        "number of tests that ran for both": 0,

        "rfv number of tests not run": 0,
        "abc number of tests not run": 0,

        "rfv number of finishes": 0,
        "abc number of finishes": 0,
        "both number of finishes": 0,
    }
    table = []
    return results, table


def get_result_from_output(text, word_that_indicated_safe, word_before_time):
    line = {
        "test ran": False,
        "test finished": False,
        "test result": None,
        "time": -1,
    }
    if len(text) != 0:
        line["test ran"] = True
        if text.count("CANCELLED") == 0:
            line["test finished"] = True
            line["test result"] = "safe" if text.count(word_that_indicated_safe) > 0 else "not safe"
            index = text.find(word_before_time) + len(word_before_time)
            list_of_words = text[index:].split(" ")
            list_of_word_filtered = []
            for w in list_of_words:
                if len(w) != 0:
                    list_of_word_filtered += [w]
            number = list_of_word_filtered[0].split("\n")[0]
            line["time"] = number
    return line


def one_if_true(condition):
    return 1 if condition else 0


def check_2_files(f1, f2, results, table):
    assert f1.split("/")[-1] == f2.split("/")[-1]
    f1_line = get_result_from_output(
        text=helperFunctions.read_file(f1),
        word_that_indicated_safe="Safe",
        word_before_time="Elapsed time = "
    )
    f2_line = get_result_from_output(
        text=helperFunctions.read_file(f2),
        word_that_indicated_safe="successful",
        word_before_time="Time = "
    )
    assert f1_line["test ran"]
    assert f2_line["test ran"]
    test_name = f1.split("/")[-1][:-8]
    table += [{
        'test_name': test_name,
        'abc_finished': f2_line["test finished"],
        'abc_result': f2_line["test result"],
        'abc_time': f2_line["time"],
        'rfv_finished': f1_line["test finished"],
        'rfv_result': f1_line["test result"],
        'rfv_time': f1_line["time"]
    }]
    results["rfv number of tests not run"] += (0 if f1_line["test ran"] else 1)
    results["abc number of tests not run"] += (0 if f2_line["test ran"] else 1)
    results["number of tests that ran for both"] += one_if_true(
        f1_line["test ran"] and f2_line["test ran"]
    )
    results["rfv number of finishes"] += one_if_true(f1_line["test finished"])
    results["abc number of finishes"] += one_if_true(f2_line["test finished"])
    both_finished = f1_line["test finished"] and f2_line["test finished"]
    results["both number of finishes"] += one_if_true(both_finished)
    if both_finished:
        assert f1_line["test result"] is not None
        assert f2_line["test result"] is not None
        assert f2_line["test result"] == f2_line["test result"]


def write_table_to_csv(table):
    # csv header
    fieldnames = ['test_name', 'abc_finished', 'abc_result', 'abc_time', 'rfv_finished', 'rfv_result', 'rfv_time']
    with open('results.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(table)


"""
***************************************************************************************************
main
***************************************************************************************************
"""


def main():
    out_files_1, out_files_2 = get_file_paths()
    results, table = get_results_and_table(
        number_of_files=len(out_files_1)
    )
    for f1, f2 in zip(out_files_1, out_files_2):
        check_2_files(
            f1=f1,
            f2=f2,
            results=results,
            table=table
        )
    print(json.dumps(table, sort_keys=False, indent=4))
    print(json.dumps(results, sort_keys=False, indent=4))
    write_table_to_csv(table=table)


"""
***************************************************************************************************
call main
***************************************************************************************************
"""

# this is better than simply defining main here because this avoids global variables
if __name__ == "__main__":
    main()
