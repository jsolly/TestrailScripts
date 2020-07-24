import unittest
from GitHub.TestrailScripts import get_funcs
from GitHub.HelperScripts import check_funcs
from other.my_secrets import MySecrets
import logging

TESTRAIL_DICT = MySecrets.TESTRAIL_DICT
PROJECT_ID = TESTRAIL_DICT["4X_DASHBOARD_PROJECT_ID"]
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # stream_handler will use this level

# formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("TestRail_Cleanup_results.log")
# file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

ALL_GIS_OBJS = MySecrets.get_all_admin_gis_objs()
NITRO_GIS_OBJS = MySecrets.get_nitro_admin_gis_objs()


class TestRailClass(unittest.TestCase):
    @staticmethod
    def log_string_checks(string, obj_id, obj_type):
        bad_links = check_funcs.check_string_for_bad_links(string)
        if bad_links:
            logger.debug(f"{obj_type}, {obj_id}, {bad_links}")

        test_cases_with_nitro = check_funcs.check_string_contains_substring(
            string, "nitro"
        )

        if test_cases_with_nitro:
            logger.debug(f"{obj_type},{obj_id},contains the string nitro")

        missing_items = check_funcs.check_string_for_missing_items(string, ALL_GIS_OBJS)
        if missing_items:
            logger.debug(f"{obj_type},{obj_id},missing items, {missing_items}")

        nitro_items = check_funcs.check_string_for_items_in_orgs(
            string,
            NITRO_GIS_OBJS,  # Dev, QA, PROD
            [
                "a910db6b36ff4066a3d4131fccc3da9b",
                "7193ed6f5fbb4306b80cb9d540349645",
                "N4jtru9dctSQR53c",
            ],
        )

        if nitro_items:
            logger.debug(f"{obj_type},{obj_id},nitro items, {nitro_items}")

    def test_test_cases_for_bad_links_and_items(self, test_cases):
        for test_case in test_cases:
            print(f"Now working on test case id: {test_case['id']}")
            try:
                big_string = ""
                test_case_deep = get_funcs.get_test_case_from_id(test_case["id"])

                if test_case_deep["custom_preconds"]:
                    big_string += " " + test_case_deep["custom_preconds"]

                if test_case_deep["custom_steps"]:
                    big_string += " " + test_case_deep["custom_steps"]

                if test_case_deep["custom_expected"]:
                    big_string += " " + test_case_deep["custom_expected"]

                if test_case_deep["custom_steps_separated"]:
                    for step in test_case_deep["custom_steps_separated"]:
                        if step["content"]:
                            big_string += " " + step["content"]

                        if step["expected"]:
                            big_string += " " + step["expected"]

                if big_string:
                    self.log_string_checks(big_string, test_case["id"], "Test case")
            except KeyError:
                pass

    def test_testrail(self):

        test_cases = get_funcs.get_test_cases_from_project_id(PROJECT_ID)
        # test_cases = get_funcs.get_test_cases_from_suite_id(PROJECT_ID, 1766)
        self.test_test_cases_for_bad_links_and_items(test_cases)

        suites = get_funcs.get_suites_from_project_id(PROJECT_ID)
        suite_sections = [
            get_funcs.get_sections_from_suite_id(PROJECT_ID, suite["id"])
            for suite in suites
        ]
        for suite in suite_sections:
            big_string = ""
            for section in suite:
                if section["description"]:
                    big_string += " " + section["description"]

            self.log_string_checks(big_string, section["suite_id"], "suite")

    def test_test_case(self):
        test_cases = [get_funcs.get_test_case_from_id(206593)]
        self.test_test_cases_for_bad_links_and_items(test_cases)


# 206506 VPN
