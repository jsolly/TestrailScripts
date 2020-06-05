import re
import requests
from GitHub.TestrailScripts import get_funcs


def check_string_for_bad_links(string):
    test_case_links = get_funcs.get_links_from_string(string)
    for link in test_case_links:
        check_is_url_reachable(link)


def check_string_contains_the_word_nitro(string) -> bool:
    nitro_pattern = re.compile("nitro", re.IGNORECASE)

    if nitro_pattern.search(string):
        return True

    return False


def check_is_url_reachable(url):
    try:
        response = requests.get(url, timeout=3)
        if response.ok:
            return True, response.status_code

        else:
            return False, response.status_code

    except requests.exceptions.SSLError:
        return True, "There was an SSLError"

    except requests.exceptions.ConnectionError:
        return False, f"Server could not be found when attempting to access {url}"

    except requests.exceptions.ReadTimeout:
        return False, f"I timed out when attempting to access {url}"


def check_string_for_nitro_items(string) -> list:
    item_ids = get_funcs.get_item_ids_from_string(string)
    try:
        items = []
        for item_id in item_ids:
            items.append(get_funcs.get_item_from_item_id(item_id))

        items = [get_funcs.get_item_from_item_id(item_id) for item_id in item_ids]
        nitro_items = [item for item in items if item.org == "nitro"]
        return nitro_items
    except Exception as e:
        print(e)


def check_string_for_missing_items(string):
    item_ids = get_funcs.get_item_ids_from_string(string)
    try:
        missing_item_ids = [
            item_id
            for item_id in item_ids
            if not get_funcs.get_item_from_item_id(item_id)
        ]

        return missing_item_ids

    except Exception as e:
        print(e)


def check_testrail_for_bad_links_and_items():

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
