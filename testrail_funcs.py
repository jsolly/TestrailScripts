import unittest
from GitHub.TestrailScripts import get_funcs
from GitHub.HelperScripts import check_funcs
from other.my_secrets import MySecrets
import logging

TESTRAIL_DICT = MySecrets.TESTRAIL_DICT

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # stream_handler will use this level

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("sample.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

ALL_GIS_OBJS = MySecrets.get_all_admin_gis_objs()
NITRO_GIS_OBJS = MySecrets.get_nitro_admin_gis_objs()


class TestRailClass(unittest.TestCase):
    @staticmethod
    def log_string_checks(string, obj, obj_type):
        obj_id = obj["obj_id"] if obj_type == "Test case" else obj["suite_id"]
        bad_links = check_funcs.check_string_for_bad_links(string)
        if bad_links:
            logger.debug(f"{obj_type} {obj_id} has these link issues: {bad_links}")

        test_cases_with_nitro = check_funcs.check_string_contains_substring(
            string, "nitro"
        )

        if test_cases_with_nitro:
            logger.debug(f"{obj_type} {obj_id} contains the string nitro")

        missing_items = check_funcs.check_string_for_missing_items(string, ALL_GIS_OBJS)
        if missing_items:
            logger.debug(f"{obj_type} {obj_id} has these missing items {missing_items}")

        nitro_items = check_funcs.check_string_for_items_in_orgs(
            string, NITRO_GIS_OBJS, "nitro"
        )

        if nitro_items:
            logger.debug(f"{obj_type} {obj_id} has these nitro items {nitro_items}")

    def test_test_cases_for_bad_links_and_items(self, test_cases):
        for test_case in test_cases:
            test_case_preconditions = test_case["custom_preconds"]
            if test_case_preconditions:
                self.log_string_checks(test_case_preconditions, test_case, "Test case")

    def test_testrail(self):
        test_cases = get_funcs.get_test_cases_from_project_id()
        # test_cases = get_funcs.get_test_cases_from_suite_id(307)
        self.test_test_cases_for_bad_links_and_items(test_cases)

        suites = get_funcs.get_suites_from_project_id(
            TESTRAIL_DICT["DASHBOARD_PROJECT_ID"]
        )
        suite_sections = [
            get_funcs.get_sections_from_suite_id(suite["id"]) for suite in suites
        ]
        for suite in suite_sections:
            for section in suite:
                if section["description"]:
                    self.log_string_checks(section["description"], section, "suite")
