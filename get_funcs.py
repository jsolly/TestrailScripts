import time
import re
from urllib.parse import urlparse
from GitHub.TestrailScripts.testrail import APIError
from other.my_secrets import MySecrets


TESTRAIL_DICT = MySecrets.TESTRAIL_DICT
TEST_RAIL_API_OBJ = MySecrets.get_test_rail_api_obj()
ADMIN_GIS_OBJS = MySecrets.get_admin_gis_objs()


TR_CLIENT_OBJ = MySecrets.get_test_rail_api_obj()


def get_test_case_from_id(test_case_id: int) -> list:
    for _ in range(5):  # Would be good to capsulize this logic
        try:
            test_case = TR_CLIENT_OBJ.send_get(uri=f"get_case/{test_case_id}")
            return test_case
        except APIError:
            print("I got throttled!")
            time.sleep(60)


def get_suites_from_project_id() -> list:
    suites = TR_CLIENT_OBJ.send_get(uri=f"get_suites/{TESTRAIL_DICT['TR_PROJECT_ID']}")
    return suites


def get_test_cases_from_project_id() -> list:
    cases = []
    suites = get_suites_from_project_id()
    for suite in suites:
        test_cases = get_test_cases_from_suite_id(suite["id"])
        cases += test_cases

    return cases


def get_test_cases_from_suite_id(suite_id: int) -> list:
    for _ in range(5):
        try:
            test_cases = TR_CLIENT_OBJ.send_get(
                uri=f"get_cases/{TESTRAIL_DICT['TR_PROJECT_ID']}&suite_id={suite_id}"
            )
            return test_cases
        except APIError:
            print("I got throttled!")
            time.sleep(60)
