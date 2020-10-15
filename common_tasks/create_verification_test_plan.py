from GitHub.TestrailScripts import create_funcs
from GitHub.TestrailScripts.testrail import APIClient

TESTRAIL_DICT = create_funcs.TESTRAIL_DICT


def create_verification_test_plan(
    client_obj, test_plan_id
):  # I'm not very proud of all this. Pretty wonky. = /
    test_plan_dict = client_obj.send_get(uri=f"get_plan/{test_plan_id}")
    project_id = test_plan_dict["project_id"]
    new_test_plan = create_funcs.Test_Plan(
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
                        new_result = create_funcs.Result(
                            case_id=test["case_id"],
                            suite_id=suite_id,
                            comment=comment_to_add,
                            assignedto_id=user_id,
                        )
                        results_to_add.append(new_result)
    except Exception as e:
        print(e)

    for test in tests_to_add:
        new_test_plan.add_test(test)

    new_test_plan_dict = new_test_plan.get_plan_as_dict()
    added_test_plan = client_obj.send_post(f"add_plan/{project_id}", new_test_plan_dict)
    added_test_plan_id = added_test_plan["id"]

    create_funcs.add_results_to_test_plan(
        client_obj=client_obj, test_plan_id=added_test_plan_id, results=results_to_add
    )


if __name__ == "__main__":
    tr_client_obj = APIClient(f"https://{TESTRAIL_DICT['BASE_URL']}")
    tr_client_obj.user = TESTRAIL_DICT["USERNAME"]
    tr_client_obj.password = TESTRAIL_DICT["PASSWORD"]
    tr_client_obj.send_get(uri=f"get_case/154433")

    create_verification_test_plan(tr_client_obj, "6444")
