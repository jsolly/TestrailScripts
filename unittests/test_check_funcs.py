import unittest
from GitHub.TestrailScripts import check_funcs


class FirstClass(unittest.TestCase):
    def test_check_string_for_bad_links(self):
        string = (
            "some text https://www.sadjklfseijo.com other text https://www.esri.com"
        )
        result = check_funcs.check_string_for_bad_links(string)
        first_link_result, second_link_result = result[0], result[1]
        self.assertFalse(first_link_result[0])
        self.assertTrue(second_link_result[0])

    def test_check_string_for_nitro_string(self):
        nitro_string = "https://nitro.maps.devext.com"
        result = check_funcs.check_string_contains_the_word_nitro(nitro_string)
        self.assertTrue(result)

    def test_check_string_for_nitro_items(self):
        string = """
            Here is a nitro item id:d847ab36f06f49bcb2fffd7efff15153
            and here is a dbqa item id:d864fe054004496d97968e7fd94edd18"
            """
        results = check_funcs.check_string_for_nitro_items(string)
        self.assertEqual(results[0].org, "nitro")

    def test_check_string_for_missing_items(self):
        self.fail("Finish the test")

    def test_check_testrail_for_bad_links_and_items(self):
        self.fail("Finish the test")
