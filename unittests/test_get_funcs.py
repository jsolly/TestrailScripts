import unittest
from GitHub.TestrailScripts import get_funcs
from other.my_secrets import MySecrets


class FirstClass(unittest.TestCase):
    gis_obj = MySecrets.get_agol_gis("DEV_ENV", "DBQA_AUTOMATION")

    def test_get_certification_assignments(self):
        # 4x cert
        # suite_dict = {
        #     "ArcGIS org Integration": 34,  # Needs update
        #     "Home Page": 4,  # Originally was 5
        #     "Dashboard Level Settings": 65,
        #     "Layout": 17,  #
        #     "Details Element": 22,  # 8 + 4 + 10
        #     "Embedded Content": 22,  # 8 + 14
        #     "Gauge": 50,  # 12 + 10 + 28 check this originally 56
        #     "Indicator": 68,  # 12 + 10 + 46 check this...originally 77
        #     "Legend Element": 11,  # 3 + 4 + 2 + 2 Check this originally 9
        #     "List": 29,  # 9 + 14 + 7
        #     "Map": 65,  # 2 + 4 + 4 + 5 + 50 .... originally got 68
        #     "Pie Chart": 118,  # 9 + 8 + 8 + 7 + 5 + 36 + 10 + 35
        #     "Rich Text Element": 4,  # 2 + 2 ..originally was 5
        #     "Selectors": 68,  # 2 + 7 + 8 + 2 + 3 + 5 + 6 + 3 + 2 + 2 + 28  ... got 68..originally was 64
        #     "Serial Chart": 156,  # 9 + 8 + 8 + 8 + 5 + 2 + 2 + 114 ... got 156... originallly 155
        #     "Data Sources": 7,  #
        #     "Side Panel": 3,  #
        #     "L10N_I8N": 24,  #
        # }

        # 3x cert
        suite_dict = {
            "ArcGIS org Integration": 40,
            "Home Page": 4,
            "Dashboard Level Settings": 15,
            "Data Sources": 7,
            "Indicator": 50,  # 9 + 41
            "Rich Text Element": 4,  # 2 + 2
            "Pie Chart": 8,
            "Details Element": 5,
            "Embedded Content": 5,
            "ArcGIS Online New Features": 7,
            "Side Panel": 3,
            "Serial Chart": 35,  # 18 + 17
            "Gauge": 10,
            "Legend Element": 3,
            "List": 5,
            "Map": 5,  # 3 + 2
            "Selectors": 17,  # 7 + 8 + 9
        }

        self.assertTrue(get_funcs.get_certification_assignments(suite_dict, 5))

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
