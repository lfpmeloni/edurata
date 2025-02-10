import requests

def handler(inputs):
    NOTION_API_KEY = inputs.get("notion_api_key")  # Get API Key from inputs
    if not NOTION_API_KEY:
        return {"error": "NOTION_API_KEY is missing. Ensure it's set in Edurata Secrets."}

    database_id = inputs.get("notion_database_id")
    if not database_id:
        return {"error": "notion_database_id is required but was not provided."}

    # Ensure required job details exist
    company_name = inputs.get("company_name", "Unknown")
    job_name = inputs.get("job_name", "Unknown")
    short_description = inputs.get("short_job_description", "No description provided.")
    iso_time = inputs.get("iso_time", None)

    data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Company Name": {"title": [{"text": {"content": company_name}}]},
            "Status": {"status": {"name": "Not applied"}},
            "Date": {"date": {"start": iso_time} if iso_time else None},
            "Job Name": {"rich_text": [{"text": {"content": job_name}}]},
            "Job Description": {"rich_text": [{"text": {"content": short_description}}]}
        }
    }

    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.notion.com/v1/pages", json=data, headers=headers)
    
    if response.status_code != 200:
        return {"error": f"Failed to create Notion card: {response.text}"}

    return {"notion_card": response.json()}