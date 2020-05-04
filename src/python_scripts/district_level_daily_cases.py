import requests
import json
import sys,os
import pdb

raw_data_url_1 = "https://api.covid19india.org/raw_data1.json"
raw_data_url_2 = "https://api.covid19india.org/raw_data2.json"
raw_data_url_3 = "https://api.covid19india.org/raw_data3.json"


raw_data_json_1 = requests.get(raw_data_url_1)
raw_data_json_2 = requests.get(raw_data_url_2)
raw_data_json_3 = requests.get(raw_data_url_3)

raw_data_dict_1 = raw_data_json_1.json()
raw_data_dict_2 = raw_data_json_2.json()
raw_data_dict_3 = raw_data_json_3.json()

district_count = {}

def prepare_data_from_raw_data_1_and_2(raw_data_dict):    

    for data in raw_data_dict['raw_data']:
            try:
                if data['detectedstate'] in district_count:
                    if data['detecteddistrict'] in district_count[data['detectedstate']]:
                        if data['dateannounced'] in district_count[data['detectedstate']][data['detecteddistrict']]:
                            district_count[data['detectedstate']][data['detecteddistrict']][data['dateannounced']] += 1
                        else:
                                district_count[data['detectedstate']][data['detecteddistrict']][data['dateannounced']] = 1

                    else:
                        district_count[data['detectedstate']][data['detecteddistrict']] = {}
                else:
                    district_count[data['detectedstate']] = {}
            except KeyError as e:
                pass

def prepare_data_from_raw_data_3(raw_data_dict):

    for data in raw_data_dict_3['raw_data']:
        if data['currentstatus'] == 'Hospitalized':
            try:
                if data['detectedstate'] in district_count:
                    if data['detecteddistrict'] in district_count[data['detectedstate']]:
                        if data['dateannounced'] in district_count[data['detectedstate']][data['detecteddistrict']]:
                            district_count[data['detectedstate']][data['detecteddistrict']][data['dateannounced']] += int(data['numcases'])
                        else:
                            if data['numcases'] != '':
                                district_count[data['detectedstate']][data['detecteddistrict']][data['dateannounced']] = int(data['numcases'])
                            else:
                                district_count[data['detectedstate']][data['detecteddistrict']][data['dateannounced']] = "Data not available"

                    else:
                        district_count[data['detectedstate']][data['detecteddistrict']] = {}
                else:
                    district_count[data['detectedstate']] = {}
            except KeyError as e:
                pass
        else:
            pass

    
def main():
    prepare_data_from_raw_data_1_and_2(raw_data_dict_1)
    prepare_data_from_raw_data_1_and_2(raw_data_dict_2)
    prepare_data_from_raw_data_3(raw_data_dict_3)

    if not os.path.exists("../json"):
        os.makedirs("../json")
    
    with open("../json/daily_district_level_cases.json", "w") as f:
        json.dump(district_count,f, indent = 4)

if __name__ == "__main__":
    main()

