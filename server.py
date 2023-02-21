
"""
============== USAGE ==============

To run this file, use the following command:
  uvicorn server:app --host 0.0.0.0 --port 8000 --reload
Launch this on 
  http://localhost:8000/csv_to_json

"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from server_classes import vehicles_handler

FILTER_HU = 0

app = FastAPI()

@app.post("/csv_to_json")
async def csv_to_json(csv_file: UploadFile = File(...)):
    """
    This method defines the api endpoint at http://localhost:8000/csv_to_json

    When running vehicles_handler().main() set agument filter_hu to True if you'd like to 
        remove all objects with field hu empty, and False otherwise

    Args:
        csv_file (UploadFile, optional): A file object passed as a payload by the request

    Raises:
        HTTPException: Whenever anything other than a csv file is sent as a payload

    Returns:
        processed_json: a python list of dictionaries that is serialized into a standart json when being returned by fastapi
    """

    if not csv_file.filename.endswith(".csv"):
        raise HTTPException(status_code=422, detail="Request must contain a CSV file.")
    
    csv_contents = await csv_file.read()
    csv_contents = csv_contents.decode("utf-8").split("\n")

    # this is a simple list of dictionaries but will be serialized to JSON when returned by the API
    processed_json = vehicles_handler().main(csv_contents, filter_hu=FILTER_HU)

    return processed_json
    

