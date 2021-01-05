from GitHub.TestrailScripts import create_funcs
from GitHub.TestrailScripts.testrail import APIClient

TESTRAIL_DICT = create_funcs.TESTRAIL_DICT

tr_client_obj = APIClient(f"https://{TESTRAIL_DICT['BASE_URL']}")
tr_client_obj.user = TESTRAIL_DICT["USERNAME"]
tr_client_obj.password = TESTRAIL_DICT["PASSWORD"]
tr_client_obj.send_get(uri=f"get_case/154433")

test_plan_id = "7188"
test_plan = tr_client_obj.send_get(uri=f"get_plan/{test_plan_id}")


def update_run_in_plan_entry_to_db_guest(run_id):
    try:
        tr_client_obj.send_post(
            uri=f"update_run_in_plan_entry/{test_plan_id}/{run_id}",
            data={"assignedto_id": 32},
        )

    except Exception as e:
        print(e)


for entry in test_plan["entries"]:
    tr_client_obj.send_post(
        uri=f"update_plan_entry/{test_plan_id}/{entry['id']}",
        data={"assignedto_id": 32},  # 32 is Dashboard guest
    )

    for run in entry["runs"]:
        update_run_in_plan_entry_to_db_guest(run["id"])
