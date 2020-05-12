import time
import re
from urllib.parse import urlparse
from GitHub.TestrailScripts.testrail import APIError
from other import my_secrets as secrets


def get_suites_from_project_id() -> list:
    suites = secrets.TR_CLIENT_OBJ.send_get(uri=f"get_suites/{secrets.TR_PROJECT_ID}")
    return suites


def get_test_cases_from_project_id() -> list:
    cases = []
    suites = get_suites_from_project_id()
    for suite in suites:
        test_cases = get_test_cases_from_suite_id(suite["id"])
        cases += test_cases

    return cases


def get_test_cases_from_suite_id(suite_id):
    for _ in range(5):
        try:
            test_cases = secrets.TR_CLIENT_OBJ.send_get(
                uri=f"get_cases/{secrets.TR_PROJECT_ID}&suite_id={suite_id}"
            )
            return test_cases
        except APIError:
            print("I got throttled!")
            time.sleep(60)


def get_test_case_from_id(test_case_id):
    for _ in range(5):  # Would be good to capsulize this logic
        try:
            test_case = secrets.TR_CLIENT_OBJ.send_get(uri=f"get_case/{test_case_id}")
            return test_case
        except APIError:
            print("I got throttled!")
            time.sleep(60)


def get_links_from_string(string):  # Change to match other ragexes
    url_pattern = re.compile(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    urls = url_pattern.findall(string)
    return urls


def get_item_ids_from_string(string):
    item_id_pattern = re.compile("[0-9a-f]{32}")
    item_ids = item_id_pattern.findall(string)
    return item_ids


def get_item_from_item_id(item_id):
    for GIS in secrets.AGOL_DBQA_ADMINS:
        item = GIS.content.get(item_id)
        if item:
            return item

    return False


def get_item_host_name(item_obj):
    item_url = item_obj.homepage
    host_name = urlparse(item_url).hostname
    return host_name
