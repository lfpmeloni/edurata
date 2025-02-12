import requests
import os

def handler(inputs):
    airtable_base_id = inputs["airtable_base_id"]
    airtable_table_id = inputs["airtable_table_id"]
    api_key = os.getenv("AIRTABLE_API_KEY")

    url = f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "filterByFormula": "AND({Status}='unprocessed')",
        "maxRecords": 10
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return {"records": response.json()["records"]}
    else:
        return {"error": response.text}