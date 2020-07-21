from GitHub.TestrailScripts import testrail
import traceback
from other.my_secrets import MySecrets
from GitHub.TestrailScripts.testrail import APIClient

TESTRAIL_DICT = MySecrets.TESTRAIL_DICT


class Test_Plan:
    def __init__(self, plan_name, client_obj, entries=[]):
        self._plan_name = plan_name
        self._entries = entries
        self._client_obj = client_obj

    def get_plan_as_dict(self):

        return {
            "name": self._plan_name,
            "entries": [
                entry.get_entry_as_dict() for entry in self._entries
            ],  # Use the entry class
        }

    def get_entry(self, suite_id):
        for entry in self._entries:
            if suite_id == entry._suite_id:
                return entry

        return False

    def add_entry(self, suite_id, case_ids):
        entry_to_add = Entry(suite_id=suite_id, case_ids=case_ids)
        self._entries.append(entry_to_add)
        return entry_to_add

    def add_test(self, test):
        case_id = test["case_id"]
        case = self._client_obj.send_get(uri=f"get_case/{case_id}")
        suite_id = case["suite_id"]

        entry = self.get_entry(suite_id)
        if entry:
            if entry.has_test_case(case_id):
                return

            else:
                entry._case_ids.append(case_id)

        else:
            self.add_entry(suite_id=suite_id, case_ids=[case_id])


class Entry:
    def __init__(self, suite_id=None, case_ids=[]):
        self._suite_id = suite_id
        self._case_ids = case_ids

    def get_entry_as_dict(self):
        return {
            "suite_id": self._suite_id,
            "case_ids": self._case_ids,
            "include_all": False,
        }

    def add_test(self, test):
        if test["case_id"] not in self._case_ids:
            self._case_ids.append(test["case_id"])

    def has_test_case(self, case_id):
        if case_id in self._case_ids:
            return True
        else:
            return False


class Run:
    def __init__(
        self,
        suite_id=None,
        name=None,
        milestone_id=None,
        assignedto_id=None,
        case_ids=[],
        config_ids=[],
    ):
        self._suite_id = suite_id
        self._name = name
        self._milestone_id = (milestone_id,)
        self._assignedto_id = assignedto_id
        self._case_ids = case_ids
        self._config_ids = config_ids

    def get_run_as_dict(self):
        return {
            "suite_id": self._suite_id,
            "name": self._name,
            "assignedto_id": self._assignedto_id,
            "include_all": False,
            "case_ids": self._case_ids,
            "config_ids": self._config_ids,
        }


class Result:
    def __init__(self, case_id, suite_id, comment, assignedto_id):
        self._comment = comment
        self._suite_id = suite_id
        self._case_id = case_id
        self._assignedto_id = assignedto_id

    def get_result_as_dict(self):
        return {
            "status_id": 4,
            "assignedto_id": self._assignedto_id,
            "comment": self._comment,
        }


def get_run_id_from_suite_id(test_plan_dict, suite_id):
    for entry in test_plan_dict["entries"]:
        for run in entry["runs"]:
            if run["suite_id"] == suite_id:
                return run["id"]


def add_results_to_test_plan(client_obj, test_plan_id, results):
    test_plan_dict = client_obj.send_get(uri=f"get_plan/{test_plan_id}")

    for result in results:
        try:
            run_id = get_run_id_from_suite_id(test_plan_dict, result._suite_id)
            case_id = result._case_id
            client_obj.send_post(
                f"add_result_for_case/{run_id}/{case_id}", result.get_result_as_dict()
            )
        except Exception:  # cases might have been deleted
            continue


def create_verification_test_plan(
    client_obj, test_plan_id
):  # I'm not very proud of all this. Pretty wonky. = /
    test_plan_dict = client_obj.send_get(uri=f"get_plan/{test_plan_id}")
    project_id = test_plan_dict["project_id"]
    new_test_plan = Test_Plan(
        plan_name=test_plan_dict["name"] + " verification after release branch merge",
        client_obj=client_obj,
    )
    results_to_add = []
    tests_to_add = []
    try:
        for entry in test_plan_dict["entries"]:
            suite_id = entry["suite_id"]
            for run in entry["runs"]:
                run_id = run["id"]
                run_results = client_obj.send_get(
                    uri=f"get_results_for_run/{run_id}/&status_id=5"
                )
                if run_results:
                    for result in run_results:
                        test_id = result["test_id"]
                        user_id = result["created_by"]
                        person_who_failed_it = client_obj.send_get(
                            uri=f"get_user/{user_id}"
                        )["name"]
                        test = client_obj.send_get(
                            uri=f"get_test/{test_id}"
                        )  # get failed test
                        tests_to_add.append(test)
                        comment_to_add = f"original failed test -> {TESTRAIL_DICT['BASE_URL']}/index.php?/tests/view/{test_id} was failed by {person_who_failed_it}"
                        new_result = Result(
                            case_id=test["case_id"],
                            suite_id=suite_id,
                            comment=comment_to_add,
                            assignedto_id=user_id,
                        )
                        results_to_add.append(new_result)
    except Exception as e:
        traceback.print_exc()

    for test in tests_to_add:
        new_test_plan.add_test(test)

    new_test_plan_dict = new_test_plan.get_plan_as_dict()
    added_test_plan = client_obj.send_post(f"add_plan/{project_id}", new_test_plan_dict)
    added_test_plan_id = added_test_plan["id"]

    add_results_to_test_plan(
        client_obj=client_obj, test_plan_id=added_test_plan_id, results=results_to_add
    )


def clone_configuration_groups(client_obj):
    configurations = client_obj.send_get(
        uri=f"get_configs/{TESTRAIL_DICT['3X_DASHBOARD_PROJECT_ID']}"
    )

    for configuration in configurations:
        client_obj.send_post(
            f"add_config_group/{TESTRAIL_DICT['4X_DASHBOARD_PROJECT_ID']}",
            {"name": configuration["name"]},
        )


def clone_configurations(client_obj):
    configuration_groups = client_obj.send_get(
        uri=f"get_configs/{TESTRAIL_DICT['3X_DASHBOARD_PROJECT_ID']}"
    )

    configurations_groups_to_add = {
        "Machine": 45,
        "Popup content": 46,
        "QA environments": 47,
        "Refresh Interval": 48,
        "Roles": 49,
        "ArcGIS Enterprise Platform": 40,
        "ArcGIS Enterprise Security Models": 41,
    }

    for configuration_group in configuration_groups:
        config_group_name = configuration_group["name"]
        try:
            if configurations_groups_to_add[config_group_name]:
                for config in configuration_group["configs"]:
                    client_obj.send_post(
                        f"add_config/{configurations_groups_to_add[config_group_name]}",
                        {"name": config["name"]},
                    )
        except KeyError:
            continue


if __name__ == "__main__":
    tr_client_obj = APIClient(f"https://{TESTRAIL_DICT['BASE_URL']}")
    tr_client_obj.user = TESTRAIL_DICT["USERNAME"]
    tr_client_obj.password = TESTRAIL_DICT["PASSWORD"]
    tr_client_obj.send_get(uri=f"get_case/154433")

    # create_verification_test_plan(tr_client_obj, "5325")

    clone_configurations(tr_client_obj)
