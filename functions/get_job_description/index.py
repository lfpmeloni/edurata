import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")

def handler(inputs):
    notion_page_id = inputs.get("notion_page_id")
    url = f"https://api.notion.com/v1/blocks/{notion_page_id}/children"
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return {"error": f"Failed to fetch Notion page: {response.text}"}

    return {"job_description": response.json()}
