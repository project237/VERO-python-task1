
"""
============== USAGE ==============

A list of example commands for running this file
Make sure you don't use quotes
  python client.py -k labelIds colorCode gruppe kurzname hu -c True 
  python client.py -k labelIds -c False
  python client.py -c 0
  python client.py

Keep in mind that flag --colored always defaults to True, and the output file columns always include column rnr, 
even if its not given in --keys 

Make sure server.py is currently running on localhost and if it is running in a port other than 8000, change
constant URL accordingly
"""

import argparse
import requests
import json
import pandas as pd
import os
import datetime as dt
from distutils import util
from pprint import pprint
from typing import Dict, List

OUTPUT_DIRECTORY = "output"
RESPONSE_FILE    = f"{OUTPUT_DIRECTORY}/server_response.UNfiltered.json" # test file, opened as input when api at login url is not responding (on server side)
INPUT_FILE       = "vehicles.csv"
KEYS             = []
TODAY            = dt.datetime.today().date()
OUTPUT_FILE      = f"{OUTPUT_DIRECTORY}/vehicles_{TODAY.isoformat()}.xlsx"
URL              = "http://localhost:8000/csv_to_json"
VALID_KEYS       = ["gruppe", "kurzname", "langtext", "info", "lagerort", "labelIds", "asu", "bisdat", "bleGroupEnum", 
                    "businessUnit", "createdOn", "editedOn", "externalId", "fuelConsumption", "gb1", "hu", "lteartikel",
                    "ownerId", "priceInformation", "rnr", "safetyCheckDate", "sort", "tachographTestDate", "userId", 
                    "vin", "vondat", "colorCode", "profilePictureUrl", "thumbPathUrl"]

def color_row(row, color_text=False, color_bg=False):
    """ 
    if --keys contain "labelIds":
        colors the row text to the color given in column colorCode, if it exists
    if --colored is set to True (color_bg in this scope)
        if column hu is empty, does nothing to row background color
        if column hu is not older than 3 months, colors row background to #007500"
        if column hu is not older than 12 months, colors row background to #FFA500"
        if column hu is older than 12 months, colors row background to #b30000"

    Args:
        row        : pd.Series object for the current row being passed
        color_text : bool
        color_bg   : bool

    Returns:
        pd.Series object with the styling string for the row (color_row_str) as well as row index 
    """
    color_text_str = ""
    if color_text:
        if row.colorCode:
            color_text_str = f"color: {row.colorCode}"

    color_bg_str = ""
    if color_bg and row['hu']:
        if pd.isna(row["hu"]):
            color_bg_str = ""

        hu_date = dt.datetime.strptime(row['hu'], '%Y-%m-%d').date() 
        time_diff = (TODAY - hu_date).days

        if time_diff <= 90:
            color_bg_str = "background-color: #007500"
        elif time_diff <= 365:
            color_bg_str = "background-color: #FFA500"
        else:
            color_bg_str = "background-color: #b30000"

    color_row_str = ""
    if color_text and color_bg:
        color_row_str = f"{color_text_str}; {color_bg_str}"
    else:
        color_row_str = color_text_str or color_bg_str
    # print(color_row_str)

    return pd.Series(color_row_str, row.index)


def process_server_response(server_response: List[Dict], keys=[], colored=True):
    """
    TODOS:
    - Save with module os
    """

    df = pd.DataFrame(server_response)

    # sort rows by field gruppe
    df = df.sort_values(by=["gruppe"])

    # if columns labelIds and colorCode will be displayed
    # we color the cell text on column colorCode (if resolved)
    color_text = False
    color_background = False
    if "labelIds" in keys:
        color_text = True

    # if colored flag is True, runs color_row() which colors the rows based on the conditions
    if colored:
        color_background = True
    df = df.style.apply(color_row, color_text=color_text, color_bg=color_background, axis=1)

    # select only the colums rnr and ones in keys
    cols = ["rnr"] + keys if "rnr" not in keys else keys

    # save the dataframe to directory "output/OUTPUT_FILE"
    df.to_excel(OUTPUT_FILE, columns=cols, index=False)


def main():
    print()
    parser = argparse.ArgumentParser(description='Print keys with color flag')
    parser.add_argument('-k', '--keys', nargs='+', help='input keys', default=[])
    parser.add_argument('-c', '--colored', default=True, help='colored flag', type=lambda x: bool(util.strtobool(x)))

    # update global variables with the arguments
    args    = parser.parse_args()
    KEYS    = args.keys
    colored = args.colored

    try:
        assert all([(k in VALID_KEYS) for k in KEYS])
    except:
        print("ERROR - NOT ALL KEYS PROVIDED ARE AMONG VALID_KEYS")
        print("TRY AGAIN WITH VALID KEYS")
        return

    print("RUNNING CLIENT WITH FOLLOWING ARGUMENTS:")
    pprint({"KEYS": KEYS, "COLORED": colored})

    # create output directory if it doesnt exist yet
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    response = None
    # Open the CSV file and prepare the request payload
    try:
        with open(INPUT_FILE, "rb") as csv_file:
            file_dict = {"csv_file": csv_file}
            try:
                response = requests.post(URL, files=file_dict)
                response = response.json() # convert response object to a list of dictionaries
            except Exception as e:
                print("\nERROR WHILE SENDING INPUT_FILE TO SERVER")
                print()
                print(f"RUNNING WITH TEST FILE: {RESPONSE_FILE}")
                # return
                with open(RESPONSE_FILE, "rb") as response_file:
                    response = json.load(response_file)
    except FileNotFoundError:
        print(f"ERROR - INPUT FILE {INPUT_FILE} WAS NOT FOUND IN CURRENT DIRECTORY")
        return
        
    process_server_response(response, keys=KEYS, colored=colored)
    print()
    print(f"FILE HAS BEEN SAVED TO RELATIVE PATH: \n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()


