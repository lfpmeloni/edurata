import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")

def handler(inputs):
    notion_page_id = inputs.get("notion_page_id")
    url = f"https://api.notion.com/v1/blocks/{notion_page_id}/children"

    # DEBUG LOGGING: Print first 5 characters of the key (DO NOT PRINT FULL KEY)
    print(f"Loaded NOTION_API_KEY: {NOTION_API_KEY[:5]}********")

    if not NOTION_API_KEY:
        return {"error": "NOTION_API_KEY is missing. Please set it in Edurata Secrets."}

    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to fetch Notion page: {response.text}"}

    return {"job_description": response.json()}
