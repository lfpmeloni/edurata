import requests
import os

def handler(inputs):
    airtable_base_id = inputs["airtable_base_id"]
    airtable_table_id = inputs["airtable_table_id"]
    record_id = inputs["record_id"]
    generated_content = inputs["generated_content"]
    api_key = os.getenv("AIRTABLE_API_KEY")

    url = f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_id}/{record_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "Generated Content": generated_content,
            "Status": "processed"
        }
    }

    response = requests.patch(url, headers=headers, json=data)
    
    return {"status": response.status_code, "response": response.text}