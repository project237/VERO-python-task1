
# RUN THS FILE WITH:
#   python client.py -k key1 key2 key3 -c 0 

import argparse
import requests
from distutils import util
from pprint import pprint

INPUT_FILE = "vehicles.csv"
KEYS       = []
COLORED    = True
URL        = "http://localhost:8000/csv_to_json"

def main():
    parser = argparse.ArgumentParser(description='Print keys with color flag')
    parser.add_argument('-k', '--keys', nargs='+', help='input keys')
    parser.add_argument('-c', '--colored', default=True, help='colored flag', type=lambda x: bool(util.strtobool(x)))

    # update global variables with the arguments
    args    = parser.parse_args()
    KEYS    = args.keys
    COLORED = args.colored

    # pprint(args)
    # print()
    # pprint(KEYS)
    # print()
    # pprint(COLORED)

    # Open the CSV file and prepare the request payload
    with open(INPUT_FILE, "rb") as csv_file:
        file_dict = {"csv_file": csv_file}
        try:
            response = requests.post(URL, files=file_dict)
        except Exception as e:
            print("ERROR WHILE SENDING REQUEST:")
            pprint(e, indent=4)
            return

    print()
    pprint(response.json())

if __name__ == "__main__":
    main()


