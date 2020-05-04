import requests
import json
import os

testing_stats_url = "https://api.covid19india.org/state_test_data.json"

testing_stats_json = requests.get(testing_stats_url)

testing_stats_dict = testing_stats_json.json()

testing_count = {}

for data in testing_stats_dict['states_tested_data']:
    if data['state'] in testing_count:
        if data['updatedon'] in testing_count[data['state']]:
            testing_count[data['state']][data['updatedon']] += int(data['totaltested'])
        else:
            if data['totaltested']:
                testing_count[data['state']][data['updatedon']] = int(data['totaltested'])
    else:
        testing_count[data['state']] = {}

if not os.path.exists("../json"):
    os.makedirs("../json")

with open("../json/statewise_daily_testing_data.json", "w") as f:
    json.dump(testing_count,f, indent = 4)