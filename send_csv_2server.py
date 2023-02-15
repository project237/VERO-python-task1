import requests
from pprint import pprint

URL = "http://localhost:8000/csv_to_json"
FILE = "vehicles.csv"
FILE2 = "dummy.txt"

# Open the CSV file and prepare the request
with open(FILE, "rb") as csv_file:
    files = {"csv_file": csv_file}
    response = requests.post(URL, files=files)

# Print the response
print()
pprint(response.json())
# pprint(response.content)


