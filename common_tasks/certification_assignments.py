import binpacking

# 4x cert
suite_dict = {
    "ArcGIS org Integration": 33,  # 33 (suite)
    "Home Page": 7,  # 7 (Suite)
    "Dashboard Level Settings": 62,  # 62 (Suite)
    "Layout": 17,  # 17 (Suite)
    "Details Element": 21,  # 7 (Common-all) + 4 (common details-identify) + 10 (suite)
    "Embedded Content": 20,  # 7 (Common-all) + 13 (suite)
    "Gauge": 47,  # 19 (Common-all) + 28 (Suite)
    "Indicator": 47,  # 4 (Common-all) + 43 (suite)
    "Legend Element": 11,  # 3 (Common-all) + 6 (common legend) + 2 (suite)
    "List": 29,  # 8 (Common-all) + 14 (actions) + 7 (suite)
    "Map": 52,  # 2 (Common-all) + 4 (common details-identify) + 14 (actions) + 32 (suite)
    "Pie Chart": 75,  # 22 (Common-all) + 18 (actions) + 55 (Pie Chart)
    "Rich Text Element": 4,  # 2 (Common-all) + 2 (suite)
    "Selectors": 78,  # 21 (Common-all) + 33 (actions) + 22 (suite)
    "Serial Chart": 147,  # 29 (Common-all) + 26 (Actions) + 92 (suite)
    "Data Sources": 23,  # 23 (suite)
    "URL Parameters": 18,  # 18 (actions)
    "Side Panel": 3,  # 3 (suite)
    # "L10N_I8N":
    "Arcade": 7,  # 7 (suite)
}

# 3x cert
# suite_dict = {
#     "ArcGIS org Integration": 41,
#     "Home Page": 5,
#     "Dashboard Level Settings": 15,
#     "Data Sources": 7,
#     "Indicator": 50,  # 9 + 41
#     "Rich Text Element": 4,  # 2 + 2
#     "Pie Chart": 8,
#     "Details Element": 5,
#     "Embedded Content": 5,
#     "ArcGIS Online New Features": 17,
#     "Side Panel": 3,
#     "Serial Chart": 35,  # 18 + 17
#     "Gauge": 10,
#     "Legend Element": 3,
#     "List": 5,
#     "Map": 5,  # 3 + 2
#     "Selectors": 17,  # 7 + 8 + 9
#     # "One Offs": 1,
# }

EMPLOYEES = 8

total_test_cases = sum(suite_dict.values())
bins = binpacking.to_constant_bin_number(suite_dict, EMPLOYEES)

print(f"There are a total of {total_test_cases} test cases")
for index, employee in enumerate(bins):
    print(f"\n Bucket {index} has {sum(employee.values())} tests")
    print(employee)
    # print(employee.keys())
