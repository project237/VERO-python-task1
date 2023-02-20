import requests
from pprint import pprint

URL        = "http://localhost:8000/csv_to_json"
INPUT_FILE  = "vehicles.csv"
FILE2      = "dummy.txt" # for testing purposes

# Open the CSV file and prepare the request
with open(INPUT_FILE, "rb") as csv_file:
    file_dict = {"csv_file": csv_file}
    response = requests.post(URL, files=file_dict)

# Print the response
print()
pprint(response.json())
# pprint(response.content)