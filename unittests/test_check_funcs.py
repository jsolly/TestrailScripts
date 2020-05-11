import unittest
from GitHub.TestrailScripts import check_funcs


class FirstClass(unittest.TestCase):

    # def test_check_testrail_for_bad_links_and_items(self):
    #     check_funcs.check_testrail_for_bad_links_and_items()

    def test_check_string_for_nitro_string(self):
        nitro_string = "https://nitro.maps.devext.com"
        result = check_funcs.check_string_for_nitro_string(nitro_string)
        self.assertTrue(result)

    def test_get_human_readable_response(self):
        url = "https://esri.box.com/s/yhy1o8j99fd2xntpn4zwmfrc4m2zz619"
        result = check_funcs.get_human_readable_response(url)
        self.assertNotEqual(result, 200)
