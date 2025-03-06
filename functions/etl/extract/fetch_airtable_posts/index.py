import requests

def handler(inputs):
    # Fetch API Key from inputs
    api_key = inputs.get("airtable_api_key")
    if not api_key:
        return {"error": "AIRTABLE_API_KEY is missing. Ensure it is set in Edurata Secrets."}

    # Fetch Airtable Base & Table ID
    airtable_base_id = inputs.get("airtable_base_id")
    airtable_table_id = inputs.get("airtable_table_id")

    if not airtable_base_id:
        return {"error": "airtable_base_id is missing."}
    
    if not airtable_table_id:
        return {"error": "airtable_table_id is missing."}

    # Airtable API request
    url = f"https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # **Filter for missing OR explicitly FALSE `processed` values**
    params = {
        "filterByFormula": "OR(NOT({processed}), {processed} = FALSE())",
        "maxRecords": 10
    }

    # Send GET request
    response = requests.get(url, headers=headers, params=params)

    # Error Handling
    if response.status_code == 401:
        return {"error": "Authentication failed. Check if the AIRTABLE_API_KEY is correct and has read access."}
    elif response.status_code == 403:
        return {"error": "Access denied. Ensure the API key has proper permissions to read this table."}
    elif response.status_code != 200:
        return {"error": f"Airtable API error {response.status_code}: {response.text}"}

    # Extract records
    all_records = response.json().get("records", [])

    # **Filter out records missing required fields**
    filtered_records = []
    for record in all_records:
        fields = record.get("fields", {})
        github_repo_url = fields.get("githubRepoURL")
        workflow_path = fields.get("workflowPath")

        if github_repo_url and workflow_path:
            filtered_records.append(record)
        else:
            print(f"⚠️ Skipping record {record.get('id')} - Missing required fields.")

    # If no valid records found, return an empty array
    if not filtered_records:
        return {"message": "No valid unprocessed records found", "records": []}

    return {"records": filtered_records}
