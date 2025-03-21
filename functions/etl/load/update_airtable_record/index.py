import requests

def handler(inputs):
    airtable_base_id = inputs.get("airtable_base_id")
    airtable_table_id = inputs.get("airtable_table_id")
    airtable_api_key = inputs.get("airtable_api_key")
    fields = inputs.get("fields")

    if not airtable_base_id:
        return {"error": "airtable_base_id is missing."}
    if not airtable_table_id:
        return {"error": "airtable_table_id is missing."}
    if not airtable_api_key:
        return {"error": "airtable_api_key is missing."}
    if not isinstance(fields, dict):
        return {"error": "fields must be a dictionary."}

    url = f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_id}"
    headers = {
        "Authorization": f"Bearer {airtable_api_key}",
        "Content-Type": "application/json"
    }

    data = { "fields": fields }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return {"error": f"Airtable API error {response.status_code}: {response.text}"}

    return {
        "status": "success",
        "created_record": response.json()
    }
