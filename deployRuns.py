"""
***************************************************************************************************
import
***************************************************************************************************
"""

import src.globalDefinitions as globalDefinitions
import src.comparisonDetails as comparisonDetails
import src.helperFunctions as helperFunctions

"""
***************************************************************************************************
main
***************************************************************************************************
"""


def main():
    # print message
    print(globalDefinitions.WELCOME_MSG)
    # make object
    details = comparisonDetails.ComparisonDetails()
    # get configuration from jason
    configuration_file_path = helperFunctions.get_path_to_saved_profile()
    print(f"configuration_file_path = {configuration_file_path}")
    details.get_parameters(configuration_file_path)
    # perform run
    output_directory = helperFunctions.get_path_to_output_directory()
    print(f"output_directory = {output_directory}")
    details.run(output_directory)


"""
***************************************************************************************************
call main
***************************************************************************************************
"""

# this is better than simply defining main here because this avoids global variables
if __name__ == "__main__":
    main()
