# To run this file, use the following command:
# uvicorn server:app --host 0.0.0.0 --port 8000 --reload
# launch this on http://localhost:8000/csv_to_json

from fastapi import FastAPI, File, UploadFile
from typing import Optional
import csv

app = FastAPI()

def csv_process(csv_file):
    msg = {f"Row {i}": row for i, row in enumerate(csv.reader(csv_file)) if i < 3}
    return msg
        
@app.post("/csv_to_json")
async def csv_to_json(csv_file: UploadFile = File(...)):

    msg = None
    if not csv_file.filename.endswith(".csv"):
        msg = "No csv found"
    else:
        contents = await csv_file.read()
        contents = contents.decode("utf-8").split("\n")
        msg = csv_process(contents)
    return {"message": msg}
