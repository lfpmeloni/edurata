import requests

def handler(inputs):
    # Fetch inputs safely
    airtable_base_id = inputs.get("airtable_base_id")
    airtable_table_id = inputs.get("airtable_table_id")
    fields = inputs.get("fields")
    api_key = inputs.get("airtable_api_key")

    # Validate inputs
    if not api_key:
        return {"error": "AIRTABLE_API_KEY is missing. Ensure it's set in Edurata Secrets."}
    if not airtable_base_id:
        return {"error": "airtable_base_id is missing."}
    if not airtable_table_id:
        return {"error": "airtable_table_id is missing."}
    if not fields or not isinstance(fields, dict):
        return {"error": "fields must be a dictionary with the data to insert."}

    # Construct Airtable API request
    url = f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": fields
    }

    # Send POST request to create new record
    response = requests.post(url, headers=headers, json=data)

    # Error handling
    if response.status_code == 401:
        return {"error": "Authentication failed. Check if the AIRTABLE_API_KEY is correct and has write permissions."}
    elif response.status_code == 403:
        return {"error": "Access denied. Ensure the API key has proper permissions to write to this table."}
    elif response.status_code != 200:
        return {"error": f"Airtable API error {response.status_code}: {response.text}"}

    return {"status": "success", "created_record": response.json()}
