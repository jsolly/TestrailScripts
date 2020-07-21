import time
from GitHub.TestrailScripts.testrail import APIError
from other.my_secrets import MySecrets
import binpacking
from GitHub.TestrailScripts import testrail


TESTRAIL_DICT = MySecrets.TESTRAIL_DICT
TEST_RAIL_API_OBJ = testrail.APIClient(
    base_url="https://" + MySecrets.TESTRAIL_DICT["BASE_URL"]
)
TEST_RAIL_API_OBJ.user = MySecrets.TESTRAIL_DICT["USERNAME"]
TEST_RAIL_API_OBJ.password = MySecrets.TESTRAIL_DICT["PASSWORD"]


def get_sections_from_suite_id(project_id, suite_id: int) -> list:
    sections = TEST_RAIL_API_OBJ.send_get(
        uri=f"get_sections/{project_id}&suite_id={suite_id}"
    )
    return sections


def get_certification_assignments(suite_dict, bin_num):
    total_test_cases = sum(suite_dict.values())
    bins = binpacking.to_constant_bin_number(suite_dict, bin_num)

    print(f"There are a total of {total_test_cases} test cases")
    for index, employee in enumerate(bins):
        print(f"\n Bucket {index} has {sum(employee.values())} tests")
        print(employee)

    return True


def get_test_case_from_id(test_case_id: int) -> list:
    for _ in range(5):  # Would be good to capsulize this logic
        try:
            test_case = TEST_RAIL_API_OBJ.send_get(uri=f"get_case/{test_case_id}")
            return test_case
        except APIError as e:
            if "Rate Limit" in e.args[0]:
                print(e)
                time.sleep(60)

        except ConnectionError as e:
            if "Max retries" in e.args[0]:
                print(e)
                time.sleep(60)

        except Exception as e:
            raise Exception(f"I've never seen this error, {e} before")


def get_suites_from_project_id(project_id) -> list:
    return TEST_RAIL_API_OBJ.send_get(uri=f"get_suites/{project_id}")


def get_test_cases_from_project_id(project_id) -> list:
    cases = []
    suites = get_suites_from_project_id(project_id)
    for suite in suites:
        test_cases = get_test_cases_from_suite_id(project_id, suite["id"])
        cases += test_cases

    return cases


def get_test_cases_from_suite_id(project_id, suite_id: int) -> list:
    for _ in range(5):
        try:
            test_cases = TEST_RAIL_API_OBJ.send_get(
                uri=f"get_cases/{project_id}&suite_id={suite_id}"
            )
            return test_cases
        except APIError as e:
            if "Rate Limit" in e.args[0]:
                print(e)
                time.sleep(60)

            else:
                raise Exception(f"I've never seen this error, {e} before")
