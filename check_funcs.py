import re
import requests
from GitHub.TestrailScripts import get_funcs
from other.my_secrets import AGOL_DICT


def check_testrail_for_bad_links_and_items():
    dirty_test_cases = {}

    test_cases = get_funcs.get_test_cases_from_project_id()
    # test_cases = get_funcs.get_test_cases_from_suite_id("307")

    for test_case in test_cases:
        dirty_results = []
        test_case_preconditions = test_case["custom_preconds"]

        if not test_case_preconditions:
            continue

        if check_string_for_nitro_string(test_case_preconditions):
            dirty_results.append("This test case contains the word 'nitro")

        test_case_links = get_funcs.get_links_from_string(test_case_preconditions)
        if test_case_links:
            for link in test_case_links:
                response = get_human_readable_response(link)
                if response != 200:
                    dirty_results.append(response)

        test_case_item_ids = get_funcs.get_item_ids_from_string(test_case_preconditions)
        if test_case_item_ids:
            for item_id in test_case_item_ids:
                item = get_funcs.get_item_from_item_id(item_id)
                if not item:
                    dirty_results.append(f"{item_id} this item is inaccessible")
                    continue

                elif (
                    get_funcs.get_item_host_name(item)
                    == AGOL_DICT["AGOL_NITRO_DEVEXT_HOST_NAME"]
                ):
                    dirty_results.append(f"{item_id} is a nitro item id")

        if dirty_results:
            dirty_test_cases[test_case["id"]] = dirty_results

    with open("broken_test_cases.txt", "w") as writer:
        for test_case, error_list in dirty_test_cases.items():
            writer.write(f"#### {test_case}")
            writer.write("\n")
            for error in error_list:
                writer.write(error)
                writer.write("\n")
            writer.write("\n")

    return dirty_test_cases


def check_string_for_nitro_string(string) -> bool:
    nitro_pattern = re.compile("nitro", re.IGNORECASE)

    if nitro_pattern.search(string):
        return True

    return False


def get_human_readable_response(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return 200

        elif response.status_code == 404:
            return f"Server responded that {url} could not be found"

        elif response.status_code == 400:
            return f"Server responded that {url} was not formatted correctly"

        elif response.status_code == 401:
            return f"Server needed authentication to access {url}"

        elif response.status_code == 403:
            return f"Server rejected request to access {url}"

        else:
            print(response)

    except requests.exceptions.SSLError:
        return 200  # This is bad, but I want to ignore it.

    except requests.exceptions.ConnectionError:
        return f"Server could not be found when attempting to access {url}"
