import unittest
from GitHub.TestrailScripts import get_funcs
from other.my_secrets import get_automation_devext_dbqa_gis, AGOL_DICT
from arcgis.gis import Item

AUTOMATION_DEVEXT_DBQA_GIS = get_automation_devext_dbqa_gis()


class FirstClass(unittest.TestCase):
    def test_get_suites_from_project_id(self):
        suites = get_funcs.get_suites_from_project_id()
        self.assertIsInstance(suites, list)

    def test_get_test_cases_from_suite_id(self):
        pie_chart_suite_id = "307"
        test_cases = get_funcs.get_test_cases_from_suite_id(pie_chart_suite_id)
        self.assertIsInstance(test_cases, list)

    def test_get_test_case_from_id(self):
        test_case_id = "76247"
        test_cases = get_funcs.get_test_case_from_id(test_case_id)
        self.assertIsInstance(test_cases, dict)
