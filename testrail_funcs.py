import re
import requests
from GitHub.TestrailScripts import get_funcs


def check_testrail_for_bad_links_and_items():  # todo: work on this

    # test_cases = get_funcs.get_test_cases_from_project_id()
    test_cases = get_funcs.get_test_cases_from_suite_id(307)

    for test_case in test_cases:
        test_case_strings = []
        test_case_preconditions = test_case["custom_preconds"]
        if test_case_preconditions:
            test_case_strings.append(test_case_preconditions)

        for string in test_case_strings:
            check_string_for_bad_links(string)
            check_string_contains_the_word_nitro(string)
            # check_string_for_nitro_items()
            # check_string_for_missing_items()

        # todo: Add the rest of the strings
