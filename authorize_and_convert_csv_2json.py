import requests
import csv
from pprint import pprint
from server_classes import vehicles

URL_LOGIN   = 'https://api.baubuddy.de/index.php/login'
URL_QUERY   = 'https://api.baubuddy.de/index.php/v1/vehicles/select/active'
FILE_NAME   = 'vehicles.csv'
OUTPUT_FILE = 'api_response.json'

headers = {
    'Authorization': 'Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz',
    'Content-Type': 'application/json'
}

data = {
    'username': '365',
    'password': '1'
}

if __name__ == "__main__": 

    response_login = requests.post(URL_LOGIN, headers=headers, json=data)
    response_query = requests.get(URL_QUERY)
    # this is a list of dictionaries
    response_query_json = response_query.json()
    # pprint(response_query_json)

    # INITIALIZING OBJECTS AND SETTING THE CSV ATTRIBUTES

    vehicles_dict = {}

    # initialize the vehicles objects and populate the csv attributes
    with open(FILE_NAME, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            vehicle            = vehicles()
            key                = vehicle.get_csv_attibutes(row)
            vehicles_dict[key] = vehicle

    # SETTING THE RESPONSE JSON ATTRIBUTES

    # pass each dict in the list by calling set_json_attributes on the the object with same key
    for response_dict in response_query_json:
        key = response_dict['kurzname']
        try:
            vehicles_dict[key].set_json_attributes(response_dict)
        except KeyError:
            continue

    print()
    print(len(vehicles_dict))
    print()
    # pprint(vars(vehicles_dict))
    for e in vehicles_dict.values():
        pprint(vars(e))


    # Use this to write the response to a file
    # with open(OUTPUT_FILE, 'w') as f:
    #     f.write(response_query.text)
