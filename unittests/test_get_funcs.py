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

    def test_get_links_from_string(self):
        string = "strings https://arcgis.com and more strings"
        link = get_funcs.get_links_from_string(string)
        self.assertEqual(
            link, "https://arcgis.com"
        )  # Is this testing a constant? Bad prtactice?

    def test_get_item_ids_from_string(self):
        string = """
                Sample webmap with all geom and refresh types:
                id: a540748151b84753b609d67488be363e
                org: dbqa in devext
                Sample dashboard
                id: d54f71aadaca4cd1899e133bdf3c028c
                org: dbqa in devext
                """
        item_ids = get_funcs.get_item_ids_from_string(string)
        actual_item_ids = [
            "a540748151b84753b609d67488be363e",
            "d54f71aadaca4cd1899e133bdf3c028c",
        ]

        self.assertEqual(item_ids, actual_item_ids)

    def test_get_item_from_item_id(self):
        item_id = "a540748151b84753b609d67488be363e"
        item = get_funcs.get_item_from_item_id(item_id)
        self.assertIsInstance(item, Item)

    def test_get_item_host_name(self):
        item = AUTOMATION_DEVEXT_DBQA_GIS.content.get(
            "ec18963f29864b7baf5f5eb236f6a545"
        )
        item_host_name = get_funcs.get_item_host_name(item)
        self.assertEqual(item_host_name, AGOL_DICT["AGOL_DBQA_DEVEXT_HOST_NAME"])
