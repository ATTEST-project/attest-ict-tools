import os, sys, getopt
import json
from shared_resources_planning import SharedResourcesPlanning


# ======================================================================================================================
#  Read Execution Arguments
# ======================================================================================================================
def print_help_message():
    print('\nShared Resources Planning Tool usage:')
    print('\n Usage: main_int.py [OPTIONS]')
    print('\n Options:')
    print('   {:25}  {}'.format('-j, --json_file=', 'launch config json file (declares the attributes: parameters.case_dir (absolute path) and parameters.specification_file)'))
    print('   {:25}  {}'.format('-h, --help', 'Help. Displays this message'))


def read_execution_arguments(argv):

    test_case_dir = str()
    spec_filename = str()

    try:
        opts, args = getopt.getopt(argv, 'hj:', ['help', 'json='])
    except getopt.GetoptError as e:
        print_help_message()
        print(str(e))
        sys.exit(2)

    if not argv or not opts:
        print_help_message()
        sys.exit()

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help_message()
            sys.exit()
        elif opt in ('-j', '--json'):
            jsonFile = open(arg)
            jsonParsed = json.load(jsonFile)
            parameters = jsonParsed['parameters']
            test_case_dir = parameters['case_dir']
            spec_filename = parameters['specification_file']

    if not test_case_dir or not spec_filename:
        print_help_message()
        sys.exit()

    return spec_filename, test_case_dir


# ======================================================================================================================
#  Shared Resources Planning
# ======================================================================================================================
def shared_resources_planning(working_directory, specification_filename):

    print('==========================================================================================================')
    print('                                     ATTEST -- SHARED RESOURCES PLANNING                                  ')
    print('==========================================================================================================')

    planning_problem = SharedResourcesPlanning(working_directory, specification_filename)
    planning_problem.read_planning_problem()
    planning_problem.run_planning_problem()

    print('==========================================================================================================')
    print('                                               END                                                        ')
    print('==========================================================================================================')


# ======================================================================================================================
#  Main
# ============================================================================cal==========================================
if __name__ == '__main__':

    filename, test_case_dir = read_execution_arguments(sys.argv[1:])
    print(filename)
    print(test_case_dir)
    shared_resources_planning( test_case_dir, filename)




