
import requests
import csv
from pprint import pprint

FILE_NAME   = "vehicles.csv" # for testing

class vehicles_handler:
    """
    In this class, we organize the code that processes vehicles.csv and returns a json file that will be sent to the client.

    No init method since this class is only going to have a single instance. So we are using class variables instead of instance variables.
    """
    url_login   = 'https://api.baubuddy.de/index.php/login'
    url_query   = 'https://api.baubuddy.de/index.php/v1/vehicles/select/active'
    url_colors  = 'https://api.baubuddy.de/dev/index.php/v1/labels/' # this will be concatenated with the labelId
    filter_hu   = None
    request_headers = {
    'Authorization': 'Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz',
    'Content-Type' : 'application/json'
    }
    reuqest_json = {
        'username': '365',
        'password': '1'
    }
    # these will be set during the execution
    csv_file            = None
    response_query_json = None
    json_data           = None
    vehicles_dict       = {}

    def main(self, csv_file, filter_hu: bool = False):
        self.filter_hu = filter_hu
        self.csv_file = csv_file
        self.request_vehicle_info()
        self.populate_vehicle_attributes()
        self.filter_hu_and_resolve_colorCodes()
        return self.json_data

    def request_vehicle_info(self):
        """
        Authorizes and requests vehicle info from url_query endpoint.
        """
        # logging in and getting the access token
        new_access_token = requests.post(self.url_login, headers=self.request_headers, json=self.reuqest_json).json()["oauth"]["access_token"]

        # setting the new access token in the headers
        self.request_headers["Authorization"] = "Bearer " + new_access_token

        response_query = requests.get(self.url_query, headers=self.request_headers, json=self.reuqest_json)
        self.response_query_json = response_query.json() # this is a list of dictionaries

    def populate_vehicle_attributes(self):
        """
        Only called by reolve_colorCode.
        Here we populate the vehicles objects with the attributes from the csv file and the api response (json).
        """
        reader = csv.reader(self.csv_file, delimiter=';', quotechar='"')
        next(reader) # skip header row
        for row in reader:
            vehicle            = vehicles()
            key                = vehicle.get_csv_attibutes(row)
            self.vehicles_dict[key] = vehicle

        # pass each dict in the list by calling set_json_attributes on the the object with same key
        for response_dict in self.response_query_json:
            key = response_dict['kurzname']
            try:
                self.vehicles_dict[key].set_json_attributes(response_dict)
            except KeyError:
                continue

    def resolve_colorCode(self, labelId):
        """
        Takes a labelId and returns the colorCode of the corresponding label.
        """
        color_url = self.url_colors + labelId
        print()
        print("color_url: ", color_url)

        response = requests.get(color_url, headers=self.request_headers, json=self.reuqest_json)
        response_json = response.json()[0] # response is a list of dicts (one dict in this case)

        pprint(response_json)
        colorCode = response_json['colorCode']
        
        # reassign to none if the return value is empty string
        if colorCode == "":
            colorCode = None
        return colorCode
    
    def filter_hu_and_resolve_colorCodes(self):
        for k, vehicle in self.vehicles_dict.copy().items():
            # delete ones with None hu
            if self.filter_hu and vehicle.hu == None:
                del self.vehicles_dict[k]
                continue
            # resolve colorCode
            if vehicle.labelIds != None:
                vehicle.colorCode = self.resolve_colorCode(vehicle.labelIds)
        
        self.json_data = list(self.vehicles_dict.values())
        # vehicles_list = list(self.vehicles_dict.values())
        # self.json_data = json.dumps([vars(v) for v in vehicles_list], indent=4, ensure_ascii=False)
    

class vehicles:
    """
    Objects of this class contain info on the parsed data structures (from the csv file and api response).

    ASSUMPTIONS:
    - For the a vehicle object to be parsed and included, its kurzname must be present both in the csv file,
    so, if it is only present in the json response, it will not be included.
    - The primary key is the kurzname attribute, 
    thus all csv rows and json objects must have this attribute as a unique value or else the last appearing entry with the same
    kurzname will overwrite (any) earlier ones. 
    - The csv columns are always in the same order. 
    """
    
    def __init__(self):
        
        # csv attributes
        self.gruppe             = None
        self.kurzname           = None
        self.langtext           = None
        self.info               = None
        self.lagerort           = None
        self.labelIds           = None

        # json attributes
        self.asu                = None
        self.bisdat             = None
        self.bleGroupEnum       = None
        self.businessUnit       = None
        self.createdOn          = None
        self.editedOn           = None
        self.externalId         = None
        self.fuelConsumption    = None
        self.gb1                = None
        self.hu                 = None
        self.lteartikel         = None
        self.ownerId            = None
        self.priceInformation   = None
        self.rnr                = None
        self.safetyCheckDate    = None
        self.sort               = None
        self.tachographTestDate = None
        self.userId             = None
        self.vin                = None
        self.vondat             = None

        # attributes to be resolved with second api call
        self.colorCode          = None

    def get_csv_attibutes(self, row: list):
        """
        Takes the parsed list of csv row attributes and assigns these to their respective attributes.

        gruppe
        kurzname
        langtext
        info
        lagerort
        labelIds
        labelIds

        Args:
            row (list): A list of the parsed csv row.

        Returns:
            self.kurzname (str): The primary key of the row.
        """
        self.gruppe              = row[0]
        self.kurzname            = row[1]
        self.langtext            = row[2]
        self.info                = row[3]
        self.lagerort            = row[4]
        self.labelIds            = row[5]

        # return the primary key
        return self.kurzname
    
    def set_json_attributes(self, json_object: dict):
        for key in json_object:
            setattr(self, key, json_object[key])


# ======================== TEST HERE ========================

if __name__ == "__main__":
    vehicles_dict = {}

    # TEST CODE FOR CLASS vehicles
    # # initialize the vehicles objects and populate the csv attributes
    # with open(FILE_NAME, 'r', newline='') as csvfile:
    #     reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    #     for row in reader:
    #         vehicle            = vehicles()
    #         key                = vehicle.get_csv_attibutes(row)
    #         vehicles_dict[key] = vehicle

    # for i, e in enumerate(vehicles_dict.values()):
    #     if i == 12:
    #         break
    #     print()
    #     print("gruppe: ", e.gruppe)
    #     print("kurzname: ", e.kurzname)
    #     print("langtext: ", e.langtext)
    #     print("info: ", e.info)
    #     print("lagerort: ", e.lagerort)
    #     print("labelIds: ", e.labelIds)

    # TEST CODE FOR CLASS vehicles_handler
    vh = vehicles_handler()
    output = None

    with open(FILE_NAME, 'r', newline='') as csvfile:
        output = vh.main(csvfile, filter_hu=True)

    # save output file as "vehicles_handler_output.json"
    with open("output/vehicles_handler_output.json", "w", encoding="utf-8") as f:
        f.write(output)