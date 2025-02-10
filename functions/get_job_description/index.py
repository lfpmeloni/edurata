import os
import requests

def handler(inputs):
    NOTION_API_KEY = inputs.get("notion_api_key")  # Get API Key from workflow inputs
    if not NOTION_API_KEY:
        return {"error": "NOTION_API_KEY is missing. Ensure it's set in Edurata Secrets."}

    notion_page_id = inputs.get("notion_page_id")
    if not notion_page_id:
        return {"error": "notion_page_id is required but was not provided."}

    url = f"https://api.notion.com/v1/blocks/{notion_page_id}/children"

    # DEBUG LOGGING: Print first 5 characters of the key (DO NOT PRINT FULL KEY)
    print(f"Loaded NOTION_API_KEY: {NOTION_API_KEY[:5]}********")

    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to fetch Notion page: {response.text}"}

    return {"job_description": response.json()}
