import requests
import csv
import os
import json
from pprint import pprint
from server_classes import vehicles

URL_LOGIN         = 'https://api.baubuddy.de/index.php/login'
URL_QUERY         = 'https://api.baubuddy.de/index.php/v1/vehicles/select/active'
URL_COLORS        = 'https://api.baubuddy.de/dev/index.php/v1/labels/' # this will be concatenated with the labelId
FILE_NAME         = 'vehicles.csv'
OUTPUT_DIR        = 'output'
OUTPUT_FILE       = 'output_server.json'
API_RESPONSE_FILE = 'api_response2.json'

output_dir = os.path.join(os.path.dirname(__file__), OUTPUT_DIR)

file_paths = {
    'output_file'       : os.path.join(output_dir, OUTPUT_FILE),
    'api_response_file' : os.path.join(output_dir, API_RESPONSE_FILE)
}

REQUEST_HEADERS = {
    'Authorization': 'Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz',
    'Content-Type' : 'application/json'
}

REUQEST_JSON = {
    'username': '365',
    'password': '1'
}

def resolve_colorCode(labelId: str, headers: dict, data: dict):
    """
    Takes a labelId and returns the colorCode of the corresponding label.
    """
    color_url = URL_COLORS + labelId
    print()
    print("color_url: ", color_url)

    response = requests.get(color_url, headers=REQUEST_HEADERS, json=REUQEST_JSON)
    response_json = response.json()[0] # response is a list of dicts (one dict in this case)

    pprint(response_json)
    colorCode = response_json['colorCode']
    
    # reassign to none if the return value is empty string
    if colorCode == "":
        colorCode = None
    return colorCode


def main(filter_hu: bool = True):

    # logging in and getting the access token
    new_access_token = requests.post(URL_LOGIN, headers=REQUEST_HEADERS, json=REUQEST_JSON).json()["oauth"]["access_token"]

    # setting the new access token in the headers
    REQUEST_HEADERS["Authorization"] = "Bearer " + new_access_token

    response_query = requests.get(URL_QUERY, headers=REQUEST_HEADERS, json=REUQEST_JSON)
    RESPONSE_QUERY_JSON = response_query.json() # this is a list of dictionaries

    # INITIALIZING OBJECTS AND SETTING THE CSV ATTRIBUTES

    VEHICLES_DICT = {}

    # initialize the vehicles objects and populate the csv attributes
    with open(FILE_NAME, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        next(reader) # skip header row
        for row in reader:
            vehicle            = vehicles()
            key                = vehicle.get_csv_attibutes(row)
            VEHICLES_DICT[key] = vehicle

    # SETTING THE RESPONSE JSON ATTRIBUTES

    # pass each dict in the list by calling set_json_attributes on the the object with same key
    for response_dict in RESPONSE_QUERY_JSON:
        # pprint(response_dict["labelIds"])
        key = response_dict['kurzname']
        try:
            VEHICLES_DICT[key].set_json_attributes(response_dict)
        except KeyError:
            continue

    print()
    print(len(VEHICLES_DICT))
    print()
    # pprint(vars(VEHICLES_DICT))

    # RESOLVING THE COLOR CODES AND DELETING THE ONES WITH NONE HU
    for k, vehicle in VEHICLES_DICT.copy().items():
        # delete ones with None hu
        if filter_hu and vehicle.hu == None:
            del VEHICLES_DICT[k]
            continue
        # resolve colorCode
        if vehicle.labelIds != None:
            vehicle.colorCode = resolve_colorCode(vehicle.labelIds, REQUEST_HEADERS, REUQEST_JSON)

    # SAVE THE VEHICLES_DICT TO A JSON FILE
    vehicles_list = list(VEHICLES_DICT.values())
    json_data = json.dumps([vars(v) for v in vehicles_list], indent=4, ensure_ascii=False)
    
    with open(file_paths['output_file'], 'w') as f:
        f.write(json_data)

    # Use this to write the response to a file
    with open(file_paths['api_response_file'], 'w') as f:
        f.write(json.dumps(response_query.json(), indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main() # filter_hu = True