from GitHub.TestrailScripts import get_funcs

get_funcs.get


TEST_RAIL_API_OBJ = testrail.APIClient(
    base_url="https://" + MySecrets.TESTRAIL_DICT["BASE_URL"]
)
TEST_RAIL_API_OBJ.user = MySecrets.TESTRAIL_DICT["USERNAME"]
TEST_RAIL_API_OBJ.password = MySecrets.TESTRAIL_DICT["PASSWORD"]
