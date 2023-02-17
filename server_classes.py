
import csv

FILE_NAME = 'vehicles.csv'

class vehicles_handler:
    def __init__(self):
        pass

    def request_vehicle_info():
        pass

    def populate_csv_attributes():
        pass

    def populate_json_attributes():
        pass

    def filter_hu_none():
        pass

    def resolve_colorCode():
        pass

    def save_to_files():
        pass

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

    # initialize the vehicles objects and populate the csv attributes
    with open(FILE_NAME, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            vehicle            = vehicles()
            key                = vehicle.get_csv_attibutes(row)
            vehicles_dict[key] = vehicle

    for i, e in enumerate(vehicles_dict.values()):
        if i == 12:
            break
        print()
        print("gruppe: ", e.gruppe)
        print("kurzname: ", e.kurzname)
        print("langtext: ", e.langtext)
        print("info: ", e.info)
        print("lagerort: ", e.lagerort)
        print("labelIds: ", e.labelIds)